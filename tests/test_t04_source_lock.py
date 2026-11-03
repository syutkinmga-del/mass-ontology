"""Offline self-tests for T-04 source integrity mechanism (NOT real RDF acceptance)."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json
import pytest

SRC = Path(__file__).resolve().parents[1] / 'scripts' / 't04_pin_external_rdf.py'
SPEC = spec_from_file_location('t04', SRC)
t04 = module_from_spec(SPEC)
SPEC.loader.exec_module(t04)


def test_source_registry_explicit_and_versioned():
    urls = [s['url'] for s in t04.SOURCES]
    assert len(urls) == 8 == len(set(urls))
    assert all(x.startswith('https://') for x in urls)
    assert all('/3.5.3/' in x for x in urls if 'qudt.org' in x)
    assert any('/sosa/2017' in x for x in urls)
    assert any('/ssn/2017' in x for x in urls)


def test_rdf_identity_mutation_rejected(tmp_path):
    spec = t04.SOURCES[0]
    good = tmp_path / 'good.ttl'
    items = '\n'.join(f'<{uri}> a <http://www.w3.org/2002/07/owl#Class> .' for uri in spec['must_have'])
    good.write_text(f'<{spec["ontology_iri"]}> a <http://www.w3.org/2002/07/owl#Ontology> .\n{items}\n')
    assert t04.parse_checked(good, spec)['triples'] == len(spec['must_have']) + 1
    bad = tmp_path / 'bad.ttl'
    bad.write_text(good.read_text().replace(spec['ontology_iri'],'https://example.org/bad',1))
    with pytest.raises(ValueError,match='ontology IRI mismatch'):
        t04.parse_checked(bad,spec)


def test_missing_required_term_rejected(tmp_path):
    spec = t04.SOURCES[0]
    f=tmp_path/'missing.ttl'
    f.write_text(f'<{spec["ontology_iri"]}> a <http://www.w3.org/2002/07/owl#Ontology> .\n')
    with pytest.raises(ValueError,match='terms not defined'):
        t04.parse_checked(f,spec)


def test_no_live_fetch_in_verify_and_detect_sha_mutation(tmp_path, monkeypatch):
    src=t04.SOURCES[0]
    monkeypatch.setattr(t04,'SOURCES',[src])
    repo=tmp_path
    vendor=repo/'vendor/external-rdf/T04-2026'
    vendor.mkdir(parents=True)
    d=repo/'docs/standards'
    d.mkdir(parents=True)
    (d/'p04-03-vocabulary-profile-manifest.json').write_text(json.dumps({'project_authored_local_profiles':[]}))
    f=vendor/src['filename']
    f.write_text(f'<{src["ontology_iri"]}> a <http://www.w3.org/2002/07/owl#Ontology> .\n' + '\n'.join(
        f'<{uri}> a <http://www.w3.org/2002/07/owl#Class> .' for uri in src['must_have']))
    info=t04.parse_checked(f,src)
    lock={'schema_version':t04.MARKER,'files':[{**src,**info,
        'repo_path':f'vendor/external-rdf/T04-2026/{src["filename"]}',
        'sha256':t04.sha256(f)}],
        'license_review':{'status':'APPROVED_BY_PROJECT_OWNER'}}
    (d/'T04-external-rdf-lock.json').write_text(json.dumps(lock))
    t04.verify(repo,require_approved=True)
    f.write_text(f.read_text()+'\n# altered\n')
    with pytest.raises(ValueError,match='SHA-256 MISMATCH'):
        t04.verify(repo,require_approved=True)


def test_qudt_353_uses_current_unit_property():
    spec = next(
        s for s in t04.SOURCES
        if s["id"] == "QUDT-SCHEMA-3.5.3"
    )

    assert (
        "http://qudt.org/schema/qudt/hasUnit"
        in spec["must_have"]
    )
    assert (
        "http://qudt.org/schema/qudt/unit"
        not in spec["must_have"]
    )
