#!/usr/bin/env python3
"""Capture auditable local evidence for MASS Ontology P04-01.

Runs tests in the user's repository; does NOT presume success or alter OWL/SysML.
Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

IMPLEMENTATION_SHA = "18f1dc21e786368a2bf0156961610e6c892e646a"
KERNEL_SHA256 = "1701bbb86e24588660ef717f2ff7f276b63c938d8569d4511dc19c42033aa788"
DOC = Path("docs/implementation/P04-01-general-maritime-vessel.md")
SOURCE = Path("baselines/sysml/MASS-SK-1.0/MASSKernel_v1.0.sysml")


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_check(root: Path, out: Path, name: str, command: list[str], *, kind: str = "normal") -> dict:
    print(f"[{name}] {' '.join(command)}", flush=True)
    start = datetime.now(timezone.utc)
    output_path = out / f"{name}.log"
    try:
        run = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=900, check=False)
        stdout, stderr, code = run.stdout, run.stderr, run.returncode
        error = None
    except (OSError, subprocess.TimeoutExpired) as exc:
        stdout = exc.stdout or "" if isinstance(exc, subprocess.TimeoutExpired) else ""
        stderr = exc.stderr or "" if isinstance(exc, subprocess.TimeoutExpired) else ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        code, error = None, str(exc)
    content = (f"$ {' '.join(command)}\n\nEXIT_CODE: {code}\n" +
               (f"ERROR: {error}\n" if error else "") +
               "\n--- STDOUT ---\n" + stdout + "\n--- STDERR ---\n" + stderr)
    output_path.write_text(content, encoding="utf-8")
    status = "BLOCKED" if error else ("PASS" if code == 0 else "FAIL")
    facts = {}
    if status == "PASS" and kind == "eight":
        count = re.search(r"(?<!\d)(\d+) passed\b", stdout)
        facts["passed_count"] = int(count.group(1)) if count else None
        if facts["passed_count"] != 8:
            status = "FAIL"
    if status == "PASS" and kind == "legacy_cq":
        q_files = sorted((root / "queries/cq").glob("cq-*.rq"))
        query_blocks = len(re.findall(r"(?m)^Query:\s", stdout))
        facts.update({"expected_cq_files": 14, "actual_cq_files": len(q_files),
                      "executed_cq_blocks": query_blocks})
        if len(q_files) != 14 or query_blocks != 14:
            status = "FAIL"
    if status == "PASS" and kind == "kernel":
        if "MASS-SK-1.0 SOURCE INTEGRITY: PASS" not in stdout:
            status = "FAIL"
    return {
        "id": name, "status": status, "command": command, "exit_code": code,
        "started_at_utc": start.isoformat(),
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "log_file": str(output_path.relative_to(root)), "log_sha256": digest(output_path),
        "facts": facts, "error": error,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Capture P04-01 local verification evidence")
    ap.add_argument("--repo", type=Path, default=Path.cwd(), help="MASS Ontology repository")
    ns = ap.parse_args()
    root = ns.repo.expanduser().resolve()
    head_result = git(root, "rev-parse", "HEAD")
    if head_result.returncode:
        ap.error(f"not a Git repository: {root}")
    head = head_result.stdout.strip()
    if not (root / DOC).is_file() or not (root / "tests/test_p04_01_maritime.py").is_file():
        ap.error("missing P04-01 implementation document/test")
    if not (root / ".venv/bin/python").exists():
        ap.error("missing .venv/bin/python; activate/install project dependencies first")
    if git(root, "merge-base", "--is-ancestor", IMPLEMENTATION_SHA, "HEAD").returncode != 0:
        ap.error(f"P04-01 implementation commit {IMPLEMENTATION_SHA} is not an ancestor of HEAD")
    # A report must describe the exact committed ontology state, not uncommitted edits.
    for cmd in (("diff", "--quiet"), ("diff", "--cached", "--quiet")):
        if git(root, *cmd).returncode != 0:
            ap.error("tracked changes are present; commit or stash them before capturing evidence")

    when = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = root / "docs" / "evidence" / "P04-01" / when
    if output.exists():
        ap.error(f"report already exists: {output}")
    output.mkdir(parents=True)
    venv = ".venv/bin/python"
    commands = [
        ("P04-01-8-tests", [venv, "-m", "pytest", "-v", "tests/test_p04_01_maritime.py"], "eight"),
        ("LEGACY-catalog", ["make", "catalog"], "normal"),
        ("LEGACY-validate", ["make", "validate"], "normal"),
        ("LEGACY-cq14", ["make", "cq"], "legacy_cq"),
        ("FULL-pytest", ["make", "test"], "normal"),
        ("KERNEL-integrity", [sys.executable, "scripts/verify_sysml_kernel_integrity.py"], "kernel"),
    ]
    results = [run_check(root, output, name, cmd, kind=kind) for name, cmd, kind in commands]
    source = root / SOURCE
    actual_sha = digest(source) if source.is_file() else None
    integrity = actual_sha == KERNEL_SHA256 and results[-1]["status"] == "PASS"
    if not integrity:
        results[-1]["status"] = "FAIL"
    overall = "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL"
    status = git(root, "status", "--porcelain=v1").stdout
    meta = {
        "work_package": "P04-01", "profile": "BH-P04 (partial P04-01 checks)",
        "status": overall, "implementation_commit_sha": IMPLEMENTATION_SHA,
        "tested_head_sha": head, "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "host_python_version": sys.version.split()[0], "platform": platform.platform(),
        "kernel_expected_sha256": KERNEL_SHA256, "kernel_observed_sha256": actual_sha,
        "tracked_changes_before_execution": False,
        "untracked_during_capture": [line for line in status.splitlines() if line.startswith("??")],
        "checks": results,
        "not_claimed": ["Full BH-V01 validation", "BH-CQ-01..03", "Full BH-P04 gate",
                         "Current SysML v2 Pilot parser/semantic validation", "External BFO/CCO equivalence"],
    }
    (output / "validation-results.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rel = output.relative_to(root)
    lines = [
        "# P04-01 — Local Validation Evidence", "",
        f"**Recorded UTC:** {meta['captured_at_utc']}",
        f"**Overall result:** **{overall}**",
        f"**Implementation commit:** `{IMPLEMENTATION_SHA}`",
        f"**Tested Git HEAD:** `{head}`",
        f"**Kernel SHA-256:** `{actual_sha or 'NOT AVAILABLE'}`",
        f"**Kernel reference SHA-256:** `{KERNEL_SHA256}`", "",
        "## Executed checks", "",
        "| Check | Status | Exit code | Log |", "|---|---|---:|---|",
    ]
    for r in results:
        lines.append(f"| {r['id']} | **{r['status']}** | {r['exit_code']} | "
                     f"[{Path(r['log_file']).name}](./{Path(r['log_file']).name}) |")
    lines += [
        "", "## Evidence integrity", "",
        "Each log SHA-256 is recorded in `validation-results.json`.",
        "Git implementation SHA is captured **before** creating this evidence record.",
        "The future evidence-documentation commit has a different SHA by design.", "",
        "## Scope limits", "",
        "This evidence verifies the P04-01 local test suite, legacy commands and immutable "
        "MASS-SK-1.0 source. It does not establish full BH-V01 or BH-CQ-01..03 PASS; "
        "these require the later Observation Core implementation and test fixtures. "
        "It is not a rerun of the SysML v2 Pilot Implementation.", "",
    ]
    (output / "validation-report.md").write_text("\n".join(lines), encoding="utf-8")
    if overall == "PASS":
        doc = root / DOC
        current = doc.read_text(encoding="utf-8")
        old_status = "**Status:** IMPLEMENTATION CANDIDATE — local test evidence must be collected; not yet a release"
        new_status = "**Status:** P04-01 VALIDATED — local checks PASS; architecture acceptance pending; not a BH-P04 release"
        if old_status in current:
            current = current.replace(old_status, new_status, 1)
        marker = "\n## P04-01 Validation Evidence Record\n"
        if marker in current:
            current = current.split(marker)[0].rstrip() + "\n"
        summary = (
            marker + "\n"
            f"- **Implementation commit:** `{IMPLEMENTATION_SHA}`.\n"
            f"- **Tested HEAD:** `{head}`.\n"
            f"- **Verification UTC:** `{meta['captured_at_utc']}`.\n"
            f"- **Executed P04-01 tests:** `8 passed` (see evidence logs).\n"
            "- **Legacy regression:** `make catalog`, `make validate`, `make cq` "
            "(14 CQ), `make test`: **PASS**.\n"
            f"- **MASS-SK-1.0:** byte integrity **PASS**; SHA-256 `{actual_sha}`.\n"
            f"- **Evidence report:** "
            f"[validation-report.md](../evidence/P04-01/{when}/validation-report.md).\n"
            f"- **Machine report:** "
            f"[validation-results.json](../evidence/P04-01/{when}/validation-results.json).\n"
            "- **Not tested:** full BH-V01/BH-CQ-01..03, future P04 profile, fresh SysML Pilot validation.\n"
        )
        doc.write_text(current.rstrip() + "\n" + summary, encoding="utf-8")
    print(f"\nRESULT: {overall}")
    print(f"Evidence: {rel}/validation-report.md")
    print(f"JSON: {rel}/validation-results.json")
    print(f"Implementation doc updated: {'YES' if overall == 'PASS' else 'NO (failed run preserved)'}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
