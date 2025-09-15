#!/usr/bin/env python3
import json
import hashlib
import os

BASE_DIR = os.path.dirname(__file__)
TX_FILE = os.path.join(BASE_DIR, "transactions.json")

def derive_identifier(mnemonic: str) -> str:
    return hashlib.sha256(mnemonic.encode()).hexdigest()[:32]

def main():
    mnemonic = input("Enter your recovered mnemonic: ").strip()
    ident = derive_identifier(mnemonic)

    if not os.path.exists(TX_FILE):
        print("[!] transactions.json not found.")
        return

    with open(TX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if ident in data:
        print("[+] Flag recovered:", data[ident])
    else:
        print("[!] No flag found for this mnemonic.")
        print("Identifier:", ident)

if __name__ == "__main__":
    main()
