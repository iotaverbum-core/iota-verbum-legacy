from pathlib import Path

GEXF = '''<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
  <graph mode="static" defaultedgetype="directed">
    <nodes>
      <node id="DSS" label="DSS"/>
      <node id="MT"  label="MT"/>
      <node id="LXX" label="LXX"/>
    </nodes>
    <edges>
      <edge id="e1" source="DSS" target="MT"  label="lineage"/>
      <edge id="e2" source="MT"  target="LXX" label="translation"/>
    </edges>
  </graph>
</gexf>'''

def main():
    root = Path(__file__).resolve().parents[1]
    outd = root/'results'/'variants'
    outd.mkdir(parents=True, exist_ok=True)
    (outd/'provenance.gexf').write_text(GEXF, encoding='utf-8')
    print('Phase9 variant_engine: wrote', outd/'provenance.gexf')

if __name__ == '__main__':
    main()
