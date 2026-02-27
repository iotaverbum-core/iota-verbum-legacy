from __future__ import annotations

from app.models import EdgeType, NarrativeEdge, NarrativeGraph, NarrativeNode, NodeType
from app.motif_detector import MotifDetector
from app.utils import graph_id, short_hash, split_sentences, utc_now_iso


class NarrativeEngine:
    def __init__(self) -> None:
        self.identity_verbs = {"am", "is", "are", "called", "named", "declared", "revealed"}
        self.effect_verbs = {"healed", "cleansed", "restored", "raised", "forgiven", "saved"}
        self.enactment_verbs = {"said", "went", "came", "took", "gave", "did", "spoke", "taught"}
        self.detector = MotifDetector()

    async def analyze(
        self,
        text: str,
        reference: str,
        lemmas: list[list[str]] | None = None,
        strongs: list[list[str]] | None = None,
    ) -> NarrativeGraph:
        sentences = split_sentences(text)
        nodes: list[NarrativeNode] = []
        for i, sentence in enumerate(sentences):
            node = self._sentence_to_node(
                sentence,
                reference,
                i,
                lemmas[i] if lemmas and i < len(lemmas) else [],
                strongs[i] if strongs and i < len(strongs) else [],
            )
            if node:
                nodes.append(node)

        edges = self._build_edges(nodes)
        motifs = self.detector.detect(nodes, edges)
        return NarrativeGraph(
            id=graph_id(reference),
            primary_reference=reference,
            nodes=nodes,
            edges=edges,
            motifs=motifs,
            metadata={
                "created_at": utc_now_iso(),
                "sentence_count": len(sentences),
                "node_count": len(nodes),
                "edge_count": len(edges),
            },
        )

    def _sentence_to_node(
        self,
        sentence: str,
        reference: str,
        index: int,
        lemmas: list[str],
        strongs: list[str],
    ) -> NarrativeNode | None:
        node_type = self._detect_node_type(sentence)
        if node_type is None:
            return None
        node_id = f"n{index + 1}_{short_hash(sentence)}"
        return NarrativeNode(
            id=node_id,
            type=node_type,
            text=sentence,
            reference=reference,
            lemmas=lemmas,
            strongs_numbers=strongs,
            confidence=0.85,
            metadata={"sentence_index": index},
        )

    def _detect_node_type(self, sentence: str) -> NodeType | None:
        s = sentence.lower()
        if any(v in s for v in self.identity_verbs) and any(p in s for p in ("i am", "he is", "you are")):
            return NodeType.IDENTITY
        if any(v in s for v in self.effect_verbs):
            return NodeType.EFFECT
        if any(v in s for v in self.enactment_verbs):
            return NodeType.ENACTMENT
        if ('"' in sentence or "'" in sentence) and "said" in s:
            return NodeType.DIALOGUE
        return NodeType.ENACTMENT

    def _build_edges(self, nodes: list[NarrativeNode]) -> list[NarrativeEdge]:
        edges: list[NarrativeEdge] = []
        for i, node in enumerate(nodes):
            if i < len(nodes) - 1:
                nxt = nodes[i + 1]
                edges.append(
                    NarrativeEdge(
                        id=f"e{i + 1}_{short_hash(f'{node.id}-{nxt.id}')}" ,
                        from_id=node.id,
                        to_id=nxt.id,
                        type=EdgeType.IMPLIES,
                        confidence=0.7,
                        theological_weight=self._weight(node, nxt),
                    )
                )

            if node.type == NodeType.IDENTITY:
                target = next((n for n in nodes[i + 1 : i + 5] if n.type == NodeType.ENACTMENT), None)
                if target:
                    edges.append(
                        NarrativeEdge(
                            id=f"e_identity_{i}_{short_hash(target.id)}",
                            from_id=node.id,
                            to_id=target.id,
                            type=EdgeType.GROUNDS,
                            confidence=0.85,
                            theological_weight=0.9,
                        )
                    )

            if node.type == NodeType.ENACTMENT:
                target = next((n for n in nodes[i + 1 : i + 3] if n.type == NodeType.EFFECT), None)
                if target:
                    edges.append(
                        NarrativeEdge(
                            id=f"e_enactment_{i}_{short_hash(target.id)}",
                            from_id=node.id,
                            to_id=target.id,
                            type=EdgeType.PRODUCES,
                            confidence=0.9,
                            theological_weight=0.95,
                        )
                    )
        return edges

    def _weight(self, node1: NarrativeNode, node2: NarrativeNode) -> float:
        weight = 0.5
        if node1.type == NodeType.IDENTITY and node2.type == NodeType.ENACTMENT:
            weight += 0.4
        if node1.type == NodeType.ENACTMENT and node2.type == NodeType.EFFECT:
            weight += 0.45
        if node1.type == NodeType.DIALOGUE or node2.type == NodeType.DIALOGUE:
            weight += 0.2
        return min(weight, 1.0)
