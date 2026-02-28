from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_PIN = "iota-verbum-core @ git+https://github.com/iotaverbum-core/iota-verbum-core.git@v0.1.0-core-canonical"


def _venv_paths(venv_dir: Path) -> tuple[Path, Path]:
    if os.name == "nt":
        bin_dir = venv_dir / "Scripts"
        return bin_dir / "python.exe", bin_dir
    bin_dir = venv_dir / "bin"
    return bin_dir / "python", bin_dir


def _run(command: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, check=True)


def test_clean_venv_installs_pinned_core_and_runs_end_to_end(tmp_path: Path):
    venv_dir = tmp_path / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    python_exe, bin_dir = _venv_paths(venv_dir)
    env = os.environ.copy()
    env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
    env["IV_LEGACY_ROOT"] = str(ROOT)

    install_spec = env.get("IV_CORE_INSTALL_SPEC", CORE_PIN)
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    assert CORE_PIN in requirements

    _run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"], ROOT, env)
    _run([str(python_exe), "-m", "pip", "install", "--no-build-isolation", install_spec], ROOT, env)
    _run([str(python_exe), "-m", "pip", "install", "--no-build-isolation", "."], ROOT, env)

    pip_show_core = _run([str(python_exe), "-m", "pip", "show", "iota-verbum-core"], ROOT, env)
    assert "Name: iota-verbum-core" in pip_show_core.stdout
    print("pip show iota-verbum-core")
    print(pip_show_core.stdout.strip())

    pip_freeze = _run([str(python_exe), "-m", "pip", "freeze"], ROOT, env)
    print("pip freeze")
    print(pip_freeze.stdout.strip())
    assert "iota-verbum-core" in pip_freeze.stdout

    module_file = _run(
        [str(python_exe), "-c", "import inspect, deterministic_ai; print(inspect.getfile(deterministic_ai))"],
        tmp_path,
        env,
    ).stdout.strip()
    print("inspect.getfile(deterministic_ai)")
    print(module_file)
    assert "site-packages" in module_file or "dist-packages" in module_file
    assert str(ROOT) not in module_file
    assert "iota-verbum-core\\src" not in module_file
    assert "iota-verbum-core/src" not in module_file
    assert "C:\\iotaverbum\\iota-verbum-core" not in module_file
    assert "/iotaverbum/iota-verbum-core" not in module_file

    iv_path = bin_dir / ("iv.exe" if os.name == "nt" else "iv")
    out_dir = tmp_path / "run"

    run_result = _run(
        [
            str(iv_path),
            "run",
            "biblical_text",
            "--dataset",
            "esv_sample",
            "--ref",
            "john_4_7_10",
            "--out",
            str(out_dir),
        ],
        ROOT,
        env,
    )
    run_payload = json.loads(run_result.stdout)
    print("iv run stdout")
    print(run_result.stdout.strip())

    assert (out_dir / "output.json").exists()
    assert (out_dir / "provenance.json").exists()
    assert (out_dir / "attestation.sha256").exists()
    assert run_payload["core"]["module_in_site_packages"] is True
    assert Path(run_payload["artifacts"]["output"]).exists()
    assert Path(run_payload["artifacts"]["provenance"]).exists()
    assert Path(run_payload["artifacts"]["attestation"]).exists()

    verify_result = _run([str(iv_path), "verify", str(out_dir)], ROOT, env)
    verify_payload = json.loads(verify_result.stdout)
    print("iv verify stdout")
    print(verify_result.stdout.strip())
    assert verify_payload["verification"]["attestation_match"] is True
    assert verify_payload["verification"]["template_match"] is True
    assert verify_payload["verification"]["input_match"] is True
