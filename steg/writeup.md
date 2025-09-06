CHALLENGE:STEG+CRYPTO:[MEDIUM]

Step 1: Inspect the PNG

The provided challenge.png looks like a plain white image. That’s a common sign of LSB (Least Significant Bit) steganography.

Step 2: Extract Hidden Data

Using a script, read the red channel LSBs in groups of 8 → this reconstructs numbers that represent encrypted values.
Result: you get a sequence of integers in the range 0–256.

Step 3: Recognize the Crypto

Looking at the numbers, they don’t directly map to ASCII. But since the modulus 257 is a prime, this looks like modular arithmetic (RSA-style).
After some testing, you realize it’s:
c = (ord(char) ^ 3) mod 257

Step 4: Decrypt the Values

To recover characters, compute cube roots modulo 257.
Because 257 is prime, you can precompute (x^3 mod 257) for all x in [0, 256] and build a lookup table.

Step 5: Rebuild the Flag

After replacing values with their modular cube roots, convert numbers back to ASCII.

Challenge description:
We found this strange PNG. 
It looks empty, but maybe there’s more hidden inside the pixels...
Can you recover the secret?


Recovered flag:
acnctf{crypto_in_pixels}


Solution:

from PIL import Image


mod = 257

exp = 3

flag_chars = []


cube_roots = {}

for x in range(mod):
    
    cube_roots[(x ** exp) % mod] = x


img = Image.open("challenge.png")

pixels = img.load()

width, height = img.size


encrypted = []

for i in range(width // 8):
    
    val = 0
    
    for bit in range(8):
        
        r, g, b = pixels[i * 8 + bit, 0]
        
        val |= (r & 1) << bit
    
    encrypted.append(val)


for val in encrypted:
    
    if val in cube_roots:
    
        flag_chars.append(chr(cube_roots[val]))
    
    else:
    
        flag_chars.append("?")

flag = "".join(flag_chars)

print("[+] Recovered flag:", flag)



