#!/usr/bin/env python3
import itertools
import os

BASE_DIR = os.path.dirname(__file__)
CORRUPTED = os.path.join(BASE_DIR, "corrupted_mnemonic.txt")
CANDIDATES = os.path.join(BASE_DIR, "candidates.txt")

def read_corrupted(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip().split()

def read_candidates(path):
    with open(path, "r", encoding="utf-8") as f:
        return [w.strip() for w in f if w.strip()]

def main():
    words = read_corrupted(CORRUPTED)
    candidates = read_candidates(CANDIDATES)
    blank_positions = [i for i, w in enumerate(words) if w == "____"]

    print(f"[+] Corrupted mnemonic: {' '.join(words)}")
    print(f"[+] Blank positions: {blank_positions}")
    print(f"[+] Candidate words count: {len(candidates)}")

    found = []
    for combo in itertools.product(candidates, repeat=len(blank_positions)):
        attempt = words[:]
        for pos, word in zip(blank_positions, combo):
            attempt[pos] = word
        candidate_mn = " ".join(attempt)

        # keep ALL candidates, no strict BIP39 check
        if candidate_mn.startswith("emotion board") and "nerve" in candidate_mn:
            print("="*60)
            print("[+] Likely mnemonic found:")
            print(candidate_mn)
            found.append(candidate_mn)

    if not found:
        print("[!] No mnemonic matched heuristic.")
    else:
        print(f"[+] Total found: {len(found)}")

if __name__ == "__main__":
    main()
