"""Align caption words to narration: silence chunks + syllable-rate DP. usage: align.py wav segs.json out.json"""
import wave, json, re, sys
import numpy as np
w = wave.open(sys.argv[1]); SR = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768.0
hop = int(0.01 * SR)
rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)])
db = 20 * np.log10(rms)
TH, MINSIL = -40, 0.14
sp = db > TH; n = len(sp); chunks = []; i = 0
while i < n:
    if sp[i]:
        j = i
        while True:
            while j < n and sp[j]: j += 1
            k = j
            while k < n and not sp[k]: k += 1
            if k < n and (k - j) * 0.01 < MINSIL: j = k; continue
            break
        chunks.append([i * 0.01, j * 0.01]); i = j
    else: i += 1
chunks = [c for c in chunks if c[1] - c[0] > 0.12]
SEGS = json.load(open(sys.argv[2]))
EXP = {'24': ['vinte', 'e', 'quatro']}
VOW = re.compile(r'[aeiouáéíóúâêôãõàüy]+', re.I)
syl = lambda s: max(1, len(VOW.findall(s)))
words = []
for si, s in enumerate(SEGS):
    for wi, tok in enumerate(s.split(' ')):
        core = tok.replace('*', ''); key = core.strip('.,?:!')
        spk = EXP.get(key, [core])
        for k, spw in enumerate(spk):
            words.append(dict(seg=si, first=(k == 0), w=spw, syl=syl(spw), punct=bool(re.search(r'[.,?:!]$', core)) and k == len(spk) - 1))
W = len(words); C = len(chunks)
dur = [c[1] - c[0] for c in chunks]
cum = np.concatenate([[0], np.cumsum([wd['syl'] for wd in words])])
def solve(rate):
    INF = 1e18; dp = np.full((C + 1, W + 1), INF); bk = np.zeros((C + 1, W + 1), int); dp[0][0] = 0
    for c in range(1, C + 1):
        for w1 in range(c, W - (C - c) + 1):
            pen = 0 if (w1 == W or words[w1 - 1]['punct']) else 1.2
            best, arg = INF, -1
            for w0 in range(c - 1, w1):
                if dp[c - 1][w0] >= INF: continue
                cost = dp[c - 1][w0] + (dur[c - 1] - rate * (cum[w1] - cum[w0])) ** 2 / (0.15 + 0.1 * dur[c - 1]) + pen
                if cost < best: best, arg = cost, w0
            dp[c][w1] = best; bk[c][w1] = arg
    b = []; w1 = W
    for c in range(C, 0, -1): w0 = bk[c][w1]; b.append((w0, w1)); w1 = w0
    return dp[C][W], b[::-1]
rate = sum(dur) / cum[-1]
for _ in range(4):
    cost, bounds = solve(rate); rate = sum(dur) / sum(cum[b] - cum[a] for a, b in bounds)
print('chunks', C, 'words', W, 'rate', round(rate, 3), 'cost', round(cost, 2))
wt = [0] * W; we = [0] * W
for (a, b), (c0, c1) in zip(bounds, chunks):
    tot = cum[b] - cum[a]
    for k in range(a, b):
        wt[k] = c0 + (c1 - c0) * (cum[k] - cum[a]) / tot; we[k] = c0 + (c1 - c0) * (cum[k + 1] - cum[a]) / tot
    print(f'{c0:6.2f}-{c1:6.2f}', ' '.join(words[k]['w'] for k in range(a, b)))
out = []
for si in range(len(SEGS)):
    ks = [k for k in range(W) if words[k]['seg'] == si and words[k]['first']]
    ke = [k for k in range(W) if words[k]['seg'] == si]
    out.append({'wt': [round(wt[k], 3) for k in ks], 'end': round(we[ke[-1]], 3)})
json.dump({'segs': out, 'audio_end': chunks[-1][1], 'cost': cost}, open(sys.argv[3], 'w'))
