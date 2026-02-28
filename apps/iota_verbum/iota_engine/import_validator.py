from pathlib import Path
import csv, json, sys

REQ = ['book','chapter','verse','lemma','token']

def check_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        hdr = next(csv.reader(f))
    missing = [c for c in REQ if c not in hdr]
    return {'file': str(path.name), 'ok': not missing, 'missing': missing}

def main():
    root = Path(__file__).resolve().parents[1]
    lang = root/'results'/'languages'
    out  = root/'results'/'reports'
    out.mkdir(parents=True, exist_ok=True)

    files = ['oshb_tokens.csv','morphgnt_tokens.csv','targum_tokens.csv']
    results = [check_csv(lang/f) for f in files]
    ok = all(r['ok'] for r in results)

    (out/'import_validation.json').write_text(json.dumps({'ok':ok, 'checks':results}, indent=2), encoding='utf-8')
    print('IMPORT VALIDATION:', 'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
