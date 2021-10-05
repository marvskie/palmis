import xlwt


FONT_HEADER = xlwt.easyxf('align: vert centre, horiz centre, wrap on; font: bold on')
FONT_LABEL = xlwt.easyxf('align: vert centre, wrap on; font: bold on')
FONT_LABEL_W_BG = xlwt.easyxf('align: vert centre, wrap on; font: bold on; pattern: pattern solid, fore_colour light_orange')
FONT_LABEL_W_BG2 = xlwt.easyxf('align: vert centre, wrap on; pattern: pattern solid, fore_colour yellow')
FONT_BODY_REG = xlwt.easyxf('align: vert centre, wrap on')
FONT_BODY_NEG = xlwt.easyxf('font: color-index red; align: wrap on', num_format_str='#,##0.00')

FONT_NUM_REG = xlwt.easyxf('align: vert centre', num_format_str='_(#,##0.00_);[Red](#,##0.00)')
FONT_NUM_REG_TOTAL = xlwt.easyxf('align: vert centre; font: bold on', num_format_str='_(#,##0.00_);[Red](#,##0.00)')
FONT_NUM_REG_TOTAL_W_BG = xlwt.easyxf(
    'align: vert centre; font: bold on; pattern: pattern solid, fore_colour light_orange', num_format_str='#,##0.00')
FONT_NUM_REG_TOTAL_W_BG2 = xlwt.easyxf('align: vert centre; pattern: pattern solid, fore_colour yellow',
                                       num_format_str='_(#,##0.00_);[Red](#,##0.00)')


def numeric_writer2(sheet, row, col, value, shortcut=None):
    fmt = FONT_NUM_REG

    if shortcut == 'total':
        fmt = FONT_NUM_REG_TOTAL
    elif shortcut == 'highlight1':
        fmt = FONT_NUM_REG_TOTAL_W_BG
    elif shortcut == 'highlight2':
        fmt = FONT_NUM_REG_TOTAL_W_BG2

    return sheet.write(row, col, value, fmt)


class DynamicHighlighting:
    highlight = ' pattern: pattern solid, fore_colour gray25'

    def __init__(self, sheet, with_highlighting=True):
        self.sheet = sheet
        self.with_highlighting = with_highlighting
        num_format_str = '_(#,##0.00_);[Red](#,##0.00)'

        format_str = 'align: vert centre, wrap on'
        self.format_str = xlwt.easyxf(format_str)
        self.format_str_highlighted = xlwt.easyxf(f'{format_str}; {self.highlight}')
        self.format_num = xlwt.easyxf(format_str, num_format_str=num_format_str)
        self.format_num_highlighted = xlwt.easyxf(f'{format_str}; {self.highlight}', num_format_str=num_format_str)

        format_str = 'align: vert centre, wrap on; font: bold on'
        self.format_str_b = xlwt.easyxf(format_str)
        self.format_str_highlighted_b = xlwt.easyxf(f'{format_str}; {self.highlight}')
        self.format_num_b = xlwt.easyxf(format_str, num_format_str=num_format_str)
        self.format_num_highlighted_b = xlwt.easyxf(f'{format_str}; {self.highlight}', num_format_str=num_format_str)

    def get_format(self, is_highlighted, is_num=False, is_bold=False):
        if is_num:
            if is_highlighted and is_bold:
                return self.format_num_highlighted_b
            elif is_highlighted and not is_bold:
                return self.format_num_highlighted
            elif not is_highlighted and is_bold:
                return self.format_num_b
            return self.format_num

        if is_highlighted and is_bold:
            return self.format_str_highlighted_b
        elif is_highlighted and not is_bold:
            return self.format_str_highlighted
        elif not is_highlighted and is_bold:
            return self.format_str_b
        return self.format_str

    def write(self,  row, col, val, is_bold=False, is_highlighted=None):
        is_num = not isinstance(val, str) or isinstance(val, xlwt.Formula)

        if is_highlighted is None:
            is_highlighted = (row % 2 == 0) and self.with_highlighting

        self.sheet.write(row, col, val, self.get_format(is_highlighted, is_num=is_num, is_bold=is_bold))

    def write_merge(self, row_1, row_2, col_1, col_2, val, is_bold=False, is_highlighted=None):
        is_num = not isinstance(val, str) or isinstance(val, xlwt.Formula)

        if is_highlighted is None:
            is_highlighted = (row_1 % 2 == 0) and self.with_highlighting

        self.sheet.write(
            row_1, row_2, col_1, col_2, val, self.get_format(is_highlighted, is_num=is_num, is_bold=is_bold))


def get_writer(sheet):
    obj = DynamicHighlighting(sheet)
    return obj
