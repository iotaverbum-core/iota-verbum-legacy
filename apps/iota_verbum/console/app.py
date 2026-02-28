from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
import json, time

app = FastAPI(title='Investor Console (Read-only)')
ROOT = Path(__file__).resolve().parents[1]

def _metrics():
    runs = len(list((ROOT/'results'/'runs').glob('*')))
    jobs = len(list((ROOT/'results'/'jobs').glob('*')))
    return runs, jobs

@app.get('/console', response_class=HTMLResponse)
def console():
    runs, jobs = _metrics()
    html = f\"\"\"<html><head><title>Iota Console</title>
    <style>body{{font-family:Inter,system-ui}} .card{{border:1px solid #ddd;padding:16px;margin:12px;border-radius:8px;}}</style>
    </head><body>
    <h2>Iota Verbum • Read-only Console</h2>
    <div class='card'><b>Runs</b>: {runs}</div>
    <div class='card'><b>Jobs</b>: {jobs}</div>
    <div class='card'><b>Updated</b>: {int(time.time())}</div>
    </body></html>\"\"\"
    return html