from __future__ import annotations

import importlib.metadata as metadata
import json
import os
import re
import shutil
import subprocess
import sysconfig
from pathlib import Path


CORE_CLI = "deterministic-ai"
CORE_DIST = "iota-verbum-core"


class CoreBridgeError(RuntimeError):
    pass


def _candidate_legacy_roots() -> list[Path]:
    candidates: list[Path] = []

    env_root = os.environ.get("IV_LEGACY_ROOT")
    if env_root:
        candidates.append(Path(env_root))

    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    here = Path(__file__).resolve()
    candidates.extend([here.parent, *here.parents])

    seen: set[str] = set()
    unique: list[Path] = []
    for candidate in candidates:
        key = str(candidate).lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(candidate)
    return unique


def legacy_root() -> Path:
    for candidate in _candidate_legacy_roots():
        if (candidate / "data" / "scripture").exists():
            return candidate
    raise CoreBridgeError("Unable to locate legacy data root. Set IV_LEGACY_ROOT to the checkout path.")


def core_distribution() -> metadata.Distribution:
    try:
        return metadata.distribution(CORE_DIST)
    except metadata.PackageNotFoundError as exc:
        raise CoreBridgeError(f"{CORE_DIST} is not installed in the active environment.") from exc


def core_site_packages_root() -> Path:
    return Path(core_distribution().locate_file("")).resolve()


def core_module_file() -> Path:
    module_path = core_site_packages_root() / "deterministic_ai.py"
    if not module_path.exists():
        raise CoreBridgeError(f"Installed Core module not found at {module_path}.")
    return module_path


def core_console_script() -> Path:
    names = [CORE_CLI, f"{CORE_CLI}.exe", f"{CORE_CLI}.cmd"]
    for name in names:
        resolved = shutil.which(name)
        if resolved:
            return Path(resolved).resolve()

    scripts_dir = Path(sysconfig.get_path("scripts"))
    for name in names:
        candidate = scripts_dir / name
        if candidate.exists():
            return candidate.resolve()

    raise CoreBridgeError(f"Unable to locate the installed '{CORE_CLI}' console script.")


def inspect_core_install() -> dict:
    dist = core_distribution()
    module_path = core_module_file()
    path_text = str(module_path).lower()
    return {
        "distribution": dist.metadata.get("Name", CORE_DIST),
        "version": dist.version,
        "site_root": str(core_site_packages_root()),
        "module_path": str(module_path),
        "module_in_site_packages": "site-packages" in path_text or "dist-packages" in path_text,
    }


def _run_core(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [str(core_console_script()), *args]
    result = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise CoreBridgeError(
            "Core invocation failed.\n"
            f"command: {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _load_dataset_manifest(dataset: str) -> dict:
    manifest_path = legacy_root() / "data" / "scripture" / dataset / "manifest.json"
    if not manifest_path.exists():
        raise CoreBridgeError(f"Dataset manifest not found: {manifest_path}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def resolve_biblical_input(dataset: str, ref: str) -> tuple[str, Path]:
    manifest = _load_dataset_manifest(dataset)
    if ref in manifest:
        record = manifest[ref]
        return ref, (legacy_root() / "data" / "scripture" / dataset / record["file"]).resolve()

    wanted = _slug(ref)
    for canonical_ref, record in manifest.items():
        file_stem = Path(record["file"]).stem
        if _slug(canonical_ref) == wanted or _slug(file_stem) == wanted:
            return canonical_ref, (legacy_root() / "data" / "scripture" / dataset / record["file"]).resolve()

    raise CoreBridgeError(f"Reference '{ref}' was not found in dataset '{dataset}'.")


def run_biblical_text(dataset: str, ref: str, out_dir: str | Path, context: list[str] | None = None) -> dict:
    canonical_ref, input_file = resolve_biblical_input(dataset, ref)
    output_dir = Path(out_dir).resolve()
    args = [
        "run",
        "--domain",
        "biblical_text",
        "--input-ref",
        canonical_ref,
        "--input-file",
        str(input_file),
        "--out",
        str(output_dir),
    ]
    for entry in context or []:
        args.extend(["--context", entry])

    result = _run_core(args, cwd=legacy_root())
    artifacts = {
        "output": output_dir / "output.json",
        "provenance": output_dir / "provenance.json",
        "attestation": output_dir / "attestation.sha256",
        "log": output_dir / "log.txt",
    }
    missing = [name for name, path in artifacts.items() if not path.exists()]
    if missing:
        raise CoreBridgeError(f"Core run completed but did not produce required artifacts: {', '.join(missing)}")

    return {
        "resolved_ref": canonical_ref,
        "dataset": dataset,
        "input_file": str(input_file),
        "out_dir": str(output_dir),
        "artifacts": {name: str(path) for name, path in artifacts.items()},
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "core": inspect_core_install(),
    }


def verify_output(out_dir: str | Path) -> dict:
    output_dir = Path(out_dir).resolve()
    provenance_path = output_dir / "provenance.json"
    if not provenance_path.exists():
        raise CoreBridgeError(f"Missing provenance file: {provenance_path}")

    result = _run_core(["validate-provenance", str(provenance_path)], cwd=core_site_packages_root())
    records = json.loads(result.stdout)
    if not records:
        raise CoreBridgeError("Core verify returned no records.")
    record = records[0]

    failures = [key for key in ("attestation_match", "template_match", "input_match") if record.get(key) is not True]
    if failures:
        raise CoreBridgeError(f"Core verify failed checks: {', '.join(failures)}")

    return {
        "out_dir": str(output_dir),
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "verification": record,
        "core": inspect_core_install(),
    }
