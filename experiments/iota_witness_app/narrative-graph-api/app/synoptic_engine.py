from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

from app.models import NarrativeGraph, ParallelGospel


class SynopticEngine:
    GOSPEL_PARALLELS: dict[str, dict[str, dict[str, Any]]] = {
        "Mark 5:21-43": {
            "Matthew 9:18-26": {
                "confidence": 0.95,
                "type": "direct",
                "differences": [
                    "Matthew compresses the intercalation",
                    "Matthew omits the Aramaic phrase Talitha koum",
                ],
            },
            "Luke 8:40-56": {
                "confidence": 0.95,
                "type": "direct",
                "differences": [
                    "Luke follows Mark's structure closely",
                    "Luke adds details about the woman's condition",
                ],
            },
        }
    }

    async def find_parallels(self, reference: str) -> dict[str, ParallelGospel]:
        result: dict[str, ParallelGospel] = {}
        for ref, data in self.GOSPEL_PARALLELS.get(reference, {}).items():
            result[ref] = ParallelGospel(
                gospel=ref.split()[0],
                reference=ref,
                graph_differences={"type": data["type"], "differences": data.get("differences", [])},
                theological_significance=self._get_theological_significance(reference, ref),
            )
        return result

    async def compare_graphs(self, graph1: NarrativeGraph, graph2: NarrativeGraph) -> dict[str, Any]:
        node_similarity = self._ratio([n.type for n in graph1.nodes], [n.type for n in graph2.nodes])
        edge_similarity = self._ratio([e.type for e in graph1.edges], [e.type for e in graph2.edges])
        motif_similarity = self._set_ratio({m.name for m in graph1.motifs}, {m.name for m in graph2.motifs})
        return {
            "overall_similarity": (node_similarity + edge_similarity + motif_similarity) / 3,
            "node_similarity": node_similarity,
            "edge_similarity": edge_similarity,
            "motif_similarity": motif_similarity,
        }

    def _ratio(self, left: list[Any], right: list[Any]) -> float:
        if not left or not right:
            return 0.0
        return SequenceMatcher(None, str(left), str(right)).ratio()

    def _set_ratio(self, left: set[str], right: set[str]) -> float:
        union = left.union(right)
        if not union:
            return 0.0
        return len(left.intersection(right)) / len(union)

    def _get_theological_significance(self, ref1: str, ref2: str) -> str | None:
        significance_map = {
            ("Mark 5:21-43", "Matthew 9:18-26"): "Matthew emphasizes authority by streamlining the narrative",
            ("Mark 5:21-43", "Luke 8:40-56"): "Luke highlights restoration through additional detail",
        }
        return significance_map.get((ref1, ref2))
