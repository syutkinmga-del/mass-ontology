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
    assert contract["status"]=="APPROVED_DESIGN_BASELINE_OPEN_ADRS_NOT_IMPLEMENTED"
    assert contract["owner_approval"]["status"]=="APPROVED_DESIGN_BASELINE_WITH_OPEN_ADRS"
    assert contract["owner_approval"]["release_authorization"] is False
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



def test_p0500_owner_design_approval_retains_six_open_adrs_and_no_release():
    contract, registry = current()
    assert v.review(contract, registry, ROOT) == []
    registration=json.loads((ROOT/v.APPROVAL).read_text(encoding="utf-8"))
    assert registration["decision"] == "APPROVED_DESIGN_BASELINE_WITH_OPEN_ADRS"
    assert registration["approved_design_source_commit_sha"] == v.APPROVED_DESIGN_SOURCE
    assert registration["owner_direction_verbatim"] == v.EXACT_OWNER_INSTRUCTION
    assert registration["signed_pdf_supplied"] is False
    assert registration["authenticated_electronic_signature"] is False
    assert registration["v050_release_authorization"] is False
    assert {x["id"] for x in registration["open_adrs"]} == v.EXPECTED_OPEN_ADRS
    assert all(x["status"] == "OPEN" for x in registration["open_adrs"])
    assert all(r["status"] == "DEFERRED" for r in contract["validation_rules"])
    assert all(q["status"] == "DEFERRED" for q in contract["competency_questions"])


@pytest.mark.parametrize("corruption", [
    "false_signed_status",
    "false_release_permission",
    "open_adr_inadvertently_closed",
    "owner_instruction_mismatched",
    "approved_source_sha_changed",
])
def test_registration_fail_closed_on_corruption(monkeypatch, corruption):
    contract, registry = current()
    approval_path = (ROOT / v.APPROVAL).resolve()
    real_read = Path.read_text

    def patched_read(path, *args, **kwargs):
        text = real_read(path, *args, **kwargs)
        if path.resolve() != approval_path:
            return text
        approval = json.loads(text)
        if corruption == "false_signed_status":
            approval["signed_pdf_supplied"] = True
        elif corruption == "false_release_permission":
            approval["v050_release_authorization"] = True
        elif corruption == "open_adr_inadvertently_closed":
            approval["open_adrs"][1]["status"] = "CLOSED"
        elif corruption == "owner_instruction_mismatched":
            approval["owner_direction_verbatim"] = "APPROVED ALL P05 AXIOMS"
        elif corruption == "approved_source_sha_changed":
            approval["approved_design_source_commit_sha"] = "deadbeef" * 5
        return json.dumps(approval)

    monkeypatch.setattr(Path, "read_text", patched_read)
    assert v.review(contract, registry, ROOT), (
        f"Owner-approval tampering not rejected by real design lint: {corruption}"
    )
