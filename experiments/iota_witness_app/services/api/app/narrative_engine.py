from __future__ import annotations

from app.motif_detector import MotifDetector
from app.narrative_models import EdgeType, NarrativeEdge, NarrativeGraph, NarrativeNode, NodeType
from app.narrative_utils import graph_id, hash_fragment, split_sentences


class NarrativeEngine:
    def __init__(self) -> None:
        self.identity_verbs = {
            "am",
            "is",
            "are",
            "called",
            "named",
            "declared",
            "revealed",
            "identified",
            "known",
            "confessed",
        }
        self.effect_verbs = {
            "healed",
            "cleansed",
            "restored",
            "raised",
            "forgiven",
            "delivered",
            "saved",
            "changed",
            "transformed",
            "became",
        }
        self.enactment_verbs = {
            "said",
            "went",
            "came",
            "took",
            "gave",
            "did",
            "spoke",
            "commanded",
            "taught",
            "preached",
        }
        self.motif_detector = MotifDetector()

    async def analyze(
        self,
        text: str,
        reference: str,
        lemmas: list[list[str]] | None = None,
        strongs: list[list[str]] | None = None,
    ) -> NarrativeGraph:
        sentences = split_sentences(text)
        nodes: list[NarrativeNode] = []
        for idx, sentence in enumerate(sentences):
            node = self._sentence_to_node(
                sentence=sentence,
                reference=reference,
                index=idx,
                lemmas=(lemmas[idx] if lemmas and idx < len(lemmas) else []),
                strongs=(strongs[idx] if strongs and idx < len(strongs) else []),
            )
            if node is not None:
                nodes.append(node)

        edges = self._build_edges(nodes)
        motifs = self.motif_detector.detect(nodes, edges)
        return NarrativeGraph(
            id=graph_id(reference),
            primary_reference=reference,
            nodes=nodes,
            edges=edges,
            motifs=motifs,
            metadata={
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
        node_id = f"n{index + 1}_{hash_fragment(sentence)}"
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
        has_identity_trigger = any(v in s for v in self.identity_verbs)
        has_identity_phrase = "i am" in s or "he is" in s or "you are" in s
        if has_identity_trigger and has_identity_phrase:
            return NodeType.IDENTITY
        if any(v in s for v in self.effect_verbs):
            return NodeType.EFFECT
        has_quote = ('"' in sentence) or ("'" in sentence)
        if has_quote and "said" in s:
            return NodeType.DIALOGUE
        if any(v in s for v in self.enactment_verbs):
            return NodeType.ENACTMENT
        return NodeType.ENACTMENT

    def _build_edges(self, nodes: list[NarrativeNode]) -> list[NarrativeEdge]:
        edges: list[NarrativeEdge] = []
        for i, node in enumerate(nodes):
            if i < len(nodes) - 1:
                nxt = nodes[i + 1]
                edges.append(
                    NarrativeEdge(
                        id=f"e{i + 1}_{hash_fragment(f'{node.id}-{nxt.id}')}",
                        from_id=node.id,
                        to_id=nxt.id,
                        type=EdgeType.IMPLIES,
                        confidence=0.7,
                        theological_weight=self._theological_weight(node, nxt),
                    )
                )

            if node.type == NodeType.IDENTITY:
                target = next(
                    (n for n in nodes[i + 1 : i + 5] if n.type == NodeType.ENACTMENT),
                    None,
                )
                if target:
                    edges.append(
                        NarrativeEdge(
                            id=f"e_ground_{i}_{hash_fragment(target.id)}",
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
                            id=f"e_prod_{i}_{hash_fragment(target.id)}",
                            from_id=node.id,
                            to_id=target.id,
                            type=EdgeType.PRODUCES,
                            confidence=0.9,
                            theological_weight=0.95,
                        )
                    )
        return edges

    def _theological_weight(self, node_a: NarrativeNode, node_b: NarrativeNode) -> float:
        weight = 0.5
        if node_a.type == NodeType.IDENTITY and node_b.type == NodeType.ENACTMENT:
            weight += 0.4
        if node_a.type == NodeType.ENACTMENT and node_b.type == NodeType.EFFECT:
            weight += 0.45
        if node_a.type == NodeType.DIALOGUE or node_b.type == NodeType.DIALOGUE:
            weight += 0.2
        return min(weight, 1.0)
