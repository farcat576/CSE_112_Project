with open("q1testcase.txt", 'r') as f:
    data = f.readlines()
    commands = [data[i].strip() for i in range(len(data))]

# assertion statements for hlt and length of input file
assert commands.index("hlt")==len(commands) - 1, "Last command is not hlt"
assert len(commands) <= 256, "Too many instructions!"

# assertion statements for each instruction
# mov + last bit later

# Opcode mapping
opcode = {"add": ["10000", 'A'], "sub": ["10001", "A"], "mov": ["1001", ""], "ld": ["10100", "D"],
          "st": ["10101", "D"], "mul": ["10110", "A"], "div": ["10111", "C"], "rs": ["11000", "B"],
          "ls": ["11001", "B"], "xor": ["11010", "A"], "or": ["11011", "A"], "and": ["11100", "A"],
          "not": ["11101", "C"], "cmp": ["11110", "C"], "jmp": ["11111", "E"], "jlt": ["01100", "E"],
          "jgt": ["01101", "E"], "je": ["01111", "E"], "hlt": ["01010", "F"]}

error_dict = {"101":"More than one hlt statement found.","102":"Last instruction is not hlt.",
              "103":"Too many instructions given.","201":"Register not found",
              "202":"Immediate value format not recognised","203":"Illegal use of FLAGS register detected.",
              "204":"Syntax Error.","301":"Variable not defined",
              "302":"Variable not defined at the beginning","303":"Label not found.",
              "304":"Syntax error in use of variable.","305":"Syntax error in use of label.",
              "306":"Variable used as label.","307":"Label used as variable."
              }
error_message = " Assembling halted."


# Register mapping
reg = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110', 'FLAGS': '111'}


# Conversion functions for each type
def type_A(reg1, reg2, reg3):
    return '00' + reg[reg1] + reg[reg2] + reg[reg3]


def type_B(reg1, imm):
    return reg[reg1] + bin(int(imm))[2:].rjust(8,'0')


def type_C(reg1, reg2):
    return '00000' + reg[reg1] + reg[reg2]


def type_D(reg1, memory):
    return reg[reg1] + var_dict[memory]


def type_E(memory):
    return '000' + label_dict[memory]


def halt():
    return '00000000000'


# Helper functions for checking instruction parts
def reg_check(register):
    return register in reg


def imm_check(imm):
    if imm[0]=='#' and imm[1:].isdigit():
        return int(imm[1:]) >= 0 and int(imm[1:]) < 256
    else:
        return 0


def flags_check(register):
    return register == "FLAGS"


def var_check(var):
    return var in var_dict


def label_check(lab):
    return lab in label_dict


# Functions to check the validity of instructions according to type
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
    return reg_check(line[1]) and var_check(line[2])


def E_check(line):
    if len(line) != 2:
        return 0
    return label_check(line[1])


def F_check(line):
    return line == ["hlt"]


# Filtering out statements
def parse(data):
    data = [line.split() for line in data]

    var_start = True
    var_dict = dict()
    label_dict = dict()
    op_dict = dict()
    err_dict = dict()
    lim = len(data)

    for i in range(lim):
        line = data[i]
        if line==[]:
            pass
        elif (len(line) == 2 and line[0] == "var"):
            assert var_start == True
            var_dict[line[1]] = bin(lim)[2:].rjust(8, '0')
            lim += 1
        elif (line[0][-1] == ":"):
            label_dict[line[0][:-1]] = bin(i)[2:].rjust(8, '0')
            line=line[1:]
            if (line[0] in opcode):
                op_dict[str(i)] = line
            else:
                err_dict[str(i)] = " ".join(line)
            var_start = False
        elif (line[0] in opcode):
            op_dict[str(i)] = line
            var_start = False
        else:
            err_dict[str(i)] = " ".join(line)
            var_start = False

    assert len(err_dict) == 0
    return var_dict, label_dict, op_dict


# var_init = filter(lambda x: x[:-1]=='var ' and len(x.split())==2,data)
# lim=len(data)
# var_dict={var_init[i][4]:bin(lim+i)[2:].rjust(8,'0') for i in range(len(var_init))}

# label_trav = [(data[i],i) for i in range(len(data)) if data[i][-1]==':' and len(data[i].split())==1]
# label_init= [elem[0] for elem in label_trav]
# label_dict={label_init[i][0][:-1]:bin(label_init[i][1])[2:].rjust(8,'0') for i in range(len(label_trav))}

# op_init = filter(lambda x: x.split()[0] in opcode,data)

# err_init =filter(lambda x: (x not in var_init) and (x not in label_init) and (x not in label_init),data)
# assert len(err_init) == 0
var_dict,label_dict,op_dict= parse(data)

L = []
for num in op_dict:
    line=op_dict[num]
    oper = line[0]
    op = opcode[oper][0]
    type = opcode[oper][1]
    if op == "1001":
        assert len(line) == 3
        assert reg_check(line[1])
        if imm_check(line[2]):
            op += "0"
            type = "B"
            L.append(op + type_B(line[1], line[2][1:]))
        if reg_check(line[2]) or flags_check(line[2]):
            op += "1"
            type = "C"
            L.append(op + type_C(line[1], line[2]))
    else:
        if type == "A":
            assert A_check(line)
            L.append(op + type_A(line[1], line[2], line[3]))
        elif type == "B":
            assert B_check(line)
            L.append(op + type_B(line[1], line[2][1:]))
        elif type == "C":
            assert C_check(line)
            L.append(op + type_C(line[1], line[2]))
        elif type == "D":
            assert D_check(line)
            L.append(op + type_D(line[1], line[2]))
        elif type == "E":
            assert E_check(line)
            L.append(op + type_E(line[1]))
        else:
            #assert F_check(op)
            L.append(op + halt())

with open('binary.txt', 'w') as f:
    for i in L:
        f.write(i + '\n')
