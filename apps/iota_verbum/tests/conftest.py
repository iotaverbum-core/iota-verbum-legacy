# tests/conftest.py
# Ensure the project root (where `engine/` lives) is on sys.path for tests.

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # .../iota_verbum
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
