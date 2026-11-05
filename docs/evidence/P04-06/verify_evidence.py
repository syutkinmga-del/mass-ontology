#!/usr/bin/env python3
"""Offline verification of committed P04-06 CI evidence (no network needed)."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile
from json import loads
from xml.etree import ElementTree as ET
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]  # repository root: docs/evidence/P04-06 -> 3 parents
EXPECTED_RUN='68e1c4f454caf85958806d761b3a671b51c7803c'
EXPECTED_ARCHIVE_SHA='84ad7fa2fce3f7d9d4817229040e018698ed1fb6bd7262035ec908bd76020649'
EXPECTED_RULES=('BH-V01','BH-V02','BH-V03','BH-V05','BH-V06','BH-V11','BH-V12')
EXPECTED_CQ={'BH-CQ-01':18,'BH-CQ-02':9,'BH-CQ-03':18}

def fail(why):
    raise SystemExit('P04-06 EVIDENCE INVALID: '+why)

try:
    files=HERE/'FILES.sha256'
    for line in files.read_text().splitlines():
        expected,rel=line.split('  ',1)
        path=ROOT/rel
        if not path.is_file() or sha256(path.read_bytes()).hexdigest()!=expected:
            fail('repository file checksum mismatch: '+rel)
    archive=HERE/'github-actions-run-41996276523.zip'
    if sha256(archive.read_bytes()).hexdigest()!=EXPECTED_ARCHIVE_SHA:
        fail('original ZIP SHA-256 mismatch')
    with ZipFile(archive) as z:
        if z.testzip() is not None:fail('ZIP CRC corruption')
        if len(z.namelist())!=16:fail('ZIP entry count')
        original=z.read('SHA256SUMS')
        if original!=(HERE/'artifact-SHA256SUMS').read_bytes():
            fail('original SHA256SUMS differs')
        seen=set()
        for ln in original.decode().splitlines():
            expected,name=ln.split('  ',1)
            if name in seen or sha256(z.read(name)).hexdigest()!=expected:
                fail('ZIP member checksum mismatch: '+name)
            seen.add(name)
        if len(seen)!=15:fail('not all 15 file checksums present')
        for name in ('report.json','behavior-validation.json','behavior-cq.json','summary.md','pytest.xml'):
            if z.read(name)!=(HERE/name).read_bytes():
                fail('extracted report differs from original ZIP: '+name)
        r=loads(z.read('report.json'))
        v=loads(z.read('behavior-validation.json'))
        q=loads(z.read('behavior-cq.json'))
        junit=ET.fromstring(z.read('pytest.xml')).find('testsuite')
    a=loads((HERE/'ci-acceptance.json').read_text())
    if r.get('status')!='PASS' or r.get('tested_commit')!=EXPECTED_RUN:
        fail('CI report not PASS/expected commit')
    if (a['implementation_commit']!=EXPECTED_RUN or a['github_actions']['conclusion']!='success'
        or a['artifact']['sha256']!=EXPECTED_ARCHIVE_SHA):
        fail('attestation metadata inconsistency')
    if set(r['BH_rules'])!=set(EXPECTED_RULES) or any(r['BH_rules'][k]!='PASS' for k in EXPECTED_RULES):
        fail('BH-V statuses incomplete')
    if any(v[k]['status']!='PASS' for k in EXPECTED_RULES):
        fail('original BH-V report failed')
    if set(q['checks'])!=set(EXPECTED_CQ) or q['status']!='PASS':
        fail('original BH-CQ report incomplete')
    for name,rows in EXPECTED_CQ.items():
        info=q['checks'][name]
        if info['status']!='PASS' or info['actual_rows']!=rows or info['expected_rows']!=rows or not info['exact_bindings']:
            fail('BH-CQ bindings differ: '+name)
    if (junit.attrib['tests'],junit.attrib['errors'],junit.attrib['failures'],junit.attrib['skipped'])!=('115','0','0','0'):
        fail('pytest has failures/skips or wrong count')
    if any(g['status']!='PASS' for g in r['gates'].values()) or len(r['gates'])!=11:
        fail('CI gates not all PASS')
    print('P04-06 EVIDENCE INTEGRITY: PASS')
    print('Source implementation commit:',EXPECTED_RUN)
    print('GitHub Actions Run: 41996276523')
    print('Original GitHub artifact and 15 member SHA-256: VERIFIED')
    print('11 gates / 115 tests / 7 BH-V / 3 BH-CQ: PASS')
except (KeyError,ValueError,IndexError,ET.ParseError,OSError,UnicodeDecodeError) as e:
    fail(str(e))
