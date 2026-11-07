#!/usr/bin/env python3
"""Render the Hindi 'Rs 5,000 vs Rs 25,000 website' reel frames.

Reuses the brand CSS, markup and logo from _system/render.py and adds a
Devanagari font (Hind) plus reveal states. Writes frames/<scene>/s<k>_<f>.png
"""
import base64
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "social-assets-softnear" / "_system"))
import render as R  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

from scenes import SCENES, PROG  # noqa: E402

W, H = 1080, 1920
HERE = Path(__file__).parent
FONTS = HERE / "fonts/fontsource-hind-5.3.0/package/files"
FACES = "".join(
    "@font-face{font-family:'Hind';font-weight:%d;src:url(data:font/woff2;base64,%s) format('woff2');}"
    % (wt, base64.b64encode((FONTS / f"hind-devanagari-{wt}-normal.woff2").read_bytes()).decode())
    for wt in (400, 500, 600, 700)
)
def md(t):
    return R.md(t).replace('&lt;br&gt;', '<br>')

EXTRA = """
html,body{font-family:'Inter Display','Inter','Hind',sans-serif}
.eyebrow,.sub,.body,.btn,.footer span,.chip{font-family:'Inter','Hind',sans-serif}
.page{padding:250px 84px 0 84px}
.content{justify-content:center;padding-bottom:40px}
h1{font-size:104px}
.hook h1{font-size:120px}
h1{;line-height:1.22;letter-spacing:-.02em;margin-top:40px}
h1.sm{font-size:92px}
.eyebrow{font-size:32px;letter-spacing:.08em}
.eyebrow:before{width:56px;height:9px}
.hl{background:linear-gradient(transparent 55%,var(--yellow) 55%,var(--yellow) 94%,transparent 94%)}
.footer{height:230px}
.footer img{height:92px}
.footer span{font-size:36px}
.r0{opacity:var(--p0);transform:translateY(calc((1 - var(--p0)) * 46px))}
.r1{opacity:var(--p1);transform:translateY(calc((1 - var(--p1)) * 46px))}
.r2{opacity:var(--p2);transform:translateY(calc((1 - var(--p2)) * 46px))}
.pill{display:inline-flex;align-items:center;gap:12px;margin-top:70px;align-self:flex-start;background:var(--ink);color:#fff;
  font-family:'Inter','Hind';font-weight:600;font-size:44px;padding:22px 36px;border-radius:22px}
.pill b{color:var(--yellow)}
/* progress */
.prog{display:flex;gap:12px;margin-bottom:56px}
.prog div{flex:1;text-align:center;font-family:'Inter','Hind';font-weight:600;font-size:28px;padding:14px 0 10px;border-radius:14px;
  background:#fff;border:2px solid var(--line);color:#94A3B8}
.prog .done{background:var(--deco-b);border-color:var(--deco-b);color:var(--blue)}
.prog .now{background:var(--yellow);border-color:var(--yellow);color:var(--ink)}
/* compare cards */
.cards{display:flex;flex-direction:column;gap:30px;margin-top:70px}
.card{border-radius:32px;padding:40px 44px;display:flex;gap:34px;align-items:flex-start}
.card .ic{flex:none;width:76px;height:76px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-family:'Inter';font-weight:800;font-size:40px}
.card .lb{font-family:'Inter','Hind';font-weight:700;font-size:28px;letter-spacing:.06em;margin-bottom:8px}
.card .tx{font-family:'Inter','Hind';font-weight:600;font-size:50px;line-height:1.3}
.bad{background:#fff;border:2px solid var(--line)}
.bad .ic{background:#EEF1F5;color:#64748B}
.bad .lb{color:#94A3B8}
.bad .tx{color:#64748B;font-weight:500}
.good{background:var(--yellow)}
.good .ic{background:var(--ink);color:var(--yellow)}
.good .lb{color:var(--ink)}
.good .tx{color:var(--ink)}
/* setup mockups */
.duo{display:flex;gap:36px;margin-top:80px;align-items:flex-end}
.mock{flex:1;background:#fff;border:2px solid var(--line);border-radius:28px;overflow:hidden}
.mock .bar{height:46px;background:#EEF1F5;display:flex;gap:10px;align-items:center;padding-left:20px}
.mock .bar i{width:14px;height:14px;border-radius:50%;background:#CBD5E1}
.mock .hero{height:330px;margin:22px;border-radius:18px;background:var(--deco-b)}
.mock .ln{height:20px;margin:16px 22px;border-radius:10px;background:#E8ECF2}
.mock .ln.s{width:55%}
.mock .bt{width:42%;height:52px;margin:24px 22px 28px;border-radius:14px;background:var(--blue)}
.price{font-family:'Inter';font-weight:800;font-size:58px;text-align:center;margin-bottom:22px;letter-spacing:-.02em}
.eq{font-family:'Inter';font-weight:800;font-size:90px;color:var(--blue);align-self:center;margin-top:60px}
.chips5{display:flex;flex-wrap:wrap;gap:18px;margin-top:56px}
.chips5 div{font-family:'Inter','Hind';font-weight:600;font-size:40px;background:#fff;border:2px solid var(--line);border-radius:18px;padding:16px 28px 10px}
.chips5 div b{color:var(--blue);font-family:'Inter';margin-right:12px}
.title-swap{position:relative;height:150px;margin-top:40px}
.title-swap h1{position:absolute;left:0;top:0;margin:0}
/* invest */
.rows{display:flex;flex-direction:column;gap:30px;margin-top:70px}
.row{border-radius:32px;padding:44px 48px;font-family:'Inter','Hind';font-size:62px;font-weight:600;line-height:1.25}
.row small{display:block;font-family:'Inter','Hind';font-size:30px;font-weight:700;letter-spacing:.06em;margin-bottom:6px}
.row.w{background:#fff;border:2px solid var(--line);color:#64748B}
.row.w small{color:#94A3B8}
.row.y{background:var(--yellow);color:var(--ink)}
.payoff{font-family:'Inter','Hind';font-weight:700;font-size:84px;line-height:1.25;margin-top:80px}
/* cta */
.qs{display:flex;flex-direction:column;gap:18px;margin-top:56px}
.q{display:flex;gap:30px;align-items:center;background:#fff;border:2px solid var(--line);border-radius:24px;padding:24px 34px 18px}
.q .n{font-family:'Inter';font-weight:800;font-size:40px;color:var(--blue);min-width:56px}
.q .t{font-family:'Inter','Hind';font-weight:600;font-size:44px}
.ctabox{margin-top:44px;background:var(--ink);border-radius:32px;padding:40px 48px;color:#fff}
.ctabox .k{font-family:'Inter','Hind';font-weight:600;font-size:42px;color:#CBD5E1}
.ctabox .kw{font-family:'Inter Display';font-weight:800;font-size:112px;color:var(--yellow);letter-spacing:-.02em;line-height:1.05;margin:6px 0 10px}
.ctabox .f{font-family:'Inter','Hind';font-weight:500;font-size:38px;color:#E2E8F0}
"""


def progress(n):
    cells = []
    for i, name in enumerate(PROG, 1):
        cls = "done" if i < n else ("now" if i == n else "")
        cells.append(f'<div class="{cls}">{name}</div>')
    return f'<div class="prog r0">{"".join(cells)}</div>'


def body(s):
    k = s["kind"]
    eb = f'<div class="eyebrow r0">{md(s["eyebrow"])}</div>'
    if k == "hook":
        return (eb + f'<h1 class="r0" style="font-size:120px">{md(s["title"])}</h1>'
                + f'<div class="pill r1">{md(s["sub"])} <b>→</b></div>')
    if k == "setup":
        def mock(price):
            return (f'<div><div class="price">{price}</div><div class="mock"><div class="bar"><i></i><i></i><i></i></div>'
                    '<div class="hero"></div><div class="ln"></div><div class="ln s"></div><div class="bt"></div></div></div>')
        chips = "".join(f"<div><b>{i}</b>{p}</div>" for i, p in enumerate(PROG, 1))
        return (eb
                + f'<div class="title-swap"><h1 class="sm" style="opacity:calc(1 - var(--p1))">{md(s["title_a"])}</h1>'
                + f'<h1 class="sm" style="opacity:var(--p1)">{md(s["title_b"])}</h1></div>'
                + f'<div class="duo r0">{mock("₹5,000")}<div class="eq">=</div>{mock("₹25,000")}</div>'
                + f'<div class="chips5 r1">{chips}</div>')
    if k == "compare":
        return (progress(s["n"]) + eb + f'<h1 class="r0 sm">{md(s["title"])}</h1>'
                + '<div class="cards">'
                + f'<div class="card bad r0"><div class="ic">✕</div><div><div class="lb">₹5,000 वाली</div><div class="tx">{md(s["bad"])}</div></div></div>'
                + f'<div class="card good r1"><div class="ic">✓</div><div><div class="lb">₹25,000 वाली</div><div class="tx">{md(s["good"])}</div></div></div>'
                + '</div>')
    if k == "invest":
        return (eb + '<div class="rows">'
                + '<div class="row w r0"><small>₹5,000 वाली</small>सस्ती वेबसाइट = खर्चा</div>'
                + '<div class="row y r1"><small>₹25,000 वाली</small>सही वेबसाइट = इन्वेस्टमेंट</div>'
                + '</div><div class="payoff r2">एक ऑर्डर आया,<br><span class="hl">पैसा वसूल।</span></div>')
    if k == "cta":
        qs = "".join(f'<div class="q"><div class="n">{i:02d}</div><div class="t">{q}</div></div>'
                     for i, q in enumerate(s["qs"], 1))
        return (eb + f'<h1 class="r0 sm">{md(s["title"])}</h1><div class="qs r0">{qs}</div>'
                + '<div class="ctabox r1"><div class="k">अपनी वेबसाइट फ़्री में चेक करवाएँ, कमेंट कीजिए</div>'
                + '<div class="kw">WEBSITE</div><div class="f">और फ़ॉलो कीजिए @official_softnear</div></div>')
    raise ValueError(k)


def page_html(s):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FACES}{R.CSS}{EXTRA}
:root{{--w:{W}px;--h:{H}px;--u:1;--pad:84px;--pad-top:250px;--foot:230px;--p0:1;--p1:0;--p2:0}}</style></head>
<body><div class="page"><div class="deco d1"></div><div class="deco d2"></div>
<div class="content">{body(s)}</div>
<div class="footer"><img src="data:image/png;base64,{R.LOGO}"><span>softnear.com</span></div></div></body></html>"""


def ease(t):
    return 1 - (1 - t) ** 3


def nstates(s):
    return 3 if s["kind"] == "invest" else 2


def main(only=None, stills=False):
    out = HERE / "frames"
    plan = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for s in SCENES:
            if only and s["id"] not in only:
                continue
            d = out / s["id"]
            d.mkdir(parents=True, exist_ok=True)
            for f in d.glob("*.png"):
                f.unlink()
            pg.set_content(page_html(s))
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(200)
            over = pg.evaluate("(()=>{const c=document.querySelector('.content');return c.scrollHeight-c.clientHeight})()")
            if over > 2:
                print("WARNING overflow", s["id"], over)
            seq = []
            n = nstates(s)
            for k in range(n):
                steps = [1.0] if stills else [ease(i / 9) for i in range(1, 10)]
                for j, v in enumerate(steps):
                    vals = {f"--p{m}": (1 if m < k else (v if m == k else 0)) for m in range(3)}
                    pg.evaluate("v=>{for(const[k,x] of Object.entries(v))document.documentElement.style.setProperty(k,x)}", vals)
                    f = d / f"s{k}_{j:02d}.png"
                    pg.screenshot(path=str(f))
                    seq.append(f.name)
            plan[s["id"]] = seq
            print(s["id"], len(seq), "frames")
        b.close()
    (out / "plan.json").write_text(json.dumps(plan, indent=1))


if __name__ == "__main__":
    args = sys.argv[1:]
    main(only=[a for a in args if not a.startswith("-")] or None, stills="--stills" in args)
