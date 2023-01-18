import operator
import sys
import math
from matplotlib import pyplot as plt

def yellow(str):return f"\033\033[0;33m{str}\033[0;0m"
def red(str):return f"\033\033[31;1m{str}\033[0;0m"
def blue(str):return f"\033\033[0;36m{str}\033[0;0m"

def fCheck(num):
    man=''
    temp=int(math.log(float(num),2))
    exp=f"{temp:03b}"
    fract=float(float(num)/2**(temp))-1

    if(int(exp,2)>7):
        return False

    count = 0
    while True:
        if(fract==0.0):
            man='00000'
            break
        fract *= 2
        l = str(fract).split('.')
        man += l[0]
        if count >= 5:
            return False
        if fract == 1.0: 
            break
        fract = float('0.'+l[1])
        count += 1

    return True

def deciConv(num):
    flt=f"{num:08b}"
    exp=flt[:3]
    value=2**(int(exp,2))

    man=flt[3:]
    val=0
    for i in range(5):
        val+=int(man[i])*(2**(-1-i))

    return (1+val)*value

def fltConv(num):
    man=''
    temp=int(math.log(float(num),2))
    exp=f"{temp:03b}"
    fract=float(float(num)/2**(temp))-1

    count = 0
    while True:
        if(fract==0.0):
            man='00000'
            break
        fract *= 2
        l = str(fract).split('.')
        man += l[0]

        if count >= 5:
           break

        if fract == 1.0: 
            break

        fract = float('0.'+l[1])
        count += 1

    n=len(man)
    for i in range(5-n):
        man+='0'
    return exp+man

def addf(a,b):
    global floatFLAG
    global FileReg
    num=deciConv(a)+deciConv(b)

    if(num>252):
        num=252
        old=FileReg['111']
        new=old[:12]+'1'+old[-3:]
        FileReg['111']=new


    if(not(fCheck(num))):
        print(f"{red('ERROR ->')} {yellow('Mantissa Overflown')} for {blue('<')} {blue(num)} {blue('>')}.\n\n")
        floatFLAG=True

    num=int(fltConv(num),2)    
    return num

def subf(a,b):
    global FileReg
    global floatFLAG
    num=deciConv(b)-deciConv(a)

    if(num<1):
        num=1
        old=FileReg['111']
        new=old[:12]+'1'+old[-3:]
        FileReg['111']=new

    if(not(fCheck(num))):
        print(f"{red('ERROR ->')} {yellow('Mantissa Overflown')} for {blue('<')} {blue(num)} {blue('>')}.\n\n")
        floatFLAG=True
    
    num=int(fltConv(num),2)
    return num

def movf(reg,value):
    return int(value,2) 

def readVar():
    global MEM;global vardict
    for entry in MEM:
        if entry[:5]=='10100' or entry[:5]=='10101':
            vardict[entry[-8:]]=0   

def ls(reg,pos):
    global FileReg
    return operator.lshift(FileReg[reg],int(pos,2))

def rs(reg,pos):
    global FileReg
    qaz=operator.rshift(FileReg[reg],int(pos,2))
    return qaz

def mov_I(reg,value):
    return int(value,2)

def mov_R(reg1,reg2):
    global FileReg
    if reg2!='111':FileReg[reg1]=FileReg[reg2]
    else:FileReg[reg1]=int(FileReg[reg2],2)

def div(reg1,reg2):
    global FileReg
    temp=FileReg[reg2]//FileReg[reg1]
    FileReg['000']=temp
    temp=FileReg[reg2]%FileReg[reg1]
    FileReg['001']=temp

def NOT(reg1,reg2):
    global FileReg
    temp=""
    for i in f"{FileReg[reg2]:016b}":
        if i=='1':temp+='0'
        else: temp+='1'
    FileReg[reg1]=int(temp,2)

def cmp(reg1,reg2):
    global FileReg
    setFlag('11110',reg2,reg1)

def ld(reg, value):
    global FileReg
    global operate
    global vardict
    FileReg[reg] = vardict[value]

def st(reg,value):
    global FileReg;global operate
    vardict[value]=FileReg[reg]

def jmp(value):
    global ProgCount;global chk
    ProgCount=value
    chk=1

def je(value):
    global operate;global ProgCount;global FileReg;global chk
    if(FileReg['111'][-1]=='1'):
        ProgCount=value
        chk=1

def jgt(value):
    global operate;global ProgCount;global FileReg;global chk
    if(FileReg['111'][-2]=='1'):
        ProgCount=value
        chk=1

def jlt(value):
    global operate;global ProgCount;global FileReg;global chk
    if(FileReg['111'][-3]=='1'):
        ProgCount=value
        chk=1

def setFlag(type,R1,R2=0,R3=0):
    global operate;global ProgCount;global FileReg
    if(type=='10000' or type=='10001' or type=='10110'):
        if(FileReg[R3]>65535):
            FileReg['111']='0000000000001000'
        elif(FileReg[R3]<0):
            FileReg['111']='0000000000001000'
        else:
            FileReg['111']='0000000000000000'
        return
    elif(type=='11110'):
        if(FileReg[R1]==FileReg[R2]):
            FileReg['111']='0000000000000001'        
        elif(FileReg[R1]>FileReg[R2]):
            FileReg['111']='0000000000000010' 
        elif(FileReg[R1]<FileReg[R2]):
            FileReg['111']='0000000000000100' 

operate={'A': {'10000': operator.add, '10001': operator.sub, '10110': operator.mul, '11010': operator.xor,
               '11011': operator.or_, '11100': operator.and_,'00000':addf,'00001':subf},
         'B': {'10010': mov_I, '11000':rs, '11001':ls,'00010':movf },
         'C': {'10011': mov_R, '10111': div, '11101': NOT, '11110': cmp},
         'D': {'10100': ld, '10101': st},
         'E': {'11111': jmp, '01100': jlt, '01101': jgt, '01111': je},
         }

FileReg={'000':0,'001':0,'010':0,'011':0,'100':0,'101':0,'110':0,'111':'0000000000000000'}

vardict = {}
MEM=[]
temp=''
count=0
chk=0
floatFLAG=False
dict_mem_acc={}
dict_mem_acc_2={}

for line in sys.stdin:
    if(line=="\n"):
             continue
    MEM.append(line.strip())

ProgCount='00000000'

readVar()

while(not(floatFLAG)):
    count+=1

    code=MEM[int(ProgCount,2)]
    temp=ProgCount
    dict_mem_acc[count]=(int(temp,2))

    if(code=='0101000000000000'):
        print(f"{ProgCount}",end=" ")
        FileReg['111']='0000000000000000'
        for reg in FileReg:
            if reg!='111':print(f"{int(FileReg[reg]):016b}",end=" ")
        else:print(f"{FileReg[reg]}",end=" ")
        print("\n",end="")
        break

    for letter in operate:
        if code[:5] in operate[letter]:
            break

    if(letter=="A"):
        FileReg['111']='0000000000000000'
        FileReg[code[-3:]]=operate[letter][code[:5]](FileReg[code[-6:-3]],FileReg[code[-9:-6]])

        setFlag(code[:5],code[-6:-3],code[-9:-6],code[-3:])
        FileReg[code[-3:]]=FileReg[code[-3:]]%65536

    elif(letter=="B"):
        FileReg['111']='0000000000000000'
        FileReg[code[-11:-8]]=operate[letter][code[:5]](code[-11:-8],code[-8:])

    elif(letter=="C"):
        operate[letter][code[:5]](code[-3:],code[-6:-3])
        if(code[:5]!='11110'):FileReg['111']='0000000000000000'
        
    elif(letter=="D"):
        FileReg['111']='0000000000000000'
        operate[letter][code[:5]](code[-11:-8], code[-8:])
        dict_mem_acc_2[count]=int(code[-8:],2)

    elif(letter=="E"):
        temp=ProgCount
        operate[letter][code[:5]](code[-8:])
        FileReg['111']='0000000000000000'
    
    
    print(f"{temp}",end=" ")
    
    for reg in FileReg:
        if reg!='111':print(f"{int(FileReg[reg]):016b}",end=" ")
        else:print(f"{FileReg[reg]}",end=" ")
    print("\n",end="")

    if(not(chk)):
        ProgCount=f"{(int(ProgCount,2)+1):08b}"
    chk=0    

l=[]
for addr in vardict:
    l.append(int(addr,2))
l.sort()

if(not(floatFLAG)):

    for i in MEM:
        print(i)

    for addr in l:
        new=f"{addr:08b}"
        print(f"{vardict[new]:016b}\n")

    for i in range(256-len(MEM)-len(vardict)):
        print('0000000000000000\n')

    plt.scatter(dict_mem_acc.keys(),dict_mem_acc.values(),color='b')
    plt.scatter(dict_mem_acc_2.keys(),dict_mem_acc_2.values(),color='b')
    plt.show()