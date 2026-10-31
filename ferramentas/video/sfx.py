import json, wave, sys
import numpy as np
meta = json.load(open('meta.json')); SR = 48000; D = meta['d']; N = int(D * SR) + SR
L = np.zeros(N); R = np.zeros(N); rng = np.random.default_rng(5)
t_ = lambda d: np.arange(int(d * SR)) / SR
def env(d, a=0.004, dec=0.2): t = t_(d); return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / dec)
def tone(f, d, dec, a=0.003): return np.sin(2 * np.pi * f * t_(d)) * env(d, a, dec)
def sweep(f0, f1, d, dec, a=0.003): t = t_(d); ph = 2 * np.pi * np.cumsum(f0 + (f1 - f0) * t / d) / SR; return np.sin(ph) * env(d, a, dec)
def bpn(d, lo, hi):
    n = rng.standard_normal(int(d * SR)); f = np.fft.rfft(n); fr = np.fft.rfftfreq(len(n), 1 / SR); f[(fr < lo) | (fr > hi)] = 0; return np.fft.irfft(f, len(n)) / 3
def mx(*xs):
    o = np.zeros(max(len(x) for x in xs))
    for x in xs: o[:len(x)] += x
    return o
def seq(parts):
    return np.concatenate(parts)
S = {}
S['pop'] = mx(sweep(900, 420, 0.15, 0.05) * 0.9, bpn(0.02, 2000, 6000) * env(0.02, 0.001, 0.004) * 0.4)
w = t_(0.6); S['whoosh'] = bpn(0.6, 300, 4500) * np.sin(np.pi * w / 0.6) ** 2 * 1.3
S['swish'] = bpn(0.32, 1500, 9000) * np.sin(np.pi * t_(0.32) / 0.32) ** 2 * 0.9
S['tick'] = tone(2100, 0.05, 0.012) * 0.8
S['coin'] = sum(tone(f, 0.5, 0.16) * a for f, a in [(2200, 1), (3310, .6), (4750, .35)]) * 0.5
S['ding'] = seq([tone(1174.7, 0.13, 0.08) + tone(2349, 0.13, 0.05) * 0.3, tone(1568, 0.9, 0.32) + tone(3136, 0.9, 0.16) * 0.3]) * 0.6
S['msg'] = seq([tone(988, 0.1, 0.06), tone(1480, 0.32, 0.11)]) * 0.7
S['thump'] = mx(sweep(110, 42, 0.8, 0.25, 0.002) * 1.3, bpn(0.05, 800, 6000) * env(0.05, 0.001, 0.01) * 0.5)
S['drop'] = sweep(900, 220, 0.42, 0.24) * 0.5
sh = np.zeros(int(1.5 * SR))
for k, f in enumerate([523.25, 659.25, 783.99, 1046.5, 1318.5]):
    s_ = tone(f, 1.1, 0.42, 0.01) + tone(f * 2, 1.1, 0.18, 0.01) * 0.25; i = int(k * 0.1 * SR); sh[i:i + len(s_)] += s_[:len(sh) - i]
S['shimmer'] = sh * 0.5
S['beep'] = seq([tone(2000, 0.06, 0.035), np.zeros(int(0.04 * SR)), tone(2600, 0.08, 0.045)]) * 0.5
S['err'] = seq([tone(330, 0.12, 0.08, 0.005), tone(262, 0.22, 0.12, 0.005)]) * 0.7
S['check'] = mx(sweep(700, 1400, 0.12, 0.08) * 0.6, tone(1760, 0.3, 0.1) * 0.4)
S['key'] = mx(bpn(0.035, 1800, 7000) * env(0.035, 0.0005, 0.008) * 1.6, tone(180, 0.06, 0.015) * 0.4)
S['send'] = mx(sweep(500, 1600, 0.25, 0.2) * 0.6, bpn(0.25, 2000, 8000) * np.sin(np.pi * t_(0.25) / 0.25) * 0.4)
VOL = {'pop': .17, 'whoosh': .08, 'swish': .08, 'tick': .12, 'coin': .14, 'ding': .19, 'msg': .16, 'thump': .3, 'drop': .12, 'shimmer': .16, 'beep': .13, 'err': .16, 'check': .17, 'key': .16, 'send': .15}
for e in meta['sfx']:
    s_ = S[e['k']] * VOL[e['k']] * e['v']; i = int(e['t'] * SR); pan = rng.uniform(-0.25, 0.25)
    j = min(N, i + len(s_)); L[i:j] += s_[:j - i] * np.sqrt((1 - pan) / 2) * 1.414; R[i:j] += s_[:j - i] * np.sqrt((1 + pan) / 2) * 1.414
ir_len = int(0.6 * SR); ir = rng.standard_normal(ir_len) * np.exp(-np.arange(ir_len) / SR / 0.16); ir /= np.sqrt((ir ** 2).sum())
def conv(x):
    n = 1 << int(np.ceil(np.log2(len(x) + ir_len))); return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]
L = L + conv(L) * 0.18; R = R + conv(R) * 0.18
tb = np.arange(N) / SR; fade = np.clip((D - tb) / 1.0, 0, 1); L *= fade; R *= fade
pk = max(abs(L).max(), abs(R).max()); g = 0.5 / pk if pk > 0.5 else 1
out = np.stack([L[:int(D * SR)], R[:int(D * SR)]], 1) * g
with wave.open('sfx.wav', 'wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print('ok', D, pk)
