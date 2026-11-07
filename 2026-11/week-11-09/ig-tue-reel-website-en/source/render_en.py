#!/usr/bin/env python3
"""Render the animated English reel scene by scene.

python3 render_en.py --check            stills at key moments -> check/
python3 render_en.py [scene ids...]     full frames + one mp4 per scene -> out/
"""
import base64, json, os, subprocess, sys, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
FPS, LEAD, GAP, LAST_HOLD = 30, 0.15, 0.45, 1.3
LOGO = "data:image/png;base64," + base64.b64encode(
    (Path.home() / "social-assets-softnear/_system/assets/softnear-logo.png").read_bytes()).decode()
SCENES = json.loads((HERE / "scenes_en.json").read_text())


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode())


def timing():
    out = []
    for i, s in enumerate(SCENES):
        vd = dur(HERE / "vo" / f"{i+1:02d}.wav")
        D = LEAD + vd + (LAST_HOLD if i == len(SCENES) - 1 else GAP)
        D = round(D * FPS) / FPS
        out.append(dict(s, D=D, vd=vd, c=[LEAD + x for x in s["cues"]], first=i == 0, last=i == len(SCENES) - 1))
    return out


def main():
    args = sys.argv[1:]
    check = "--check" in args
    only = [a for a in args if not a.startswith("-")]
    T = timing()
    (HERE / "timing.json").write_text(json.dumps(T, indent=1, ensure_ascii=False))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto((HERE / "stage.html").as_uri())
        for s in T:
            if only and s["id"] not in only:
                continue
            pg.evaluate("([id,l])=>build(id,l)", [s["id"], LOGO])
            pg.wait_for_timeout(150)
            js = "([t,c,D,f,l])=>setT(t,c,D,f,l)"
            if check:
                d = HERE / "check"; d.mkdir(exist_ok=True)
                times = sorted(set([round(x + 1.0, 2) for x in s["c"]] + [s["D"] - 0.35, 0.9]))
                for t in times:
                    pg.evaluate(js, [t, s["c"], s["D"], s["first"], s["last"]])
                    pg.screenshot(path=str(d / f"{s['id']}_{t:05.2f}.jpg"), type="jpeg", quality=80)
                continue
            fd = HERE / "frames" / s["id"]
            shutil.rmtree(fd, ignore_errors=True); fd.mkdir(parents=True)
            n = int(round(s["D"] * FPS))
            for f in range(n):
                pg.evaluate(js, [f / FPS, s["c"], s["D"], s["first"], s["last"]])
                pg.screenshot(path=str(fd / f"{f:05d}.jpg"), type="jpeg", quality=92)
            out = HERE / "out"; out.mkdir(exist_ok=True)
            tmp, fin = out / f"{s['id']}.tmp.mp4", out / f"{s['id']}.mp4"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(fd / "%05d.jpg"),
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-r", str(FPS), str(tmp)], check=True)
            os.replace(tmp, fin)
            print(s["id"], n, "frames", s["D"], "s", flush=True)
        b.close()


if __name__ == "__main__":
    main()
