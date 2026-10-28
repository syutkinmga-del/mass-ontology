#!/usr/bin/env python3
"""P04-00: capture a local immutable baseline and run existing legacy gates.

No network requests, installations, git commits, or ontology edits. Writes reports
outside the repository. Execute in the local repository with `python3 scripts/capture_p04_baseline.py`.
"""
from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REMOTE_SHA = "44d7131fac9c0827fa973e06067200e5b31f3328"
OUT = ROOT.parent / f"{ROOT.name}-p04-00-evidence"
OUT.mkdir(parents=True, exist_ok=True)
RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def run(argv: list[str], *, timeout: int = 240):
    try:
        r = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                           errors="replace", timeout=timeout, check=False)
        return {"status": "PASS" if r.returncode == 0 else "FAIL",
                "return_code": r.returncode, "stdout": r.stdout, "stderr": r.stderr}
    except FileNotFoundError as exc:
        return {"status": "BLOCKED", "return_code": None, "stdout": "", "stderr": str(exc)}
    except subprocess.TimeoutExpired as exc:
        return {"status": "BLOCKED", "return_code": None,
                "stdout": (exc.stdout or b"").decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or ""),
                "stderr": f"Timed out after {timeout} sec"}


def one_line(argv: list[str]):
    r = run(argv, timeout=12)
    return r["stdout"].strip() if r["status"] == "PASS" else None


def sha256(file: Path):
    h = hashlib.sha256()
    with file.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def find_kernel():
    candidates = [ROOT / "MASSKernel_v1.0.sysml",
                  ROOT / "sysml" / "MASSKernel_v1.0.sysml",
                  ROOT / "models" / "MASSKernel_v1.0.sysml"]
    tracked = run(["git", "ls-files", "--", "*MASSKernel_v1.0.sysml"])
    if tracked["status"] == "PASS":
        for relative in tracked["stdout"].splitlines():
            candidates.append(ROOT / relative)
    for p in candidates:
        if p.is_file():
            return {"path": str(p), "sha256": sha256(p), "status": "FOUND"}
    return {"path": None, "sha256": None, "status": "NOT_AVAILABLE_IN_REPO"}


def versions():
    venv_py = ROOT / ".venv" / "bin" / "python"
    package_names = ["rdflib", "pyshacl", "pytest", "owlrl", "pyparsing"]
    result = {"venv_python": str(venv_py), "exists": venv_py.is_file(),
              "packages": {}}
    if not venv_py.is_file():
        return result
    r = run([str(venv_py), "-c", "import json,importlib.metadata as m; print(json.dumps({p: (m.version(p) if any(d.metadata.get('Name','').lower()==p.lower() for d in m.distributions()) else None) for p in ['rdflib','pyshacl','pytest','owlrl','pyparsing']}))"], timeout=40)
    if r["status"] == "PASS":
        try:
            result["packages"] = json.loads(r["stdout"])
        except json.JSONDecodeError:
            result["version_probe_error"] = r["stdout"][-200:]
    else:
        result["version_probe_error"] = r["stderr"][-300:]
    return result


def main():
    now = datetime.now(timezone.utc).isoformat()
    head = one_line(["git", "rev-parse", "HEAD"])
    branch = one_line(["git", "branch", "--show-current"])
    git_status = run(["git", "status", "--porcelain=v1"], timeout=15)
    current_changes = git_status["stdout"].splitlines() if git_status["status"] == "PASS" else []
    evidence = {
        "work_package": "P04-00", "captured_at_utc": now,
        "repository": str(ROOT), "python_runtime": platform.python_version(),
        "remote_observed_baseline_sha": EXPECTED_REMOTE_SHA,
        "local_head_sha": head, "branch": branch,
        "matches_observed_baseline": (head == EXPECTED_REMOTE_SHA) if head else None,
        "worktree_clean": (not current_changes) if git_status["status"] == "PASS" else None,
        "worktree_changes": current_changes,
        "sysml_kernel": find_kernel(), "environment": versions(),
        "legacy_checks": {},
        "observation": "GitHub remote SHA is a recorded point-in-time reference; local HEAD may have advanced. No CI/test PASS is inferred from documentation approval."
    }
    make_path = shutil.which("make")
    interpreter = ROOT / ".venv" / "bin" / "python"
    for target in ["catalog", "validate", "cq", "test"]:
        if not make_path or not interpreter.is_file():
            result = {"status": "BLOCKED", "return_code": None, "stdout": "",
                      "stderr": "Missing make or .venv/bin/python"}
        else:
            result = run([make_path, target], timeout=240)
        logfile = OUT / f"{RUN_ID}-{target}.log"
        logfile.write_text(f"$ make {target}\nSTATUS: {result['status']}\nEXIT CODE: {result['return_code']}\n\nSTDOUT:\n{result['stdout']}\n\nSTDERR:\n{result['stderr']}\n", encoding="utf-8")
        evidence["legacy_checks"][target] = {"status": result["status"],
                                             "return_code": result["return_code"],
                                             "log_path": str(logfile),
                                             "log_sha256": sha256(logfile)}
    expected_cq = ROOT / "tests" / "expected-cq-results.json"
    if expected_cq.exists():
        try:
            counts = json.loads(expected_cq.read_text(encoding="utf-8"))
            evidence["legacy_cq_expected_count"] = len(counts)
            evidence["legacy_cq_expected_file_sha256"] = sha256(expected_cq)
        except (ValueError, OSError) as exc:
            evidence["legacy_cq_error"] = str(exc)
    report_path = OUT / f"{RUN_ID}-baseline.json"
    report_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"P04-00 baseline SHA (observed remote): {EXPECTED_REMOTE_SHA}")
    print(f"Local HEAD: {head or 'NOT AVAILABLE'}")
    print(f"HEAD matches observed baseline: {evidence['matches_observed_baseline']}")
    print(f"Working tree clean: {evidence['worktree_clean']}")
    print(f"SysML Kernel: {evidence['sysml_kernel']['status']}")
    for target, result in evidence["legacy_checks"].items():
        print(f"make {target}: {result['status']}")
    print(f"\nEvidence report: {report_path}")
    print("Reports stored outside repo; no modifications to ontology or Git metadata.")


if __name__ == "__main__":
    main()
