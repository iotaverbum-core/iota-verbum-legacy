import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR  = ROOT / "Scripts"
RAW  = ROOT / "data" / "raw"
OUT  = ROOT / "data" / "original"
OUT.mkdir(parents=True, exist_ok=True)

def main():
  conv1 = SCR / "convert_oshb_osis_to_csv.py"
  conv2 = SCR / "convert_morphgnt_tsv_to_csv.py"
  py = ROOT / ".venv" / "Scripts" / "python.exe"
  if conv1.exists():
    subprocess.run([str(py), str(conv1)], check=False)
  if conv2.exists():
    subprocess.run([str(py), str(conv2)], check=False)
  print("Import driver finished.")
if __name__ == "__main__":
  main()