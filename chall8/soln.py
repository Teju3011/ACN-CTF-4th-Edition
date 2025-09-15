import sys

# Preset byte array used in scrambled key generation (same as C challenge)
PRESET_VALS = [
    63, -94, 29, 87, -119, -61, 78, 114, -71, -40,
    -6, 6, 52, 92, -99, -31, 35, 103, -85, -115,
    69, -14, -58, 56, 126, -112, -47, 90, -73, -17,
    44, -127, -92, 111, 57, -56, -38, -11, 11, 125,
    -111, -26, 66, 58, -51, 117, -6
]

def rotate_left_16(value, count):
    return ((value << count) & 0xFFFF) | (value >> (16 - count))

def generate_scrambled_key(mask_key):
    result = []
    for i, val in enumerate(PRESET_VALS):
        # Convert val to byte (signed to unsigned)
        val_byte = val if val >= 0 else val + 256
        b = val_byte ^ ((mask_key >> (i % 8)) & 0xFF)
        result.append(b)
    return result

def xor_byte_with_mask(data, mask_key):
    mask = mask_key & 0xFF
    return bytes([b ^ mask for b in data])

def xor_with_key_transformation(data, key):
    res = bytearray(len(data))
    for i in range(len(data)):
        val = data[i] ^ key[i % len(key)]
        val = (~val & 0xFF) ^ ((i * 13) & 0xFF)
        res[i] = val
    return bytes(res)

def xor_transform(data, key):
    res = bytearray(len(data))
    for i in range(len(data)):
        res[i] = data[i] ^ key[i % len(key)]
    return bytes(res)

def hex_decode(s):
    return bytes.fromhex(s.strip())

def try_decrypt(cipher_hex, mask_key):
    cipher_bytes = hex_decode(cipher_hex)
    scrambled_key = generate_scrambled_key(mask_key)

    # Reverse step 3 (final xor_transform)
    step3 = xor_transform(cipher_bytes, scrambled_key)

    # Reverse step 2 (xor_with_key_transformation)
    # Need to invert: decrypted[i] = (~(encrypted[i] ^ key) ^ (i*13))
    # Rearranged: encrypted[i] = ~ (decrypted[i] ^ (i*13)) ^ key
    # We invert by:
    step2 = bytearray(len(step3))
    for i in range(len(step3)):
        step2[i] = (~(step3[i] ^ (i * 13) & 0xFF) & 0xFF)

    # step2[i] = step1[i] ^ scrambled_key[i % len]
    # So step1[i] = step2[i] ^ scrambled_key[i % len]
    step1 = bytearray(len(step2))
    for i in range(len(step2)):
        step1[i] = step2[i] ^ scrambled_key[i % len(scrambled_key)]

    # Reverse step 1 (xor_byte_with_mask)
    flag_bytes = bytes([b ^ (mask_key & 0xFF) for b in step1])

    return flag_bytes

def is_readable_flag(s):
    # Basic check: printable ASCII and starts with standard flag format
    try:
        text = s.decode('utf-8')
    except UnicodeDecodeError:
        return False
    if text.startswith("ACNCTF{") and text.endswith("}") and all(32 <= c < 127 for c in s):
        return True
    return False

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <encrypted_hex_string>")
        return

    cipher_hex = sys.argv[1]
    print("[*] Starting brute force for mask_key in range 0-65535")

    for mask_key in range(0, 65536):
        flag_bytes = try_decrypt(cipher_hex, mask_key)
        if is_readable_flag(flag_bytes):
            print(f"[+] Potential flag found with mask_key={mask_key:#06x}:")
            print(flag_bytes.decode('utf-8'))
            break
    else:
        print("[-] No valid flag found with tested mask keys.")

if __name__ == "__main__":
    main()
