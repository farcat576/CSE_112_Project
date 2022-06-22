#lines are in the form ["str","str","str"]

lineA = ['or','R1','R2','R3']
lineB = ['mov', 'R1', '$8']
lineC = ['div','R4','R3']
lineD = ['ld',]
valid_registers = ['R0','R1','R2','R3','R4','R5','R6']

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


# def type_A(line):
#     assert len(line) == 4
#     for i in line[1:]:
#         assert i in valid_registers, "Syntax Error"
#
# def type_B(line):
#     assert len(line) == 3
#     assert line[1] in valid_registers, "Syntax Error"
#     assert int(line[2][1:]) < 256, "Immediate value exceeds 8 bits"
#
# def type_C(line):
#     assert len(line) == 3
#     for i in line[1:]:
#         assert i in valid_registers, "Syntax Error"
#
# def type_F(line):
#     assert len(line) == 1








