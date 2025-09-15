import base58

key = 100_000_000
key_bytes = key.to_bytes(4, 'big')
flag_segments = []

with open("addresses.txt") as f:
    for addr in f:
        decoded = base58.b58decode_check(addr.strip())
        payload = decoded[1:]  # remove version byte
        original = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(payload)])
        flag_segments.append(original.decode('utf-8'))

flag = "".join(flag_segments)
print("Flag:", flag)
