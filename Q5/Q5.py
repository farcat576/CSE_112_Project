def log_2(x):
    x=int(x)
    result =0
    while(x):
        result+=1
        x=x//2
    return result

data_in={"b":0, "kb":10, "Mb":20, "Gb":30, "Tb": 40, "B":3, "kB":13, "MB":23, "GB":33, "TB": 43}
data_out=[(0,"b"),(3,"B"),(13,"kB"),(23,"MB"),(33,"GB"),(43,"TB")]
address={"Bit":0, "Nibble":2, "Byte":3, "Word": "CPU"}

class Computer:
    def __init__(self,space,addressing):
        space = space.strip()[:2]
        type = addressing.strip()[0]
        self.memory=log_2(space[0])*data_in(space[1])
        self.addressing = address(type)
    
    def address_bit(self):
        return self.memory-self.addressing
    
class Query_1(Computer):
    def __init__(self,text):
        Computer.__init__(self,text[0],text[1])
        self.instruction=int(text[2])
        self.register=int(text[3])
    
    def opcode_bit(self):
        return self.instruction-self.address_bit()-7
    
    def filler_bit(self):
        return self.address_bit(self)-7
    
    def max_op(self):
        return 2**self.opcode_bit()
    
    def max_reg(self):
        return 2**7
    
class Query_2(Computer):
    def __init__(self,text):
        Computer.__init__(self,text[0],text[1])
        CPU =text[2].strip()[0]
        type = text[3].strip()[0]
        self.CPU=log_2(CPU)
        self.new_addressing=address(type)

        if self.addressing == "CPU":
            self.addressing = self.CPU
        if self.new_addressing == "CPU":
            self.new_addressing = self.CPU
    
    def new_bit(self):
        return self.memory-self.new_addressing
    
    def new_pins(self):
        return self.new_bit() - self.address_bit()
    
class Query_3(Computer):
    def __init__(self, text):
        Computer.__init__(self,text[0],text[1]) 
        CPU =text[2].strip()[0]
        type = text[4].strip()[0]
        self.pins=int(text[3].split()[0])
        self.add =address(type)
    
    def new_memory(self):
        total = self.pins+self.add
        i=0
        while data_out[i][0]<total:
            i+=1
        if i==6:
            i=5
        
        num = 2**(total-data_out[i][0])
        type = data_out[i][1]

def main():
    L=[]
    if len(L) == 5:
        Query_3(L)
    else:
        if L[2].isdigit() and L[3].isdigit():
            Query_1(L)
        else:
            Query_2(L)
