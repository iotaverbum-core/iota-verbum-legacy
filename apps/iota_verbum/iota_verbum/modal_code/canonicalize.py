from __future__ import annotations

from .parser import parse_modal_code
from .render import render_document


def canonicalize_text(text: str) -> str:
    doc = parse_modal_code(text)
    return render_document(doc)
