reg={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}

def type_A(reg1,reg2,reg3):
    return '00'+reg[reg1]+reg[reg2]+reg[reg3]

def type_B(reg1,imm):
    return reg[reg1]+bin(int(imm))[2:]

def type_C(reg1,reg2):
    return '00000'+reg[reg1]+reg[2]
