# -*- coding=utf-8 -*-

def printf(fmt: str, *args):
    print(fmt % args, end='')


def gets(s): # TODO
    s_in = input()
    for i, c in enumerate(s_in):
        s[i] = c
