final_list = ["1001000100001010","1001001001100100","1011000011001010","1010101100000101","0101000000000000"]

with open("binary.txt",'w') as f:
    for i in final_list:
        f.write(i + "\n")
