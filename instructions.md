#  ACN-CTF — Crypto Challenges (Instructions)

Welcome to the **Cryptography** track of ACN-CTF. This directory contains a set of crypto challenges ranging from easy to hard.  
Each problem lives in its own folder under `crypto/`. Read the problem folder README and files for the challenge-specific artifacts.

---

## 1) Echo Storm (Thunder Morse)
**Difficulty:** Easy

**Description:**  
An audio file hides more than static noise.
Listen carefully — the signal carries the secret.

**Files provided (public):**
- `challenge/thunder.wav` (or generator `generate_thunder.py`)



**Organizer notes (PRIVATE):**

- Flag : `acnctf{thunder_heard_the_truth}`

---

## 2) Rain Grid (Forecast Grid)
**Difficulty:** Easy

**Description:**  
A short ciphertext repeats in patterns.
Find the hidden key and unlock the message.

**Files provided (public):**
- `challenge/ciphertext.txt` (e.g. `RCVPKFQYFVMNDRQGR`)

**Hints (public):**
- Hint 1: The storm scribbles are not random — the letters repeat in a cycle, like drops falling in rhythm. Think about grids where rows shift against each other.
- Hint 2: Forecasts often rely on a four-letter word. What falls from the sky again and again?

**Organizer notes (PRIVATE):**
- Key: `RAIN` (Vigenère). Plaintext: `ACNCTF{ILOVEAMRITA}` → formatted flag: `acnctf{i_love_amrita}`

---

## 3) Scroll of the Silent Monk (Monk’s Manuscript)
**Difficulty:** Medium

**Description:**  
A strange script encodes the flag.
Crack the cipher and reveal its true form.

**Files provided (public):**
- `decrypt.png` (ciphertext produced with the monk cipher)
- `writeup.md` containing instructions and allowed tools

**Hints (public):**
- Focus on frequency and repeated patterns.


**Organizer notes (PRIVATE):**
- The plaintext flag (organizer-only): `acnctf{monkpower}`

---

## 4) Layer Lock (Layers of the Storm)  
**TYPE:** Medium  
**Problem input:** encrypted file + riddle file

**Description:**  
The message is wrapped in multiple classic ciphers.
Peel back each layer to reach the core.

**Files provided (public):**
- `encrypt.txt` (the multi-layer encoded string)
- `riddle.txt` (the riddle describing steps)
- `writeup.md` with high-level instructions

**HIDDEN PATH (derived from riddle):**  
- Two tongues whisper in fire → **Hex**  
- Sun’s battalion marches five by five → **Base32**  
- Shadow flips them → **Atbash**  
- Old emperor shifts me thirteen winters → **ROT13**  
- Thunder speaks in broken silence → **Morse**

**ENCRYPTION ORDER (from plaintext to final output):**  
`hex` → `base32` → `atbash` → `rot13` → `morse`

**Hinting (public):**
- Riddle is the authoritative sequence; read it carefully and map each phrase to a transformation.


**Organizer notes (PRIVATE):**
- Example ciphertext: (challenge content should contain the morse string).  
- Final flag (organizer-only): `acnctf{br0ken_l0ck_l0l}`

---

## 5) Forecast in Disguise (Stegano + Crypto)
**Difficulty:** Medium

**Description:**  
The image looks empty at first glance.
Dig into the pixels and break the code inside.

**Files provided (public):**
- `challenge.png` (visually empty PNG)
- `writeup.md` with extraction instructions

**Hints (public):**
- Inspect the red-channel LSBs 
- The numeric residues suggest modular arithmetic; 

**Organizer notes (PRIVATE):**
- Extraction reconstructs integers 0–256. Recognize `c = (ord(char) ** 3) mod 257`. Precompute cube roots modulo 257 to invert.  
- Recovered flag (organizer-only): `acnctf{crypto_in_pixels}`

**Provided organizer solver example (private):**
- A Python script using PIL to read pixels, extract LSBs, build `encrypted[]`, map through cube-root lookup, and reassemble ASCII.

---

## 6) Whispers of the Prime (Predictable LCG RSA)
**Difficulty:** Hard

**Description:**  
A weak random generator betrayed an RSA system.
Use the leaked values to reconstruct the secret.

**Files provided (public):**
- `public.pem` (RSA public key)
- `flag.enc` (encrypted flag as integer or binary)
- `dump.txt` (leaked LCG outputs)
- `writeup.md` (notes on format and approach)

**Hints (public):**
- Use leaked outputs and the known structure to derive candidate primes.  
- Consider using `sympy.nextprime()` on reconstructed values if primes are near the leaked outputs.

**Organizer notes (PRIVATE):**
- Example approach: take leaked 8 values, OR with a known high bit (if used), use `sympy.nextprime()` for each candidate, compute `N` and `phi`, invert `e` to get `d`, decrypt ciphertext.  
- Flag (organizer-only): `acnctf{Predictable_LCG_RSA}`

---

## 7) Twisted Arcs (Elliptic Curve / Timing / RNG attack)
**Difficulty:** Hard

**Description:**  
Elliptic curves hide the key, but timing leaks reveal more than intended.
Exploit the flaws to recover the message.

**Files provided (public):**
- `challenge/satellite_pub.pem` (long-term public key)
- `challenge/ephemeral_pubs/msgX_pub.pem` (ephemeral public keys for messages)
- `challenge/ciphertexts/msgX.enc` (encrypted messages)
- `challenge/timing_leaks/msgX_hw.txt` (Hamming weight / timing leakage data)
- `challenge/README.md` describing the leak model and allowed methods

**Hints (public):**
- Timing/Hamming leaks provide partial information about ephemeral private keys.  
- Possible approaches: brute-force LFSR seeds (if feasible), or use lattice/HNP techniques to recover partial key bits.

**Organizer notes (PRIVATE):**
- Simulate LFSR to generate candidates, match Hamming weight traces, verify candidates by computing matching public keys.  
- Example recovered flag (organizer-only): `acnctf{echoes_from_the_leo_satellite}`

**Provided organizer solver (private):**
- Python PoC that simulates the LFSR, reconstructs ephemeral keys, derives shared secret with provided satellite public key, HKDF → XOR decrypts ciphertext.

---

## GENERAL SOLVER TOOLS & TIPS
- Audio & stego: Audacity, `sox`, Python (`numpy`, `scipy`, `PIL`).
- Ciphers: CyberChef, `hashcat`, `john`, simple Python scripts.
- RSA / number theory: Python (`sympy`, `gmpy2`), Sage (if available).
- ECC / side-channels: Python cryptography libraries, lattice libraries (`fpylll`), and familiarity with Hidden Number Problem (HNP).
- For any networked or Dockerized challenge, check the challenge folder for deployment instructions.

---


### Private solutions and flags (organizer-only)
- Echo Storm (Thunder Morse): `acnctf{thunder_heard_the_truth}`  
- Rain Grid (Forecast Grid): `acnctf{i_love_amrita}`  
- Monk’s Manuscript: `acnctf{monkpower}`  
- Cipher Onion (Layers): `acnctf{br0ken_l0ck_l0l}`  
- Forecast in Disguise (Stego+Crypto): `acnctf{crypto_in_pixels}`  
- Whispers of the Prime (Predictable LCG RSA): `acnctf{Predictable_LCG_RSA}`  
- Twisted Arcs (ECC timing/RNG): `acnctf{echoes_from_the_leo_satellite}`

(Include private solution scripts and longer writeups in your private solutions folder.)

---


---

