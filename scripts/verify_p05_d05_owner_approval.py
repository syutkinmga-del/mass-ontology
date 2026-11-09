#!/usr/bin/env python3
"""Verify a later owner text decision against an earlier immutable P05-D05 ADR."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
RECORD = "docs/standards/P05-D05-owner-approval.json"
DECISION = "docs/governance/DEC-P05-D05-2026-11-09-alternative-b-approval.md"
ADR = "docs/architecture/ADR-P05-D05-environmentspace-feature-reference.md"
CANDIDATE = "docs/standards/P05-01-environmentspace-adr-candidate.json"
OLD = "docs/standards/P05-00-design-approval.json"
SOURCE = "c4e9e7537b625dc5582b9505af232a959309c622"
V040 = "d0f2368df4268cfe3c6079a1681502cad0b867fb"
V040_TAG = "9da6a854d663d8c3b455f96521ea87d3579646cc"
OPEN = {"P05-D04","P05-D06","P05-D07","P05-D08","P05-D09"}
VERBATIM = "утверждаю  альтернативу B с условиями: `EnvironmentSpace` как `geo:Feature`, отдельные версионируемые `geo:Geometry`, самостоятельная роль `referencesVessel` и отсутствие автоматических COLREG-выводов."


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, capture_output=True,
                          text=True, check=False, timeout=30)


def verify(x: dict, text: str, candidate: dict, historic: dict, root: Path) -> list[str]:
    issues: list[str] = []
    def must(condition: bool, message: str) -> None:
        if not condition:
            issues.append(message)

    must(x.get("schema_version") == "P05-D05-owner-approval-v1"
         and x.get("decision_id") == "DEC-P05-D05-2026-11-09-01"
         and x.get("decision_date") == "2026-11-09"
         and x.get("stage") == "P05-01" and x.get("profile") == "BH-P05"
         and x.get("decision_status") == "CLOSED_APPROVED_ALTERNATIVE_B"
         and x.get("approved_alternative_id") == "B_FEATURE_SUBCLASS_DISTINCT_GEOMETRY",
         "Wrong ID, stage or approved Alternative B")
    must(x.get("approved_source_commit_sha") == SOURCE
         and x.get("approval_is_later_separate_git_commit") is True
         and x.get("approval_does_not_extend_to_unreviewed_revisions") is True,
         "Owner approval must bind prior exact design commit")
    must(x.get("owner_instruction_verbatim") == VERBATIM
         and ("> " + VERBATIM) in text and SOURCE in text
         and "P05-D05: CLOSED" in text,
         "Exact owner chat statement not preserved in decision")
    must(x.get("evidence_type") == "EXPLICIT_OWNER_CHAT_TEXT_NOT_ELECTRONIC_SIGNATURE"
         and x.get("signed_pdf_provided") is False
         and x.get("authenticated_signature") is False
         and x.get("identity_independently_verified") is False
         and x.get("governance_record") == DECISION,
         "Owner text must never be represented as cryptographic signature")
    must(x.get("open_adrs") == sorted(OPEN)
         and x.get("geo_rdf_owl_import_approved") is False
         and x.get("external_geo_rights_and_sha_verified") is False
         and x.get("geo_engine_conformance_achieved") is False
         and x.get("v050_release_authorized") is False
         and x.get("bh_p05_runtime_tests") == "DEFERRED_NOT_EXECUTED"
         and x.get("p05_cq_04_to_10") == "DEFERRED"
         and x.get("p05_validation_v04_v07_v08_v09_v10") == "DEFERRED",
         "Unresolved ADRs, rights, runtime tests or release permission overstated")
    clauses = x.get("approved_constraints", [])
    clauses_by_id = {q.get("id"): q for q in clauses if isinstance(q, dict)}
    must(len(clauses) == 4 and set(clauses_by_id) ==
         {"D05-B01","D05-B02","D05-B03","D05-B04"},
         "Four explicit approved conditions not registered once each")
    a, b, c, d = (clauses_by_id.get(i, {}) for i in
                  ("D05-B01","D05-B02","D05-B03","D05-B04"))
    must(a.get("subject") == "bh:EnvironmentSpace"
         and a.get("relation") == "rdfs:subClassOf"
         and a.get("object") == "geo:Feature"
         and a.get("excluded_relation") == "owl:equivalentClass",
         "Feature specialization or no-equivalence condition altered")
    must(b.get("geometry_class") == "geo:Geometry"
         and b.get("property") == "geo:hasGeometry"
         and b.get("separate_identifiers") is True and b.get("versioned") is True,
         "Independent versioned geometry condition altered")
    must(c.get("vessel_reference_role") == "bh:referencesVessel"
         and c.get("environment_reference_role") == "bh:referencesSpace"
         and c.get("referent_type") == "maritime:Vessel"
         and c.get("role_separation") is True
         and c.get("never_retype_vessel_as_environmentspace") is True,
         "Independent vessel reference role condition altered")
    must(d.get("automatic_colreg_conclusions_allowed") is False
         and d.get("automatic_control_or_safety_claims_allowed") is False,
         "No automatic COLREG conclusion condition altered")
    must(x.get("approved_next_step") ==
         "P05-01_NARROW_ENVIRONMENTSPACE_OWL_SHACL_FIXTURE_IMPLEMENTATION_SEPARATE_PR"
         and x.get("reference_roles_validated_in") == "P05-03"
         and x.get("geometry_engine_and_source_validation_in") == "P05-02",
         "Implementation boundary incorrectly extended")

    must(candidate.get("status") == "PROPOSED_FOR_OWNER_DECISION"
         and candidate.get("decision_status") == "OPEN"
         and candidate.get("candidate_not_approved") is True
         and candidate.get("selected_candidate") == "B_FEATURE_SUBCLASS_DISTINCT_GEOMETRY",
         "Historical P05-D05 proposal must not be rewritten")
    must(historic.get("decision") == "APPROVED_DESIGN_BASELINE_WITH_OPEN_ADRS"
         and {q.get("id") for q in historic.get("open_adrs", [])} ==
             OPEN | {"P05-D05"}
         and all(q.get("status") == "OPEN" for q in historic.get("open_adrs", []))
         and historic.get("v050_release_authorization") is False,
         "Historical P05-00 approval must stay intact")

    frozen_blobs = {
        ADR: "1c3177e15da6e5d0bfd11760dbeea6630bc48910",
        CANDIDATE: "1c8269d568689393cdf42d121fb0f42630b72f59",
    }
    must(x.get("approved_source_files") == frozen_blobs,
         "Approved source blob inventory changed")
    target = git(root, "cat-file", "-t", SOURCE)
    must(target.returncode == 0 and target.stdout.strip() == "commit",
         "Original D05 source is not a Git commit")
    anc = git(root, "merge-base", "--is-ancestor", SOURCE, "HEAD")
    must(anc.returncode == 0, "Approved D05 source must precede governance registration")
    for name, oid in frozen_blobs.items():
        q = git(root, "ls-tree", SOURCE, "--", name)
        header = q.stdout.split("\t", 1)[0].split() if q.returncode == 0 else []
        must(len(header) == 3 and header[1] == "blob" and header[2] == oid,
             "Approved source Git blob did not match: " + name)
    t = git(root, "rev-parse", "refs/tags/v0.4.0^{commit}")
    tag = git(root, "rev-parse", "refs/tags/v0.4.0")
    kind = git(root, "cat-file", "-t", "refs/tags/v0.4.0")
    must(t.returncode == 0 and t.stdout.strip() == V040
         and tag.returncode == 0 and tag.stdout.strip() == V040_TAG
         and kind.returncode == 0 and kind.stdout.strip() == "tag"
         and x.get("v040_release_target_sha") == V040
         and x.get("v040_annotated_tag_object_sha") == V040_TAG,
         "Frozen v0.4.0 annotated tag moved")
    for name in [RECORD, DECISION, ADR, CANDIDATE, OLD]:
        must((root / name).is_file(), "Missing required evidence file " + name)
    return issues


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=ROOT)
    p.add_argument("--report", type=Path, default=Path("run/p05-d05/approval-review.json"))
    args = p.parse_args()
    root = args.repo.resolve()
    report = (root / args.report).resolve()
    if not report.is_relative_to(root):
        p.error("Report outside repository")
    try:
        record = json.loads((root / RECORD).read_text(encoding="utf-8"))
        decision = (root / DECISION).read_text(encoding="utf-8")
        candidate = json.loads((root / CANDIDATE).read_text(encoding="utf-8"))
        historic = json.loads((root / OLD).read_text(encoding="utf-8"))
        issues = verify(record, decision, candidate, historic, root)
    except (OSError, ValueError, TypeError, subprocess.TimeoutExpired) as exc:
        issues = [f"{type(exc).__name__}: {exc}"]
    result = {
        "schema_version": "P05-D05-detached-owner-approval-verifier-v1",
        "date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "decision": "PASS" if not issues else "FAIL",
        "source_sha": SOURCE,
        "issues": issues,
        "D05_status": "CLOSED_APPROVED_ALTERNATIVE_B" if not issues else "INVALID",
        "remaining_open_adrs": sorted(OPEN),
        "evidence": "EXPLICIT_CHAT_TEXT_NOT_ELECTRONIC_SIGNATURE",
        "BH_P05_runtime": "DEFERRED_NOT_EXECUTED",
        "release_v050_authorized": False,
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
