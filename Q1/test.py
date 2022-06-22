reg = {"R0" : '000' , "R1" : '001' , "R2" : '010' , "R3" : '011' , "R4" : '100' , "R5" : '101' , "R6" : '110' , "FLAGS" : '111'}

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
