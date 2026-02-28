import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from iota_verbum.modal_code.attest import attest_text
from iota_verbum.modal_code.canonicalize import canonicalize_text


FIXTURE = Path("tests/fixtures/genesis_1_3.modal.txt")


def _run_cli(args: list[str]) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "iota_verbum.modal_code"] + args
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")


def test_modal_code_cli_roundtrip():
    text = FIXTURE.read_text(encoding="utf-8")
    expected_attest = attest_text(text)

    with TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        out_json = tmp / "genesis.json"
        out_canon = tmp / "genesis.canon.txt"
        out_attest = tmp / "genesis.attest.json"

        result = _run_cli(["parse", "--in", str(FIXTURE), "--out", str(out_json)])
        assert result.returncode == 0, result.stderr
        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["meta"]["format"] == "iota_verbum::modal_code"
        assert "attestation" in payload

        result = _run_cli(["validate", "--in", str(FIXTURE)])
        assert result.returncode == 0
        assert "OK" in result.stdout

        result = _run_cli(
            ["canonicalize", "--in", str(FIXTURE), "--out", str(out_canon)]
        )
        assert result.returncode == 0, result.stderr
        canon_text = out_canon.read_text(encoding="utf-8")
        assert canon_text.endswith("\n")
        assert canon_text == canonicalize_text(text)

        result = _run_cli(["attest", "--in", str(FIXTURE), "--out", str(out_attest)])
        assert result.returncode == 0, result.stderr
        attest_payload = json.loads(out_attest.read_text(encoding="utf-8"))
        assert attest_payload == expected_attest
