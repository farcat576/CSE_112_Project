#Initializing all needed hardware equivalents
MEM = ['0'*16] * 256

PC = '0'*8

RF = {'000' : 0, '001' : 0, '010' : 0, '011' : 0, '100' : 0, '101' : 0, '110' : 0, '111' : '0000000000000000'}

overflow_lim = 2**16 -1
underflow_lim = 0

#Implemement dec_int helper function
#Deal with Branch instructions messing with PC
#Implement invert later on as python gives signed answer
#Left and right shifts can cause overflow

#Classes for each type
class A:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.reg1 = line[7:10]
        self.reg2 = line[10:13]
        self.reg3 = line[13:16]
    
    def add(self):
        ans = RF[self.reg1] + RF[self.reg2]
        if ans > overflow_lim:
            RF['111'][-4] = '1'
            ans = ans % (overflow_lim + 1)
        RF[self.reg3] = ans
    
    def subtract(self):
        ans = RF[self.reg1] - RF[self.reg2]
        if ans < underflow_lim:
            RF['111'][-4] = '1'
            ans = 0
        RF[self.reg3] = ans
    
    def multiply(self):
        ans = RF[self.reg1] * RF[self.reg2]
        if ans > overflow_lim:
            RF['111'][-4] = '1'
            ans = ans % (overflow_lim + 1)
        RF[self.reg3] = ans
    
    def bool_xor(self):
        RF[self.reg3] = RF[self.reg1] ^ RF[self.reg2]
    
    def bool_or(self):
        RF[self.reg3] = RF[self.reg1] | RF[self.reg2]
    
    def bool_and(self):
        RF[self.reg3] = RF[self.reg1] & RF[self.reg2]

class B:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.reg = line[5:8]
        self.imm = dec_int(line[8:16])
    
    def mov_i(self):
        RF[self.reg] = self.imm
    
    def right(self):
        RF[self.reg] = RF[self.reg] >> self.imm
    
    def left(self):
        RF[self.reg] = RF[self.reg] << self.imm

class C:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.reg1 = line[10:13]
        self.reg2 = line[13:16]
    
    def mov_r(self):
        RF[self.reg2] = RF[self.reg1]
    
    def divide(self):
        RF['000'] = RF[self.reg1] // RF[self.reg2]
        RF['001'] = RF[self.reg1] % RF[self.reg2]
    
    def invert(self):
        RF[self.reg2] = ~RF[self.reg1]
    
    def compare(self):
        ineq = RF[self.reg1] > RF[self.reg2]
        eq = RF[self.reg1] == RF[self.reg2]
        if ineq:
            RF['111'][-2] = '1'
        elif eq:
            RF['111'][-1] = '1'
        else:
            RF['111'][-3] = '1'

class D:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.reg = line[5:8]
        self.mem = dec_int(line[8:16])
    
    def load(self):
        RF[self.reg] = MEM[self.mem]
    
    def store(self):
        MEM[self.mem] = RF[self.reg]

class E:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.mem = line[8:16]
    
    def unconditional(self):
        PC = self.mem
    
    def less(self):
        if RF['111'][-3] == '1':
            unconditional(self)
    
    def greater(self):
        if RF['111'][-2] == '1':
            unconditional(self)
    
    def equal(self):
        if RF['111'][-1] == '1':
            unconditional(self)

#Opcode mapping        
opcode = {"10000": ["add", "A"], "10001": ["sub", "A"], "10010": ["mov_i", "B"], "10011": ["mov_r", "C"], "10100": ["ld", "D"],
          "10101": ["st", "D"], "10110": ["mul", "A"], "10111": ["div", "C"], "11000": ["rs", "B"], "11001": ["ls", "B"],
          "11010": ["xor", "A"], "11011": ["or", "A"], "11100": ["and", "A"],
          "11101": ["not", "C"], "11110": ["cmp", "C"], "11111": ["jmp", "E"],
          "01100": ["jlt", "E"], "01101": ["jgt", "E"], "01111": ["je", "E"], "01010": ["hlt", "F"]}

#Initialising lines as instructions of their respective types
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
