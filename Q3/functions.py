def bin_to_float(binary):
    exp = binary[:3]
    mantissa = binary[3:]
    return 2**(int(exp,2)) * (1 + int(mantissa,2)/(2**5))

def float_to_bin(float_num):
    decimal,fraction = str(float_num).split('.')
    x = int(decimal)
    binf = ''
    for i in range(7):
        if x == 1:
            exp = i
            break
        x//=2
    if exp>7:
        return "can't be represented"
    exponent = bin(exp)[2:].rjust(3,'0')
    fraction = int(fraction)/10**len(fraction)
    for i in range(5-exp):
        fraction*=2
        if fraction>=1:
            fraction-=1
            binf+='1'
        else:
            binf+='0'
        if (fraction)%1 == 0:
            break
    decimal = bin(int(decimal))[2:]
    binf = (decimal + binf).rstrip('0')[1:]
    if len(binf)>6:
        #redirect for error
        return("can't be represented")
    return (exponent + binf).ljust(8, "0")


def float_check(f: str) -> bool:
    whole, decimal = f[1:].split('.')
    if f[0] == '$':
        return True
    else:
        return error()
