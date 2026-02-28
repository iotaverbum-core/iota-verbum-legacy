from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import threading, time, zipfile, json, uuid

router = APIRouter(prefix='/jobs', tags=['jobs'])
ROOT = Path(__file__).resolve().parents[2]
JOBS_DIR = ROOT/'results'/'jobs'
STATE = {}  # job_id -> dict(status, path)

def _artifact_zip(job_id:str)->Path:
    out = JOBS_DIR/job_id
    out.mkdir(parents=True, exist_ok=True)
    z = out/'artifact.zip'
    with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as zh:
        # include latest reports if any
        for p in (ROOT/'results').rglob('*'):
            if p.is_file() and p.suffix.lower() in ('.txt','.docx','.json','.png','.svg'):
                try: zh.write(p, arcname=p.relative_to(ROOT))
                except: pass
        # small status file
        (out/'status.json').write_text(json.dumps({'ok':True,'ts':int(time.time())}),encoding='utf-8')
        zh.write(out/'status.json', arcname=f'jobs/{job_id}/status.json')
    return z

def _runner(job_id:str, kind:str, payload:dict):
    STATE[job_id] = {'status':'running','path':None}
    try:
        time.sleep(0.5)  # simulate work
        z = _artifact_zip(job_id)
        STATE[job_id] = {'status':'done','path':str(z)}
    except Exception as e:
        STATE[job_id] = {'status':'error','error':str(e)}

@router.post('/submit')
def submit(job_type:str, payload:dict|None=None):
    job_id = uuid.uuid4().hex[:12]
    threading.Thread(target=_runner, args=(job_id, job_type, payload or {}), daemon=True).start()
    return {'job_id':job_id,'status':'queued'}

@router.get('/{job_id}/status')
def status(job_id:str):
    if job_id not in STATE: return {'status':'unknown'}
    return STATE[job_id]

@router.get('/{job_id}/artifact')
def artifact(job_id:str):
    item = STATE.get(job_id)
    if not item or item.get('status')!='done':
        raise HTTPException(404,'artifact not ready')
    return FileResponse(item['path'], filename='artifact.zip', media_type='application/zip')