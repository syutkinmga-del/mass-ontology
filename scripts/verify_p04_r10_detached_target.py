#!/usr/bin/env python3
"""Verify R10 from a later governance ref against an earlier immutable release commit.

Unlike in-tree R10 checks, the candidate being assessed is NOT the current
registration HEAD. Fail closed on missing exact owner confirmation. No tag or
GitHub Release is ever created here.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RECORD = "docs/governance/P04-07-R10-2026-02-release-target.json"
HISTORIC_R10 = "docs/governance/DEC-P04-07-v0.4.0-release.md"
OLD_SIGNED_SHA = "81b33951cbed446ebff5192099125f56ff474fb0"
R08 = "R08_LICENSE_NOTICES"
R10 = "R10_OWNER_APPROVAL"


def run(args: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False, timeout=180)


def git_bytes(root: Path, revision: str, path: str) -> bytes | None:
    proc = subprocess.run(["git", "show", f"{revision}:{path}"], cwd=root,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
                          timeout=60)
    return proc.stdout if proc.returncode == 0 else None


def result(root: Path) -> dict:
    findings: list[str] = []
    try:
        doc = json.loads((root / RECORD).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        doc = {}
        findings.append(f"R10 candidate registry unavailable: {exc}")

    candidate = doc.get("proposed_commit_sha")
    if not isinstance(candidate, str) or not re.fullmatch(r"[0-9a-f]{40}", candidate):
        candidate = None
        findings.append("Missing canonical 40-hex frozen candidate SHA")

    head_proc = run(["git", "rev-parse", "HEAD"], cwd=root)
    registry_head = head_proc.stdout.strip() if head_proc.returncode == 0 else None

    if candidate:
        kind = run(["git", "cat-file", "-t", candidate], cwd=root)
        if kind.returncode != 0 or kind.stdout.strip() != "commit":
            findings.append("Proposed release target does not resolve to Git commit")
        ancestry = run(["git", "merge-base", "--is-ancestor", candidate, "HEAD"], cwd=root)
        if ancestry.returncode:
            findings.append("Frozen target is not an ancestor of the governance registration HEAD")

    if doc.get("schema_version") != "P04-07-R10-exact-release-target-v1":
        findings.append("Unexpected R10 target registration schema")
    if doc.get("decision_number") != "P04-07-R10-2026-02":
        findings.append("Wrong decision number")
    if doc.get("target_release") != "v0.4.0" or doc.get("target_profile") != "BH-P04":
        findings.append("Unexpected release/profile scope")
    if doc.get("prior_signed_r10_commit_sha") != OLD_SIGNED_SHA:
        findings.append("Historical signed R10 target was changed")
    if doc.get("release_target_is_registration_commit") is not False:
        findings.append("Self-referential release registration is forbidden")

    if candidate:
        historic = git_bytes(root, candidate, HISTORIC_R10)
        if historic is None or OLD_SIGNED_SHA.encode() not in historic:
            findings.append("Historical R10 record not intact at candidate")
        notices = git_bytes(root, candidate, "THIRD_PARTY_NOTICES.md")
        expected_notice = doc.get("evidence", {}).get("rr05_notices_sha256")
        if notices is None or hashlib.sha256(notices).hexdigest() != expected_notice:
            findings.append("Frozen candidate RR-05 notices bytes do not match approved digest")

    approval_ok = True
    must = {
        "decision": "APPROVED_FOR_RELEASE",
        "approved_commit_sha": candidate,
        "owner_exact_sha_confirmation_received": True,
        "owner": "Сюткин Андрей Вениаминович",
    }
    for field, expected in must.items():
        if doc.get(field) != expected:
            approval_ok = False
            findings.append(f"R10 missing exact owner authorization: {field}")
    date = doc.get("approval_date")
    if not isinstance(date, str) or not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", date):
        approval_ok = False
        findings.append("Explicit owner approval date missing")
    method = doc.get("approval_evidence_type")
    if method not in {
        "EXPLICIT_OWNER_CHAT_TEXT_NOT_ELECTRONIC_SIGNATURE",
        "SIGNED_PRIVATE_PDF_DIGEST_RECORDED_NOT_INDEPENDENTLY_AUTHENTICATED",
    }:
        approval_ok = False
        findings.append("Approval method missing or unsupported")
    if method == "EXPLICIT_OWNER_CHAT_TEXT_NOT_ELECTRONIC_SIGNATURE" and doc.get("signed_pdf_sha256"):
        approval_ok = False
        findings.append("Chat approval must not impersonate a signed PDF")
    registered_path = "docs/governance/DEC-P04-07-R10-2026-02-chat-approval.md"
    if doc.get("registration_note") != registered_path:
        approval_ok = False
        findings.append("R10 registration record reference missing or changed")
    registered = root / registered_path
    if not registered.is_file():
        approval_ok = False
        findings.append("R10 explicit owner statement is absent")
    else:
        registered_text = registered.read_text(encoding="utf-8")
        owner_statement = doc.get("owner_statement")
        if (not isinstance(owner_statement, str)
                or not owner_statement.startswith("УТВЕРЖДАЮ выпуск MASS Ontology v0.4.0")
                or candidate is None or candidate not in owner_statement
                or owner_statement not in registered_text
                or "**Decision:** APPROVED FOR RELEASE" not in registered_text
                or f"**Approved commit SHA:** `{candidate}`" not in registered_text
                or "**Signed PDF supplied:** NO" not in registered_text):
            approval_ok = False
            findings.append("R10 in-chat statement, exact target or evidence type not independently corroborated by registration")
    tag_permission = doc.get("authorization_for_annotated_tag")
    if not isinstance(tag_permission, dict) or tag_permission != {
        "authorized": True, "tag": "v0.4.0",
        "target_sha": candidate, "contingent_on_independent_checks": True,
    }:
        approval_ok = False
        findings.append("No exact-target conditional annotated tag authorization")


    source_checks: dict = {}
    rr05_passed = False
    source_review_return = None
    if candidate and not any("does not resolve" in f for f in findings):
        with tempfile.TemporaryDirectory(prefix="p04-r10-target-") as tmp:
            worktree = Path(tmp) / "candidate"
            add = run(["git", "worktree", "add", "--detach", str(worktree), candidate], cwd=root)
            if add.returncode:
                findings.append("Cannot checkout frozen candidate for independent review: " + add.stderr[-500:])
            else:
                try:
                    check = run([sys.executable, str(worktree / "scripts/review_release_p04_candidate.py"),
                                 "--repo", str(worktree),
                                 "--report", "run/release-review/exact-target.json"],
                                cwd=worktree)
                    source_review_return = check.returncode
                    report_path = worktree / "run/release-review/exact-target.json"
                    if report_path.is_file():
                        original_report = json.loads(report_path.read_text(encoding="utf-8"))
                        source_checks = original_report.get("checks", {})
                        rr05_passed = original_report.get("rr05_exact_notice_verifier_status") == "PASS"
                    else:
                        findings.append("Frozen candidate produced no source R01–R10 report")
                except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
                    findings.append("Unable to run frozen source review: " + str(exc))
                finally:
                    run(["git", "worktree", "remove", "--force", str(worktree)], cwd=root)

    required_source = [f"R{i:02d}" for i in range(1, 10)]
    for prefix in required_source:
        gates = [v for key, v in source_checks.items() if key.startswith(prefix + "_")]
        if len(gates) != 1 or gates[0].get("status") != "PASS":
            findings.append("Frozen candidate source gate did not pass: " + prefix)
    if not rr05_passed:
        findings.append("Frozen candidate RR-05 exact notice verifier not PASS")

    r10_status = "PASS" if approval_ok and not any(
        "Self-referential" in x or "Historical signed" in x or "ancestor" in x
        for x in findings
    ) else "BLOCKED"
    checks = {k: v for k, v in source_checks.items() if not k.startswith("R10_")}
    checks[R10] = {
        "status": r10_status,
        "detail": (
            f"Separate R10-2026-02 owner approval binds exact source commit {candidate}"
            if r10_status == "PASS"
            else "R10-2026-02 exact source SHA owner approval is pending or invalid"
        ),
    }
    decision = "GO" if not findings and len(checks) == 10 else "NO_GO"
    return {
        "schema_version": "P04-07-detached-r10-target-review-v1",
        "reviewed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "decision": decision,
        "release_candidate_sha": candidate,
        "governance_registration_head_sha": registry_head,
        "registration_is_release_target": candidate == registry_head,
        "source_review_process_exit_code": source_review_return,
        "source_R01_to_R09_pass": all(
            v["status"] == "PASS" for k, v in checks.items() if not k.startswith("R10_")
        ) and len(source_checks) >= 10,
        "source_RR05_exact_notice_pass": rr05_passed,
        "checks": checks,
        "findings": findings,
        "ci_on_exact_candidate": "Independent GitHub Actions review also required; registry IDs are references, not proof of a live API check",
        "publication_executed": False,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=ROOT)
    p.add_argument("--report", default="run/release-review/p04-07-detached-r10.json")
    args = p.parse_args()
    root = args.repo.resolve()
    path = (root / args.report).resolve()
    if not path.is_relative_to(root):
        p.error("Report must be inside the governance repository")
    outcome = result(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(outcome, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for gate, entry in outcome["checks"].items():
        print(gate, entry["status"], "-", entry["detail"], flush=True)
    for msg in outcome["findings"]:
        print("BLOCKER:", msg, flush=True)
    print("DETACHED TARGET RELEASE REVIEW:", outcome["decision"], flush=True)
    print("Release target:", outcome["release_candidate_sha"], flush=True)
    print("Registration commit:", outcome["governance_registration_head_sha"], flush=True)
    print("Report:", path, flush=True)
    return 0 if outcome["decision"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
