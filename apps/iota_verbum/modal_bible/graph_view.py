from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set, Dict, List, Tuple
import re

from modal_bible.models import ModalPassage


OPERATOR_PATTERN = re.compile(r"\b(\[\]|<>|EFF|box|diamond|eff)\b|(\bRS\b)")
ENTITY_PATTERN = re.compile(r"\b(YHWH|Psalmist|Christ|Nations|Israel|Enemies|FutureGeneration|Church)\b")


@dataclass
class LambdaGraph:
    """
    A minimal graph-view over a ModalPassage.
    Nodes are just strings for now (operators, entities, statement IDs).
    Edges connect statement IDs to the operators/entities they use.
    """
    passage_id: str
    operator_nodes: Set[str] = field(default_factory=set)
    entity_nodes: Set[str] = field(default_factory=set)
    statement_nodes: Set[str] = field(default_factory=set)
    edges: List[Tuple[str, str, str]] = field(default_factory=list)
    # edges: (from_node, relation, to_node)

    @classmethod
    def from_passage(cls, passage: ModalPassage) -> "LambdaGraph":
        graph = cls(passage_id=passage.passage_id)

        for unit in passage.units:
            for stmt in unit.statements:
                graph.statement_nodes.add(stmt.id)
                for line in stmt.lambda_iv:
                    # Find operators and RS predicate
                    for match in OPERATOR_PATTERN.finditer(line):
                        op = match.group(0)
                        if op:
                            graph.operator_nodes.add(op)
                            graph.edges.append((stmt.id, "uses_operator", op))

                    # Find key entities (simplistic, first pass)
                    for ent in ENTITY_PATTERN.findall(line):
                        if ent:
                            graph.entity_nodes.add(ent)
                            graph.edges.append((stmt.id, "mentions_entity", ent))

        return graph

    def to_adjacency(self) -> Dict[str, List[Tuple[str, str]]]:
        """
        Simple adjacency list: node -> list of (relation, target).
        """
        adj: Dict[str, List[Tuple[str, str]]] = {}
        for src, rel, dst in self.edges:
            adj.setdefault(src, []).append((rel, dst))
        return adj
