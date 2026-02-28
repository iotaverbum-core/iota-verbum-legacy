# ───────────────────────────────────────────────────────────────
# © Matthew Neal | The Daily Covenant | 2025
# Scripture-Oriented Modal Base (SOMB) – Project Auditor
# Scans all .py files, saves SHA256 hashes (init), and verifies later (verify).
# ───────────────────────────────────────────────────────────────

import hashlib, json, sys, os
from pathlib import Path

# Optional color output (works if colorama is installed)
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    GREEN, RED, YELLOW, CYAN, RESET = Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.CYAN, Style.RESET_ALL
except Exception:
    GREEN = RED = YELLOW = CYAN = RESET = ""

ROOT = Path(__file__).resolve().parent
HASH_FILE = ROOT / "HASHES.json"

def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def find_py_files() -> list[Path]:
    # All .py files under ROOT (excluding venv and __pycache__)
    files = []
    for p in ROOT.rglob("*.py"):
        if ".venv" in p.parts or "__pycache__" in p.parts:
            continue
        files.append(p.relative_to(ROOT))
    # Sort for deterministic output
    return sorted(files, key=lambda p: str(p).lower())

def init_hashes():
    files = find_py_files()
    data = {"base_path": str(ROOT), "files": {}}
    for rel in files:
        data["files"][str(rel)] = sha256_of(ROOT / rel)
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"{CYAN}Initialized hash set for {len(files)} file(s). Saved to {HASH_FILE.name}.{RESET}")

def verify_hashes():
    if not HASH_FILE.exists():
        print(f"{RED}No {HASH_FILE.name} found. Run: python somb_audit.py init{RESET}")
        sys.exit(1)

    with open(HASH_FILE, "r", encoding="utf-8") as f:
        baseline = json.load(f)

    baseline_files = set(baseline.get("files", {}).keys())
    current_files = set(str(p) for p in find_py_files())

    added = current_files - baseline_files
    removed = baseline_files - current_files
    common = current_files & baseline_files

    ok = 0
    changed = 0

    print(f"{CYAN}Verifying files against {HASH_FILE.name}…{RESET}")

    for rel in sorted(common):
        current = sha256_of(ROOT / rel)
        original = baseline["files"][rel]
        if current == original:
            print(f"{GREEN}✅ {rel} – authentic{RESET}")
            ok += 1
        else:
            print(f"{RED}⚠️  {rel} – modified{RESET}")
            changed += 1

    for rel in sorted(added):
        print(f"{YELLOW}➕ New file not in baseline: {rel}{RESET}")

    for rel in sorted(removed):
        print(f"{YELLOW}➖ Missing file (was in baseline): {rel}{RESET}")

    print(f"\n{CYAN}Summary:{RESET} {ok} authentic, {changed} modified, {len(added)} added, {len(removed)} removed.")
    if changed > 0:
        sys.exit(2)

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in {"init", "verify"}:
        print("Usage: python somb_audit.py [init|verify]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "init":
        init_hashes()
    elif cmd == "verify":
        verify_hashes()

if __name__ == "__main__":
    main()
