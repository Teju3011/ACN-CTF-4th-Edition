#!/usr/bin/env python3
# solver_vigenere.py - quick Vigenere decrypt helper
import string

ALPHA = string.ascii_uppercase

def vigenere_decrypt(ciphertext, key):
    res = []
    ki = 0
    key = key.upper()
    for ch in ciphertext:
        if ch.upper() in ALPHA:
            cidx = ALPHA.index(ch.upper())
            kidx = ALPHA.index(key[ki % len(key)])
            pidx = (cidx - kidx) % 26
            res.append(ALPHA[pidx])
            ki += 1
        else:
            res.append(ch)
    return "".join(res)

if __name__ == "__main__":
    ct = "RCVPKFQYFVMNDRQGR"
    key = "RAIN"
    pt = vigenere_decrypt(ct, key)
    print("Ciphertext:", ct)
    print("Key:", key)
    print("Plaintext:", pt)
    # produce flag in acnctf{} format (lowercase, underscores)
    if pt.startswith("ACNCTF{") and pt.endswith("}"):
        inner = pt[len("ACNCTF{"):-1]
        flag = "acnctf{" + inner.lower().replace(" ", "_") + "}"
        print("Flag:", flag)
