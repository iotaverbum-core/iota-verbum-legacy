import re, json, hashlib, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEX = yaml.safe_load((ROOT / "lexicons.yaml").read_text(encoding="utf-8"))
RULES = yaml.safe_load((ROOT / "rules.yaml").read_text(encoding="utf-8"))

def normalize(text: str) -> str:
    import re
    return re.sub(r"\s+", " ", text.strip())

def sentence_clause_split(text: str):
    text = normalize(text)
    markers = [";", ".", ":", ",", " when ", " that ", " so that ", " therefore ", " then ", " thus "]
    for m in markers:
        text = text.replace(m.strip(), "|||"+m.strip()+" ")
    parts = [normalize(p) for p in text.split("|||") if p.strip()]
    return [{"span": f"c{i+1}", "text": p} for i,p in enumerate(parts)]

def contains_any(text, terms):
    t = text.lower()
    return any(w.lower() in t for w in terms)

def extract_nodes(clauses):
    nodes = []
    for c in clauses:
        txt = c["text"]; span = c["span"]
        # Identity
        if any(contains_any(txt, LEX["identity"][k]) for k in ["persons","divine_titles","kingdom_objects"]):
            if contains_any(txt, LEX["copula"]) or "of" in txt.lower():
                nodes.append({"id": f"n{len(nodes)+1}","kind":"identity","lemma":"identity","text":txt,"span":span,"confidence":0.8})
        # Enactment
        allverbs = sum(LEX["enactment_verbs"].values(), [])
        if contains_any(txt, allverbs):
            core = next((v for v in allverbs if v in txt.lower()), "verb")
            nodes.append({"id": f"n{len(nodes)+1}","kind":"enactment","lemma":core,"text":txt,"span":span,"confidence":0.75})
        # Effect
        if contains_any(txt, LEX["effect_markers"]) or "produce" in txt.lower() or "harvest" in txt.lower():
            nodes.append({"id": f"n{len(nodes)+1}","kind":"effect","lemma":"result","text":txt,"span":span,"confidence":0.8})
    return nodes

def build_edges(nodes):
    edges = []
    ids = [n for n in nodes if n["kind"]=="identity"]
    ens = [n for n in nodes if n["kind"]=="enactment"]
    efs = [n for n in nodes if n["kind"]=="effect"]

    if ids and ens:
        edges.append({"from": ids[0]["id"], "to": ens[0]["id"], "relation":"grounds", "confidence":0.8})
    for i in range(len(ens)):
        if i < len(efs):
            edges.append({"from": ens[i]["id"], "to": efs[i]["id"], "relation":"produces", "confidence":0.75})
    if len(efs) > 1:
        edges.append({"from": efs[0]["id"], "to": efs[1]["id"], "relation":"implies", "confidence":0.7})
    return edges

def creed_check(nodes):
    text = " ".join(n["text"] for n in nodes).lower()
    notes = []; status = "pass"
    if "like god" in text or "made god" in text:
        status = "warn"; notes.append("deity softening")
    if "christ is a creature" in text or "spirit is a force only" in text:
        status = "fail"; notes.append("creed hard fail phrase")
    return {"status":status,"notes":notes}

def finalize(ref, translation, nodes, edges, creed):
    sig = "".join([n["kind"][0] for n in nodes]) + "".join([e["relation"][0] for e in edges]) + ref
    watermark = hashlib.sha256(sig.encode()).hexdigest()[:16]
    return {"ref":ref,"translation":translation,"nodes":nodes,"edges":edges,"creed":creed,"watermark":watermark}

def iota_parse(doc):
    clauses = sentence_clause_split(doc["text"])
    nodes = extract_nodes(clauses)
    edges = build_edges(nodes)
    creed = creed_check(nodes)
    return finalize(doc["ref"], doc["translation"], nodes, edges, creed)
