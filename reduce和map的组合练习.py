# -*- coding: utf-8 -*-
from functools import reduce


def str2float(s):  # s='123.45'

    digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

    def char2num(c):  # 将字符串数字转成数字
        return digits[c]

    def fn(x, y):  # 处理数字的乘积(包括小数点前和小数点后)
        return x * 10 + y

    intNum, floatNum = s.split('.')  # 将一个浮点数分成整数部分和小数部分

    intNum = reduce(fn, map(char2num, intNum))  # 处理整数的乘积
    # 小数部分的处理,例如0.45-->'45'-->45-->45*  10**(-len(小数部分的位数))
    floatNum = 10 ** (-len(floatNum)) * reduce(fn, map(char2num, floatNum))
    return intNum + floatNum


str2float('0.45')