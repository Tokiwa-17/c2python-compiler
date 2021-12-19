from cstdio import *
from cstring import *
def main():
    printf("Please input a string:")
    s = [None] * 100
    gets(s)
    len = strlen(s)
    mid = len / 2
    i = 0
    while i < len / 2:
        if s[i] != s[len-1 - i]:
            printf("Not a palindrome!")
            return 0
        i = i + 1
    printf("A palindrome!")
    return 0

if __name__ == '__main__':
    main()