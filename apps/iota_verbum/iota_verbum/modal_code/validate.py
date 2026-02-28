from __future__ import annotations

from typing import Any, Iterable, List, Tuple

from .model import EnactmentNode, ModalDocument, SceneNode
from .schema import VERSE_REF_PATTERN


def _is_valid_value(value: Any) -> bool:
    if isinstance(value, (str, bool, int, float)):
        return True
    if isinstance(value, list):
        return all(_is_valid_value(v) for v in value)
    if isinstance(value, dict):
        return all(
            isinstance(k, str) and _is_valid_value(v) for k, v in value.items()
        )
    return False


def _collect_nodes(doc: ModalDocument) -> Iterable[Any]:
    for node in doc.nodes:
        yield node
    for scene in doc.scenes:
        yield scene


def validate_document(doc: ModalDocument) -> List[Tuple[int, str]]:
    errors: List[Tuple[int, str]] = []
    seen_ids = {}

    for node in _collect_nodes(doc):
        node_id = getattr(node, "id", None)
        line_no = getattr(node, "line_no", 0) or 0
        if not node_id:
            errors.append((line_no, "Node missing id"))
            continue
        scene_id = getattr(node, "_scene_id", None)
        uniq_key = (scene_id, node_id) if scene_id else node_id
        if uniq_key in seen_ids:
            errors.append((line_no, f"Duplicate id: {node_id}"))
        else:
            seen_ids[uniq_key] = line_no

        verse_refs = getattr(node, "verse_refs", [])
        for ref in verse_refs:
            if not VERSE_REF_PATTERN.fullmatch(ref):
                errors.append((line_no, f"Invalid verse ref: {ref}"))

        fields = getattr(node, "fields", None)
        if fields is not None and not _is_valid_value(fields):
            errors.append((line_no, f"Invalid field types in node {node_id}"))

        if isinstance(node, EnactmentNode):
            for outcome in node.outcomes:
                if not _is_valid_value(outcome.value):
                    errors.append(
                        (line_no, f"Invalid outcome value in {node_id}: {outcome.key}")
                    )

    node_ids = {n.id for n in doc.nodes}
    for scene in doc.scenes:
        line_no = scene.line_no or 0
        for child_id in scene.children:
            if child_id not in node_ids:
                errors.append(
                    (line_no, f"Scene {scene.id} references unknown node {child_id}")
                )

    return errors
