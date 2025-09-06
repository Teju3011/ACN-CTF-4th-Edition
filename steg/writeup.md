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

Participants are given only challenge.py and stegosolver.py is solution 


Recovered flag:
acnctf{crypto_in_pixels}


