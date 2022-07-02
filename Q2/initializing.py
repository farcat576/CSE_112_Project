MEM = ['0'*16] * 256

PC = '0'*8

RF = {'000' : 0, '001' : 0, '010' : 0, '011' : 0, '100' : 0, '101' : 0, '110' : 0, '111' : '0000000000000000'}

class A:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.reg1 = line[7:10]
        self.reg2 = line[10:13]
        self.reg3 = line[13:16]

class B:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.reg = line[5:8]
        self.imm = line[8:16]

class C:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.reg1 = line[10:13]
        self.reg2 = line[13:16]

class D:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.reg = line[5:8]
        self.mem = line[8:16]

class E:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.mem = line[8:16]

opcode = {"10000": ["add", "A"], "10001": ["sub", "A"], "10010": ["mov", ""], "10011": ["mov", ""], "10100": ["ld", "D"],
          "10101": ["st", "D"], "10110": ["mul", "A"], "10111": ["div", "C"], "11000": ["rs", "B"], "11001": ["ls", "B"],
          "11010": ["xor", "A"], "11011": ["or", "A"], "11100": ["and", "A"],
          "11101": ["not", "C"], "11110": ["cmp", "C"], "11111": ["jmp", "E"],
          "01100": ["jlt", "E"], "01101": ["jgt", "E"], "01111": ["je", "E"], "01010": ["hlt", "F"]}

def exec(line):
    code=line[:5]
    type=opcode[code][1]
    if type == "A":
        line = A(line)
    elif type == "B":
        line = B(line)
    elif type == "C":
        line = B(line)
    elif type == "D":
        line = D(line)
    elif type == "E":
        line = E(line)
