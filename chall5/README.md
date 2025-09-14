# Keyed Rotate

Welcome to the challenge!  
You’re given a Linux x86_64 binary that hides the flag. Your task is to reverse engineer the binary and recover the flag in the format:

ACNCTF{...}


---

## Challenge Description
The binary accepts an input string and performs multiple transformations before deciding if the secret is correct. The real flag is not stored in plaintext — instead, it is reconstructed at runtime using a hidden key and a simple cipher routine.

Your job is to reverse engineer the binary, understand how the decryption works, and recover the original flag.

---

## Hint
There is a tiny function that computes a 5-byte key and writes it into a local array (you may see names like `local_###` in the decompiler). The key is used to XOR (and then adjust) the encrypted bytes. A decompiler will make this function obvious.

---

## Notes
- Target platform: **Linux x86_64**
- Tools allowed: any reverse engineering suite (e.g., Ghidra, IDA, Binary Ninja, radare2, objdump, gdb)
- No source code is provided; you must work only with the compiled binary.

Goodluck.
