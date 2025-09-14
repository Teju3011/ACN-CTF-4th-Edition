# Thunder Morse — Solution (private)

**Flag:** `flag{thunder_heard_the_truth}`

## Steps to solve
1. Open `thunder.wav` in Audacity (or plot a spectrogram with Python). You will see repeating tone bursts.
2. Zoom and measure durations: short ~0.08s (dot), long ~0.24s (dash). Spacing indicates symbol/letter/word boundaries.
3. Translate sequence of dots/dashes into letters using standard Morse mapping.
   - Example: `....` -> H, `.` -> E, `.-..` -> L, etc.
4. The decoded text spells the flag directly: `flag{thunder_heard_the_truth}`.

## Quick programmatic decode (optional)
A simple script `solver_decoder.py` (provided) can threshold the audio amplitude and extract durations to convert to dot/dash, then map to text. This is helpful for automated verification.


## How to get started
1. Download (or generate) `challenge/thunder.wav`.  
   - To generate locally: install Python dependencies and run:
     ```bash
     cd challenge
     python3 generate_thunder.py
     ```
     This will create `thunder.wav` in the `challenge/` folder.
2. Use an audio tool (Audacity, `sox`, or Python) to inspect the file. Look at the waveform or spectrogram.
3. Convert the beeps to dot/dash timing (or use an automated decoder).
4. Decode Morse to ASCII to reveal the flag.

```
cd challenge
pip3 install numpy scipy
python3 generate_thunder.py # Creates thunder.wav and morse.txt
# Optionally open thunder.wav with Audacity or play it:
aplay thunder.wav   # on Linux
```

---

## Tools recommended
- Audacity (spectrogram & zoom)  
- `sox` / `sox`'s `play` / `sox`'s `spectrum` commands  
- Python with `scipy` / `numpy` (if you prefer programmatic detection)  
- Online Morse decoders (optional) or local scripts

---
## Notes for organizers
- The generator script embeds the flag `flag{thunder_heard_the_truth}` by default. Edit `generate_thunder.py` to change the flag text or timings.
- Keep `private_solutions/` private until the contest finishes.
