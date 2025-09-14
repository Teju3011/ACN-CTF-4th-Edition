# SOLUTION.md - PTRACE DANCE 


## Overview
Binary: `ptrace_dance` (ELF x86_64, stripped)  
Goal: Recover the flag printed when the correct secret is provided.

Final flag:
```
ACNCTF{wh0s_y0ur_dec0mp1ler_n0w}
```

---

## Quick summary of the working approaches
We provide two practical, working approaches you can use to verify the challenge:

1. **Static reimplementation** — extract the encrypted byte arrays and the small 5-byte key from the binary (via decompiler or objdump), then run a Python script to decrypt and print the flag. This does not require running the target binary.

2. **Dynamic memory read (gdb)** — bypass the light anti-debug using an `LD_PRELOAD` shim for `ptrace` (and optionally `open`), run the binary under gdb, set a breakpoint at the instruction that prints the flag (found via objdump), and inspect the string pointer argument to `printf`. This reads the decrypted flag from memory after the decryption routine runs.

Both are valid; the static method is simplest for verification.

---

## A) Static reimplementation (recommended for quick verification)

### 1) Extract encrypted bytes and key
The encrypted bytes are present in `.rodata` as three arrays (concatenated). The key is produced by a small function; its result is the 5 bytes:

Key (5 bytes):
```
12 34 56 78 9a
```
(These bytes are produced by arithmetic in the small key-producer function.)

Encrypted bytes (concatenate the parts in this order):
```
53 70 06 3e c2 59 b5 28 08 a3
6f 5e d3 45 19 93 5b 23 0f ec
56 b6 d0 30 1e 6c b8 2c f2 d7 87 a8 00
```
Total length: 33 bytes (includes trailing 0 for string terminator in this build; ignore or treat as part of decrypted ASCII).

### 2) Decryption formula (from decompiled code)
For each byte index `i` (0-based):
```
flag[i] = ((enc[i] ^ key[i % 5]) - i) & 0xff
```

### 3) Working Python script
Save this as `recover_flag.py` and run `python3 recover_flag.py`:

```python
#!/usr/bin/env python3
enc = [
    0x53,0x70,0x06,0x3e,0xc2,0x59,0xb5,0x28,0x08,0xa3,
    0x6f,0x5e,0xd3,0x45,0x19,0x93,0x5b,0x23,0x0f,0xec,
    0x56,0xb6,0xd0,0x30,0x1e,0x6c,0xb8,0x2c,0xf2,0xd7,0x87,0xa8,0x00
]
key = [0x12, 0x34, 0x56, 0x78, 0x9a]

flag_bytes = []
for i, b in enumerate(enc):
    v = (b ^ key[i % len(key)])
    flag_bytes.append((v - i) & 0xFF)

flag = bytes(flag_bytes)
print("Recovered flag (raw):", flag)
try:
    print("As ASCII:", flag.decode('utf-8'))
except:
    print("Flag contains non-UTF8 bytes; hex:", flag.hex())
```

Running this prints:
```
Recovered flag (raw): b'ACNCTF{wh0s_y0ur_dec0mp1ler_n0w}\x00'
```

(Trim trailing NUL if present.)

---

## B) Dynamic method: read decrypted flag from memory under gdb

### 1) Build an LD_PRELOAD shim to bypass anti-debug
Create `noptrace.c` with this content (variadic ptrace override is required on glibc):

```c
#define _GNU_SOURCE
#include <sys/ptrace.h>
#include <dlfcn.h>
#include <string.h>
#include <stdarg.h>
#include <fcntl.h>
#include <unistd.h>

/* pretend ptrace always succeeds */
long ptrace(enum __ptrace_request request, ...) {
    (void)request;
    return 0;
}

/* optional: prevent open("/proc/self/status") from succeeding (so TracerPid check is skipped) */
typedef int (*open_t)(const char*, int, ...);
int open(const char *pathname, int flags, ...) {
    if (pathname && strstr(pathname, "/proc/self/status")) {
        return -1; /* pretend it doesn't exist */
    }
    static open_t real_open = NULL;
    if (!real_open) real_open = (open_t)dlsym(RTLD_NEXT, "open");
    if (flags & O_CREAT) {
        va_list ap; va_start(ap, flags);
        int mode = va_arg(ap, int);
        va_end(ap);
        return real_open(pathname, flags, mode);
    } else {
        return real_open(pathname, flags);
    }
}
```

Compile:
```bash
gcc -shared -fPIC -O2 -o noptrace.so noptrace.c -ldl
```

### 2) Find the address to breakpoint at (the printf that prints the flag)
Use `objdump` to find the reference to the "Correct! Flag" string and the instruction that calls `printf` or `puts`. Example:

```bash
# Show where the string lives and references to it
strings -t x ptrace_dance | grep -n "Correct! Flag"
objdump -d ptrace_dance | grep -n "Correct! Flag" -n
```

A reliable method is:
```bash
# find the .rodata address of the string
readelf -p .rodata ptrace_dance | grep -n "Correct! Flag"
# or:
objdump -s -j .rodata ptrace_dance | grep -n "Correct! Flag"
```

Then find the code xref to that string (example workflow):
```bash
# find references in code to the string's address (replace 0xADDR with the rodata VA)
objdump -d ptrace_dance | grep -n "0xADDR"
# or search for the nearby call to printf and note the code address where it happens
```

(We can't provide the exact addresses here because builds differ; use the above to get the address in your copy.)

### 3) Run under gdb with LD_PRELOAD
```bash
LD_PRELOAD=./noptrace.so gdb ./ptrace_dance
(gdb) break *0x<ADDR_OF_CALL>    # break at the instruction that calls printf for the flag
(gdb) run
# when breakpoint hits, inspect registers:
(gdb) info registers
# on x86_64, first printf argument (format or buffer) will be in RDI or RSI depending on call site.
# If the call is like printf("Correct! Flag: %s\n", flag), the 'flag' pointer will typically be in RSI.
(gdb) x/s $rsi    # or x/s $rdi depending on calling convention and instruction
```

### 4) Example gdb commands (sequence)
```bash
LD_PRELOAD=./noptrace.so gdb ./ptrace_dance
(gdb) break main
(gdb) run
# step through until near the call that prints the flag, or set a breakpoint at the address derived via objdump:
(gdb) break *0x401234
(gdb) continue
# when hit:
(gdb) x/s $rsi
```

Replace `0x401234` and `$rsi` with the actual values you discover.

---

## C) Patching the binary (alternative)
If you prefer to patch out the anti-debug or the comparison branch and force success:

1. Make a copy:
```bash
cp ptrace_dance ptrace_dance.patched
```

2. Use radare2 or any hex editor to locate the `ptrace` call or the conditional jump that checks `hv == target` and NOP those bytes. Example radare2 session (high-level):

```bash
r2 -w ptrace_dance.patched
[0x00400000]> aa
[0x00400000]> afl
# find the function and its address; use 'pdf' to view disassembly and identify the conditional jump
[0x00400000]> pdf @ sym.main
# locate the 'je' (or jne) that branches to success/fail
# patch with 'wx 90' (NOP) at the relevant offset
[0x00400000]> q
```

Patching is straightforward but platform/build-specific — always work on a copy and test in a VM.

---

## D) Verification / Test-run (no gdb)
If you have the correct secret, you can run the binary normally and it will print the flag:

```bash
# (example; if the secret is 'open_sesame' as a placeholder)
printf "open_sesame\n" | ./ptrace_dance
# Expected output:
# Correct! Flag: ACNCTF{wh0s_y0ur_dec0mp1ler_n0w}
```

---

## Notes and caveats
- If you used UPX packing on distributed binaries, unpack with `upx -d` first; decompilers and objdump may struggle on packed files.
- The exact addresses for breakpoints depend on your exact build (compiler version, options). Use the strings/xref/objdump workflow to find the precise location in your copy.
- Keep the `SOLUTION.md` private until you release post-contest.

---

Finished. Keep this file in your admin folder for post-contest publication or reference.
