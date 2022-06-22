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
opcode = {"add":["10000",'A'], "sub":["10001","A"], "mov":"10010", "ld":["10100","D"],
        "st":["10101","D"],"mul":["10110","A"],"div":["10111","C"],"rs":["11000","B"],
        "ls":["11001","B"],"xor":["11010","A"],"or":["11011","A"],"and":["11100","A"],
        "not":["11101","C"],"cmp":["11110","C"],"jmp":["11111","E"],"jlt":["01100","E"],
        "jgt":["01101","E"],"je":["01111","E"],"hlt":["01010","F"]}



# for line in data:
#     line = line.split()
#     if line[0] in opcode:
#



