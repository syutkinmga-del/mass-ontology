#!/usr/bin/env python3
"""P05-00 design-only fail-closed contract lint, not P05 ontology validation.

No class/shape/CQ execution is implied. A PASS confirms integrity of the
proposed design artifacts and that all P05 runtime rules are still DEFERRED.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = "docs/standards/P05-00-bh-p05-design-contract.json"
REGISTRY = "docs/standards/P05-00-external-spatial-source-register.json"
EXPECTED_CQS = {f"BH-CQ-{i:02d}" for i in range(4, 11)}
EXPECTED_RULES = {"BH-V04", "BH-V07", "BH-V08", "BH-V09", "BH-V10"}
EXPECTED_CONCEPTS = {"C08","C09","C10","C11","C12","C13","M01"}
FROZEN = "d0f2368df4268cfe3c6079a1681502cad0b867fb"
GRAPH_ROLES = ("observed", "context", "derived_interaction", "inferred_semantic", "provenance")


def review(contract: dict, source: dict, repo: Path = ROOT) -> list[str]:
    errors = []
    def require(ok: bool, description: str) -> None:
        if not ok:
            errors.append(description)

    require(contract.get("schema_version")=="P05-00-design-and-validation-contract-v1", "contract schema mismatch")
    require(contract.get("profile")=="BH-P05" and contract.get("stage")=="P05-00", "wrong profile/stage")
    require(contract.get("target_release")=="v0.5.0", "wrong proposed release")
    require(contract.get("status")=="DRAFT_REVIEW_REQUIRED_NOT_IMPLEMENTED", "design is prematurely approved or implemented")
    baseline = contract.get("source_baseline", {})
    require(baseline.get("published_tag_target_sha")==FROZEN, "approved v0.4.0 SHA not frozen")
    require(baseline.get("published_release")=="v0.4.0", "v0.4.0 release not recorded")

    approval=contract.get("owner_approval",{})
    require(approval=={"status":"PENDING","date":None,"evidence_type":None,"release_authorization":False},
            "P05-00 falsely claims an approval or release authorization")
    completion=contract.get("completion",{})
    require(completion.get("any_p05_ontology_runtime_gate_passed") is False,
            "P05-00 is design only; cannot assert runtime PASS")
    require(completion.get("contract_lint_executed") is False,
            "P05-00 source manifest may not pre-assert CI completion")
    require(completion.get("design_files_present") is False,
            "P05-00 manifest cannot be used to claim formal design acceptance")

    cq=contract.get("competency_questions", [])
    rules=contract.get("validation_rules", [])
    concepts=contract.get("concepts", [])
    require(isinstance(cq,list) and len(cq)==len(EXPECTED_CQS) and {c.get("id") for c in cq}==EXPECTED_CQS,
            "BH-CQ-04..10 coverage incomplete or duplicated")
    require(isinstance(rules,list) and len(rules)==len(EXPECTED_RULES) and {r.get("id") for r in rules}==EXPECTED_RULES,
            "BH-V04/V07..V10 coverage incomplete or duplicated")
    require(isinstance(concepts,list) and len(concepts)==len(EXPECTED_CONCEPTS)
            and {c.get("id") for c in concepts}==EXPECTED_CONCEPTS, "P05 concept inventory incomplete")
    for item in cq:
        require(item.get("status")=="DEFERRED" and item.get("oracle") and item.get("variables"),
                "CQ not explicitly deferred or lacking oracle: "+str(item.get("id")))
        require(bool(item.get("rules")) and set(item.get("rules", [])).issubset(EXPECTED_RULES),
                "CQ missing validation linkage: "+str(item.get("id")))
    for item in rules:
        require(item.get("status")=="DEFERRED" and bool(item.get("mechanism"))
                and bool(item.get("positive")) and bool(item.get("negative")),
                "P05 rule falsely marked executed or lacks positive/negative oracle: "+str(item.get("id")))
    for item in concepts:
        require(item.get("implementation_status")=="NOT_IMPLEMENTED"
                and item.get("design_status")=="PROPOSED" and item.get("owner") and item.get("source"),
                "P05 concept incorrectly asserted implemented or lacks provenance: "+str(item.get("id")))

    g=contract.get("graph_policy", {})
    graphs=g.get("graphs", {})
    require(g.get("status")=="PROPOSED" and g.get("default_union") is False,
            "Named-graph fail-closed separation missing")
    require(set(graphs)==set(GRAPH_ROLES) and len(set(graphs.values()))==len(GRAPH_ROLES),
            "Graph roles must be five distinct named IRIs")
    require(all(isinstance(x,str) and x.startswith("https://") for x in graphs.values()),
            "Named graph identifiers must be explicit HTTPS IRIs")
    require(set(g.get("inference_input_graphs",[]))=={"observed","context","derived_interaction"}
            and g.get("inference_output_graphs")==["inferred_semantic"],
            "Pre-inference vs post-inference graph allowlists invalid")
    require(g.get("label_leakage_policy")=="FORBID_OUTPUT_LABELS_IN_ANY_PREINFERENCE_INSTANCE_GRAPH",
            "No label leakage control")

    spatial=contract.get("spatial_policy", {})
    require(spatial.get("status")=="PROPOSED"
            and spatial.get("standard_candidate")=="OGC GeoSPARQL 1.1 / 22-047r1"
            and spatial.get("crs")=="http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            and spatial.get("wkt_axis_order")=="longitude latitude"
            and spatial.get("crs_iri_explicit_in_fixture") is True,
            "Spatial GeoSPARQL 1.1 + CRS84/WKT axis design mismatch")
    require(spatial.get("geo_vendor_snapshot_sha256") is None
            and spatial.get("geo_owl_import_approved") is False
            and spatial.get("geo_runtime_engine_conformance")=="NOT_TESTED",
            "Unverified external GeoSPARQL pin/import/runtime falsely claimed")

    require(source.get("schema_version")=="P05-00-external-spatial-source-register-v1",
            "External spatial source registry schema mismatch")
    require(source.get("status")=="CANDIDATE_DOCUMENTATION_ONLY_NO_OWL_IMPORT_NO_RUNTIME_PASS",
            "External source registry falsely claims pinning or runtime pass")
    entries=source.get("registrations",[])
    ids={x.get("id") for x in entries}
    require(len(entries)==5 and ids=={
        "P05-OGC-GEOSPARQL-1.1","P05-OGC-CRS84","P05-W3C-RDF-DATASET",
        "P05-W3C-SPARQL-1.1","P05-P04-FROZEN-T04"},
        "External spatial evidence register incomplete")
    geo=next((x for x in entries if x.get("id")=="P05-OGC-GEOSPARQL-1.1"), {})
    require(geo.get("specification")=="OGC 22-047r1, version 1.1"
            and geo.get("sha256") is None
            and geo.get("rdf_snapshot_selected") is False
            and geo.get("owl_import_allowed") is False
            and geo.get("engine_capabilities_tested") is False
            and geo.get("redistribution_licence_verified") is False,
            "GeoSPARQL version/rights/IRI/engine status incorrectly asserted")

    for key in ("authority","review_documents"):
        for rel in contract.get(key,[]):
            require((repo / rel).is_file(), f"Missing referenced {key} file: {rel}")
    for rel in ("docs/roadmap.md",
                "docs/reviews/DCCR-01-xiong-ship-behavior-review.md",
                "docs/reviews/DCCR-02-semantic-design-review.md",
                "docs/reviews/DCCR-03-ontology-alignment-specification.md",
                "docs/reviews/DCCR-04-validation-contract.md"):
        require((repo / rel).is_file(), "Missing immutable existing governance source: "+rel)
    review_doc=(repo / "docs/reviews/P05-00-design-baseline.md")
    policy_doc=(repo / "docs/architecture/p05-00-spatial-graph-crs-policy.md")
    if review_doc.is_file() and policy_doc.is_file():
        review_text=review_doc.read_text(encoding="utf-8")
        policy_text=policy_doc.read_text(encoding="utf-8")
        require("DRAFT FOR DESIGN REVIEW" in review_text
                and "Owner decision for P05-00" in review_text,
                "Design review incorrectly asserts owner acceptance")
        require(all(tag in review_text for tag in EXPECTED_CQS | EXPECTED_RULES),
                "Review lacks one or more DCCR CQ/rule traceability identifiers")
        require("longitude latitude" in policy_text and "Dataset(default_union=False)" in policy_text,
                "Spatial/graph policy lacks explicit axis and graph isolation")
        require("BH-V08" in policy_text and "BH-V10" in policy_text,
                "Graph policy omits leakage/non-entailment guards")
        require("time:intervalMeets" in policy_text and "bh:TemporalUnit" in policy_text,
                "Graph policy omits temporal extent/record distinction")
    return errors


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=ROOT)
    p.add_argument("--report", type=Path, default=Path("run/p05-00/design-contract-report.json"))
    args=p.parse_args()
    root=args.repo.resolve()
    report_path=(root / args.report).resolve()
    if not report_path.is_relative_to(root):
        p.error("report must stay within repository")
    try:
        a=json.loads((root/CONTRACT).read_text(encoding="utf-8"))
        b=json.loads((root/REGISTRY).read_text(encoding="utf-8"))
        failures=review(a,b,root)
    except (OSError,ValueError,TypeError) as e:
        failures=[f"{type(e).__name__}: {e}"]
    result={
        "schema_version":"P05-00-design-contract-lint-report-v1",
        "reviewed_utc":datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "profile":"BH-P05",
        "stage":"P05-00",
        "status":"PASS" if not failures else "FAIL",
        "failures":failures,
        "runtime_BH_P05_tests":"DEFERRED_NOT_EXECUTED",
        "owner_approval":"PENDING",
        "does_not_authorize_P05_implementation_or_release":True,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 0 if not failures else 2


if __name__=="__main__":
    raise SystemExit(main())
