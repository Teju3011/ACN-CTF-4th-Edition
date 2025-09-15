# Bitcoin Whisper - CTF Challenge

**Difficulty:** Hard  
**Category:** Cryptography / Bitcoin

## Description

The blockchain doesn’t just move coins. Sometimes it whispers secrets.  

A mysterious hacker has hidden a secret inside a series of Bitcoin addresses. Each address contains part of the flag. But it’s encrypted — only those who understand the language of Bitcoin and its hidden codes can uncover it.  

Decode the addresses, reveal the hidden segments, and reconstruct the secret.  


“A mysterious hacker has hidden a secret inside a series of Bitcoin addresses. Each address contains part of the flag. Decode the addresses, reveal the hidden segments, and reconstruct the secret. The flag format is acnctf{…}.”

**Files Provided:**  
- `addresses.txt` : A list of Bitcoin addresses containing hidden flag segments.

## Rules

- Combine the segments in order.  
- XOR is the secret handshake; the key is hidden in a puzzle.  
- Final flag format: `acnctf{…}`

Good luck, detective.  

## Hint
The secret lives where coins sleep.  
Count what you cannot spend: 100 million of something tiny.  
The more you know, the less obvious it is.  
Read the addresses as messages, not money.  
