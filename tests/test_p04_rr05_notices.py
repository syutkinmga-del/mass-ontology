"""RR05 fail-closed policy tests; do not infer owner licensing signoff."""
from pathlib import Path
import importlib.util, hashlib,json
import pytest
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('p0407_rr05',ROOT/'scripts/verify_p04_rr05_notices.py')
r=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(r)

def test_notice_digests_and_all_source_files():
    data=r.verify(ROOT)
    assert data['status']=='PASS',data
    assert data['vendor_files_checked']==8

def test_no_owner_approval_implicit():
    path=ROOT/'docs/governance/DEC-P04-07-rights-approval.json'
    if not path.exists():assert r.verify(ROOT,require_approval=True)['status']!='PASS'

def test_baseline_licenses_are_explicit_and_separate():
    txt=(ROOT/'THIRD_PARTY_NOTICES.md').read_text()
    assert 'excluded' in txt and 'Apache-2.0' in txt
    assert 'no explicit license' in txt.lower() or 'does not contain an explicit' in (ROOT/'docs/evidence/P04-07/rights-review/RR05-PROV-O-EVIDENCE.md').read_text().lower()

def test_old_author_notice_hash_is_not_current():
    assert r.EXPECTED_NOTICE!='c908a4adedc9a1fbe70f9df27dfcbdf361d82a2795658f7c08089da62d384d6f'

def test_old_author_license_sha_is_preserved():
    assert r.sha(ROOT/'LICENSE')==r.EXPECTED_LICENSE

def test_full_upstream_notices_exist():
    for rel in ('docs/licenses/third-party/W3C-20150513-LICENSE.txt','docs/licenses/third-party/OGC-1.0-LICENSE.txt'):
        assert (ROOT/rel).stat().st_size>800
