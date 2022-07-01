import sys

with open("q1testcase.txt", 'r') as f:
    data = f.readlines()
    commands = [data[i].strip() for i in range(len(data))]

output = open('binary.txt',"w")

def error(error_dict, error_code, error_line = '-1'):
    if error_line == '-1':
        output.write(error_dict[error_code] + "\nAssembling halted." )
        output.close()
        sys.exit()
    output.write("At line " + error_line + ', ' + error_dict[error_code] + "\nAssembling halted.")
    output.close()
    sys.exit()

# assertion statements for each instruction
L = []

# Opcode mapping
opcode = {"add": ["10000", 'A'], "sub": ["10001", "A"], "mov": ["1001", ""], "ld": ["10100", "D"],
          "st": ["10101", "D"], "mul": ["10110", "A"], "div": ["10111", "C"], "rs": ["11000", "B"],
          "ls": ["11001", "B"], "xor": ["11010", "A"], "or": ["11011", "A"], "and": ["11100", "A"],
          "not": ["11101", "C"], "cmp": ["11110", "C"], "jmp": ["11111", "E"], "jlt": ["01100", "E"],
          "jgt": ["01101", "E"], "je": ["01111", "E"], "hlt": ["01010", "F"]}

error_dict = {"101": "duplicate hlt statement detected.", "102": "Last instruction is not hlt.",
              "103": "Too many instructions given.", "201": "Register not found",
              "202": "Immediate value format not recognised", "203": "Illegal use of FLAGS register detected.",
              "204": "Syntax Error.", "301": "Variable not defined",
              "302": "Variable not defined at the beginning", "303": "Label not found.",
              "304": "Syntax error in use of variable.", "305": "Syntax error in use of label.",
              "306": "Variable used as label.", "307": "Label used as variable."
              }


# Filtering out statements
def parse(data):
    data = [line.split() for line in data]
    data = list(filter(lambda a: a != [], data))

    var_start = True
    var_dict = dict()
    label_dict = dict()
    op_dict = dict()
    err_dict = dict()
    lim = len(data)

    for i in range(lim):
        line = data[i]
        if (line[0] == "var"):
            if (len(line)!=2):
                error(error_dict, "304", str(i + 1))
            if not var_start:
                error(error_dict, "302", str(i + 1))
            var_dict[line[1]] = bin(lim)[2:].rjust(8, '0')
            lim += 1
        elif (": " in " ".join(line)):
            if (line[0][-1] != ":"):
                error(error_dict, "305", str(i + 1))
            label_dict[line[0][:-1]] = bin(i)[2:].rjust(8, '0')
            line = line[1:]
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

    if len(err_dict):
        error_ln=list(err_dict.keys())[0]
        error(error_dict, "204", error_ln)
    return var_dict, label_dict, op_dict

var_dict, label_dict, op_dict = parse(data)

lin=commands.count("hlt")
if lin == 0:
    error(error_dict,'102')
elif lin > 1:
    error(error_dict,"101",str(commands.index('hlt') + 1))
elif len(commands) > 256:
    error(error_dict, "103")

# Register mapping
reg = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110', 'FLAGS': '111'}

# Conversion functions for each type
def type_A(reg1, reg2, reg3):
    return '00' + reg[reg1] + reg[reg2] + reg[reg3]


def type_B(reg1, imm):
    return reg[reg1] + bin(int(imm))[2:].rjust(8, '0')


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
    return register in reg and register != "FLAGS"


def imm_check(imm):
    if imm[0] == '$' and imm[1:].isdigit():
        return int(imm[1:]) >= 0 and int(imm[1:]) < 256
    else:
        return False


def flags_check(register):
    return register == "FLAGS"


def var_check(var):
    return var in var_dict


def label_check(lab):
    return lab in label_dict


# Functions to check the validity of instructions according to type
def A_check(line, error_ln):
    if len(line) != 4:
        error(error_dict, "204",error_ln)
    elif not ((reg_check(line[1])) and (reg_check(line[2])) and (reg_check(line[3]))):
        if (flags_check(line[1]) or flags_check(line[2]) or flags_check(line[3])):
            error(error_dict, "203", error_ln)
        error(error_dict, "204", error_ln)
    else:
        return True


#immediate value is not checked, pls fix
def B_check(line,error_ln):
    if len(line) != 3:
        error(error_dict, "204", error_ln)
    elif not (reg_check(line[1])):
        if (flags_check(line[1])):
            error(error_dict, "203", error_ln)
        error(error_dict, "201", error_ln)
    elif not (imm_check(line[2])):
        error(error_dict, "202",str(int(error_ln)))
    return True
    #return reg_check(line[1]) and imm_check(len[2])


def C_check(line,error_ln):
    if len(line) != 3:
        error(error_dict, "204", error_ln)
    if not (reg_check(line[1]) and reg_check(line[2])):
        error(error_dict, "201", error_ln)
    return True


def D_check(line,error_ln):
    if len(line) != 3:
        error(error_dict, "204", error_ln)
    if not (reg_check(line[1])):
        if (flags_check(line[1])):
            error(error_dict, "203", error_ln)
        error(error_dict, "201", error_ln)
    if not (var_check(line[2])):
        if label_check(line[2]):
            error(error_dict, "307", error_ln)
        error(error_dict, "301", error_ln)
    return True


def E_check(line,error_ln):
    if len(line) != 2:
        error(error_dict, "204", error_ln)
    if not (label_check(line[1])) :
        if var_check(line[2]):
            error(error_dict, "306", error_ln)
        error(error_dict, "303", error_ln)
    return True

def F_check(line,error_ln):
    if line != ["hlt"]:
        error(error_dict, "204", error_ln)
    return True

def process():
    for num in op_dict:
        line = op_dict[num]
        oper = line[0]
        op = opcode[oper][0]
        type = opcode[oper][1]
        if op == "1001":
            if len(line) != 3:
                error(error_dict, "204", str(int(num) + 1))
            elif not reg_check(line[1]):
                error(error_dict, "201", str(int(num) + 1))
            
            if imm_check(line[2]):
                op += "0"
                type = "B"
                L.append(op + type_B(line[1], line[2][1:]))
            elif reg_check(line[2]) or flags_check(line[2]):
                op += "1"
                type = "C"
                L.append(op + type_C(line[1], line[2]))
            else:
                error(error_dict, "204", str(int(num) + 1))
        else:
            if type == "A":
                A_check(line,str(int(num) + 1))
                L.append(op + type_A(line[1], line[2], line[3]))
            elif type == "B":
                B_check(line,str(int(num) + 1))
                L.append(op + type_B(line[1], line[2][1:]))
            elif type == "C":
                C_check(line,str(int(num) + 1))
                L.append(op + type_C(line[1], line[2]))
            elif type == "D":
                D_check(line,str(int(num) + 1))
                L.append(op + type_D(line[1], line[2]))
            elif type == "E":
                E_check(line,str(int(num) + 1))
                L.append(op + type_E(line[1]))
            else:
                F_check(line,str(int(num) + 1))
                L.append(op + halt())

    return L

def main(output):
    L = process()
    #with open('binary.txt', 'w') as f:
    for i in range(len(L)-1):
        output.write(L[i] + '\n')

    output.write(L[len(L)-1])

main(output)

#Comments done till label_check

# Errors:
# 1. incase the hlt instruction is contained at the end in a label, the program should run but it does not
# 2. incase there is say 1 empty line and 257 lines of code, the assembler should still assemble as it is said that it can write <= 256 lines and the new lines are to be ignored
# 3. Variables point to the wrong addresses, they should be reduced by the length of the var_dict
# refer testcase2.txt for checking the above error 3 and testcase1.txt for checking error 2, in folder testcases
