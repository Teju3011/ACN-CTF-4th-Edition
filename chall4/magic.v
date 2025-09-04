def magic(val, inp):
    if val == 0:
        return ((inp << 3) | (inp >> 5)) & 0xFF
    elif val == 1:
        return ((inp >> 2) ^ 0x5A) & 0xFF
    elif val == 2:
        return (inp + 77) & 0xFF
    elif val == 3:
        return (inp ^ 0x33) & 0xFF

def chall(inp):
    val0 = (inp >> 0) & 3
    val1 = (inp >> 2) & 3
    val2 = (inp >> 4) & 3
    val3 = (inp >> 6) & 3
    res0 = magic(val0, inp)
    res1 = magic(val1, res0)
    res2 = magic(val2, res1)
    res3 = magic(val3, res2)
    return res3

flag = "acnctf{404_fl4g_n0t_f0und}"
targets = [chall(ord(c)) for c in flag]
print("Targets:", targets)