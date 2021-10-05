from datetime import datetime

from django.db.models import F, Sum

from ppb.documents.formats import *


def compose_summary_of_release(releases, sheet, filters):
    headers = ['#', 'Servicing MFO', 'Unit', 'RRF Amount', 'Specific Purpose', 'RRF No.', 'Status', 'ASA No.',
               'ASA Amount']
    widths = [5, 12, 15, 15, 40, 15, 10, 15, 15]
    cols = len(headers)
    row = 0

    sheet.write_merge(row, row, 0, cols - 1, 'Summary of Releases', FONT_HEADER)
    row += 1
    for key, value in filters.items():
        sheet.write_merge(row, row, 0, 1, key.upper(), FONT_LABEL)
        sheet.write_merge(row, row, 2, len(headers) - 1, value, FONT_BODY_REG)
        row += 1

    writer = get_writer(sheet)

    row += 2
    for i, header in enumerate(headers):
        writer.write(row, i, header, is_highlighted=False, is_bold=True)
        sheet.col(i).width = 256 * widths[i]

    row += 1
    index = 1

    for item in releases:
        status_ = item.status if item.status else 'Unknown'
        writer.write(row, 1, item.servicing_mfo.name)
        writer.write(row, 2, item.unit.name)
        writer.write(row, 3, item.amount)
        writer.write(row, 4, item.specific_purpose)
        writer.write(row, 5, item.rrf_no)
        writer.write(row, 6, status_)

        from ppb.models import FundReleaseAsaItem
        asas = FundReleaseAsaItem.objects.filter(
            release_item=item.fund_release_item, asa__unit=item.unit).annotate(advice_no=F('asa__advice_no'))

        if not asas.exists():
            writer.write(row, 0, f'{index}')
            writer.write(row, 7, '-')
            writer.write(row, 8, 0)
            index += 1
            row += 1

        for asa in asas:
            writer.write(row, 0, f'{index}')
            writer.write(row, 7, asa.advice_no)
            writer.write(row, 8, asa.amount)
            index += 1
            row += 1


def compose_apb_monitor(budget, wb):
    now = datetime.today()
    for q, quarter in enumerate(['1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter'], start=1):
        sheet = wb.add_sheet(quarter)

        row = 0
        sheet.write_merge(row, row, 0, 8,
                          f'Annual Plan and Budget for {quarter}, FY {now.year} ({budget.description})', FONT_HEADER)
        row += 1
        sheet.write_merge(row, row, 0, 8, f'(Balance as of {now})', FONT_HEADER)

        row += 2
        sheet.write(row, 4, 'Programs/Activities/Projects', FONT_HEADER)
        sheet.write_merge(row, row, 5, 8, quarter, FONT_HEADER)

        row += 1
        headers = [('Date', 15),
                   ('RRF No.', 15),
                   ('Servicing Unit', 15),
                   ('Recipient Unit', 15),
                   ('By Expenditure Program', 30),
                   ('Programmed', 18),
                   ('Released', 18),
                   ('SDF for Approval', 18),
                   ('Balance', 18)]

        for i, (header, size) in enumerate(headers):
            sheet.col(i).width = size * 256
            sheet.write(row, i, header, FONT_HEADER)

        row += 1

        expenditure_program = None
        level2 = None
        level4 = None
        level6 = None

        from ppb.models import SuggestedPap
        suggested_paps = SuggestedPap.objects.filter(pk__in=budget.pawaf_items.filter(**{f'amount_q{q}__gt': 0}).values('suggested_pap'))

        for suggested_pap in suggested_paps.order_by('-sub_pap__major_pap__expenditure_program',
                                                     'sub_pap__major_pap__pa_sub_program',
                                                     'sub_pap__major_pap__name',
                                                     'name'):
            if (expenditure_program is None or
                    expenditure_program != suggested_pap.sub_pap.major_pap.get_expenditure_program_display()):
                expenditure_program = suggested_pap.sub_pap.major_pap.get_expenditure_program_display()
                sheet.write(row, 4, expenditure_program, FONT_LABEL)
                row += 1

            if (level2 is None or level2 != suggested_pap.sub_pap.major_pap.get_pa_sub_program_display()):
                level2 = suggested_pap.sub_pap.major_pap.get_pa_sub_program_display()
                sheet.write(row, 4, f'   - {level2}', FONT_LABEL)
                row += 1

            if (level4 is None or level4 != suggested_pap.sub_pap.major_pap.name):
                level4 = suggested_pap.sub_pap.major_pap.name
                sheet.write(row, 4, f'      - {level4}', FONT_LABEL)
                row += 1

            if (level6 is None or level6 != suggested_pap.name):
                level6 = suggested_pap.name
                sheet.write(row, 4, f'        - {level6}', FONT_LABEL)
                row += 1

            for item in budget.pawaf_items.filter(**{f'amount_q{q}__gt': 0, 'suggested_pap': suggested_pap}):
                sheet.write(row, 4, f'          {item.specific_pap}', FONT_BODY_REG)
                sheet.write(row, 5, getattr(item, f'amount_q{q}'), FONT_NUM_REG)
                row += 1


def compose_budget_summary(budget, budget_items, sheet):
    top_headers = ['Branch', 'End User', 'Major PAP', 'Specific PAP', 'Procurement', 'Object Code']
    sub_headers = ['Q1', 'Q2', 'Q3', 'Q4', 'Total'] * 3
    widths = [11, 15, 35, 35, 15, 15] + [17] * 15
    cols = len(widths)
    row = 0

    sheet.write_merge(row, row, 0, cols - 1, f'{budget.description} Budget Summary', FONT_HEADER)

    row += 2
    for i, header in enumerate(top_headers):
        sheet.write_merge(row, row + 1, i, i, header, FONT_LABEL)

    i = len(top_headers)
    sheet.write_merge(row, row, i, i + 4, 'Programmed Amount', FONT_HEADER)
    i += 5
    sheet.write_merge(row, row, i, i + 4, 'RRF Amount', FONT_HEADER)
    i += 5
    sheet.write_merge(row, row, i, i + 4, 'Available Balance', FONT_HEADER)

    row += 1
    for i, header in enumerate(sub_headers, start=len(top_headers)):
        sheet.write(row, i, header, FONT_HEADER)

    for i, width in enumerate(widths):
        sheet.col(i).width = 256 * width

    row += 1
    start_row = row + 1
    writer = get_writer(sheet)

    for item in budget_items:
        for breakdown in item.budget_breakdown.all():
            writer.write(row, 0, item.branch)
            writer.write(row, 1, item.branch)
            writer.write(row, 2, item.suggested_pap.sub_pap.major_pap.name)
            writer.write(row, 3, item.specific_pap)
            if breakdown.procurement_mode_id:
                writer.write(row, 4, breakdown.procurement_mode.name)
            else:
                writer.write(row, 4, 'None')

            writer.write(row, 5, breakdown.object_code.code)
            writer.write(row, 6, breakdown.amount_q1)
            writer.write(row, 7, breakdown.amount_q2)
            writer.write(row, 8, breakdown.amount_q3)
            writer.write(row, 9, breakdown.amount_q4)
            writer.write(row, 10, breakdown.amount, is_bold=True)

            # charged fields are property that aggregate values
            # minimize calls, call once and store to var
            charged_q1 = breakdown.charged_q1
            charged_q2 = breakdown.charged_q2
            charged_q3 = breakdown.charged_q3
            charged_q4 = breakdown.charged_q4
            charged_amount = round(charged_q1 + charged_q2 + charged_q3 + charged_q4, 2)

            writer.write(row, 11, charged_q1)
            writer.write(row, 12, charged_q2)
            writer.write(row, 13, charged_q3)
            writer.write(row, 14, charged_q4)
            writer.write(row, 15, charged_amount, is_bold=True)

            writer.write(row, 16, breakdown.amount_q1 - charged_q1)
            writer.write(row, 17, breakdown.amount_q2 - charged_q2)
            writer.write(row, 18, breakdown.amount_q3 - charged_q3)
            writer.write(row, 19, breakdown.amount_q4 - charged_q4)
            writer.write(row, 20, breakdown.amount - charged_amount, is_bold=True)

            row += 1

    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(6, 6 + 15):
        letter = letters[i]
        writer.write(row, i, xlwt.Formula(f'sum({letter}{start_row}:{letter}{row})'),
                     is_highlighted=False, is_bold=True)
