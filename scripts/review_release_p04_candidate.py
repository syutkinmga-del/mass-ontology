#!/usr/bin/env python3
"""P04-07 formal follow-up: R01-R10 source checks plus exact release-target authorization.

This command generates machine-readable review evidence. It never creates a tag,
publishes a GitHub Release, or infers owner approval from CI alone.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

import review_release_p04 as base

ROOT = Path(__file__).resolve().parents[1]
R10_RECORD = "docs/governance/DEC-P04-07-v0.4.0-release.md"
RR05_VERIFIER = "scripts/verify_p04_rr05_notices.py"
R10_GATE = "R10_OWNER_APPROVAL"
R08_GATE = "R08_LICENSE_NOTICES"


def inspect(root: Path) -> dict:
    report = base.run_review(root)
    checks = report["checks"]
    head_run = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                              capture_output=True, text=True, check=False)
    head = head_run.stdout.strip().lower() if head_run.returncode == 0 else None

    record_file = root / R10_RECORD
    text = record_file.read_text(encoding="utf-8") if record_file.is_file() else ""
    matches = re.findall(r"^\*\*Approved commit SHA:\*\*\s*`([0-9a-fA-F]{40})`\s*$",
                         text, flags=re.MULTILINE)
    approved_sha = matches[0].lower() if len(matches) == 1 else None
    valid_target = head is not None and approved_sha is not None and head == approved_sha

    if checks[R10_GATE]["status"] == "PASS":
        if not valid_target:
            checks[R10_GATE] = base.result(
                False,
                "Signed R10 SHA is " + (approved_sha or "missing/ambiguous") +
                "; proposed candidate HEAD is " + (head or "unavailable") +
                ". A separate explicit exact-SHA authorization is required; " +
                "the historical signed decision does not authorize this newer commit.",
                blocked=True,
            )
        else:
            checks[R10_GATE] = base.result(
                True, "Owner approval is recorded and matches proposed exact candidate SHA " + head
            )

    rr05 = subprocess.run([sys.executable, str(root / RR05_VERIFIER),
                           "--repo", str(root), "--require-approval"],
                          cwd=root, capture_output=True, text=True, timeout=120,
                          check=False)
    if rr05.returncode and checks[R08_GATE]["status"] == "PASS":
        checks[R08_GATE] = base.result(
            False, "RR-05 fail-closed verifier failed on this candidate: " +
            (rr05.stderr or rr05.stdout)[-700:]
        )

    # The original R01-R10 report checks source and archive evidence.
    # Checking live GitHub Actions on the candidate SHA is a separate release duty.
    report["schema_version"] = "P04-07-release-review-exact-target-v1"
    report["reviewed_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    report["candidate_head_sha"] = head
    report["signed_r10_approved_sha"] = approved_sha
    report["signed_r10_matches_candidate"] = valid_target
    report["rr05_exact_notice_verifier_status"] = "PASS" if rr05.returncode == 0 else "FAIL"
    report["live_ci_on_candidate_sha"] = "VERIFY_SEPARATELY_FROM_GITHUB_ACTIONS"
    report["tag_and_github_release_published_by_script"] = False
    report["approval_evidence_boundary"] = (
        "Historical R10 owner-signed authorization is distinct from any CI success. "
        "RR-05-2026-02 is an explicit owner chat text statement, not a digital signature."
    )
    report["decision"] = ("GO" if all(v["status"] == "PASS" for v in checks.values())
                          and valid_target and rr05.returncode == 0 else "NO_GO")
    return report


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=ROOT)
    p.add_argument("--report", default="run/release-review/p04-07-follow-up.json")
    args = p.parse_args()
    root = args.repo.resolve()
    dest = (root / args.report).resolve()
    if not dest.is_relative_to(root):
        p.error("report must remain inside the repository")
    report = inspect(root)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    for gate, val in report["checks"].items():
        print(gate, val["status"], "-", val["detail"], flush=True)
    print("P04-07 FORMAL EXACT-SHA READINESS:", report["decision"], flush=True)
    print("CANDIDATE:", report["candidate_head_sha"], flush=True)
    print("SIGNED R10 TARGET:", report["signed_r10_approved_sha"], flush=True)
    print("RR-05 EXACT NOTICES:", report["rr05_exact_notice_verifier_status"], flush=True)
    print("Report:", dest, flush=True)
    return 0 if report["decision"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
