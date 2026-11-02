"""P04-02 scoped structural/temporal checks and mutation-negative cases.

These tests are NOT the official BH-V01..BH-V06 acceptance suite; the complete
SHACL, reasoner, external ontology and AIS profiles are P04-03/P04-04 work.
No online ontology resolution or automatic owl:imports is performed.
"""
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest
from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, URIRef, Literal

ROOT = Path(__file__).resolve().parents[1]
BH = Namespace("https://w3id.org/mass-ontology/behavior#")
MARITIME = Namespace("https://w3id.org/mass-ontology/maritime#")
COMMON = Namespace("https://w3id.org/mass-ontology/common#")
MASS = Namespace("https://w3id.org/mass-ontology/core#")
NAV = Namespace("https://w3id.org/mass-ontology/navigation#")
TIME = Namespace("http://www.w3.org/2006/time#")
EX = Namespace("https://w3id.org/mass-ontology/p04-02/example#")
SOURCE_FILES = (
    "01-common/common-core.ttl",
    "02-maritime/maritime-core.ttl",
    "02-maritime/vessel-compatibility.ttl",
    "03-mass-core/mass-core.ttl",
    "04-navigation/navigation-situation.ttl",
    "07-behavior/ship-behavior.ttl",
    "examples/p04-02-structural-trajectory.ttl",
)
DATA_FILE = "examples/p04-02-structural-trajectory.ttl"


def graph_from_repo():
    graph = Graph()
    for file in SOURCE_FILES:
        graph.parse(ROOT / file, format="turtle")
    return graph


def data_only():
    graph = Graph()
    graph.parse(ROOT / DATA_FILE, format="turtle")
    return graph


def parents(graph, cls):
    seen, queue = set(), [cls]
    while queue:
        x = queue.pop()
        if x in seen:
            continue
        seen.add(x)
        queue.extend(graph.objects(x, RDFS.subClassOf))
    return seen


def exactly_one(graph, subject, predicate):
    values = list(graph.objects(subject, predicate))
    if len(values) != 1:
        raise ValueError("expected-exactly-one")
    return values[0]


def utc_instant(graph, node):
    if (node, RDF.type, TIME.Instant) not in graph:
        raise ValueError("not-time-instant")
    value = exactly_one(graph, node, TIME.inXSDDateTimeStamp)
    if not isinstance(value, Literal) or value.datatype != XSD.dateTimeStamp:
        raise ValueError("not-date-time-stamp")
    dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("missing-timezone")
    return dt.astimezone(timezone.utc)


def interval_bounds(graph, interval):
    if (interval, RDF.type, TIME.ProperInterval) not in graph:
        raise ValueError("not-proper-interval")
    start = utc_instant(graph, exactly_one(graph, interval, TIME.hasBeginning))
    end = utc_instant(graph, exactly_one(graph, interval, TIME.hasEnd))
    if start >= end:
        raise ValueError("invalid-bounds")
    return start, end


def fixture_errors(graph):
    """Local curated-fixture oracle; BH-V01/02/03 will later use SHACL+Python."""
    problems = []
    tracks = set(graph.subjects(RDF.type, BH.Trajectory))
    for track in tracks:
        vessels = list(graph.objects(track, BH.ofVessel))
        if len(vessels) != 1 or any((v, RDF.type, MARITIME.Vessel) not in graph for v in vessels):
            problems.append("one-explicit-vessel")
        elif (vessels[0], BH.hasTrajectory, track) not in graph:
            problems.append("vessel-reciprocal-link")

        units = set(graph.objects(track, BH.hasTemporalUnit))
        if not units:
            problems.append("empty-track")
        sorted_units = []
        for unit in units:
            if (unit, RDF.type, BH.TemporalUnit) not in graph:
                problems.append("not-temporal-unit")
            parents_ = list(graph.objects(unit, BH.partOfTrajectory))
            if parents_ != [track]:
                problems.append("unit-parent-inconsistent")
            try:
                extent = exactly_one(graph, unit, BH.hasTemporalExtent)
                if extent == unit:
                    problems.append("segment-equals-interval")
                bounds = interval_bounds(graph, extent)
            except (ValueError, TypeError, OverflowError):
                problems.append("invalid-temporal-extent")
                bounds = None
            try:
                idx = exactly_one(graph, unit, BH.segmentIndex)
                if idx.datatype != XSD.nonNegativeInteger or int(str(idx)) < 0:
                    raise ValueError("invalid-segment-index")
                idx_value = int(str(idx))
            except (ValueError, AttributeError, TypeError):
                problems.append("invalid-segment-index")
                idx_value = None
            if bounds is not None and idx_value is not None:
                sorted_units.append((idx_value, unit, *bounds))
        if len(sorted_units) == len(units):
            sorted_units.sort()
            indices = [item[0] for item in sorted_units]
            if indices != list(range(len(indices))):
                problems.append("segment-indices-not-contiguous")
            for i, (_idx, current, start, end) in enumerate(sorted_units):
                if i and start < sorted_units[i - 1][3]:
                    problems.append("segment-overlap")
                nxt = list(graph.objects(current, BH.nextTemporalUnit))
                if nxt and (i == len(sorted_units) - 1 or nxt != [sorted_units[i + 1][1]]):
                    problems.append("invalid-sequence-adjacency")
        for unit in units:
            for desc in graph.objects(unit, BH.hasPhysicalBehavior):
                if (desc, RDF.type, BH.PositionState) not in graph and \
                   (desc, RDF.type, BH.SpeedState) not in graph and \
                   (desc, RDF.type, BH.CourseState) not in graph:
                    problems.append("unexpected-physical-description")
    return problems


def test_ontology_identity_and_local_imports():
    graph = graph_from_repo()
    ontology = URIRef("https://w3id.org/mass-ontology/behavior")
    assert (ontology, RDF.type, OWL.Ontology) in graph
    assert (ontology, OWL.imports, URIRef("https://w3id.org/mass-ontology/common")) in graph
    assert (ontology, OWL.imports, URIRef("https://w3id.org/mass-ontology/maritime")) in graph
    assert not list(graph.triples((ontology, OWL.imports, URIRef("http://www.w3.org/2006/time"))))


def test_class_hierarchy_representation_not_process_or_interval():
    graph = graph_from_repo()
    for cls in (BH.Trajectory, BH.TemporalUnit, BH.PhysicalBehavior):
        assert COMMON.InformationArtifact in parents(graph, cls)
        assert COMMON.Process not in parents(graph, cls)
        assert TIME.ProperInterval not in parents(graph, cls)
    for cls in (BH.PositionState, BH.SpeedState, BH.CourseState):
        assert BH.PhysicalBehavior in parents(graph, cls)
    assert BH.BehaviorDescription in parents(graph, BH.PhysicalBehavior)


def test_expected_property_semantics():
    graph = graph_from_repo()
    expected = {
        BH.ofVessel: (BH.Trajectory, MARITIME.Vessel),
        BH.hasTrajectory: (MARITIME.Vessel, BH.Trajectory),
        BH.hasTemporalUnit: (BH.Trajectory, BH.TemporalUnit),
        BH.partOfTrajectory: (BH.TemporalUnit, BH.Trajectory),
        BH.hasTemporalExtent: (BH.TemporalUnit, TIME.TemporalEntity),
        BH.hasPhysicalBehavior: (BH.TemporalUnit, BH.PhysicalBehavior),
        BH.nextTemporalUnit: (BH.TemporalUnit, BH.TemporalUnit),
    }
    for prop, (domain, range_) in expected.items():
        assert (prop, RDF.type, OWL.ObjectProperty) in graph
        assert (prop, RDFS.domain, domain) in graph
        assert (prop, RDFS.range, range_) in graph
    assert (BH.segmentIndex, RDF.type, OWL.DatatypeProperty) in graph
    assert (BH.segmentIndex, RDFS.range, XSD.nonNegativeInteger) in graph


def test_no_premature_equivalences_disjointness_or_future_axioms():
    schema = Graph()
    schema.parse(ROOT / "07-behavior/ship-behavior.ttl", format="turtle")
    for property_ in (OWL.equivalentClass, OWL.disjointWith, OWL.sameAs, OWL.inverseOf,
                      OWL.propertyChainAxiom):
        assert not list(schema.triples((None, property_, None)))
    for forbidden in (BH.SemanticBehavior, BH.InteractionBehavior, BH.EnvironmentSpace):
        assert (forbidden, RDF.type, OWL.Class) not in schema
    for forbidden_import in ("http://www.w3.org/2006/time", "https://github.com/BFO-ontology/BFO-2020"):
        assert (None, OWL.imports, URIRef(forbidden_import)) not in schema


def test_local_catalog_uses_behavior_ontology_iri():
    tree = ET.parse(ROOT / "catalog-v001.xml")
    entries = [(e.get("name"), e.get("uri")) for e in tree.findall("{urn:oasis:names:tc:entity:xmlns:xml:catalog}uri")]
    assert entries.count(("https://w3id.org/mass-ontology/behavior", "07-behavior/ship-behavior.ttl")) == 1
    assert len(set(k for k, _ in entries)) == len(entries)


def test_synthetic_fixture_valid_and_three_independent_dimensions():
    graph = graph_from_repo()
    assert fixture_errors(graph) == []
    units = list(graph.objects(EX.trajectory_001, BH.hasTemporalUnit))
    assert len(units) == 3
    for unit in units:
        types = {t for p in graph.objects(unit, BH.hasPhysicalBehavior)
                 for t in graph.objects(p, RDF.type)}
        assert {BH.PositionState, BH.SpeedState, BH.CourseState} <= types


def test_gap_is_allowed_but_not_claimed_meeting():
    graph = data_only()
    _, end_1 = interval_bounds(graph, EX.interval_001)
    start_2, _ = interval_bounds(graph, EX.interval_002)
    assert start_2 > end_1  # gap; no fabricated continuity
    assert (EX.unit_001, BH.nextTemporalUnit, EX.unit_002) in graph
    assert not list(graph.triples((None, TIME.intervalMeets, None)))
    assert not list(graph.triples((None, TIME.intervalBefore, None)))
    assert not list(graph.triples((None, TIME.intervalAfter, None)))


def test_fixture_no_metrics_or_prov_until_p04_03():
    graph = data_only()
    assert not any("qudt.org" in str(p) or "w3.org/ns/sosa" in str(p)
                   for _, p, _ in graph)
    assert not any("w3.org/ns/prov" in str(p) for _, p, _ in graph)


def test_p04_01_specialization_preserved():
    graph = graph_from_repo()
    assert MARITIME.Vessel in parents(graph, MASS.MASSVessel)
    assert MARITIME.Vessel in parents(graph, NAV.TargetShip)
    assert MASS.MASSVessel not in parents(graph, NAV.TargetShip)


@pytest.mark.parametrize("mutation,expected", [
    ("no_vessel", "one-explicit-vessel"),
    ("two_vessels", "one-explicit-vessel"),
    ("missing_extent", "invalid-temporal-extent"),
    ("bad_parent", "unit-parent-inconsistent"),
    ("overlap", "segment-overlap"),
    ("reversed", "invalid-temporal-extent"),
    ("duplicate_index", "segment-indices-not-contiguous"),
    ("false_next", "invalid-sequence-adjacency"),
])
def test_mutation_negative_fixtures(mutation, expected):
    graph = graph_from_repo()
    if mutation == "no_vessel":
        graph.remove((EX.trajectory_001, BH.ofVessel, EX.vessel_001))
    elif mutation == "two_vessels":
        graph.add((EX.vessel_002, RDF.type, MARITIME.Vessel))
        graph.add((EX.trajectory_001, BH.ofVessel, EX.vessel_002))
    elif mutation == "missing_extent":
        graph.remove((EX.unit_001, BH.hasTemporalExtent, EX.interval_001))
    elif mutation == "bad_parent":
        graph.remove((EX.unit_001, BH.partOfTrajectory, EX.trajectory_001))
    elif mutation == "overlap":
        graph.set((EX.begin_002, TIME.inXSDDateTimeStamp,
                   Literal("2026-10-28T12:01:30Z", datatype=XSD.dateTimeStamp)))
    elif mutation == "reversed":
        graph.set((EX.end_001, TIME.inXSDDateTimeStamp,
                   Literal("2026-10-28T11:59:00Z", datatype=XSD.dateTimeStamp)))
    elif mutation == "duplicate_index":
        graph.set((EX.unit_002, BH.segmentIndex, Literal(1, datatype=XSD.nonNegativeInteger)))
    elif mutation == "false_next":
        graph.remove((EX.unit_000, BH.nextTemporalUnit, EX.unit_001))
        graph.add((EX.unit_000, BH.nextTemporalUnit, EX.unit_002))
    assert expected in fixture_errors(graph)
