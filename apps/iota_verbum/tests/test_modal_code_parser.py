from iota_verbum.modal_code.parser import ParseError, parse_modal_code


def test_tabs_are_invalid():
    text = "iota_verbum :: modal_code\n\t□L::GOD\n"
    try:
        parse_modal_code(text)
    except ParseError as exc:
        assert "Tabs are not allowed" in str(exc)
    else:
        raise AssertionError("Expected ParseError for tabs")


def test_outcome_requires_enactment():
    text = "\n".join(
        [
            "iota_verbum :: modal_code",
            "@SCENE::A [Gen 1:1]",
            "  →H::SAY [Gen 1:1]",
            "    speaker: □L::GOD",
            "    ⊢ effect: test",
        ]
    )
    try:
        parse_modal_code(text)
    except ParseError as exc:
        assert "Outcome found outside Enactment node" in str(exc)
    else:
        raise AssertionError("Expected ParseError for outcome outside enactment")
