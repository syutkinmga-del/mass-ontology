"""P04-05 BH-CQ-01..03: exact SPARQL result regression and negative cases.

Separate from CQ-01..14; no live network, no edits of published P04-03/P04-04.
"""
from __future__ import annotations
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from copy import deepcopy
import json
import shutil

import pytest
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import XSD

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'scripts' / 'run_behavior_cq.py'
SPEC = spec_from_file_location('p04_05_behavior_cq', SRC)
cq = module_from_spec(SPEC)
SPEC.loader.exec_module(cq)

EX = Namespace('https://w3id.org/mass-ontology/p04-03/example#')
SOSA = Namespace('http://www.w3.org/ns/sosa/')
TIME = Namespace('http://www.w3.org/2006/time#')
OB = Namespace('https://w3id.org/mass-ontology/observation#')
QUDT = Namespace('http://qudt.org/schema/qudt/')
UNIT = Namespace('http://qudt.org/vocab/unit/')


def graph():
    return Graph().parse(ROOT / cq.BASELINE_FIXTURE, format='turtle')


def test_controlled_fixture_and_oracles_are_locked():
    manifest, expected = cq.validate_manifest(ROOT)
    assert manifest['fixture']['triples'] == len(graph()) == 370
    assert [len(expected[x]['rows']) for x in cq.CQ_IDS] == [18, 9, 18]
    assert manifest['fixture']['sha256'] == (
        '2f73990cd4dc88fd4e21c4694d35c6628d0afac613080434d33deed3f41cf301')


def test_all_three_queries_return_exact_expected_bindings():
    report = cq.run_suite(ROOT)
    assert report['status'] == 'PASS', report
    assert set(report['checks']) == set(cq.CQ_IDS)
    assert all(item['exact_bindings'] is True for item in report['checks'].values())


def test_full_query_results_distinguish_position_speed_course():
    manifest, expected = cq.validate_manifest(ROOT)
    rows = expected['BH-CQ-03']['rows']
    pos = [r for r in rows if r['stateClass']['value'].endswith('#PositionState')]
    speed = [r for r in rows if r['stateClass']['value'].endswith('#SpeedState')]
    course = [r for r in rows if r['stateClass']['value'].endswith('#CourseState')]
    assert len(pos) == len(speed) == len(course) == 6
    assert all({'latitude', 'longitude', 'crs'} <= r.keys() and
               'numericValue' not in r and 'quantityUnit' not in r for r in pos)
    assert all('latitude' not in r and 'longitude' not in r and
               r['numericValue']['datatype'] == str(XSD.decimal) for r in speed + course)
    assert {r['quantityUnit']['value'] for r in speed} == {str(UNIT.KN)}
    assert {r['quantityUnit']['value'] for r in course} == {str(UNIT.DEG)}


def test_cq01_rejects_observation_property_mutation_with_same_row_count():
    g = graph()
    triple = (EX.observation_cog_000, SOSA.observedProperty, OB.CourseOverGround)
    assert triple in g
    g.remove(triple)
    g.add((triple[0], triple[1], OB.SpeedOverGround))
    out = cq.run_suite(ROOT, graph=g)
    assert out['checks']['BH-CQ-01']['status'] == 'FAIL'
    assert out['checks']['BH-CQ-01']['reason'] == 'EXACT_BINDINGS_MISMATCH'
    assert out['checks']['BH-CQ-01']['actual_rows'] == 18
    assert out['checks']['BH-CQ-01']['expected_rows'] == 18
    assert out['checks']['BH-CQ-02']['status'] == 'PASS'


def test_cq02_rejects_changed_bounds_with_same_row_count():
    g = graph()
    triple = (EX.end_002, TIME.inXSDDateTimeStamp,
              Literal('2026-10-28T12:05:00Z', datatype=XSD.dateTimeStamp))
    assert triple in g
    g.remove(triple)
    g.add((triple[0],triple[1],Literal('2026-10-28T12:05:01Z',datatype=XSD.dateTimeStamp)))
    out = cq.run_suite(ROOT, graph=g)
    assert out['checks']['BH-CQ-02']['status'] == 'FAIL'
    assert out['checks']['BH-CQ-02']['actual_rows'] == 9
    assert out['checks']['BH-CQ-02']['expected_rows'] == 9
    assert out['checks']['BH-CQ-01']['status'] == 'PASS'


def test_cq03_rejects_wrong_qudt_unit_with_same_row_count():
    g = graph()
    original = (EX.quantity_sog_000, QUDT.hasUnit, UNIT.KN)
    assert original in g
    g.remove(original)
    g.add((original[0],original[1],UNIT.SEC))
    out = cq.run_suite(ROOT,graph=g)
    assert out['checks']['BH-CQ-03']['status'] == 'FAIL'
    assert out['checks']['BH-CQ-03']['actual_rows'] == 18
    assert out['checks']['BH-CQ-03']['expected_rows'] == 18
    assert out['checks']['BH-CQ-01']['status'] == 'PASS'


def test_cq03_rejects_position_coordinate_mutation_same_row_count():
    g=graph()
    before=(EX.position_result_000, OB.longitudeDegrees,
            Literal('30.100',datatype=XSD.decimal))
    assert before in g
    g.remove(before)
    g.add((before[0],before[1],Literal('30.101',datatype=XSD.decimal)))
    out=cq.run_suite(ROOT,graph=g)
    assert out['checks']['BH-CQ-03']['status']=='FAIL'
    assert out['checks']['BH-CQ-03']['actual_rows']==18


def test_cq03_rejects_returned_zero_replacement_for_unbound_fields():
    _,expected=cq.validate_manifest(ROOT)
    actual=deepcopy(expected['BH-CQ-03'])
    row=next(r for r in actual['rows'] if 'numericValue' in r)
    row['latitude']={'type':'literal','value':'0','datatype':str(XSD.decimal)}
    cmp=cq.compare_exact(actual,expected['BH-CQ-03'])
    assert cmp['status']=='FAIL' and cmp['reason']=='EXACT_BINDINGS_MISMATCH'


def test_duplicate_and_missing_binding_with_unchanged_row_count_fails():
    _,expected=cq.validate_manifest(ROOT)
    actual=deepcopy(expected['BH-CQ-01'])
    actual['rows'][0]=deepcopy(actual['rows'][1])
    cmp=cq.compare_exact(actual,expected['BH-CQ-01'])
    assert cmp['status']=='FAIL'
    assert cmp['actual_rows']==cmp['expected_rows']==18


def test_variable_order_is_part_of_contract():
    _,expected=cq.validate_manifest(ROOT)
    actual=deepcopy(expected['BH-CQ-02'])
    actual['variables']=list(reversed(actual['variables']))
    assert cq.compare_exact(actual,expected['BH-CQ-02'])['reason']=='VARIABLES_MISMATCH'


def test_query_same_cardinality_wrong_bindings_rejected():
    qfile=ROOT/'queries/behavior/bh-cq-01.rq'
    q=qfile.read_text()
    altered=q.replace('sosa:observedProperty ?observedProperty',
                      'sosa:hasFeatureOfInterest ?observedProperty')
    assert q!=altered
    out=cq.run_suite(ROOT, query_overrides={'BH-CQ-01':altered})
    assert out['checks']['BH-CQ-01']['status']=='FAIL'
    assert out['checks']['BH-CQ-01']['actual_rows']==18
    assert out['checks']['BH-CQ-01']['expected_rows']==18
    assert out['checks']['BH-CQ-02']['status']=='PASS'


def test_missing_result_time_reduces_cq01_and_cq03_rows():
    g=graph()
    g.remove((EX.observation_position_001,SOSA.resultTime,None))
    out=cq.run_suite(ROOT, graph=g)
    assert out['checks']['BH-CQ-01']['status']=='FAIL'
    assert out['checks']['BH-CQ-03']['status']=='FAIL'
    assert out['checks']['BH-CQ-02']['status']=='PASS'


def test_fixture_sha_mutation_detected_before_sparql(tmp_path):
    repo=tmp_path/'repo'
    (repo/'docs/standards').mkdir(parents=True)
    (repo/'examples').mkdir()
    shutil.copyfile(ROOT/cq.MANIFEST,repo/cq.MANIFEST)
    fixture=repo/cq.BASELINE_FIXTURE
    shutil.copyfile(ROOT/cq.BASELINE_FIXTURE,fixture)
    fixture.write_bytes(fixture.read_bytes()+b'\n# unauthorized change\n')
    with pytest.raises(cq.CQValidationError,match='SHA-256 mismatch'):
        cq.validate_manifest(repo)


def test_oracle_hash_mutation_detected(tmp_path):
    repo=tmp_path/'repo'
    manifest=json.loads((ROOT/cq.MANIFEST).read_text())
    for rel in [cq.BASELINE_FIXTURE,*[v['query_path'] for v in manifest['cqs'].values()],
                *[v['expected_path'] for v in manifest['cqs'].values()]]:
        (repo/rel).parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/rel,repo/rel)
    (repo/cq.MANIFEST).parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/cq.MANIFEST,repo/cq.MANIFEST)
    golden=repo/'tests/behavior/expected/bh-cq-01.json'
    golden.write_bytes(golden.read_bytes()+b'\n')
    with pytest.raises(cq.CQValidationError,match='SHA-256 mismatch'):
        cq.validate_manifest(repo)


def test_future_profiles_not_claimed():
    assert cq.main(['--profile','p05'])==2
    assert cq.main(['--profile','p09'])==2
