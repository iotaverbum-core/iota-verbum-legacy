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
    """
    Parse the base text TSV for Mark.

    Handles UTF-8 BOM and skips comment lines starting with '#'.
    """
    verses: List[dict] = []
    with open(path, "r", encoding="utf-8-sig") as f:  # note utf-8-sig
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            # skip comments even if there is a BOM in front
            if line.lstrip().startswith("#"):
                continue
            parts = line.split("\t", maxsplit=2)
            if len(parts) != 3:
                continue
            chapter_s, verse_s, text = parts
            verses.append(
                {
                    "chapter": int(chapter_s),
                    "verse": int(verse_s),
                    "text": text,
                }
            )
    return verses


def parse_morph(path: Path = MARK_MORPH_FILE) -> Dict[tuple, List[dict]]:
    """
    Parse the morphology TSV for Mark.

    Handles UTF-8 BOM and skips comment lines starting with '#'.
    """
    result: Dict[tuple, List[dict]] = {}
    with open(path, "r", encoding="utf-8-sig") as f:  # note utf-8-sig
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.lstrip().startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) < 6:
                continue
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
            "title_iota": "Î”-Seed-Grows-To-Ripeness",
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
