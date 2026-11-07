#!/usr/bin/env python3
"""Original score + sound design + voiceover mix for the "Net and water" reel (no samples).
python3 music.py TIMING.json VO_DIR OUT.wav
TIMING comes from timing.py; VO_DIR holds 01.wav..07.wav (one voiceover file per scene).
Every sound effect is placed on the same cues the animation uses, so picture and sound stay in sync."""
import json, sys, wave
from pathlib import Path
import numpy as np

SR = 44100
SC = json.loads(Path(sys.argv[1]).read_text())
VO = Path(sys.argv[2])
LEAD = .35
T0 = {}; C = {}; acc = 0.0
for s in SC:
    T0[s["id"]] = acc; C[s["id"]] = s["cues"]; acc += s["D"]
DUR = acc
N = int(DUR * SR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(11)
t_all = np.arange(N) / SR

def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N or i + len(sig) <= 0: return
    a = max(0, -i); i = max(i, 0); j = min(N, i + len(sig) - a)
    s = sig[a:a + j - i] * gain
    L[i:j] += s * np.sqrt(.5 * (1 - pan)); R[i:j] += s * np.sqrt(.5 * (1 + pan))

def tt(d): return np.arange(int(d * SR)) / SR
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def lp_fast(x, cutoff):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / (1 + (f / cutoff) ** 4), len(x))
def bp_fast(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * (1 / (1 + (lo / np.maximum(f, 1)) ** 4)) / (1 + (f / hi) ** 4), len(x))

# ---------- instruments ----------
def kick(g=1.0):
    t = tt(.45); f = 45 + 110 * np.exp(-t * 28)
    return g * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
def clap():
    t = tt(.25); n = rng.standard_normal(len(t))
    env = np.exp(-t * 26) + .6 * np.exp(-np.maximum(t - .012, 0) * 30) * (t > .012)
    return bp_fast(n * env, 900, 3500) * .9
def hat(o=False):
    t = tt(.2 if o else .06); n = rng.standard_normal(len(t))
    return bp_fast(n * np.exp(-t * (18 if o else 70)), 6000, 14000) * .35
def pad(midis, d, bright=1.0):
    t = tt(d); s = np.zeros(len(t))
    for m in midis:
        for det in (-.07, .07):
            ph = rng.uniform(0, 6.28); f = hz(m + det)
            s += np.sin(2 * np.pi * f * t + ph) + .3 * np.sin(4 * np.pi * f * t) * bright + .12 * np.sin(6 * np.pi * f * t) * bright
    env = np.minimum(1, t / .35) * np.minimum(1, (d - t) / .4)
    return s * env / (len(midis) * 2)
def pluck(m, d=.5):
    t = tt(d); f = hz(m)
    return (np.sin(2 * np.pi * f * t) + .5 * np.sin(4 * np.pi * f * t) * np.exp(-t * 12)) * np.exp(-t * 7) * np.minimum(1, t / .003)
def bass(m, d):
    t = tt(d); f = hz(m)
    s = np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t)
    return s * np.minimum(1, t / .01) * np.exp(-t * 2.2) * np.minimum(1, (d - t) / .05)
def impact():
    t = tt(2.2); f = 30 + 80 * np.exp(-t * 9)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.4)
    n = lp_fast(rng.standard_normal(len(t)), 1800) * np.exp(-t * 9) * .7
    return boom + n
def riser(d):
    t = tt(d); n = rng.standard_normal(len(t))
    x = bp_fast(n, 1500, 9000) * (t / d) ** 2.2
    return x * .5 + .25 * np.sin(2 * np.pi * (200 * t + 500 * t * t / d)) * (t / d) ** 2
def whoosh(d=.45):
    t = tt(d); n = rng.standard_normal(len(t)); env = np.sin(np.pi * t / d) ** 2
    return bp_fast(n, 400, 5000) * env * .55
def splash():
    t = tt(1.4); n = rng.standard_normal(len(t))
    s = bp_fast(n, 600, 7000) * np.exp(-t * 4.5)
    for k in range(9):  # bubbles
        st = .15 + .09 * k; b = tt(.08); f = 500 + 900 * rng.random()
        bub = np.sin(2 * np.pi * (f * b + 2500 * b * b)) * np.exp(-b * 45) * .35
        i = int(st * SR); s[i:i + len(bub)] += bub[:len(s) - i]
    return s
def rumble(d):
    t = tt(d); return lp_fast(rng.standard_normal(len(t)), 220) * np.sin(np.pi * t / d) * 1.2
def clink():
    t = tt(.35); s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * dcy) for f, dcy in ((2900, 14), (4100, 20), (5600, 26)))
    return s * .22
def tick():
    t = tt(.04); return bp_fast(rng.standard_normal(len(t)), 2500, 8000) * np.exp(-t * 160) * .6
def popf():
    t = tt(.12); return np.sin(2 * np.pi * (300 * t + 4000 * t * t)) * np.exp(-t * 40) * .45
def ding(m=88):
    t = tt(1.2); f = hz(m)
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 3.5) + .4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 8)) * .3
def chime(ms):
    out = np.zeros(int(1.8 * SR))
    for k, m in enumerate(ms):
        d = ding(m); i = int(k * .07 * SR); out[i:i + len(d)] += d[:len(out) - i]
    return out
def thud():
    t = tt(.6); f = 60 + 90 * np.exp(-t * 20)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) + lp_fast(rng.standard_normal(len(t)), 900) * np.exp(-t * 25) * .5
def key():
    t = tt(.05); return bp_fast(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t * 120) * .45
def wind(d):
    t = tt(d); n = rng.standard_normal(len(t))
    w = bp_fast(n, 250, 1400) * (0.6 + 0.4 * np.sin(2 * np.pi * .35 * t))
    return w * np.minimum(1, t / .6) * np.minimum(1, (d - t) / .6) * .5

# ---------- score ----------
BPM = 100; B = 60 / BPM
prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
roots = [45, 41, 36, 43]
dry0, dry1 = T0["04-dry"], T0["05-journey"]
full0 = T0["03-water"]
bar = 4 * B
nb = int(DUR / bar) + 1
for b in range(nb):
    t0 = b * bar
    if t0 >= DUR: break
    ch = prog[b % 4]; inside_dry = dry0 - .2 <= t0 < dry1 - .2
    add(pad(ch, bar + .3, .6 if inside_dry else 1.0), t0, .16 if inside_dry else .2, 0)
    if inside_dry: continue
    for e in range(8):  # eighth-note bass pulse
        te = t0 + e * B / 2
        if te < 1.2: continue
        add(bass(roots[b % 4], B / 2 * .95), te, .32 if t0 >= full0 else .2)
    if t0 >= T0["02-net"]:
        for q in range(4):
            add(kick(), t0 + q * B, .55 if q in (0, 2) else .3)
        for e in range(8): add(hat(e % 2 == 1), t0 + e * B / 2, .5)
    if t0 >= full0:
        add(clap(), t0 + B, .35); add(clap(), t0 + 3 * B, .35)
        arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12]
        for s16 in range(8):
            add(pluck(arp[s16 % 4], .45), t0 + s16 * B / 2, .14, -.3 if s16 % 2 else .3)

# ---------- sound design (absolute time = scene start + cue) ----------
def at(sid, k, off=0.0): return T0[sid] + C[sid][k] + off
h = "01-hook"
add(pluck(76), at(h, 0), .3); add(pluck(79), at(h, 1), .3)
add(riser(1.15), at(h, 2, -1.15), .5); add(impact(), at(h, 2), .85)
for sid in list(T0)[1:]:
    add(whoosh(), T0[sid] - .32, .6)
n = "02-net"
for k in range(10): add(tick(), at(n, 1, k * .12), .45)
add(rumble(1.6), at(n, 3, -.35), .55); add(splash(), at(n, 3, .55), .8)
w = "03-water"
for k in range(3):
    add(impact()[:int(.6 * SR)], at(w, k), .3); add(ding(81 + k * 3), at(w, k, .3), .6)
for i in range(12): add(clink(), at(w, 0, .4 + .93 + i * .42), .7, (-.3, .3)[i % 2])
k = 0
while at(w, 1, .3 + k * .25) < at(w, 2): add(tick(), at(w, 1, .3 + k * .25), .6); k += 1
for i in range(9): add(popf(), at(w, 2, .6 + i * .3), .7, (-.4, .4)[i % 2])
d = "04-dry"
add(wind(SC[3]["D"]), T0[d], .9); add(thud(), at(d, 2), .9); add(impact(), at(d, 2), .4)
j = "05-journey"
add(popf(), at(j, 0), .6)
for i in range(10): add(whoosh(.25), at(j, 0, .5 + i * .38 + .5), .15, .2)
for k in range(3): add(ding(84 + k * 2), at(j, 1 + k, .3), .7)
add(chime([72, 76, 79, 84]), at(j, 4), .9)
for i in range(3): add(ding(91), at(j, 4, .6 + i * .55), .5)
o = "06-both"
add(impact()[:int(.8 * SR)], T0[o] + .12, .45)
add(pluck(57, .8), at(o, 0), .3); add(pluck(52, .8), at(o, 1), .3)
for i in range(4): add(splash()[:int(.4 * SR)], at(o, 1, .5 + i * .35), .2)
add(chime([72, 76, 79]), at(o, 2), .8); add(chime([84, 88, 91]), at(o, 2, 1.4), .7)
c = "07-cta"
add(popf(), at(c, 1), .8)
for i in range(10): add(key(), at(c, 2, i / 12), .8)
add(whoosh(.35), at(c, 2, 1.2), .5); add(chime([72, 76, 79, 84, 88]), at(c, 3), .6)
add(pad([48, 55, 60, 64, 67], 3.2, 1.0), DUR - 3.4, .25)

# ---------- voiceover + ducking ----------
def readwav(p):
    with wave.open(str(p)) as f:
        x = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float64) / 32768
        if f.getnchannels() == 2: x = x.reshape(-1, 2).mean(1)
    return x
voice = np.zeros(N)
for i, s in enumerate(SC):
    v = readwav(VO / f"{i+1:02d}.wav"); v = v / (np.abs(v).max() + 1e-9)
    st = int((T0[s["id"]] + LEAD) * SR); e = min(N, st + len(v)); voice[st:e] += v[:e - st]
# ---------- reverb + master ----------
def reverb(x, seed):
    r = np.random.default_rng(seed); n = int(1.8 * SR); t = np.arange(n) / SR
    ir = r.standard_normal(n) * np.exp(-t / .45); ir[:int(.01 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
    m = 1 << int(np.ceil(np.log2(len(x) + n)))
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x)]
L = L + .22 * reverb(L, 1); R = R + .22 * reverb(R, 2)
env = np.minimum(1, t_all / .3) * np.minimum(1, (DUR - t_all) / 1.6)
bed = np.stack([L, R], 1) * env[:, None]
bed = np.tanh(bed / (np.abs(bed).max() + 1e-9) * 1.6) / np.tanh(1.6)
# duck the bed while the voice speaks: smoothed voice envelope -> gain 1.0 .. 0.28
win = int(.05 * SR); ve = np.convolve(np.abs(voice), np.ones(win) / win, "same")
ve = np.convolve((ve > .02).astype(float), np.ones(int(.35 * SR)) / int(.35 * SR), "same")
duck = 1 - .72 * np.clip(ve * 1.5, 0, 1)
mix = bed * .42 * duck[:, None] + voice[:, None] * .9
mix = mix / (np.abs(mix).max() + 1e-9) * .89
with wave.open(sys.argv[3], "wb") as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
    f.writeframes((mix * 32767).astype(np.int16).tobytes())
print("ok", round(DUR, 2))
