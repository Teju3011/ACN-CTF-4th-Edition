# Writeup — Verilog Flag Checker
## Easy Reverse Engineering Challenge

Category: Reverse Engineering
Difficulty: Easy

Description
We found a mysterious hardware design written in Verilog. It looks like it’s checking some kind of secret. Can you reverse engineer it to recover the hidden flag?

## Challenge
Files provided:
```
magic.v

chall.v

t_chall.v
```

Analyze the modules, figure out the transformations, and decode the numbers in the testbench.

Flag Format

`acnctf{...}`


````
GOOD LUCK!
````
.


.


.


## SOLUTION

## 1. Inspect the code
- `magic.v` defines a function `magic(val, inp)` with four possible transformations (rotate, xor, add, etc.).  
- `chall.v` chains four `magic` calls together, with `val0..val3` derived from bit-slices of the input.  
- `t_chall.v` provides an array of 26 target values — the “encrypted flag.”

## 2. Recreate the logic in Python
```python
def magic(val, inp):
    if val == 0: return ((inp << 3) | (inp >> 5)) & 0xFF
    if val == 1: return ((inp >> 2) ^ 0x5A) & 0xFF
    if val == 2: return (inp + 77) & 0xFF
    if val == 3: return (inp ^ 0x33) & 0xFF
    return inp

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
```

## 3. Brute-force the targets
Each number in the target array corresponds to one flag character passed through `chall()`.  
Since the mapping isn’t one-to-one (collisions), try all printable candidates and pick the one that forms a valid flag.

## 4. Recover the flag
After brute forcing and resolving collisions, the correct flag emerges:

```
acnctf{404_fl4g_n0t_f0und}
```
