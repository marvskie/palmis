import xlwt

from django.db.models import *

from ppb import consts
from ppb.models import *
from ppb.documents.formats import *


def compose_fund_monitoring(wb: xlwt.Workbook, budget_record: Pawaf, activity: PawafItem, branch: str):
    budget_description = budget_record.description.replace('FY 2020', '').strip().upper()
    budget_items = budget_record.pawaf_items.exclude(chargeability_distribution__isnull=True).order_by('id')

    if activity:
        budget_items = budget_items.filter(pk=activity.pk)

    if branch:
        budget_items = budget_items.filter(branch__iexact=branch)
    else:
        summary_sheet = wb.add_sheet(budget_description)

    sheets = {}
    headers = ['Specific PAPs (7L)', 'RRF No.', 'Specific Purpose /Activity', 'Servicing Unit', 'Programmed Amount',
               'RRF Amount', 'Available Balance']
    widths = [30, 18, 30, 18, 22, 22, 22]
    items = set()

    for i in range(4):
        sheet = wb.add_sheet(f'{budget_description}-{i + 1}')
        row = 0
        for j in range(len(headers)):
            sheet.write(row, j, headers[j], FONT_LABEL)
            sheet.col(j).width = 256 * widths[j]
        row += 1

        sheets[f'q{i + 1}'] = {'sheet': sheet, 'row': row}

    for budget_item in budget_items:
        dist = budget_item.parsed_distribution
        specific_pap = budget_item.specific_pap
        done_paps = set()
        for fund_release, release_items in dist.items():
            if branch and fund_release.cmd:
                continue
            done_releases = set()
            for release_item, mfos in release_items.items():
                done_activities = set()
                for mfo, quarters in mfos.items():
                    for quarter, charged in quarters.items():
                        amount = getattr(budget_item, f'amount_{quarter}', 0.)
                        total_quarter_charged = getattr(budget_item, f'charged_{quarter}', 0.)
                        sheet = sheets[quarter]['sheet']
                        row = sheets[quarter]['row']

                        if total_quarter_charged > 0:
                            pap_q = f'{budget_item.id}_{quarter}'
                            if pap_q not in done_paps:
                                sheet.write_merge(row, row, 0, 3, specific_pap, FONT_LABEL_W_BG)
                                numeric_writer2(sheet, row, 4, amount, shortcut='highlight1')
                                numeric_writer2(sheet, row, 5, total_quarter_charged, shortcut='highlight1')
                                numeric_writer2(sheet, row, 6, amount - total_quarter_charged, shortcut='highlight1')
                                items.add(budget_item)
                                row += 1
                                done_paps.add(pap_q)

                        if charged > 0:
                            rrf_q = f'{fund_release.id}_{quarter}'

                            if rrf_q not in done_releases:
                                sheet.write(row, 1, fund_release.rrf_no, FONT_BODY_REG)
                                done_releases.add(rrf_q)

                            activity_q = f'{release_item.specific_purpose}_{quarter}'
                            if activity_q not in done_activities:
                                sheet.write(row, 2, release_item.specific_purpose, FONT_BODY_REG)
                                done_activities.add(activity_q)

                            sheet.write(row, 3, mfo.name, FONT_BODY_REG)
                            numeric_writer2(sheet, row, 5, charged)
                            row += 1

                        sheets[quarter]['row'] = row

    if branch is None:
        _compose_utilization_summary_sheet(summary_sheet, items)


def _compose_utilization_summary_sheet(sheet, budget_items):
    headers = ['Specific PAPs (7L)', 'RRF No.', 'Specific Purpose /Activity', 'ASA No.',
               'Released Amount', 'Unreleased Balance', 'Programmed Amount', 'Available Balance']
    widths = [35, 18, 35, 18, 22, 22, 22, 22]

    row = 0

    for j in range(len(headers)):
        sheet.write(row, j, headers[j], FONT_LABEL)
        sheet.col(j).width = 256 * widths[j]
    row += 1

    for budget_item in budget_items:
        sheet.write_merge(row, row, 0, 3, budget_item.specific_pap, FONT_LABEL_W_BG)
        numeric_writer2(sheet, row, 6, budget_item.amount, shortcut='highlight1')
        numeric_writer2(sheet, row, 7, budget_item.amount - budget_item.charged_amount, shortcut='highlight1')

        released_amount = 0.0
        top_row = row
        row += 1

        dist = budget_item.parsed_distribution
        for fund_release, release_items in dist.items():
            sheet.write(row, 1, fund_release.rrf_no, FONT_BODY_REG)
            for release_item in release_items.keys():
                sheet.write(row, 2, release_item.specific_purpose, FONT_LABEL_W_BG2)
                sheet.write(row, 3, '', FONT_LABEL_W_BG2)
                numeric_writer2(sheet, row, 4, release_item.released, shortcut='highlight2')
                numeric_writer2(sheet, row, 5, release_item.balance, shortcut='highlight2')
                row += 1

                asa_items = release_item.asa_items.all()
                for asa_item in asa_items:
                    sheet.write(row, 3, asa_item.asa.advice_no, FONT_BODY_REG)
                    numeric_writer2(sheet, row, 4, asa_item.amount)
                    released_amount += asa_item.amount
                    row += 1

        numeric_writer2(sheet, top_row, 4, released_amount, shortcut='highlight1')
        numeric_writer2(sheet, top_row, 5, budget_item.charged_amount - released_amount, shortcut='highlight1')
