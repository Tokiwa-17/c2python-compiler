# -*- coding=utf-8 -*-

def printf(fmt: str, *args):
    print(fmt % args, end='')


def gets(s): # TODO
    s_in = input()
    for i, c in enumerate(s_in):
        s[i] = c

def atof(s):
    if isinstance(s, str):
        try:
            s = float(s)
            return s
        except:
            raise Exception('The format of str is incorrect.')
    else:
        mstr = ''
        for i in s:
            if i is None:
                break
            mstr += i
        return float(mstr)