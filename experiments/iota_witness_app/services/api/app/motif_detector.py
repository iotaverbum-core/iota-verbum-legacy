from __future__ import annotations

from app.narrative_models import EdgeType, Motif, NarrativeEdge, NarrativeNode, NodeType


class MotifDetector:
    def detect(self, nodes: list[NarrativeNode], edges: list[NarrativeEdge]) -> list[Motif]:
        motifs: list[Motif] = []

        faith_nodes = [
            n.id
            for n in nodes
            if any(
                token in n.text.lower()
                for token in ("faith", "believe", "trust")
            )
        ]
        if faith_nodes:
            motifs.append(
                Motif(
                    name="faith",
                    confidence=0.85,
                    occurrences=faith_nodes,
                    cross_references=["Hebrews 11:1", "Romans 10:17"],
                    description="Elements of faith and belief in the narrative.",
                )
            )

        authority_edges = [
            e.id for e in edges if e.type == EdgeType.GROUNDS and e.theological_weight >= 0.8
        ]
        if authority_edges:
            motifs.append(
                Motif(
                    name="divine_authority",
                    confidence=0.9,
                    occurrences=authority_edges,
                    cross_references=["Matthew 28:18", "John 5:27"],
                    description="Identity claims ground authority-bearing action.",
                )
            )

        healing_nodes = [
            n.id
            for n in nodes
            if n.type == NodeType.EFFECT
            and any(token in n.text.lower() for token in ("heal", "restore", "save", "cleanse"))
        ]
        if healing_nodes:
            motifs.append(
                Motif(
                    name="healing_restoration",
                    confidence=0.88,
                    occurrences=healing_nodes,
                    cross_references=["Isaiah 53:5", "1 Peter 2:24"],
                    description="Divine healing and restoration pattern.",
                )
            )

        return motifs
