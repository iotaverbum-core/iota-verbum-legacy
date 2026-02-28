from __future__ import annotations

import argparse
import json

from iota_verbum.core_bridge import CoreBridgeError, run_biblical_text, verify_output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="iv", description="Legacy CLI wrapper for pinned iota-verbum-core.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a pinned Core pipeline through the legacy bridge.")
    run_parser.add_argument("domain", choices=["biblical_text"])
    run_parser.add_argument("--dataset", required=True)
    run_parser.add_argument("--ref", required=True)
    run_parser.add_argument("--out", required=True)
    run_parser.add_argument("--context", action="append", default=[])

    verify_parser = subparsers.add_parser("verify", help="Verify a Core output directory.")
    verify_parser.add_argument("out_dir")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "run":
            payload = run_biblical_text(args.dataset, args.ref, args.out, args.context)
        else:
            payload = verify_output(args.out_dir)
    except CoreBridgeError as exc:
        parser.exit(1, f"{exc}\n")

    print(json.dumps(payload, indent=2))
    return 0
