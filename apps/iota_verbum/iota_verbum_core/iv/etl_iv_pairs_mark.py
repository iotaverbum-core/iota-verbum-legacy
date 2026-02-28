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
