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
opcode = {"add":["10000",'A'], "sub":["10001","A"], "mov":"10010", "ld":["10100","D"],"st":["10101","D"],"mul":["10110","A"],"div":"10111",
          "rs":"11000","ls":"11001","xor":"11010","or":"11011","and":"11100","not":"11101","cmp":"11110",
          "jmp":"11111","jlt":"01100","jgt":"01101","je":"01111","hlt":"01010"}



for line in data:
    line = line.split()
    if line[0] in opcode:




