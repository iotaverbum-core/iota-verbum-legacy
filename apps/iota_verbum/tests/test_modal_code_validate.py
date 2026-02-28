from iota_verbum.modal_code.parser import parse_modal_code
from iota_verbum.modal_code.validate import validate_document


def test_invalid_verse_ref():
    text = "\n".join(
        [
            "iota_verbum :: modal_code",
            "□L::GOD [Gen 1:1-2x]",
            "  name: God",
        ]
    )
    doc = parse_modal_code(text)
    errors = validate_document(doc)
    assert any("Invalid verse ref" in msg for _, msg in errors)


def test_duplicate_ids():
    text = "\n".join(
        [
            "iota_verbum :: modal_code",
            "□L::GOD",
            "  name: God",
            "□L::GOD",
            "  name: God",
        ]
    )
    doc = parse_modal_code(text)
    errors = validate_document(doc)
    assert any("Duplicate id" in msg for _, msg in errors)
