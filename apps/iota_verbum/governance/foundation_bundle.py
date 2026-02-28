import zipfile, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT/'dist'; DIST.mkdir(exist_ok=True)
def main():
    stamp = str(int(time.time()))
    out = DIST/f'iota_governance_bundle_{stamp}.zip'
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in (ROOT/'governance'/'policies').rglob('*'):
            if p.is_file(): z.write(p, arcname=str(p.relative_to(ROOT)))
        for p in (ROOT/'results'/'governance').glob('audit_report.json'):
            z.write(p, arcname=str(p.relative_to(ROOT)))
        # include API schema if present
        for p in (ROOT/'web'/'api').glob('openapi*.json'):
            z.write(p, arcname=str(p.relative_to(ROOT)))
        # include simple pubkey placeholder
        pk = ROOT/'results'/'provenance'/'pubkey.pem'
        if pk.exists(): z.write(pk, arcname=str(pk.relative_to(ROOT)))
    print('Bundle:', out)
if __name__=='__main__': main()