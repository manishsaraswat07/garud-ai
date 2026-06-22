# engine.py - Garud AI v3 Detection Engine (Bug-Fixed)
# Modules: Scam, Fake News, Toxic/Hate Speech, Financial Fraud, Misinformation, Overall Risk
#
# FIXES APPLIED:
#   1. Overall score now uses MAX(modules) blended with weighted-average,
#      so one strong signal (e.g. Scam=83%) is no longer diluted to a low score.
#   2. Keyword matching now uses word-boundary regex instead of plain substring
#      search, preventing false positives (e.g. "fees" no longer matches inside "coffees").
#   3. Multiple distinct keyword hits within the same category now add partial
#      extra weight (escalation), instead of every category capping at one hit.

import re

# ─────────────────────────────────────────────
# MODULE 1: SCAM DETECTION
# ─────────────────────────────────────────────
SCAM_SIGNALS = {
    "Urgency Language": {
        "keywords": ["immediately", "urgent", "act now", "expires today", "limited time",
                     "hurry", "asap", "within 24 hours", "suspended", "blocked",
                     "deadline", "last chance", "final notice", "right now"],
        "weight": 25,
        "icon": "clock"
    },
    "Financial Request": {
        "keywords": ["bank account", "credit card number", "send money", "wire transfer",
                     "payment required", "processing fees", "pay in bitcoin", "pay in crypto",
                     "send a gift card", "upi payment", "pay now", "complete the transaction",
                     "digital wallet"],
        "weight": 30,
        "icon": "dollar"
    },
    "Suspicious Link": {
        "keywords": ["click here", "click the link", "bit.ly", "tinyurl", "http://",
                     "login now", "verify here", "access now", "follow this link", "tap here"],
        "weight": 20,
        "icon": "link"
    },
    "Account Verification": {
        "keywords": ["verify your account", "confirm your identity", "update your details",
                     "account verification", "re-enter your password", "provide your otp",
                     "enter your pin", "kyc", "account suspended", "confirm your email"],
        "weight": 25,
        "icon": "lock"
    },
    "Prize / Lottery": {
        "keywords": ["you have won", "congratulations you", "you are the winner", "won a prize",
                     "lottery", "lucky draw", "claim your reward", "claim your prize",
                     "free gift", "you are chosen", "lucky winner", "jackpot", "sweepstakes"],
        "weight": 20,
        "icon": "gift"
    },
}

# ─────────────────────────────────────────────
# MODULE 2: FAKE NEWS DETECTION
# ─────────────────────────────────────────────
FAKE_NEWS_SIGNALS = {
    "Sensational Headline": {
        "keywords": ["shocking", "you won't believe", "mind blowing", "unbelievable",
                     "exclusive", "breaking", "bombshell", "jaw dropping", "stunning revelation",
                     "they don't want you to know", "secret revealed"],
        "weight": 25,
        "icon": "newspaper"
    },
    "Unverified Source": {
        "keywords": ["anonymous source", "sources say", "rumor has it", "reportedly true",
                     "insiders claim", "leaked documents", "unnamed official",
                     "according to some reports", "many people are saying"],
        "weight": 20,
        "icon": "eye"
    },
    "Conspiracy Language": {
        "keywords": ["deep state", "cover up", "they are hiding", "mainstream media lies",
                     "government conspiracy", "hidden agenda", "new world order",
                     "illuminati", "false flag", "wake up sheeple", "plandemic"],
        "weight": 30,
        "icon": "spiral"
    },
    "Emotional Manipulation": {
        "keywords": ["outrage", "share before deleted", "spread the word", "wake up",
                     "open your eyes", "they will silence", "before it's too late",
                     "share now", "forward this", "must read"],
        "weight": 25,
        "icon": "megaphone"
    },
}

# ─────────────────────────────────────────────
# MODULE 3: TOXIC / HATE SPEECH DETECTION
# ─────────────────────────────────────────────
TOXIC_SIGNALS = {
    "Personal Attack": {
        "keywords": ["idiot", "stupid", "moron", "loser", "worthless", "pathetic",
                     "dumb", "you are trash", "garbage person", "you suck",
                     "you're nothing", "go die", "kill yourself"],
        "weight": 35,
        "icon": "sword"
    },
    "Discriminatory Language": {
        "keywords": ["hate all", "they are all", "those people", "inferior race",
                     "should be banned", "don't belong here", "go back to",
                     "not one of us", "subhuman"],
        "weight": 40,
        "icon": "ban"
    },
    "Threat Language": {
        "keywords": ["i will hurt", "you will pay", "watch your back", "come after you",
                     "make you regret", "destroy you", "end you", "you'll be sorry"],
        "weight": 40,
        "icon": "alert-triangle"
    },
    "Profanity / Slur": {
        "keywords": ["f***", "b****", "a**hole", "shut up", "bastard",
                     "screw you", "go to hell"],
        "weight": 20,
        "icon": "alert-triangle"
    },
}

# ─────────────────────────────────────────────
# MODULE 4: FINANCIAL FRAUD DETECTION
# ─────────────────────────────────────────────
FRAUD_SIGNALS = {
    "Ponzi / Pyramid Scheme": {
        "keywords": ["guaranteed returns", "double your money", "get rich quick",
                     "invest now", "100% profit", "risk free investment",
                     "passive income", "recruit others", "multi level", "mlm",
                     "unlimited earning", "financial freedom fast"],
        "weight": 35,
        "icon": "trending-up"
    },
    "Fake Investment": {
        "keywords": ["offshore account", "secret trading", "insider tip", "sure shot",
                     "high yield", "no risk", "guaranteed profit", "forex signals",
                     "crypto pump", "ten x returns", "returns guaranteed"],
        "weight": 30,
        "icon": "bar-chart"
    },
    "Identity Theft Attempt": {
        "keywords": ["social security", "aadhaar number", "pan card", "bank details",
                     "account number", "routing number", "confirm your ssn",
                     "share your card", "cvv", "date of birth required"],
        "weight": 35,
        "icon": "id-card"
    },
    "Advance Fee Fraud": {
        "keywords": ["processing fee", "release fee", "small fee to unlock",
                     "pay to receive", "advance payment", "refundable deposit",
                     "unlock your funds", "transfer fee", "handling charge"],
        "weight": 30,
        "icon": "coins"
    },
}

# ─────────────────────────────────────────────
# MODULE 5: MISINFORMATION DETECTION
# ─────────────────────────────────────────────
MISINFO_SIGNALS = {
    "Health Misinformation": {
        "keywords": ["doctors don't want you to know", "cure for cancer", "miracle cure",
                     "vaccine causes", "5g causes", "detox your body",
                     "big pharma hiding", "natural cure banned", "cures covid",
                     "alkaline water cures", "bleach cure"],
        "weight": 35,
        "icon": "activity"
    },
    "Scientific Denial": {
        "keywords": ["climate change is fake", "evolution is a lie", "flat earth",
                     "moon landing fake", "earth is flat", "scientists are lying",
                     "global warming hoax", "vaccines are poison"],
        "weight": 30,
        "icon": "flask"
    },
    "False Statistics": {
        "keywords": ["studies show 100%", "proven by science", "experts agree completely",
                     "statistics prove", "research shows always", "100% effective",
                     "zero side effects", "clinically proven to cure"],
        "weight": 20,
        "icon": "bar-chart"
    },
    "Fabricated Events": {
        "keywords": ["did not happen", "staged attack", "crisis actor", "false flag event",
                     "fake shooting", "government staged", "hoax attack", "scripted event"],
        "weight": 35,
        "icon": "theater-masks"
    },
}


# ─────────────────────────────────────────────
# SCORING ENGINE
# ─────────────────────────────────────────────

def _build_pattern(keyword: str) -> re.Pattern:
    """
    Build a word-boundary regex for a keyword/phrase so it only matches
    whole words — prevents 'fees' from matching inside 'coffees', etc.
    Multi-word phrases (e.g. "click here") still match as a phrase.
    """
    escaped = re.escape(keyword)
    return re.compile(r"(?<!\w)" + escaped + r"(?!\w)", re.IGNORECASE)


def _score_module(text_lower: str, signals: dict) -> tuple[int, list[dict]]:
    """
    Generic scorer for any signal module. Returns (score 0-100, detected list).

    Fix: uses word-boundary matching (no substring false positives) and gives
    a small escalation bonus when a category has multiple distinct keyword hits,
    so a message hammering one theme repeatedly scores higher than a single
    incidental mention.
    """
    detected = []
    total_weight = 0
    max_possible = sum(s["weight"] for s in signals.values())

    for name, config in signals.items():
        hits = 0
        for kw in config["keywords"]:
            if _build_pattern(kw).search(text_lower):
                hits += 1

        if hits > 0:
            detected.append({"name": name, "icon": config["icon"]})
            # Base weight for the category, plus escalation bonus for multiple
            # distinct hits (+25% of weight per extra hit, capped at +100%,
            # i.e. 2 hits = 1.25x, 3 hits = 1.5x, 5+ hits = 2x weight).
            bonus_multiplier = 1 + min(hits - 1, 4) * 0.25
            total_weight += config["weight"] * bonus_multiplier

    score = min(int(round((total_weight / max_possible) * 100)), 100) if max_possible else 0

    # Severity floor: if any single category racked up 3+ distinct keyword
    # hits, that's strong, unambiguous evidence — don't let the module's
    # overall weight ratio undersell it. Push the score to at least 65.
    max_hits_in_one_category = 0
    for name, config in signals.items():
        hits = sum(1 for kw in config["keywords"] if _build_pattern(kw).search(text_lower))
        max_hits_in_one_category = max(max_hits_in_one_category, hits)
    if max_hits_in_one_category >= 3:
        score = max(score, 65)

    return score, detected


def _risk_level(score: int) -> tuple[str, str]:
    """Return (level label, color hex) for a score."""
    if score >= 60:
        return "High", "#ff4b4b"
    elif score >= 30:
        return "Medium", "#f0a500"
    else:
        return "Low", "#00c48c"


# Safety tips per module
MODULE_TIPS = {
    "scam": [
        "Never share OTPs, PINs, or passwords with anyone.",
        "Verify suspicious messages directly via official websites or helplines.",
        "Legitimate organizations never demand instant action.",
    ],
    "fake_news": [
        "Cross-check news with at least two reputable sources.",
        "Look for the original source — not just a forwarded screenshot.",
        "Check the date; old news is often recirculated as new.",
    ],
    "toxic": [
        "This message may violate platform community guidelines.",
        "Avoid engaging — report and block the sender.",
        "Online harassment is a punishable offence in many jurisdictions.",
    ],
    "fraud": [
        "No legitimate investment guarantees returns — it's always a red flag.",
        "Never share your Aadhaar, PAN, bank or card details over chat.",
        "Report financial fraud immediately to your bank and cybercrime.gov.in.",
    ],
    "misinfo": [
        "Always verify health claims with licensed medical professionals.",
        "Scientific consensus is built over years — be wary of 'breakthroughs'.",
        "Use fact-checking sites like AltNews, Snopes, or FactCheck.org.",
    ],
}


def analyze(text: str) -> dict:
    """
    Full Garud AI analysis. Returns all module scores + overall risk.
    """
    t = text.lower()

    scam_score, scam_signals       = _score_module(t, SCAM_SIGNALS)
    news_score, news_signals       = _score_module(t, FAKE_NEWS_SIGNALS)
    toxic_score, toxic_signals     = _score_module(t, TOXIC_SIGNALS)
    fraud_score, fraud_signals     = _score_module(t, FRAUD_SIGNALS)
    misinfo_score, misinfo_signals = _score_module(t, MISINFO_SIGNALS)

    # ── FIX: Overall risk now mirrors the single strongest module's score
    # directly (so "Scam=83%" always shows "Overall=83%-ish", never diluted
    # down to a misleadingly low number), then adds a small bonus if multiple
    # modules fire at once (a multi-threat message is genuinely more risky
    # than a single-category one).
    module_scores = {
        "scam": scam_score, "fraud": fraud_score, "toxic": toxic_score,
        "fake_news": news_score, "misinfo": misinfo_score,
    }
    strongest = max(module_scores.values())

    # Count how many modules are meaningfully active (score >= 30)
    active_modules = sum(1 for s in module_scores.values() if s >= 30)
    multi_signal_bonus = max(0, active_modules - 1) * 6  # +6 per extra active module

    overall = min(int(round(strongest + multi_signal_bonus)), 100)

    # Collect active tips
    tips = []
    if scam_score   >= 30: tips.extend(MODULE_TIPS["scam"])
    if news_score   >= 30: tips.extend(MODULE_TIPS["fake_news"])
    if toxic_score  >= 30: tips.extend(MODULE_TIPS["toxic"])
    if fraud_score  >= 30: tips.extend(MODULE_TIPS["fraud"])
    if misinfo_score >= 30: tips.extend(MODULE_TIPS["misinfo"])
    if not tips:
        tips = ["This message appears safe. Stay alert and trust your instincts."]

    return {
        "overall":        {"score": overall,       **dict(zip(["level","color"], _risk_level(overall)))},
        "scam":           {"score": scam_score,     **dict(zip(["level","color"], _risk_level(scam_score))),    "signals": scam_signals},
        "fake_news":      {"score": news_score,     **dict(zip(["level","color"], _risk_level(news_score))),    "signals": news_signals},
        "toxic":          {"score": toxic_score,    **dict(zip(["level","color"], _risk_level(toxic_score))),   "signals": toxic_signals},
        "fraud":          {"score": fraud_score,    **dict(zip(["level","color"], _risk_level(fraud_score))),   "signals": fraud_signals},
        "misinfo":        {"score": misinfo_score,  **dict(zip(["level","color"], _risk_level(misinfo_score))), "signals": misinfo_signals},
        "tips":           tips,
    }
