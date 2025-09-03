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



from Crypto.PublicKey import RSA



\\# Load ciphertext and public key



c\\\_int = int(open("flag.enc").read())



pub = RSA.import\\\_key(open("public.pem").read())



N, e = pub.n, pub.e



\\# Load the original primes (organizer-only)



with open("primes.txt") as f:



\&#x20;   primes = \\\[int(x.strip()) for x in f.readlines()]



\\# Recompute phi and modulus



phi = 1



N\\\_reconstructed = 1



for p in primes:



\&#x20;   phi \\\*= (p - 1)



\&#x20;   N\\\_reconstructed \\\*= p



\\# Compute private key



d = pow(e, -1, phi)



\\# Decrypt flag



m\\\_int = pow(c\\\_int, d, N\\\_reconstructed)



flag\\\_bytes = m\\\_int.to\\\_bytes((m\\\_int.bit\\\_length()+7)//8, "big")



flag = flag\\\_bytes.decode()



print("\\\[+] Extracted Flag:", flag)



---



\## Flag



```

ACNCTF{Predictable\_LCG\_RSA}

```



