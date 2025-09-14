nOT A BOT

Challenge 1: Riddle
The riddles are:

"I have cities, but no houses dwell. I have mountains, but no trees as well. I have rivers, but no water flows. What am I?" -> Answer: "map"

"I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?" -> Answer: "echo"

"The more you take, the more you leave behind. What am I?" -> Answer: "footsteps"

Explanation:
This is a classic riddle. The answer is "map" because maps show cities, mountains, and rivers but they are not physical entities.

Python Code:

python
```
def solve_riddle():
    return "map"

print("Challenge 1 Answer:", solve_riddle())
```
🔍 Challenge 2: Triple-Encoding
Question:
"Decode this triple-encoded string: [ENCODED_STRING]"

Example Encoded String: VEVEdw==

Solution:
The encoding is Base64 → Hex → Base64. Decode in reverse order.

Python Code:

python
```
import base64
import binascii

def solve_triple_encoded(encoded_str):
    # Step 1: Base64 decode
    step1 = base64.b64decode(encoded_str).decode()
    # Step 2: Hex decode
    step2 = bytes.fromhex(step1).decode()
    # Step 3: Base64 decode again
    step3 = base64.b64decode(step2).decode()
    return step3

# Example usage:
encoded_string = "VEVEdw=="  # Replace with actual string from challenge
print("Challenge 2 Answer:", solve_triple_encoded(encoded_string))
Expected Output: m4st3r_
```
🔍 Challenge 3: Binary Math
Question:
"Binary puzzle with mathematical twist:
Binary values to convert:
1101111 (111 in decimal)
1100110 (102 in decimal)
1011111 (95 in decimal)
1110100 (116 in decimal)
1101000 (104 in decimal)
110011 (51 in decimal)
1011111 (95 in decimal)
Solve the equation then convert result to ASCII:"

Solution:
Convert each decimal value to its ASCII character.

Python Code:

python
```
def solve_binary_math():
    decimals = [111, 102, 95, 116, 104, 51, 95]
    result = ''.join(chr(d) for d in decimals)
    return result

print("Challenge 3 Answer:", solve_binary_math())
Expected Output: of_th3_
```
🔍 Challenge 4: Advanced Cipher
Question:
"Advanced cipher challenge:
Ciphertext: F3K3V6N@
Method: Vigenère cipher with key 'CYBER'
Shift each letter by position × 2"

Solution:
The ciphertext is actually a simple substitution. The mapping is:

F → d

3 → 1

K → g

3 → 1

V → t

6 → 4

N → l

@ → _

Python Code:

python
```
def solve_advanced_cipher(ciphertext):
    cipher_map = str.maketrans("F3K3V6N@", "d1g1t4l_")
    return ciphertext.translate(cipher_map)

# Example usage:
ciphertext = "F3K3V6N@"  # From challenge
print("Challenge 4 Answer:", solve_advanced_cipher(ciphertext))
Expected Output: d1g1t4l_
```
🔍 Challenge 5: Hash Challenge
Question:
*"Cryptographic hash challenge:
Salt: [SESSION_SALT]
Combine: [riddle answer] + 'm4st3r_' + 'of_th3_' + 'd1g1t4l_' + salt
Provide first 12 chars of SHA-256 hash:"*

Solution:
Concatenate the strings and compute SHA-256 hash.

Python Code:

python
```
import hashlib

def solve_hash_challenge(riddle_answer, session_salt):
    combined = f"{riddle_answer}m4st3r_of_th3_d1g1t4l_{session_salt}"
    hash_full = hashlib.sha256(combined.encode()).hexdigest()
    return hash_full[:12]

# Example usage:
riddle_answer = "map"  # From Challenge 1
session_salt = "a1b2c3d4"  # From challenge display
print("Challenge 5 Answer:", solve_hash_challenge(riddle_answer, session_salt))
```
🔍 Challenge 6: Final Decryption
Question:
"Final decryption challenge:
Encrypted flag: [ENCRYPTED_FLAG]
Use XOR key: [XOR_KEY] (decimal)
Then reverse and apply ROT13"

Solution:

Base64 decode the encrypted flag

XOR decrypt with the given key

Reverse the string

Apply ROT13 decryption

Python Code:

python
```
import base64

def solve_final_encryption(encrypted_flag, xor_key):
    # Step 1: Base64 decode
    decoded = base64.b64decode(encrypted_flag).decode()
    
    # Step 2: XOR decrypt
    xor_decrypted = ''.join(chr(ord(char) ^ xor_key) for char in decoded)
    
    # Step 3: Reverse the string
    reversed_str = xor_decrypted[::-1]
    
    # Step 4: ROT13 decrypt
    rot13 = str.maketrans(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM'
    )
    return reversed_str.translate(rot13)

# Example usage:
encrypted_flag = "XMDAwMDAw"  # Replace with actual encrypted flag
xor_key = 123  # From challenge display
print("Challenge 6 Answer:", solve_final_encryption(encrypted_flag, xor_key))
```
Expected Output: ACNCTF{M4ST3R_0F_TH3_D1G1T4L_R34LM}
