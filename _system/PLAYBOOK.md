# Weekly content run

The scheduled task follows this file every week. It plans next week's Instagram,
Facebook and LinkedIn posts for Softnear using two public skill packs, renders the
media, pushes the media here, and drafts every post into PostDesk for review.
Nothing is published by this job: PostDesk holds every post as "pending review".

## 0. Setup (every run starts in a fresh workspace)

```bash
cd /home/claude
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/Jakeschincariol/instagram-agent-skill ig
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/sergebulaev/linkedin-skills li
# the assets repo needs push access: call add_repo(owner=softneartechnologies, repo=social-assets-softnear, access=push) first
git clone --depth 1 https://github.com/softneartechnologies/social-assets-softnear assets
mkdir -p ~/.claude/instagram && cp assets/_system/brand.md ~/.claude/instagram/voice.md
cp assets/_system/brand.md li/references/voice-profile.md     # filled: yes
python3 -c "import playwright" && which ffmpeg                  # renderer needs both
```

## 1. Target week and context

- Target week = the next Monday to Sunday after today (Asia/Kolkata).
- Week folder: `assets/YYYY-MM/week-MM-DD/` named after that Monday (month of the Monday).
- If that folder already exists, or PostDesk already has posts with campaign `Week of YYYY-MM-DD`, the week is done: only handle rejected posts (below), then stop and report.
- PostDesk `get_studio_info`: note dates/platforms already taken; do not double-book a platform on a day.
- PostDesk `list_posts status=rejected`: read `reviewer_notes`; fix and `update_post` those first, and apply the lesson to this week.
- Read `assets/_system/log.md`: do not repeat an angle or hook formula used in the last 4 weeks.
- Read `assets/_system/brand.md`: facts, pillars, positions, banned words. Never invent numbers or clients.

## 2. Plan (use the skills' own rules)

Read and follow:
- `ig/skills/ig-plan/SKILL.md` for the Instagram week (Proof / Teach / Opinion / Story / Offer mix, hook formula numbers from `ig/skills/ig-reel/hooks.json`).
- `li/skills/linkedin-content-planner/SKILL.md` for the LinkedIn week (pillar mix, F-formula per day, goal mix, inbound-readiness check).

Weekly slots (studio timezone Asia/Kolkata):

| platform | posts | days / times | formats |
| --- | --- | --- | --- |
| LinkedIn | 3 | Tue, Wed, Thu at 13:30 (08:00 UK, 09:00 CET) | 1200x1200 image each |
| Instagram | 3 | Mon 19:30, Wed 19:30, Fri 19:30 | 2 carousels (6-8 slides, 1080x1350) + 1 reel (1080x1920 MP4 from 5-6 text frames) |
| Facebook | 3 | Tue 18:30, Thu 18:30, Sat 11:00 | 1200x1200 image each |

Rules for the mix (lead generation first, see "Lead generation rules" in `brand.md`):
- **Pick this week's targets first.** Choose 3 service x industry pairs from the tables in `brand.md` (e.g. S11 Shopify x I8 Retail, S8 AI automations x I4 Logistics, S2 App development x I7 Healthcare). Read `_system/log.md` and pick pairs not used in the last 4 weeks, so every service and industry gets covered over time.
- Each pair gets one post per platform, rewritten for that platform's buyer:
  - LinkedIn: decision makers (founders, CTOs, ops and marketing heads) in that industry.
  - Instagram: founders and small-business owners; carousels for checklists and cost breakdowns, the reel for the sharpest pain point.
  - Facebook: small and mid-size business owners; plain language, local-business examples.
- Every post: buyer named in the first 2 lines, one pain, one service as the fix, one lead action with a keyword or link, and a lead offer from `brand.md`. Put the keyword and target pair in the PostDesk title, e.g. `W46 – S11xI8 – Shopify speed – keyword SPEED`.
- At least 2 posts a week are direct offers; at most 1 post a week has no service in it (proof or people).
- Use the industry's own words and search terms in captions (e.g. "LMS", "patient app", "dispatch app", "Shopify theme") so Instagram and LinkedIn search can find them. Hashtags: industry + service, specific, never generic.
- Facebook posts can share an idea with LinkedIn/Instagram but are rewritten for small-business owners (`li/skills/linkedin-repurposer/SKILL.md`, `ig/skills/ig-repurpose/SKILL.md`). Never copy-paste between platforms.
- Links: service page + UTM tags (`brand.md`, rule 5).

Write the plan to `WEEK/plan.md` (the calendar table from the skills, plus target pair, buyer, angle, pillar, formula, lead action/keyword and lead offer per post).

## 3. Write the copy

- Instagram carousels: `ig/skills/ig-carousel/SKILL.md` (cover <= 6 words, one idea per slide, recap slide, one CTA). Caption = Job B in `ig/skills/ig-caption/SKILL.md`.
- Instagram reel: `ig/skills/ig-reel/SKILL.md`. Score 3 hooks with `python3 ig/skills/ig-reel/hookscore.py`, keep the best. Caption = Job A. Put the voiceover script and beat sheet (`beats.py`) in the PostDesk `media_brief` so the team can re-shoot it with a face if they want.
- Every Instagram caption: run `python3 ig/skills/ig-human/humanize.py`, then `detect.py` until PASS, then `python3 ig/skills/ig-caption/caption.py FILE --keywords "..."` until READY. No links in IG captions.
- LinkedIn: `li/skills/linkedin-post-writer/SKILL.md` (number-first or statement line 1, never a question first, 900-1,300 chars, closing question, 0-2 hashtags, link in first comment). Then apply `li/skills/linkedin-humanizer/SKILL.md` in audit mode and fix blockers.
- Facebook: conversational, 300-700 chars, one question, link to the relevant softnear.com page in `link_url`. Run it through `humanize.py` + `detect.py` too.

## 4. Render the media

Write `WEEK/week.json`:

```json
{
  "handle": "@official_softnear",
  "posts": [
    {"id": "li-tue-scope", "platform": "linkedin", "format": "image",
     "slides": [{"kind": "headline", "eyebrow": "How we build",
                 "title": "Most projects fail on ~~bad code.~~ unclear scope",
                 "sub": "Nobody agreed on what ==done== looks like.",
                 "chips": ["Scope", "Users", "?Definition of done"]}]},
    {"id": "ig-mon-mvp", "platform": "instagram", "format": "carousel", "slides": [...]},
    {"id": "ig-fri-reel", "platform": "instagram", "format": "reel", "seconds_per_slide": 2.8, "slides": [...]}
  ]
}
```

Slide kinds: `headline` (eyebrow, title, sub, chips), `list` (eyebrow, title, items[{text, tag}], highlight index), `point` (eyebrow, title, body), `stat` (eyebrow, big, title, body), `statement` (eyebrow, title, sub; vertically centred), `cta` (title, body, button).
Markup: `==highlight==`, `~~strike~~`, `**blue**`. A chip starting with `?` is the highlighted one.

```bash
cd assets && python3 _system/render.py YYYY-MM/week-MM-DD/week.json
```

Then open every PNG with the Read tool and check: no text overflowing the footer, nothing clipped, headline readable at thumbnail size, slide counter correct. Shorten copy and re-render until clean.

## 5. Push the media

```bash
cd assets && git add -A && git commit -m "Week of YYYY-MM-DD: plan and media" && git fetch origin main && git rebase origin/main && git push origin HEAD:main
```

Public URL of a file: `https://raw.githubusercontent.com/softneartechnologies/social-assets-softnear/main/<path>`. Check one with `curl -sI` before using them.

## 6. Draft into PostDesk

Use the `postdesk-softnear` connector (tools `mcp__postdesk-softnear__*`).

`create_posts` once with all 9 posts:
- `campaign`: `Week of YYYY-MM-DD`
- `title`: `W<ISO week> – <pillar> – <angle>`
- `content` without hashtags; `hashtags` separate; `first_comment` for the LinkedIn link
- `media_urls`: raw URLs in slide order (reel: the MP4 first)
- `post_type`: post / carousel / reel
- `media_brief`: slide copy, alt text, and for the reel the script and beat sheet

## 7. Log and report

Append to `_system/log.md`: week, each post's platform, service x industry pair, pillar, formula/hook number, angle, keyword. Before planning, also read PostDesk comments/notes and any lead feedback the team leaves in `_system/leads.md`, and plan more of what produced leads. Commit and push.
Finish with a short message: what was planned, the folder link, and anything flagged (rejected posts fixed, `{{number}}` placeholders, render problems).
