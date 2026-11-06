#!/usr/bin/env python3
"""Verify RR-05 notice readiness against pinned original vendor bytes; never grants rights."""
from __future__ import annotations
from pathlib import Path
import argparse,hashlib,json,sys
HERE=Path(__file__).resolve().parents[1]
EXPECTED_NOTICE='7387ce9b98911917bb02ea9f3228fad2942fe65c8c7974d2f9890e01620f8ce5'
PREVIOUS_APPROVED_NOTICE='fdcdcaaa2c4e47914f575b26ed6aef0513324957b09e1286ca6012b532022fc4'
CORRIGENDUM_RECORD='docs/governance/DEC-P04-07-RR05-2026-02-approval.json'
EXPECTED_LICENSE='cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30'
EXPECTED={
    'sosa-2017.ttl':'c70b0d1c843c0047e4c98e0a89392e46a05752ff6365bda7f7f55303905a0392',
    'ssn-2017.ttl':'184d86189191146e314cc52b1bceb96fca11e70aacbc160d71588102a5153eb9',
    'qudt-schema-3.5.3.ttl':'807b5b03a8759670a6412822c7624cc6180c5e80ff7b9b3b8e4bee98e1c1c882',
    'qudt-unit-3.5.3.ttl':'89df26d7f8ebb54a80d6bd4e03f3268b16a7acdc7b90490346273c03817971d4',
    'qudt-quantitykind-3.5.3.ttl':'730052a9a760f0f70ac389e8d7e493a729bc8ea2e5f226af68a4b279e7232d81',
    'qudt-dimensionvector-3.5.3.ttl':'eaa321908ce06afa5176c5cbdf375aef4e3176390f18db663a628a96aa9678a3',
    'owl-time.ttl':'251bd6970b0d7a5efa97ff681afe81a297df85deab3d860fa4f8eeba72d8f16c',
    'prov-o.ttl':'7d203989f67b38bca572253942acc5a1bf24ce3ccfece16f072dcb4be2b79a96',
}
INVENTORY='docs/evidence/P04-07/rights-review/RR05-vocabulary-rights-matrix.json'

def sha(p:Path):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(root:Path,*,require_approval=False)->dict:
    findings=[]
    def check(condition,msg):
        if not condition:findings.append(msg)
    lock_file=root/'docs/standards/T04-external-rdf-lock.json'
    try:lock=json.loads(lock_file.read_text(encoding='utf8'))
    except Exception as e:return {'status':'BLOCKED','findings':['T04 lock missing/broken: '+str(e)]}
    entries={it['repo_path']:it for it in lock.get('files',[])}
    check(len(entries)==8,'Expected exactly eight T04 artifacts')
    for name,digest in EXPECTED.items():
        rel='vendor/external-rdf/T04-2026/'+name
        p=root/rel
        check(rel in entries,'Missing T04 entry for '+name)
        if rel in entries:check(entries[rel].get('sha256')==digest,'T04 lock digest mismatch '+name)
        check(p.is_file() and sha(p)==digest,'Source bytes missing/mutated '+name)
    third=root/'THIRD_PARTY_NOTICES.md'
    check(third.is_file() and sha(third)==EXPECTED_NOTICE,'Revised THIRD_PARTY_NOTICES.md hash mismatch')
    if third.is_file():
        txt=third.read_text(encoding='utf8')
        for name in EXPECTED:check(name in txt,'Missing attribution '+name)
        for x in ('W3C','OGC','QUDT.org','CC BY 4.0','PROV-O','dcterms:license','Apache-2.0','excluded'):
            check(x.lower() in txt.lower(),'Notice lacks important scope/license term '+x)
    check((root/'LICENSE').is_file() and sha(root/'LICENSE')==EXPECTED_LICENSE,'Project Apache-2.0 LICENSE mutated')
    for rel,terms in {
        'docs/licenses/third-party/W3C-20150513-LICENSE.txt':('PERMISSION','DISCLAIMERS','W3C'),
        'docs/licenses/third-party/OGC-1.0-LICENSE.txt':('OGC','DISCLAIMER','COPYRIGHT'),
        'docs/evidence/P04-07/rights-review/RR05-PROV-O-EVIDENCE.md':('explicit','W3C','2015'),
        INVENTORY:('prov-o.ttl','owl-time.ttl','sosa-2017.ttl'),
    }.items():
        p=root/rel
        check(p.is_file() and all(t.lower() in p.read_text(encoding='utf8').lower() for t in terms),'Missing/incomplete '+rel)
    if require_approval:
        path=root/'docs/governance/DEC-P04-07-rights-approval.json'
        if not path.is_file():findings.append('Owner rights approval JSON not yet present')
        else:
            try:
                j=json.loads(path.read_text(encoding='utf8'))
                for k,v in {
                  'decision':'APPROVED',
                  'third_party_review_status':'APPROVED_BY_PROJECT_OWNER',
                  'project_license_spdx':'Apache-2.0',
                  'project_license_sha256':EXPECTED_LICENSE,
                  'third_party_notices_sha256':EXPECTED_NOTICE,
                  'owl_time_cc_by_4_reconciled':True,
                  'prov_o_exact_artifact_rights_confirmed':True,
                }.items():check(j.get(k)==v,'Approved rights record has wrong '+k)
                for k in ('approved_by','project_rights_holder','approval_date'):
                    check(isinstance(j.get(k),str) and len(j[k])>=8 and 'TBD' not in j[k], 'Unapproved identity/date '+k)
                # New exact-byte corrigendum approval must be independent of the 2026-11-06 signed RR-05 original.
                # An explicit owner chat text approval is not an electronic or verified signature.
                try:
                    corrigendum=json.loads((root/CORRIGENDUM_RECORD).read_text(encoding='utf8'))
                except (OSError,ValueError) as e:
                    findings.append('Missing/invalid RR05-2026-02 text approval record: '+str(e))
                    corrigendum={}
                for k,v in {
                    'schema_version':'P04-07-RR05-corrigendum-approval-v1',
                    'decision_number':'P04-07-RR05-2026-02',
                    'decision':'APPROVED',
                    'approved_notices_sha256':EXPECTED_NOTICE,
                    'previous_notices_sha256':PREVIOUS_APPROVED_NOTICE,
                    'approval_date':'2026-11-06',
                    'approval_evidence_type':'EXPLICIT_OWNER_CHAT_TEXT_NOT_ELECTRONIC_SIGNATURE',
                    'signed_pdf_supplied':False,
                    'signature_authentication_independently_verified':False,
                }.items():check(corrigendum.get(k)==v,'Corrigendum approval mismatch '+k)
                check(corrigendum.get('approved_by')==j.get('approved_by'),
                      'Corrigendum approver does not match project rights holder')
                amendment=j.get('rr05_corrigendum_2026_02',{})
                for k,v in {
                    'decision_number':'P04-07-RR05-2026-02',
                    'newly_approved_notices_sha256':EXPECTED_NOTICE,
                    'previous_approved_notices_sha256':PREVIOUS_APPROVED_NOTICE,
                    'approval_record':CORRIGENDUM_RECORD,
                    'approval_evidence_type':'EXPLICIT_OWNER_CHAT_TEXT_NOT_ELECTRONIC_SIGNATURE',
                    'signature_authentication_independently_verified':False,
                }.items():check(amendment.get(k)==v,'Rights-register amendment mismatch '+k)
                check(j.get('signed_rr05_owner_decision',{}).get('decision_number')=='P04-07-RR05-2026-01',
                      'Historical signed RR-05 decision changed or missing')
                check((root/'docs/governance/DEC-P04-07-RR05-2026-02-chat-approval.md').is_file(),
                      'Public text approval registration missing')
            except Exception as e:findings.append('Invalid approval record: '+str(e))
    return {'status':'PASS' if not findings else 'BLOCKED' if require_approval and findings==['Owner rights approval JSON not yet present'] else 'FAIL',
            'findings':findings,'notice_sha256':EXPECTED_NOTICE,'vendor_files_checked':len(EXPECTED),'owner_approval_required':require_approval}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',default=str(HERE))
    p.add_argument('--require-approval',action='store_true')
    a=p.parse_args();r=verify(Path(a.repo).resolve(),require_approval=a.require_approval)
    print(json.dumps(r,ensure_ascii=False,indent=2))
    return 0 if r['status']=='PASS' else 2
if __name__=='__main__':sys.exit(main())
