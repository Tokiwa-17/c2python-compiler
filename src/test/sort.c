#include <stdio.h>

void insertSort(int data[], int l, int r) {
    int auxiliary = 0;
    for (int i = l+1; i <= r; i++) {
        if (data[i] < data[i - 1]) {
	    auxiliary = data[i];
            int j = i - 1;
            while (j >= l && data[j] > auxiliary) {
                data[j + 1] = data[j];
                j -= 1;
            }
            data[j + 1] = auxiliary;
        }
    }
}
int main(){
    int array[12] = { 14, 10, 18, 16, 20, 26, 23, 29, 26, 35, 32, 37 };
    insertSort(array, 0,11);
    for (int i = 0; i < 12; ++i) printf("%d ", array[i]);
    return 0;
}
