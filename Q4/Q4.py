from sys import exit, stdin, stdout
import numpy as np
import matplotlib.pyplot as plt

#Initializing all needed hardware equivalents
MEM = ['0'*16] * 256

PC = 0

RF = {'000' : 0, '001' : 0, '010' : 0, '011' : 0, '100' : 0, '101' : 0, '110' : 0, '111' : ['0']*16}

overflow_lim = 2**16 -1
underflow_lim = 0
prev_flags = ['0']*16

data = stdin.readlines()
data = [line.strip() for line in data]
data = list(filter(lambda a: a != "", data))

def fix_mem():
    for i in range(len(data)):
        MEM[i] = data[i]

fix_mem()

#Variables and function for plotting the scatter graph
x_axis = []
y_axis = []
cycle = 1

def plot_graph():
    global x_axis
    plt.xticks([i for i in range(max(x_axis) + 20)])
    colours = [i for i in range(len(x_axis))]
    x_axis = np.array(x_axis)
    global y_axis
    plt.yticks([i for i in range(max(y_axis) + 20)])
    y_axis = np.array(y_axis)
    colours = np.array(colours)

    area = (5 * 1) ** 2

    plt.scatter(x_axis, y_axis, s = area, c = colours, alpha = 0.5)
    plt.xticks([i for i in range((max(x_axis) + 1)*2)])
    plt.yticks([i for i in range((max(y_axis) + 1)*2)])
    plt.title("Scatter Plot Diagram")
    plt.show()
#____________________________________________________________

def make_binary(number, length):
    if number == '0000000000000000':
        return '0000000000000000'
    if type(number) == list:
        number = ''.join(number)
        return number
    number = bin(number)[2:]
    number = number.rjust(length, "0")
    return number

def mem_dump():
    for line in MEM:
        stdout.write(line + "\n")

def line_output():
    stdout.write(f"{make_binary(PC,8)} ")
    for register in RF:
        stdout.write(f"{make_binary(RF[register],16)} ")
    stdout.write("\n")


# refactor for stdio, test this thing...
# reset FLAGS overflow and underflow bits whenever needed

def dec_int(string):
    string=string[::-1]
    result=sum([int(string[i])*(2**i)
                for i in range(len(string))])
    return result

#Classes for each type
class A:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.reg1 = line[7:10]
        self.reg2 = line[10:13]
        self.reg3 = line[13:16]
        self.oper(self)
    
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
        self.oper(self)
    
    def mov_i(self):
        RF[self.reg] = self.imm
    
    def right(self):
        ans = RF[self.reg] >> self.imm
        if ans > overflow_lim:
            ans = ans % (overflow_lim + 1)
        RF[self.reg] = ans
        
    
    def left(self):
        RF[self.reg] = RF[self.reg] << self.imm

class C:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.reg1 = line[10:13]
        self.reg2 = line[13:16]
        self.oper(self)
    
    def mov_r(self):
        RF[self.reg2] = RF[self.reg1]
    
    def divide(self):
        if RF[self.reg1] // RF[self.reg2]%0 != 0:
            RF['000'] = RF[self.reg1] // RF[self.reg2]
            RF['001'] = RF[self.reg1] % RF[self.reg2]
        
    
    def invert(self):
        RF[self.reg2] = overflow_lim + 1 + ~RF[self.reg1]
    
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
        self.oper(self)
    
    def load(self):
        x_axis.append(cycle)
        y_axis.append(self.mem)
        RF[self.reg] = MEM[self.mem]
    
    def store(self):
        x_axis.append(cycle)
        y_axis.append(self.mem)
        MEM[self.mem] = make_binary(RF[self.reg],16)

class E:
    def __init__(self, line):
        self.oper = opcode[line[:5]][0]
        self.mem = dec_int(line[8:16])
        self.oper(self)
    
    def unconditional(self):
        x_axis.append(cycle)
        y_axis.append(self.mem)
        global PC
        PC = self.mem - 1
    
    def less(self):
        if RF['111'][-3] == '1':
            E.unconditional(self)
    
    def greater(self):
        if RF['111'][-2] == '1':
            E.unconditional(self)
    
    def equal(self):
        if RF['111'][-1] == '1':
            E.unconditional(self)

#Opcode mapping        
opcode = {"10000": [A.add, "A"], "10001": [A.subtract, "A"], "10010": [B.mov_i, "B"], "10011": [C.mov_r, "C"], "10100": [D.load, "D"],
          "10101": [D.store, "D"], "10110": [A.multiply, "A"], "10111": [C.divide, "C"], "11000": [B.right, "B"], "11001": [B.left, "B"],
          "11010": [A.bool_xor, "A"], "11011": [A.bool_or, "A"], "11100": [A.bool_and, "A"],
          "11101": [C.invert, "C"], "11110": [C.compare, "C"], "11111": [E.unconditional, "E"],
          "01100": [E.less, "E"], "01101": [E.greater, "E"], "01111": [E.equal, "E"], "01010": ["hlt", "F"]}

#Initialising lines as instructions of their respective types
def exec(line):
    
    prev_flags=RF['111']
    code=line[:5]
    type=opcode[code][1]
    
    if type == "A":
        line = A(line)
    elif type == "B":
        line = B(line)
    elif type == "C":
        line = C(line)
    elif type == "D":
        line = D(line)
    elif type == "E":
        line = E(line)
    
    for ind in range(1,5):
        if prev_flags[-ind] == RF['111'][-ind]:
            RF['111'][-ind]='0'
    
    line_output()
    # else:
    #     output_testing()
    #     PC += 1
    #     exit()
    global cycle
    cycle += 1



while MEM[PC] != "0101000000000000":
    exec(MEM[PC])
    PC += 1

#output()
#line_output()
#mem_dump()
plot_graph()

