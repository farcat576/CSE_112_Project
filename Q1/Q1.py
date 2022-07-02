import sys

#Creating a list of strings of the given input and storing it in a variable commands
with open("q1testcase.txt", 'r') as f:
    data = f.readlines()
    commands = [data[i].strip() for i in range(len(data))] 
    commands = list(filter(lambda a: a != "", commands))

output = open('binary.txt',"w")
L = []

# Opcode mapping
opcode = {"add": ["10000", 'A'], "sub": ["10001", "A"], "mov": ["1001", ""], "ld": ["10100", "D"],
          "st": ["10101", "D"], "mul": ["10110", "A"], "div": ["10111", "C"], "rs": ["11000", "B"],
          "ls": ["11001", "B"], "xor": ["11010", "A"], "or": ["11011", "A"], "and": ["11100", "A"],
          "not": ["11101", "C"], "cmp": ["11110", "C"], "jmp": ["11111", "E"], "jlt": ["01100", "E"],
          "jgt": ["01101", "E"], "je": ["01111", "E"], "hlt": ["01010", "F"]}

#creating error_dict which contains code-error mapping and is called in error() function
error_dict = {"101": "duplicate hlt statement detected.", "102": "Last instruction is not hlt.",
              "103": "Too many instructions given.", "201": "Register not found",
              "202": "Immediate value format not recognised", "203": "Illegal use of FLAGS register detected.",
              "204": "Syntax Error.", "301": "Variable not defined",
              "302": "Variable not defined at the beginning", "303": "Label not found.",
              "304": "Syntax error in use of variable.", "305": "Syntax error in use of label.",
              "306": "Variable used as label.", "307": "Label used as variable.",
              "308": "Variable already initialised before.", "309": "Label already initialised before."
              }

def error(error_code, error_line = '-1'):
    """Universal program for checking errors"""
    if error_line == '-1':
        output.write(error_dict[error_code] + "\nAssembling halted." )
        output.close()
        sys.exit()  #Ending the program incase an error is detected
    output.write("At line " + error_line + ', ' + error_dict[error_code] + "\nAssembling halted.")
    output.close() 
    sys.exit() #Ending the program incase an error is detected

# Filtering out statements
def parse(data):
    data = [line.split() for line in data]

    var_start = True #Declaring var_start for handling the position of variable declaration in input
    var_dict = dict()
    label_dict = dict()
    op_dict = dict()
    lim = len(data)

    if lim > 256:
        error("103")

    #parsing through the data in order to define variables, mark labels and normal statements
    for i in range(lim):
        line = data[i]
        #checks if variable is in the start and if variable is legally identified
        if (line[0] == "var"): 
            if (len(line)!=2):
                error("304", str(i + 1))
            if not var_start:
                error("302", str(i + 1))
            if line[1] in var_dict:
                error("308", str(i + 1))
            var_dict[line[1]] = lim
            lim += 1
        #checks for a colon in the line, if present then check conditions for a label and store line in label_dict
        elif (": " in " ".join(line)): 
            if (line[0][-1] != ":"):
                error("305", str(i + 1))
            if line[0][:-1] in label_dict:
                error("309", str(i + 1))
            label_dict[line[0][:-1]] = i
            line = line[1:]
            if (line[0] in opcode):
                op_dict[str(i)] = line
            else:
                error("204", str(i + 1))
            var_start = False
        #checking if the line is in opcode and appending to op_dict for assembling
        elif (line[0] in opcode):
            op_dict[str(i)] = line
            var_start = False
        else:
            error("204", str(i + 1))
    
    lin=list(op_dict.values()).count(["hlt"])
    if lin == 0:
        error('102')
    elif lin > 1:
        error("101", str(data.index(['hlt']) + 1))
    
    #variable declaration do not take up code space in the memory
    offset = len(var_dict)
    var_dict = {key : bin(var_dict[key]-offset)[2:].rjust(8, '0')
                for key in var_dict}
    label_dict = {key : bin(label_dict[key]-offset)[2:].rjust(8, '0') 
                for key in label_dict}
    op_dict = {str(int(key) - offset) : op_dict[key]
                for key in op_dict}

    return var_dict, label_dict, op_dict

var_dict, label_dict, op_dict = parse(commands)

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

#checking if format of given immediate value is valid and is in the range 0-255(both inclusive)
def imm_check(imm):
    if imm[0] == '$' and imm[1:].isdigit():
        return int(imm[1:]) >= 0 and int(imm[1:]) < 256
    else:
        return False

# Boolean functions that check whether the given parameter holds true or not
def flags_check(register):
    return register == "FLAGS"


def var_check(var):
    return var in var_dict


def label_check(lab):
    return lab in label_dict


# Functions to check the validity of instructions according to type
def A_check(line, error_ln):
    if len(line) != 4:
        error("204",error_ln)
    elif not ((reg_check(line[1])) and (reg_check(line[2])) and (reg_check(line[3]))):
        if (flags_check(line[1]) or flags_check(line[2]) or flags_check(line[3])):
            error("203", error_ln)
        error("204", error_ln)
    else:
        return True


#immediate value is not checked, pls fix
def B_check(line,error_ln):
    if len(line) != 3:
        error("204", error_ln)
    elif not (reg_check(line[1])):
        if (flags_check(line[1])):
            error("203", error_ln)
        error("201", error_ln)
    elif not (imm_check(line[2])):
        error("202",str(int(error_ln)))
    return True


def C_check(line,error_ln):
    if len(line) != 3:
        error("204", error_ln)
    if not (reg_check(line[1]) and reg_check(line[2])):
        error("201", error_ln)
    return True


def D_check(line,error_ln):
    if len(line) != 3:
        error("204", error_ln)
    if not (reg_check(line[1])):
        if (flags_check(line[1])):
            error("203", error_ln)
        error("201", error_ln)
    if not (var_check(line[2])):
        if label_check(line[2]):
            error("307", error_ln)
        error("301", error_ln)
    return True


def E_check(line,error_ln):
    if len(line) != 2:
        error("204", error_ln)
    if not (label_check(line[1])) :
        if var_check(line[2]):
            error("306", error_ln)
        error("303", error_ln)
    return True

def F_check(line,error_ln):
    if line != ["hlt"]:
        error("204", error_ln)
    return True

def process():
    for num in op_dict:
        line = op_dict[num]
        oper = line[0]
        op = opcode[oper][0]
        type = opcode[oper][1]
        if op == "1001":
            if len(line) != 3:
                error("204", str(int(num) + 1))
            elif not reg_check(line[1]):
                error("201", str(int(num) + 1))
            
            if imm_check(line[2]):
                op += "0"
                type = "B"
                L.append(op + type_B(line[1], line[2][1:]))
            elif reg_check(line[2]) or flags_check(line[2]):
                op += "1"
                type = "C"
                L.append(op + type_C(line[1], line[2]))
            else:
                error("204", str(int(num) + 1))
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
