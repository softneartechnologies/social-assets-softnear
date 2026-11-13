# Softnear content plan · week of 16 November 2026 (W47)

Built with `ig-plan` + `linkedin-content-planner`, written with `ig-carousel`, `ig-reel`, `ig-caption`, `linkedin-post-writer`. All 6 IG/FB captions pass `ig-human/detect.py` (PASS, 75.6-85.7); the 3 IG captions pass `caption.py` (READY). LinkedIn posts checked against the `linkedin-humanizer` audit rules (statement or number-first line 1, no question opener, 1,130-1,300 chars, no reveal bridges or staccato triads, closing question, P.S., 2 hashtags, link in first comment). Reel hook 87.0 STRONG, beat sheet 16.4 s, clean. Times Asia/Kolkata. All 9 posts are in PostDesk as pending review.

**Results this week:** PostDesk insights say "keep the current plan" (3 scored posts, 0 leads), so no proven/variation/experiment split this week.

## This week's targets (service x industry, none used in the last 4 weeks)

| pair | buyer | pain | keyword | lead offer | page |
|---|---|---|---|---|---|
| S1 Web development x I6 Travel & hospitality | hotel, homestay and resort owners; hotel marketing heads | website hides the rate, no direct booking button | HOTEL | free cost and timeline estimate | /services/web-development |
| S12 AI/ML automations (document AI) x I9 Manufacturing | factory owners, accounts and ops heads at manufacturers | supplier invoices typed into Tally/ERP by hand | INVOICE | free 20-minute call | /services/ai-development |
| S9 UI/UX design x I3 Fintech | founders, product and growth heads of loan, wallet and payments apps | sign-ups lost before/at KYC | KYC | free 20-minute call | /services/ui-ux-design |

From the content library: IG Mon and LI Wed develop the team's "net and water" idea (rate, trust, button on landing; "website is the net, traffic is the water") for hotels, as the library's follow-up ideas suggest.

## Calendar

| Day | Time | Platform | Format | Pair | Pillar | Formula / hook | Angle | Lead action | Goal |
|---|---|---|---|---|---|---|---|---|---|
| Mon 16 | 19:30 | Instagram | Carousel, 8 slides | S1xI6 | Buyer pain + fix (Teach) | #7 Wrong Way, Right Way | Your hotel site hides the price: 3 jobs + net/water | Comment HOTEL | Saves |
| Tue 17 | 13:30 | LinkedIn | Image | S12xI9 | How we build / AI in real software (Authority) | F20 Diverging-Curves Close | Same ERP, two plants, a year apart: AI where the process repeats, plus a review screen | Question + P.S. DM INVOICE + link in first comment | Reposts |
| Tue 17 | 18:30 | Facebook | Image | S9xI3 | Buyer pain + fix | repurposed | Loan/wallet app: 14 fields before KYC, ask 3 | Comment KYC | Comments |
| Wed 18 | 13:30 | LinkedIn | Image | S1xI6 | Buyer pain + fix | F17 Controlled A/B (thought experiment) | Same ad, two websites, one shows the rate | Question + P.S. DM HOTEL + link in first comment | Comments |
| Wed 18 | 19:30 | Instagram | Reel, 6 frames, Hindi VO | S9xI3 | Buyer pain + fix (Opinion) | #3 Nobody Tells You (87.0) | 14 KYC questions kill sign-ups | Comment KYC | Reach |
| Thu 19 | 13:30 | LinkedIn | Image | S9xI3 | Offer | F2 R.I.P. Obituary | R.I.P. the sign-up form that asks everything first; same KYC, different order | DM KYC + link in first comment | Reposts/DMs |
| Thu 19 | 18:30 | Facebook | Image | S12xI9 | Buyer pain + fix | repurposed | Factories: stop typing supplier invoices | Comment INVOICE | Comments |
| Fri 20 | 19:30 | Instagram | Carousel, 7 slides | S12xI9 | Offer | #12 The Objection | "AI will get our invoices wrong." Read, draft, flag, approve | Comment INVOICE | Comments |
| Sat 21 | 11:00 | Facebook | Image | S1xI6 | Offer | repurposed | Homestays: guests shouldn't call for the price | Comment HOTEL | Comments |

Already in the week (carried over, not part of this plan): FB Mon 16 net&water Hindi reel (#34), IG Tue 17 net&water English reel (#36), LI Fri 20 net&water video (#35), IG Sat 21 website price reel (#30). Week totals: IG 5/5, FB 4/4, LI 4/4. R4: no pair on two platforms on the same day.

Direct offers: 3 (LI Thu, IG Fri, FB Sat). Posts with no service: 0. Pillars: Buyer pain + fix 5, Offer 3, How we build/AI 1.

**Engagement (20 min/day):** 5 reach accounts (hospitality marketing, fintech product and Indian manufacturing/MSME voices), 3 peer dev agencies, 2 buyer accounts (boutique hotel groups, NBFC/lending apps, mid-size manufacturers). Never pitch in a comment.

**Inbound-readiness check:** receipt/data post: none this week (no new public numbers in brand.md) · soft offer ✓ · no pillar over 60% ✓ · no formula repeated in 4 weeks ✓ · goal mix saves/comments/reposts/reach ✓. Missing again: a vulnerability/story post (needs a real team story).

## For the team to confirm before approving

- **Reel (IG Wed) has no voiceover yet.** Bloom generated both voiceovers (Hindi and English), but the cloud run could not download them. PostDesk holds the silent cut. Build `reel-hi.mp4` with `ig-wed-reel-kyc/source/build_vo.py` (see `script.md`) and swap the media before approving.
- "14 fields / 14 questions" is an illustrative number for a long sign-up form, not a statistic. Change it if you prefer.
- Process claims written by the planner: LI Tue / FB Thu / IG Fri say document AI fills a **draft** in **Tally, SAP Business One or the ERP** and flags low-confidence fields for review; LI Thu / reel / FB Tue suggest showing the offer before documents (check this against your lending clients' compliance rules); IG Mon / LI Wed / FB Sat describe what we build into hotel sites (booking engine, map, reviews, WhatsApp button) and "the checklist we work from". Adjust if the real process or stack differs.
- Someone must reply to HOTEL, INVOICE and KYC comments/DMs.
- English-voiceover reel for LinkedIn is not scheduled (LI's extra slot this week is taken). Add it to a later free slot if wanted: `calendar.py next posts.json linkedin video --key S9xI3 --lang english`.

Copy: `copy/` · Media: one folder per post · Reel script, voiceovers and rebuild: `ig-wed-reel-kyc/script.md`, `reel-beats.txt`.
