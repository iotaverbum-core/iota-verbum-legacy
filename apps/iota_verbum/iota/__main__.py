from __future__ import annotations

import argparse
import json
from pathlib import Path

from core import attestation
from core.conscience.extractor import GroundTruthExtractor


def _load_input(domain: str, input_path: Path):
    data_bytes = input_path.read_bytes()
    if domain == "biblical_text":
        return data_bytes.decode("utf-8")
    return json.loads(data_bytes.decode("utf-8-sig"))


def run_extract(args: argparse.Namespace) -> int:
    extractor = GroundTruthExtractor(args.domain)
    input_path = Path(args.input)
    input_data = _load_input(args.domain, input_path)
    ground_truth = extractor.extract(input_data, input_ref=args.input_ref)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    attestation.write_json(out_dir / "ground_truth.json", ground_truth)
    attestation.write_text(
        out_dir / "attestation.sha256",
        ground_truth["attestation_sha256"] + "\n",
    )
    attestation.write_json(out_dir / "deterministic_output.json", ground_truth["deterministic_output"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="iota", description="Iota Verbum CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    extract = sub.add_parser("extract", help="Extract ground truth for ConScience.")
    extract.add_argument("--domain", required=True)
    extract.add_argument("--input", required=True)
    extract.add_argument("--input-ref")
    extract.add_argument("--out", required=True)
    extract.set_defaults(func=run_extract)
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
