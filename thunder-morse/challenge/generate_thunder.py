#!/usr/bin/env python3
"""
generate_thunder.py

Generates thunder.wav containing Morse code for a flag message, mixed with light rain noise.
Default sample rate: 44100 Hz
Usage: python3 generate_thunder.py
"""

import numpy as np
from scipy.io.wavfile import write
import os
import argparse

# ---------- Config ----------
SAMPLE_RATE = 44100
TONE_FREQ = 750.0          # frequency of the Morse tone (Hz)
DOT_DURATION = 0.08        # seconds
DASH_DURATION = DOT_DURATION * 3
SYMBOL_GAP = DOT_DURATION  # gap between elements of a character
LETTER_GAP = DOT_DURATION * 3
WORD_GAP = DOT_DURATION * 7
AMPLITUDE = 0.8            # tone amplitude (0.0 - 1.0)
NOISE_AMPLITUDE = 0.12     # rain / ambient noise amplitude
OUTPUT_WAV = "thunder.wav"
MORSE_TXT = "morse.txt"
# Default message (flag)
FLAG = "flag{thunder_heard_the_truth}"

# ---------- Morse table ----------
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
    'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----',
    '{': '.-.-.', '}': '-.-.-', '_': '..--.-', '-': '-....-',
    # we'll include a mapping for brace and underscore for the flag string if needed
}

def text_to_morse(text):
    text = text.upper()
    words = text.split(" ")
    morse_words = []
    for w in words:
        symbols = []
        for ch in w:
            if ch in MORSE_CODE:
                symbols.append(MORSE_CODE[ch])
            else:
                # handle braces and punctuation mapping by sending as letters if not found
                # fallback: map braces manually
                if ch == '{':
                    symbols.append('..--.')  # not standard; players can still decode by audio-to-text
                elif ch == '}':
                    symbols.append('-.--.-')
                else:
                    # Skip unknown characters
                    continue
        morse_words.append(" ".join(symbols))
    return "   ".join(morse_words)  # 3 spaces as word gap marker

def tone(duration, amp=1.0):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave = amp * np.sin(2 * np.pi * TONE_FREQ * t)
    # apply short fade-in/out to avoid clicks
    fade_len = int(0.005 * SAMPLE_RATE)
    if fade_len*2 < len(wave):
        fade = np.linspace(0,1,fade_len)
        wave[:fade_len] *= fade
        wave[-fade_len:] *= fade[::-1]
    return wave

def silence(duration):
    return np.zeros(int(SAMPLE_RATE * duration), dtype=np.float32)

def generate_morse_signal(morse_str):
    # morse_str uses '.' '-' and spaces (single space between chars, 3 spaces between words)
    out = []
    tokens = morse_str.split(" ")
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '':
            # this indicates a word gap (since we used triple spaces)
            # add word gap if previous not just added
            out.append(silence(WORD_GAP))
            # skip contiguous blanks
            while i < len(tokens) and tokens[i] == '':
                i += 1
            continue
        # token is a morse char like ".-" or "..."
        for j, sym in enumerate(token):
            if sym == '.':
                out.append(tone(DOT_DURATION, amp=AMPLITUDE))
            elif sym == '-':
                out.append(tone(DASH_DURATION, amp=AMPLITUDE))
            # gap between symbols
            if j != len(token) - 1:
                out.append(silence(SYMBOL_GAP))
        # after character, letter gap
        out.append(silence(LETTER_GAP))
        i += 1
    return np.concatenate([x for x in out if x.size > 0])

def add_ambient_noise(signal):
    # light "rain" produced by filtered white noise
    noise = np.random.normal(0, 1.0, len(signal))
    # simple low-pass filter by cumulative average (cheap)
    from scipy.signal import butter, lfilter
    b, a = butter(4, 0.05)
    filtered = lfilter(b, a, noise)
    # scale and add
    maxsig = np.max(np.abs(signal)) if np.max(np.abs(signal)) != 0 else 1.0
    filtered = filtered / (np.max(np.abs(filtered)) + 1e-9) * maxsig * NOISE_AMPLITUDE
    return signal + filtered

def main(output=OUTPUT_WAV, flag=FLAG):
    # build morse string
    morse_str = text_to_morse(flag)
    print("Morse representation:", morse_str)
    # write morse to verify file
    with open(MORSE_TXT, "w") as f:
        f.write(morse_str + "\n")
    signal = generate_morse_signal(morse_str)
    # add short ambient storm intro and outro
    intro = np.zeros(int(SAMPLE_RATE * 0.4))
    outro = np.zeros(int(SAMPLE_RATE * 0.4))
    full = np.concatenate([intro, signal, outro])
    # add ambient noise
    full_noisy = add_ambient_noise(full)
    # normalize to int16
    full_noisy = full_noisy / (np.max(np.abs(full_noisy)) + 1e-9)
    scaled = (full_noisy * 32767).astype(np.int16)
    write(output, SAMPLE_RATE, scaled)
    print(f"WAV written to {output} ({len(scaled)/SAMPLE_RATE:.2f}s)")
    print(f"Morse pattern (saved to {MORSE_TXT}).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate thunder.wav with Morse-encoded flag")
    parser.add_argument("--out", "-o", default=OUTPUT_WAV, help="Output WAV filename")
    parser.add_argument("--flag", "-f", default=FLAG, help="Flag text to encode (wrap in braces)")
    args = parser.parse_args()
    main(output=args.out, flag=args.flag)

