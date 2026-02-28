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
    "he",
    "she",
    "they",
    "we",
    "i",
    "you",
    "him",
    "her",
    "them",
    "us",
    "me",
    "my",
    "our",
    "your",
    "his",
    "their",
    "thee",
    "thou",
}


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


def normalize_text(text: str) -> str:
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
    return segments, boundaries


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
    segments_by_id = {seg["clause_id"]: seg for seg in segments}

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
                    "token_pos": seg["token_start"],
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
                        "token_pos": seg["token_start"],
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
                    "token_pos": seg["token_start"],
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
                    "token_pos": seg["token_start"] + offset,
                }
            )

    for boundary in boundaries:
        reason = boundary["reason"]
        if reason in {":", ";", "—", "–"}:
            before, after = _evidence_window(text, boundary["boundary"])
            thresholds.append(
                {
                    "kind": "reframe",
                    "trigger": reason,
                    "from_clause_id": None,
                    "to_clause_id": None,
                    "evidence_before": before,
                    "evidence_after": after,
                    "token_pos": boundary["boundary"],
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
                    "token_pos": segments[idx]["token_start"],
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
                    "token_pos": segments[idx]["token_start"],
                }
            )

    thresholds.sort(key=lambda t: (t["token_pos"], t["kind"], t["trigger"]))
    for item in thresholds:
        item.pop("token_pos", None)
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


def load_template(passage_ref: str):
    templates_root = resolve_repo_path("data/templates/witness_cards/v2")
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
            template = json.loads(path.read_text(encoding="utf-8"))
            template["_template_path"] = _to_repo_relative(path)
            return template
    raise FileNotFoundError("No template found for v2 witness card generation.")


def _render_template_line(line: str, context: dict):
    def replace(match):
        key = match.group(1)
        if key in context:
            return context[key]
        return f"{{missing:{key}}}"

    return re.sub(r"\{([a-z0-9_]+)\}", replace, line)


def render_template_lines(lines, context):
    rendered = []
    for line in lines:
        rendered.append(_render_template_line(line, context))
    return rendered


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


def generate_witness_card_v2(passage: str, textfile: str, moment: str, out: str):
    if textfile:
        passage_text_path = resolve_repo_path(textfile)
        passage_text = passage_text_path.read_text(encoding="utf-8")
        textfile_value = textfile
    else:
        passage_text = (
            "And the Word became flesh and dwelt among us, and we have seen his glory, "
            "glory as of the only Son from the Father, full of grace and truth."
        )
        textfile_value = None

    normalized_text = normalize_text(passage_text)
    normalized_text_sha256 = _sha256_text(normalized_text)
    passage_text_sha256 = _sha256_text(passage_text.strip())
    generator_bytes = Path(__file__).read_bytes()
    generator_sha256 = hashlib.sha256(generator_bytes).hexdigest()

    segments, boundaries = build_segments(normalized_text)
    verbs_detailed = extract_verbs(normalized_text, segments)
    time_markers_detailed = extract_time_markers(normalized_text, segments)
    thresholds_detailed = extract_thresholds(normalized_text, segments, boundaries)

    template = load_template(passage)
    focus_nouns = template.get("focus_nouns", [])
    silences_detailed = extract_silences(
        normalized_text, segments, verbs_detailed, focus_nouns
    )

    verbs_simple = [v["verb_text"] for v in verbs_detailed]
    thresholds_simple = [t["trigger"] for t in thresholds_detailed]
    silences_simple = [s["silence_type"] for s in silences_detailed]
    time_markers_simple = [m["text"] for m in time_markers_detailed]

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
    }

    card_base = f"v2|{passage}|{normalized_text}|{moment}"
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

    witness_prompts = render_template_lines(template.get("witness_prompts", []), context)
    prayer_frames = render_template_lines(template.get("prayer_frames", []), context)
    prayer = "\n".join([line for line in prayer_frames if line.strip()])
    safety_notes = [
        "This is pastoral presence, not diagnosis.",
        "Invite gently; do not pressure outcomes.",
    ] + template.get("safety_notes_append", [])

    template_id = template.get("template_id") or template.get("id")
    card = {
        "id": card_id,
        "spec_version": "v2",
        "passage": {"ref": passage, "text": normalized_text},
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
        "version": "v2",
        "method": "heuristic_v2",
        "inputs": {
            "passage_ref": passage,
            "moment": moment,
            "textfile": textfile_value,
        },
        "card_sha256": card_hash,
        "passage_text_sha256": passage_text_sha256,
        "normalized_text_sha256": normalized_text_sha256,
        "template_path": template.get("_template_path"),
        "generator_sha256": generator_sha256,
    }
    with (out_dir / "provenance.json").open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(provenance, indent=2, ensure_ascii=True, sort_keys=True))

    with (out_dir / "attestation.sha256").open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(card_hash + "\n")

    log_lines = [
        "witness_card_generator v2",
        f"output_dir={out_dir}",
        "files_written=card.json, card.md, provenance.json, attestation.sha256, log.txt",
    ]
    with (out_dir / "log.txt").open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(log_lines) + "\n")

    return card_id, card_hash
