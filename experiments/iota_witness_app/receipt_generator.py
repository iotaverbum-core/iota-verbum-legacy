"""
EDEN Attestation Receipt Generator
Produces a human-readable, verifiable PDF receipt for a given entry response.
"""
from __future__ import annotations

import io
from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ── Brand palette ──────────────────────────────────────────────────────────────
INK = colors.HexColor("#111111")
MIST = colors.HexColor("#F5F5F0")
RULE = colors.HexColor("#CCCCCC")
PASS_COLOR = colors.HexColor("#1A6B3A")
FAIL_COLOR = colors.HexColor("#8B1A1A")
ACCENT = colors.HexColor("#444444")

PAGE_W, PAGE_H = A4
MARGIN = 22 * mm


# ── Styles ─────────────────────────────────────────────────────────────────────
def _build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "wordmark": ParagraphStyle(
            "wordmark",
            parent=base["Normal"],
            fontSize=28,
            leading=32,
            textColor=INK,
            fontName="Helvetica-Bold",
            spaceAfter=2,
        ),
        "tagline": ParagraphStyle(
            "tagline",
            parent=base["Normal"],
            fontSize=9,
            leading=12,
            textColor=ACCENT,
            fontName="Helvetica",
            spaceAfter=0,
        ),
        "section_head": ParagraphStyle(
            "section_head",
            parent=base["Normal"],
            fontSize=8,
            leading=10,
            textColor=ACCENT,
            fontName="Helvetica-Bold",
            spaceBefore=14,
            spaceAfter=5,
            textTransform="uppercase",
        ),
        "meta_label": ParagraphStyle(
            "meta_label",
            parent=base["Normal"],
            fontSize=8,
            leading=11,
            textColor=ACCENT,
            fontName="Helvetica",
        ),
        "meta_value": ParagraphStyle(
            "meta_value",
            parent=base["Normal"],
            fontSize=9,
            leading=12,
            textColor=INK,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontSize=10,
            leading=15,
            textColor=INK,
            fontName="Helvetica",
        ),
        "response_text": ParagraphStyle(
            "response_text",
            parent=base["Normal"],
            fontSize=11,
            leading=17,
            textColor=INK,
            fontName="Helvetica",
            leftIndent=6,
            borderPad=8,
        ),
        "rule_pass": ParagraphStyle(
            "rule_pass",
            parent=base["Normal"],
            fontSize=9,
            leading=13,
            textColor=PASS_COLOR,
            fontName="Helvetica",
        ),
        "rule_fail": ParagraphStyle(
            "rule_fail",
            parent=base["Normal"],
            fontSize=9,
            leading=13,
            textColor=FAIL_COLOR,
            fontName="Helvetica",
        ),
        "hash": ParagraphStyle(
            "hash",
            parent=base["Normal"],
            fontSize=7,
            leading=10,
            textColor=ACCENT,
            fontName="Courier",
            wordWrap="CJK",
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontSize=7,
            leading=10,
            textColor=ACCENT,
            fontName="Helvetica",
        ),
        "disclaimer": ParagraphStyle(
            "disclaimer",
            parent=base["Normal"],
            fontSize=8,
            leading=12,
            textColor=ACCENT,
            fontName="Helvetica-Oblique",
        ),
    }


# ── Plain-language rule descriptions ──────────────────────────────────────────
RULE_LABELS: dict[str, str] = {
    "HR1": "No false divine authority claims",
    "HR2": "Christ-centred grounding present",
    "HR3": "Exactly one hinge action",
    "HR4": "Entrustment language present",
    "HR5": "Word and line limits observed",
    "HR6": "No shame-weighting language",
}


def _rule_symbol(passed: bool) -> str:
    return "\u2713" if passed else "\u2717"


# ── Main generator ─────────────────────────────────────────────────────────────
def generate_receipt(
    *,
    entry_kind: str,                      # "season" | "moment"
    eden_text: str,
    modal: dict[str, Any],
    attestation: dict[str, Any],
    local_mode: bool,
    crisis_flag: bool,
    created_at: datetime,
    entry_id: str,
    include_original_text: bool = False,
    original_text: str | None = None,
) -> bytes:
    """Return PDF bytes for an attestation receipt."""

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title="EDEN Attestation Receipt",
        author="EDEN Witness Companion",
    )

    S = _build_styles()
    story = []

    # ── Header ────────────────────────────────────────────────────────────────
    story.append(Paragraph("\u25a1 \u25c7 \u2192 \u0394", S["wordmark"]))
    story.append(Paragraph("EDEN Witness Companion &mdash; Attestation Receipt", S["tagline"]))
    story.append(Spacer(1, 4 * mm))
    story.append(HRFlowable(width="100%", thickness=1, color=INK, spaceAfter=4 * mm))

    # ── Meta block ────────────────────────────────────────────────────────────
    kind_display = entry_kind.capitalize()
    mode_display = "Crisis response" if crisis_flag else ("Local (no AI)" if local_mode else "AI-assisted")
    date_display = created_at.strftime("%-d %B %Y, %H:%M UTC") if hasattr(created_at, "strftime") else str(created_at)

    meta_data = [
        ["Entry type", kind_display],
        ["Date", date_display],
        ["Mode", mode_display],
        ["Entry ID", entry_id],
    ]

    meta_table = Table(
        [[Paragraph(label, S["meta_label"]), Paragraph(value, S["meta_value"])]
         for label, value in meta_data],
        colWidths=[35 * mm, None],
        hAlign="LEFT",
    )
    meta_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(meta_table)

    # ── Original text (opt-in) ────────────────────────────────────────────────
    if include_original_text and original_text:
        story.append(Paragraph("Your entry", S["section_head"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=3 * mm))
        story.append(Paragraph(original_text.replace("\n", "<br/>"), S["body"]))

    # ── EDEN response ─────────────────────────────────────────────────────────
    story.append(Paragraph("EDEN response", S["section_head"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=3 * mm))

    # Shaded background box via single-cell table
    response_table = Table(
        [[Paragraph(eden_text.replace("\n\n", "<br/><br/>").replace("\n", "<br/>"), S["response_text"])]],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    response_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MIST),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(response_table)

    # ── Distortion reading ────────────────────────────────────────────────────
    dominant = modal.get("dominant_distortion", "—")
    velocity = modal.get("velocity_score", 0.0)
    union = modal.get("union_score", 0.0)

    story.append(Paragraph("Modal reading", S["section_head"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=3 * mm))

    modal_data = [
        ["Dominant pattern", dominant.capitalize()],
        ["Velocity (urgency)", f"{velocity:.2f} / 1.00"],
        ["Union score", f"{union:.2f} / 1.00"],
    ]
    modal_table = Table(
        [[Paragraph(label, S["meta_label"]), Paragraph(value, S["meta_value"])]
         for label, value in modal_data],
        colWidths=[45 * mm, None],
        hAlign="LEFT",
    )
    modal_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(modal_table)

    # ── Guardrail rules ───────────────────────────────────────────────────────
    story.append(Paragraph("Guardrail checks", S["section_head"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=3 * mm))

    rules = attestation.get("rules", [])
    for rule in rules:
        name = rule.get("rule", "")
        passed = bool(rule.get("passed", False))
        label = RULE_LABELS.get(name, name)
        symbol = _rule_symbol(passed)
        style = S["rule_pass"] if passed else S["rule_fail"]
        story.append(Paragraph(f"{symbol}  {label}", style))

    if not rules:
        story.append(Paragraph("No rule data available.", S["body"]))

    # ── Tamper-evident hashes ─────────────────────────────────────────────────
    hashes = attestation.get("hashes", {})
    if hashes:
        story.append(Paragraph("Verification hashes", S["section_head"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=3 * mm))
        story.append(Paragraph(
            "These hashes verify that the response above has not been altered after generation. "
            "A spiritual director or counsellor may record the final hash as a log reference.",
            S["body"]
        ))
        story.append(Spacer(1, 3 * mm))

        hash_labels = {
            "entry_sha256": "Entry text hash",
            "analysis_sha256": "Modal analysis hash",
            "draft_sha256": "Draft hash",
            "final_sha256": "Final response hash",
            "rules_sha256": "Rules hash",
        }
        for key, label in hash_labels.items():
            value = hashes.get(key, "—")
            story.append(Paragraph(f"<b>{label}</b>", S["meta_label"]))
            story.append(Paragraph(value, S["hash"]))
            story.append(Spacer(1, 2 * mm))

        ts = hashes.get("timestamp", "—")
        story.append(Paragraph(f"Attested at: {ts}", S["footer"]))

    # ── Disclaimer ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 6 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=3 * mm))
    story.append(Paragraph(
        "EDEN is a spiritual companion and is not therapy, medical care, or crisis care. "
        "This receipt documents what was generated and the rules it was held to. "
        "It does not constitute clinical or pastoral advice.",
        S["disclaimer"]
    ))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        "edenwitness.app \u00b7 support@edenwitness.app",
        S["footer"]
    ))

    doc.build(story)
    buf.seek(0)
    return buf.read()
