#!/usr/bin/env python3
"""P05-01 D05 ADR integrity gate only; does NOT implement or approve GeoSPARQL.

Fails closed when the proposed architecture is represented as owner-approved,
when P05-D05 is prematurely closed, or when v0.5.0 release permission is asserted.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "docs/standards/P05-01-environmentspace-adr-candidate.json"
ADR = "docs/architecture/ADR-P05-D05-environmentspace-feature-reference.md"
PREVIOUS_APPROVAL = "docs/standards/P05-00-design-approval.json"
SOURCE_SHA = "b43b9423cc24075bc67010d5b04f47f58161260f"
DESIGN_SHA = "a73a7c8c5bc5f11a789405abd6d94da870d295b3"
FROZEN_V040 = "d0f2368df4268cfe3c6079a1681502cad0b867fb"
CASES = {f"D05-T{i:02d}" for i in range(1, 8)}
OTHER_ADRS = {f"P05-D{i:02d}" for i in [4,6,7,8,9]}


def check(obj: dict, prior: dict, doc: str, root: Path=ROOT) -> list[str]:
    failures: list[str] = []
    def require(value: bool, msg: str) -> None:
        if not value:
            failures.append(msg)
    require(obj.get("schema_version") == "P05-01-environmentspace-adr-v1"
            and obj.get("stage") == "P05-01"
            and obj.get("profile") == "BH-P05"
            and obj.get("target_release") == "v0.5.0",
            "Stage and version must be P05-01 / BH-P05 / v0.5.0")
    require(obj.get("decision_id") == "P05-D05"
            and obj.get("decision_status") == "OPEN"
            and obj.get("candidate_not_approved") is True
            and obj.get("status") == "PROPOSED_FOR_OWNER_DECISION",
            "P05-D05 must be OPEN until a separate owner decision")
    require(obj.get("selected_candidate") == "B_FEATURE_SUBCLASS_DISTINCT_GEOMETRY",
            "Candidate alternative B must be documented, not silently replaced")
    require(obj.get("parent_design_baseline_sha") == DESIGN_SHA
            and obj.get("branch_baseline_sha") == SOURCE_SHA
            and prior.get("approved_design_source_commit_sha") == DESIGN_SHA,
            "Immutable P05-00 design SHA or P05-01 base mismatch")
    require(prior.get("decision") == "APPROVED_DESIGN_BASELINE_WITH_OPEN_ADRS"
            and prior.get("evidence_kind") ==
                "OWNER_DIRECTED_CHAT_TEXT_NOT_ELECTRONIC_SIGNATURE"
            and prior.get("v050_release_authorization") is False,
            "Prior design approval incorrectly extended or misrepresented")
    require({a.get("id") for a in prior.get("open_adrs", [])} ==
            OTHER_ADRS | {"P05-D05"}
            and all(a.get("status") == "OPEN" for a in prior.get("open_adrs", [])),
            "P05-00 prior approval must leave all six ADRs OPEN")

    proposed = obj.get("recommendation", {})
    axiom = proposed.get("candidate_subclass_axiom", {})
    require(axiom == {"subject":"bh:EnvironmentSpace",
                      "predicate":"rdfs:subClassOf",
                      "object":"geo:Feature",
                      "status":"PROPOSED_NOT_PRODUCTION"},
            "EnvironmentSpace subclass axiom is not approved or improperly modeled")
    geo=proposed.get("geometry", {})
    require(geo.get("class") == "geo:Geometry"
            and geo.get("link") == "geo:hasGeometry"
            and geo.get("distinct_feature_and_geometry") is True
            and geo.get("allow_multiple_versioned_representations") is True
            and geo.get("default_geometry") == "NO_UNQUALIFIED_DEFAULT_IN_PILOT"
            and geo.get("crs_policy") == "CRS84_EXPLICIT_LON_LAT",
            "Feature geometry identity, version or CRS policy unresolved")
    require(proposed.get("source_ontology_import") is False
            and proposed.get("no_global_axiom") ==
                "maritime:Vessel rdfs:subClassOf geo:Feature",
            "Unsafe vendor import or global maritime-vessel Feature typing")
    refs=proposed.get("vessel_reference_role", {})
    require(refs.get("proposed_property")=="bh:referencesVessel"
            and refs.get("relation_class")=="bh:InteractionBehavior"
            and refs.get("range")=="maritime:Vessel"
            and refs.get("environment_property")=="bh:referencesSpace"
            and refs.get("environment_range")=="bh:EnvironmentSpace"
            and refs.get("shape_rule") ==
                "XOR_ONE_REFERENCE_ROLE_ONE_REFERENCE_OBJECT_ONE_SUBJECT"
            and refs.get("disallow_subject_equals_reference") is True
            and refs.get("model_vessel_as_environmentspace") is False
            and refs.get("production_status")=="DEFERRED_UNTIL_ADR_APPROVAL_AND_P05_03",
            "Spatial vs vessel reference identity and XOR role contract invalid")
    require(len(proposed.get("non_equivalences", [])) == 4
            and len(proposed.get("identity_rules", []))==4,
            "Missing four required identity and non-equivalence protections")
    alternatives=obj.get("alternatives",[])
    require({a.get("id") for a in alternatives} == {
        "A_GEOMETRY_SUBCLASS", "B_FEATURE_SUBCLASS_DISTINCT_GEOMETRY",
        "C_EQUIVALENCE_TO_FEATURE", "D_ODD_OR_ENCOUNTER_IDENTITY",
        "E_SPATIALOBJECT_ONLY"
    } and len(alternatives)==5,
            "ADR alternatives incomplete")
    require(next((a.get("status") for a in alternatives
                  if a.get("id") == "B_FEATURE_SUBCLASS_DISTINCT_GEOMETRY"), None)
            == "RECOMMEND_FOR_APPROVAL",
            "Recommended candidate B must not be labeled owner approved")
    scenarios=obj.get("candidate_validation_scenarios",[])
    require(len(scenarios)==7 and {x.get("id") for x in scenarios}==CASES
            and all(x.get("positive") and x.get("negative") and x.get("target")
                    for x in scenarios),
            "Seven prospective positive and negative D05 test designs required")
    require(set(obj.get("other_open_adrs",[]))==OTHER_ADRS
            and len(obj.get("other_open_adrs",[]))==5,
            "Remaining P05-D04/D06..D09 must remain OPEN")
    require(obj.get("owner_approval") == {
        "status":"PENDING_EXPLICIT_D05_DECISION",
        "date":None,"evidence_type":None,"chosen_alternative":None},
        "Owner D05 approval improperly assumed")
    require(obj.get("production_ontology_status") == "BLOCKED_PENDING_D05"
            and obj.get("geo_rdf_publisher_source_status") ==
                "PENDING_D04_RIGHTS_HASH_AND_ENGINE"
            and obj.get("runtime_BH_P05_tests") == "DEFERRED_NOT_EXECUTED"
            and obj.get("v050_release_authorization") is False,
            "Unapproved production code, external RDF, BH-P05 runtime or release authorization claimed")
    require("PROPOSED_FOR_OWNER_DESIGN_DECISION" in doc
            and "P05-D05 remains OPEN" in doc
            and "PENDING_OWNER_DECISION" in doc
            and "NOT production Turtle" in doc
            and "BH-V07" in doc and "BH-CQ-04" in doc
            and "OGC GeoSPARQL 1.1" in doc,
            "ADR does not disclose open decision, scope and source traceability")
    require(ADR in obj.get("references", {}).get("internal", []) or
            (root / ADR).is_file(),
            "P05-01 ADR source document missing")
    for p in obj.get("references", {}).get("internal", []):
        require((root / p).is_file(), "Missing internal citation " + str(p))
    for p in [MANIFEST,ADR,PREVIOUS_APPROVAL]:
        require((root / p).is_file(), "Missing contract file " + p)

    # Do not accept an accidentally moved published tag as a valid base.
    r=subprocess.run(["git","rev-parse","refs/tags/v0.4.0^{commit}"],
                     cwd=root, capture_output=True, text=True, check=False,timeout=20)
    require(r.returncode==0 and r.stdout.strip()==FROZEN_V040,
            "v0.4.0 tag moved, absent or is not available from the full checkout")
    return failures


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=ROOT)
    ap.add_argument("--report",type=Path,default=Path("run/p05-01/adr-review.json"))
    args=ap.parse_args()
    root=args.repo.resolve()
    path=(root / args.report).resolve()
    if not path.is_relative_to(root):
        ap.error("Report path must be inside repository")
    try:
        proposal=json.loads((root/MANIFEST).read_text(encoding="utf-8"))
        previous=json.loads((root/PREVIOUS_APPROVAL).read_text(encoding="utf-8"))
        document=(root/ADR).read_text(encoding="utf-8")
        failures=check(proposal,previous,document,root)
    except (OSError, ValueError, TypeError, subprocess.TimeoutExpired) as e:
        failures=[type(e).__name__+": "+str(e)]
    evidence={
        "schema_version":"P05-01-adr-design-lint-v1",
        "completed_utc":datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "decision_id":"P05-D05",
        "status":"PASS" if not failures else "FAIL",
        "failures":failures,
        "owner_decision":"OPEN_PENDING_APPROVAL",
        "production_ontology":"BLOCKED",
        "runtime_BH_P05_tests":"DEFERRED_NOT_EXECUTED",
        "no_release_authorization":True,
    }
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(evidence,ensure_ascii=False,indent=2),flush=True)
    return 0 if not failures else 2


if __name__=="__main__":
    sys.exit(main())
