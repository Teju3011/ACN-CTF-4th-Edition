\#  Predictable LCG RSA\\\[hard]



\## Challenge Overview



Participants are given:



\* `public.pem` → RSA public key

\* `flag.enc` → Encrypted flag

\* `dump.txt` → Leaked outputs from the RNG



The RSA modulus was generated using \*\*8 primes\*\* with a \*\*Linear Congruential Generator (LCG)\*\*. The leaked outputs can be used to reconstruct the primes and derive the private key.



---



\## Solution



Python code:
# participant_solve.py

import sympy

from Crypto.PublicKey import RSA

# Load public key and ciphertext
pub = RSA.import_key(open("public.pem").read())

c_int = int(open("flag.enc").read())

# Load leaked LCG outputs
with open("dump.txt") as f:
   
    lcg_outputs = [int(x.strip()) for x in f.readlines()]

if len(lcg_outputs) != 8:
    
    raise Exception("dump.txt must contain all 8 outputs")

# Reconstruct candidate numbers and primes

candidates = [x | (1 << 120) for x in lcg_outputs]

primes = [sympy.nextprime(c) for c in candidates]

# Reconstruct modulus and phi
N = 1

phi = 1

for p in primes:
    
    N *= p
    
    phi *= (p-1)

# Reconstruct private key

d = pow(pub.e, -1, phi)

# Decrypt flag
m_int = pow(c_int, d, N)

flag_bytes = m_int.to_bytes((m_int.bit_length()+7)//8, "big")

flag = flag_bytes.decode()


print("[+] Flag:", flag)


























---



\## Flag



```

ACNCTF{Predictable_LCG_RSA}

```







