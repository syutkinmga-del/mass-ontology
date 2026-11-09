"""D05 owner authorization tests: text-based approval, not ontology execution."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "d05_owner", ROOT / "scripts/verify_p05_d05_owner_approval.py"
)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def loaded():
    return (
        json.loads((ROOT / gate.RECORD).read_text(encoding="utf-8")),
        (ROOT / gate.DECISION).read_text(encoding="utf-8"),
        json.loads((ROOT / gate.CANDIDATE).read_text(encoding="utf-8")),
        json.loads((ROOT / gate.OLD).read_text(encoding="utf-8")),
    )


def test_owner_text_approval_detached_from_immutable_design_source():
    x, text, proposed, historic = loaded()
    assert gate.verify(x,text,proposed,historic,ROOT) == []
    assert x["decision_status"] == "CLOSED_APPROVED_ALTERNATIVE_B"
    assert x["approved_source_commit_sha"] == gate.SOURCE
    assert x["evidence_type"] == "EXPLICIT_OWNER_CHAT_TEXT_NOT_ELECTRONIC_SIGNATURE"
    assert not x["authenticated_signature"]
    assert x["open_adrs"] == sorted(gate.OPEN)
    assert not x["v050_release_authorized"]


@pytest.mark.parametrize("change", [
    "source_sha",
    "owner_verbatim",
    "signed_pdf_fake",
    "invalid_ontology_equivalence",
    "geometry_not_versioned",
    "vessel_as_space",
    "automatic_colreg",
    "geo_import",
    "release_authorization",
    "p05_runtime_pass",
    "close_another_adr",
    "alter_frozen_blob",
    "alter_historical_decision",
    "no_provenance_record",
])
def test_d05_owner_approval_fail_closed_under_mutation(change):
    x, text, old, historic = loaded()
    x, old, historic = (deepcopy(q) for q in (x, old, historic))
    clauses = {v["id"]:v for v in x["approved_constraints"]}
    if change == "source_sha":
        x["approved_source_commit_sha"] = "deadbeef" * 5
    elif change == "owner_verbatim":
        x["owner_instruction_verbatim"] = "approve all"
    elif change == "signed_pdf_fake":
        x["signed_pdf_provided"] = True
    elif change == "invalid_ontology_equivalence":
        clauses["D05-B01"]["relation"] = "owl:equivalentClass"
    elif change == "geometry_not_versioned":
        clauses["D05-B02"]["versioned"] = False
    elif change == "vessel_as_space":
        clauses["D05-B03"]["never_retype_vessel_as_environmentspace"] = False
    elif change == "automatic_colreg":
        clauses["D05-B04"]["automatic_colreg_conclusions_allowed"] = True
    elif change == "geo_import":
        x["geo_rdf_owl_import_approved"] = True
    elif change == "release_authorization":
        x["v050_release_authorized"] = True
    elif change == "p05_runtime_pass":
        x["bh_p05_runtime_tests"] = "PASS"
    elif change == "close_another_adr":
        x["open_adrs"].pop()
    elif change == "alter_frozen_blob":
        x["approved_source_files"][gate.ADR] = "deadbeef" * 5
    elif change == "alter_historical_decision":
        historic["open_adrs"][1]["status"] = "CLOSED"
    elif change == "no_provenance_record":
        x["governance_record"] = "docs/governance/imaginary.md"
    else:
        raise AssertionError(change)
    assert gate.verify(x, text, old, historic, ROOT), (
        "Invalid owner approval escaped verifier: " + change
    )


def test_exact_proposal_as_of_state_kept_after_approval():
    approval, document, prior, historic = loaded()
    assert prior["decision_status"] == "OPEN"
    assert prior["owner_approval"]["status"] == "PENDING_EXPLICIT_D05_DECISION"
    assert historic["open_adrs"][1]["status"] == "OPEN"
    assert approval["candidate_decision_is_historically_open"] is True
    assert approval["decision_status"] == "CLOSED_APPROVED_ALTERNATIVE_B"
