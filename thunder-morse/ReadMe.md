#  Thunder Morse

**Category:** Crypto / Stego — Easy  

---

## Story
The storm knocked out the text feeds — but someone left an audio recording of their last message.  
Listen carefully: the signal hides the key to the weather bunker.

Can you extract the message and find the flag?

---

## Files
- `challenge/generate_thunder.py` — Python script that generates the `thunder.wav` audio (run locally to produce the file).  
- `challenge/thunder.wav` — (optional) the generated audio file (10–30s) with Morse code embedded. You can add the WAV directly to the `challenge/` folder if you prefer not to run the generator.  
- Progressive hints (unlockable).
---

## Goal
Decode the hidden Morse audio and find the flag. The flag has the format:


---


## Hints
- Hint 1: Try opening thunder.wav in Audacity or a spectrogram tool. Zoom into the signal and look for repeated tones.

- Hint 2: The pattern of short and long beeps is Morse code (dot = short, dash = long). Convert dot/dash to letters and read the flag.


---

