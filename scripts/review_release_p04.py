#!/usr/bin/env python3
"""P04-07 candidate release readiness gate (not a release/tagging tool).

No network access, no release mutation, and no user approval is inferred.
Only verifies the recorded evidence and explicitly approved release controls.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '11491acb0685e69c0aed6ec749eea4d138162b30'
IMPLEMENTATION = '68e1c4f454caf85958806d761b3a671b51c7803c'
TARGET = '0.4.0'
BH_RULES = ('BH-V01','BH-V02','BH-V03','BH-V05','BH-V06','BH-V11','BH-V12')
BH_CQ = {'BH-CQ-01':18,'BH-CQ-02':9,'BH-CQ-03':18}
GATES = (
 'R01_SOURCE_BASELINE','R02_DESIGN_SCOPE','R03_CI_EVIDENCE',
 'R04_INTEGRITY','R05_VERSION','R06_DOCS','R07_CHANGELOG',
 'R08_LICENSE_NOTICES','R09_RELEASE_NOTES','R10_OWNER_APPROVAL'
)
HASHES = {
 'baselines/sysml/MASS-SK-1.0/MASSKernel_v1.0.sysml': '1701bbb86e24588660ef717f2ff7f276b63c938d8569d4511dc19c42033aa788',
 'docs/standards/T04-external-rdf-lock.json':'ebacb2bd81ed836df52fb2915a386fb54daef07d479b9f6bbfd9d84f5278f4af',
 'examples/p04-04-synthetic-ais-qudt353.ttl':'2f73990cd4dc88fd4e21c4694d35c6628d0afac613080434d33deed3f41cf301',
}
REQUIRED_DCCR = (
 'docs/reviews/DCCR-01-xiong-ship-behavior-review.md',
 'docs/reviews/DCCR-02-semantic-design-review.md',
 'docs/reviews/DCCR-03-ontology-alignment-specification.md',
 'docs/reviews/DCCR-04-validation-contract.md',
 'docs/roadmap.md',
)


def h(path: Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result(ok: bool, reason: str, *, blocked: bool=False)->dict:
    return {'status': ('PASS' if ok else 'BLOCKED' if blocked else 'FAIL'), 'detail':reason}


def run_cmd(args: list[str], root: Path, timeout=40):
    try:
        return subprocess.run(args,cwd=root,text=True,capture_output=True,timeout=timeout,check=False)
    except (OSError,subprocess.TimeoutExpired) as exc:
        return None


def source_baseline(root: Path)->dict:
    head=run_cmd(['git','rev-parse','HEAD'],root)
    anc=run_cmd(['git','merge-base','--is-ancestor',BASELINE,'HEAD'],root)
    if head is None or anc is None or head.returncode or anc.returncode:
        return result(False, 'Published evidence commit is not verified as an ancestor of local HEAD; fetch full history.',blocked=True)
    return result(True,'HEAD='+head.stdout.strip()+'; P04-06 evidence ancestor verified')


def design_scope(root:Path)->dict:
    missing=[p for p in REQUIRED_DCCR if not (root/p).is_file()]
    if missing:return result(False,'Missing design/roadmap: '+', '.join(missing))
    changed=[]
    for rel in REQUIRED_DCCR:
        old=run_cmd(['git','show',f'{BASELINE}:{rel}'],root)
        if old is None or old.returncode:
            return result(False,'Cannot compare immutable governance baseline for '+rel,blocked=True)
        # text-only DCCR and Roadmap currently UTF8; unchanged historical contract required.
        if (root/rel).read_text(encoding='utf-8') != old.stdout:
            changed.append(rel)
    if changed: return result(False,'Historical approved documents changed without separate approval: '+', '.join(changed))
    return result(True,'Four approved DCCR reviews and Roadmap v1.1 present, unchanged from P04-06 evidence commit')


def ci_payload(evidence:dict)->dict:
    try:
        x=evidence['execution'];gh=evidence['github_actions']
        if evidence.get('implementation_commit')!=IMPLEMENTATION or x.get('tested_commit')!=IMPLEMENTATION:
            raise ValueError('wrong implementation SHA')
        if gh.get('head_sha')!=IMPLEMENTATION or gh.get('conclusion')!='success':
            raise ValueError('GitHub Actions run does not evidence success on implementation SHA')
        if gh.get('run_id')!=41996276523:
            raise ValueError('unexpected source CI run')
        if evidence.get('acceptance_status')!='CI_PASS_VERIFIED' or x.get('status')!='PASS' or x.get('profile')!='p04':
            raise ValueError('CI acceptance, status, or profile incorrect')
        gates=x.get('gates',{})
        if len(gates)!=11 or set(gates.values())!={'PASS'}:raise ValueError('not all 11 mandatory gates PASS')
        p=x['pytest']
        if p.get('tests',0)<115 or any(p.get(k)!=0 for k in ('errors','failures','skipped')):
            raise ValueError('unexpected pytest errors/failures/skips or insufficient test count')
        if {k:x['bh_rules'].get(k) for k in BH_RULES}!={k:'PASS' for k in BH_RULES}:
            raise ValueError('one or more 7 required BH-V not PASS')
        if set(x['bh_rules'])!=set(BH_RULES):raise ValueError('wrong P04 rule set')
        if set(x['bh_cq'])!=set(BH_CQ):raise ValueError('wrong P04 CQ set')
        for key,count in BH_CQ.items():
            q=x['bh_cq'][key]
            if q.get('rows')!=count or q.get('exact_bindings') is not True or q.get('status')!='PASS':
                raise ValueError(key+' has incorrect bindings/results')
        a=evidence['artifact']
        if a.get('sha256')!='84ad7fa2fce3f7d9d4817229040e018698ed1fb6bd7262035ec908bd76020649':
            raise ValueError('original GitHub Actions artifact digest mismatch')
    except (KeyError,TypeError,ValueError) as exc:
        return result(False,'CI artifact acceptance mismatch: '+str(exc))
    return result(True,'GitHub Actions implementation run success, 11 gates, 115 tests/zero skips, 7 BH-V and 3 BH-CQ PASS')


def ci_evidence(root:Path)->dict:
    p=root/'docs/evidence/P04-06/ci-acceptance.json'
    if not p.is_file():return result(False,'P04-06 acceptance file missing',blocked=True)
    try:return ci_payload(json.loads(p.read_text(encoding='utf-8')))
    except (ValueError,OSError) as exc:return result(False,'P04-06 acceptance JSON invalid: '+str(exc))


def integrity(root:Path)->dict:
    invalid=[]
    for rel,expected in HASHES.items():
        f=root/rel
        if not f.is_file() or h(f)!=expected:invalid.append(rel)
    if invalid:return result(False,'Critical baseline source hash mismatch: '+', '.join(invalid))
    verifier=root/'docs/evidence/P04-06/verify_evidence.py'
    if not verifier.is_file():return result(False,'P04-06 archive verifier missing',blocked=True)
    p=run_cmd([sys.executable,str(verifier)],root,timeout=90)
    if p is None or p.returncode:
        return result(False,'P04-06 evidence archive verifier did not PASS: '+((p.stderr or p.stdout)[-300:] if p else 'not executable'))
    return result(True,'MASS-SK-1.0, T-04, fixture pinned SHA-256; P04-06 ZIP and original logs verified')


def versions(root:Path)->dict:
    try:
        version=(root/'VERSION').read_text().strip()
        py=tomllib.loads((root/'pyproject.toml').read_text())['project']['version']
    except (OSError,KeyError,tomllib.TOMLDecodeError) as exc:
        return result(False,'Missing/invalid VERSION or pyproject.toml: '+str(exc))
    if version!=TARGET or py!=TARGET:
        return result(False,f'Expected both VERSION and pyproject.toml {TARGET}; found {version!r}, {py!r}')
    return result(True,'VERSION and Python package metadata match v'+TARGET)


def markdown_fences_balanced(s:str)->bool:
    return sum(bool(re.match(r'^\s*```',l)) for l in s.splitlines())%2==0


def public_docs(root:Path)->dict:
    paths=('README.md','docs/index.md')
    try:r,d=[(root/p).read_text(encoding='utf-8') for p in paths]
    except OSError:return result(False,'README.md or docs/index.md missing')
    issues=[]
    if not markdown_fences_balanced(r):issues.append('README.md unclosed code fence')
    if not markdown_fences_balanced(d):issues.append('docs/index.md unclosed code fence')
    if 'make validatpytest' in r:issues.append('README.md contains invalid make command')
    if not re.search(r'(?:Current (?:development|release) status|Release status):\s*v0\.4\.0',r,re.I):
        issues.append('README.md current release status is not v0.4.0')
    if not re.search(r'(?:Development line|Release status):\s*v0\.4\.0',d,re.I):
        issues.append('docs/index.md current release status is not v0.4.0')
    if 'make behavior-test' not in r or 'BH-P04' not in r:
        issues.append('README.md lacks BH-P04 validation instructions')
    if issues:return result(False,'; '.join(issues))
    return result(True,'Top-level docs correctly describe v0.4.0/BH-P04 and are Markdown-balanced')


def changelog(root:Path)->dict:
    f=root/'CHANGELOG.md'
    if not f.is_file():return result(False,'CHANGELOG.md missing')
    s=f.read_text()
    if not markdown_fences_balanced(s):return result(False,'CHANGELOG.md unclosed Markdown code fence')
    if not re.search(r'^##\s+(?:\[)?v?0\.4\.0(?:\])?\b',s,re.M):
        return result(False,'Missing explicit v0.4.0 release section in CHANGELOG.md')
    return result(True,'v0.4.0 release history present; Markdown fences balanced')


def license_notices(root:Path)->dict:
    """RR-04/05: owner permission is a separate record, never inferred from a file name.

    The decision binds the *actual* reviewed LICENSE and notices bytes. The gate
    intentionally does not authenticate a signatory's legal authority; that
    requires the project's governance review of the rights holder.
    """
    lic=root/'LICENSE'; third=root/'THIRD_PARTY_NOTICES.md'
    if not lic.is_file() or len(lic.read_bytes().strip())<80:
        return result(False,'RR-04: project LICENSE absent or empty; explicit rights-holder license decision required',blocked=True)
    if not third.is_file():
        return result(False,'RR-05: THIRD_PARTY_NOTICES.md absent',blocked=True)
    notice=third.read_text(encoding='utf-8')
    expected=('sosa-2017.ttl','ssn-2017.ttl','qudt-schema-3.5.3.ttl',
              'qudt-unit-3.5.3.ttl','qudt-quantitykind-3.5.3.ttl',
              'qudt-dimensionvector-3.5.3.ttl','owl-time.ttl','prov-o.ttl')
    if any(x not in notice for x in expected) or not all(x in notice.upper() for x in ('QUDT','W3C','OGC','CC BY')):
        return result(False,'RR-05: incomplete per-artifact external vocabulary notices')
    record=root/'docs/governance/DEC-P04-07-rights-approval.json'
    if not record.is_file():
        return result(False,'RR-04/05: no separately recorded rights-holder approval for LICENSE and notices',blocked=True)
    try:
        a=json.loads(record.read_text(encoding='utf-8'))
    except (ValueError,OSError) as e:
        return result(False,'RR-04/05: invalid rights-approval JSON: '+str(e))
    if a.get('schema_version')!='P04-07-rights-approval-v1' or a.get('decision')!='APPROVED':
        return result(False,'RR-04/05: owner decision has not approved redistribution',blocked=True)
    if a.get('third_party_review_status')!='APPROVED_BY_PROJECT_OWNER':
        return result(False,'RR-05: external RDF notice review still pending',blocked=True)
    name=a.get('approved_by',''); holder=a.get('project_rights_holder','')
    if not isinstance(name,str) or not isinstance(holder,str) or any(not x.strip() or x.strip().upper() in ('TBD','UNKNOWN','NONE','PLACEHOLDER') for x in (name,holder)):
        return result(False,'RR-04/05: actual approver and rights-holder identity required',blocked=True)
    date=a.get('approval_date','')
    if not isinstance(date,str) or not re.fullmatch(r'20\d\d-\d\d-\d\d',date):
        return result(False,'RR-04/05: dated approval required',blocked=True)
    spdx=a.get('project_license_spdx','')
    if not isinstance(spdx,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.\-+]{1,64}',spdx) or spdx.upper() in ('TBD','UNKNOWN'):
        return result(False,'RR-04: approved project license identifier required')
    scope=a.get('scope','')
    if not isinstance(scope,str) or 'vendor/external-rdf/T04-2026' not in scope or 'excluded' not in scope.lower():
        return result(False,'RR-04/05: approved project license must explicitly exclude third-party RDF')
    if a.get('owl_time_cc_by_4_reconciled') is not True or a.get('prov_o_exact_artifact_rights_confirmed') is not True:
        return result(False,'RR-05: OWL-Time in-RDF CC BY 4.0 / PROV-O artifact rights remain unverified',blocked=True)
    if a.get('project_license_sha256') != h(lic) or a.get('third_party_notices_sha256') != h(third):
        return result(False,'RR-04/05: rights approval hashes do not match reviewed LICENSE/THIRD_PARTY_NOTICES bytes')
    return result(True,'Rights-holder approved license/8 vendor notices; exact reviewed SHA-256 bytes and T-04 license exceptions recorded')


def release_notes(root:Path)->dict:
    f=root/'docs/releases/v0.4.0-release-notes.md'
    if not f.is_file():return result(False,'Final v0.4.0 release notes absent; draft is not a release record')
    s=f.read_text(encoding='utf-8')
    req=('BH-P04','synthetic','DEFERRED','MASS-SK-1.0','T-04')
    if not all(x.lower() in s.lower() for x in req) or not markdown_fences_balanced(s):
        return result(False,'Release notes do not state P04 limitations/deferred work or have bad Markdown')
    return result(True,'Final release notes describe verified scope, provenance, and exclusions')


def owner_approval(root:Path)->dict:
    f=root/'docs/governance/DEC-P04-07-v0.4.0-release.md'
    if not f.is_file():return result(False,'Release owner approval absent; cannot infer it from passing CI',blocked=True)
    s=f.read_text(encoding='utf-8')
    decision=bool(re.search(r'^\*\*Decision:\*\*\s*APPROVED FOR RELEASE\s*$',s,re.M))
    who=re.search(r'^\*\*Approved by:\*\*\s*(\S.+)\s*$',s,re.M)
    when=bool(re.search(r'^\*\*Approval date:\*\*\s*20\d\d-\d\d-\d\d\s*$',s,re.M))
    if not decision or not who or 'TBD' in who.group(1).upper() or not when:
        return result(False,'Release decision not an explicit dated project-owner approval',blocked=True)
    return result(True,'Explicit, dated release-owner approval recorded')


def run_review(root:Path)->dict:
    checks={
      GATES[0]:source_baseline(root),
      GATES[1]:design_scope(root),
      GATES[2]:ci_evidence(root),
      GATES[3]:integrity(root),
      GATES[4]:versions(root),
      GATES[5]:public_docs(root),
      GATES[6]:changelog(root),
      GATES[7]:license_notices(root),
      GATES[8]:release_notes(root),
      GATES[9]:owner_approval(root)
    }
    gate='GO' if all(x['status']=='PASS' for x in checks.values()) else 'NO_GO'
    return {'schema_version':'P04-07-release-review-v1','profile':'BH-P04',
            'release_candidate':'v0.4.0','source_baseline_commit':BASELINE,
            'reviewed_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'decision':gate,'checks':checks,
            'future_profiles':'DEFERRED: BH-P05/BH-P09',
            'scope_boundary':'Research/synthetic AIS observation ontology; no real AIS performance, SysML parsing or navigation certification',
            'release_tag_created':False}


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,default=ROOT)
    p.add_argument('--report',default='run/release-review/p04-07-readiness.json')
    a=p.parse_args()
    repo=a.repo.resolve()
    out=(repo/a.report).resolve() if not Path(a.report).is_absolute() else Path(a.report).resolve()
    if not out.is_relative_to(repo):p.error('report must be inside repository')
    report=run_review(repo)
    for k,v in report['checks'].items():print(k,v['status'],'—',v['detail'])
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('P04-07 RELEASE READINESS:',report['decision'])
    print('Report:',out)
    return 0 if report['decision']=='GO' else 2

if __name__=='__main__':raise SystemExit(main())
