#!/usr/bin/env python3
"""Check exact author-license decision registration; fail closed for missing/modified bytes."""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APPROVED_LICENSE="cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
APPROVED_NOTICES="c908a4adedc9a1fbe70f9df27dfcbdf361d82a2795658f7c08089da62d384d6f"
SCAN="fdc68b4e393b03535be896c4d3ebd0357d9aba64ca1aa03d48283d7f0e68e19e"
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def verify(root=ROOT, signed_pdf=None):
    checks=[]
    lic=root/'LICENSE'; notice=root/'THIRD_PARTY_NOTICES.md'
    j=root/'docs/governance/DEC-P04-07-author-license-approval.json'
    for label,path,expected in (('LICENSE',lic,APPROVED_LICENSE),('THIRD_PARTY_NOTICES.md',notice,APPROVED_NOTICES)):
        ok=path.is_file() and sha(path)==expected
        checks.append((label,ok))
    try:d=json.loads(j.read_text(encoding='utf-8'))
    except (OSError,ValueError):d={}
    ok=(d.get('schema_version')=='P04-07-author-license-decision-registration-v1'
        and d.get('decision')=='APACHE_2_0_APPROVED_FOR_AUTHOR_OWNED_WORKS'
        and d.get('project_license',{}).get('sha256')==APPROVED_LICENSE
        and d.get('third_party',{}).get('sha256')==APPROVED_NOTICES
        and d.get('signed_source',{}).get('sha256')==SCAN
        and d.get('third_party',{}).get('excluded_from_author_apache_2_0') is True
        and d.get('p04_r08_status')=='BLOCKED_PENDING_THIRD_PARTY_APPROVAL'
        and d.get('release_go_status')=='NOT_AUTHORIZED')
    checks.append(('signed author decision registration (not R08)',ok))
    if signed_pdf:
        f=Path(signed_pdf)
        checks.append(('private signed scan SHA-256',f.is_file() and sha(f)==SCAN))
    for label,ok in checks:print(f"{'PASS' if ok else 'FAIL'} {label}")
    passed=all(v for _,v in checks)
    print('P04-07 AUTHOR LICENSE REGISTRATION:', 'PASS' if passed else 'FAIL')
    print('P04-07 COMBINED R08: BLOCKED (third-party sign-off not asserted)')
    return passed
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,default=ROOT)
    p.add_argument('--signed-pdf',type=Path)
    a=p.parse_args()
    raise SystemExit(0 if verify(a.repo.resolve(),a.signed_pdf) else 1)
