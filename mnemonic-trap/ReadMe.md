# Mnemonic Trap — Challenge folder

## Overview
A 12-word BIP39 mnemonic has been corrupted: three words are replaced with `____`. Use the provided `candidates.txt` to brute-force the blanks. Only the exact original mnemonic passes the BIP39 checksum. When recovered, derive the seed-based identifier and lookup the flag (organizer places `transactions.json` on the server).

## Files
- corrupted_mnemonic.txt — the 12-word mnemonic with `____` blanks
- candidates.txt — candidate words (one per line)
- brute_mnemonic.py — brute-force utility for players
- derive_flag.py — derive identifier and lookup flag (needs transactions.json on server)
- generate_mapping.py — ORGANIZER ONLY: create transactions.json from secret mnemonic & flag
- get_flag.py — organizer convenience to test mapping locally
- test_flow.py — optional local test harness to verify end-to-end

## Player quickstart
1. Install dependencies:
   ```bash
   cd challenge
   python -m pip install --user -r requirements.txt
