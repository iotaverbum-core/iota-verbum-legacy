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
