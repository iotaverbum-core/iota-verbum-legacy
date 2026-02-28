#!/usr/bin/env python
"""
ivb_attest.py
────────────────────────────────────────────────────
Iota Verbum – Interpretation Attestation Engine v0.1

Given:
  - an IV id (e.g. IV.MRK.04.26-04.29.GROWING_SEED)
  - an interpretation (summary + claims)
this script produces a structured JSON attestation:

  - ties the interpretation to the IVB modal Bible (IV ref + arc)
  - runs SOMB’s creed + modal checks
  - returns a "sound / drift-risk / rejected / unknown" status

Usage (from repo root):

  python ivb_attest.py \
      --iv-id IV.MRK.04.26-04.29.GROWING_SEED \
      --author "Matthew Neal" \
      --role "preacher_draft" \
      --summary "Jesus, the crucified Sower, entrusts kingdom growth to the Father until final harvest." \
      --claim "Jesus is the divine Sower who owns the field of history." \
      --claim "The kingdom grows invisibly but infallibly to a final eschatological harvest."

"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml  # requires PyYAML

# Import SOMB logic (lexicon + creed + scoring)
from somb_core import SOMBCore, LEX, CREED  # type: ignore


BASE = Path(__file__).parent
IV_SEED_PATH = BASE / "iota_verbum_core" / "iv" / "data" / "mark_iv_seed.yaml"


# ────────────────────────────── DATA CLASSES ────────────────────────────────

@dataclass
class IVRef:
    iv_id: str
    book_code: str
    pericope_id: str


@dataclass
class TextualBasis:
    base_text_id: str
    variant_profile_id: str
    textual_confidence: float


@dataclass
class ModalBasis:
    box: str
    diamond: str
    delta: str
    interpretive_confidence: float


@dataclass
class AuthorInfo:
    name: str
    role: str


@dataclass
class InterpretationInfo:
    author: AuthorInfo
    summary: str
    claims: List[str]


@dataclass
class CreedAlignment:
    status: str  # "pass" | "fail" | "unknown"
    notes: str


@dataclass
class CanonicalAlignment:
    status: str  # "coherent" | "drift-risk" | "contradiction" | "unknown"
    primary_arcs: List[str]
    notes: str


@dataclass
class ModalEthicsAlignment:
    status: str  # "coherent" | "drift-risk" | "contradiction" | "unknown"
    score: int
    notes: str


@dataclass
class Checks:
    creed_alignment: CreedAlignment
    canonical_alignment: CanonicalAlignment
    modal_ethics: ModalEthicsAlignment


@dataclass
class InterpretationAttestation:
    attestation_id: str
    timestamp: str
    iv_ref: IVRef
    textual_basis: TextualBasis
    modal_basis: ModalBasis
    interpretation: InterpretationInfo
    checks: Checks
    status: str  # "sound" | "drift-risk" | "rejected" | "unknown"


# ────────────────────────────── HELPERS ─────────────────────────────────────

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mk_attestation_id(iv_id: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    safe_iv = re.sub(r"[^A-Z0-9]+", ".", iv_id.upper())
    return f"INTA.{safe_iv}.{ts}"


def load_iv_seed() -> Dict[str, Dict[str, Any]]:
    """
    Load mark_iv_seed.yaml and index by iv_id.
    """
    if not IV_SEED_PATH.exists():
        raise FileNotFoundError(f"IV seed file not found at {IV_SEED_PATH}")

    with IV_SEED_PATH.open("r", encoding="utf-8-sig") as f:
        data = yaml.safe_load(f) or []

    index: Dict[str, Dict[str, Any]] = {}
    for entry in data:
        iv_id = entry.get("iv_id")
        if not iv_id:
            continue
        index[iv_id] = entry
    return index


def build_iv_ref(iv_entry: Dict[str, Any]) -> IVRef:
    return IVRef(
        iv_id=iv_entry["iv_id"],
        book_code=iv_entry.get("book_code", ""),
        pericope_id=iv_entry.get("pericope_id", "")
    )


def build_textual_basis(iv_entry: Dict[str, Any]) -> TextualBasis:
    # For now, we use simple placeholders for base_text_id & variant_profile_id.
    # You can later wire this into your full IVB text layer.
    textual_conf = float(iv_entry.get("textual_confidence", 0.0) or 0.0)
    return TextualBasis(
        base_text_id=iv_entry.get("base_text_id", "NA28_MRK"),
        variant_profile_id=iv_entry.get("variant_profile_id", "DEFAULT"),
        textual_confidence=textual_conf
    )


def build_modal_basis(iv_entry: Dict[str, Any]) -> ModalBasis:
    modal = iv_entry.get("modal", {}) or {}
    box = modal.get("box", {}).get("label", "")
    diamond = modal.get("diamond", {}).get("label", "")
    delta = modal.get("delta", {}).get("label", "")
    inter_conf = float(iv_entry.get("interpretive_confidence", 0.0) or 0.0)
    return ModalBasis(
        box=box,
        diamond=diamond,
        delta=delta,
        interpretive_confidence=inter_conf
    )


def run_creed_alignment(text: str, somb: SOMBCore) -> CreedAlignment:
    creed = somb.creed_filter(text)
    if creed.nicene_dissonance:
        status = "fail"
        notes = f"Dissonance: {', '.join(creed.nicene_dissonance)}."
    elif creed.nicene_affirmations:
        status = "pass"
        notes = f"Anchors: {', '.join(creed.nicene_affirmations)}."
    else:
        status = "unknown"
        notes = "No explicit Nicene anchors or dissonances detected."
    return CreedAlignment(status=status, notes=notes)


def run_canonical_alignment(iv_entry: Dict[str, Any], claims: List[str]) -> CanonicalAlignment:
    """
    v0.1:
      - we simply surface the primary_arc_id and do a light heuristic check.
      - you can later plug this into full canonical arc logic.
    """
    primary_arc = iv_entry.get("primary_arc_id")
    arcs = [primary_arc] if primary_arc else []
    notes_parts: List[str] = []

    # VERY light heuristic example: if claims explicitly deny an arc keyword, flag drift-risk.
    status = "coherent"
    lowered = " ".join(claims).lower()

    if primary_arc and "kingdom" in primary_arc.lower():
        if "purely internal" in lowered or "not eschatological" in lowered:
            status = "drift-risk"
            notes_parts.append("Claim underplays eschatological horizon of kingdom arc.")

    if not primary_arc:
        status = "unknown"
        notes_parts.append("No primary_arc_id present in IV; canonical check limited.")

    notes = " ".join(notes_parts) if notes_parts else "Canonical check based on primary_arc_id only (v0.1)."
    return CanonicalAlignment(status=status, primary_arcs=arcs, notes=notes)


def run_modal_ethics(text: str, somb: SOMBCore) -> ModalEthicsAlignment:
    mp = somb.interpret(text)
    sc = mp.scorecard
    # Simple rule: score >= 70 and modal_ok = coherent; else drift-risk
    if mp.modal_ok and sc.score >= 70:
        status = "coherent"
        notes = "Modal pattern and creed alignment above threshold."
    elif sc.score >= 40:
        status = "drift-risk"
        notes = "Partial modal structure detected; see risks for refinement."
    else:
        status = "contradiction"
        notes = "Modal pattern significantly deficient or creed dissonances present."

    # We pack SOMB risks into the notes for now (you can expose them separately later)
    if sc.risks:
        notes += " Risks: " + "; ".join(sc.risks)
    return ModalEthicsAlignment(status=status, score=sc.score, notes=notes)


def overall_status(creed: CreedAlignment, canon: CanonicalAlignment, modal: ModalEthicsAlignment) -> str:
    if creed.status == "fail" or modal.status == "contradiction":
        return "rejected"
    if creed.status == "pass" and modal.status == "coherent" and canon.status in ("coherent", "unknown"):
        return "sound"
    if creed.status in ("unknown", "pass") and modal.status in ("coherent", "drift-risk"):
        return "drift-risk"
    return "unknown"


def attest_interpretation(
    iv_id: str,
    author_name: str,
    author_role: str,
    summary: str,
    claims: List[str]
) -> InterpretationAttestation:
    iv_index = load_iv_seed()
    if iv_id not in iv_index:
        raise KeyError(f"IV id not found in seed file: {iv_id}")

    iv_entry = iv_index[iv_id]

    iv_ref = build_iv_ref(iv_entry)
    textual_basis = build_textual_basis(iv_entry)
    modal_basis = build_modal_basis(iv_entry)

    author = AuthorInfo(name=author_name, role=author_role)
    interp = InterpretationInfo(author=author, summary=summary, claims=claims)

    # For SOMB checks we combine summary + claims into one text block
    text_block = summary + "\n" + "\n".join(claims)
    somb = SOMBCore(LEX, CREED)

    creed_al = run_creed_alignment(text_block, somb)
    canon_al = run_canonical_alignment(iv_entry, claims)
    modal_al = run_modal_ethics(text_block, somb)

    checks = Checks(
        creed_alignment=creed_al,
        canonical_alignment=canon_al,
        modal_ethics=modal_al
    )

    status = overall_status(creed_al, canon_al, modal_al)

    att = InterpretationAttestation(
        attestation_id=_mk_attestation_id(iv_id),
        timestamp=_now_iso(),
        iv_ref=iv_ref,
        textual_basis=textual_basis,
        modal_basis=modal_basis,
        interpretation=interp,
        checks=checks,
        status=status
    )
    return att


# ────────────────────────────── CLI ─────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Iota Verbum – Interpretation Attestation (IVB + SOMB)."
    )
    p.add_argument("--iv-id", required=True, help="IV id (e.g. IV.MRK.04.26-04.29.GROWING_SEED)")
    p.add_argument("--author", required=True, help="Author name")
    p.add_argument("--role", required=True, help="Author role (e.g. preacher_draft, commentary, ai_agent)")
    p.add_argument("--summary", required=True, help="Short summary of the interpretation")
    p.add_argument(
        "--claim",
        action="append",
        dest="claims",
        default=[],
        help="Discrete doctrinal/practical claim (can be passed multiple times)"
    )
    p.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output"
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    att = attest_interpretation(
        iv_id=args.iv_id,
        author_name=args.author,
        author_role=args.role,
        summary=args.summary,
        claims=args.claims or []
    )
    payload = asdict(att)
    if args.pretty:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(payload, separators=(",", ":"), ensure_ascii=False))


if __name__ == "__main__":
    main()
