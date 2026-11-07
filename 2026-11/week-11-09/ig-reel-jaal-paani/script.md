# Reel: "जाल और पानी" (website = fishing net)

Source: team script, 2026-11-08 (full original in `_system/content-library.md`)
Target: small and local business owners who have a website but get few enquiries · services S5 Website + S10 SEO (traffic)
Keyword: `पता नहीं` (comment) · DM → free 20-minute call
1080x1920 · 30 fps · 58.2 s · text-led animated reel, no voiceover · original score + sound design (`source/music.py`)

## Beat sheet (on-screen text → animation). Times are for recording a voiceover to match.

| time | scene | on screen | animation |
| --- | --- | --- | --- |
| 0:00 | Hook | वेबसाइट है, पर कस्टमर नहीं? · हम वेबसाइट बनाते हैं। और हम ही कह रहे हैं: **वेबसाइट से कस्टमर नहीं आते।** | lines rise, headline slams in with a hit and shake; "आज की इंक्वायरी: 0 · LIVE" card |
| 0:05.6 | Net | वेबसाइट = **मछली पकड़ने का जाल** → जाल कितना भी अच्छा हो, उसे **पानी में** डालना पड़ता है। | website mock turns into a net (mesh draws in, floats pop); water rises, net drops in with a splash, fish swim in |
| 0:13.0 | 3 waters | पानी **3 जगह** है: 1 एड, जहां पैसा लगता है · 2 गूगल, जहां टाइम लगता है · 3 सोशल मीडिया, जहां मेहनत लगती है | three cards rise with waves: coins drop into an ad · clock spins while rank climbs #48 → #3 · posts fill a phone, hearts float |
| 0:23.6 | Dry net | …और बैठ गया, उसके पास एक सुंदर जाल है — **सूखा।** | empty net on poles over cracked ground, sun, tumbleweed, "इंक्वायरी: 0"; music drops to wind; "सूखा।" stamp |
| 0:30.4 | Journey | लोग **एड** से आए, फिर वेबसाइट ने… रेट दिखाया ✓ भरोसा दिया ✓ बटन दिया ✓ · तब वो **कस्टमर** बने | visitors fly from a sponsored ad into a phone site, visitor counter, three rows tick, notifications "नई इंक्वायरी आई", +3 |
| 0:40.0 | Both | दोनों चाहिए। ✕ अकेली वेबसाइट, कुछ नहीं · ✕ एड का पैसा, पानी में · ✓ **जाल + पानी** = कस्टमर | rows rise, coins sink in water, net + water = ✓ |
| 0:47.8 | CTA | आपकी वेबसाइट पर लोग **कहां से** आते हैं? poll: एड से / गूगल से / सोशल मीडिया से / **पता नहीं** → comment box types "पता नहीं" · कमेंट में लिखो "पता नहीं" · या DM करो, बात करते हैं · फ़्री 20 मिनट कॉल · @official_softnear | poll options rise, "पता नहीं" gets tapped and fills yellow, comment types and sends |

## Rebuild
`source/`: `scenes.json` (durations, cues), `stage.html` (all animation), `render.py` (frames → per-scene mp4), `music.py` (score, `python3 music.py music.wav`).
Join scenes with the concat demuxer, then mux `music.wav` (AAC 192k). Needs Playwright, ffmpeg, Inter and Hind fonts.
