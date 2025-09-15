\## Challenge Write-Up: Hidden Key Validator

A runtime password checker hides both the key and reward using simple encoding and heavy obfuscation. Static analysis won’t reveal secrets easily, and brute force is deliberately slowed down. Solve it by carefully analyzing the binary’s behavior and uncovering the correct input to unlock the hidden content.

\### Summary



This challenge implements a password verification program where both the password and the flag are stored only as XOR-encoded bytes. The program verifies the input password byte-by-byte at runtime and reveals the flag only if the password matches exactly. Neither the plaintext password nor flag appears as static strings in the binary.



\### Key Features



\- XOR encoding with a single-byte key (0x5A) hides password and flag strings.

\- Runtime bytewise decoding and comparison.

\- Runtime dummy delay loops reduce brute-force speed.

\- Compatible with movfuscator tool for heavy instruction-level obfuscation.

\- An unused hidden string hints that the password length is 7.



\### How to Solve



There are two primary approaches:



1\. \*\*Brute Force:\*\*  

&nbsp;  The runtime delay slows brute forcing, but with enough time and optimization, trying all 7-character combinations can eventually find the correct password.



2\. \*\*Dynamic Analysis \& Patching:\*\*  

&nbsp;  - Use a disassembler/debugger to analyze the movfuscated binary.  

&nbsp;  - Identify where the XOR decoding and comparison happen.  

&nbsp;  - Patch the binary to bypass the password check or to reveal the flag directly.  

&nbsp;  - A helpful tool for this is the \[`demovofuscate`](https://github.com/xoreaxeaxeax/demovofuscate) GitHub repository, which provides scripts for deobfuscating movfuscator-obfuscated binaries.



\### Conclusion



This challenge prevents simple static extraction by encoding secrets and complicates analysis via movfuscator obfuscation. Breaking it requires either patient brute forcing slowed by deliberate delays or sophisticated reverse engineering and binary patching, aided by tools like demovofuscate.

