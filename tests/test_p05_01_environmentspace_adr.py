"""P05-01 static design gates; no production OWL, SPARQL/geospatial conformance."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("p0501adr", ROOT/"scripts/validate_p05_01_adr.py")
v=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)


def current():
    return (
        json.loads((ROOT/v.MANIFEST).read_text(encoding="utf-8")),
        json.loads((ROOT/v.PREVIOUS_APPROVAL).read_text(encoding="utf-8")),
        (ROOT/v.ADR).read_text(encoding="utf-8"),
    )


def test_p0501_adr_design_candidate_integrity_and_owner_gate():
    obj,prior,doc=current()
    assert v.check(obj,prior,doc,ROOT)==[]
    assert obj["decision_status"]=="OPEN"
    assert obj["owner_approval"]["status"]=="PENDING_EXPLICIT_D05_DECISION"
    assert obj["runtime_BH_P05_tests"]=="DEFERRED_NOT_EXECUTED"
    assert not obj["v050_release_authorization"]


@pytest.mark.parametrize("mutation",[
    "premature_owner_approval",
    "production_class_claim",
    "unsafe_geometry_equivalence",
    "global_vessel_geofeature",
    "confused_vessel_ref",
    "both_references_allowed",
    "no_crs_policy",
    "one_missing_negative_oracle",
    "external_rdf_import",
    "wrong_v040_baseline",
    "other_adr_closed",
    "unsupported_release_authorization",
])
def test_p0501_fail_closed_against_ontology_and_governance_mutants(mutation):
    obj,prior,doc=current()
    obj,prior=deepcopy(obj),deepcopy(prior)
    recommendation=obj["recommendation"]
    if mutation=="premature_owner_approval":
        obj["decision_status"]="CLOSED"
        obj["owner_approval"]["status"]="APPROVED"
    elif mutation=="production_class_claim":
        recommendation["candidate_subclass_axiom"]["status"]="PRODUCTION"
    elif mutation=="unsafe_geometry_equivalence":
        recommendation["candidate_subclass_axiom"]["object"]="geo:Geometry"
    elif mutation=="global_vessel_geofeature":
        recommendation["no_global_axiom"]="maritime:Vessel rdfs:subClassOf geo:Geometry"
    elif mutation=="confused_vessel_ref":
        recommendation["vessel_reference_role"]["model_vessel_as_environmentspace"]=True
    elif mutation=="both_references_allowed":
        recommendation["vessel_reference_role"]["shape_rule"]="ALLOW_TWO_REFERENCES"
    elif mutation=="no_crs_policy":
        recommendation["geometry"]["crs_policy"]="UNKNOWN"
    elif mutation=="one_missing_negative_oracle":
        obj["candidate_validation_scenarios"][2]["negative"]=""
    elif mutation=="external_rdf_import":
        recommendation["source_ontology_import"]=True
    elif mutation=="wrong_v040_baseline":
        prior["approved_design_source_commit_sha"]="deadbeef"*5
    elif mutation=="other_adr_closed":
        obj["other_open_adrs"].pop()
    elif mutation=="unsupported_release_authorization":
        obj["v050_release_authorization"]=True
    else:
        raise AssertionError(mutation)
    assert v.check(obj,prior,doc,ROOT), "unsafe mutation passed: "+mutation


def test_p0501_governance_approval_remains_preliminary():
    obj,prior,doc=current()
    assert "PROPOSED_FOR_OWNER_DESIGN_DECISION" in doc
    assert "P05-D05 remains OPEN" in doc
    assert "PENDING_OWNER_DECISION" in doc
    assert prior["v050_release_authorization"] is False
    assert {x["id"] for x in prior["open_adrs"]} == {
        "P05-D04","P05-D05","P05-D06","P05-D07","P05-D08","P05-D09"
    }
