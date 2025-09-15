### **Challenge Title**

**The MOVing Target**

### **Challenge Description**

We've recovered a strange validator program from a target system. It's been compiled into an almost unrecognizable form, and it seems to be waiting for a specific key. It's sluggish to test inputs manually. Your mission is to find a way to trigger its success condition without guessing.

**File provided:** `chall`

### **Challenge Writeup**
**Category:** Reverse Engineering
**Techniques:** XOR Decoding, Dynamic Analysis, Binary Patching

#### **1. Analysis Summary**

The binary is a password validator where the correct password and the target flag are both stored in a single-byte XOR-encoded format (key: `0x5A`). The core verification logic performs a byte-by-byte comparison between the user's input and the decoded password. The flag is decoded and printed only upon a successful match.

Key characteristics of the binary:
*   **Obfuscation:** The code is heavily obfuscated using the Movfuscator compiler, which translates all instructions into `MOV` operations, complicating static analysis.
*   **Anti-Brute-Force:** Dummy delay loops are inserted to intentionally slow down execution, making a naive brute-force attack impractical.
*   **Data Hiding:** No plaintext strings are present in the binary. The encoded password and flag are stored as data bytes.
*   **Hint:** An unused, encoded string decodes to `"7_chars"`, indicating the required password length.

#### **2. Solution Plan**

Two primary methods exist to solve this challenge.

**Method 1: Controlled Brute-Force (Theoretical but Inefficient)**
Due to the runtime delays, a full 7-character brute-force (e.g., ~95^7 possibilities) is computationally infeasible. A more targeted approach would be to brute-force one character at a time by analyzing the program's behavior (e.g., timing differences or exit codes), but the obfuscation and delays make this complex.

**Method 2: Dynamic Analysis and Patching (Recommended)**
This is the most efficient solution. The goal is to bypass the password check entirely.

1.  **Deobfuscation Preparation:** Use a tool like `demovofuscate` to symbolically execute the binary and simplify the control flow graph, making it easier to analyze in a disassembler.
2.  **Locate Critical Functions:** Load the (deobfuscated) binary into a debugger (e.g., GDB with GEF/PEDA, or x64dbg). The critical points to find are:
    *   The XOR decoding routine for the stored password.
    *   The XOR decoding routine for the flag.
    *   The `strcmp` or byte-wise comparison function.
3.  **Extract the Encoded Data:** The encoded password and flag are stored as static arrays of bytes. These can be extracted directly from the binary's data section once located.
4.  **Decode the Data:** Since the XOR key (`0x5A`) is known, the solution can be achieved without execution. Decode all bytes in the suspected data arrays to reveal the plaintext password and flag.
    *   `plaintext_byte = encoded_byte XOR 0x5A`
5.  **Patching (Alternative):** Instead of decoding offline, the binary can be patched to circumvent the check. This can be done by:
    *   **NOP-ing the Check:** Overwriting the jump after the comparison instruction to always jump to the success branch.
    *   **Direct Printing:** Modifying the program's flow to jump directly to the flag decoding and printing routine, regardless of input.

**Solution:**
The correct password is `javabad`, which will yield the flag: `ACNCTF{M0vfusc470r_R3duc7i0_Fl4g}`

#### **3. Conclusion**

The challenge's security relies on obfuscation (Movfuscator) and steganography (XOR-encoding) rather than cryptographic strength. The single-byte XOR is trivial to break once the encoding scheme is identified. The primary obstacle is the obfuscated control flow, which is effectively mitigated using dynamic analysis tools and debugger-assisted exploration. The solution involves directly extracting and decoding the XOR-encoded data segments or patching the binary to force the correct execution path.
