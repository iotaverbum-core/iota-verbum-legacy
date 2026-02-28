import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

import iv_witness_card_v2
import iv_witness_card_v3
import iv_witness_card_v4


SAMPLE_TEXT = (
    "And the Word became flesh and dwelt among us, and we have seen his glory, "
    "glory as of the only Son from the Father, full of grace and truth."
)

COMMON_VERBS = [
    "be",
    "became",
    "dwell",
    "dwelt",
    "see",
    "seen",
    "come",
    "came",
    "go",
    "went",
    "speak",
    "say",
    "said",
    "walk",
    "walked",
    "give",
    "gave",
    "take",
    "took",
    "touch",
    "enter",
    "leave",
    "stand",
    "sit",
    "rise",
    "keep",
    "remain",
    "abide",
    "know",
    "love",
]

TIME_MARKERS = [
    "when",
    "then",
    "now",
    "after",
    "before",
    "while",
    "as",
    "again",
    "until",
]

THRESHOLD_CUES = [
    "into",
    "out of",
    "through",
    "door",
    "gate",
    "river",
    "house",
    "home",
]

SILENCE_CUES = ["no", "without", "not yet", "paused", "silence", "still"]
HELPER_VERBS = {"am", "are", "is", "was", "were", "be", "been", "being", "has", "have", "had"}


def normalize_whitespace(text: str) -> str:
    # Collapse all whitespace (including newlines/tabs) into single spaces.
    return " ".join(text.split()).strip()


def _tokens(text: str):
    return re.findall(r"[a-z']+", text.lower())


def resolve_repo_path(p: str) -> Path:
    path = Path(p)
    if path.is_absolute():
        return path
    repo_root = Path(__file__).resolve().parent
    return repo_root / path


def extract_verbs(text: str, moment: str):
    tokens = _tokens(text + " " + moment)
    found = []
    for verb in COMMON_VERBS:
        if verb in tokens:
            found.append(verb)
    # -ed/-ing fallback, but only if preceded by "to" or a helper verb
    for i, token in enumerate(tokens):
        if not (token.endswith("ed") or token.endswith("ing")):
            continue
        prev = tokens[i - 1] if i > 0 else ""
        if prev == "to" or prev in HELPER_VERBS:
            if token not in found:
                found.append(token)
    if not found:
        found = ["see", "speak", "come"]
    return found[:10]


def extract_time_markers(text: str, moment: str):
    tokens = _tokens(text + " " + moment)
    found = [m for m in TIME_MARKERS if m in tokens]
    return found


def extract_thresholds(text: str, moment: str):
    hay = (text + " " + moment).lower()
    found = []

    # Physical/scene cues
    for cue in THRESHOLD_CUES:
        if cue in hay and cue not in found:
            found.append(cue)

    # Theological thresholds (deterministic, stable ordering)
    if ("became" in hay or "flesh" in hay) and "incarnation" not in found:
        found.append("incarnation")
    if ("dwelt" in hay or "among" in hay) and "dwelling among" not in found:
        found.append("dwelling among")
    if ("seen" in hay or "glory" in hay) and "witnessed glory" not in found:
        found.append("witnessed glory")

    return found


def extract_silences(text: str, moment: str):
    hay = (text + " " + moment).lower()
    tokens = _tokens(hay)
    found = []
    for cue in SILENCE_CUES:
        if cue == "not yet":
            if "not yet" in hay:
                found.append(cue)
        elif cue in tokens:
            found.append(cue)
    return found


def infer_camera_moves(text: str, moment: str):
    hay = (text + " " + moment).lower()
    moves = []
    if any(w in hay for w in ["many", "crowd", "all", "people"]):
        moves.append("wide shot")
    if any(w in hay for w in ["face", "eyes", "seen", "saw"]):
        moves.append("close-up")
    if any(w in hay for w in ["walk", "walked", "came", "went", "enter", "leave"]):
        moves.append("tracking shot")
    if any(w in hay for w in ["look", "see", "glory"]):
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
    if "seen" in hay or "glory" in hay:
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


def witness_prompts_from_text(text: str, moment: str):
    hay = (text + " " + moment).lower()
    prompts = [
        "Where do you sense presence in this moment?",
        "What part of this scene feels most tender?",
        "What would it mean to stay with this without fixing it?",
        "What small detail feels like grace today?",
        "Who might need gentle witness alongside you?",
    ]
    if "light" in hay or "dark" in hay:
        prompts.insert(1, "Where is light already finding you?")
    if "door" in hay or "gate" in hay or "threshold" in hay:
        prompts.insert(2, "What threshold are you standing at right now?")
    unique = []
    for prompt in prompts:
        if prompt not in unique:
            unique.append(prompt)
    return unique[:5]


def prayer_from_text(text: str):
    hay = text.lower()
    lines = []
    if "word" in hay and "flesh" in hay:
        lines.append("Word made flesh, be near to us.")
    else:
        lines.append("God of presence, be near to us.")
    lines.append("Help us see what is true without fear.")
    if "grace" in hay and "truth" in hay:
        lines.append("Let grace and truth steady our steps.")
    else:
        lines.append("Let mercy and truth steady our steps.")
    lines.append("Teach us to witness with gentleness and care.")
    return "\n".join(lines[:6])


def build_card(passage_ref: str, passage_text: str, moment: str):
    card_base = f"{passage_ref}|{passage_text}|{moment}"
    card_id = "witness_card_" + hashlib.sha256(card_base.encode("utf-8")).hexdigest()[:12]

    scene = {
        "time_markers": extract_time_markers(passage_text, moment),
        "verbs": extract_verbs(passage_text, moment),
        "thresholds": extract_thresholds(passage_text, moment),
        "silences": extract_silences(passage_text, moment),
        "camera_moves": infer_camera_moves(passage_text, moment),
    }

    card = {
        "id": card_id,
        "passage": {"ref": passage_ref, "text": passage_text},
        "moment": moment,
        "scene": scene,
        "modal_triad": modal_triad_from_text(passage_text),
        "witness_prompts": witness_prompts_from_text(passage_text, moment),
        "prayer": prayer_from_text(passage_text),
        "safety": {
            "avoidances": ["moralism", "fixing", "certainty claims"],
            "notes": [
                "This is pastoral presence, not diagnosis.",
                "Invite gently; do not pressure outcomes.",
            ],
        },
    }
    return card


def render_markdown(card: dict):
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
    lines.append(f"Time markers: {', '.join(card['scene']['time_markers']) or 'none'}")
    lines.append(f"Verbs: {', '.join(card['scene']['verbs'])}")
    lines.append(f"Thresholds: {', '.join(card['scene']['thresholds']) or 'none'}")
    lines.append(f"Silences: {', '.join(card['scene']['silences']) or 'none'}")
    lines.append(f"Camera moves: {', '.join(card['scene']['camera_moves'])}")
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


def write_outputs(out_dir: Path, card: dict):
    out_dir.mkdir(parents=True, exist_ok=True)

    card_json = json.dumps(card, indent=2, ensure_ascii=True)
    card_path = out_dir / "card.json"
    card_path.write_text(card_json, encoding="utf-8")

    card_md = render_markdown(card)
    (out_dir / "card.md").write_text(card_md, encoding="utf-8")

    card_hash = hashlib.sha256(card_json.encode("utf-8")).hexdigest()
    provenance = {
        "version": "v1",
        "method": "heuristic_v1",
        "inputs": {
            "passage_ref": card["passage"]["ref"],
            "moment": card["moment"],
        },
        "card_sha256": card_hash,
    }
    (out_dir / "provenance.json").write_text(
        json.dumps(provenance, indent=2, ensure_ascii=True), encoding="utf-8"
    )

    (out_dir / "attestation.sha256").write_text(card_hash + "\n", encoding="utf-8")

    log_lines = [
        "witness_card_generator v1",
        f"output_dir={out_dir}",
        "files_written=card.json, card.md, provenance.json, attestation.sha256, log.txt",
    ]
    (out_dir / "log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")


def generate_witness_card(passage: str, textfile: str, moment: str, out: str):
    if textfile:
        passage_text_path = resolve_repo_path(textfile)
        passage_text = passage_text_path.read_text(encoding="utf-8")
        textfile_value = textfile
    else:
        passage_text = SAMPLE_TEXT
        textfile_value = None

    passage_text = normalize_whitespace(passage_text)
    passage_text_sha256 = hashlib.sha256(passage_text.encode("utf-8")).hexdigest()
    generator_bytes = Path(__file__).read_bytes()
    generator_sha256 = hashlib.sha256(generator_bytes).hexdigest()

    card = build_card(passage, passage_text, moment)
    out_dir = Path(out)
    write_outputs(out_dir, card)

    provenance_path = out_dir / "provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance["inputs"]["textfile"] = textfile_value
    provenance["passage_text_sha256"] = passage_text_sha256
    provenance["generator_sha256"] = generator_sha256
    provenance_path.write_text(json.dumps(provenance, indent=2, ensure_ascii=True), encoding="utf-8")

    attestation = (out_dir / "attestation.sha256").read_text(encoding="utf-8").strip()
    return card["id"], attestation


def run_batch(batchfile: str, version: str) -> dict:
    batch_path = Path(batchfile)
    csv_bytes = batch_path.read_bytes()
    batch_id = hashlib.sha256(csv_bytes).hexdigest()[:12]

    summary_dir = Path("outputs") / "witness_cards" / "_batch_runs" / batch_id
    summary_dir.mkdir(parents=True, exist_ok=True)

    results = []
    rows_total = 0
    rows_succeeded = 0
    rows_failed = 0

    with batch_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"passage", "textfile", "moment", "out"}
        if not required.issubset(set(reader.fieldnames or [])):
            missing = sorted(list(required - set(reader.fieldnames or [])))
            raise ValueError(f"batchfile missing required columns: {', '.join(missing)}")

        for row_index, row in enumerate(reader, start=1):
            rows_total += 1
            passage_ref = (row.get("passage") or "").strip()
            textfile = (row.get("textfile") or "").strip()
            moment = (row.get("moment") or "").strip()
            out = (row.get("out") or "").strip()

            try:
                if not passage_ref:
                    raise ValueError("passage is empty")
                if not moment:
                    raise ValueError("moment is empty")
                if not out:
                    raise ValueError("out is empty")

                if version == "v4":
                    card_id, attestation = iv_witness_card_v4.generate_witness_card_v4(
                        passage_ref, textfile or None, moment, out
                    )
                elif version == "v3":
                    card_id, attestation = iv_witness_card_v3.generate_witness_card_v3(
                        passage_ref, textfile or None, moment, out
                    )
                elif version == "v2":
                    card_id, attestation = iv_witness_card_v2.generate_witness_card_v2(
                        passage_ref, textfile or None, moment, out
                    )
                else:
                    card_id, attestation = generate_witness_card(
                        passage_ref, textfile or None, moment, out
                    )

                results.append(
                    {
                        "row_index": row_index,
                        "out": out,
                        "passage": passage_ref,
                        "status": "ok",
                        "card_id": card_id,
                        "attestation": attestation,
                    }
                )
                rows_succeeded += 1
            except Exception as exc:
                results.append(
                    {
                        "row_index": row_index,
                        "out": out,
                        "passage": passage_ref,
                        "status": "error",
                        "error": str(exc),
                    }
                )
                rows_failed += 1

    batch_summary = {
        "batch_id": batch_id,
        "batchfile": str(batchfile).replace("\\", "/"),
        "version": version,
        "rows_total": rows_total,
        "rows_succeeded": rows_succeeded,
        "rows_failed": rows_failed,
        "results": results,
    }

    (summary_dir / "batch_summary.json").write_text(
        json.dumps(batch_summary, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )

    log_lines = []
    for result in results:
        if result["status"] == "ok":
            log_lines.append(
                f"row={result['row_index']} status=ok out={result['out']} card_id={result['card_id']}"
            )
        else:
            log_lines.append(
                f"row={result['row_index']} status=error out={result.get('out','')} "
                f"error={result.get('error','')}"
            )
    (summary_dir / "batch_log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    return batch_summary


def main(argv=None):
    parser = argparse.ArgumentParser(description="Witness Card Generator")
    parser.add_argument("--passage", help="Scripture reference, e.g., John 1:14")
    parser.add_argument("--textfile", help="Path to scripture text file")
    parser.add_argument("--moment", help="2-6 sentence user moment")
    parser.add_argument("--out", help="Output directory")
    parser.add_argument("--batchfile", help="CSV file for batch generation")
    parser.add_argument(
        "--version",
        choices=["v1", "v2", "v3", "v4"],
        default="v1",
        help="Generator version (default: v1)",
    )
    parser.add_argument("--dataset", help="Dataset name for manifest-based loading")
    parser.add_argument("--manifest", help="Path to manifest.json for passage lookup")
    parser.add_argument(
        "--review-mode",
        choices=["none", "template", "ai"],
        default="none",
        help="Optional review.md generation mode (v3 only)",
    )

    args = parser.parse_args(argv)

    if args.batchfile:
        run_batch(args.batchfile, args.version)
        return

    if not args.passage:
        parser.error("--passage is required unless --batchfile is provided")
    if not args.moment:
        parser.error("--moment is required unless --batchfile is provided")
    if not args.out:
        parser.error("--out is required unless --batchfile is provided")

    if args.version == "v4":
        iv_witness_card_v4.generate_witness_card_v4(
            args.passage,
            args.textfile,
            args.moment,
            args.out,
            dataset=args.dataset,
            manifest=args.manifest,
            review_mode=args.review_mode,
        )
    elif args.version == "v3":
        iv_witness_card_v3.generate_witness_card_v3(
            args.passage,
            args.textfile,
            args.moment,
            args.out,
            dataset=args.dataset,
            manifest=args.manifest,
            review_mode=args.review_mode,
        )
    elif args.version == "v2":
        iv_witness_card_v2.generate_witness_card_v2(
            args.passage, args.textfile, args.moment, args.out
        )
    else:
        generate_witness_card(args.passage, args.textfile, args.moment, args.out)


if __name__ == "__main__":
    main()
