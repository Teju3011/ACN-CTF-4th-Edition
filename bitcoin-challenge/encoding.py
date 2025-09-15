import base58, hashlib

flag_segments = [
    b"acnctf{",
    b"bitcoin",
    b"_whisper",
    b"_uncover",
    b"ed}"
]

key = 100_000_000
key_bytes = key.to_bytes(4, 'big')
addresses = []

for seg in flag_segments:
    # XOR segment
    xored = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(seg)])
    # Prepend version byte
    payload = b'\x00' + xored
    # Compute checksum
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    # Full payload
    full_payload = payload + checksum
    # Base58 encode
    addr = base58.b58encode(full_payload).decode()
    addresses.append(addr)

with open("addresses.txt", "w") as f:
    f.write("\n".join(addresses))

print("Addresses:", addresses)
