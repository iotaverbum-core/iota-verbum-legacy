import json
from pathlib import Path

from iv_witness_card import main


def test_batch_generation(tmp_path: Path):
    out1 = tmp_path / "out1"
    out2 = tmp_path / "out2"
    csv_path = tmp_path / "batch.csv"

    csv_path.write_text(
        "passage,textfile,moment,out\n"
        f"John 1:14,,\"I feel tired but I'm staying.\",{out1.as_posix()}\n"
        f"John 1:14,,\"I feel overwhelmed but I'm present.\",{out2.as_posix()}\n",
        encoding="utf-8",
    )

    main(["--batchfile", str(csv_path)])

    expected = ["card.json", "card.md", "provenance.json", "attestation.sha256", "log.txt"]
    for p in [out1, out2]:
        for name in expected:
            assert (p / name).exists()

    batch_root = Path("outputs") / "witness_cards" / "_batch_runs"
    summaries = list(batch_root.glob("*/batch_summary.json"))
    assert summaries, "No batch_summary.json produced"

    summary = json.loads(summaries[-1].read_text(encoding="utf-8"))
    assert summary["rows_total"] == 2
    assert summary["rows_succeeded"] == 2
