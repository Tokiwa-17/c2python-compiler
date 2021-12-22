from cstdio import *
from cstring import *
text=[None]*256

pattern=[None]*256

next=[None]*1024

def main():
    global text
    global pattern
    global next
    printf("Please enter the text:\n")
    gets(text)
    printf("\nPlease enter the pattern:\n")
    gets(pattern)
    getNext()
    start=0
    flag=0
    pos = None
    tLen=strlen(text)
    while start<tLen:
        pos=kmp(start)
        if pos!=-1:
            printf("A match occurs at %d\n",pos+1)
            start=pos+1
            flag=1
        else:
            break
    if  not flag:
        printf("No match.")
    printf("\n")
    return 0

def kmp(start):
    global text
    global pattern
    global next
    pLen=strlen(pattern)
    tLen=strlen(text)
    i=start
    j=0
    while i<tLen and j<pLen:
        if j==-1 or text[i]==pattern[j]:
            i = i+1
            j = j+1
        else:
            j=next[j]
    if j==pLen:
        return i-j
    else:
        return -1

def getNext():
    global text
    global pattern
    global next
    pLen=strlen(pattern)
    next[0]=-1
    i=0
    j=-1
    while i<pLen-1:
        if j==-1 or pattern[i]==pattern[j]:
            i=i+1
            j=j+1
            if pattern[i]==pattern[j]:
                next[i]=next[j]
            else:
                next[i]=j
        else:
            j=next[j]

if __name__ == '__main__':
    main()