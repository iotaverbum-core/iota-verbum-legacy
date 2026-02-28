from pathlib import Path
import json, time

def main():
    root = Path(__file__).resolve().parents[1]
    out  = root/'results'/'languages'
    out.mkdir(parents=True, exist_ok=True)

    # Write tiny sample token CSVs (stand-ins for OSHB / MorphGNT / Targum)
    (out/'oshb_tokens.csv').write_text('book,chapter,verse,lemma,token\nGen,1,1,בּרא,ברא\n', encoding='utf-8')
    (out/'morphgnt_tokens.csv').write_text('book,chapter,verse,lemma,token\nMark,4,26,σπείρω,σπείρῃ\n', encoding='utf-8')
    (out/'targum_tokens.csv').write_text('book,chapter,verse,lemma,token\nGen,1,1,ברא,ברא\n', encoding='utf-8')

    manifest = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'corpora': [
            {'name':'OSHB','files':['oshb_tokens.csv']},
            {'name':'MorphGNT','files':['morphgnt_tokens.csv']},
            {'name':'Targum','files':['targum_tokens.csv']},
        ]
    }
    (out/'originals_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Phase8 import_driver: wrote samples + manifest to', out)

if __name__ == '__main__':
    main()
