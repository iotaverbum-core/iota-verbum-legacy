from pathlib import Path
import sys

# Ensure repo root is on sys.path so we can import modal_bible.*
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from modal_bible.models import ModalPassage
from modal_bible.graph_view import LambdaGraph


def main():
    base = Path(__file__).resolve().parents[1]  # repo root-ish
    ps22_path = base / "modal_bible" / "psalms" / "ps22.lambda.json"

    passage = ModalPassage.load(ps22_path)
    graph = LambdaGraph.from_passage(passage)

    print(f"Passage: {passage.passage_id} – {passage.title}")
    print("Identity invariants (□ / []):")
    for inv in passage.identity_invariants:
        print("  ", inv)

    print("\nOperators found in Psalm 22:")
    for op in sorted(graph.operator_nodes):
        print("  ", op)

    print("\nEntities found in Psalm 22:")
    for ent in sorted(graph.entity_nodes):
        print("  ", ent)

    print("\nSample adjacency (first 5 statement nodes):")
    adj = graph.to_adjacency()
    for stmt_id in list(adj.keys())[:5]:
        print(f"  {stmt_id}:")
        for rel, dst in adj[stmt_id]:
            print(f"    - {rel} -> {dst}")


if __name__ == "__main__":
    main()
