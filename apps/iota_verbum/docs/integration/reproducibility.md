# Reproducibility Quickstart
- Conda: \conda env create -f infra/conda/environment.yml && conda activate iota\
- Docker: \docker compose -f infra/docker/docker-compose.yml up --build\
- Manifested run: \python scripts/run_reproducible.py --repro-tag test\
"@

Write-NoBOM "scripts/run_reproducible.py" @"
import argparse, hashlib, json, os, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT/'results'/'runs'
def sha256_file(p: Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(8192), b''): h.update(chunk)
    return h.hexdigest()
def manifest(tag:str)->dict:
    files=[]
    for rel in ('web','scripts','console','governance'):
        base=ROOT/rel
        if base.exists():
            for p in base.rglob('*.*'):
                try: files.append({'path':str(p.relative_to(ROOT)),'sha256':sha256_file(p)})
                except: pass
    return {'tag':tag,'ts':int(time.time()),'files':files}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repro-tag',required=True)
    args=ap.parse_args()
    outdir=RESULTS/args.repro_tag
    outdir.mkdir(parents=True, exist_ok=True)
    m=manifest(args.repro_tag)
    (outdir/'run_manifest.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
    # Simulate pipeline snapshot artifact
    (outdir/'_ok.txt').write_text('run ok',encoding='utf-8')
    print(f'Wrote manifest → {outdir}')
if __name__=='__main__': main()