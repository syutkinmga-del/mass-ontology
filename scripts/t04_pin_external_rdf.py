#!/usr/bin/env python3
"""T-04: acquire, pin and offline-verify authoritative RDF snapshots.

No external ontology imports are added to MASS OWL files or XML catalog.
Do not claim BH-V11 PASS based solely on this source-integrity gate.
Requires: Python >=3.12, rdflib from repository .venv; no requests dependency.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from urllib.request import Request, urlopen
from urllib.parse import urlsplit

from rdflib import Graph, URIRef
from rdflib.namespace import RDF, OWL

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'vendor' / 'external-rdf' / 'T04-2026'
LOCK = ROOT / 'docs' / 'standards' / 'T04-external-rdf-lock.json'
MARKER = 'T04-2026-v1'

# Canonical W3C version URLs and qudt.org versioned releases, not mutable latest URLs.
# Exact graph subjects/OWL versionIRIs are audited from the retrieved bytes.
SOURCES = [
    dict(id='SOSA-2017', filename='sosa-2017.ttl', url='https://www.w3.org/ns/sosa/2017',
         standard='SOSA/SSN W3C Recommendation 19 October 2017', namespace='http://www.w3.org/ns/sosa/',
         ontology_iri='http://www.w3.org/ns/sosa/', version_iri='http://www.w3.org/ns/sosa/2017',
         official_git_fallback='https://raw.githubusercontent.com/w3c/sdw/f3171647f6437b73e1caf871f056d233feb4a9da/ssn/integrated/sosa.ttl',
         official_git_blob_sha1='ef1319ba171278197bf4735b858eec086f2321a0',
         must_have=['http://www.w3.org/ns/sosa/Observation', 'http://www.w3.org/ns/sosa/hasResult',
                    'http://www.w3.org/ns/sosa/phenomenonTime', 'http://www.w3.org/ns/sosa/resultTime'],
         license_code='W3C-OGC-SOSA-SSN-2017'),
    dict(id='SSN-2017', filename='ssn-2017.ttl', url='https://www.w3.org/ns/ssn/2017',
         standard='SOSA/SSN W3C Recommendation 19 October 2017', namespace='http://www.w3.org/ns/ssn/',
         ontology_iri='http://www.w3.org/ns/ssn/', version_iri='http://www.w3.org/ns/ssn/2017',
         official_git_fallback='https://raw.githubusercontent.com/w3c/sdw/f3171647f6437b73e1caf871f056d233feb4a9da/ssn/integrated/ssn.ttl',
         official_git_blob_sha1='0b6a78bae8f90ea6db1d39b49b9c66d164637fff',
         must_have=['http://www.w3.org/ns/ssn/System', 'http://www.w3.org/ns/ssn/Deployment'],
         license_code='W3C-OGC-SOSA-SSN-2017'),
    dict(id='QUDT-SCHEMA-3.5.3', filename='qudt-schema-3.5.3.ttl', url='https://qudt.org/3.5.3/schema/qudt',
         standard='QUDT 3.5.3, 2026-10-20', namespace='http://qudt.org/schema/qudt/',
         ontology_iri='http://qudt.org/3.5.3/schema/qudt', version_iri='http://qudt.org/3.5.3/schema/qudt',
         must_have=['http://qudt.org/schema/qudt/QuantityValue', 'http://qudt.org/schema/qudt/numericValue',
                    'http://qudt.org/schema/qudt/hasUnit'],license_code='QUDT-CC-BY-4.0'),
    dict(id='QUDT-UNITS-3.5.3', filename='qudt-unit-3.5.3.ttl', url='https://qudt.org/3.5.3/vocab/unit',
         standard='QUDT 3.5.3, 2026-10-20', namespace='http://qudt.org/vocab/unit/',
         ontology_iri='http://qudt.org/3.5.3/vocab/unit', version_iri='http://qudt.org/3.5.3/vocab/unit',
         must_have=['http://qudt.org/vocab/unit/KN','http://qudt.org/vocab/unit/DEG'],
         license_code='QUDT-CC-BY-4.0'),
    dict(id='QUDT-QUANTITYKIND-3.5.3', filename='qudt-quantitykind-3.5.3.ttl',
         url='https://qudt.org/3.5.3/vocab/quantitykind', standard='QUDT 3.5.3, 2026-10-20',
         namespace='http://qudt.org/vocab/quantitykind/',
         ontology_iri='http://qudt.org/3.5.3/vocab/quantitykind',
         version_iri='http://qudt.org/3.5.3/vocab/quantitykind',
         must_have=['http://qudt.org/vocab/quantitykind/Speed'],license_code='QUDT-CC-BY-4.0'),
    dict(id='QUDT-DIMENSIONVECTOR-3.5.3', filename='qudt-dimensionvector-3.5.3.ttl',
         url='https://qudt.org/3.5.3/vocab/dimensionvector', standard='QUDT 3.5.3, 2026-10-20',
         namespace='http://qudt.org/vocab/dimensionvector/',
         ontology_iri='http://qudt.org/3.5.3/vocab/dimensionvector',
         version_iri='http://qudt.org/3.5.3/vocab/dimensionvector',
         must_have=[], license_code='QUDT-CC-BY-4.0'),
    dict(id='OWL-TIME', filename='owl-time.ttl',url='https://www.w3.org/2006/time',
         standard='W3C OWL-Time Recommendation 2017; RDF may contain subsequent maintenance updates',
         namespace='http://www.w3.org/2006/time#',ontology_iri='http://www.w3.org/2006/time',
         version_iri=None,
         must_have=['http://www.w3.org/2006/time#ProperInterval',
                    'http://www.w3.org/2006/time#Instant',
                    'http://www.w3.org/2006/time#inXSDDateTimeStamp'],
         license_code='W3C-SOFTWARE-AND-DOCUMENT'),
    dict(id='PROV-O',filename='prov-o.ttl',url='https://www.w3.org/ns/prov-o.ttl',
         standard='W3C PROV-O Recommendation 2013-04-30',namespace='http://www.w3.org/ns/prov#',
         ontology_iri='http://www.w3.org/ns/prov#',version_iri=None,
         must_have=['http://www.w3.org/ns/prov#Entity', 'http://www.w3.org/ns/prov#Activity',
                    'http://www.w3.org/ns/prov#wasDerivedFrom', 'http://www.w3.org/ns/prov#wasGeneratedBy'],
         license_code='W3C-SOFTWARE-AND-DOCUMENT'),
]

TRUSTED_HOSTS = {'www.w3.org', 'w3.org', 'qudt.org', 'www.qudt.org', 'raw.githubusercontent.com'}
MAX_BYTES = 40 * 1024 * 1024


def sha256(p: Path) -> str:
    d = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            d.update(chunk)
    return d.hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def parse_checked(p: Path, src: dict) -> dict:
    graph = Graph()
    raw = p.read_bytes()
    if raw[:256].lower().find(b'<html') >= 0 or b'<!doctype html' in raw[:512].lower():
        raise ValueError(f'{src["id"]}: HTML received instead of RDF')
    # Exact file bytes are not normalized/reserialized. HTTP Content-Type is not trusted.
    errs = []
    for fmt in ('turtle','xml'):
        try:
            graph.parse(data=raw, format=fmt)
            break
        except Exception as exc:
            errs.append(f'{fmt}: {str(exc)[:180]}')
            graph = Graph()
    else:
        raise ValueError(f'{src["id"]}: not valid Turtle or RDF/XML: {errs}')
    ontologies = sorted(str(x) for x in graph.subjects(RDF.type, OWL.Ontology))
    if not ontologies:
        raise ValueError(f'{src["id"]}: no rdf:type owl:Ontology found')
    expected = src['ontology_iri']
    def iri_equivalent(uri):
        return uri.rstrip('/#') == expected.rstrip('/#')
    # For QUDT some graphs use versioned ontology subjects; record instead of assuming generic ontology IRI.
    if not any(iri_equivalent(x) for x in ontologies):
        raise ValueError(f'{src["id"]}: ontology IRI mismatch; expected {expected}; actual {ontologies[:5]}')
    missing = [iri for iri in src['must_have'] if not any(graph.triples((URIRef(iri),None,None)))]
    if missing:
        raise ValueError(f'{src["id"]}: terms not defined: {missing}')
    version_iris = sorted({str(x) for x in graph.objects(None, OWL.versionIRI)})
    # QUDT release graphs require a matching explicit owl:versionIRI if one is present;
    # for W3C 2017 permanent URI distinguish retrieval path from RDF-declared versionIRI.
    if src['id'].startswith('QUDT-') and version_iris and src['version_iri'] not in version_iris:
        raise ValueError(f'{src["id"]}: version mismatch: expected {src["version_iri"]}, actual {version_iris[:5]}')
    return {'triples': len(graph), 'ontology_iris_found':ontologies,
            'owl_version_iris_found':version_iris,
            'version_iri_declared':src['version_iri'] in version_iris if src['version_iri'] else None}


def download_one(src: dict, path: Path, url: str | None = None) -> str:
    req = Request(url or src['url'], headers={
        'Accept': 'text/turtle, application/x-turtle;q=0.9, application/rdf+xml;q=0.7',
        'User-Agent': 'MASS-Ontology-T04-Dependency-Control/1.0 (offline-reproducibility)'})
    with urlopen(req,timeout=90) as response:
        actual_url = response.geturl()
        hostname = urlsplit(actual_url).hostname
        if hostname not in TRUSTED_HOSTS or urlsplit(actual_url).scheme != 'https':
            raise ValueError(f'{src["id"]}: unapproved redirect URL: {actual_url}')
        length = 0
        with path.open('wb') as dst:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                length += len(chunk)
                if length > MAX_BYTES:
                    raise ValueError(f'{src["id"]}: file exceeds {MAX_BYTES} bytes')
                dst.write(chunk)
    if length < 100:
        raise ValueError(f'{src["id"]}: unexpectedly small RDF file: {length} bytes')
    return actual_url


def local_profile_check(repo: Path, manifest: dict) -> None:
    p = repo / 'docs' / 'standards' / 'p04-03-vocabulary-profile-manifest.json'
    if not p.exists():
        raise ValueError('P04-03 source manifest missing')
    source = json.loads(p.read_text())
    for row in source.get('project_authored_local_profiles',[]):
        file = repo / row['path']
        if not file.is_file() or sha256(file) != row['sha256']:
            raise ValueError(f'P04-03 local project profile has changed: {row["path"]}')
    manifest['p04_03_local_profiles_checked'] = len(source.get('project_authored_local_profiles', []))


def acquire(repo: Path) -> None:
    dest = repo / 'vendor' / 'external-rdf' / 'T04-2026'
    lock = repo / 'docs' / 'standards' / 'T04-external-rdf-lock.json'
    if lock.exists() or dest.exists():
        raise ValueError('A T-04 lock/snapshot directory already exists. Run --verify; never silently repin existing bytes.')
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.t04-temp-',dir=dest.parent) as staging:
        st=Path(staging)
        result={'schema_version':MARKER,'captured_utc':now(),
            'status':'PINNED_BYTES_PENDING_LICENSE_SIGNOFF_AND_BH_V11',
            'repository_commit_checked':get_commit(repo),
            'import_policy':'REFERENCE_ONLY_NO_LIVE_EXTERNAL_OWL_IMPORTS',
            'redistribution_policy':'Retain upstream attribution and license notices; consult local review doc.',
            'license_review':{'status':'PENDING_OWNER_APPROVAL','approved_utc':None},
            'files':[]}
        local_profile_check(repo,result)
        for src in SOURCES:
            p=st/src['filename']
            print(f'ACQUIRE {src["id"]}: {src["url"]}',flush=True)
            try:
                resolved=download_one(src,p)
                details=parse_checked(p,src)
            except Exception as primary_error:
                if not src.get('official_git_fallback'):
                    raise
                print(f'  Publisher canonical URL failed verification: {primary_error}', flush=True)
                print('  Trying W3C official immutable Git snapshot (not a mutable latest URL)',flush=True)
                resolved=download_one(src,p,src['official_git_fallback'])
                details=parse_checked(p,src)
                git_blob=b'blob '+str(p.stat().st_size).encode('ascii')+b'\0'+p.read_bytes()
                git_blob_hash=hashlib.sha1(git_blob).hexdigest()  # git native object identity, not security checksum
                if git_blob_hash != src['official_git_blob_sha1']:
                    raise ValueError(f'Official W3C git blob mismatch for {src["id"]}')
            entry={**src,'resolved_url':resolved,'repo_path':f'vendor/external-rdf/T04-2026/{src["filename"]}',
                   'sha256':sha256(p),'file_size_bytes':p.stat().st_size,**details}
            result['files'].append(entry)
            print(f'  RDF {details["triples"]} triples, sha256={entry["sha256"]}',flush=True)
        lock.parent.mkdir(parents=True,exist_ok=True)
        # Transactional: do not write lock until every remote graph has parsed and passed ontology/term checks.
        os.replace(st,dest)
        lock.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        print('T04 RDF SNAPSHOTS ACQUIRED and LOCKED; license owner acceptance still required.')


def get_commit(repo:Path) -> str | None:
    import subprocess
    try:
        return subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def verify(repo:Path, require_approved:bool = False) -> dict:
    lock=repo/'docs'/'standards'/'T04-external-rdf-lock.json'
    if not lock.is_file():
        raise ValueError('T-04 lock missing; run --acquire first')
    m=json.loads(lock.read_text(encoding='utf-8'))
    if m['schema_version'] != MARKER or len(m['files']) != len(SOURCES):
        raise ValueError('T-04 lock incomplete or incompatible')
    source_by_id={s['id']:s for s in SOURCES}
    seen=set()
    local_profile_check(repo,m)
    for row in m['files']:
        sid=row['id']
        if sid in seen or sid not in source_by_id:
            raise ValueError('duplicate/unrecognized snapshot ID')
        seen.add(sid)
        src=source_by_id[sid]
        for key in ('url','version_iri','ontology_iri','namespace','license_code','filename','official_git_fallback','official_git_blob_sha1'):
            if row.get(key) != src.get(key):
                raise ValueError(f'{sid}: source metadata modified: {key}')
        path=repo/row['repo_path']
        if not path.is_file() or path.is_symlink() or path.resolve() != (repo/'vendor'/'external-rdf'/'T04-2026'/src['filename']).resolve():
            raise ValueError(f'{sid}: snapshot missing, symlink, or wrong path')
        digest=sha256(path)
        if digest!=row['sha256']:
            raise ValueError(f'{sid}: SHA-256 MISMATCH actual={digest} expected={row["sha256"]}')
        info=parse_checked(path,src)
        if info['triples']!=row['triples'] or info['ontology_iris_found']!=row['ontology_iris_found']:
            raise ValueError(f'{sid}: RDF graph identity changed')
        print(f'PASS {sid}: sha256={digest}, triples={info["triples"]}')
    if require_approved and m['license_review']['status']!='APPROVED_BY_PROJECT_OWNER':
        raise ValueError('license attribution review still pending; run --approve-licenses after review')
    print('T-04 BYTE/IRI/TERMS VERIFICATION PASS')
    print('LICENSE CONTROL:',m['license_review']['status'])
    print('BH-V11: NOT CLAIMED (requires subsequent import/catalog negative tests).')
    return m


def approve_licenses(repo:Path):
    m=verify(repo)
    m['license_review']={'status':'APPROVED_BY_PROJECT_OWNER','approved_utc':now(),
      'acknowledgment':'Project owner manually confirmed review of docs/standards/T04-source-and-license-review.md and upstream attribution requirements.'}
    m['status']='T04_RDF_AND_LICENSE_CONTROLS_VERIFIED_BH_V11_PENDING'
    lock=repo/'docs'/'standards'/'T04-external-rdf-lock.json'
    lock.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('LICENSE REVIEW ACKNOWLEDGED. Run --verify for offline repeatability.')


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--acquire',action='store_true',help='download verified versioned RDF artifacts and lock original bytes')
    mode.add_argument('--verify',action='store_true',help='strict offline byte and graph-IRI check')
    mode.add_argument('--approve-licenses',action='store_true',help='record project owner license signoff after reviewing terms')
    p.add_argument('--repo',type=Path,default=ROOT)
    a=p.parse_args();repo=a.repo.resolve()
    try:
        if a.acquire:acquire(repo)
        elif a.verify:verify(repo,require_approved=True)
        else:approve_licenses(repo)
        return 0
    except Exception as e:
        print(f'T-04 BLOCKED: {e}',file=sys.stderr)
        return 1

if __name__=='__main__':raise SystemExit(main())
