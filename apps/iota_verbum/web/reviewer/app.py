from pathlib import Path
from flask import Flask, send_from_directory, jsonify
import json

ROOT = Path(__file__).resolve().parents[2]
APP  = Flask(__name__, static_folder=str(ROOT/'web'/'reviewer'/'static'), template_folder=str(ROOT/'web'/'reviewer'/'templates'))

@APP.get('/')
def index():
    return send_from_directory(APP.template_folder, 'index.html')

@APP.get('/cache')
def cache():
    p = ROOT / 'results' / 'manifest' / 'cache.json'
    if p.exists():
        return jsonify(json.loads(p.read_text(encoding='utf-8')))
    return jsonify({"message":"no cache"}), 404

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=5055, debug=False)