"""P05-00 design-only contract guardrails: NOT BH-P05 ontology conformance tests."""
from __future__ import annotations
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "p0500_contract", ROOT / "scripts/validate_p05_00_design.py"
)
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)


def current():
    a=json.loads((ROOT/v.CONTRACT).read_text(encoding="utf-8"))
    b=json.loads((ROOT/v.REGISTRY).read_text(encoding="utf-8"))
    return a,b


def test_p0500_proposal_has_complete_contract_without_runtime_claim():
    contract, sources=current()
    assert v.review(contract,sources,ROOT)==[]
    assert contract["status"]=="DRAFT_REVIEW_REQUIRED_NOT_IMPLEMENTED"
    assert contract["owner_approval"]["status"]=="PENDING"
    assert contract["completion"]["any_p05_ontology_runtime_gate_passed"] is False
    assert {q["id"] for q in contract["competency_questions"]} == v.EXPECTED_CQS
    assert {r["id"] for r in contract["validation_rules"]} == v.EXPECTED_RULES


@pytest.mark.parametrize("mutation",[
    "approved_without_owner",
    "runtime_success_fabricated",
    "one_missing_cq",
    "one_missing_rule",
    "leaked_label_graph",
    "default_union",
    "unsupported_geo_import",
    "wrong_axis",
    "wrong_frozen_source",
    "no_negative_oracle",
    "unsupported_geo_version",
    "false_publisher_rights",
])
def test_p0500_contract_fail_closed_on_claim_or_scope_mutation(mutation):
    a,b=current()
    a,b=deepcopy(a),deepcopy(b)
    if mutation=="approved_without_owner":
        a["owner_approval"]["status"]="APPROVED"
    elif mutation=="runtime_success_fabricated":
        a["completion"]["any_p05_ontology_runtime_gate_passed"]=True
    elif mutation=="one_missing_cq":
        a["competency_questions"].pop()
    elif mutation=="one_missing_rule":
        a["validation_rules"].pop()
    elif mutation=="leaked_label_graph":
        a["graph_policy"]["inference_input_graphs"].append("inferred_semantic")
    elif mutation=="default_union":
        a["graph_policy"]["default_union"]=True
    elif mutation=="unsupported_geo_import":
        a["spatial_policy"]["geo_owl_import_approved"]=True
    elif mutation=="wrong_axis":
        a["spatial_policy"]["wkt_axis_order"]="latitude longitude"
    elif mutation=="wrong_frozen_source":
        a["source_baseline"]["published_tag_target_sha"]="deadbeef"*5
    elif mutation=="no_negative_oracle":
        a["validation_rules"][0]["negative"]=[]
    elif mutation=="unsupported_geo_version":
        b["registrations"][0]["specification"]="OGC GeoSPARQL Next draft"
    elif mutation=="false_publisher_rights":
        b["registrations"][0]["redistribution_licence_verified"]=True
    else:
        raise AssertionError(mutation)
    assert v.review(a,b,ROOT), f"Contract mutation escaped guardrails: {mutation}"

