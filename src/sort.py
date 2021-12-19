from cstdio import *
from cstring import *
def main():
    array = [None] * 12
    array[0] = 14
    array[1] = 10
    array[2] = 18
    array[3] = 16
    array[4] = 20
    array[5] = 26
    array[6] = 23
    array[7] = 29
    array[8] = 26
    array[9] = 35
    array[10] = 32
    array[11] = 37
    insertSort(array, 0, 11)
    i = 0
    while i < 12:
        printf("%d ", array[i])
        i  =  i + 1
    return 0

def insertSort(data, l, r):
    auxiliary = 0
    i = l + 1
    while i <= r:
        if data[i] < data[i-1]:
            auxiliary = data[i]
            j = i-1
            while j >= l and data[j] > auxiliary:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = auxiliary
        i = i + 1

if __name__ == '__main__':
    main()