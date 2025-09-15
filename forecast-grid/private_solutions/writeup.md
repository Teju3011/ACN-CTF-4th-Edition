# Forecast Grid — Solution (private)
You are given a single long text (Base64-encoded). Decode it to obtain a lengthy narrative — that narrative has been encrypted with a repeating-key substitution. Recover the underlying story, locate the unusual capital letters hidden inside, and assemble them into the required flag format.

**Ciphertext:** RCVPKF{ERRTPRI_PIGKEZAJ}  
**Vigenère key:** RAIN

## Step-by-step
1. The ciphertext contains letters A–Z and retains braces/underscore unchanged.
2. Use Vigenère decryption with key `RAIN` (repeat key as necessary over letters only).
   - Decryption formula: P = (C - K + 26) mod 26, where letters A=0..Z=25.
3. Applying that to the ciphertext yields:
4. Format flag per contest requirements (lowercase + underscores inside braces):

## Quick manual verification (example)
- Cipher char R (17) with key R (17): (17 - 17) mod 26 = 0 -> A
- Continue across the string respecting only letter characters.

**Final flag (private):** `ACNCTF{ILOVEAMRITA}`


After decoding you should get a phrase; format it into `acnctf{lowercase_with_underscores}`.

---

## How to solve
1. Inspect `challenge/ciphertext.txt`.  
2. Use the hint(s) if necessary.  
3. Use any Vigenère decoder (online or local) to try the key.  
4. Convert the decoded phrase to lower-case and replace spaces with underscores between the braces.

---

## Hints
- Hint 1 is intentionally small; ask for Hint 2 if you get stuck.
