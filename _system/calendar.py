#!/usr/bin/env python3
"""Calendar guard for the Softnear PostDesk calendar.

Save the output of PostDesk list_posts(from=<today>, limit=200) as JSON, then:

  python3 _system/calendar.py check posts.json
      -> lists every rule break (exit code 1 if any). Must print OK before
         create_posts / update_post batches are considered done.

  python3 _system/calendar.py next posts.json instagram reel [--after 2026-11-10] [--lang hindi] [--key S5xI8]
      -> prints the next free slot ("YYYY-MM-DD HH:MM") for that platform and
         post type that respects every rule below. Use it for every new reel or
         any post made outside the weekly plan.

Rules (see PLAYBOOK.md "Calendar rules"):
  R1 max one post per platform per day
  R2 weekly caps: instagram 5, facebook 4, linkedin 4 (Mon-Sun, Asia/Kolkata)
  R3 slots: planned posts use PLANNED slots, extra reels/videos use EXTRA slots
  R4 the same service x industry pair never on two platforms on the same day
  R5 one language per piece per platform per week (Hindi and English versions
     of the same piece never in the same week on the same platform)
"""
import json, re, sys, datetime as dt
from collections import defaultdict

CAP = {"instagram": 5, "facebook": 4, "linkedin": 4}
# weekday: 0=Mon ... 6=Sun
PLANNED = {
    "instagram": [(0, "19:30"), (2, "19:30"), (4, "19:30")],
    "facebook": [(1, "18:30"), (3, "18:30"), (5, "11:00")],
    "linkedin": [(1, "13:30"), (2, "13:30"), (3, "13:30")],
}
EXTRA = {  # reel / video slots for content made outside the weekly plan
    "instagram": [(1, "19:30"), (5, "19:30")],
    "facebook": [(0, "18:30")],
    "linkedin": [(4, "13:30")],
}
SKIP = {"failed"}


def load(path):
    posts = json.load(open(path))
    if isinstance(posts, dict):
        posts = posts.get("posts") or posts.get("items") or []
    out = []
    for p in posts:
        if p.get("status") in SKIP or not p.get("scheduled_local"):
            continue
        when = dt.datetime.fromisoformat(p["scheduled_local"][:16])
        title = p.get("title", "")
        m = re.search(r"\bS\d+(?:\+S\d+)?\s*x\s*(?:I\d+|[a-z ]+?)(?=\s+–|\s*$)", title, re.I)
        key = re.sub(r"\s+", "", m.group(0)).lower() if m else None
        lang = "hindi" if re.search(r"hindi", title, re.I) else ("english" if re.search(r"english", title, re.I) else None)
        if lang == "english" and re.search(r"hindi voiceover", title, re.I):
            lang = "hindi"
        out.append(dict(id=p.get("id"), platform=p["platform"], when=when, title=title,
                        key=key, lang=lang, status=p.get("status")))
    return out


def week(d):
    return (d - dt.timedelta(days=d.weekday())).date()


def problems(posts):
    errs = []
    day = defaultdict(list)
    wk = defaultdict(list)
    for p in posts:
        day[(p["platform"], p["when"].date())].append(p)
        wk[(p["platform"], week(p["when"]))].append(p)
    for (pl, d), ps in sorted(day.items()):
        if len(ps) > 1:
            errs.append(f"R1 {pl} {d}: {len(ps)} posts {[x['id'] for x in ps]}")
    for (pl, w), ps in sorted(wk.items()):
        if len(ps) > CAP[pl]:
            errs.append(f"R2 {pl} week of {w}: {len(ps)} posts (cap {CAP[pl]}) {[x['id'] for x in ps]}")
        langs = defaultdict(set)
        for x in ps:
            if x["key"] and x["lang"]:
                langs[x["key"]].add(x["lang"])
        for k, ls in langs.items():
            if len(ls) > 1:
                errs.append(f"R5 {pl} week of {w}: {k} in both Hindi and English")
    same = defaultdict(list)
    for p in posts:
        if p["key"]:
            same[(p["key"], p["when"].date())].append(p)
    for (k, d), ps in sorted(same.items()):
        if len({x["platform"] for x in ps}) > 1:
            errs.append(f"R4 {d}: {k} on {sorted({x['platform'] for x in ps})} {[x['id'] for x in ps]}")
    return errs


def next_slot(posts, platform, kind, after, lang=None, key=None):
    slots = EXTRA[platform] if kind in ("reel", "video", "extra") else PLANNED[platform]
    d = after
    for _ in range(120):
        for wd, hm in slots:
            if d.weekday() != wd:
                continue
            when = dt.datetime.combine(d, dt.time.fromisoformat(hm))
            trial = posts + [dict(id="NEW", platform=platform, when=when, title="", key=key, lang=lang, status="new")]
            if not problems(trial) or set(problems(trial)) <= set(problems(posts)):
                return when
        d += dt.timedelta(days=1)
    return None


def main(a):
    if len(a) < 2 or a[0] not in ("check", "next"):
        print(__doc__); return 2
    posts = load(a[1])
    if a[0] == "check":
        errs = problems(posts)
        print("\n".join(errs) if errs else "OK: calendar follows R1-R5")
        return 1 if errs else 0
    platform, kind = a[2], a[3]
    opts = dict(zip(a[4::2], a[5::2]))
    after = dt.date.fromisoformat(opts.get("--after", (dt.date.today() + dt.timedelta(days=1)).isoformat()))
    w = next_slot(posts, platform, kind, after, opts.get("--lang"), (opts.get("--key") or "").lower() or None)
    print(w.strftime("%Y-%m-%d %H:%M") if w else "no free slot in 120 days")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
