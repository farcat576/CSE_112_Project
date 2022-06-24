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
    return '00000'+reg[reg1]+reg[reg2]

def type_D(reg1,memory):
    return reg[reg1] + var_dict[memory]

def type_E(memory):
    return '000' + label_dict[memory]

def halt():
    return '0000000000'

def reg_check(register):
    return register in reg

def imm_check(imm):
    if imm.isdigit():
        return int(imm)>=0 and int(imm)<256
    else:
        return 0

def flags_check(register):
    return register == "FLAGS":

def A_check(line):
    if len(line) != 4:
        return 0
    return (line[1] in reg) and (line[2] in reg) and (line[3] in reg)


def B_check(line):
    if len(line) != 3:
        return 0
    return reg_check(line[1]) and imm_check(len[2])

def C_check(line):
    if len(line) != 3:
        return 0
    return reg_check(line[1]) and reg_check(line[2])

def D_check(line):
    if len(line) != 3:
        return 0
    return reg_check(line[1]) and (line[2] in var_dict)

def E_check(line):
    if len(line) != 2:
        return 0
    return reg_check(line[1])

def F_check(line):
    return line==["hlt"]

var_init = filter(lambda x: x[:-1]=='var ' and len(x.split())==2,data)
lim=len(data)
var_dict={var_init[i][4]:str(lim+i) for i in range(len(var_init))}

label_trav = [(data[i],i) for i in range(len(data)) if data[i][-1]==':' and len(data[i].split())==1]
label_init= [elem[0] for elem in label_trav]
label_dict={label_init[i][0][:-1]:str(label_init[i][1]) for i in range(len(label_trav))}

op_init = filter(lambda x: x.split()[0] in opcode,data)

err_init =filter(lambda x: (x not in var_init) and (x not in label_init) and (x not in label_init),data)
assert len(err_init) == 0

L=[]
for line in op_init:
    line = line.split()
    op = opcode[line[0]][0]
    type = opcode[line[0]][1]
    if op == "1001":
        assert len(line) == 3
        assert reg_check(line[1])
        if imm_check(line[2]):
            op += "0"
            type = "B"
            L.append(op +  type_B(line[1],line[2][1:]))
        if reg_check(line[2]) or flags_check(line[2]):
            op += "1"
            type = "C"
            L.append(op +  type_C(line[1],line[2]))
    else:
        if type == "A":
            assert A_check(line)
            L.append(op +  type_A(line[1],line[2],line[3]))
        elif type == "B":
            assert B_check(line)
            L.append(op +  type_B(line[1],line[2][1:]))
        elif type == "C":
            assert C_check(line)
            L.append(op +  type_C(line[1],line[2]))
        elif type == "D":
            assert D_check(line)
            L.append(op +  type_D(line[1],line[2]))
        elif type == "E":
            assert E_check(line)
            L.append(op +  type_E(line[1]))
        else:
            assert F_check(line)
            L.append(op +  halt())

with open('binary.txt' ,'w') as f:
    f.write(L)
#
#Check var and label again
#Fix binary string widths
#Mix all code together
#Change parameters of writing parts
#Handle asserts
