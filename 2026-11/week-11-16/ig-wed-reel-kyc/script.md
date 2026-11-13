# Reel: "14 KYC questions kill sign-ups" (S9 UI/UX x I3 Fintech)

Target: founders and product heads of loan, wallet and payments apps in India · keyword `KYC` · free 20-minute call
Hook: #3 Nobody Tells You, "Nobody tells you: 14 KYC questions kill sign-ups." scored 87.0 STRONG (hookscore.py). Beat sheet: `../reel-beats.txt` (16.4 s at 165 wpm, clean).
1080x1920 · 6 English text frames rendered by `_system/render.py` · on-screen text English in both versions.

| frame | on screen (English) | English voiceover | Hindi voiceover |
| --- | --- | --- | --- |
| 1 | 14 KYC questions **kill sign-ups.** | Nobody tells you: fourteen KYC questions kill sign-ups. | कोई नहीं बताता: KYC से पहले चौदह सवाल, और साइन-अप खत्म। |
| 2 | Wanted the loan. **Form kept going.** | They wanted the loan. The form kept going. | यूज़र को लोन चाहिए था। पर फॉर्म खत्म ही नहीं हुआ। |
| 3 | Ask 3 things first: Name / Phone / PAN | Ask three things first. Name, phone, PAN. | पहले सिर्फ़ तीन चीज़ें पूछो। नाम, फ़ोन, PAN। |
| 4 | Offer first. **Documents after.** | Show the offer. Then ask for documents. | पहले ऑफ़र दिखाओ। फिर डॉक्यूमेंट माँगो। |
| 5 | Save now. **Finish later.** | Let them save, and come back later. | सेव करके, बाद में लौटने दो। |
| 6 | Comment **KYC** · Free 20-minute call on your sign-up flow · @official_softnear | We design fintech sign-ups people finish. Comment KYC. | हम ऐसे फ़िनटेक साइन-अप डिज़ाइन करते हैं, जो लोग पूरा करते हैं। कमेंट करो, KYC। |

## Files

- `reel.mp4`: silent cut, 3 s per frame (what is attached in PostDesk until the voiced file replaces it).
- Voiceover: ElevenLabs v4 "christopher" via Bloom (brand Softnear), one clip per frame, generated 2026-11-13. Media IDs in `source/timing.json`. The weekly job could not download them (the Bloom asset host is blocked from the cloud run), so the voiced files are not built yet.
- `source/build_vo.py`: builds the voiced reel from the frames + clips, cards timed to each clip.

## Build the voiced versions (team, ~1 minute)

```bash
# download the 6 Hindi and 6 English clips from Bloom (Softnear brand > Audio) as vo/hi/01.mp3..06.mp3 and vo/en/01.mp3..06.mp3
cd 2026-11/week-11-16/ig-wed-reel-kyc/source
python3 build_vo.py hi vo/hi ../reel-hi.mp4    # ~31 s, for Instagram (Wed) and Facebook
python3 build_vo.py en vo/en ../reel-en.mp4    # ~27 s, for LinkedIn in a later free slot
```
Then replace the media on PostDesk post (IG Wed) with `reel-hi.mp4`. Brand rule: never publish the silent cut.
