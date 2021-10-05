from uuid import uuid4
import os
import datetime

from django.utils.deconstruct import deconstructible
from django.db.models import Func
import django_filters


class Round(Func):
  function = 'ROUND'
  template = "%(function)s(%(expressions)s::numeric, 2)"


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        now = datetime.datetime.now()
        self.path = sub_path.replace('%Y', f'{now.year}').replace('%m', f'{now.month:02}')

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]

        # set filename as random string
        filename = f'{uuid4().hex}.{ext}'

        # return the whole path to the file
        return os.path.join(self.path, filename)


ones = ["", "one ", "two ", "three ", "four ", "five ", "six ", "seven ", "eight ", "nine ", "ten ", "eleven ",
        "twelve ", "thirteen ", "fourteen ", "fifteen ", "sixteen ", "seventeen ", "eighteen ", "nineteen "]

twenties = ["", "", "twenty ", "thirty ", "forty ", "fifty ", "sixty ", "seventy ", "eighty ", "ninety "]

thousands = ["", "thousand ", "million ", "billion ", "trillion "]


def num999(n):
    c = n % 10  # singles digit
    b = int(((n % 100) - c) / 10)  # tens digit
    a = int(((n % 1000) - (b * 10) - c) / 100)  # hundreds digit
    t = ""
    h = ""
    if a != 0:
        t = ones[a] + "hundred "
    if b <= 1:
        h = ones[n % 100]
    elif b > 1:
        h = twenties[b] + ones[c]
    st = t + h
    return st


def numbig(num):
    if num == 0:
        return 'zero'
    i = 3
    n = str(num)
    word = ""
    k = 0
    while i == 3:
        nw = n[-i:]
        n = n[:-i]
        if int(nw) == 0:
            word = num999(int(nw)) + thousands[int(nw)] + word
        else:
            word = num999(int(nw)) + thousands[k] + word
        if n == '':
            i = i+1
        k += 1
    return word[:-1]


def num2eng(amount):
    whole = int(amount)
    dec = int(round((amount - whole) * 100, 2))

    words = numbig(whole) + ' pesos '

    if dec:
        words += f'and {dec}/100'

    return words.title()


class InListFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value not in (None, ''):
            fieldname_list = value.split(',')
            return qs.filter(**{'{0}__{1}'.format(
                self.field_name, self.lookup_expr): fieldname_list})
        return super().filter(qs, value)


def quarter_formatting(q1, q2, q3, q4):
    qs = [q1, q2, q3, q4]
    word = ['1st', '2nd', '3rd', '4th']
    suffix = 'Qtr'

    num_q = sum(qs)

    if num_q == 1:
        index = qs.index(True)
        return f'{word[index]} {suffix}'
    elif num_q == 2:
        first = qs.index(True)
        second = qs.index(True, min(first + 1, len(qs) - 1))

        return f'{word[first]} and {word[second]} {suffix}'
    elif num_q == 3:
        first = qs.index(True)
        second = qs.index(True, min(first + 1, len(qs) - 1))
        third = qs.index(True, min(second + 1, len(qs) - 1))

        if (first + 1 == second) and (second + 1 == third):  # consecutive
            return f'{word[first]} to {word[third]} {suffix}'
        else:  # non-consecutive
            return f'{word[first]}, {word[second]}, and {word[third]} {suffix}'

    elif num_q == 4:
        return f'{word[0]}-{word[-1]} {suffix}'

    return ''
