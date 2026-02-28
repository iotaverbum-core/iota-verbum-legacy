from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pathlib import Path
import time, json

router = APIRouter(prefix='/partner', tags=['partner'])
SECRET = 'dev-shared-secret'  # replace for prod

def _modalize(text:str)->dict:
    # toy modalization: detect simple tokens, produce JSON + inline SVG
    identity = '□' if any(w.lower()=='god' for w in text.split()) else '□'
    svg = f\"\"\"<svg xmlns='http://www.w3.org/2000/svg' width='460' height='120'>
    <rect x='10' y='10' width='100' height='40' rx='6' ry='6' fill='#eee' stroke='#333'/>
    <text x='60' y='35' text-anchor='middle' font-family='Inter' font-size='18'>□L</text>
    <text x='160' y='35' font-family='Inter' font-size='18'>→</text>
    <rect x='190' y='10' width='140' height='40' rx='6' ry='6' fill='#eee' stroke='#333'/>
    <text x='260' y='35' text-anchor='middle' font-family='Inter' font-size='18'>◇E L(t)</text>
    <text x='350' y='35' font-family='Inter' font-size='18'>→</text>
    <rect x='370' y='10' width='80' height='40' rx='6' ry='6' fill='#eee' stroke='#333'/>
    <text x='410' y='35' text-anchor='middle' font-family='Inter' font-size='18'>Δ</text>
    </svg>\"\"\"
    return {'identity':identity,'enactment':'◇E L(t)','effect':'Δ','svg':svg,'ts':int(time.time())}

@router.post('/auth/token')
def token(shared_secret:str=Form(...)):
    return {'ok': shared_secret==SECRET, 'token': 'dev-token' if shared_secret==SECRET else None}

@router.post('/analyze')
async def analyze(token:str=Form(...), text:str=Form(None), file:UploadFile=File(None)):
    if token!='dev-token': return JSONResponse({'error':'unauthorized'}, status_code=401)
    data = text or (await file.read()).decode('utf-8')
    return _modalize(data)

@router.get('/report/{rid}')
def report(rid:str):
    # simple echo stub
    return {'report_id':rid,'status':'ready'}