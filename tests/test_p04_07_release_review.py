"""Meta-tests for P04-07 release-review controls. No live GitHub/network calls."""
import importlib.util
from pathlib import Path
import json
import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('p0407',ROOT/'scripts/review_release_p04.py')
r=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r)


def write(root, path, text):
    p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')


def baseline_payload():
    return {
        'implementation_commit':r.IMPLEMENTATION,'acceptance_status':'CI_PASS_VERIFIED',
        'github_actions':{'head_sha':r.IMPLEMENTATION,'conclusion':'success','run_id':41996276523},
        'execution':{'tested_commit':r.IMPLEMENTATION,'status':'PASS','profile':'p04',
            'gates':{f'gate{i}':'PASS' for i in range(11)},
            'pytest':{'tests':115,'errors':0,'failures':0,'skipped':0},
            'bh_rules':{x:'PASS' for x in r.BH_RULES},
            'bh_cq':{k:{'rows':v,'exact_bindings':True,'status':'PASS'} for k,v in r.BH_CQ.items()}},
        'artifact':{'sha256':'84ad7fa2fce3f7d9d4817229040e018698ed1fb6bd7262035ec908bd76020649'}
    }


def test_valid_ci_payload_pass():
    assert r.ci_payload(baseline_payload())['status']=='PASS'

@pytest.mark.parametrize('failure',('skip','wrongsha','no_exact','bad_rule','bad_gate','wrong_run','missing_cq'))
def test_ci_fail_closed(failure):
    x=baseline_payload()
    if failure=='skip':x['execution']['pytest']['skipped']=1
    if failure=='wrongsha':x['implementation_commit']='bad'
    if failure=='no_exact':x['execution']['bh_cq']['BH-CQ-03']['exact_bindings']=False
    if failure=='bad_rule':x['execution']['bh_rules']['BH-V05']='SKIPPED'
    if failure=='bad_gate':x['execution']['gates']['gate10']='BLOCKED'
    if failure=='wrong_run':x['github_actions']['run_id']=123
    if failure=='missing_cq':x['execution']['bh_cq'].pop('BH-CQ-02')
    assert r.ci_payload(x)['status']=='FAIL'


def test_markdown_balance():
    assert r.markdown_fences_balanced('```\nx\n```\n')
    assert not r.markdown_fences_balanced('```bash\nmake validate\n')


def test_version_mismatch_blocked(tmp_path):
    write(tmp_path,'VERSION','0.1.0\n')
    write(tmp_path,'pyproject.toml','[project]\nversion="0.1.0"\n')
    assert r.versions(tmp_path)['status']=='FAIL'


def test_version_equal_pass(tmp_path):
    write(tmp_path,'VERSION','0.4.0\n')
    write(tmp_path,'pyproject.toml','[project]\nversion="0.4.0"\n')
    assert r.versions(tmp_path)['status']=='PASS'


def test_public_docs_require_current_and_closed_fences(tmp_path):
    write(tmp_path,'README.md','# Ontology\n## Current development status: v0.3.0-dev\n```\n')
    write(tmp_path,'docs/index.md','# Docs\n## Development line: v0.3.0-dev\n')
    assert r.public_docs(tmp_path)['status']=='FAIL'
    write(tmp_path,'README.md','## Current release status: v0.4.0\nBH-P04\nmake behavior-test\n')
    write(tmp_path,'docs/index.md','## Release status: v0.4.0\n')
    assert r.public_docs(tmp_path)['status']=='PASS'


def test_changelog_requires_released_section_and_closed_fences(tmp_path):
    write(tmp_path,'CHANGELOG.md','# Log\n## Unreleased — v0.3.0-dev\n```bash\n')
    assert r.changelog(tmp_path)['status']=='FAIL'
    write(tmp_path,'CHANGELOG.md','# Log\n## v0.4.0 — Observation Core\nNo real AIS claims.\n')
    assert r.changelog(tmp_path)['status']=='PASS'


def test_license_and_notices_require_explicit_rights_approval(tmp_path):
    assert r.license_notices(tmp_path)['status']=='BLOCKED'
    lic='Apache License\nVersion 2.0, January 2004\n'+'A'*120
    write(tmp_path,'LICENSE',lic)
    notice='\n'.join([
        'QUDT CC BY 4.0 W3C OGC',
        'sosa-2017.ttl','ssn-2017.ttl','qudt-schema-3.5.3.ttl',
        'qudt-unit-3.5.3.ttl','qudt-quantitykind-3.5.3.ttl',
        'qudt-dimensionvector-3.5.3.ttl','owl-time.ttl','prov-o.ttl'
    ])
    write(tmp_path,'THIRD_PARTY_NOTICES.md',notice)
    assert r.license_notices(tmp_path)['status']=='BLOCKED'
    approval={
        'schema_version':'P04-07-rights-approval-v1',
        'decision':'APPROVED',
        'approved_by':'Actual Authorized Reviewer',
        'approval_date':'2026-11-05',
        'project_license_spdx':'Apache-2.0',
        'project_rights_holder':'Actual Rights Holder',
        'project_license_sha256':r.h(tmp_path/'LICENSE'),
        'third_party_notices_sha256':r.h(tmp_path/'THIRD_PARTY_NOTICES.md'),
        'third_party_review_status':'APPROVED_BY_PROJECT_OWNER',
        'scope':'Project-authored files only; vendor/external-rdf/T04-2026 excluded',
        'owl_time_cc_by_4_reconciled':True,
        'prov_o_exact_artifact_rights_confirmed':True,
    }
    write(tmp_path,'docs/governance/DEC-P04-07-rights-approval.json',json.dumps(approval))
    assert r.license_notices(tmp_path)['status']=='PASS'
    approval['third_party_notices_sha256']='0'*64
    write(tmp_path,'docs/governance/DEC-P04-07-rights-approval.json',json.dumps(approval))
    assert r.license_notices(tmp_path)['status']=='FAIL'
    approval['third_party_notices_sha256']=r.h(tmp_path/'THIRD_PARTY_NOTICES.md')
    approval['owl_time_cc_by_4_reconciled']=False
    write(tmp_path,'docs/governance/DEC-P04-07-rights-approval.json',json.dumps(approval))
    assert r.license_notices(tmp_path)['status']=='BLOCKED'


def test_release_notes_require_boundaries(tmp_path):
    assert r.release_notes(tmp_path)['status']=='FAIL'
    write(tmp_path,'docs/releases/v0.4.0-release-notes.md','BH-P04 synthetic AIS. Future P05 DEFERRED. MASS-SK-1.0 protected. T-04.\n')
    assert r.release_notes(tmp_path)['status']=='PASS'


def test_owner_approval_cannot_be_inferred(tmp_path):
    assert r.owner_approval(tmp_path)['status']=='BLOCKED'
    write(tmp_path,'docs/governance/DEC-P04-07-v0.4.0-release.md','**Decision:** PENDING\n**Approved by:** TBD\n')
    assert r.owner_approval(tmp_path)['status']=='BLOCKED'
    write(tmp_path,'docs/governance/DEC-P04-07-v0.4.0-release.md',
          '**Decision:** APPROVED FOR RELEASE\n**Approved by:** Actual Project Owner\n**Approval date:** 2026-11-05\n')
    assert r.owner_approval(tmp_path)['status']=='PASS'


def test_report_fails_until_all_controls_pass(monkeypatch,tmp_path):
    monkeypatch.setattr(r,'source_baseline',lambda root:r.result(True,'ok'))
    monkeypatch.setattr(r,'design_scope',lambda root:r.result(True,'ok'))
    monkeypatch.setattr(r,'ci_evidence',lambda root:r.result(True,'ok'))
    monkeypatch.setattr(r,'integrity',lambda root:r.result(True,'ok'))
    for f in ('versions','public_docs','changelog','license_notices','release_notes'):
        monkeypatch.setattr(r,f,lambda root:r.result(True,'ok'))
    monkeypatch.setattr(r,'owner_approval',lambda root:r.result(False,'await owner',blocked=True))
    x=r.run_review(tmp_path)
    assert x['decision']=='NO_GO'
    assert x['checks']['R10_OWNER_APPROVAL']['status']=='BLOCKED'
