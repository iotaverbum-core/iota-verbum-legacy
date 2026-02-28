import re

VERSE_REF_PATTERN = re.compile(
    r"\[Gen\s+\d+:\d+(-\d+)?(\s*[-–]\s*\d+:\d+)?\]"
)

NODE_PREFIXES = {
    "□L::": "ground",
    "@SCENE::": "scene",
    "→H::": "hinge",
    "◇E::": "enactment",
}

OUTCOME_PREFIX = "⊢"
RUPTURE_MARKER = "⟂"
HR_CHAR = "─"
