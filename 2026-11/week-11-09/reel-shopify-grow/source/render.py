#!/usr/bin/env python3
"""Render the Shopify / e-commerce "GROW" reel scene by scene from stage.html.

TIMING=timing_hi.json REEL_WORK=dir python3 render.py --check     stills at key moments -> dir/check/
TIMING=timing_hi.json REEL_WORK=dir python3 render.py [scene ids]  frames + one mp4 per scene -> dir/out/
Timing files come from timing.py (scene lengths and cues from the voiceover).
Needs Playwright (chromium), ffmpeg, and the Inter + Hind fonts installed.
"""
import base64, json, os, subprocess, sys, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
REPO = HERE.parents[3]
FPS = 30
LOGO = "data:image/png;base64," + base64.b64encode((REPO / "_system/assets/softnear-logo.png").read_bytes()).decode()
SCENES = json.loads(Path(os.environ.get("TIMING", HERE / "timing_en.json")).read_text())
WORK = Path(os.environ.get("REEL_WORK", HERE / "work"))


def main():
    args = sys.argv[1:]
    check = "--check" in args
    only = [a for a in args if not a.startswith("-")]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto((HERE / "stage.html").as_uri())
        pg.evaluate("document.fonts.ready")
        for i, s in enumerate(SCENES):
            if only and s["id"] not in only:
                continue
            first, last = i == 0, i == len(SCENES) - 1
            pg.evaluate("([id,l])=>build(id,l)", [s["id"], LOGO])
            pg.wait_for_timeout(200)
            js = "([t,c,D,f,l])=>setT(t,c,D,f,l)"
            if check:
                d = WORK / "check"; d.mkdir(parents=True, exist_ok=True)
                times = sorted(set([round(x + .9, 2) for x in s["cues"]] + [s["D"] - .35]))
                for t in times:
                    pg.evaluate(js, [t, s["cues"], s["D"], first, last])
                    pg.screenshot(path=str(d / f"{s['id']}_{t:05.2f}.jpg"), type="jpeg", quality=80)
                continue
            fd = WORK / "frames" / s["id"]
            shutil.rmtree(fd, ignore_errors=True); fd.mkdir(parents=True)
            n = int(round(s["D"] * FPS))
            for f in range(n):
                pg.evaluate(js, [f / FPS, s["cues"], s["D"], first, last])
                pg.screenshot(path=str(fd / f"{f:05d}.jpg"), type="jpeg", quality=92)
            out = WORK / "out"; out.mkdir(parents=True, exist_ok=True)
            tmp, fin = out / f"{s['id']}.tmp.mp4", out / f"{s['id']}.mp4"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(fd / "%05d.jpg"),
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-r", str(FPS), str(tmp)], check=True)
            os.replace(tmp, fin)
            shutil.rmtree(fd, ignore_errors=True)
            print(s["id"], n, "frames", flush=True)
        b.close()


if __name__ == "__main__":
    main()
