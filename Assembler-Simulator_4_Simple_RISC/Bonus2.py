import math

unit={'bit':1,'b':1,'nibble':4,'byte':8,'B':8,'k':10,'M':20,'G':30,'T':40,'P':50,'E':60,'Z':70,'Y':80}

qur=input("Type of query (type I/II/III): ")

if(qur=="type I"):
    number,unt=input("Enter memory space (with unit): ").split()
    typ_mem=input("Enter type of addressable memory: ").split()[0]
    instBITS=int(input("Enter length of instruction in bits: "))
    regBITS=int(input("Enter length of register in bits: "))

    if(len(unt)==1):
        addrBITS=int((unit[unt])+math.log(int(number),2))
    elif(len(unt)==2):
        addrBITS=int((unit[unt[0]]+math.log(unit[unt[1:]],2))+math.log(int(number),2))
    else:
        addrBITS=int(unit["word"]+math.log(int(number),2))

    opcodeBITS=instBITS-regBITS-addrBITS

    print("Minimum bits are needed to represent an address-> ", addrBITS)
    print("Number of bits needed by opcode-> ", opcodeBITS)
    print("Number of filler bits in Instruction type 2-> ",instBITS-opcodeBITS-2*(regBITS))
    print("Maximum numbers of instructions this ISA can support-> ",2**(opcodeBITS))
    print("Maximum number of registers this ISA can support-> ",2**(regBITS))


elif(qur=="type II"):

    mem_space=input("Enter memory space (with unit): ")

    system_enchancement=[0,0]

    system_enchancement[0]=input("Enter addresable memory of CPU: ").split()[0]

    word=int(input("Enter CPU supporting system (in bit): "))
    
    system_enchancement[1]=input("Enter enhanced addressable memory: ").split()[0]

    if(system_enchancement[0]=='word' and system_enchancement[1]=='word'):
        print(0)

    elif(system_enchancement[0]=='word'):
        print(int(math.log((word/unit[system_enchancement[1]]),2)))

    elif(system_enchancement[1]=='word'):
        print(int(math.log((unit[system_enchancement[0]]/word),2)))

    else:
        print(int(math.log((unit[system_enchancement[0]]/unit[system_enchancement[1]]),2)))
    
else:
    word=int(input("Enter CPU supporting system (in bit): "))
    addressPin=int(input("Enter number of address pins: "))
    typ_mem=input("Enter type of addressable memory: ").split()[0]

    if(typ_mem=="word"):
        ans_bit=2**(addressPin) * word
    
    else:
        ans_bit=2**(addressPin) * unit[typ_mem]

    ans_byte=ans_bit/8

    print("in Byte -> ",ans_byte)
    print("in GB   -> ",ans_byte/(2**(30)))