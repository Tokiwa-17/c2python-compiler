from cstdio import *
from cstring import *
text = [None] * 256

text2 = [None] * 5
text2[0] = 'a'
text2[1] = 'b'
text2[2] = 'c'

def main():
    global text
    global text2
    text[1] = '1'
    A = test()
    return 0

if __name__ == '__main__':
    main()