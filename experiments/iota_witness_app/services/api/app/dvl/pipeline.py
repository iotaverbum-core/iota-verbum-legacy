from __future__ import annotations

import re
from typing import Any

from app.dvl.attest import attest
from app.dvl.repair import render_final_text, repair_segments
from app.dvl.rules import validate_rules
from app.llm.openai_client import generate_draft
from app.modal.analyze import analyze_modal
from app.safety.crisis import crisis_response, has_crisis_language

SEGMENT_RE = re.compile(r"\[\[(G|R|D|H|E)\]\]\s*(.*?)(?=\n\[\[(?:G|R|D|H|E)\]\]|\Z)", re.DOTALL)


def parse_segments(text: str) -> dict[str, str]:
    found = {tag: body.strip() for tag, body in SEGMENT_RE.findall(text)}
    return {k: found.get(k, "") for k in ["G", "R", "D", "H", "E"]}


def _local_mode_draft(modal: dict[str, Any], moment_mode: bool = False) -> str:
    distortion = modal.get("dominant_distortion", "fear")
    reflect = "Name what happened in one plain sentence."
    if moment_mode:
        reflect = "Name what happened in one plain sentence. Keep it brief."
    return (
        "[[G]] Jesus is near in this moment.\n"
        f"[[R]] {reflect}\n"
        f"[[D]] You are leaning toward {distortion}.\n"
        "[[H]] Take one steady breath and do one faithful next step.\n"
        "[[E]] Leave the outcome with the Lord."
    )


def _crisis_mode_draft() -> str:
    return (
        "[[G]] Jesus sees you right now.\n"
        "[[R]] Pause and seek immediate in-person support.\n"
        "[[D]] This is a crisis moment.\n"
        "[[H]] Contact local emergency services now if you may act on self-harm thoughts.\n"
        "[[E]] Leave the outcome with the Lord."
    )


def process_entry(
    entry_text: str,
    moment_mode: bool = False,
    ai_consent: bool = False,
    local_only: bool = False,
) -> dict[str, Any]:
    analysis = analyze_modal(entry_text)
    crisis_flag = has_crisis_language(entry_text)
    use_llm = ai_consent and (not local_only) and (not crisis_flag)

    if crisis_flag:
        draft = _crisis_mode_draft()
    elif not use_llm:
        draft = _local_mode_draft(analysis, moment_mode=moment_mode)
    else:
        draft = generate_draft(
            entry_text=entry_text,
            modal=analysis,
            moment_mode=moment_mode,
            use_llm=True,
        )
    segments = parse_segments(draft)
    repaired_segments = repair_segments(segments=segments, modal=analysis, moment_mode=moment_mode)
    if crisis_flag:
        final_text = crisis_response()
    else:
        final_text = render_final_text(repaired_segments)

    words = final_text.split()
    cap = 120 if moment_mode else 200
    final_text = " ".join(words[:cap]).strip()

    rules = validate_rules(repaired_segments, final_text)
    rule_results = [{"rule": rr.name, "passed": rr.passed, "reason": rr.reason} for rr in rules]

    attestation = attest(
        entry_text=entry_text,
        analysis=analysis,
        draft=draft,
        final_text=final_text,
        rule_results=rule_results,
    )

    return {
        "modal": analysis,
        "eden_text": final_text,
        "hinge_action": repaired_segments.get("H", ""),
        "local_mode": not use_llm,
        "crisis_flag": crisis_flag,
        "attestation": {
            "hashes": attestation,
            "rules": rule_results,
        },
        "draft": draft,
    }
