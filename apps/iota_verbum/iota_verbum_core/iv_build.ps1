# iv_build.ps1
# One-shot builder for a tiny Iota Verbum pilot (Mark 4).
# Run from inside the iota_verbum_core folder:  .\iv_build.ps1

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

Write-Host "=== Iota Verbum Pilot Build ==="

# 1. Ensure folder structure
$dirs = @(
  "$root\app",
  "$root\app\routers",
  "$root\corpus",
  "$root\corpus\data",
  "$root\corpus\data\raw",
  "$root\corpus\data\processed",
  "$root\iv",
  "$root\iv\data",
  "$root\build_output"
)
foreach ($d in $dirs) {
  if (-not (Test-Path $d)) {
    New-Item -ItemType Directory -Path $d | Out-Null
  }
}

# 2. Python environment
if (-not (Test-Path "$root\venv")) {
  Write-Host "Creating virtual environment..."
  python -m venv "$root\venv"
}
Write-Host "Activating virtual environment..."
& "$root\venv\Scripts\Activate.ps1"

Write-Host "Installing Python packages..."
pip install --upgrade pip | Out-Null
pip install fastapi uvicorn sqlalchemy pydantic pyyaml "uvicorn[standard]" | Out-Null

# 3. FILE CONTENTS (here-strings)

# app\__init__.py
$appInit = @'
# app package init
'@

# app\db.py
$appDb = @'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./iv_core.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'@

# app\models.py
$appModels = @'
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class Book(Base):
    __tablename__ = "books"
    book_code = Column(String, primary_key=True)
    canon_pos = Column(Integer)
    name_en = Column(String)
    language = Column(String)
    testament = Column(String)


class Unit(Base):
    __tablename__ = "units"
    unit_id = Column(String, primary_key=True)
    book_code = Column(String, ForeignKey("books.book_code"))
    chapter = Column(Integer)
    verse = Column(Integer)
    sub_id = Column(String, nullable=True)
    unit_type = Column(String)
    base_ref = Column(String, nullable=True)
    canonical_label = Column(String, nullable=True)
    book = relationship("Book", backref="units")


class Token(Base):
    __tablename__ = "tokens"
    token_id = Column(String, primary_key=True)
    unit_id = Column(String, ForeignKey("units.unit_id"))
    position = Column(Integer)
    surface = Column(String)
    normalized = Column(String)
    lemma_id = Column(String)
    lemma_gloss_en = Column(String, nullable=True)
    morph_code = Column(String)
    pos = Column(String, nullable=True)
    strongs = Column(String, nullable=True)
    unit = relationship("Unit", backref="tokens")


class Pericope(Base):
    __tablename__ = "pericopes"
    pericope_id = Column(String, primary_key=True)
    book_code = Column(String, ForeignKey("books.book_code"))
    start_unit_id = Column(String)
    end_unit_id = Column(String)
    title_en = Column(String)
    title_iota = Column(String)
    genre = Column(String)
    book = relationship("Book", backref="pericopes")


class Witness(Base):
    __tablename__ = "witnesses"
    witness_id = Column(String, primary_key=True)
    siglum = Column(String, unique=True, index=True)
    description = Column(String)
    family = Column(String, nullable=True)


class VariantSite(Base):
    __tablename__ = "variant_sites"
    site_id = Column(String, primary_key=True)
    unit_id = Column(String, ForeignKey("units.unit_id"))
    position_hint = Column(String, nullable=True)
    note = Column(String, nullable=True)
    unit = relationship("Unit", backref="variant_sites")


class Variant(Base):
    __tablename__ = "variants"
    variant_id = Column(String, primary_key=True)
    site_id = Column(String, ForeignKey("variant_sites.site_id"))
    reading_key = Column(String)
    reading_text = Column(Text)
    relation = Column(String, nullable=True)
    site = relationship("VariantSite", backref="variants")


class VariantSupport(Base):
    __tablename__ = "variant_support"
    id = Column(Integer, primary_key=True, autoincrement=True)
    variant_id = Column(String, ForeignKey("variants.variant_id"))
    witness_id = Column(String, ForeignKey("witnesses.witness_id"))
    support_level = Column(String)
    weight = Column(Float)
    variant = relationship("Variant", backref="support")
    witness = relationship("Witness")


class IVPair(Base):
    __tablename__ = "iv_pairs"
    iv_id = Column(String, primary_key=True)
    book_code = Column(String, ForeignKey("books.book_code"))
    scope = Column(String)
    pericope_id = Column(String, ForeignKey("pericopes.pericope_id"), nullable=True)
    primary_arc_id = Column(String, nullable=True)
    box_label = Column(String)
    box_description = Column(Text)
    diamond_label = Column(String)
    diamond_description = Column(Text)
    delta_label = Column(String)
    delta_description = Column(Text)
    textual_confidence = Column(Float, nullable=True)
    interpretive_confidence = Column(Float, nullable=True)
    summary = Column(Text, nullable=True)


class IVPairUnit(Base):
    __tablename__ = "iv_pair_units"
    id = Column(Integer, primary_key=True, autoincrement=True)
    iv_id = Column(String, ForeignKey("iv_pairs.iv_id"))
    unit_id = Column(String, ForeignKey("units.unit_id"))


class CanonicalArc(Base):
    __tablename__ = "canonical_arcs"
    arc_id = Column(String, primary_key=True)
    label = Column(String)
    description = Column(Text)
    links = Column(Text)  # simple JSON string of references
'@

# app\routers\__init__.py
$appRoutersInit = @'
# routers package init
'@

# app\routers\ivb.py
$appRouterIvb = @'
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
'@

# app\main.py
$appMain = @'
from fastapi import FastAPI
from .db import engine, Base
from . import models  # noqa: F401
from .routers import ivb

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Iota Verbum Pilot")

app.include_router(ivb.router)


@app.get("/")
def root():
    return {"message": "Iota Verbum pilot running"}
'@

# app\init_db.py
$appInitDb = @'
from .db import engine, Base
from . import models  # noqa: F401

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
'@

# corpus\__init__.py
$corpusInit = @'
# corpus package init
'@

# corpus\config.py
$corpusConfig = @'
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

BOOK_CODE = "MRK"

MARK_BASE_FILE = DATA_RAW / "mark_base.txt"
MARK_MORPH_FILE = DATA_RAW / "mark_morph.txt"

MARK_UNITS_FILE = DATA_PROCESSED / "mark_units.jsonl"
MARK_TOKENS_FILE = DATA_PROCESSED / "mark_tokens.jsonl"
MARK_PERICOPES_FILE = DATA_PROCESSED / "mark_pericopes.jsonl"
'@

# corpus\etl_mark.py
$corpusEtl = @'
import json
from pathlib import Path
from typing import List, Dict

from .config import (
    BOOK_CODE,
    MARK_BASE_FILE,
    MARK_MORPH_FILE,
    MARK_UNITS_FILE,
    MARK_TOKENS_FILE,
    MARK_PERICOPES_FILE,
)


def parse_base_text(path: Path = MARK_BASE_FILE) -> List[dict]:
    verses: List[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            chapter_s, verse_s, text = line.split("\t", maxsplit=2)
            verses.append(
                {
                    "chapter": int(chapter_s),
                    "verse": int(verse_s),
                    "text": text,
                }
            )
    return verses


def parse_morph(path: Path = MARK_MORPH_FILE) -> Dict[tuple, List[dict]]:
    result: Dict[tuple, List[dict]] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            chapter = int(fields[0])
            verse = int(fields[1])
            position = int(fields[2])
            surface = fields[3]
            lemma_id = fields[4]
            morph_code = fields[5]
            pos = fields[6] if len(fields) > 6 and fields[6] else None
            strongs = fields[7] if len(fields) > 7 and fields[7] else None
            key = (chapter, verse)
            result.setdefault(key, []).append(
                {
                    "chapter": chapter,
                    "verse": verse,
                    "position": position,
                    "surface": surface,
                    "lemma_id": lemma_id,
                    "morph_code": morph_code,
                    "pos": pos,
                    "strongs": strongs,
                }
            )
    return result


def build_units_jsonl(verses: List[dict], out_path: Path = MARK_UNITS_FILE) -> None:
    with open(out_path, "w", encoding="utf-8") as out:
        for v in verses:
            unit_id = f"{BOOK_CODE}.{v['chapter']:02d}.{v['verse']:02d}"
            obj = {
                "unit_id": unit_id,
                "book_code": BOOK_CODE,
                "chapter": v["chapter"],
                "verse": v["verse"],
                "sub_id": None,
                "unit_type": "verse",
                "base_ref": unit_id.replace(".", ""),
                "canonical_label": f"Mark {v['chapter']}:{v['verse']}",
            }
            out.write(json.dumps(obj, ensure_ascii=False) + "\n")


def build_tokens_jsonl(
    morph_index: Dict[tuple, List[dict]], out_path: Path = MARK_TOKENS_FILE
) -> None:
    with open(out_path, "w", encoding="utf-8") as out:
        for (chapter, verse), tokens in sorted(morph_index.items()):
            unit_id = f"{BOOK_CODE}.{chapter:02d}.{verse:02d}"
            for t in tokens:
                token_id = f"{unit_id}.t{t['position']:02d}"
                obj = {
                    "token_id": token_id,
                    "unit_id": unit_id,
                    "position": t["position"],
                    "surface": t["surface"],
                    "normalized": t["surface"],
                    "lemma_id": t["lemma_id"],
                    "lemma_gloss_en": None,
                    "morph_code": t["morph_code"],
                    "pos": t["pos"],
                    "strongs": t["strongs"],
                }
                out.write(json.dumps(obj, ensure_ascii=False) + "\n")


def build_pericopes_jsonl(out_path: Path = MARK_PERICOPES_FILE) -> None:
    seed_pericopes = [
        {
            "pericope_id": "MRK.04.26-04.29.GROWING_SEED",
            "start_unit_id": "MRK.04.26",
            "end_unit_id": "MRK.04.29",
            "title_en": "Parable of the Growing Seed",
            "title_iota": "Δ-Seed-Grows-To-Ripeness",
            "genre": "parable",
        }
    ]
    with open(out_path, "w", encoding="utf-8") as out:
        for p in seed_pericopes:
            obj = {
                **p,
                "book_code": BOOK_CODE,
            }
            out.write(json.dumps(obj, ensure_ascii=False) + "\n")


def run_mark_etl() -> None:
    verses = parse_base_text()
    morph_index = parse_morph()
    build_units_jsonl(verses)
    build_tokens_jsonl(morph_index)
    build_pericopes_jsonl()


if __name__ == "__main__":
    run_mark_etl()
'@

# corpus\db_loader.py
$corpusDbLoader = @'
import json
from pathlib import Path
from typing import Iterable

from sqlalchemy.orm import Session

from .config import (
    BOOK_CODE,
    MARK_UNITS_FILE,
    MARK_TOKENS_FILE,
    MARK_PERICOPES_FILE,
)
from app.db import SessionLocal
from app.models import Book, Unit, Token, Pericope


def load_jsonl(path: Path) -> Iterable[dict]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def ensure_book(session: Session) -> None:
    if not session.get(Book, BOOK_CODE):
        session.add(
            Book(
                book_code=BOOK_CODE,
                canon_pos=41,
                name_en="Mark",
                language="grc",
                testament="NT",
            )
        )


def load_units(session: Session, path: Path = MARK_UNITS_FILE) -> None:
    for obj in load_jsonl(path):
        if not session.get(Unit, obj["unit_id"]):
            session.add(Unit(**obj))


def load_tokens(session: Session, path: Path = MARK_TOKENS_FILE) -> None:
    for obj in load_jsonl(path):
        if not session.get(Token, obj["token_id"]):
            session.add(Token(**obj))


def load_pericopes(session: Session, path: Path = MARK_PERICOPES_FILE) -> None:
    for obj in load_jsonl(path):
        if not session.get(Pericope, obj["pericope_id"]):
            session.add(Pericope(**obj))


def load_mark_corpus() -> None:
    session: Session = SessionLocal()
    try:
        ensure_book(session)
        load_units(session)
        load_tokens(session)
        load_pericopes(session)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    load_mark_corpus()
'@

# iv\__init__.py
$ivInit = @'
# iv package init
'@

# iv\data\mark_iv_seed.yaml
$ivSeed = @'
- iv_id: IV.MRK.01.14-15.INAUGURAL_PROCLAMATION
  book_code: MRK
  scope: pericope
  pericope_id: MRK.01.14-15.INAUGURAL_PROCLAMATION
  unit_ids: [MRK.01.14, MRK.01.15]
  primary_arc_id: ARC.KINGDOM_SEED_GROWTH
  modal:
    box:
      label: "□-King-Proclaimer"
      description: "Jesus appears as the anointed King whose voice carries divine authority."
    diamond:
      label: "◇-Announce-Kingdom-Call-To-Repent"
      description: "He preaches the gospel of God, announcing fulfilled time and commanding repentance and faith."
    delta:
      label: "Δ-Kingdom-At-Hand-Faithful-Response"
      description: "The kingdom has drawn near; the fitting human effect is repentance and trust."
  textual_confidence: 0.97
  interpretive_confidence: 0.9
  summary: "The King’s inaugural proclamation frames the rest of Mark."
  notes:
    - "□ identity: Jesus as divine King."
    - "◇ enactment: proclamation and command."
    - "Δ effect: responsive repentance and faith."

- iv_id: IV.MRK.04.26-29.GROWING_SEED
  book_code: MRK
  scope: pericope
  pericope_id: MRK.04.26-04.29.GROWING_SEED
  unit_ids: [MRK.04.26, MRK.04.27, MRK.04.28, MRK.04.29]
  primary_arc_id: ARC.KINGDOM_SEED_GROWTH
  modal:
    box:
      label: "□-Sower-Son-Faithful"
      description: "The Son acts as faithful sower, trusting the Father’s hidden agency."
    diamond:
      label: "◇-Sow-Sleep-Trust"
      description: "He sows the word, then entrusts unseen growth to God."
    delta:
      label: "Δ-Seed-Grows-To-Ripeness"
      description: "The kingdom matures to an appointed harvest."
  textual_confidence: 0.95
  interpretive_confidence: 0.85
  summary: "The parable of the growing seed shows the kingdom’s unseen but inevitable growth toward harvest."
  notes:
    - "□ identity emphasises divine agency."
    - "◇ enactment includes sowing and waiting."
    - "Δ effect is harvest/ripeness."
'@

# iv\etl_iv_pairs_mark.py
$ivEtl = @'
import json
from pathlib import Path
from typing import Any, Dict, List

import yaml
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import IVPair, IVPairUnit, CanonicalArc

BASE_DIR = Path(__file__).resolve().parent
IV_SEED_FILE = BASE_DIR / "data" / "mark_iv_seed.yaml"
IV_PAIRS_FILE = BASE_DIR / "data" / "iv_pairs_mark.jsonl"


def load_seed() -> List[Dict[str, Any]]:
    with open(IV_SEED_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_jsonl(records: List[Dict[str, Any]], out_path: Path = IV_PAIRS_FILE) -> None:
    with open(out_path, "w", encoding="utf-8") as out:
        for rec in records:
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")


def seed_to_db(records: List[Dict[str, Any]]) -> None:
    session: Session = SessionLocal()
    try:
        # Ensure canonical arc
        arc_id = "ARC.KINGDOM_SEED_GROWTH"
        arc = session.get(CanonicalArc, arc_id)
        if not arc:
            arc = CanonicalArc(
                arc_id=arc_id,
                label="Seed \u2192 Growth \u2192 Harvest",
                description="Canon-wide pattern linking seed parables and eschatological harvest texts.",
                links=json.dumps(
                    ["MRK.04.26-29", "1COR.15.35-49", "REV.14.14-20"],
                    ensure_ascii=False,
                ),
            )
            session.add(arc)
            session.flush()

        for rec in records:
            iv = IVPair(
                iv_id=rec["iv_id"],
                book_code=rec["book_code"],
                scope=rec["scope"],
                pericope_id=rec.get("pericope_id"),
                primary_arc_id=rec.get("primary_arc_id"),
                box_label=rec["modal"]["box"]["label"],
                box_description=rec["modal"]["box"]["description"],
                diamond_label=rec["modal"]["diamond"]["label"],
                diamond_description=rec["modal"]["diamond"]["description"],
                delta_label=rec["modal"]["delta"]["label"],
                delta_description=rec["modal"]["delta"]["description"],
                textual_confidence=rec.get("textual_confidence"),
                interpretive_confidence=rec.get("interpretive_confidence"),
                summary=rec.get("summary"),
            )
            session.merge(iv)
            session.flush()
            for unit_id in rec.get("unit_ids", []):
                session.add(IVPairUnit(iv_id=rec["iv_id"], unit_id=unit_id))

        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def run_iv_pairs_mark() -> None:
    records = load_seed()
    write_jsonl(records)
    seed_to_db(records)


if __name__ == "__main__":
    run_iv_pairs_mark()
'@

# corpus\data\raw\mark_base.txt
$markBase = @'
# chapter	verse	text
4	26	Kai elegen hoti houtos estin he basileia tou theou hos anthropos bale ton sporon epi tes ges
4	27	kai katheude kai egeiretai nux kai hemera kai ho sperma blastanei kai mekynetai hos ouk oiden autos
4	28	automate he ge karpophorei proton chorton eita stachyn eita pleres siton en to stachy
4	29	hotan de paradidid ho karpos euthus apostellei to drepanon hoti paresteken ho therismos
'@

# corpus\data\raw\mark_morph.txt
$markMorph = @'
# chap	verse	pos	surface	lemma	morph	pos_tag	strongs
4	26	1	Kai	kai	CONJ	CONJ	G2532
4	26	2	elegen	lego	V-IAI-3S	V	G3004
4	26	3	houtos	houtos	DEM	PRON	G3778
4	26	4	estin	eimi	V-PAI-3S	V	G1510
4	26	5	he	ho	ART	DET	G3588
4	26	6	basileia	basileia	N-NSF	N	G932
4	26	7	tou	ho	ART	DET	G3588
4	26	8	theou	theos	N-GSM	N	G2316

4	27	1	kai	kai	CONJ	CONJ	G2532
4	27	2	katheude	katheudo	V-PAS-3S	V	G2518
4	27	3	egeiretai	egeiro	V-PMI-3S	V	G1453
4	27	4	nux	nux	N-NSF	N	G3571
4	27	5	hemera	hemera	N-NSF	N	G2250

4	28	1	automate	automatos	ADV	ADV	G844
4	28	2	he	ho	ART	DET	G3588
4	28	3	ge	ge	N-NSF	N	G1093
4	28	4	karpophorei	karpophoreo	V-PAI-3S	V	G2592

4	29	1	hotan	hotan	CONJ	CONJ	G3752
4	29	2	ho	ho	ART	DET	G3588
4	29	3	karpos	karpos	N-NSM	N	G2590
4	29	4	aposteilei	apostello	V-AAS-3S	V	G649
4	29	5	to	to	ART	DET	G3588
4	29	6	drepanon	drepanon	N-ASN	N	G1407
'@

# 4. WRITE FILES
Set-Content -Path "$root\app\__init__.py" -Value $appInit -Encoding UTF8
Set-Content -Path "$root\app\db.py" -Value $appDb -Encoding UTF8
Set-Content -Path "$root\app\models.py" -Value $appModels -Encoding UTF8
Set-Content -Path "$root\app\routers\__init__.py" -Value $appRoutersInit -Encoding UTF8
Set-Content -Path "$root\app\routers\ivb.py" -Value $appRouterIvb -Encoding UTF8
Set-Content -Path "$root\app\main.py" -Value $appMain -Encoding UTF8
Set-Content -Path "$root\app\init_db.py" -Value $appInitDb -Encoding UTF8

Set-Content -Path "$root\corpus\__init__.py" -Value $corpusInit -Encoding UTF8
Set-Content -Path "$root\corpus\config.py" -Value $corpusConfig -Encoding UTF8
Set-Content -Path "$root\corpus\etl_mark.py" -Value $corpusEtl -Encoding UTF8
Set-Content -Path "$root\corpus\db_loader.py" -Value $corpusDbLoader -Encoding UTF8

Set-Content -Path "$root\iv\__init__.py" -Value $ivInit -Encoding UTF8
Set-Content -Path "$root\iv\data\mark_iv_seed.yaml" -Value $ivSeed -Encoding UTF8
Set-Content -Path "$root\iv\etl_iv_pairs_mark.py" -Value $ivEtl -Encoding UTF8

Set-Content -Path "$root\corpus\data\raw\mark_base.txt" -Value $markBase -Encoding UTF8
Set-Content -Path "$root\corpus\data\raw\mark_morph.txt" -Value $markMorph -Encoding UTF8

Write-Host "Python files and data written."

# 5. INITIALISE DB
Write-Host "Initialising database..."
python -m app.init_db

# 6. RUN ETL FOR MARK
Write-Host "Running Mark ETL..."
python -m corpus.etl_mark
python -m corpus.db_loader

# 7. RUN IV PAIRS ETL
Write-Host "Seeding IV pairs..."
python -m iv.etl_iv_pairs_mark

Write-Host ""
Write-Host "=== Build complete ==="
Write-Host "To run the FastAPI app, run this in a new PowerShell window:"
Write-Host "    cd `"$root`""
Write-Host "    & `"$root\venv\Scripts\Activate.ps1`""
Write-Host "    uvicorn app.main:app --reload"
Write-Host ""
Write-Host "Once uvicorn is running, you can get IVB.MRK.04.json with:"
Write-Host "    Invoke-RestMethod -Uri 'http://127.0.0.1:8000/ivb/chapter?book_code=MRK&chapter=4' |"
Write-Host "      ConvertTo-Json -Depth 10 |"
Write-Host "      Out-File -FilePath '$root\build_output\IVB.MRK.04.json' -Encoding utf8"
Write-Host ""
Write-Host "Then open build_output\\IVB.MRK.04.json in your editor."
