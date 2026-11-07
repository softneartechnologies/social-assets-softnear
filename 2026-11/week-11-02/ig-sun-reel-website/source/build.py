#!/usr/bin/env python3
"""Assemble the reel: per-scene video files from frames, voice track, music bed, final mux."""
import json
import os
import subprocess
from pathlib import Path

import numpy as np
from scipy.io import wavfile

from scenes import SCENES

HERE = Path(__file__).parent
FR = HERE / "frames"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
FPS = 30
LEAD = 0.15   # silence before each line
GAP = 0.40    # silence after each line
SR = 44100


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode())


def run(cmd):
    subprocess.run(cmd, check=True)


plan = json.loads((FR / "plan.json").read_text())
timeline = []
voice = []
for i, s in enumerate(SCENES, 1):
    wav = HERE / "vo" / f"{i:02d}.wav"
    vd = dur(wav)
    total = LEAD + vd + GAP
    total = round(total * FPS) / FPS
    # state start times (seconds into the scene)
    starts = [0.0, LEAD + s["split"] * vd]
    if "split2" in s:
        starts.append(LEAD + s["split2"] * vd)
    frames = plan[s["id"]]
    # build concat list: animation frames (1/FPS each), last frame of each state held until the next start
    lines, t = [], 0.0
    for k, st in enumerate(starts):
        seq = [f for f in frames if f.startswith(f"s{k}_")]
        end = starts[k + 1] if k + 1 < len(starts) else total
        for j, f in enumerate(seq):
            d = 1 / FPS if j < len(seq) - 1 else max(1 / FPS, end - st - (len(seq) - 1) / FPS)
            lines.append(f"file '{FR / s['id'] / f}'\nduration {d:.5f}")
    lines.append(f"file '{FR / s['id'] / frames[-1]}'")
    lst = OUT / f"{s['id']}.txt"
    lst.write_text("ffconcat version 1.0\n" + "\n".join(lines) + "\n")
    tmp, final = OUT / f"{s['id']}.tmp.mp4", OUT / f"{s['id']}.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-vf", f"fps={FPS},format=yuv420p", "-t", f"{total:.4f}", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "18", "-r", str(FPS), str(tmp)])
    os.replace(tmp, final)
    timeline.append((s["id"], total))
    sr, a = wavfile.read(wav)
    a = a.astype(np.float32) / 32768.0
    if a.ndim > 1:
        a = a.mean(axis=1)
    seg = np.zeros(int(round(total * SR)), np.float32)
    o = int(LEAD * SR)
    seg[o:o + len(a)] = a[: len(seg) - o]
    voice.append(seg)
    print(s["id"], f"{total:.2f}s")

v = np.concatenate(voice)
N = len(v)
T = N / SR
print("total", round(T, 2))

# --- original music bed: warm pad + soft pulse, 96 bpm, I-vi-IV-V in C ---
t = np.arange(N) / SR
bpm = 96
beat = 60 / bpm
bar = 4 * beat
chords = [[48, 55, 64, 71], [45, 52, 60, 67], [41, 48, 57, 64], [43, 50, 59, 65]]  # Cmaj7 Am7 Fmaj7 G7
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
music = np.zeros(N, np.float32)
nb = int(np.ceil(T / bar))
for b in range(nb):
    s0, s1 = int(b * bar * SR), min(N, int((b + 1) * bar * SR))
    tt = t[s0:s1] - b * bar
    env = np.minimum(1, tt / 0.6) * np.minimum(1, (bar - tt) / 0.4)
    for m in chords[b % 4]:
        f = hz(m)
        music[s0:s1] += 0.06 * env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt + 0.5))
    # bass on beats 1 and 3
    for k in (0, 2):
        bs = s0 + int(k * beat * SR)
        L = min(int(0.45 * SR), N - bs)
        if L > 0:
            tb = np.arange(L) / SR
            music[bs:bs + L] += 0.18 * np.sin(2 * np.pi * hz(chords[b % 4][0] - 12) * tb) * np.exp(-tb * 5)
    # soft click on every beat
    for k in range(4):
        cs = s0 + int(k * beat * SR)
        L = min(int(0.05 * SR), N - cs)
        if L > 0:
            music[cs:cs + L] += 0.05 * np.random.default_rng(b * 4 + k).standard_normal(L) * np.exp(-np.arange(L) / SR * 90)
music /= np.abs(music).max() + 1e-9
# duck under the voice
envv = np.convolve(np.abs(v), np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
duck = np.where(envv > 0.01, 0.10, 0.22).astype(np.float32)
duck = np.convolve(duck, np.ones(int(0.2 * SR)) / int(0.2 * SR), mode="same")
fade = np.minimum(1, np.minimum(t / 0.5, (T - t) / 1.2))
mix = v * 0.95 + music * duck * fade
mix /= max(1.0, np.abs(mix).max() / 0.95)
wavfile.write(OUT / "mix.wav", SR, (mix * 32767).astype(np.int16))
wavfile.write(OUT / "voice_only.wav", SR, (v * 32767).astype(np.int16))
wavfile.write(OUT / "music_only.wav", SR, (music * 0.5 * fade * 32767).astype(np.int16))

(OUT / "scenes.txt").write_text("".join(f"file '{OUT / (sid + '.mp4')}'\n" for sid, _ in timeline))
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(OUT / "scenes.txt"),
     "-c", "copy", str(OUT / "video.mp4")])
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(OUT / "video.mp4"), "-i", str(OUT / "mix.wav"),
     "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
     "-movflags", "+faststart", str(OUT / "reel.tmp.mp4")])
os.replace(OUT / "reel.tmp.mp4", OUT / "reel.mp4")
json.dump(timeline, open(OUT / "timeline.json", "w"))
print("done", OUT / "reel.mp4")
