"""P04-03 implementation tests, NOT the complete BH-P04 SHACL/reasoner/CQ suite.

All source fixture data are synthetic, prevalidated and explicitly timestamped.
No remote RDF imports or real AIS decoding occur.
"""
import copy
import importlib.util
import json
from decimal import Decimal
from pathlib import Path
import hashlib
import xml.etree.ElementTree as ET

import pytest
from rdflib import Graph, Literal, Namespace, RDF, OWL, RDFS, XSD, URIRef

ROOT=Path(__file__).resolve().parents[1]
EX=Namespace("https://w3id.org/mass-ontology/p04-03/example#")
BH=Namespace("https://w3id.org/mass-ontology/behavior#")
MAR=Namespace("https://w3id.org/mass-ontology/maritime#")
OBS=Namespace("https://w3id.org/mass-ontology/observation#")
SOSA=Namespace("http://www.w3.org/ns/sosa/")
QUDT=Namespace("http://qudt.org/schema/qudt/")
UNIT=Namespace("http://qudt.org/vocab/unit/")
TIME=Namespace("http://www.w3.org/2006/time#")
PROV=Namespace("http://www.w3.org/ns/prov#")
MEAS=Namespace("https://w3id.org/mass-ontology/measurement#")
LOCAL_MODULES=(
    "05-observation/mass-observation.ttl",
    "06-quantities/mass-measurement-policy.ttl",
    "07-behavior/behavior-observation-bridge.ttl",
)

@pytest.fixture(scope="module")
def gen():
    spec=importlib.util.spec_from_file_location("p04gen",ROOT/"scripts/generate_p04_03_fixture.py")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

@pytest.fixture(scope="module")
def cfg():
    return json.loads((ROOT/"tests/observation/fixtures/p04-03-synthetic-input.json").read_text())

@pytest.fixture(scope="module")
def data():
    g=Graph()
    g.parse(ROOT/"examples/p04-03-synthetic-ais.ttl",format="turtle")
    return g


def one(g,s,p):
    values=list(g.objects(s,p))
    assert len(values)==1,(s,p,values)
    return values[0]


def test_local_ontology_modules_and_import_boundary():
    graph=Graph()
    for name in LOCAL_MODULES:graph.parse(ROOT/name,format="turtle")
    iris={URIRef("https://w3id.org/mass-ontology/"+s) for s in ("observation","measurement","behavior-observation-bridge")}
    for iri in iris:assert (iri,RDF.type,OWL.Ontology) in graph
    assert all(str(imp).startswith("https://w3id.org/mass-ontology/")
               for imp in graph.objects(None,OWL.imports))
    assert (BH.supportedByObservation,RDFS.range,SOSA.Observation) in graph
    assert (BH.hasQuantityValue,RDFS.range,QUDT.QuantityValue) in graph
    assert (MEAS.SOGPolicy,MEAS.acceptedUnit,UNIT.KN) in graph
    assert (MEAS.COGPolicy,MEAS.acceptedUnit,UNIT.DEG) in graph


def test_catalog_has_three_new_mappings():
    ns="{urn:oasis:names:tc:entity:xmlns:xml:catalog}uri"
    root=ET.parse(ROOT/"catalog-v001.xml").getroot()
    mapping={x.attrib["name"]:x.attrib["uri"] for x in root.findall(ns)}
    for suffix,path in (("observation",LOCAL_MODULES[0]),("measurement",LOCAL_MODULES[1]),("behavior-observation-bridge",LOCAL_MODULES[2])):
        assert mapping["https://w3id.org/mass-ontology/"+suffix]==path
    assert len(mapping)==len(root.findall(ns)),"duplicate catalog IRI"


def test_reproducible_bytes_and_graph(gen,cfg,data):
    content=gen.deterministic_turtle(cfg)
    path=ROOT/"examples/p04-03-synthetic-ais.ttl"
    assert content.encode()==path.read_bytes()
    assert len(data)==370
    assert hashlib.sha256(path.read_bytes()).hexdigest()=="e38875638271b85dfd82006d0fea9f9018ca0399f3fad5aba02c8146db9f87e4"


def test_vessel_trajectory_and_three_temporal_units(data):
    assert (EX.vessel_001,RDF.type,MAR.Vessel) in data
    assert one(data,EX.trajectory_001,BH.ofVessel)==EX.vessel_001
    units=set(data.objects(EX.trajectory_001,BH.hasTemporalUnit))
    assert units=={EX.unit_000,EX.unit_001,EX.unit_002}
    for i,unit in enumerate((EX.unit_000,EX.unit_001,EX.unit_002)):
        assert one(data,unit,BH.partOfTrajectory)==EX.trajectory_001
        assert int(one(data,unit,BH.segmentIndex))==i
        assert (unit,RDF.type,BH.TemporalUnit) in data
        assert (unit,RDF.type,TIME.ProperInterval) not in data
        interval=one(data,unit,BH.hasTemporalExtent)
        assert (interval,RDF.type,TIME.ProperInterval) in data


def test_separate_time_instances_and_known_gap(data):
    for i in range(3):
        interval=EX[f"interval_{i:03}"]
        a=one(data,one(data,interval,TIME.hasBeginning),TIME.inXSDDateTimeStamp)
        b=one(data,one(data,interval,TIME.hasEnd),TIME.inXSDDateTimeStamp)
        assert a.datatype==XSD.dateTimeStamp and b.datatype==XSD.dateTimeStamp
        assert a<b
    assert one(data,EX.coverage_gap_001,OBS.gapStartsAt)==Literal("2026-10-28T12:02:00Z",datatype=XSD.dateTimeStamp)
    assert one(data,EX.coverage_gap_001,OBS.gapEndsAt)==Literal("2026-10-28T12:04:00Z",datatype=XSD.dateTimeStamp)
    assert (EX.unit_001,BH.nextTemporalUnit,EX.unit_002) in data
    assert list(data.triples((None,TIME.intervalMeets,None)))==[]


def test_sosa_observations_and_qudt_values(data):
    assert len(set(data.subjects(RDF.type,SOSA.Observation)))==18
    assert len(set(data.subjects(RDF.type,QUDT.QuantityValue)))==12
    for idx in range(6):
        suffix=f"{idx:03}"
        for kind,unit,prop in (("sog",UNIT.KN,OBS.SpeedOverGround),("cog",UNIT.DEG,OBS.CourseOverGround)):
            o=EX[f"observation_{kind}_{suffix}"]
            q=one(data,o,SOSA.hasResult)
            assert (q,RDF.type,QUDT.QuantityValue) in data
            assert one(data,q,QUDT.unit)==unit
            assert one(data,q,QUDT.numericValue).datatype==XSD.decimal
            assert one(data,o,SOSA.observedProperty)==prop
            assert one(data,o,SOSA.hasFeatureOfInterest)==EX.vessel_001
            assert (o,PROV.wasDerivedFrom,EX[f"raw_{suffix}"]) in data


def test_sample_at_boundary_assigned_to_next_segment(data):
    for kind,state in (("sog",EX.speed_001),("cog",EX.course_001),("position",EX.position_001)):
        obs=EX[f"observation_{kind}_002"]
        assert (state,BH.supportedByObservation,obs) in data
        previous={"sog":EX.speed_000,"cog":EX.course_000,"position":EX.position_000}[kind]
        assert (previous,BH.supportedByObservation,obs) not in data


def test_observation_event_result_receipt_are_distinct(data):
    event=one(data,EX.observation_sog_000,SOSA.phenomenonTime)
    assert (event,RDF.type,TIME.Instant) in data
    assert one(data,event,TIME.inXSDDateTimeStamp)==Literal("2026-10-28T12:00:00Z",datatype=XSD.dateTimeStamp)
    assert one(data,EX.raw_000,OBS.receivedAtTime)==Literal("2026-10-28T12:00:01Z",datatype=XSD.dateTimeStamp)
    assert one(data,EX.observation_sog_000,SOSA.resultTime)==Literal("2026-10-28T12:00:02Z",datatype=XSD.dateTimeStamp)
    assert one(data,EX.raw_000,OBS.ingestedAtTime)==Literal("2026-10-28T12:00:03Z",datatype=XSD.dateTimeStamp)
    assert one(data,EX.raw_000,OBS.eventTimeQuality)==Literal("provided-complete-utc")
    assert list(data.triples((None,SOSA.madeBySensor,None)))==[]


def test_provenance_and_segmentation_identity(data):
    assert (EX.segmentation_run,RDF.type,PROV.Activity) in data
    assert one(data,EX.segmentation_run,OBS.segmentationMethodId)==Literal("fixed-boundary-synthetic")
    assert one(data,EX.segmentation_run,OBS.segmentationVersion)==Literal("1.0.0")
    assert one(data,EX.segmentation_run,OBS.sampleAssignmentPolicy)==Literal("[start,end)")
    for i in range(3):
        assert (EX[f"unit_{i:03}"],PROV.wasGeneratedBy,EX.segmentation_run) in data
    assert (EX.unit_002,PROV.wasDerivedFrom,EX.raw_004) in data
    assert (EX.unit_001,PROV.wasDerivedFrom,EX.raw_004) not in data


def test_position_named_crs_no_geosparql(data):
    result=one(data,EX.observation_position_000,SOSA.hasResult)
    assert (result,RDF.type,OBS.PositionResult) in data
    assert Decimal(str(one(data,result,OBS.latitudeDegrees)))==Decimal("59.901")
    assert Decimal(str(one(data,result,OBS.longitudeDegrees)))==Decimal("30.100")
    assert one(data,result,OBS.coordinateReferenceSystem)==URIRef("http://www.opengis.net/def/crs/EPSG/0/4326")
    assert not any("geosparql" in str(p) for p in data.predicates())


def test_unavailable_measurement_not_made_into_quantity(gen,cfg):
    mod=copy.deepcopy(cfg)
    mod["samples"][0]["sog_kn"]=None
    mod["samples"][0]["sog_status"]="unavailable"
    g=gen.build_graph(mod)
    assert (EX.observation_sog_000,RDF.type,SOSA.Observation) not in g
    assert (EX.quantity_sog_000,RDF.type,QUDT.QuantityValue) not in g
    assert (EX.raw_000,OBS.sourceAvailability,Literal("SOG:unavailable")) in g
    assert (EX.observation_cog_000,RDF.type,SOSA.Observation) in g

@pytest.mark.parametrize("mutation,expected",[
    (lambda d:d["samples"][0].update(event_time="12:00:00Z"),"full-utc-second-timestamp-required"),
    (lambda d:d.update(source_event_time_quality="reconstructed"),"untrusted-or-reconstructed-event-time"),
    (lambda d:d["unit_policy"].update(sog="http://qudt.org/vocab/unit/SEC"),"sog_kn-invalid-unit-policy"),
    (lambda d:d["samples"][0].update(sog_kn="not-a-number"),"invalid-sog_kn"),
    (lambda d:d["samples"][0].update(sog_kn="8.2",sog_status="unavailable"),"sog_kn-sentinel-cannot-be-valid-numeric"),
    (lambda d:d["samples"][0].update(cog_deg="360.0"),"invalid-cog"),
    (lambda d:d["samples"][0].update(lat_deg="91"),"invalid-coordinate"),
    (lambda d:d["samples"][0].update(event_time="2026-10-28T12:02:00Z"),"sample-outside-segment-or-overlap"),
    (lambda d:d["segmentation"].update(thresholds={"gap_seconds":120}),"unapproved-segmentation-policy"),
])
def test_reject_invalid_input(gen,cfg,mutation,expected):
    mod=copy.deepcopy(cfg)
    mutation(mod)
    with pytest.raises(ValueError,match=expected):gen.build_graph(mod)
