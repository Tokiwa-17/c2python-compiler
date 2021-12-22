from cstdio import *
from cstring import *
class Unit:
    flag = None
    op = None
    num = None

check_flag=0

def main():
    global check_flag
    Evaluate()
    return 0

def Evaluate():
    global check_flag
    Input_array=[None]*100
    Unit_arry=[Unit() for i in range(100)]
    printf("Please enter an expression(without blank symbol):\n")
    gets(Input_array)
    check_flag=Check(Input_array)
    if check_flag:
        printf("Format error!\n")
    else:
        Unit_len=Convert(Unit_arry,Input_array)
        ans=Calculate(Unit_arry,Unit_len)
        if check_flag:
            printf("The answer is %lf\n",ans)
        else:
            printf("Format error!\n")

def Calculate(Unit_arry,Unit_len):
    global check_flag
    i = None
    Num_pointer=0
    Op_pointer=0
    Num_stack=[None]*100
    Num_stack[0]=0
    Op_stack=[None]*100
    Op_stack[0]=0
    i=0
    while i<Unit_len:
        if Unit_arry[i].flag!=-1:
            if Unit_arry[i].flag:
                Num_stack[Num_pointer]=Unit_arry[i].num
                Num_pointer=Num_pointer+1
            else:
                if Op_pointer==0 or Unit_arry[i].op=='(':
                    Op_stack[Op_pointer]=Unit_arry[i].op
                    Op_pointer=Op_pointer+1
                else:
                    if Unit_arry[i].op==')':
                        Op_pointer=Op_pointer-1
                        Num_pointer=Num_pointer-1
                        while Op_stack[Op_pointer]!='(' and Op_pointer!=0:
                            Num_stack[Num_pointer-1]=Compute(Num_stack[Num_pointer-1],Num_stack[Num_pointer],Op_stack[Op_pointer])
                            Op_pointer=Op_pointer-1
                            Num_pointer=Num_pointer-1
                        Num_pointer=Num_pointer+1
                    else:
                        if Compare(Unit_arry[i].op,Op_stack[Op_pointer-1]):
                            Op_stack[Op_pointer]=Unit_arry[i].op
                            Op_pointer=Op_pointer+1
                        else:
                            Op_pointer=Op_pointer-1
                            Num_pointer=Num_pointer-1
                            while Compare(Unit_arry[i].op,Op_stack[Op_pointer])==0 and Op_pointer!=-1:
                                Num_stack[Num_pointer-1]=Compute(Num_stack[Num_pointer-1],Num_stack[Num_pointer],Op_stack[Op_pointer])
                                Op_pointer=Op_pointer-1
                                Num_pointer=Num_pointer-1
                            Op_pointer=Op_pointer+1
                            Num_pointer=Num_pointer+1
                            Op_stack[Op_pointer]=Unit_arry[i].op
                            Op_pointer=Op_pointer+1
        i=i+1
    Op_pointer=Op_pointer-1
    Num_pointer=Num_pointer-1
    while Op_pointer!=-1:
        Num_stack[Num_pointer-1]=Compute(Num_stack[Num_pointer-1],Num_stack[Num_pointer],Op_stack[Op_pointer])
        Op_pointer=Op_pointer-1
        Num_pointer=Num_pointer-1
    if Op_pointer==-1 and Num_pointer==0:
        check_flag=1
    return Num_stack[0]

def Compute(x,y,op):
    global check_flag
    if op=='+':
        return x+y
    if op=='-':
        return x-y
    if op=='*':
        return x*y
    if op=='/':
        return x/y

def Compare(op1,op2):
    global check_flag
    list=[None]*6
    list[0]="("
    list[1]="+"
    list[2]="-"
    list[3]="*"
    list[4]="/"
    map=[None]*25
    map[0]=1
    map[1]=0
    map[2]=0
    map[3]=0
    map[4]=0
    map[5]=1
    map[6]=0
    map[7]=0
    map[8]=0
    map[9]=0
    map[10]=1
    map[11]=0
    map[12]=0
    map[13]=0
    map[14]=0
    map[15]=1
    map[16]=1
    map[17]=1
    map[18]=0
    map[19]=0
    map[20]=1
    map[21]=1
    map[22]=1
    map[23]=0
    map[24]=0
    i = None
    j = None
    i=0
    while i<5:
        if op1==list[i]:
            break
        i=i+1
    j=0
    while j<5:
        if op2==list[j]:
            break
        j=j+1
    return map[i*5+j]

def Convert(Unit_arry,Input_array):
    global check_flag
    len=strlen(Input_array)
    i = None
    Unit_len=0
    i=0
    while i<len:
        if Isop(Input_array[i]):
            Unit_arry[Unit_len].flag=0
            Unit_arry[Unit_len].op=Input_array[i]
            Unit_len=Unit_len+1
        else:
            Unit_arry[Unit_len].flag=1
            temp=[None]*100
            k=0
            
            while isnumber(Input_array[i]) or Input_array[i]=='.':
                temp[k]=Input_array[i]
                k=k+1
                i=i+1
            i=i-1
            Unit_arry[Unit_len].num=atof(temp)
            if Unit_len==1 and Unit_arry[Unit_len-1].flag==0 and Unit_arry[Unit_len-1].op=='-':
                Unit_arry[Unit_len-1].flag=-1
                Unit_arry[Unit_len].num*=-1
            if Unit_len>=2 and Unit_arry[Unit_len-1].flag==0 and Unit_arry[Unit_len-1].op=='-' and Unit_arry[Unit_len-2].flag==0 and Unit_arry[Unit_len-2].op!=')':
                Unit_arry[Unit_len-1].flag=-1
                Unit_arry[Unit_len].num*=-1
            if Unit_len==1 and Unit_arry[Unit_len-1].flag==0 and Unit_arry[Unit_len-1].op=='+':
                Unit_arry[Unit_len-1].flag=-1
            if Unit_len>=2 and Unit_arry[Unit_len-1].flag==0 and Unit_arry[Unit_len-1].op=='+' and Unit_arry[Unit_len-2].flag==0 and Unit_arry[Unit_len-2].op!=')':
                Unit_arry[Unit_len-1].flag=-1
            Unit_len=Unit_len+1
        i=i+1
    return Unit_len

def Check(Input_array):
    global check_flag
    len=strlen(Input_array)
    i = None
    i=0
    while i<len:
        if  not Isop(Input_array[i]) and Input_array[i]!='.' and  not isnumber(Input_array[i]):
            return 1
        if isnumber(Input_array[i]):
            num_len=0
            Cur_positoin=i+1
            while isnumber(Input_array[Cur_positoin]) or Input_array[Cur_positoin]=='.':
                num_len=num_len+1
                Cur_positoin=Cur_positoin+1
            if num_len>=16:
                return 1
        i=i+1
    return 0

def Isop(ch):
    global check_flag
    if ch=='+' or ch=='-' or ch=='*' or ch=='/' or ch=='(' or ch==')' or ch=='=':
        return 1
    return 0

def isnumber(x):
    global check_flag
    if x=='0' or x=='1' or x=='2' or x=='3' or x=='4' or x=='5' or x=='6' or x=='7' or x=='8' or x=='9':
        return True
    else:
        return False

if __name__ == '__main__':
    main()