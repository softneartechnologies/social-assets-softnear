#!/usr/bin/env python3
"""Build timing_<lang>.json from per-scene voiceover files: scene length and animation cues
land on sentence starts (found from the pauses between sentences).
python3 timing.py VO_DIR LANG OUT.json"""
import json, re, subprocess, sys
from pathlib import Path
LEAD, GAP, LAST = .35, .45, 1.6
SENT = {"hi": [3, 3, 4, 3, 5, 4, 4], "en": [3, 3, 4, 3, 5, 5, 4]}   # sentences per scene in the VO
TAIL = [1.5, 2.0, 2.0, 1.4, 2.4, 2.4, 2.6]          # time the animation needs after its last cue
IDS = ["01-hook", "02-net", "03-water", "04-dry", "05-journey", "06-both", "07-cta"]
def starts(f, n):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(f), "-af", "silencedetect=n=-38dB:d=0.12", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]))
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", o)]
    se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", o)]
    first = se[0] if ss and ss[0] < .05 else 0.0
    gaps = [(e - s, e) for s, e in zip(ss, se) if s > .3 and e < d - .15]
    best = sorted(sorted(gaps, reverse=True)[:n - 1], key=lambda g: g[1])
    if len(best) < n - 1: raise SystemExit(f"{f}: found {len(best)+1} sentences, expected {n}")
    return d, [first] + [e for _, e in best]
vo, lang, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
T = []
for i, sid in enumerate(IDS):
    d, s = starts(vo / f"{i+1:02d}.wav", SENT[lang][i])
    s = [LEAD + x for x in s]
    cues = {"01-hook": s, "02-net": [s[0] + .7, s[0] + 1.4, s[1], s[2]], "03-water": s[1:], "04-dry": s,
            "05-journey": s, "06-both": s[1:4], "07-cta": s}[sid]
    D = max(LEAD + d + (LAST if i == 6 else GAP), cues[-1] + TAIL[i])
    T.append({"id": sid, "D": round(round(D * 30) / 30, 4), "cues": [round(c, 3) for c in cues], "vo": d, "lang": lang})
Path(out).write_text(json.dumps(T, indent=1))
print(lang, round(sum(t["D"] for t in T), 1), "s:", [(t["id"], t["D"]) for t in T])
