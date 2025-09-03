## Challenge: **Obfuscated Gateway**

**Category:** Reverse Engineering  
**Difficulty:** Easy/Medium

### Description

You've stumbled upon a locked terminal protected by a mysterious program. It seems the developer tried to hide the secret key and the precious flag within the code, but not well enough. The binary taunts you with a fake flag: `flag{N2gxNV8xNV9uMHRfN2gzX2ZsNGdfN2gwdWdo}`.

Your mission is to pass the password check and reveal the **true flag** hidden within the program's obfuscated layers.

**Download:** `chall2_rev.exe`

---

### Solution

The provided program is a C++ binary that asks for a password. If the correct password is given, it prints the real flag.

#### Step 1: Static Analysis - Understanding the Obfuscation

The core of the challenge is that the real password (`7h15_15_n0t_7h3_fl4g_7h0ugh`) and the real flag (`ACNCTF{...}`) are not stored as plain text strings in the binary. Instead, they are broken into 4-byte chunks, each byte is XORed with the key `0x4A`, and then the result is packed into 32-bit integers.

The `decode` function reverses this process:
1. It takes each 32-bit integer from the array.
2. It extracts each byte (shifting: 24, 16, 8, 0 bits).
3. It XORs each byte with the key `0x4A` to get the original character.
4. It reconstructs the original string.

The strings are only assembled in memory at runtime when the `decode` function is called.

#### Step 2: Dynamic Analysis - Extracting the Strings

Since the decoding function is present in the binary, the easiest way to solve this is to debug the program and extract the password and flag after they are decoded into memory.

**Using a Debugger (x64dbg/Ghidra/Cutter):**

1.  **Locate the Decode Function:** The `decode` function is the key. Set a breakpoint on its return statement or any point after it has finished executing.
2.  **Find the Decoded Strings:** After the `decode` function runs, the result (the plain text string) will be stored in a variable on the stack or in a register.
    *   The password is decoded first and stored in a variable.
    *   The flag is decoded second and stored in another variable.
3.  **Inspect Memory:** When the breakpoint is hit, simply inspect the memory address pointed to by the return value (often stored in the `RAX` register on x64) to see the decoded string.

**Simpler Approach - Patching the Binary:**

Another straightforward method is to patch the binary's execution flow to print the flag regardless of the password check.

1.  **Locate the Jump Instruction:** Find the conditional jump (`jne` or `je`) that follows the password comparison (`strcmp` or similar).
2.  **Patch the Jump:** Change the jump instruction to its opposite or to a `nop` (no operation) to force the program to always take the path that prints the real flag.

For example, changing:
```asm
JNE SHORT 00401589 ; Jump to "Incorrect password" if not equal
```
to:
```asm
NOP
NOP               ; Effectively do nothing, allowing execution to continue to the flag print.
```

#### Step 3: The Answer

By either debugging the program or patching it, we can recover the real flag without knowing the password initially.

**Password:** `7h15_15_n0t_7h3_fl4g_7h0ugh`  
**Real Flag:** `ACNCTF{N0w th15 1s teh Fl4g. C0ngr4tz!}`

---

### Explanation

The developer's mistake was including the decoding routine within the binary itself. While the strings were obfuscated in the static binary (making `strings` or a simple hex dump useless), the necessary logic to deobfuscate them was present and accessible at runtime.

This challenge demonstrates a fundamental principle in reverse engineering: **obfuscation is not encryption**. If the client possesses the algorithm and the key, so does the reverse engineer. The XOR operation is trivial to reverse if the key is known, and in this case, the key was hardcoded (`0x4A`), making the obfuscation merely a speed bump.

**Flag:** `ACNCTF{N0w th15 1s teh Fl4g. C0ngr4tz!}`
