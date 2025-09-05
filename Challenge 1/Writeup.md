Challenge 1 – Hidden Portraits



Category: Forensics / Steganography



📜 Description

Sometimes what you see isn’t what you get.

Two portraits gaze back at you — each carrying whispers of a secret.

One holds the key, buried beneath layers unseen.

The other guards the truth, transformed beyond recognition.

Unlock the first to awaken the second. Only then will the hidden message reveal itself — a trace of what once was, locked in a cryptic form.



Flag format: ACNCTF{}



🔎 Approach

1 — Inspect the base64.png image using Hex Editor (Hex Analysis) or using strings in Linux or ubuntu.

You might find a passphrase as unlock\_me.

2 — Base64 Encode the Passphrase

3 — Extract the Hidden File (fingerprint.py) from Second Image using Steghide 

Command - steghide extract -sf image1.jpeg

&nbsp;   It will ask for the passphrase which the base64 decoded passphrase.

&nbsp;   enter it and u will get a .py file 

4 — Run the Extracted Python Script

Command - python3 fingerprint.py

Output: flag{hidden\_in\_exif}

5 — Convert the Flag to MD5sum

Based on the question or the clue convert the flag to MD5sum and wrap it in ACNCTF{} format.



✅ Solution

The final flag is:

ACNCTF{4ff54b43cd8ec104efdf2714199c0357}























