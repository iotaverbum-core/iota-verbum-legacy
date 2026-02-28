from pathlib import Path

from iota_verbum.modal_code.attest import attest_text
from iota_verbum.modal_code.canonicalize import canonicalize_text
from iota_verbum.modal_code.parser import parse_modal_code


FIXTURE_PATH = Path("tests/fixtures/genesis_1_3.modal.txt")


def test_modal_code_golden():
    text = FIXTURE_PATH.read_text(encoding="utf-8")
    doc = parse_modal_code(text)
    canonical = canonicalize_text(text)
    doc2 = parse_modal_code(canonical)

    assert doc.to_dict() == doc2.to_dict()
    assert canonicalize_text(canonical) == canonical

    attest = attest_text(text)
    expected = {
        "input_sha256": "e1632ce019cbba5a86ce6a37dfc4bdf8db0c68e772b1ff5cba965bee2d576811",
        "canonical_text_sha256": "eef920dc9e6dfb7f5f470c0aa90861ace05100d4c41b0d4d38612c4b82865e39",
        "ast_sha256": "b726e1b5bbbe8e9594c3563ba4433eee402cf3629b3dc6605fea102a27451be8",
        "combined_sha256": "02f9898de729c327702648cbb1de2e39599edfccc9937fcab7e46021c204c2a9",
    }
    assert attest == expected
