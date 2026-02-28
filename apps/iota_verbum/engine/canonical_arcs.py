from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
IV   = ROOT / "results" / "iv"
OUTJ = IV / "canonical_arcs.json"
OUTG = IV / "canonical_arcs.gexf"

def parse_refs(text: str):
  # naive finder: Book chap:verse
  return re.findall(r'([A-Za-z]+)\s+\d+:\d+(?:-\d+)?', text)

def main():
  nodes = set(); edges = {}
  for f in IV.glob("IV_*.md"):
    t = f.read_text(encoding="utf-8", errors="ignore")
    refs = parse_refs(t)
    if len(refs) >= 2:
      a, b = refs[0], refs[1]
      nodes.add(a); nodes.add(b)
      edges[(a,b)] = edges.get((a,b), 0) + 1
  if not edges:
    # fallback to filenames
    for f in IV.glob("IV_*.md"):
      parts = f.stem.split("__")
      if len(parts)==2:
        a = parts[0].replace("IV_","").split("_")[0]
        b = parts[1].split("_")[0]
        nodes.add(a); nodes.add(b)
        edges[(a,b)] = edges.get((a,b), 0) + 1
  graph = {"nodes": sorted(list(nodes)), "edges":[{"source":a,"target":b,"weight":w} for (a,b),w in edges.items()]}
  OUTJ.write_text(json.dumps(graph, indent=2), encoding="utf-8")
  # write GEXF
  try:
    import networkx as nx
    G = nx.DiGraph()
    for n in nodes: G.add_node(n)
    for (a,b),w in edges.items(): G.add_edge(a,b,weight=w)
    nx.write_gexf(G, OUTG)
  except Exception:
    pass
  print("Canonical arcs built:", len(edges), "edges")
if __name__ == "__main__":
  main()