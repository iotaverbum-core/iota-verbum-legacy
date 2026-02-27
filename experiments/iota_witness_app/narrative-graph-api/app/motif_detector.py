from __future__ import annotations

from app.models import EdgeType, Motif, NarrativeEdge, NarrativeNode, NodeType


class MotifDetector:
    def detect(self, nodes: list[NarrativeNode], edges: list[NarrativeEdge]) -> list[Motif]:
        motifs: list[Motif] = []

        faith = [n.id for n in nodes if any(t in n.text.lower() for t in ("faith", "believe", "trust"))]
        if faith:
            motifs.append(
                Motif(
                    name="faith",
                    confidence=0.85,
                    occurrences=faith,
                    cross_references=["Hebrews 11:1", "Romans 10:17"],
                    description="Elements of faith and belief in the narrative",
                )
            )

        authority = [e.id for e in edges if e.type == EdgeType.GROUNDS and e.theological_weight >= 0.8]
        if authority:
            motifs.append(
                Motif(
                    name="divine_authority",
                    confidence=0.9,
                    occurrences=authority,
                    cross_references=["Matthew 28:18", "John 5:27"],
                    description="Identity claims ground authority-bearing action",
                )
            )

        healing = [
            n.id
            for n in nodes
            if n.type == NodeType.EFFECT and any(t in n.text.lower() for t in ("heal", "restore", "save"))
        ]
        if healing:
            motifs.append(
                Motif(
                    name="healing_restoration",
                    confidence=0.88,
                    occurrences=healing,
                    cross_references=["Isaiah 53:5", "1 Peter 2:24"],
                    description="Divine healing and restoration",
                )
            )

        return motifs
