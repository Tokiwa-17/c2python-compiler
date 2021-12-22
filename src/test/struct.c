#include <stdio.h>
#include "a.h"
// 结构体定义 + 变量声明
struct foo
{
    char a[10];
} a, b;

// 结构体定义中嵌套结构体
struct bar{
    int x;
    struct foo y;
};

// 结构体数组声明
struct bar c[10];

int main()
{
    // 结构体变量声明
    struct foo q;

    // 结构体成员变量赋值等
    q.a[0] = 'c';
    c[9].y.a[0] = 'd';
    printf("%s", c[9].y.a);
    return 0;
}