# Partner Quickstart
- Install: \pip install requests\
- Auth + analyze: see \examples/minimal_script.py\
"@

# -------------------------
# Phase 16 — Investor Console (simple HTML, no extra deps)
# -------------------------
Write-NoBOM "web/api/v1_metrics.py" @"
from fastapi import APIRouter
from pathlib import Path
import time

router = APIRouter(prefix='/metrics', tags=['metrics'])
ROOT = Path(__file__).resolve().parents[2]

@router.get('/kpis')
def kpis():
    runs = len(list((ROOT/'results'/'runs').glob('*')))
    jobs = len(list((ROOT/'results'/'jobs').glob('*')))
    phases_done = 12  # through Phase 12 baseline
    return {'runs':runs,'jobs':jobs,'phases_done':phases_done,'ts':int(time.time())}