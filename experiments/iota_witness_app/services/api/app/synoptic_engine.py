from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

from app.narrative_models import NarrativeGraph, ParallelGospel


class SynopticEngine:
    GOSPEL_PARALLELS: dict[str, dict[str, dict[str, Any]]] = {
        "Mark 5:21-43": {
            "Matthew 9:18-26": {
                "confidence": 0.95,
                "type": "direct",
                "differences": [
                    "Matthew compresses the intercalation.",
                    "Matthew omits the Aramaic phrase Talitha koum.",
                ],
            },
            "Luke 8:40-56": {
                "confidence": 0.95,
                "type": "direct",
                "differences": [
                    "Luke follows Mark's structure closely.",
                    "Luke includes additional condition details.",
                ],
            },
        }
    }

    async def find_parallels(self, reference: str) -> dict[str, ParallelGospel]:
        parallels: dict[str, ParallelGospel] = {}
        for ref, data in self.GOSPEL_PARALLELS.get(reference, {}).items():
            parallels[ref] = ParallelGospel(
                gospel=ref.split()[0],
                reference=ref,
                graph_differences={
                    "type": data["type"],
                    "differences": data.get("differences", []),
                },
                theological_significance=self._theological_significance(reference, ref),
            )
        return parallels

    async def compare_graphs(self, a: NarrativeGraph, b: NarrativeGraph) -> dict[str, Any]:
        node_similarity = self._seq_ratio([n.type for n in a.nodes], [n.type for n in b.nodes])
        edge_similarity = self._seq_ratio([e.type for e in a.edges], [e.type for e in b.edges])
        motif_similarity = self._set_ratio({m.name for m in a.motifs}, {m.name for m in b.motifs})
        return {
            "overall_similarity": (node_similarity + edge_similarity + motif_similarity) / 3,
            "node_similarity": node_similarity,
            "edge_similarity": edge_similarity,
            "motif_similarity": motif_similarity,
        }

    def _seq_ratio(self, left: list[Any], right: list[Any]) -> float:
        if not left or not right:
            return 0.0
        return SequenceMatcher(None, str(left), str(right)).ratio()

    def _set_ratio(self, left: set[str], right: set[str]) -> float:
        union = left.union(right)
        if not union:
            return 0.0
        return len(left.intersection(right)) / len(union)

    def _theological_significance(self, ref_a: str, ref_b: str) -> str | None:
        significance_map = {
            ("Mark 5:21-43", "Matthew 9:18-26"): "Matthew streamlines to foreground authority.",
            ("Mark 5:21-43", "Luke 8:40-56"): "Luke emphasizes restoration through detail.",
        }
        return significance_map.get((ref_a, ref_b))
