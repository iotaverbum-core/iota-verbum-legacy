from __future__ import annotations

DISTORTION_LEXICON = {
    "fear": {
        "panic": 1.0,
        "afraid": 0.9,
        "anxious": 0.8,
        "scared": 0.9,
        "worried": 0.6,
        "threat": 0.8,
    },
    "control": {
        "must": 0.9,
        "force": 1.0,
        "manage": 0.6,
        "fix": 0.7,
        "perfect": 0.8,
        "secure": 0.8,
    },
    "pride": {
        "better": 0.7,
        "above": 0.6,
        "deserve": 0.8,
        "prove": 0.8,
        "image": 0.7,
        "special": 0.6,
    },
    "withdrawal": {
        "numb": 0.9,
        "avoid": 0.8,
        "retreat": 0.8,
        "hide": 0.7,
        "shutdown": 1.0,
        "isolated": 0.8,
    },
    "shame": {
        "worthless": 1.0,
        "disgusting": 1.0,
        "failure": 0.8,
        "ashamed": 1.0,
        "dirty": 0.9,
        "condemned": 0.8,
    },
}

UNION_MARKERS = {
    "christ": 1.0,
    "jesus": 1.0,
    "lord": 0.9,
    "cross": 0.8,
    "grace": 0.8,
    "mercy": 0.7,
    "beloved": 0.7,
    "abide": 0.8,
}

VELOCITY_MARKERS = {
    "now": 0.6,
    "immediately": 1.0,
    "urgent": 1.0,
    "tonight": 0.7,
    "quick": 0.6,
    "asap": 1.0,
    "right": 0.4,
    "today": 0.5,
}

DESPAIR_MARKERS = {"hopeless", "no way out", "give up", "end it", "nothing matters"}
