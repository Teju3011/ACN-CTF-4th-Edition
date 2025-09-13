#!/usr/bin/env python3
# solver_decoder.py
# Simple amplitude-threshold based Morse extractor for thunder.wav
import numpy as np
from scipy.io.wavfile import read
from collections import deque

MORSE_TO_TEXT = {
    '.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F',
    '--.':'G','....':'H','..':'I','.---':'J','-.-':'K','.-..':'L',
    '--':'M','-.':'N','---':'O','.--.':'P','--.-':'Q','.-.':'R',
    '...':'S','-':'T','..-':'U','...-':'V','.--':'W','-..-':'X',
    '-.--':'Y','--..':'Z','-----':'0','.----':'1','..---':'2','...--':'3',
    '....-':'4','.....':'5','-....':'6','--...':'7','---..':'8','----.':'9'
}

def extract_dots_dashes(fname):
    sr, data = read(fname)
    if data.ndim > 1:
        data = data.mean(axis=1)
    data = np.abs(data)
    # normalize
    data = data / (np.max(data) + 1e-9)
    # threshold
    thresh = 0.25
    tone = data > thresh
    # measure runs
    runs = []
    cur = tone[0]
    count = 1
    for b in tone[1:]:
        if b == cur:
            count += 1
        else:
            runs.append((cur, count))
            cur = b
            count = 1
    runs.append((cur, count))
    # convert counts -> durations (seconds)
    durations = [(val, cnt / sr) for val, cnt in runs]
    # convert to morse using heuristic: dot ~ 0.08, dash ~ 0.24, letter gap ~ 0.24, word gap ~ 0.56
    morse = []
    cur_symbol = []
    i = 0
    while i < len(durations):
        is_tone, dur = durations[i]
        if is_tone:
            # tone: dot or dash
            if dur < 0.15:
                cur_symbol.append('.')
            else:
                cur_symbol.append('-')
        else:
            # silence
            if dur < 0.15:
                # between parts of letter
                pass
            elif dur < 0.45:
                # letter gap
                morse.append(''.join(cur_symbol))
                cur_symbol = []
            else:
                # word gap
                morse.append(''.join(cur_symbol))
                morse.append('/')  # word separator
                cur_symbol = []
        i += 1
    if cur_symbol:
        morse.append(''.join(cur_symbol))
    return morse

def morse_to_text(morse_list):
    words = []
    cur = []
    for token in morse_list:
        if token == '/':
            if cur:
                words.append(''.join(cur))
                cur = []
            words.append(' ')
        else:
            if token == '':
                continue
            cur.append(MORSE_TO_TEXT.get(token, '?'))
    if cur:
        words.append(''.join(cur))
    return ''.join(words)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("usage: solver_decoder.py thunder.wav")
        sys.exit(1)
    morse = extract_dots_dashes(sys.argv[1])
    print("Morse tokens:", morse)
    text = morse_to_text(morse)
    print("Decoded text:", text)
