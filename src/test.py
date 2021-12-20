from cstdio import *
from cstring import *
<<<<<<< HEAD
text = [None] * 256

text2 = [None] * 5
text2[0] = 'a'
text2[1] = 'b'
text2[2] = 'c'

def main():
    global text
    global text2
=======
text2 = [None] * 5
text2[0] = 'a'
text2[1] = 'b'
text2[2] = 'c'

a = 0

def main():
    global text2
    global a
>>>>>>> c1de9a8f077359fc7515d85eefc9aef58de5c3c4
    text[1] = '1'
    A = test()
    return 0

if __name__ == '__main__':
    main()