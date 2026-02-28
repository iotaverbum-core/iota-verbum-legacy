from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .attest import attest_text
from .canonicalize import canonicalize_text
from .parser import ParseError, parse_modal_code
from .validate import validate_document


def _read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def _write_text(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def _write_json(path: str, data: object) -> None:
    text = json.dumps(data, sort_keys=True, indent=2)
    _write_text(path, text + "\n")


def cmd_parse(args: argparse.Namespace) -> int:
    text = _read_text(args.input)
    doc = parse_modal_code(text)
    attest = attest_text(text)
    doc.attestation = {
        "input_sha256": attest["input_sha256"],
        "canonical_sha256": attest["canonical_text_sha256"],
    }
    payload = doc.to_dict()
    if args.output:
        _write_json(args.output, payload)
    else:
        print(json.dumps(payload, sort_keys=True, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    text = _read_text(args.input)
    try:
        doc = parse_modal_code(text)
    except ParseError as exc:
        print(str(exc))
        return 2
    errors = validate_document(doc)
    if errors:
        for line_no, message in errors:
            if line_no:
                print(f"Line {line_no}: {message}")
            else:
                print(message)
        return 2
    print("OK")
    return 0


def cmd_canonicalize(args: argparse.Namespace) -> int:
    text = _read_text(args.input)
    canonical = canonicalize_text(text)
    if args.output:
        _write_text(args.output, canonical)
    else:
        print(canonical, end="")
    return 0


def cmd_attest(args: argparse.Namespace) -> int:
    text = _read_text(args.input)
    attest = attest_text(text)
    if args.output:
        _write_json(args.output, attest)
    else:
        print(json.dumps(attest, sort_keys=True, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="iota_verbum.modal_code")
    sub = parser.add_subparsers(dest="command", required=True)

    p_parse = sub.add_parser("parse", help="Parse modal_code into JSON AST")
    p_parse.add_argument("--in", dest="input", required=True)
    p_parse.add_argument("--out", dest="output")
    p_parse.set_defaults(func=cmd_parse)

    p_validate = sub.add_parser("validate", help="Validate modal_code")
    p_validate.add_argument("--in", dest="input", required=True)
    p_validate.set_defaults(func=cmd_validate)

    p_canon = sub.add_parser("canonicalize", help="Canonicalize modal_code")
    p_canon.add_argument("--in", dest="input", required=True)
    p_canon.add_argument("--out", dest="output")
    p_canon.set_defaults(func=cmd_canonicalize)

    p_attest = sub.add_parser("attest", help="Attest modal_code hashes")
    p_attest.add_argument("--in", dest="input", required=True)
    p_attest.add_argument("--out", dest="output")
    p_attest.set_defaults(func=cmd_attest)

    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
