from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import (
    Book,
    Unit,
    Token,
    Pericope,
    IVPair,
    IVPairUnit,
    CanonicalArc,
    VariantSite,
    Variant,
    VariantSupport,
    Witness,
)

router = APIRouter(prefix="/ivb", tags=["ivb"])


def _pericope_intersects_chapter(pericope: Pericope, chapter_units: List[Unit]) -> bool:
    if not chapter_units:
        return False
    chapter_unit_ids = [u.unit_id for u in chapter_units]
    chapter_min = min(chapter_unit_ids)
    chapter_max = max(chapter_unit_ids)
    return not (pericope.end_unit_id < chapter_min or pericope.start_unit_id > chapter_max)


@router.get("/chapter")
def get_ivb_chapter(
    book_code: str = Query(..., example="MRK"),
    chapter: int = Query(..., ge=1, example=4),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    book: Optional[Book] = db.get(Book, book_code)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    units: List[Unit] = (
        db.query(Unit)
        .filter(Unit.book_code == book_code, Unit.chapter == chapter)
        .order_by(Unit.verse, Unit.sub_id)
        .all()
    )
    if not units:
        raise HTTPException(status_code=404, detail="No units for chapter")

    unit_ids = [u.unit_id for u in units]

    tokens: List[Token] = (
        db.query(Token)
        .filter(Token.unit_id.in_(unit_ids))
        .order_by(Token.unit_id, Token.position)
        .all()
    )
    token_map: Dict[str, List[Token]] = {uid: [] for uid in unit_ids}
    for t in tokens:
        token_map.setdefault(t.unit_id, []).append(t)

    ivb_units: List[Dict[str, Any]] = []
    for u in units:
        ivb_units.append(
            {
                "unit_id": u.unit_id,
                "unit_type": u.unit_type,
                "text_ref": f"{book.name_en} {u.chapter}:{u.verse}",
                "tokens": [
                    {
                        "position": t.position,
                        "surface": t.surface,
                        "lemma_id": t.lemma_id,
                        "morph_code": t.morph_code,
                        "strongs": t.strongs,
                    }
                    for t in token_map.get(u.unit_id, [])
                ],
            }
        )

    pericopes: List[Pericope] = (
        db.query(Pericope).filter(Pericope.book_code == book_code).all()
    )
    ivb_pericopes: List[Dict[str, Any]] = []
    pericope_ids: List[str] = []
    for p in pericopes:
        if _pericope_intersects_chapter(p, units):
            ivb_pericopes.append(
                {
                    "pericope_id": p.pericope_id,
                    "start_unit_id": p.start_unit_id,
                    "end_unit_id": p.end_unit_id,
                    "title_en": p.title_en,
                    "title_iota": p.title_iota,
                    "genre": p.genre,
                }
            )
            pericope_ids.append(p.pericope_id)

    iv_pairs: List[IVPair] = (
        db.query(IVPair)
        .filter(IVPair.book_code == book_code, IVPair.pericope_id.in_(pericope_ids))
        .all()
    )
    iv_ids = [iv.iv_id for iv in iv_pairs]

    iv_units: List[IVPairUnit] = (
        db.query(IVPairUnit).filter(IVPairUnit.iv_id.in_(iv_ids)).all()
    )
    iv_unit_map: Dict[str, List[str]] = {iv_id: [] for iv_id in iv_ids}
    for link in iv_units:
        iv_unit_map.setdefault(link.iv_id, []).append(link.unit_id)

    arc_ids = [iv.primary_arc_id for iv in iv_pairs if iv.primary_arc_id]
    arcs: List[CanonicalArc] = []
    arc_map: Dict[str, CanonicalArc] = {}
    if arc_ids:
        arcs = (
            db.query(CanonicalArc)
            .filter(CanonicalArc.arc_id.in_(arc_ids))
            .all()
        )
        arc_map = {a.arc_id: a for a in arcs}

    ivb_modals: List[Dict[str, Any]] = []
    for iv in iv_pairs:
        ivb_modals.append(
            {
                "iv_id": iv.iv_id,
                "scope": iv.scope,
                "pericope_id": iv.pericope_id,
                "unit_ids": iv_unit_map.get(iv.iv_id, []),
                "primary_arc_id": iv.primary_arc_id,
                "modal": {
                    "box": {
                        "label": iv.box_label,
                        "description": iv.box_description,
                    },
                    "diamond": {
                        "label": iv.diamond_label,
                        "description": iv.diamond_description,
                    },
                    "delta": {
                        "label": iv.delta_label,
                        "description": iv.delta_description,
                    },
                },
                "confidence": {
                    "textual": iv.textual_confidence,
                    "interpretive": iv.interpretive_confidence,
                },
                "summary": iv.summary,
            }
        )

    # Variants stub: we define empty list for now
    ivb_variants: List[Dict[str, Any]] = []

    ivb_arcs: List[Dict[str, Any]] = []
    for arc_id, arc in arc_map.items():
        ivb_arcs.append(
            {
                "arc_id": arc.arc_id,
                "label": arc.label,
                "description": arc.description,
                "links": arc.links,
            }
        )

    ivb_doc = {
        "ivb_version": "1.0",
        "doc_id": f"IVB.{book_code}.{chapter:02d}",
        "meta": {
            "book_code": book_code,
            "chapter": chapter,
            "language": book.language,
            "book_name_en": book.name_en,
            "base_text_source": "DEMO_TSV",
            "morph_source": "DEMO_TSV",
            "generated_by": "iota_verbum",
            "generated_at": datetime.utcnow().isoformat() + "Z",
        },
        "units": ivb_units,
        "pericopes": ivb_pericopes,
        "modals": ivb_modals,
        "variants": ivb_variants,
        "arcs": ivb_arcs,
    }

    return ivb_doc
