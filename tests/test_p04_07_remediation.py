"""Release-candidate packaging and fail-closed rights checks, not permission to release."""
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('p0407_revised',ROOT/'scripts/review_release_p04.py')
r=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r)


def test_candidate_versions_and_documentation():
    assert r.versions(ROOT)['status']=='PASS'
    assert r.public_docs(ROOT)['status']=='PASS'
    assert r.changelog(ROOT)['status']=='PASS'
    assert r.release_notes(ROOT)['status']=='PASS'


def test_rights_review_cannot_pass_without_owner_decision():
    decision=ROOT/'docs/governance/DEC-P04-07-rights-approval.json'
    # A real authorized decision may be published in a later governance commit.
    if not decision.exists():
        assert r.license_notices(ROOT)['status'] in ('BLOCKED','FAIL')
    else:
        assert r.license_notices(ROOT)['status'] in ('PASS','BLOCKED','FAIL')


def test_release_approval_not_inferred_from_candidate():
    decision=ROOT/'docs/governance/DEC-P04-07-v0.4.0-release.md'
    if not decision.exists():
        assert r.owner_approval(ROOT)['status']=='BLOCKED'


def test_all_eight_external_sources_named_in_notice():
    text=(ROOT/'THIRD_PARTY_NOTICES.md').read_text(encoding='utf-8')
    for x in ('sosa-2017.ttl','ssn-2017.ttl','qudt-schema-3.5.3.ttl',
              'qudt-unit-3.5.3.ttl','qudt-quantitykind-3.5.3.ttl',
              'qudt-dimensionvector-3.5.3.ttl','owl-time.ttl','prov-o.ttl'):
        assert x in text


def test_license_candidate_is_not_authorized_project_license():
    candidate=ROOT/'docs/releases/LICENSE-Apache-2.0-CANDIDATE.txt'
    assert candidate.is_file() and candidate.stat().st_size>10000
    assert 'Apache License' in candidate.read_text(encoding='utf-8')
    # Do not infer authorization from existence of the candidate text.
    assert 'CANDIDATE' in candidate.name
