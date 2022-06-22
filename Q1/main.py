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

var_init = filter(lambda x: x[:3]=='var' and len(x.split())==2,data)
lim=len(data)
var_dict={var_init[i][4]:str(lim+i) for i in range(len(var_init))}

label_init = [(data[i],i) for i in range(len(data)) if data[i][-1]==':' and len(data[i].split())==1 ]
label_dict={label_init[i][0][:-1]:str(label_init[i][1]) for i in range(len(var_init))}

out=[]
 for line in data:
     line = line.split()
     if line[0] in opcode:
            op = opcode[line[0]][0]
            type = opcode[line[0]][1]
            if op == "1001":
                assert len(line) == 3
                assert reg_check(line[1])
                if imm_check(line[2]):
                    op += "0"
                    type = "B"
                if reg_check(line[2]) or flags_check(line[2]):
                    op += "1"
                    type = "C"
            else:
                if type == "A":
                    assert check_A(line)
                elif type == "B":
                    assert check_B(line)
                elif type == "C":
                    assert check_C(line)
                elif type == "D":
                    assert check_D(line)
                elif type == "E":
                    assert check_E(line)
                else:
                    assert check_F(line)
#
#Check var and label again
#Fix binary string widths
#Mix all code together
#Change parameters of writing parts
#Handle asserts



