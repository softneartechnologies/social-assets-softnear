"""Scene content for the Rs 5,000 vs Rs 25,000 website reel (Hindi).

Each scene: list of states. State k reveals every element tagged r{k}.
`split` = fraction of the voice line at which state 1 appears (state 0 at 0).
"""

PROG = ["डिज़ाइन", "डोमेन", "स्पीड", "गूगल", "लीड्स"]


def compare(n, slug, topic, title, bad, good, split):
    return {
        "id": f"0{n+2}-{slug}",
        "kind": "compare",
        "n": n,
        "eyebrow": f"फ़र्क {n}/5 · {topic}",
        "title": title,
        "bad": bad,
        "good": good,
        "split": split,
    }


SCENES = [
    {
        "id": "01-hook", "kind": "hook",
        "eyebrow": "वेबसाइट बनवाने से पहले",
        "title": "₹5,000 की वेबसाइट<br>==सबसे महंगी==<br>पड़ती है",
        "sub": "कैसे? 5 फ़र्क देखिए",
        "split": 0.45,
    },
    {
        "id": "02-setup", "kind": "setup",
        "eyebrow": "₹5,000 vs ₹25,000",
        "title_a": "दिखने में ==एक जैसी==",
        "title_b": "पर अंदर ==5 बड़े फ़र्क==",
        "split": 0.62,
    },
    compare(1, "design", "डिज़ाइन", "हज़ारों जैसी या<br>==सिर्फ़ आपकी==?",
            "वही टेम्पलेट, जो हज़ारों साइट्स पर लगा है",
            "आपके बिज़नेस के लिए कस्टम डिज़ाइन", 0.52),
    compare(2, "domain", "डोमेन", "डोमेन ==किसके नाम==<br>पर है?",
            "कई बार डेवलपर के नाम पर",
            "आपके नाम पर, कंट्रोल आपका", 0.55),
    compare(3, "speed", "स्पीड", "साइट खुलती है या<br>==घूमती रहती है==?",
            "सस्ती होस्टिंग, स्लो साइट, ग्राहक गायब",
            "फ़ास्ट होस्टिंग, पेज झट से खुले", 0.5),
    compare(4, "google", "गूगल", "गूगल पर<br>==आप दिखते हैं==?",
            "SEO नहीं, गूगल को पता ही नहीं कि आप हैं",
            "SEO सेटअप: ग्राहक ढूंढे, तो आप दिखें", 0.6),
    compare(5, "leads", "लीड्स", "ब्रोशर या<br>==लीड मशीन==?",
            "सिर्फ़ एक ऑनलाइन ब्रोशर",
            "WhatsApp बटन + इंक्वायरी फ़ॉर्म = असली लीड्स", 0.45),
    {
        "id": "08-invest", "kind": "invest",
        "eyebrow": "असली हिसाब",
        "split": 0.36,
        "split2": 0.68,
    },
    {
        "id": "09-cta", "kind": "cta",
        "eyebrow": "प्राइस मत देखिए",
        "title": "ये ==5 सवाल== पूछिए",
        "qs": ["डिज़ाइन कस्टम है?", "डोमेन मेरे नाम पर है?", "साइट तेज़ खुलती है?",
               "SEO सेटअप है?", "WhatsApp और फ़ॉर्म हैं?"],
        "split": 0.42,
    },
]
