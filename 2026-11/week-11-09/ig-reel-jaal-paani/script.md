# Reel: "Net and water" (website = fishing net)

Source: team script, 2026-11-08 (full original in `_system/content-library.md`)
Target: small and local business owners who have a website but get few enquiries · services S5 Website + S10 SEO (traffic)
Keyword: comment `DON'T KNOW` (Hindi viewers may write `पता नहीं`: treat both the same) · DM → free 20-minute call
1080x1920 · 30 fps · on-screen text in English · original score + sound design (`source/music.py`)

Two versions, same visuals, timed to their own voice:

| file | voiceover | length |
| --- | --- | --- |
| `reel-hi.mp4` | Hindi (ElevenLabs v4 "Christopher" via Bloom) | 62.2 s |
| `reel-en.mp4` | English (ElevenLabs v4 "Christopher" via Bloom) | 58.4 s |

## Script (voiceover → on screen)

| scene | Hindi voiceover | English voiceover | on screen (English, both versions) |
| --- | --- | --- | --- |
| Hook | हम वेबसाइट बनाते हैं। और हम ही कह रहे हैं। वेबसाइट से कस्टमर नहीं आते। | We build websites. And we're the ones telling you. A website alone won't bring you customers. | Got a website, but no customers? · We build websites. And we're telling you: **A website alone won't bring customers.** · "Enquiries today: 0" |
| Net | वेबसाइट, मछली पकड़ने का जाल है। जाल कितना भी अच्छा हो। उसे पानी में डालना पड़ता है। | Your website is a fishing net. However good the net is. It has to go in the water. | Your website = **a fishing net** → However good the net, it has to go **in the water.** (net draws, water rises, splash, fish) |
| 3 waters | पानी तीन जगह है। एड, जहां पैसा लगता है। गूगल, जहां टाइम लगता है। और सोशल मीडिया, जहां मेहनत लगती है। | And the water is in three places. Ads, where it costs money. Google, where it costs time. And social media, where it costs effort. | It's in **3 places**: Ads · costs money / Google · costs time / Social media · costs effort (coins, clock + rank, posts + hearts) |
| Dry net | जिसने सिर्फ़ वेबसाइट बनाई, और बैठ गया। उसके पास एक सुंदर जाल है। सूखा। | Build a website and just sit back. You've got a beautiful net. Bone dry. | Built a website and waited? …and just sat back? You've got a beautiful net — **Bone dry.** |
| Journey | लोग एड से आए। वेबसाइट ने रेट दिखाया। भरोसा दिया। बटन दिया। तब वो कस्टमर बने। | People came from an ad. The website showed the price. Built trust. Gave them a button. That's when they became customers. | People came from **an ad**, then the website… Showed the price ✓ Built trust ✓ Gave a button ✓ · That's when they became **customers** +3 |
| Both | दोनों चाहिए। अकेली वेबसाइट, कुछ नहीं। और बिना वेबसाइट के, एड का पैसा पानी में। जाल और पानी, दोनों चाहिए। | You need both. A website alone does nothing. And without a website, your ad money goes in the water. Net and water. You need both. | You need both. ✕ A website alone does nothing · ✕ Ad money, thrown in the water · ✓ **Net + water** = customers |
| CTA | आपकी वेबसाइट पर लोग कहां से आते हैं? पता नहीं? तो कमेंट में लिखो, डोंट नो। या डीएम करो, बात करते हैं। | So where do your website visitors come from? Don't know? Comment, don't know. Or DM us, and let's talk. | Where do your website visitors **come from?** poll: From ads / From Google / From social media / **Don't know** → comment types DON'T KNOW · Or DM us, let's talk · free 20-minute call · @official_softnear |

## Rebuild
`source/`: `stage.html` (all animation), `timing.py` (scene lengths and cues from each voiceover's sentence starts → `timing_hi.json`, `timing_en.json`), `render.py` (frames → per-scene mp4), `music.py` (score, sound effects on the same cues, voiceover mix with ducking).

```bash
python3 timing.py vo/hi hi timing_hi.json
TIMING=timing_hi.json REEL_WORK=work/hi python3 render.py
python3 music.py timing_hi.json vo/hi mix_hi.wav
# concat work/hi/out/*.mp4, mux mix_hi.wav (AAC 192k, loudnorm I=-14)
```
Voice files are not committed. To swap in a human recording, save one file per scene as `vo/<lang>/01.wav`…`07.wav` (same sentences) and rerun the steps.
