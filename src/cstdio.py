# -*- coding=utf-8 -*-

def printf_0(fmt: str, *args):
    print(fmt % args, end='')


def gets_0(s): # TODO
    s_in = input()
    for i, c in enumerate(s_in):
        s[i] = c
