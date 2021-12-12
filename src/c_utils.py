import os

#c_utils = [strlen_py, gets_py, printf_py, system_py]

# system in C
system_py = '''
def system_0(s):
    if not isinstance(s, tr):
        raise SyntaxError
    os.system(s)
'''

# gets in C
gets_py = '''

'''

# printf in C
printf_py = '''

'''

# strlen in C
strlen_py = '''
def strlen_0(s):
    if isinstance(s, str):
        return len(s)
    else:
        _len = 0
        for i in s:
            if i is None:
                break
            _len += 1
        return _len

'''