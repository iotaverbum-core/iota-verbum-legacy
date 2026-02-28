import hashlib
import json
import re
from pathlib import Path


VERB_LEXICON = {
    "am",
    "are",
    "is",
    "was",
    "were",
    "be",
    "become",
    "became",
    "been",
    "being",
    "have",
    "has",
    "had",
    "hath",
    "do",
    "doth",
    "did",
    "say",
    "said",
    "saith",
    "spake",
    "speak",
    "answered",
    "cried",
    "come",
    "came",
    "cometh",
    "go",
    "went",
    "make",
    "made",
    "dwell",
    "dwelt",
    "behold",
    "beheld",
    "see",
    "seen",
    "saw",
    "bear",
    "bore",
    "take",
    "took",
    "give",
    "gave",
    "stand",
    "stood",
    "sit",
    "sat",
    "rise",
    "rose",
    "walk",
    "walked",
    "enter",
    "entered",
    "leave",
    "left",
    "remain",
    "abide",
    "keep",
    "kept",
    "know",
    "knew",
    "love",
    "loved",
    "feel",
    "felt",
    "show",
    "showed",
    "try",
    "tried",
    "bring",
    "brought",
    "send",
    "sent",
    "looked",
    "heard",
    "followed",
    "turn",
    "turned",
    "staying",
    "stayed",
    "standing",
}

VERB_STOPLIST = {
    "tired",
    "red",
    "bed",
    "led",
    "naked",
    "wicked",
    "beloved",
}

SPEECH_INTRODUCERS = {"say", "said", "saith", "spake", "answered", "cried"}

IRREGULAR_LEMMA = {
    "became": "become",
    "was": "be",
    "were": "be",
    "been": "be",
    "am": "be",
    "is": "be",
    "are": "be",
    "hath": "have",
    "has": "have",
    "had": "have",
    "did": "do",
    "doth": "do",
    "said": "say",
    "saith": "say",
    "spake": "speak",
    "came": "come",
    "cometh": "come",
    "went": "go",
    "made": "make",
    "dwelt": "dwell",
    "beheld": "behold",
    "seen": "see",
    "saw": "see",
    "took": "take",
    "gave": "give",
    "stood": "stand",
    "sat": "sit",
    "rose": "rise",
    "kept": "keep",
    "knew": "know",
    "felt": "feel",
    "showed": "show",
    "tried": "try",
    "brought": "bring",
    "sent": "send",
}

PAST_TENSE = {
    "became",
    "was",
    "were",
    "had",
    "did",
    "said",
    "spake",
    "came",
    "went",
    "made",
    "dwelt",
    "beheld",
    "seen",
    "saw",
    "took",
    "gave",
    "stood",
    "sat",
    "rose",
    "kept",
    "knew",
    "felt",
    "showed",
    "tried",
    "brought",
    "sent",
}

TIME_MARKER_PATTERNS = [
    ("the next day", "sequence"),
    ("after these things", "sequence"),
    ("in those days", "anchor"),
    ("at that time", "anchor"),
    ("when", "simultaneity"),
    ("while", "simultaneity"),
    ("before", "sequence"),
    ("after", "sequence"),
    ("now", "anchor"),
    ("then", "sequence"),
    ("and it came to pass", "anchor"),
    ("behold", "anchor"),
]

TURN_WORDS = {
    "but": "contrast",
    "yet": "contrast",
    "nevertheless": "contrast",
    "therefore": "resolution",
    "so": "resolution",
}

REORIENTATION_PHRASES = {
    "and behold": "disclosure",
    "behold": "disclosure",
    "after these things": "reframe",
    "from that time": "reframe",
}

ABBREVIATIONS = {"mr", "mrs", "ms", "dr", "vs", "jr", "sr", "st", "prof", "rev"}

PRONOUNS = {
    "he": ("M", "S"),
    "him": ("M", "S"),
    "his": ("M", "S"),
    "she": ("F", "S"),
    "her": ("F", "S"),
    "hers": ("F", "S"),
    "they": ("P", "P"),
    "them": ("P", "P"),
    "their": ("P", "P"),
    "we": ("P", "P"),
    "us": ("P", "P"),
    "i": ("N", "S"),
    "me": ("N", "S"),
    "my": ("N", "S"),
    "you": ("N", "S"),
    "your": ("N", "S"),
    "it": ("N", "S"),
    "its": ("N", "S"),
}

ATTRIBUTION_VERBS = {
    "said",
    "asked",
    "replied",
    "answered",
    "declared",
    "proclaimed",
    "spoke",
    "told",
    "cried",
    "shouted",
    "whispered",
    "continued",
    "began",
    "responded",
    "testified",
    "commanded",
    "warned",
    "promised",
}

WH_WORDS = {"what", "where", "who", "why", "when", "how", "which", "whom", "whose"}

INVITATION_VERBS = {"come", "follow", "see", "look", "listen", "hear", "stay", "abide"}

IMPERATIVE_VERBS = {
    "give",
    "go",
    "come",
    "follow",
    "see",
    "look",
    "listen",
    "hear",
    "stay",
    "abide",
    "tell",
    "take",
    "drink",
    "ask",
    "seek",
}

COMMAND_INDICATORS = {"now", "immediately", "must", "shall"}

VOCATIVE_TITLES = {"rabbi", "lord", "teacher", "father"}


def resolve_repo_path(p: str) -> Path:
    path = Path(p)
    if path.is_absolute():
        return path
    repo_root = Path(__file__).resolve().parent
    return repo_root / path


def _to_repo_relative(path: Path) -> str:
    repo_root = Path(__file__).resolve().parent
    try:
        return str(path.relative_to(repo_root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_text(text: str) -> str:
    text = text.lstrip("\ufeff")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = (
        text.replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
        .replace("—", "—")
        .replace("–", "–")
    )
    paragraphs = re.split(r"\n\s*\n", text.strip())
    normalized_paragraphs = []
    for para in paragraphs:
        cleaned = " ".join(para.split())
        normalized_paragraphs.append(cleaned)
    return "\n\n".join(normalized_paragraphs).strip()


def normalize_passage_ref(ref: str) -> str:
    raw = (ref or "").strip()
    raw = raw.replace(".", ":")
    raw = " ".join(raw.split())
    if not raw:
        raise ValueError("passage reference is empty")
    tokens = raw.split()
    if len(tokens) < 2:
        raise ValueError(f"passage reference missing chapter/verse: {ref}")
    if tokens[0].isdigit() and len(tokens) >= 3:
        book_raw = f"{tokens[0]} {tokens[1]}"
        rest = " ".join(tokens[2:])
    else:
        book_raw = tokens[0]
        rest = " ".join(tokens[1:])

    def keyize(value: str) -> str:
        return re.sub(r"[^a-z0-9]", "", value.lower())

    book_key = keyize(book_raw)
    book_map = {
        "john": "John",
        "jn": "John",
        "jhn": "John",
        "1corinthians": "1 Corinthians",
        "1cor": "1 Corinthians",
        "1co": "1 Corinthians",
        "2corinthians": "2 Corinthians",
        "2cor": "2 Corinthians",
        "2co": "2 Corinthians",
        "psalm": "Psalm",
        "psalms": "Psalm",
        "ps": "Psalm",
        "psa": "Psalm",
        "genesis": "Genesis",
        "gen": "Genesis",
        "exodus": "Exodus",
        "exo": "Exodus",
    }
    book = book_map.get(book_key)
    if not book:
        book = book_raw.title()
    return f"{book} {rest}"


def _iter_tokens_with_spans(text: str):
    for match in re.finditer(r"[A-Za-z']+", text):
        yield match.group(0), match.start(), match.end()


def split_sentences(text: str):
    spans = []
    start = 0
    i = 0
    length = len(text)
    while i < length:
        ch = text[i]
        if ch == "\n":
            end = i
            if end > start:
                spans.append((start, end))
            i += 1
            while i < length and text[i].isspace():
                i += 1
            start = i
            continue
        if ch in ".!?":
            last_word_match = re.search(r"[A-Za-z']+$", text[:i])
            last_word = last_word_match.group(0).lower() if last_word_match else ""
            if ch == "." and last_word in ABBREVIATIONS:
                i += 1
                continue
            end = i + 1
            if end > start:
                spans.append((start, end))
            i = end
            while i < length and text[i].isspace():
                i += 1
            start = i
            continue
        i += 1
    if start < length:
        spans.append((start, length))
    return spans


def split_clauses(sentence_text: str):
    breaks = []
    for delim in [";", ":", "—", "–"]:
        for match in re.finditer(re.escape(delim), sentence_text):
            breaks.append(
                {
                    "index": match.start(),
                    "next_start": match.start() + 1,
                    "reason": delim,
                }
            )
    for conj in [" and ", " but ", " yet "]:
        for match in re.finditer(re.escape(conj), sentence_text):
            idx = match.start()
            breaks.append({"index": idx, "next_start": idx + 1, "reason": conj.strip()})
    breaks = sorted(breaks, key=lambda b: (b["index"], b["reason"]))

    clauses = []
    boundaries = []
    cursor = 0
    for br in breaks:
        if br["index"] <= cursor:
            continue
        end = br["index"]
        clauses.append((cursor, end))
        boundaries.append({"boundary": br["index"], "reason": br["reason"]})
        cursor = br["next_start"]
    if cursor < len(sentence_text):
        clauses.append((cursor, len(sentence_text)))
    return clauses, boundaries


def build_segments(text: str):
    segments = []
    boundaries = []
    sentence_spans = split_sentences(text)
    for sentence_id, (s_start, s_end) in enumerate(sentence_spans):
        sentence_text = text[s_start:s_end]
        clause_spans, clause_boundaries = split_clauses(sentence_text)
        for clause_index, (c_start, c_end) in enumerate(clause_spans):
            abs_start = s_start + c_start
            abs_end = s_start + c_end
            while abs_start < abs_end and text[abs_start].isspace():
                abs_start += 1
            while abs_end > abs_start and text[abs_end - 1].isspace():
                abs_end -= 1
            clause_id = f"s{sentence_id}.c{clause_index}"
            segments.append(
                {
                    "sentence_id": sentence_id,
                    "clause_id": clause_id,
                    "text": text[abs_start:abs_end],
                    "token_start": abs_start,
                    "token_end": abs_end,
                }
            )
        for boundary in clause_boundaries:
            boundaries.append(
                {
                    "sentence_id": sentence_id,
                    "boundary": s_start + boundary["boundary"],
                    "reason": boundary["reason"],
                }
            )
    return segments, boundaries, sentence_spans


def _lemma_guess(token: str):
    lower = token.lower()
    if lower in IRREGULAR_LEMMA:
        return IRREGULAR_LEMMA[lower]
    if lower.endswith("eth"):
        return lower[:-3]
    if lower.endswith("est"):
        return lower[:-3]
    if lower.endswith("ing") and len(lower) > 4:
        base = lower[:-3]
        if base.endswith("k"):
            return base + "e"
        return base
    if lower.endswith("ed") and len(lower) > 3:
        if lower.endswith("ied"):
            return lower[:-3] + "y"
        return lower[:-2]
    return lower


def _tense_guess(token: str):
    lower = token.lower()
    if lower in PAST_TENSE or lower.endswith("ed"):
        return "past"
    if lower.endswith("ing"):
        return "present"
    if lower.endswith("eth") or lower.endswith("est"):
        return "present"
    if lower in {"am", "is", "are", "do", "doth", "hath"}:
        return "present"
    return "unknown"


def extract_verbs(text: str, segments):
    verb_instances = []
    segment_iter = iter(sorted(segments, key=lambda s: s["token_start"]))
    current_segment = next(segment_iter, None)

    for token, start, end in _iter_tokens_with_spans(text):
        lower = token.lower()
        while current_segment and start >= current_segment["token_end"]:
            current_segment = next(segment_iter, None)
        if not current_segment or start < current_segment["token_start"]:
            continue

        is_verb = False
        if lower in VERB_LEXICON:
            is_verb = True
        elif lower.endswith(("ed", "ing", "eth", "est")) and lower not in VERB_STOPLIST:
            is_verb = True

        if not is_verb:
            continue

        lemma = _lemma_guess(token)
        verb_instances.append(
            {
                "verb_text": token,
                "lemma_guess": lemma,
                "tense_guess": _tense_guess(token),
                "role": "speech_introducer" if lemma in SPEECH_INTRODUCERS else "action",
                "token_span": [start, end],
                "clause_id": current_segment["clause_id"],
            }
        )

    verb_instances.sort(
        key=lambda v: (v["clause_id"], v["token_span"][0], v["verb_text"].lower())
    )
    return verb_instances


def extract_time_markers(text: str, segments):
    markers = []
    segment_map = {seg["clause_id"]: seg for seg in segments}
    for phrase, kind in TIME_MARKER_PATTERNS:
        for match in re.finditer(rf"\b{re.escape(phrase)}\b", text, flags=re.IGNORECASE):
            start, end = match.start(), match.end()
            clause_id = None
            sentence_id = None
            for seg in segments:
                if seg["token_start"] <= start < seg["token_end"]:
                    clause_id = seg["clause_id"]
                    sentence_id = seg["sentence_id"]
                    break
            markers.append(
                {
                    "text": text[start:end],
                    "type": kind,
                    "scope": "clause" if clause_id else "sentence",
                    "clause_id": clause_id,
                    "sentence_id": sentence_id,
                    "token_span": [start, end],
                }
            )

    markers.sort(key=lambda m: m["token_span"][0])
    return markers


def _evidence_window(text: str, index: int, window: int = 60):
    start = max(0, index - window)
    end = min(len(text), index + window)
    before = text[start:index].strip()
    after = text[index:end].strip()
    return before, after


def extract_thresholds(text: str, segments, boundaries):
    thresholds = []

    for idx, seg in enumerate(segments):
        clause_text = seg["text"].strip()
        lower = clause_text.lower()
        match = re.match(r"^(and\s+)?(but|yet|nevertheless|therefore|so)\b", lower)
        if match:
            trigger = match.group(2)
            kind = TURN_WORDS.get(trigger, "contrast")
            before, after = _evidence_window(text, seg["token_start"])
            thresholds.append(
                {
                    "kind": kind,
                    "trigger": trigger,
                    "from_clause_id": segments[idx - 1]["clause_id"] if idx > 0 else None,
                    "to_clause_id": seg["clause_id"],
                    "evidence_before": before,
                    "evidence_after": after,
                    "token_span": [seg["token_start"], seg["token_start"] + len(trigger)],
                }
            )

        for phrase, kind in REORIENTATION_PHRASES.items():
            if lower.startswith(phrase):
                before, after = _evidence_window(text, seg["token_start"])
                thresholds.append(
                    {
                        "kind": kind,
                        "trigger": phrase,
                        "from_clause_id": segments[idx - 1]["clause_id"] if idx > 0 else None,
                        "to_clause_id": seg["clause_id"],
                        "evidence_before": before,
                        "evidence_after": after,
                        "token_span": [seg["token_start"], seg["token_start"] + len(phrase)],
                    }
                )

        and_pronoun = re.match(r"^and\s+(we|he|she|they)\b", lower)
        if and_pronoun:
            before, after = _evidence_window(text, seg["token_start"])
            trigger = f"and {and_pronoun.group(1)}"
            thresholds.append(
                {
                    "kind": "disclosure",
                    "trigger": trigger,
                    "from_clause_id": segments[idx - 1]["clause_id"] if idx > 0 else None,
                    "to_clause_id": seg["clause_id"],
                    "evidence_before": before,
                    "evidence_after": after,
                    "token_span": [seg["token_start"], seg["token_start"] + len(trigger)],
                }
            )

        if "full of" in lower:
            offset = lower.index("full of")
            before, after = _evidence_window(text, seg["token_start"] + offset)
            thresholds.append(
                {
                    "kind": "escalation",
                    "trigger": "full of",
                    "from_clause_id": segments[idx - 1]["clause_id"] if idx > 0 else None,
                    "to_clause_id": seg["clause_id"],
                    "evidence_before": before,
                    "evidence_after": after,
                    "token_span": [
                        seg["token_start"] + offset,
                        seg["token_start"] + offset + len("full of"),
                    ],
                }
            )

    for boundary in boundaries:
        reason = boundary["reason"]
        if reason in {":", ";", "?", "?"}:
            before, after = _evidence_window(text, boundary["boundary"])
            thresholds.append(
                {
                    "kind": "reframe",
                    "trigger": reason,
                    "from_clause_id": None,
                    "to_clause_id": None,
                    "evidence_before": before,
                    "evidence_after": after,
                    "token_span": [boundary["boundary"], boundary["boundary"] + 1],
                }
            )

    for idx in range(1, len(segments)):
        prev = segments[idx - 1]["text"]
        curr = segments[idx]["text"]
        prev_pronouns = sum(1 for t, _, _ in _iter_tokens_with_spans(prev) if t.lower() in PRONOUNS)
        prev_proper = re.search(r"\b[A-Z][a-z]+\b", prev)
        curr_proper = re.search(r"\b[A-Z][a-z]+\b", curr)
        if prev_pronouns >= 2 and not prev_proper and curr_proper:
            before, after = _evidence_window(text, segments[idx]["token_start"])
            thresholds.append(
                {
                    "kind": "disclosure",
                    "trigger": "subject_shift",
                    "from_clause_id": segments[idx - 1]["clause_id"],
                    "to_clause_id": segments[idx]["clause_id"],
                    "evidence_before": before,
                    "evidence_after": after,
                    "token_span": [
                        segments[idx]["token_start"],
                        segments[idx]["token_start"] + len("subject_shift"),
                    ],
                }
            )

    quote_flags = [('"'
                   in seg["text"]) for seg in segments]
    for idx in range(1, len(segments)):
        if quote_flags[idx] != quote_flags[idx - 1]:
            before, after = _evidence_window(text, segments[idx]["token_start"])
            thresholds.append(
                {
                    "kind": "interruption",
                    "trigger": "quote_boundary",
                    "from_clause_id": segments[idx - 1]["clause_id"],
                    "to_clause_id": segments[idx]["clause_id"],
                    "evidence_before": before,
                    "evidence_after": after,
                    "token_span": [
                        segments[idx]["token_start"],
                        segments[idx]["token_start"] + len("quote_boundary"),
                    ],
                }
            )

    thresholds.sort(
        key=lambda t: (t["token_span"][0], t["kind"], t["trigger"])
    )
    return thresholds


def extract_silences(text: str, segments, verbs, focus_nouns):
    silences = []
    verbs_by_clause = {}
    for verb in verbs:
        verbs_by_clause.setdefault(verb["clause_id"], []).append(verb)

    sentence_and_counts = {}
    for seg in segments:
        sentence_id = seg["sentence_id"]
        sentence_and_counts.setdefault(sentence_id, 0)
        sentence_and_counts[sentence_id] += sum(
            1 for t, _, _ in _iter_tokens_with_spans(seg["text"]) if t.lower() == "and"
        )

    for seg in segments:
        clause_id = seg["clause_id"]
        clause_text = seg["text"]
        lower = clause_text.lower()
        clause_verbs = verbs_by_clause.get(clause_id, [])
        token_count = sum(1 for _ in _iter_tokens_with_spans(clause_text))

        if "—" in clause_text or "–" in clause_text:
            silences.append(
                {
                    "silence_type": "interruption",
                    "clause_id": clause_id,
                    "signal": "em_dash",
                    "note_seed": "speech interrupted or cut",
                    "token_pos": seg["token_start"],
                }
            )

        if sentence_and_counts.get(seg["sentence_id"], 0) >= 3:
            silences.append(
                {
                    "silence_type": "compression",
                    "clause_id": clause_id,
                    "signal": f"and_chain_{sentence_and_counts[seg['sentence_id']]}",
                    "note_seed": "events compressed by repeated 'and'",
                    "token_pos": seg["token_start"],
                }
            )

        if token_count >= 12 and len(clause_verbs) <= 2:
            silences.append(
                {
                    "silence_type": "density",
                    "clause_id": clause_id,
                    "signal": "low_verb_ratio",
                    "note_seed": "thick with nouns, few verbs",
                    "token_pos": seg["token_start"],
                }
            )

        if re.search(r"\b(was|were)\s+\w+(ed|en)\b", lower):
            silences.append(
                {
                    "silence_type": "passive_gap",
                    "clause_id": clause_id,
                    "signal": "passive_voice",
                    "note_seed": "action without named agent",
                    "token_pos": seg["token_start"],
                }
            )

        if focus_nouns:
            noun_hits = sum(1 for noun in focus_nouns if noun.lower() in lower)
            if noun_hits >= 2 and len(clause_verbs) <= 2:
                silences.append(
                    {
                        "silence_type": "withholding",
                        "clause_id": clause_id,
                        "signal": "focus_noun_cluster",
                        "note_seed": "weighty terms clustered without explanation",
                        "token_pos": seg["token_start"],
                    }
                )

    silences.sort(key=lambda s: (s["token_pos"], s["silence_type"]))
    for item in silences:
        item.pop("token_pos", None)
    return silences


def infer_camera_moves(text: str):
    hay = text.lower()
    moves = []
    if any(w in hay for w in ["many", "crowd", "all", "people"]):
        moves.append("wide shot")
    if any(w in hay for w in ["face", "eyes", "seen", "saw", "beheld"]):
        moves.append("close-up")
    if any(w in hay for w in ["walk", "walked", "came", "went", "enter", "leave"]):
        moves.append("tracking shot")
    if any(w in hay for w in ["look", "see", "glory", "beheld"]):
        moves.append("slow pan")
    if any(w in hay for w in ["door", "gate", "threshold", "into", "out of"]):
        moves.append("over-the-shoulder")
    if not moves:
        moves = ["wide shot", "close-up", "slow pan"]
    unique = []
    for move in moves:
        if move not in unique:
            unique.append(move)
    if len(unique) < 3:
        unique.extend(["wide shot", "close-up", "slow pan"])
    return unique[:5]


def modal_triad_from_text(text: str):
    hay = text.lower()
    identity = []
    enactment = []
    effect = []

    if "word" in hay:
        identity.append("The Word is present.")
    if "light" in hay:
        identity.append("Light that shines in the dark.")
    if "son" in hay or "father" in hay:
        identity.append("The Son from the Father.")

    if "flesh" in hay:
        enactment.append("Takes on flesh and nearness.")
    if "dwelt" in hay or "dwell" in hay:
        enactment.append("Dwells among ordinary life.")
    if "seen" in hay or "glory" in hay or "beheld" in hay:
        enactment.append("Lets glory be witnessed.")

    if "grace" in hay:
        effect.append("Grace steadies what is fragile.")
    if "truth" in hay:
        effect.append("Truth clarifies without crushing.")
    if "glory" in hay:
        effect.append("Glory reframes the moment.")

    if len(identity) < 3:
        identity.extend(
            [
                "God comes near.",
                "Presence without fear.",
                "Mercy that does not withdraw.",
            ]
        )
    if len(enactment) < 3:
        enactment.extend(
            [
                "Enters the scene quietly.",
                "Stays with what is real.",
                "Moves toward the vulnerable.",
            ]
        )
    if len(effect) < 3:
        effect.extend(
            [
                "Hope opens without demand.",
                "Attention becomes shelter.",
                "A path forward becomes visible.",
            ]
        )

    return {
        "identity": identity[:6],
        "enactment": enactment[:6],
        "effect": effect[:6],
    }


def load_template_v4(passage_ref: str):
    templates_root = resolve_repo_path("data/templates/witness_cards/v4")
    tokens = passage_ref.split()
    if not tokens:
        raise ValueError("passage_ref is empty")
    if tokens[0].isdigit() and len(tokens) > 1:
        book = f"{tokens[0]}_{tokens[1]}".lower()
        book_key = tokens[1].lower()
    else:
        book = tokens[0].lower()
        book_key = book
    passage_slug = re.sub(r"[^a-z0-9_]+", "_", passage_ref.lower()).strip("_")
    exact_path = templates_root / f"{passage_slug}.json"
    book_path = templates_root / f"{book}.json"
    nt_books = {
        "matthew",
        "mark",
        "luke",
        "john",
        "acts",
        "romans",
        "corinthians",
        "galatians",
        "ephesians",
        "philippians",
        "colossians",
        "thessalonians",
        "timothy",
        "titus",
        "philemon",
        "hebrews",
        "james",
        "peter",
        "jude",
        "revelation",
    }
    testament_path = templates_root / ("nt.json" if book_key in nt_books else "ot.json")
    generic_path = templates_root / "generic.json"

    for path in [exact_path, book_path, testament_path, generic_path]:
        if path.exists():
            template = json.loads(path.read_text(encoding="utf-8-sig"))
            template["_template_path"] = _to_repo_relative(path)
            return template

    v3_root = resolve_repo_path("data/templates/witness_cards/v3")
    for path in [v3_root / f"{passage_slug}.json", v3_root / f"{book}.json", v3_root / "nt.json", v3_root / "generic.json"]:
        if path.exists():
            template = json.loads(path.read_text(encoding="utf-8-sig"))
            template["_template_path"] = _to_repo_relative(path)
            return template

    v2_root = resolve_repo_path("data/templates/witness_cards/v2")
    for path in [v2_root / f"{passage_slug}.json", v2_root / f"{book}.json", v2_root / "nt.json", v2_root / "generic.json"]:
        if path.exists():
            template = json.loads(path.read_text(encoding="utf-8-sig"))
            template["_template_path"] = _to_repo_relative(path)
            return template
    raise FileNotFoundError("No template found for v4 witness card generation.")


def _render_template_line(line: str, context: dict):
    def replace(match):
        key = match.group(1)
        if key in context:
            return context[key]
        return f"{{missing:{key}}}"

    return re.sub(r"\{([a-z0-9_]+)\}", replace, line)


def render_template_lines(lines, context):
    rendered = []
    placeholders_used = []
    for line in lines:
        placeholders = re.findall(r"\{([a-z0-9_]+)\}", line)
        rendered.append(_render_template_line(line, context))
        placeholders_used.append(placeholders)
    return rendered, placeholders_used


def build_scene_language(scene):
    verbs = scene["verbs"][:5]
    thresholds = scene["thresholds_detailed"][:3]
    silences = scene["silences_detailed"]
    time_markers = scene["time_markers"]

    silence_priority = {
        "withholding": 1,
        "density": 2,
        "passive_gap": 3,
        "interruption": 4,
        "compression": 5,
    }
    silences_sorted = sorted(
        silences,
        key=lambda s: (silence_priority.get(s["silence_type"], 9), s["clause_id"]),
    )
    silences_top = []
    seen_types = set()
    for item in silences_sorted:
        if item["silence_type"] in seen_types:
            continue
        silences_top.append(item)
        seen_types.add(item["silence_type"])
        if len(silences_top) >= 2:
            break

    lines = []
    if verbs:
        lines.append(f"Verbs carrying the motion: {', '.join(verbs)}")
    else:
        lines.append("Verbs carrying the motion: none detected")

    if time_markers:
        lines.append(f"Time markers: {', '.join(time_markers)}")
    else:
        lines.append("Time markers: none detected")

    if thresholds:
        for item in thresholds:
            trigger = item["trigger"]
            evidence = item["evidence_after"] or "no immediate evidence"
            lines.append(f"A turn in the scene at '{trigger}': {evidence}")
    else:
        lines.append("No explicit thresholds detected.")

    if scene.get("frames"):
        lines.append(f"Action frames: {'; '.join(scene['frames'][:3])}")
    if scene.get("characters"):
        labels = [c["label"] for c in scene["characters"]][:5]
        if labels:
            lines.append(f"Characters: {', '.join(labels)}")

    if silences_top:
        for item in silences_top:
            lines.append(f"The text moves past {item['silence_type']}: {item['note_seed']}")
    else:
        lines.append("No explicit silences detected.")

    return lines


def render_markdown(card: dict, scene_language):
    lines = []
    lines.append(f"# Witness Card: {card['passage']['ref']}")
    lines.append("")
    lines.append("## Passage")
    lines.append(card["passage"]["text"])
    lines.append("")
    lines.append("## Moment")
    lines.append(card["moment"])
    lines.append("")
    lines.append("## Scene")
    lines.extend(scene_language)
    lines.append("")
    lines.append("## Modal Triad")
    lines.append("Identity:")
    for item in card["modal_triad"]["identity"]:
        lines.append(f"- {item}")
    lines.append("Enactment:")
    for item in card["modal_triad"]["enactment"]:
        lines.append(f"- {item}")
    lines.append("Effect:")
    for item in card["modal_triad"]["effect"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Witness Prompts")
    for item in card["witness_prompts"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Prayer")
    lines.append(card["prayer"])
    lines.append("")
    lines.append("## Safety")
    lines.append(f"Avoidances: {', '.join(card['safety']['avoidances'])}")
    for note in card["safety"]["notes"]:
        lines.append(f"- {note}")
    lines.append("")
    return "\n".join(lines)


def _extract_entities(text: str):
    hay = text.lower()
    mentions = []
    if "woman of samaria" in hay or "samaritan woman" in hay:
        mentions.append({"label": "woman_of_Samaria", "gender": "F", "number": "S"})
    if "jesus" in hay:
        mentions.append({"label": "Jesus", "gender": "M", "number": "S"})
    if "john" in hay:
        mentions.append({"label": "John", "gender": "M", "number": "S"})
    if "disciples" in hay:
        mentions.append({"label": "disciples", "gender": "P", "number": "P"})
    return mentions


def _role_for_mention(text: str, label: str):
    lower = text.lower()
    if label == "woman_of_Samaria":
        key = "woman of samaria" if "woman of samaria" in lower else "samaritan woman"
    else:
        key = label.lower()
    idx = lower.find(key)
    if idx == -1:
        return "object"
    for verb in ATTRIBUTION_VERBS:
        verb_idx = lower.find(verb, idx + len(key))
        if verb_idx != -1:
            return "subject"
    return "object"


def _collect_entity_mentions(segments):
    mentions = []
    for seg in segments:
        for entity in _extract_entities(seg["text"]):
            mentions.append(
                {
                    "label": entity["label"],
                    "gender": entity["gender"],
                    "number": entity["number"],
                    "sentence_id": seg["sentence_id"],
                    "clause_id": seg["clause_id"],
                    "role": _role_for_mention(seg["text"], entity["label"]),
                    "token_start": seg["token_start"],
                }
            )
    return mentions


def _find_attribution_speaker(text: str):
    lower = text.lower()
    for label in ["jesus", "john", "disciples", "woman of samaria", "samaritan woman"]:
        for verb in ATTRIBUTION_VERBS:
            pattern = rf"\b{re.escape(label)}\b[^.?!]{{0,80}}\b{verb}\b"
            if re.search(pattern, lower):
                if label == "woman of samaria" or label == "samaritan woman":
                    return "woman_of_Samaria"
                return label.title() if label != "disciples" else "disciples"
    return None


def _resolve_pronoun(pronoun: str, utterance_sentence: int, mentions):
    gender, number = PRONOUNS.get(pronoun.lower(), ("N", "S"))
    candidates = []
    for mention in mentions:
        distance = utterance_sentence - mention["sentence_id"]
        if distance < 0 or distance > 2:
            continue
        if gender in {"M", "F", "P"} and mention["gender"] != gender:
            continue
        if number == "P" and mention["number"] != "P":
            continue
        role_priority = 0 if mention["role"] == "subject" else 1
        candidates.append((distance, role_priority, -mention["token_start"], mention["label"]))
    if not candidates:
        return None
    candidates.sort()
    return candidates[0][3]


def guess_speaker(
    utterance_text,
    sentence_text,
    prior_clause_text,
    utterance_sentence,
    mentions,
    prior_speaker,
    unknown_state,
):
    pre_quote = sentence_text
    speaker = _find_attribution_speaker(pre_quote)
    if speaker:
        return speaker

    speaker = _find_attribution_speaker(prior_clause_text or "")
    if speaker:
        return speaker

    words = utterance_text.strip().split()
    if words:
        first = re.sub(r"[^A-Za-z]", "", words[0]).lower()
        if first in VOCATIVE_TITLES and prior_speaker:
            return prior_speaker

    pronoun_match = re.search(r"\b(he|she|they)\b", pre_quote.lower())
    if pronoun_match:
        resolved = _resolve_pronoun(pronoun_match.group(1), utterance_sentence, mentions)
        if resolved:
            return resolved

    if prior_speaker:
        return prior_speaker

    pronoun_hint = pronoun_match.group(1) if pronoun_match else ""
    gender, number = PRONOUNS.get(pronoun_hint.lower(), ("N", "S"))
    if number == "P":
        key = "unknown_P"
    elif gender == "M":
        key = "unknown_M"
    elif gender == "F":
        key = "unknown_F"
    else:
        key = "unknown_N"
    unknown_state.setdefault(key, 0)
    unknown_state[key] += 1
    return f"{key}_{unknown_state[key]}"


def starts_with_wh_word(text: str) -> bool:
    words = [w for w in re.split(r"\s+", text.strip().lower()) if w]
    return bool(words and words[0] in WH_WORDS)


def starts_with_imperative_verb(text: str) -> bool:
    words = [w for w in re.split(r"\s+", text.strip().lower()) if w]
    return bool(words and words[0] in IMPERATIVE_VERBS)


def has_command_indicators(text: str) -> bool:
    lower = text.lower()
    return any(indicator in lower for indicator in COMMAND_INDICATORS)


def first_person_subject(text: str) -> bool:
    return bool(re.search(r"\b(i|we)\b", text.lower()))


def classify_speech_act(text: str, prior_utterance):
    stripped = text.strip()
    lower = stripped.lower()
    if stripped.endswith("?") or starts_with_wh_word(stripped):
        return "question"

    if (
        lower.startswith(tuple(INVITATION_VERBS))
        or "let us" in lower
        or "come and" in lower
        or "you will see" in lower
    ):
        return "invitation"

    if starts_with_imperative_verb(stripped):
        first_word = re.split(r"\s+", stripped.lower())[0]
        if first_word not in INVITATION_VERBS:
            return "command"
        if stripped.endswith("!") or has_command_indicators(stripped):
            return "command"

    if stripped.split()[0:1] == ["Behold"] and stripped.endswith("!"):
        return "testimony"
    if first_person_subject(stripped):
        if re.search(r"\b(we have seen|i testify|i bear witness|truly|i say to you)\b", lower):
            return "testimony"
        if re.search(r"\b(saw|heard|beheld|testify)\b", lower):
            return "testimony"

    return "unknown"


def extract_utterances(text: str, segments, sentence_spans, mentions):
    utterances = []
    unknown_state = {}
    prior_speaker = None
    prior_utterance = None
    for match in re.finditer(r"\"([^\"]+)\"", text):
        utterance_text = match.group(1).strip()
        start, end = match.start(1), match.end(1)
        clause_id = None
        sentence_id = None
        for seg in segments:
            if seg["token_start"] <= start < seg["token_end"]:
                clause_id = seg["clause_id"]
                sentence_id = seg["sentence_id"]
                break
        sentence_text = ""
        prior_clause_text = ""
        if sentence_id is not None:
            s_start, _ = sentence_spans[sentence_id]
            sentence_text = text[s_start:start]
            if clause_id:
                seg_index = next(
                    (i for i, seg in enumerate(segments) if seg["clause_id"] == clause_id),
                    None,
                )
                if seg_index is not None and seg_index > 0:
                    prior_clause_text = segments[seg_index - 1]["text"]

        speaker_guess = guess_speaker(
            utterance_text,
            sentence_text,
            prior_clause_text,
            sentence_id or 0,
            mentions,
            prior_speaker,
            unknown_state,
        )
        speech_act = classify_speech_act(
            utterance_text,
            prior_utterance
            or {"speech_act": "unknown", "speaker_guess": None, "current_speaker": None},
        )
        if prior_utterance and prior_utterance["speech_act"] == "question":
            if prior_utterance["speaker_guess"] != speaker_guess and speech_act == "unknown":
                speech_act = "response"

        utterance_entry = {
            "text": utterance_text,
            "speaker_guess": speaker_guess,
            "speech_act": speech_act,
            "clause_id": clause_id,
            "token_span": [start, end],
        }
        utterances.append(utterance_entry)
        prior_speaker = speaker_guess
        prior_utterance = {
            "speech_act": speech_act,
            "speaker_guess": speaker_guess,
            "current_speaker": speaker_guess,
        }
    return utterances


def _character_meta():
    return {
        "Jesus": {"char_id": "char_jesus", "label": "Jesus", "gender": "M", "number": "S"},
        "John": {"char_id": "char_john", "label": "John", "gender": "M", "number": "S"},
        "disciples": {"char_id": "char_disciples", "label": "disciples", "gender": "P", "number": "P"},
        "woman_of_Samaria": {
            "char_id": "char_woman_of_samaria",
            "label": "woman_of_Samaria",
            "gender": "F",
            "number": "S",
        },
    }


def build_character_registry(text: str, segments):
    meta = _character_meta()
    patterns = [
        ("woman_of_Samaria", r"\bwoman of Samaria\b"),
        ("woman_of_Samaria", r"\bSamaritan woman\b"),
        ("Jesus", r"\bJesus\b"),
        ("John", r"\bJohn\b"),
        ("disciples", r"\bdisciples\b"),
    ]
    char_mentions = {m["char_id"]: [] for m in meta.values()}

    for seg in segments:
        for label_key, pattern in patterns:
            for match in re.finditer(pattern, seg["text"]):
                meta_entry = meta[label_key]
                start = seg["token_start"] + match.start()
                end = seg["token_start"] + match.end()
                char_mentions[meta_entry["char_id"]].append(
                    {
                        "clause_id": seg["clause_id"],
                        "token_span": [start, end],
                        "surface": seg["text"][match.start():match.end()],
                        "sentence_id": seg["sentence_id"],
                        "role": _role_for_mention(seg["text"], meta_entry["label"]),
                    }
                )

    characters = []
    for label_key, entry in meta.items():
        mentions = char_mentions[entry["char_id"]]
        if not mentions:
            continue
        mentions = sorted(mentions, key=lambda m: (m["token_span"][0], m["surface"]))
        characters.append(
            {
                "char_id": entry["char_id"],
                "label": entry["label"],
                "gender": entry["gender"],
                "number": entry["number"],
                "mentions": [
                    {
                        "clause_id": m["clause_id"],
                        "token_span": m["token_span"],
                        "surface": m["surface"],
                    }
                    for m in mentions
                ],
                "_mentions_meta": mentions,
            }
        )

    characters.sort(
        key=lambda c: (
            c["_mentions_meta"][0]["token_span"][0],
            c["label"],
        )
    )
    return characters


def _build_candidate_mentions(characters):
    candidates = []
    for char in characters:
        for mention in char.get("_mentions_meta", []):
            candidates.append(
                {
                    "char_id": char["char_id"],
                    "label": char["label"],
                    "gender": char.get("gender"),
                    "number": char.get("number"),
                    "sentence_id": mention["sentence_id"],
                    "token_start": mention["token_span"][0],
                    "role": mention.get("role", "object"),
                }
            )
    return candidates


def _unknown_char_id(gender, number, unknown_state):
    if number == "P":
        key = "unknown_P"
    elif gender == "M":
        key = "unknown_M"
    elif gender == "F":
        key = "unknown_F"
    else:
        key = "unknown_N"
    unknown_state.setdefault(key, 0)
    unknown_state[key] += 1
    return f"char_{key}_{unknown_state[key]}", key


def build_coref_links(text: str, segments, characters):
    candidates = _build_candidate_mentions(characters)
    unknown_state = {}
    coref_links = []

    pronoun_pattern = re.compile(
        r"\b(he|she|they|him|her|them|his|their|it|its)\b", re.IGNORECASE
    )

    for seg in segments:
        for match in pronoun_pattern.finditer(seg["text"]):
            pronoun = match.group(1)
            start = seg["token_start"] + match.start()
            end = seg["token_start"] + match.end()
            gender, number = PRONOUNS.get(pronoun.lower(), ("N", "S"))

            lookback = [
                c
                for c in candidates
                if 0 <= seg["sentence_id"] - c["sentence_id"] <= 2
            ]

            filtered = []
            for c in lookback:
                if gender in {"M", "F"} and c["gender"] != gender:
                    continue
                if number == "P" and c["number"] != "P":
                    continue
                filtered.append(c)

            rule = "recency"
            if gender in {"M", "F"}:
                rule = "gender_match"
            elif number == "P":
                rule = "number_match"

            if not filtered:
                char_id, key = _unknown_char_id(gender, number, unknown_state)
                characters.append(
                    {
                        "char_id": char_id,
                        "label": key,
                        "gender": gender,
                        "number": number,
                        "mentions": [],
                        "_mentions_meta": [],
                    }
                )
                coref_links.append(
                    {
                        "from": {
                            "clause_id": seg["clause_id"],
                            "token_span": [start, end],
                            "surface_pronoun": pronoun,
                        },
                        "to_char_id": char_id,
                        "rule": "lookback_limit",
                        "evidence": f"no match within lookback for {pronoun}",
                    }
                )
                continue

            role_priority = {"subject": 0, "object": 1, "possessive": 2}
            def sort_key(c):
                return (
                    seg["sentence_id"] - c["sentence_id"],
                    role_priority.get(c["role"], 1),
                    -c["token_start"],
                )
            sorted_candidates = sorted(filtered, key=sort_key)
            chosen = sorted_candidates[0]

            if len(filtered) > 1:
                roles = {c["role"] for c in filtered}
                if len(roles) > 1:
                    rule = "role_priority"

            coref_links.append(
                {
                    "from": {
                        "clause_id": seg["clause_id"],
                        "token_span": [start, end],
                        "surface_pronoun": pronoun,
                    },
                    "to_char_id": chosen["char_id"],
                    "rule": rule,
                    "evidence": f"resolved {pronoun} to {chosen['char_id']} by {rule}",
                }
            )

    coref_links.sort(key=lambda c: (c["from"]["token_span"][0], c["to_char_id"]))
    for idx, link in enumerate(coref_links):
        link["id"] = f"coref_{idx}"
    return characters, coref_links


def _resolve_pronoun_label(token_span, coref_links, characters):
    lookup = {tuple(link["from"]["token_span"]): link["to_char_id"] for link in coref_links}
    char_map = {c["char_id"]: c["label"] for c in characters}
    char_id = lookup.get(tuple(token_span))
    if not char_id:
        return None
    return char_map.get(char_id, char_id)


def _frame_string(actor, verb, obj, indirect_object):
    if actor is None:
        actor = "unknown"
    if indirect_object:
        return f"{actor} {verb} to {indirect_object}"
    if obj:
        return f"{actor} {verb} {obj}"
    return f"{actor} {verb}"


def extract_action_frames(text: str, segments, verbs_detailed, characters, coref_links):
    frames = []
    unknown_actor_state = {}
    for verb in verbs_detailed:
        clause = next((s for s in segments if s["clause_id"] == verb["clause_id"]), None)
        if not clause:
            continue
        clause_text = clause["text"]
        clause_start = clause["token_start"]
        verb_start = verb["token_span"][0]

        entity_patterns = [
            ("woman_of_Samaria", r"\bwoman of Samaria\b"),
            ("woman_of_Samaria", r"\bSamaritan woman\b"),
            ("Jesus", r"\bJesus\b"),
            ("John", r"\bJohn\b"),
            ("disciples", r"\bdisciples\b"),
        ]

        matches = []
        for label, pattern in entity_patterns:
            for match in re.finditer(pattern, clause_text):
                matches.append((match.start(), match.end(), label))

        pronoun_pattern = re.compile(
            r"\b(he|she|they|him|her|them|his|their|it|its)\b", re.IGNORECASE
        )
        for match in pronoun_pattern.finditer(clause_text):
            matches.append((match.start(), match.end(), match.group(1)))

        before = [m for m in matches if clause_start + m[0] < verb_start]
        after = [m for m in matches if clause_start + m[0] > verb_start]

        actor = None
        if before:
            start, end, label = sorted(before, key=lambda m: (m[0], m[1]))[-1]
            token_span = [clause_start + start, clause_start + end]
            resolved = _resolve_pronoun_label(token_span, coref_links, characters)
            if resolved:
                actor = resolved
            else:
                actor = label

        if not actor:
            unknown_actor_state.setdefault("unknown_actor", 0)
            unknown_actor_state["unknown_actor"] += 1
            actor = f"unknown_actor_{unknown_actor_state['unknown_actor']}"

        obj = None
        if after:
            start, end, label = sorted(after, key=lambda m: (m[0], m[1]))[0]
            token_span = [clause_start + start, clause_start + end]
            resolved = _resolve_pronoun_label(token_span, coref_links, characters)
            obj = resolved or label

        indirect_object = None
        modifiers = []
        suffix = clause_text[verb_start - clause_start:]
        io_match = re.search(r"\b(to|for)\s+([^,.;!?]+)", suffix)
        if io_match:
            indirect_object = io_match.group(2).strip()
            modifiers.append(f"{io_match.group(1)} {indirect_object}")

        prep_patterns = [
            "in",
            "on",
            "at",
            "by",
            "with",
            "among",
            "into",
            "from",
            "about",
            "that day",
            "the next day",
        ]
        for prep in prep_patterns:
            m = re.search(rf"\b{re.escape(prep)}\b[^,.;!?]*", suffix)
            if m:
                mod = m.group(0).strip()
                if mod and mod not in modifiers:
                    modifiers.append(mod)

        tokens = [t.lower() for t, _, _ in _iter_tokens_with_spans(clause_text)]
        polarity = "affirm"
        if "not" in tokens or "no" in tokens or "never" in tokens:
            polarity = "neg"

        voice_guess = "active"
        if re.search(r"\b(was|were|is|are|been|be)\s+\w+(ed|en)\b", clause_text.lower()):
            voice_guess = "passive"

        frame = {
            "id": None,
            "actor": actor,
            "verb": verb["verb_text"],
            "object": obj,
            "indirect_object": indirect_object,
            "modifiers": modifiers,
            "polarity": polarity,
            "voice_guess": voice_guess,
            "clause_id": verb["clause_id"],
            "token_span": verb["token_span"],
        }
        frames.append(frame)

    frames.sort(key=lambda f: (f["token_span"][0], f["verb"], f["actor"]))
    for idx, frame in enumerate(frames):
        frame["id"] = f"frame_{idx}"
    frames_simple = [_frame_string(f["actor"], f["verb"], f["object"], f["indirect_object"]) for f in frames]
    return frames_simple, frames


def build_evidence_map_v4(thresholds, silences, utterances, prompts, frames, characters, coref_links):
    evidence = {
        "thresholds": [],
        "silences": [],
        "utterances": [],
        "witness_prompts": [],
        "frames": [],
        "characters": [],
        "coref_links": [],
    }

    for idx, threshold in enumerate(thresholds):
        evidence["thresholds"].append(
            {
                "id": f"threshold_{idx}",
                "clause_id": threshold.get("to_clause_id"),
                "token_span": threshold.get("token_span"),
                "trigger": threshold.get("trigger"),
                "kind": threshold.get("kind"),
                "evidence_before": threshold.get("evidence_before"),
                "evidence_after": threshold.get("evidence_after"),
            }
        )

    for idx, silence in enumerate(silences):
        evidence["silences"].append(
            {
                "id": f"silence_{idx}",
                "type": silence.get("silence_type"),
                "clause_ids": [silence.get("clause_id")],
                "signal": silence.get("signal"),
                "note_seed": silence.get("note_seed"),
            }
        )

    for idx, utterance in enumerate(utterances):
        evidence["utterances"].append(
            {
                "id": f"utterance_{idx}",
                "clause_id": utterance.get("clause_id"),
                "token_span": utterance.get("token_span"),
                "speaker_guess": utterance.get("speaker_guess"),
                "text": utterance.get("text"),
                "speech_act": utterance.get("speech_act"),
            }
        )

    for idx, prompt in enumerate(prompts):
        evidence["witness_prompts"].append(
            {
                "id": f"prompt_{idx}",
                "text": prompt["text"],
                "linked_threshold": prompt.get("linked_threshold"),
                "linked_utterance": prompt.get("linked_utterance"),
                "linked_silence": prompt.get("linked_silence"),
            }
        )

    for frame in frames:
        evidence["frames"].append(
            {
                "id": frame["id"],
                "clause_id": frame["clause_id"],
                "token_span": frame["token_span"],
                "actor": frame["actor"],
                "verb": frame["verb"],
                "object": frame["object"],
                "indirect_object": frame["indirect_object"],
            }
        )

    for char in characters:
        if not char.get("mentions"):
            continue
        first = char["mentions"][0]
        evidence["characters"].append(
            {
                "char_id": char["char_id"],
                "label": char["label"],
                "first_mention_clause_id": first["clause_id"],
                "first_mention_token_span": first["token_span"],
            }
        )

    for link in coref_links:
        evidence["coref_links"].append(
            {
                "id": link["id"],
                "from": link["from"],
                "to_char_id": link["to_char_id"],
                "rule": link["rule"],
                "evidence": link["evidence"],
            }
        )

    return evidence


def _load_manifest(manifest_path: Path):
    raw = manifest_path.read_text(encoding="utf-8")
    normalized = raw.replace("\r\n", "\n").replace("\r", "\n")
    manifest_sha256 = _sha256_text(normalized)
    data = json.loads(raw)
    passages = data.get("passages") if isinstance(data, dict) and "passages" in data else data
    if not isinstance(passages, dict):
        raise ValueError("manifest must map passage refs to entries")
    return passages, manifest_sha256


def _resolve_passage_from_manifest(passage_ref: str, manifest_path: Path):
    passages, manifest_sha256 = _load_manifest(manifest_path)
    normalized_ref = normalize_passage_ref(passage_ref)
    entry = passages.get(normalized_ref)
    if not entry:
        raise ValueError(f"passage not found in manifest: {normalized_ref}")
    file_path = manifest_path.parent / entry["file"]
    passage_bytes = file_path.read_bytes()
    expected_sha = entry.get("sha256")
    actual_sha = _sha256_bytes(passage_bytes)
    if expected_sha and actual_sha != expected_sha:
        raise ValueError("manifest sha256 mismatch for passage file")
    return {
        "passage_ref": normalized_ref,
        "file_path": file_path,
        "file_rel": entry["file"],
        "manifest_sha256": manifest_sha256,
        "passage_bytes": passage_bytes,
    }


def _resolve_passage_text(passage_ref: str, textfile: str, manifest: str, dataset: str):
    if textfile:
        passage_text_path = resolve_repo_path(textfile)
        passage_text = passage_text_path.read_text(encoding="utf-8")
        return {
            "passage_ref": passage_ref,
            "textfile": textfile,
            "passage_text": passage_text,
            "manifest_sha256": None,
            "dataset": None,
        }
    if manifest:
        manifest_path = resolve_repo_path(manifest)
        resolved = _resolve_passage_from_manifest(passage_ref, manifest_path)
        passage_text = resolved["passage_bytes"].decode("utf-8")
        return {
            "passage_ref": resolved["passage_ref"],
            "textfile": resolved["file_rel"],
            "passage_text": passage_text,
            "manifest_sha256": resolved["manifest_sha256"],
            "dataset": None,
        }
    if dataset:
        manifest_path = resolve_repo_path(f"data/scripture/{dataset}/manifest.json")
        resolved = _resolve_passage_from_manifest(passage_ref, manifest_path)
        passage_text = resolved["passage_bytes"].decode("utf-8")
        return {
            "passage_ref": resolved["passage_ref"],
            "textfile": resolved["file_rel"],
            "passage_text": passage_text,
            "manifest_sha256": resolved["manifest_sha256"],
            "dataset": dataset,
        }
    raise ValueError("must provide --textfile, --dataset, or --manifest")


def generate_review_md(card: dict):
    lines = []
    lines.append("# Witness Card Review")
    lines.append("")
    lines.append(f"Passage: {card['passage']['ref']}")
    lines.append(f"Moment: {card['moment']}")
    lines.append("")
    lines.append("Speakers:")
    for speaker in card["scene"]["speakers"]:
        lines.append(f"- {speaker}")
    lines.append("Questions:")
    for question in card["scene"]["questions"]:
        lines.append(f"- {question}")
    lines.append("Utterances:")
    for utterance in card["scene"]["utterances"]:
        lines.append(f"- {utterance}")
    lines.append("")
    lines.append("Template:")
    lines.append(card["template"]["path"] or "unknown")
    lines.append("")
    return "\n".join(lines)


def generate_witness_card_v4(
    passage: str,
    textfile: str,
    moment: str,
    out: str,
    dataset: str = None,
    manifest: str = None,
    review_mode: str = "none",
):
    resolved = _resolve_passage_text(passage, textfile, manifest, dataset)
    passage_ref = resolved["passage_ref"]
    passage_text = resolved["passage_text"]
    textfile_value = resolved["textfile"]
    manifest_sha256 = resolved["manifest_sha256"]
    dataset_value = resolved["dataset"]

    normalized_text = normalize_text(passage_text)
    normalized_text_sha256 = _sha256_text(normalized_text)
    passage_text_sha256 = _sha256_text(passage_text.strip())
    generator_bytes = Path(__file__).read_bytes()
    generator_sha256 = hashlib.sha256(generator_bytes).hexdigest()

    segments, boundaries, sentence_spans = build_segments(normalized_text)
    verbs_detailed = extract_verbs(normalized_text, segments)
    time_markers_detailed = extract_time_markers(normalized_text, segments)
    thresholds_detailed = extract_thresholds(normalized_text, segments, boundaries)

    template = load_template_v4(passage_ref)
    focus_nouns = template.get("focus_nouns", [])
    silences_detailed = extract_silences(
        normalized_text, segments, verbs_detailed, focus_nouns
    )

    mentions = _collect_entity_mentions(segments)
    utterances_detailed = extract_utterances(
        normalized_text, segments, sentence_spans, mentions
    )
    characters = build_character_registry(normalized_text, segments)
    characters, coref_links = build_coref_links(normalized_text, segments, characters)
    frames_simple, frames_detailed = extract_action_frames(
        normalized_text, segments, verbs_detailed, characters, coref_links
    )

    verbs_simple = [v["verb_text"] for v in verbs_detailed]
    thresholds_simple = [t["trigger"] for t in thresholds_detailed]
    silences_simple = [s["silence_type"] for s in silences_detailed]
    time_markers_simple = [m["text"] for m in time_markers_detailed]
    utterances_simple = [u["text"] for u in utterances_detailed]

    speakers = []
    questions = []
    for utt in utterances_detailed:
        if utt["speaker_guess"] not in speakers:
            speakers.append(utt["speaker_guess"])
        if utt["speech_act"] == "question":
            questions.append(utt["text"])

    characters_output = [
        {"char_id": c["char_id"], "label": c["label"], "mentions": c["mentions"]}
        for c in characters
    ]

    scene = {
        "time_markers": time_markers_simple,
        "verbs": verbs_simple,
        "thresholds": thresholds_simple,
        "silences": silences_simple,
        "camera_moves": infer_camera_moves(normalized_text),
        "segments": segments,
        "verbs_detailed": verbs_detailed,
        "time_markers_detailed": time_markers_detailed,
        "thresholds_detailed": thresholds_detailed,
        "silences_detailed": silences_detailed,
        "utterances": utterances_simple,
        "utterances_detailed": utterances_detailed,
        "frames": frames_simple,
        "frames_detailed": frames_detailed,
        "characters": characters_output,
        "coref_links": coref_links,
        "speakers": speakers,
        "questions": questions,
    }

    card_base = f"v4|{passage_ref}|{normalized_text}|{moment}"
    card_id = "witness_card_" + hashlib.sha256(card_base.encode("utf-8")).hexdigest()[:12]

    context = {
        "focus_nouns": ", ".join(focus_nouns),
    }
    helper_verbs = {"have", "has", "had", "am", "is", "are", "was", "were"}
    context_verbs = [v for v in verbs_simple if v.lower() not in helper_verbs]
    if not context_verbs:
        context_verbs = verbs_simple
    for idx, verb in enumerate(context_verbs[:6], start=1):
        context[f"verb_{idx}"] = verb
    for idx, marker in enumerate(time_markers_simple[:6], start=1):
        context[f"time_marker_{idx}"] = marker
    for idx, threshold in enumerate(thresholds_simple[:6], start=1):
        context[f"threshold_{idx}"] = threshold

    for idx, speaker in enumerate(speakers[:6], start=1):
        context[f"speaker_{idx}"] = speaker
    for idx, question in enumerate(questions[:6], start=1):
        context[f"question_{idx}"] = question
    for idx, utt in enumerate(utterances_simple[:6], start=1):
        context[f"utterance_{idx}"] = utt

    invitations = [u["text"] for u in utterances_detailed if u["speech_act"] == "invitation"]
    commands = [u["text"] for u in utterances_detailed if u["speech_act"] == "command"]
    testimonies = [u["text"] for u in utterances_detailed if u["speech_act"] == "testimony"]
    for idx, utt in enumerate(invitations[:6], start=1):
        context[f"invitation_{idx}"] = utt
    for idx, utt in enumerate(commands[:6], start=1):
        context[f"command_{idx}"] = utt
    for idx, utt in enumerate(testimonies[:6], start=1):
        context[f"testimony_{idx}"] = utt

    actors = []
    actions = []
    objects = []
    for frame in frames_detailed:
        if frame["actor"] and frame["actor"] not in actors:
            actors.append(frame["actor"])
        actions.append(frame["verb"])
        if frame.get("object"):
            objects.append(frame["object"])

    for idx, actor in enumerate(actors[:6], start=1):
        context[f"actor_{idx}"] = actor
    for idx, action in enumerate(actions[:6], start=1):
        context[f"action_{idx}"] = action
    for idx, obj in enumerate(objects[:6], start=1):
        context[f"object_{idx}"] = obj
    for idx, frame in enumerate(frames_simple[:6], start=1):
        context[f"frame_{idx}"] = frame

    movement_frame = None
    for frame in frames_detailed:
        if frame["verb"].lower() not in ATTRIBUTION_VERBS:
            movement_frame = _frame_string(
                frame["actor"], frame["verb"], frame.get("object"), frame.get("indirect_object")
            )
            break
    if movement_frame:
        context["movement_1"] = movement_frame

    witness_prompts, prompt_placeholders = render_template_lines(
        template.get("witness_prompts", []), context
    )
    prayer_frames, _ = render_template_lines(template.get("prayer_frames", []), context)
    prayer = "\n".join([line for line in prayer_frames if line.strip()])
    safety_notes = [
        "This is pastoral presence, not diagnosis.",
        "Invite gently; do not pressure outcomes.",
    ] + template.get("safety_notes_append", [])

    prompt_links = []
    for idx, placeholders in enumerate(prompt_placeholders):
        link = {"text": witness_prompts[idx]}
        for placeholder in placeholders:
            if placeholder.startswith("threshold_"):
                index = int(placeholder.split("_")[1]) - 1
                if 0 <= index < len(thresholds_detailed):
                    link["linked_threshold"] = f"threshold_{index}"
                    break
            if placeholder.startswith("utterance_") or placeholder.startswith("question_"):
                index = int(placeholder.split("_")[1]) - 1
                if 0 <= index < len(utterances_detailed):
                    link["linked_utterance"] = f"utterance_{index}"
                    break
        prompt_links.append(link)

    scene["evidence_map"] = build_evidence_map_v4(
        thresholds_detailed,
        silences_detailed,
        utterances_detailed,
        prompt_links,
        frames_detailed,
        characters_output,
        coref_links,
    )

    template_id = template.get("template_id") or template.get("id")
    card = {
        "id": card_id,
        "spec_version": "v4",
        "passage": {"ref": passage_ref, "text": normalized_text},
        "moment": moment,
        "scene": scene,
        "modal_triad": modal_triad_from_text(normalized_text),
        "witness_prompts": witness_prompts,
        "prayer": prayer,
        "safety": {
            "avoidances": ["moralism", "fixing", "certainty claims"],
            "notes": safety_notes,
        },
        "template": {
            "id": template_id,
            "path": template.get("_template_path"),
        },
    }

    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    card_json = json.dumps(card, indent=2, ensure_ascii=True, sort_keys=True)
    with (out_dir / "card.json").open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(card_json)

    scene_language = build_scene_language(scene)
    card_md = render_markdown(card, scene_language)
    with (out_dir / "card.md").open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(card_md)

    card_hash = hashlib.sha256(card_json.encode("utf-8")).hexdigest()
    provenance = {
        "version": "v4",
        "method": "heuristic_v4",
        "inputs": {
            "passage_ref": passage_ref,
            "moment": moment,
            "textfile": textfile_value,
        },
        "card_sha256": card_hash,
        "passage_text_sha256": passage_text_sha256,
        "normalized_text_sha256": normalized_text_sha256,
        "template_path": template.get("_template_path"),
        "generator_sha256": generator_sha256,
        "review_md_generated": review_mode == "template",
        "review_mode": "template" if review_mode == "template" else "none",
    }
    if dataset_value:
        provenance["inputs"]["dataset"] = dataset_value
    if manifest_sha256:
        provenance["dataset_manifest_sha256"] = manifest_sha256

    with (out_dir / "provenance.json").open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(provenance, indent=2, ensure_ascii=True, sort_keys=True))

    with (out_dir / "attestation.sha256").open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(card_hash + "\n")

    log_lines = [
        "witness_card_generator v4",
        f"output_dir={out_dir}",
        "files_written=card.json, card.md, provenance.json, attestation.sha256, log.txt",
    ]
    with (out_dir / "log.txt").open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(log_lines) + "\n")

    if review_mode == "template":
        review_md = generate_review_md(card)
        with (out_dir / "review.md").open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(review_md)
    elif review_mode == "ai":
        raise ValueError("review-mode ai is not supported in offline mode")

    return card_id, card_hash
