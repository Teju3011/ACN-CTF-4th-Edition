# sol.py
# Robust solver for the Verilog Flag Checker (handles collisions)

from itertools import product
import re

def magic(val, inp):
    if val == 0:
        return ((inp << 3) | (inp >> 5)) & 0xFF
    elif val == 1:
        return ((inp >> 2) ^ 0x5A) & 0xFF
    elif val == 2:
        return (inp + 77) & 0xFF
    elif val == 3:
        return (inp ^ 0x33) & 0xFF
    return inp

def chall(inp):
    val0 = (inp >> 0) & 3
    val1 = (inp >> 2) & 3
    val2 = (inp >> 4) & 3
    val3 = (inp >> 6) & 3
    res0 = magic(val0, inp)
    res1 = magic(val1, res0)
    res2 = magic(val2, res1)
    res3 = magic(val3, res2)
    return res3

# targets (from t_chall.v)
targets = [
    77, 105, 111, 105, 74, 106, 115, 10, 249, 10, 73, 106,
    125, 10, 125, 73, 111, 249, 74, 73, 106, 249, 68, 111,
    125, 75
]

# printable set (same as you used)
printable = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_!@#$%^&*()-+=<>?/|.,:;"

# build candidate pools for each target (restrict to user's printable set if possible)
pools = []
for t in targets:
    cand_bytes = [b for b in range(256) if chall(b) == t]
    cand_userprint = [chr(b) for b in cand_bytes if 32 <= b <= 126 and chr(b) in printable]
    if not cand_userprint:
        # fall back to any printable ASCII
        cand_userprint = [chr(b) for b in cand_bytes if 32 <= b <= 126]
    if not cand_userprint:
        cand_userprint = ['?']
    pools.append(cand_userprint)

# scoring heuristics to pick the most "flag-like" solution
def score_solution(s):
    score = 0
    if '404' in s:         score += 100
    if 'fl4g' in s:        score += 200
    if 'flag' in s:        score += 100
    if 'n0t' in s:         score += 150
    if 'not' in s:         score += 50
    if 'f0und' in s:       score += 80
    if 'found' in s:       score += 40
    if '_' in s:           score += 10
    # small penalty for extra digits in the body (besides 404)
    body = s[len("acnctf{"):-1] if s.startswith("acnctf{") and s.endswith("}") else s
    score -= sum(ch.isdigit() for ch in body)
    return score

# restrict to plausible flag pattern to prune search
flag_re = re.compile(r"^acnctf\{[0-9a-z_]+\}$")

best = None
best_score = -10**9
# iterate all combos (in this challenge the space is small — safe to enumerate)
for combo in product(*pools):
    s = ''.join(combo)
    if not flag_re.match(s):
        continue
    sc = score_solution(s)
    if sc > best_score or (sc == best_score and (best is None or s < best)):
        best_score = sc
        best = s

print("Recovered flag:", best)
