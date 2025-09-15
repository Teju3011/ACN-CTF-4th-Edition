# Challenge Title  

**XORtificate of Obfuscation**
## Challenge Description  
We've intercepted a binary that applies a proprietary, multi-layered bit-mixing algorithm to sensitive data. The output is all we have. The encryption key is small, but the layers are intertwined. Prove you can peel them back.

---
### **Challenge Writeup: XOR Layer Reversal**

**Challenge:** XORtificate of Obfuscation
**Category:** Reverse Engineering
**Provided File:** `output.txt`

#### **1. Analysis Summary**

The target binary implements a custom encryption routine with three distinct layers of XOR-based transformations. The core logic, after unpacking the UPX-packed binary, reveals the following sequential process applied to the input flag:

1.  **Initial XOR:** Each byte of the flag is XORed with the least significant byte (LSB) of a dynamically generated 16-bit mask key.
2.  **Scrambling Layer:** The output from layer 1 is processed with a preset scrambling key array. For each byte `i`, the operation is: `data[i] = (data[i] ^ scrambling_key[i]) + i & 0xFF`. The `+ i` operation introduces an index-dependent shift.
3.  **Final XOR:** The result from layer 2 is XORed again with the same scrambling key used in the previous layer.

The encrypted output is then hex-encoded and written to `output.txt`.

#### **2. Solution Plan**

The solution requires reversing each encryption layer in the opposite order. The 16-bit mask key is not stored and must be brute-forced.

**Step 1: Data Preparation**
Hex-decode the contents of `output.txt` to obtain the raw ciphertext byte array `c`.

**Step 2: Reverse Layer 3 (Final XOR)**
Since the third layer is a simple XOR with the scrambling key `s`, it is reversed by repeating the operation: `layer2_out[i] = c[i] ^ s[i]`.

**Step 3: Reverse Layer 2 (Scrambling Layer)**
This layer is the most complex to reverse. The forward operation is:
`layer2_out[i] = (layer1_out[i] ^ s[i]) + i) & 0xFF`

To reverse it, we must solve for `layer1_out[i]`:
1.  First, reverse the addition by performing a subtraction modulo 256: `temp = (layer2_out[i] - i) & 0xFF`
2.  Then, reverse the XOR: `layer1_out[i] = temp ^ s[i]`

**Step 4: Reverse Layer 1 (Initial XOR) & Key Recovery**
The first layer is a XOR with the LSB of the 16-bit mask key `k`: `layer1_out[i] = flag[i] ^ (k & 0xFF)`.

The scrambling key array `s` is derived from this same 16-bit key `k` and a preset array. Therefore, the entire decryption process depends on guessing the correct value of `k` (0x0000 to 0xFFFF). The solution is to iterate over all 65536 possible keys.

**Algorithm:**
For each candidate key `key` in range(0, 65536):
1.  Reconstruct the known scrambling key array `s` based on `key`.
2.  Decrypt the ciphertext `c` by reversing layers 3 and 2 as described.
3.  Reverse layer 1: `potential_flag_byte = decrypted_layer1_byte ^ (key & 0xFF)`
4.  Check if the resulting string is entirely printable ASCII and contains the expected flag format (e.g., `CTF{...`). The correct key will yield a coherent flag.

#### **3. Conclusion**

The encryption's security relies on the obscurity of the custom algorithm rather than key strength. The 16-bit key space is small enough for a brute-force attack once the reversible nature of each transformation is understood. The solution involves a straightforward script to iterate through all possible keys, applying the reversed operations to the ciphertext until a valid plaintext is found.