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
