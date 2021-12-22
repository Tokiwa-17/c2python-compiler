# -*- coding=utf-8 -*-

def strlen(s):
    if isinstance(s, str):
        return len(s)
    else:
        return s.index(None)
