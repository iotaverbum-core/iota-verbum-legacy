import hashlib
from colorama import Fore, Style, init
init(autoreset=True)

# === SIGNATURE INFO ===
ORIGINAL_HASH = "3703CA1C078CD50B10A69FB477CF6F33DDD4D03D26575E6C91610B72B255F8AC"
FILE_PATH = "main.py"
# =======================

def get_file_hash(path):
    with open(path, "rb") as f:
        file_bytes = f.read()
        return hashlib.sha256(file_bytes).hexdigest().upper()

def verify_signature():
    print(Fore.CYAN + "🔍 Checking file integrity for:", FILE_PATH)
    current_hash = get_file_hash(FILE_PATH)
    print("Current Hash:", current_hash)
    print("Original Hash:", ORIGINAL_HASH)

    if current_hash == ORIGINAL_HASH:
        print(Fore.GREEN + "✅ File is authentic. No changes detected.")
    else:
        print(Fore.RED + "⚠️ WARNING: File has been modified or tampered with!")

if __name__ == "__main__":
    verify_signature()
