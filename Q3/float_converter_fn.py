def float_to_bin(float_num):
    decimal,fraction = str(float_num).split('.')
    binf = ''
    decimal = bin(int(decimal))[2:]
    fraction = int(fraction)/10**len(fraction)
    for i in range(8):
        fraction*=2
        if fraction>=1:
            fraction-=1
            binf+='1'
        else:
            binf+='0'
        if (fraction)%1 == 0:
            break
    binf = decimal + '.' + binf.ljust(8,'0')
    res = '1.'
    flag = 0
    for i in range(1,6):
        if binf[i] == '.':
            flag = 1
            continue
        else:
            res += binf[i]
    if flag:
        res += binf[6]
    x = binf.index('.')
    return bin(x-1)[2:].rjust(3,'0') + res.ljust(7,'0')[2:] 
  
  #Need to incorporate on to main code
