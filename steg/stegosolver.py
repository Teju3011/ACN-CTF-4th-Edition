# solver.py
from PIL import Image

mod = 257
exp = 3
flag_chars = []

# Precompute cube roots modulo 257
cube_roots = {}
for x in range(mod):
    cube_roots[(x ** exp) % mod] = x

# Load challenge image
img = Image.open("challenge.png")
pixels = img.load()
width, height = img.size

# Recover encrypted values
encrypted = []
for i in range(width // 8):
    val = 0
    for bit in range(8):
        r, g, b = pixels[i * 8 + bit, 0]
        val |= (r & 1) << bit
    encrypted.append(val)

# Decrypt each value
for val in encrypted:
    if val in cube_roots:
        flag_chars.append(chr(cube_roots[val]))
    else:
        flag_chars.append("?")

flag = "".join(flag_chars)
print("[+] Recovered flag:", flag)
