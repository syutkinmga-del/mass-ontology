"""P04-01 general-vessel integration and negative mutation checks.

Not a substitute for full BH-P04 validation (which starts in P04-04).
Only locally cataloged modules are parsed: no network ontology imports.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef

ROOT = Path(__file__).resolve().parents[1]
MARITIME = Namespace("https://w3id.org/mass-ontology/maritime#")
MASS = Namespace("https://w3id.org/mass-ontology/core#")
NAV = Namespace("https://w3id.org/mass-ontology/navigation#")
COMMON = Namespace("https://w3id.org/mass-ontology/common#")
EX = Namespace("https://w3id.org/mass-ontology/example#")

FILES = (
    "01-common/common-core.ttl",
    "02-maritime/maritime-core.ttl",
    "02-maritime/vessel-compatibility.ttl",
    "03-mass-core/mass-core.ttl",
    "04-navigation/navigation-situation.ttl",
    "examples/example-encounter-scenario.ttl",
)


def load_graph():
    graph = Graph()
    for relative in FILES:
        graph.parse(ROOT / relative, format="turtle")
    return graph


def superclasses(graph, cls):
    """Transitive RDFS subclass reachability, including the starting class."""
    seen, stack = set(), [cls]
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(graph.objects(current, RDFS.subClassOf))
    return seen


def asserted_or_subclass_type(graph, individual, cls):
    return any(cls in superclasses(graph, asserted)
               for asserted in graph.objects(individual, RDF.type))


def compatibility_violations(graph):
    """P04-01 invariant oracle, used by positive and mutation-negative tests."""
    errors = []
    if (MARITIME.Vessel, RDF.type, OWL.Class) not in graph:
        errors.append("missing-maritime-vessel-class")
    if COMMON.EngineeredSystem not in superclasses(graph, MARITIME.Vessel):
        errors.append("missing-local-upper-class")
    if MARITIME.Vessel not in superclasses(graph, MASS.MASSVessel):
        errors.append("mass-vessel-not-general-vessel")
    if MASS.MASSVessel in superclasses(graph, MARITIME.Vessel):
        errors.append("generic-vessel-implies-mass")
    if MARITIME.Vessel not in superclasses(graph, NAV.TargetShip):
        errors.append("target-not-general-vessel")
    if MASS.MASSVessel in superclasses(graph, NAV.TargetShip):
        errors.append("target-implies-mass")
    if MASS.MASSVessel not in superclasses(graph, NAV.OwnShip):
        errors.append("legacy-ownship-inheritance-lost")
    for cls in (MARITIME.Vessel, MASS.MASSVessel, NAV.TargetShip, NAV.OwnShip):
        if any((cls, OWL.equivalentClass, other) in graph or
               (other, OWL.equivalentClass, cls) in graph
               for other in (MARITIME.Vessel, MASS.MASSVessel, NAV.TargetShip, NAV.OwnShip)
               if other != cls):
            errors.append("unexpected-equivalence")
            break
    return errors


def test_ontology_identity_and_local_import_iris():
    graph = load_graph()
    a = URIRef("https://w3id.org/mass-ontology/maritime")
    b = URIRef("https://w3id.org/mass-ontology/maritime-compatibility")
    assert (a, RDF.type, OWL.Ontology) in graph
    assert (b, RDF.type, OWL.Ontology) in graph
    assert (a, OWL.imports, URIRef("https://w3id.org/mass-ontology/common")) in graph
    assert (b, OWL.imports, URIRef("https://w3id.org/mass-ontology/navigation")) in graph


def test_registry_has_local_maritime_mappings():
    tree = ET.parse(ROOT / "catalog-v001.xml")
    entries = {
        item.get("name"): item.get("uri")
        for item in tree.findall("{urn:oasis:names:tc:entity:xmlns:xml:catalog}uri")
    }
    assert entries["https://w3id.org/mass-ontology/maritime"] == "02-maritime/maritime-core.ttl"
    assert entries["https://w3id.org/mass-ontology/maritime-compatibility"] == "02-maritime/vessel-compatibility.ttl"
    for name, relative in entries.items():
        assert (ROOT / relative).is_file(), name


def test_general_vessel_classification_and_legacy_compatibility():
    assert compatibility_violations(load_graph()) == []


def test_existing_encounter_roles_reach_general_vessel():
    graph = load_graph()
    assert asserted_or_subclass_type(graph, EX.own_ship_001, MARITIME.Vessel)
    assert asserted_or_subclass_type(graph, EX.target_ship_001, MARITIME.Vessel)
    assert asserted_or_subclass_type(graph, EX.own_ship_001, MASS.MASSVessel)
    assert not asserted_or_subclass_type(graph, EX.target_ship_001, MASS.MASSVessel)


def test_no_prohibited_equivalences_or_disjointness_in_new_modules():
    graph = Graph()
    for file in ("02-maritime/maritime-core.ttl", "02-maritime/vessel-compatibility.ttl"):
        graph.parse(ROOT / file, format="turtle")
    assert not list(graph.triples((None, OWL.equivalentClass, None)))
    assert not list(graph.triples((None, OWL.disjointWith, None)))
    assert not list(graph.triples((None, OWL.sameAs, None)))


@pytest.mark.parametrize("bad_subject,bad_parent,expected", [
    (NAV.TargetShip, MASS.MASSVessel, "target-implies-mass"),
    (MARITIME.Vessel, MASS.MASSVessel, "generic-vessel-implies-mass"),
])
def test_mutation_negative_unwanted_mass_specialization(bad_subject, bad_parent, expected):
    graph = load_graph()
    graph.add((bad_subject, RDFS.subClassOf, bad_parent))
    assert expected in compatibility_violations(graph)


def test_mutation_negative_missing_target_bridge():
    graph = load_graph()
    graph.remove((NAV.TargetShip, RDFS.subClassOf, MARITIME.Vessel))
    assert "target-not-general-vessel" in compatibility_violations(graph)
