#!/usr/bin/env python3
import json
import hashlib
import os
import sys

BASE_DIR = os.path.dirname(__file__)
TX_FILE = os.path.join(BASE_DIR, "transactions.json")

def derive_identifier(mnemonic: str) -> str:
    return hashlib.sha256(mnemonic.encode()).hexdigest()[:32]

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} \"<mnemonic>\" \"<flag>\"")
        sys.exit(1)

    mnemonic, flag = sys.argv[1], sys.argv[2]
    ident = derive_identifier(mnemonic)

    # load or create mapping file
    if os.path.exists(TX_FILE):
        with open(TX_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    data[ident] = flag

    with open(TX_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("[+] transactions.json created/updated")
    print(f"[+] Identifier: {ident}")
    print("[+] Flag saved (organizer only).")

if __name__ == "__main__":
    main()
