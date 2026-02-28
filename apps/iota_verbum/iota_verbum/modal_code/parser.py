from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Dict, List, Optional, Tuple

from .model import (
    EnactmentNode,
    GroundNode,
    HingeNode,
    ModalDocument,
    Outcome,
    SceneNode,
)
from .schema import HR_CHAR, NODE_PREFIXES, OUTCOME_PREFIX, RUPTURE_MARKER


@dataclass
class ParseError(Exception):
    line_no: int
    message: str

    def __str__(self) -> str:
        return f"Line {self.line_no}: {self.message}"


LEGEND_ENTRY_RE = re.compile(r"(\\[v\\]|[@□◇→⊢⟂])\\s*=\\s*([^#]+)")
VERSE_REF_RE = re.compile(r"\[[^\]]+\]")


def _parse_legend(line: str) -> Dict[str, str]:
    legend: Dict[str, str] = {}
    for match in LEGEND_ENTRY_RE.finditer(line):
        symbol = match.group(1).strip()
        meaning = match.group(2).strip()
        legend[symbol] = meaning
    return legend


def _parse_source_title(line: str) -> str:
    if "Text:" not in line:
        return ""
    text_part = line.split("Text:", 1)[1]
    if "# Legend" in text_part:
        text_part = text_part.split("# Legend", 1)[0]
    return text_part.strip()


def _is_hr(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and all(ch == HR_CHAR for ch in stripped)


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.startswith('"') and value.endswith('"') and len(value) >= 2:
        try:
            import json

            return json.loads(value)
        except Exception:
            return value[1:-1]
    if value.startswith("'") and value.endswith("'") and len(value) >= 2:
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.isdigit():
        return int(value)
    try:
        if "." in value:
            return float(value)
    except ValueError:
        pass
    if value.startswith("[") and value.endswith("]"):
        try:
            import json

            return json.loads(value)
        except Exception:
            return value
    return value


def _parse_list_item(item: str) -> Any:
    item = item.strip()
    if ":" in item:
        key, rest = item.split(":", 1)
        key = key.strip()
        rest = rest.strip()
        if key and rest and re.fullmatch(r"[A-Za-z0-9_@\\-]+", key):
            return {key: _parse_scalar(rest)}
    return _parse_scalar(item)


def _parse_key_value(content: str) -> Tuple[str, Optional[str]]:
    if ":" not in content:
        return content.strip(), None
    key, rest = content.split(":", 1)
    key = key.strip()
    rest = rest.strip()
    if rest == "":
        return key, None
    return key, rest


def _find_prefix(content: str) -> Optional[str]:
    for prefix in NODE_PREFIXES.keys():
        if content.startswith(prefix):
            return prefix
    return None


class _FieldBuilder:
    def __init__(self, base_indent: int, line_no: int, root_container: Any = None) -> None:
        self.base_indent = base_indent
        if root_container is None:
            root_container = {}
        self.stack: List[Tuple[int, Any]] = [(base_indent, root_container)]
        self.line_no = line_no

    def _ensure_container(self, indent: int) -> Any:
        while self.stack and indent < self.stack[-1][0]:
            self.stack.pop()
        if not self.stack:
            raise ParseError(self.line_no, "Indentation underflow")
        if indent > self.stack[-1][0]:
            raise ParseError(self.line_no, "Unexpected indentation")
        return self.stack[-1][1]

    def add_key_value(
        self,
        indent: int,
        key: str,
        value: Optional[str],
        next_indent: Optional[int],
        next_is_list_item: bool,
    ) -> None:
        parent = self._ensure_container(indent)
        if not isinstance(parent, dict):
            raise ParseError(self.line_no, f"Cannot set key '{key}' on a list")
        if value is None:
            if next_indent is not None and next_indent > indent:
                if next_is_list_item:
                    child: Any = []
                else:
                    child = {}
                parent[key] = child
                self.stack.append((indent + 2, child))
            else:
                parent[key] = {}
        else:
            parent[key] = _parse_scalar(value)

    def add_list_item(self, indent: int, item: str) -> None:
        parent = self._ensure_container(indent)
        if not isinstance(parent, list):
            raise ParseError(self.line_no, "List item without list container")
        parent.append(_parse_list_item(item))


def parse_modal_code(text: str) -> ModalDocument:
    lines = text.splitlines()
    if not lines:
        raise ParseError(1, "Empty input")

    header_line = lines[0].lstrip("\ufeff")
    legend = _parse_legend(header_line)
    meta = {
        "format": "iota_verbum::modal_code",
        "source_title": _parse_source_title(header_line),
    }

    nodes: List[Any] = []
    scenes: List[SceneNode] = []
    scene_by_id: Dict[str, SceneNode] = {}
    current_scene: Optional[SceneNode] = None
    current_node: Optional[Any] = None
    current_node_indent: Optional[int] = None
    field_builder: Optional[_FieldBuilder] = None
    active_outcome_builder: Optional[_FieldBuilder] = None
    active_outcome_start_indent: Optional[int] = None

    def finalize_node() -> None:
        nonlocal current_node, field_builder, current_node_indent
        if current_node is None:
            return
        nodes.append(current_node)
        if current_scene is not None and hasattr(current_node, "id"):
            setattr(current_node, "_scene_id", current_scene.id)
            setattr(current_node, "_in_scene", True)
            current_scene.children.append(current_node.id)
        current_node = None
        current_node_indent = None
        field_builder = None

    def start_node(node: Any, indent: int, line_no: int) -> None:
        nonlocal current_node, current_node_indent, field_builder
        finalize_node()
        current_node = node
        current_node_indent = indent
        field_builder = _FieldBuilder(indent + 2, line_no, root_container=node.fields)

    for idx in range(1, len(lines)):
        raw_line = lines[idx]
        line_no = idx + 1
        if "\t" in raw_line:
            raise ParseError(line_no, "Tabs are not allowed")
        if not raw_line.strip():
            continue
        if _is_hr(raw_line):
            continue
        if raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        content = raw_line.strip()

        if active_outcome_builder is not None and active_outcome_start_indent is not None:
            if indent <= active_outcome_start_indent:
                active_outcome_builder = None
                active_outcome_start_indent = None
            else:
                active_outcome_builder.line_no = line_no
                if content.startswith("- "):
                    active_outcome_builder.add_list_item(indent, content[2:].strip())
                else:
                    next_indent = None
                    next_is_list_item = False
                    for j in range(idx + 1, len(lines)):
                        probe = lines[j]
                        if "\t" in probe:
                            raise ParseError(j + 1, "Tabs are not allowed")
                        if not probe.strip():
                            continue
                        if _is_hr(probe):
                            continue
                        if probe.lstrip().startswith("#"):
                            continue
                        next_indent = len(probe) - len(probe.lstrip(" "))
                        next_is_list_item = probe.strip().startswith("- ")
                        break
                    key, value = _parse_key_value(content)
                    active_outcome_builder.add_key_value(
                        indent,
                        key,
                        value,
                        next_indent,
                        next_is_list_item,
                    )
                continue

        prefix = _find_prefix(content)
        if prefix is not None:
            verse_refs = VERSE_REF_RE.findall(content)
            content_no_refs = VERSE_REF_RE.sub("", content).strip()
            node_id = content_no_refs
            if prefix == "@SCENE::":
                finalize_node()
                scene = SceneNode(id=node_id, verse_refs=verse_refs, line_no=line_no)
                scenes.append(scene)
                scene_by_id[node_id] = scene
                current_scene = scene
                current_node = None
                current_node_indent = None
                field_builder = None
            elif prefix == "□L::":
                start_node(
                    GroundNode(id=node_id, verse_refs=verse_refs, line_no=line_no),
                    indent,
                    line_no,
                )
            elif prefix == "→H::":
                start_node(
                    HingeNode(id=node_id, verse_refs=verse_refs, line_no=line_no),
                    indent,
                    line_no,
                )
            elif prefix == "◇E::":
                start_node(
                    EnactmentNode(id=node_id, verse_refs=verse_refs, line_no=line_no),
                    indent,
                    line_no,
                )
            else:
                raise ParseError(line_no, f"Unknown node prefix: {prefix}")
            continue

        if current_node is None:
            raise ParseError(line_no, "Field line found outside a node")
        if current_node_indent is None or indent <= current_node_indent:
            raise ParseError(line_no, "Field indentation must be greater than node line")

        if content.startswith(OUTCOME_PREFIX):
            if not isinstance(current_node, EnactmentNode):
                raise ParseError(line_no, "Outcome found outside Enactment node")
            outcome_text = content[len(OUTCOME_PREFIX) :].strip()
            rupture = False
            if outcome_text.startswith(RUPTURE_MARKER):
                rupture = True
                outcome_text = outcome_text[len(RUPTURE_MARKER) :].strip()
            key, value = _parse_key_value(outcome_text)
            if value is None:
                next_indent = None
                next_is_list_item = False
                for j in range(idx + 1, len(lines)):
                    probe = lines[j]
                    if "\t" in probe:
                        raise ParseError(j + 1, "Tabs are not allowed")
                    if not probe.strip():
                        continue
                    if _is_hr(probe):
                        continue
                    if probe.lstrip().startswith("#"):
                        continue
                    next_indent = len(probe) - len(probe.lstrip(" "))
                    next_is_list_item = probe.strip().startswith("- ")
                    break
                if next_indent is not None and next_indent > indent:
                    if next_is_list_item:
                        container: Any = []
                    else:
                        container = {}
                    current_node.outcomes.append(
                        Outcome(key=key, value=container, rupture=rupture)
                    )
                    active_outcome_builder = _FieldBuilder(
                        indent + 2, line_no, root_container=container
                    )
                    active_outcome_start_indent = indent
                else:
                    current_node.outcomes.append(
                        Outcome(key=key, value=True, rupture=rupture)
                    )
            else:
                current_node.outcomes.append(
                    Outcome(key=key, value=_parse_scalar(value), rupture=rupture)
                )
            continue

        if field_builder is None:
            raise ParseError(line_no, "Internal parser error: missing field builder")
        field_builder.line_no = line_no

        next_indent: Optional[int] = None
        next_is_list_item = False
        for j in range(idx + 1, len(lines)):
            probe = lines[j]
            if "\t" in probe:
                raise ParseError(j + 1, "Tabs are not allowed")
            if not probe.strip():
                continue
            if _is_hr(probe):
                continue
            if probe.lstrip().startswith("#"):
                continue
            next_indent = len(probe) - len(probe.lstrip(" "))
            next_is_list_item = probe.strip().startswith("- ")
            break

        if content.startswith("- "):
            item = content[2:].strip()
            field_builder.add_list_item(indent, item)
            continue

        key, value = _parse_key_value(content)
        field_builder.add_key_value(
            indent,
            key,
            value,
            next_indent,
            next_is_list_item,
        )

    finalize_node()

    ordered_nodes: List[Any] = []
    for n in nodes:
        if getattr(n, "_in_scene", False):
            continue
        if n.id.startswith("□L::"):
            ordered_nodes.append(n)

    for scene in scenes:
        for n in nodes:
            if getattr(n, "_scene_id", None) == scene.id:
                ordered_nodes.append(n)

    for n in nodes:
        if n not in ordered_nodes:
            ordered_nodes.append(n)

    return ModalDocument(meta=meta, legend=legend, nodes=ordered_nodes, scenes=scenes)
