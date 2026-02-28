from pathlib import Path
import json

def main():
    root = Path(__file__).resolve().parents[1]
    iv   = root/'results'/'iv'
    outd = root/'results'/'iv'
    outd.mkdir(parents=True, exist_ok=True)

    files = sorted([p for p in iv.glob('*.json')])
    node_ids = [p.stem for p in files]
    nodes = [{'id':n, 'label':n} for n in node_ids]

    edges = []
    if len(node_ids) >= 2:
        center = node_ids[-1]       # e.g., mark_4_26_29
        for n in node_ids[:-1]:
            edges.append({'from': n, 'to': center, 'type':'canonical_arc'})
    arcs = {'nodes': nodes, 'edges': edges}

    (outd/'canonical_arcs.json').write_text(json.dumps(arcs, indent=2), encoding='utf-8-sig')
    print('Phase10 canonical_arcs: wrote', outd/'canonical_arcs.json')

if __name__ == '__main__':
    main()
