#!/usr/bin/env python3
"""Build the voiced reel from the rendered frames and one voiceover clip per frame.

  python3 build_vo.py hi vo/hi ../reel-hi.mp4
  python3 build_vo.py en vo/en ../reel-en.mp4

vo/<lang>/01.mp3 ... 06.mp3: the Bloom clips listed in timing.json (or a human
recording, one sentence per file). Each frame stays up for its clip plus a short
lead and gap, so the cards change on the voice. Short slide-left crossfades,
loudness normalised to -14 LUFS for Instagram.
"""
import subprocess, sys, json
from pathlib import Path

LEAD, GAP, TAIL, FADE = 0.2, 0.25, 1.2, 0.35
here = Path(__file__).resolve().parent
lang, vo, out = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
frames = sorted((here.parent).glob("slide-*.png"))
clips = sorted(vo.glob("*.mp3")) or sorted(vo.glob("*.wav"))
assert len(frames) == len(clips), f"{len(frames)} frames but {len(clips)} clips"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]))
lens = [dur(c) for c in clips]
D = [LEAD + l + GAP + (TAIL if i == len(lens) - 1 else 0) + (FADE if i < len(lens) - 1 else 0) for i, l in enumerate(lens)]
args, flt = [], []
for f, d in zip(frames, D):
    args += ["-loop", "1", "-t", f"{d:.3f}", "-i", str(f)]
for c in clips:
    args += ["-i", str(c)]
n = len(frames)
prev, off = "[0:v]", 0.0
for i in range(1, n):
    off += D[i - 1] - FADE
    lab = f"[x{i}]" if i < n - 1 else "[xv]"
    flt.append(f"{prev}[{i}:v]xfade=transition=slideleft:duration={FADE}:offset={off:.3f}{lab}")
    prev = lab
flt.append("[xv]format=yuv420p[v]")
# each clip delayed to its frame start + LEAD
start = 0.0
amix = []
for i in range(n):
    ms = int((start + LEAD) * 1000)
    flt.append(f"[{n+i}:a]aresample=48000,adelay={ms}|{ms}[a{i}]")
    amix.append(f"[a{i}]")
    start += D[i] - FADE
total = sum(D) - FADE * (n - 1)
flt.append("".join(amix) + f"amix=inputs={n}:normalize=0,loudnorm=I=-14:TP=-1.5,apad=whole_dur={total:.3f}[a]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", ";".join(flt),
                "-map", "[v]", "-map", "[a]", "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", out], check=True)
print(out, round(total, 2), "s")
