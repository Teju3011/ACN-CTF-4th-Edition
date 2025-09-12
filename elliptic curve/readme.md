
Challenge Type: Elliptic Curve / RNG / Timing Attack / CTF Cryptanalysis [hard]
Files provided:

satellite_pub.pem → satellite’s long-term public key

ephemeral_pubs/msgX_pub.pem → ephemeral public keys for each message

ciphertexts/msgX.enc → encrypted messages

timing_leaks/msgX_hw.txt → simulated Hamming weight of ephemeral private keys

Goal: Recover the flag in msg9.enc. Flag format: acnctf{...}

1. Understanding the challenge

The satellite communication uses ephemeral ECDH keys for each message. Each ephemeral key is generated from a weak 32-bit LFSR.

Key observations:

Ephemeral public keys are provided, but private keys are hidden.

Each ephemeral private key leaks partial information via the Hamming weight (simulated timing leak).

The last message contains the flag.

The challenge simulates a real-world side-channel attack scenario: you know some information about ephemeral private keys but must reconstruct them to decrypt messages.

2. Analyzing the leak

Each ephemeral private key k is generated as 256-bit integers from a weak 32-bit LFSR.

The Hamming weight of k is given in timing_leaks/msgX_hw.txt.

Hamming weight gives a partial bitwise oracle:

It reveals the number of bits set to 1 in the private key.

It’s noisy but narrows the possible values of k.

3. Reconstructing ephemeral private keys

Participants can attempt to recover ephemeral keys using two approaches:

Brute-force / seed guessing:

LFSR has 32-bit seed, giving 2^32 possible starting states.

For each candidate seed, you can simulate the LFSR to generate ephemeral private keys.

Check if the Hamming weight matches the timing leak.

Feasible because 2^32 is large but manageable with some optimization.

Partial key recovery + lattice attacks:

Use Hamming weight to get partial bits of k.

Cast it as a Hidden Number Problem (HNP):

You know R = k * G (ephemeral public key).

Some bits of k are known (from Hamming weight).

Solve for the unknown bits using lattice techniques (LLL).

Either method allows reconstruction of ephemeral private keys without knowing the full seed.

4. Deriving shared secrets

Once the ephemeral private key k is recovered:

Compute shared secret using ECDH:
shared_secret = ephemeral_priv.exchange(ec.ECDH(), sat_pub)
Derive symmetric key using HKDF:
derived_key = HKDF(hashes.SHA256(),
                   length=len(ciphertext),
                   salt=None,
                   info=b"leo").derive(shared_secret)
5. Decrypting the flagged message

The ciphertext is a simple XOR of the plaintext and the derived key:
plaintext = bytes([ct[i] ^ derived_key[i] for i in range(len(ct))])
If the ephemeral key is correct, the decrypted plaintext starts with acnctf{…}.
6.Challenges / difficulty

The timing leak is noisy — Hamming weight only gives partial info.

The LFSR seed is unknown → participants must guess or reduce the seed space.

Requires cryptanalysis techniques: HNP, lattice attacks, or side-channel reasoning.
7. Key Takeaways

Weak RNG + ephemeral key leaks → realistic side-channel scenario.

Partial information (Hamming weight) can be exploited to recover ephemeral private keys.

Lattice / HNP attacks are essential for solving large-scale biased key problems.

This challenge demonstrates real-world crypto pitfalls: ephemeral keys must be truly random, and timing leaks can be catastrophic.

8. Solution outline (without giving ephemeral key)

Read timing leaks to extract Hamming weight of ephemeral keys.

Simulate LFSR to generate candidate ephemeral private keys.

Match Hamming weight to reduce candidate keys.

Use ephemeral public key to verify the candidate private key.

Compute shared secret → HKDF → derived key → decrypt ciphertext.

Extract the flag: acnctf{echoes_from_the_leo_satellite}

✅ Flag (for verification)
acnctf{echoes_from_the_leo_satellite}


Solution script:
"""
attack_recover_flag_ctf_solution.py

Full solution for the CTF-ready "Echoes from the LEO" challenge.
Automatically reconstructs ephemeral keys using the known LFSR seed,
derives shared secrets, and decrypts the flagged message.
"""

import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# ------------------------------
# Helpers
# ------------------------------
def lfsr32(state):
    """32-bit LFSR with polynomial x^32 + x^22 + x^2 + 1"""
    bit = ((state >> 31) ^ (state >> 21) ^ (state >> 1) ^ state) & 1
    return ((state << 1) | bit) & 0xFFFFFFFF

def generate_ephemeral_int(state):
    """Generate 256-bit ephemeral int using LFSR"""
    k = 0
    for _ in range(8):  # 8 * 32 = 256 bits
        state = lfsr32(state)
        k = (k << 32) | state
    return k, state

# ------------------------------
# Config
# ------------------------------
OUTDIR = "challenge_ctf"
NUM_MESSAGES = 10
FLAG_MSG_INDEX = NUM_MESSAGES - 1
LFSR_SEED = 0x12345678  # known only to solution
FLAG_LENGTH = 41  # length of acnctf{...}

# ------------------------------
# Step 1: Load satellite public key
# ------------------------------
with open(os.path.join(OUTDIR, "satellite_pub.pem"), "rb") as f:
    sat_pub = serialization.load_pem_public_key(f.read())

# ------------------------------
# Step 2: Reconstruct ephemeral private keys
# ------------------------------
state = LFSR_SEED
ephemeral_privs = []

for i in range(NUM_MESSAGES):
    eph_int, state = generate_ephemeral_int(state)
    ephemeral_priv = ec.derive_private_key(eph_int, ec.SECP256R1())
    ephemeral_privs.append(ephemeral_priv)

# ------------------------------
# Step 3: Load flagged ciphertext
# ------------------------------
cipher_file = os.path.join(OUTDIR, f"ciphertexts/msg{FLAG_MSG_INDEX}.enc")
with open(cipher_file, "rb") as f:
    ct = f.read()

# ------------------------------
# Step 4: Derive shared secret and HKDF key
# ------------------------------
flag_priv = ephemeral_privs[FLAG_MSG_INDEX]
shared_secret = flag_priv.exchange(ec.ECDH(), sat_pub)

derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=len(ct),
    salt=None,
    info=b"leo",
).derive(shared_secret)

# ------------------------------
# Step 5: Decrypt XOR
# ------------------------------
plaintext = bytes([ct[i] ^ derived_key[i] for i in range(len(ct))])

# ------------------------------
# Step 6: Display result
# ------------------------------
if plaintext.startswith(b"acnctf{"):
    print("[+] Recovered flag:", plaintext.decode())
else:
    print("[!] Decryption failed. Raw bytes:", plaintext)
