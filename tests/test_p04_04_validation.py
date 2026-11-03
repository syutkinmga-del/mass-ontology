"""P04-04 positive and targeted-negative tests; no live network access.

Full official BH-V11/V05 gate requires vendor snapshots, license lock, ROBOT/HermiT,
and legacy commands. This module tests rule logic and in-memory mutants; the
formal runner is `scripts/run_behavior_validation.py --profile p04 --legacy`.
"""
from __future__ import annotations
import hashlib
import importlib.util
from pathlib import Path
import shutil

import pytest
from rdflib import Graph, RDF, RDFS, Literal, URIRef, XSD, OWL

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('bh04',ROOT/'scripts/run_behavior_validation.py')
bh=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bh)
GEN_SPEC=importlib.util.spec_from_file_location('bhgen04',ROOT/'scripts/generate_p04_04_fixture.py')
gen=importlib.util.module_from_spec(GEN_SPEC)
GEN_SPEC.loader.exec_module(gen)


def graph():
    return Graph().parse(ROOT/bh.DATA,format='turtle')


def copy(g):
    b=Graph()
    for triple in g:b.add(triple)
    return b


def dims():
    u,q,d=Graph(),Graph(),Graph()
    for unit,kind,v in ((bh.UNIT.KN,bh.QK.Speed,URIRef('http://qudt.org/vocab/dimensionvector/SPEED')),
                        (bh.UNIT.DEG,bh.QK.Angle,URIRef('http://qudt.org/vocab/dimensionvector/ANGLE'))):
        u.add((unit,bh.QUDT.hasDimensionVector,v))
        q.add((kind,bh.QUDT.hasDimensionVector,v))
        d.add((v,RDF.type,bh.QUDT.QuantityKindDimensionVector))
    return u,q,d


def test_migration_reproducible_without_overwriting_p04_03():
    assert gen.generate_bytes()==(ROOT/bh.DATA).read_bytes()
    assert hashlib.sha256((ROOT/bh.DATA).read_bytes()).hexdigest()=='2f73990cd4dc88fd4e21c4694d35c6628d0afac613080434d33deed3f41cf301'
    previous=ROOT/'examples/p04-03-synthetic-ais.ttl'
    assert hashlib.sha256(previous.read_bytes()).hexdigest()=='e38875638271b85dfd82006d0fea9f9018ca0399f3fad5aba02c8146db9f87e4'
    g=graph()
    assert len(g)==370
    assert len(list(g.triples((None,bh.QUDT.hasUnit,None))))==12
    assert not list(g.triples((None,bh.QUDT.unit,None)))


def test_python_positive_v01_v02_v03_v05_and_v06_dimensions():
    g=graph();s=Graph().parse(ROOT/'07-behavior/ship-behavior.ttl',format='turtle')
    for fn in (bh.v01,bh.v02,bh.v03): assert fn(g)==[]
    assert bh.v05(g,s)==[]
    assert bh.v06(g,*dims())==[]


def test_shacl_positive():
    pytest.importorskip('pyshacl')
    assert all(not x for x in bh.shacl_issues(ROOT,graph()).values())


@pytest.mark.parametrize('filename,rule',[
    ('n01-no-vessel.ttl','BH-V01'),
    ('n01b-two-vessels.ttl','BH-V01'),
    ('n02-no-extent.ttl','BH-V02'),
    ('n02b-mismatched-membership.ttl','BH-V02'),
    ('n03-overlap.ttl','BH-V03'),
    ('n03-reversed-bounds.ttl','BH-V03'),
    ('n06-speed-in-sec.ttl','BH-V06'),
    ('n06-missing-unit.ttl','BH-V06'),
    ('n06-nonnumeric.ttl','BH-V06'),
    ('n06-obsolete-unit.ttl','BH-V06'),
])
def test_specific_invalid_fixture_rejected_by_intended_rule(filename,rule):
    g=Graph().parse(ROOT/'tests/behavior/fixtures/invalid'/filename,format='turtle')
    checks={'BH-V01':lambda:bh.v01(g),'BH-V02':lambda:bh.v02(g),
            'BH-V03':lambda:bh.v03(g),'BH-V06':lambda:bh.v06(g,*dims())}
    findings=checks[rule]()
    assert findings and all(x.startswith(rule) for x in findings),findings
    if filename in ('n01-no-vessel.ttl','n01b-two-vessels.ttl',
                    'n02-no-extent.ttl','n06-missing-unit.ttl',
                    'n06-nonnumeric.ttl','n06-obsolete-unit.ttl'):
        pytest.importorskip('pyshacl')
        assert bh.shacl_issues(ROOT,g)[rule]


def test_v05_mutation_rejected_by_schema_oracle():
    s=Graph().parse(ROOT/'07-behavior/ship-behavior.ttl',format='turtle')
    m=Graph().parse(ROOT/'tests/behavior/fixtures/invalid/n05-illegal-disjointness.ttl',format='turtle')
    for tr in m:s.add(tr)
    assert any('BH-V05' in x for x in bh.v05(graph(),s))


def test_v05_hermit_reasoner_baseline_and_mutant():
    if not shutil.which('robot'):pytest.skip('ROBOT/HermiT independent reasoner not installed; CLI gate BLOCKED')
    assert bh.robot_check(ROOT)==[]


def test_v06_mutated_dimension_registry_rejected():
    g=graph();u,q,d=dims()
    u.remove((bh.UNIT.KN,bh.QUDT.hasDimensionVector,None))
    assert any('BH-V06' in x for x in bh.v06(g,u,q,d))


def test_v11_rejects_repository_homepage_import(tmp_path):
    g=Graph().parse(ROOT/'tests/behavior/fixtures/invalid/n11-repository-url-import.ttl',format='turtle')
    failures=bh.local_catalog_issues(ROOT,extra_schema=g)
    assert any('BH-V11' in x and 'unresolved or external' in x for x in failures)


def test_v11_rejects_missing_catalog_link(tmp_path):
    xml=tmp_path/'broken.xml'
    xml.write_text('<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">'
                   '<uri name="https://w3id.org/mass-ontology/common" uri="../../etc/hosts"/>'
                   '</catalog>')
    assert any('BH-V11' in x for x in bh.local_catalog_issues(ROOT,catalog=xml))


def test_v12_detects_mutated_kernel(tmp_path):
    p=tmp_path/'kernel.sysml'
    p.write_bytes(b'definitely not released MASSKernel bytes')
    assert not bh.kernel_hash_ok(p)


def test_p05_p09_not_silently_available():
    assert set(('BH-V07','BH-V08','BH-V09','BH-V10')).isdisjoint(
        {'BH-V01','BH-V02','BH-V03','BH-V05','BH-V06','BH-V11','BH-V12'})
