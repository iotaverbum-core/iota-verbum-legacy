import json

from iota_verbum import cli


def test_run_command_delegates_to_core_bridge(monkeypatch, capsys, tmp_path):
    expected = {
        "resolved_ref": "John 4:7-10",
        "out_dir": str(tmp_path),
        "artifacts": {"output": str(tmp_path / "output.json")},
    }

    def fake_run(dataset, ref, out, context):
        assert dataset == "esv_sample"
        assert ref == "john_4_7_10"
        assert out == str(tmp_path)
        assert context == ["moment=smoke test"]
        return expected

    monkeypatch.setattr(cli, "run_biblical_text", fake_run)

    rc = cli.main(
        [
            "run",
            "biblical_text",
            "--dataset",
            "esv_sample",
            "--ref",
            "john_4_7_10",
            "--out",
            str(tmp_path),
            "--context",
            "moment=smoke test",
        ]
    )

    assert rc == 0
    assert json.loads(capsys.readouterr().out) == expected


def test_verify_command_delegates_to_core_bridge(monkeypatch, capsys, tmp_path):
    expected = {
        "out_dir": str(tmp_path),
        "verification": {
            "attestation_match": True,
            "template_match": True,
            "input_match": True,
        },
    }

    monkeypatch.setattr(cli, "verify_output", lambda out_dir: expected)
    rc = cli.main(["verify", str(tmp_path)])

    assert rc == 0
    assert json.loads(capsys.readouterr().out) == expected
