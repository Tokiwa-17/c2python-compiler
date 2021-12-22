from cstdio import *
from cstring import *
class foo:
    a=[None]*10
a=foo()
b=foo()

class bar:
    x = None
    y=foo()

c=[bar() for i in range(10)]

def main():
    global a
    global b
    global c
    q=foo()
    q.a[0]='c'
    c[9].y.a[0]='d'
    printf("%s",c[9].y.a)
    return 0

if __name__ == '__main__':
    main()