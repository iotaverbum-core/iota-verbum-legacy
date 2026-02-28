from pathlib import Path
import pandas as pd, json
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
VAR  = ROOT / "results" / "variants"
VAR.mkdir(parents=True, exist_ok=True)

def main():
  G = nx.DiGraph()
  # minimal: stitch provenance if present; else create placeholder
  app = VAR / "apparatus_*.csv"
  added = 0
  for f in VAR.glob("*.csv"):
    try:
      df = pd.read_csv(f)
      if {"source","tradition","reading"}.issubset(df.columns):
        for _, r in df.iterrows():
          s = f"{r['source']}"
          t = f"{r['tradition']}"
          rd = f"{r['reading']}"
          G.add_node(s, kind="source")
          G.add_node(t, kind="tradition")
          G.add_node(rd, kind="reading")
          G.add_edge(s, t)
          G.add_edge(t, rd)
          added += 1
    except Exception:
      pass
  if added == 0:
    G.add_node("Unknown_Source", kind="source")
    G.add_node("Unknown_Tradition", kind="tradition")
    G.add_node("Unknown_Reading", kind="reading")
    G.add_edge("Unknown_Source","Unknown_Tradition")
    G.add_edge("Unknown_Tradition","Unknown_Reading")
  nx.write_gexf(G, VAR / "provenance.gexf")
  jsonld = {
    "@context": {"@vocab":"https://example.org/variant#"},
    "@graph": [
      {"@id": n, "kind": G.nodes[n].get("kind")} for n in G.nodes
    ] + [{"@id": f"{u}->{v}", "from":u, "to":v} for u,v in G.edges]
  }
  (VAR / "provenance.jsonld").write_text(json.dumps(jsonld, indent=2), encoding="utf-8")
  print("Variant provenance exported:", added, "edges")
if __name__ == "__main__":
  main()