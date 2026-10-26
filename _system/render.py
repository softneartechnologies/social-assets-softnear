#!/usr/bin/env python3
"""Render a week's Softnear social media from a JSON spec.

Usage:
    python3 _system/render.py weeks/2026-11-02/week.json

The spec lists posts; each post has slides. Output goes next to the spec:
    <week dir>/<post id>/slide-01.png ...   (images / carousels)
    <week dir>/<post id>/reel.mp4           (reels, built from the slides)
and a manifest.json mapping post id -> list of repo-relative file paths.

Slide kinds: headline, list, point, stat, statement, cta.
Inline markup in any text field: ==highlight==  ~~strike~~  **bold-blue**
"""
import html
import json
import re
import subprocess
import sys
import base64
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
LOGO = base64.b64encode((ROOT / "assets" / "softnear-logo.png").read_bytes()).decode()

SIZES = {
    "instagram": (1080, 1350),
    "facebook": (1200, 1200),
    "linkedin": (1200, 1200),
    "reel": (1080, 1920),
}

CSS = """
:root{--bg:#F7F9FC;--ink:#0F172A;--muted:#475569;--blue:#3B8DF0;--yellow:#FFD635;
--yellow-soft:#FFF6D1;--card:#FFFFFF;--line:#E3E8F0;--deco-b:#E8EFFA;--deco-y:#F7F5E8}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:var(--w);height:var(--h);background:var(--bg);font-family:'Inter Display','Inter',sans-serif;color:var(--ink);overflow:hidden}
.page{position:relative;width:100%;height:100%;padding:var(--pad-top) var(--pad) 0 var(--pad);display:flex;flex-direction:column}
.deco{position:absolute;border-radius:90px;transform:rotate(45deg);z-index:0}
.d1{width:56%;height:56%;right:-24%;top:-24%;background:var(--deco-b);opacity:.75}
.d2{width:30%;height:30%;right:-14%;top:-6%;background:var(--deco-y);border-radius:110px;opacity:.9}
.d3{display:none}
.content{position:relative;z-index:1;flex:1;display:flex;flex-direction:column;padding-bottom:calc(var(--u)*44px);min-height:0}
.eyebrow{display:flex;align-items:center;gap:18px;color:var(--blue);font-family:'Inter';font-weight:700;letter-spacing:.16em;text-transform:uppercase;font-size:calc(var(--u)*24px)}
.eyebrow:before{content:"";width:46px;height:7px;border-radius:4px;background:var(--yellow)}
h1{font-weight:700;letter-spacing:-.035em;line-height:1.04;margin-top:calc(var(--u)*34px)}
.t-xl{font-size:calc(var(--u)*96px)} .t-l{font-size:calc(var(--u)*80px)} .t-m{font-size:calc(var(--u)*64px)} .t-s{font-size:calc(var(--u)*52px)}
.sub{font-family:'Inter';font-weight:500;font-size:calc(var(--u)*44px);line-height:1.3;letter-spacing:-.015em;margin-top:calc(var(--u)*56px);max-width:92%}
.body{font-family:'Inter';font-weight:400;color:var(--muted);font-size:calc(var(--u)*38px);line-height:1.42;margin-top:calc(var(--u)*40px);max-width:94%}
.hl{background:linear-gradient(transparent 58%,var(--yellow) 58%,var(--yellow) 96%,transparent 96%);padding:0 4px}
.st{color:#4B5563;text-decoration:line-through;text-decoration-color:var(--blue);text-decoration-thickness:.09em}
.bb{color:var(--blue)}
.chips{display:flex;flex-wrap:wrap;gap:20px;margin-top:calc(var(--u)*64px)}
.chip{display:flex;align-items:center;gap:14px;font-family:'Inter';font-weight:500;font-size:calc(var(--u)*30px);color:var(--muted);background:var(--card);border:2px solid var(--line);border-radius:16px;padding:18px 26px}
.chip i{width:30px;height:30px;border:3px solid var(--blue);border-radius:7px;display:inline-flex;align-items:center;justify-content:center;color:var(--blue);font-style:normal;font-size:18px;font-weight:800}
.chip.on{background:var(--yellow-soft);border-color:var(--yellow);color:var(--ink);font-weight:600}
.chip.on i{border-color:var(--ink);color:var(--ink)}
.items{display:flex;flex-direction:column;gap:calc(var(--u)*28px);margin-top:calc(var(--u)*64px)}
.item{display:flex;gap:calc(var(--u)*52px);align-items:flex-start;background:var(--card);border:2px solid var(--line);border-radius:28px;padding:calc(var(--u)*40px) calc(var(--u)*40px)}
.item.on{background:var(--yellow);border-color:var(--yellow)}
.item .n{font-weight:700;font-size:calc(var(--u)*54px);color:var(--blue);letter-spacing:-.03em;min-width:calc(var(--u)*72px);line-height:1}
.item.on .n{color:var(--ink)}
.item .tx{font-weight:500;font-size:calc(var(--u)*36px);line-height:1.3;letter-spacing:-.01em}
.items.compact{gap:calc(var(--u)*16px);margin-top:calc(var(--u)*44px)}
.items.compact .item{padding:calc(var(--u)*24px) calc(var(--u)*34px);border-radius:22px;gap:calc(var(--u)*36px);align-items:center}
.items.compact .n{font-size:calc(var(--u)*40px);min-width:calc(var(--u)*56px)}
.items.compact .tx{font-size:calc(var(--u)*32px)}
.tag{display:inline-block;margin-top:14px;background:var(--ink);color:#fff;font-family:'Inter';font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:calc(var(--u)*20px);padding:9px 16px;border-radius:8px}
.big{font-weight:700;letter-spacing:-.05em;line-height:.95;font-size:calc(var(--u)*200px);margin-top:calc(var(--u)*50px);color:var(--ink)}
.big .unit{color:var(--blue)}
.btn{align-self:flex-start;margin-top:calc(var(--u)*60px);background:var(--ink);color:#fff;font-family:'Inter';font-weight:700;font-size:calc(var(--u)*32px);padding:24px 36px;border-radius:18px}
.btn b{color:var(--yellow)}
.counter{position:absolute;top:calc(var(--pad-top) - 6px);right:var(--pad);z-index:2;font-family:'Inter';font-weight:700;font-size:calc(var(--u)*24px);color:var(--ink);background:#fff;border:2px solid var(--line);border-radius:30px;padding:8px 18px}
.footer{position:relative;z-index:1;border-top:2px solid var(--line);height:var(--foot);display:flex;align-items:center;justify-content:space-between}
.footer img{height:68px}
.footer span{font-family:'Inter';font-weight:600;font-size:calc(var(--u)*28px);color:var(--muted)}
.center{justify-content:center}
"""


def md(text):
    t = html.escape(text or "")
    t = re.sub(r"==(.+?)==", r'<span class="hl">\1</span>', t)
    t = re.sub(r"~~(.+?)~~", r'<span class="st">\1</span>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r'<span class="bb">\1</span>', t)
    return t.replace("\n", "<br>")


def title_class(text, kind):
    n = len(re.sub(r"[=~*]", "", text or ""))
    if kind == "stat":
        return "t-s"
    if n <= 28:
        return "t-xl"
    if n <= 60:
        return "t-l"
    if n <= 95:
        return "t-m"
    return "t-s"


def slide_html(s, w, h, idx, total, handle, center=False):
    kind = s.get("kind", "headline")
    u = w / 1080 * (1.3 if h >= 1900 else 1)
    parts = []
    if s.get("eyebrow"):
        parts.append(f'<div class="eyebrow">{md(s["eyebrow"])}</div>')
    if kind == "stat":
        parts.append(f'<div class="big">{md(s.get("big",""))}</div>')
    if s.get("title"):
        tc = title_class(s["title"], kind)
        if idx == 1 and total > 1 and kind == "headline":
            tc = {"t-l": "t-xl", "t-m": "t-l"}.get(tc, tc)
        if kind == "list" and len(s.get("items", [])) > 2:
            tc = {"t-xl": "t-l", "t-l": "t-m"}.get(tc, tc)
        parts.append(f'<h1 class="{tc}">{md(s["title"])}</h1>')
    if s.get("sub"):
        parts.append(f'<div class="sub">{md(s["sub"])}</div>')
    if s.get("body"):
        parts.append(f'<div class="body">{md(s["body"])}</div>')
    if s.get("items"):
        rows = []
        for i, it in enumerate(s["items"]):
            it = it if isinstance(it, dict) else {"text": it}
            on = " on" if s.get("highlight") == i or it.get("on") else ""
            tag = f'<div><span class="tag">{md(it["tag"])}</span></div>' if it.get("tag") else ""
            rows.append(f'<div class="item{on}"><div class="n">{i+1:02d}</div><div class="tx">{md(it["text"])}{tag}</div></div>')
        compact = " compact" if (len(rows) > 4 or s.get("compact")) else ""
        parts.append(f'<div class="items{compact}">' + "".join(rows) + "</div>")
    if s.get("chips"):
        chips = []
        for c in s["chips"]:
            on = c.startswith("?")
            label = c[1:] if on else c
            chips.append(f'<div class="chip{" on" if on else ""}"><i>{"?" if on else "✓"}</i>{md(label)}</div>')
        parts.append('<div class="chips">' + "".join(chips) + "</div>")
    if kind == "cta" and s.get("button"):
        parts.append(f'<div class="btn">{md(s["button"])}</div>')
    counter = f'<div class="counter">{idx}/{total}</div>' if total > 1 else ""
    right = handle if total > 1 else "softnear.com"
    pad = 90 * (w / 1080)
    pad_top = (330 if h >= 1900 else 160) * u if kind != "cta" else (300 * u)
    if kind == "list" and h < 1900:
        pad_top = 120 * u
    foot = 180 * u if h >= 1900 else 170 * u
    vcenter = " center" if (center or kind in ("cta", "statement") or h >= 1900
                          or (h > w and kind != "list")) else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
:root{{--w:{w}px;--h:{h}px;--u:{u};--pad:{pad}px;--pad-top:{pad_top}px;--foot:{foot}px}}</style></head>
<body><div class="page"><div class="deco d1"></div><div class="deco d2"></div><div class="deco d3"></div>{counter}
<div class="content{vcenter}">{''.join(parts)}</div>
<div class="footer"><img src="data:image/png;base64,{LOGO}"><span>{html.escape(right)}</span></div></div></body></html>"""


def build_reel(frames, out, seconds):
    """Turn slide frames into a 1080x1920 MP4 with short crossfades."""
    n = len(frames)
    inputs = []
    for f in frames:
        inputs += ["-loop", "1", "-t", str(seconds), "-i", str(f)]
    fade = 0.4
    if n == 1:
        flt = "[0:v]format=yuv420p[v]"
    else:
        chain, prev = [], "[0:v]"
        for i in range(1, n):
            offset = i * (seconds - fade)
            label = f"[x{i}]" if i < n - 1 else "[xv]"
            chain.append(f"{prev}[{i}:v]xfade=transition=slideleft:duration={fade}:offset={offset:.2f}{label}")
            prev = label
        flt = ";".join(chain) + ";[xv]format=yuv420p[v]"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", flt, "-map", "[v]",
           "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)


def main(spec_path):
    spec_path = Path(spec_path).resolve()
    week_dir = spec_path.parent
    repo = ROOT.parent
    spec = json.loads(spec_path.read_text())
    handle = spec.get("handle", "@official_softnear")
    manifest = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for post in spec["posts"]:
            fmt = post.get("format", "image")
            key = "reel" if fmt == "reel" else post["platform"]
            w, h = SIZES[key]
            out_dir = week_dir / post["id"]
            out_dir.mkdir(parents=True, exist_ok=True)
            for old in out_dir.glob("*"):
                old.unlink()
            page = browser.new_page(viewport={"width": w, "height": h})
            slides = post["slides"]
            total = len(slides) if fmt in ("carousel", "reel") else 1
            files = []
            for i, s in enumerate(slides, 1):
                page.set_content(slide_html(s, w, h, i, total if fmt == "carousel" else 1, handle))
                page.wait_for_timeout(150)
                over = page.evaluate("(() => {const c=document.querySelector('.content');return c.scrollHeight - c.clientHeight})()")
                if over > 2:
                    print(f"  WARNING {post['id']} slide {i}: content overflows by {over}px - shorten the copy")
                f = out_dir / f"slide-{i:02d}.png"
                page.screenshot(path=str(f))
                files.append(f)
            page.close()
            if fmt == "reel":
                mp4 = out_dir / "reel.mp4"
                build_reel(files, mp4, post.get("seconds_per_slide", 2.8))
                cover = files[0]
                manifest[post["id"]] = [str(mp4.relative_to(repo)), str(cover.relative_to(repo))]
            else:
                manifest[post["id"]] = [str(f.relative_to(repo)) for f in files]
            print(post["id"], "->", len(files), "file(s)")
        browser.close()
    (week_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print("manifest written:", week_dir / "manifest.json")


if __name__ == "__main__":
    main(sys.argv[1])
