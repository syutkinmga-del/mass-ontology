"""Positive and mutation-negative file integrity tests, not SysML semantic tests."""

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASELINE_DIR = ROOT / "baselines" / "sysml" / "MASS-SK-1.0"
CHECKER = ROOT / "scripts" / "verify_sysml_kernel_integrity.py"


def run_integrity_check(directory: Path):
    return subprocess.run(
        [sys.executable, str(CHECKER), "--baseline-dir", str(directory)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_released_sysml_kernel_identity():
    run = run_integrity_check(BASELINE_DIR)
    assert run.returncode == 0, run.stdout + run.stderr
    assert "SOURCE INTEGRITY: PASS" in run.stdout


def test_mutated_sysml_kernel_is_rejected(tmp_path):
    scratch = tmp_path / "MASS-SK-1.0"
    shutil.copytree(BASELINE_DIR, scratch)
    source = scratch / "MASSKernel_v1.0.sysml"
    with source.open("ab") as stream:
        stream.write(b"\n// unauthorized mutation\n")
    run = run_integrity_check(scratch)
    assert run.returncode != 0
    assert "Released source hash mismatch" in run.stdout
