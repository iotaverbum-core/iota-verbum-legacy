from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List

from .model import EnactmentNode, ModalDocument, Outcome, SceneNode
from .schema import HR_CHAR, RUPTURE_MARKER

HR_LINE = HR_CHAR * 87


def _sorted_keys(keys: Iterable[str]) -> List[str]:
    keys = list(keys)
    priority = []
    for key in ["name", "identity"]:
        if key in keys:
            priority.append(key)
            keys.remove(key)
    return priority + sorted(keys)


def _needs_quotes(value: str) -> bool:
    if value == "":
        return True
    if re.search(r"\\s", value):
        return True
    if any(ch in value for ch in ['"', ":", "#"]):
        return True
    return False


def _format_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        if _needs_quotes(value):
            escaped = value.replace('"', '\\"')
            return f"\"{escaped}\""
        return value
    return str(value)


def _render_value(value: Any, indent: int) -> List[str]:
    lines: List[str] = []
    if isinstance(value, dict):
        for key in _sorted_keys(value.keys()):
            val = value[key]
            if isinstance(val, (dict, list)):
                lines.append(" " * indent + f"{key}:")
                lines.extend(_render_value(val, indent + 2))
            else:
                lines.append(" " * indent + f"{key}: {_format_scalar(val)}")
        return lines
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                if len(item) == 1:
                    k, v = next(iter(item.items()))
                    if isinstance(v, (dict, list)):
                        lines.append(" " * indent + f"- {k}:")
                        lines.extend(_render_value(v, indent + 2))
                    else:
                        lines.append(
                            " " * indent + f"- {k}: {_format_scalar(v)}"
                        )
                else:
                    lines.append(" " * indent + "-")
                    lines.extend(_render_value(item, indent + 2))
            else:
                lines.append(" " * indent + f"- {_format_scalar(item)}")
        return lines
    lines.append(" " * indent + _format_scalar(value))
    return lines


def _render_outcomes(outcomes: List[Outcome], indent: int) -> List[str]:
    lines: List[str] = []
    for outcome in outcomes:
        prefix = "⊢"
        if outcome.rupture:
            prefix += f" {RUPTURE_MARKER}"
        value = outcome.value
        if isinstance(value, (dict, list)):
            lines.append(" " * indent + f"{prefix} {outcome.key}:")
            lines.extend(_render_value(value, indent + 2))
        elif value is True:
            lines.append(" " * indent + f"{prefix} {outcome.key}: true")
        else:
            lines.append(
                " " * indent + f"{prefix} {outcome.key}: {_format_scalar(value)}"
            )
    return lines


def _render_node_header(node_id: str, verse_refs: List[str]) -> str:
    if verse_refs:
        return f"{node_id} {' '.join(verse_refs)}"
    return node_id


def _render_node(node: Any, indent: int) -> List[str]:
    lines: List[str] = []
    lines.append(" " * indent + _render_node_header(node.id, node.verse_refs))
    if hasattr(node, "fields"):
        lines.extend(_render_value(node.fields, indent + 2))
    if isinstance(node, EnactmentNode):
        lines.extend(_render_outcomes(node.outcomes, indent + 2))
    return lines


def render_document(doc: ModalDocument) -> str:
    lines: List[str] = []

    legend_parts: List[str] = []
    if doc.legend:
        legend_parts.append("# Legend:")
        for symbol in _sorted_keys(doc.legend.keys()):
            legend_parts.append(f"# {symbol} = {doc.legend[symbol]}")
    header = f"iota_verbum :: modal_code"
    if doc.meta.get("source_title"):
        header += f" # Text: {doc.meta['source_title']}"
    if legend_parts:
        header += " " + " ".join(legend_parts)
    lines.append(header)
    lines.append(HR_LINE)

    def _in_scene(node: Any) -> bool:
        if hasattr(node, "_in_scene"):
            return bool(getattr(node, "_in_scene"))
        return any(node.id in scene.children for scene in doc.scenes)

    ground_nodes = [n for n in doc.nodes if n.id.startswith("□L::") and not _in_scene(n)]
    top_level_other_nodes = [
        n for n in doc.nodes if not _in_scene(n) and not n.id.startswith("□L::")
    ]

    for node in ground_nodes:
        lines.extend(_render_node(node, 0))
    if ground_nodes:
        lines.append(HR_LINE)

    for scene in doc.scenes:
        lines.append(_render_node_header(scene.id, scene.verse_refs))
        scene_nodes = [n for n in doc.nodes if getattr(n, "_scene_id", None) == scene.id]
        if scene_nodes:
            for child in scene_nodes:
                lines.extend(_render_node(child, 2))
        else:
            queue_by_id: Dict[str, List[Any]] = {}
            for n in doc.nodes:
                queue_by_id.setdefault(n.id, []).append(n)
            for child_id in scene.children:
                bucket = queue_by_id.get(child_id, [])
                if not bucket:
                    continue
                child = bucket.pop(0)
                lines.extend(_render_node(child, 2))
        lines.append(HR_LINE)

    if top_level_other_nodes:
        for node in top_level_other_nodes:
            lines.extend(_render_node(node, 0))
        lines.append(HR_LINE)

    if lines and lines[-1] == HR_LINE:
        lines.pop()

    return "\n".join(lines) + "\n"
