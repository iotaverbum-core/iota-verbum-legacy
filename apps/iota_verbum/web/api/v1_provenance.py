from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
router = APIRouter(prefix='/provenance', tags=['provenance'])
ROOT = Path(__file__).resolve().parents[2]
PDIR = ROOT/'results'/'provenance'
@router.get('/ledger')
def ledger():
    p=PDIR/'ledger.jsonl'
    if not p.exists(): raise HTTPException(404,'ledger not found')
    return FileResponse(str(p), media_type='application/json', filename='ledger.jsonl')
@router.get('/graph.gexf')
def graph():
    p=PDIR/'ledger.gexf'
    if not p.exists(): raise HTTPException(404,'graph not found')
    return FileResponse(str(p), media_type='application/xml', filename='ledger.gexf')
@router.get('/signature')
def sig():
    p=PDIR/'ledger.sig'
    if not p.exists(): raise HTTPException(404,'signature not found')
    return FileResponse(str(p), media_type='text/plain', filename='ledger.sig')