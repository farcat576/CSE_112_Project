def log_2(x):
    x=int(x)
    result =0
    while(x):
        result+=1
        x=x//2
    return result-1

data_in={"b":0, "kb":10, "Mb":20, "Gb":30, "Tb": 40, "B":3, "kB":13, "MB":23, "GB":33, "TB": 43}
data_out=[(0,"b"),(3,"B"),(13,"kB"),(23,"MB"),(33,"GB"),(43,"TB")]
address={"Bit":0, "Nibble":2, "Byte":3, "Word": "CPU"}

class Computer:
    def __init__(self,space,addressing):
        space = space.split()[:2]
        type = addressing.split()[0]
        self.memory=log_2(space[0])+data_in[space[1]]
        self.addressing = address[type]
    
    def address_bit(self):
        return self.memory-self.addressing
    
class Query_1(Computer):
    def __init__(self,text):
        Computer.__init__(self,text[0],text[1])
        self.instruction=int(text[2])
        self.register=int(text[3])

        print(self.address_bit())
        print(self.opcode_bit())
        print(self.filler_bit())
        print(self.max_op())
        print(self.max_reg())
    
    def opcode_bit(self):
        return self.instruction-self.address_bit()-self.register
    
    def filler_bit(self):
        return self.address_bit()-self.register
    
    def max_op(self):
        return 2**self.opcode_bit()
    
    def max_reg(self):
        return 2**self.register
    
class Query_2(Computer):
    def __init__(self,text):
        Computer.__init__(self,text[0],text[1])
        type = text[3].split()[0]
        self.CPU=log_2(text[2].split()[0])
        self.new_addressing=address[type]

        if self.addressing == "CPU":
            self.addressing = self.CPU
        if self.new_addressing == "CPU":
            self.new_addressing = self.CPU
        print(self.new_pins())
    
    def new_bit(self):
        return self.memory-self.new_addressing
    
    def new_pins(self):
        return self.new_bit() - self.address_bit()
    
class Query_3(Computer):
    def __init__(self, text):
        Computer.__init__(self,text[0],text[1]) 
        self.CPU =log_2(text[2].split()[0])
        type = text[4].split()[0]
        self.pins=int(text[3].split()[0])
        self.add =address[type]

        if self.addressing == "CPU":
            self.addressing = self.CPU
        if self.add == "CPU":
            self.add = self.CPU
        print(self.new_memory())
    
    def new_memory(self):
        total = self.pins+self.add
        i=0
        while data_out[i][0]<total:
            i+=1
        i-=1
        
        num = 2**(total-data_out[i][0])
        type = data_out[i][1]
        return str(num)+" "+type

def main():
    L=[]
    L=[input().strip() for i in range(4)]
    if L[3][-4:] == "pins":
        L.append(input().strip())
    if len(L) == 5:
        Query_3(L)
    else:
        if L[2].isdigit() and L[3].isdigit():
            Query_1(L)
        else:
            Query_2(L)

main()
