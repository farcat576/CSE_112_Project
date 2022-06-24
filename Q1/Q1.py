with open("q1testcase.txt",'r') as f:
    data = f.readlines()
    commands = [data[i].strip() for i in range(len(data))]
    print(data)
    print(commands)

#assertion statements for hlt and length of input file
assert commands[len(commands) - 1] == "hlt","Last command is not hlt"
assert len(commands) <= 256, "Too many instructions!"

#assertion statements for each instruction
#mov + last bit later
opcode = {"add":["10000",'A'], "sub":["10001","A"], "mov":["1001",""], "ld":["10100","D"],
        "st":["10101","D"],"mul":["10110","A"],"div":["10111","C"],"rs":["11000","B"],
        "ls":["11001","B"],"xor":["11010","A"],"or":["11011","A"],"and":["11100","A"],
        "not":["11101","C"],"cmp":["11110","C"],"jmp":["11111","E"],"jlt":["01100","E"],
        "jgt":["01101","E"],"je":["01111","E"],"hlt":["01010","F"]}

reg={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}

def type_A(reg1,reg2,reg3):
    return '00'+reg[reg1]+reg[reg2]+reg[reg3]

def type_B(reg1,imm):
    return reg[reg1]+bin(int(imm))[2:]

def type_C(reg1,reg2):
    return '00000'+reg[reg1]+reg[2]

def type_D(reg1,memory):
    return reg[reg1] + bin(memory)[2:]

def type_E(reg1,memory):
    return reg[reg1] + bin(memory)[2:]

def halt():
    return '010100000000000'

def reg_check(register):
    if register in reg:
        return 1
    else:
        return 0

def imm_check(imm):
    if imm>=0 and imm<256 and imm.isdigit():
        return 1
    else:
        return 0

def flags_check(register):
    if register == "FLAGS":
        return 1
    else:
        return 0

def type_A(line):
    if len(line) != 4:
        return 0
    for i in line[1:]:
        if i not in valid_registers:
            return 0
    return 1


def type_B(line):
    if len(line) != 3:
        return 0
    if line[1] not in valid_registers:
        return 0
    if int(line[2][1:]) > 256:
        return 0

    return 1

def type_C(line):
    if len(line) != 3:
        return 0
    for i in line[1:]:
        if i not in valid_registers:
            return 0
    return 1


def type_F(line):
    if len(line) != 1:
        return 0
    return 1

var_init = filter(lambda x: x[:3]=='var' and len(x.split())==2,data)
lim=len(data)
var_dict={var_init[i][4]:str(lim+i) for i in range(len(var_init))}

label_init = [(data[i],i) for i in range(len(data)) if data[i][-1]==':' and len(data[i].split())==1 ]
label_dict={label_init[i][0][:-1]:str(label_init[i][1]) for i in range(len(var_init))}

L=[]
for line in data:
    line = line.split()
    if line[0] in opcode:
        op = opcode[line[0]][0]
        type = opcode[line[0]][1]
        if op == "1001":
            assert len(line) == 3
            assert reg_check(line[1])
            if imm_check(line[2]):
                op += "0"
                type = "B"
            if reg_check(line[2]) or flags_check(line[2]):
                op += "1"
                type = "C"
        else:
            if type == "A":
                assert check_A(line)
            elif type == "B":
                assert check_B(line)
            elif type == "C":
                assert check_C(line)
            elif type == "D":
                assert check_D(line)
            elif type == "E":
                assert check_E(line)
            else:
                assert check_F(line)
        if type == "A":
            L.append(op +  type_A(line))
        elif type == "B":
            L.append(op +  type_B(line))
        elif type == "C":
            L.append(op +  type_C(line))
        elif type == "D":
            L.append(op +  type_D(line))
        elif type == "E":
            L.append(op +  type_E(line))
        else:
            L.append(op +  halt())
with open('binary.txt' ,'w') as f:
    f.write(L)
#
#Check var and label again
#Fix binary string widths
#Mix all code together
#Change parameters of writing parts
#Handle asserts
