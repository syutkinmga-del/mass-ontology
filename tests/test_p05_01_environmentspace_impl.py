"""P05-01 EnvironmentSpace implementation: D05 *local* OWL/SHACL fixtures.

This is NOT full BH-P05, GeoSPARQL function conformance, ODD applicability,
COLREG, R10 approval or P05-D04/D08 external evidence.
"""
from __future__ import annotations
from copy import deepcopy
import importlib.util
from pathlib import Path

import pytest
from rdflib import Graph, Literal, RDF, RDFS, OWL, XSD, URIRef

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location(
    "environmentspace_p05", ROOT/"scripts/validate_p05_01_environmentspace.py"
)
gate=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


@pytest.fixture(scope="module")
def schema():
    return gate.load_graph(ROOT, gate.SCHEMA)


@pytest.fixture(scope="module")
def shapes():
    return gate.load_graph(ROOT, gate.SHAPES)


def clone(g: Graph) -> Graph:
    new=Graph()
    for triple in g:
        new.add(triple)
    return new


def test_approved_d05_ontology_is_production_module_without_unsafe_imports(schema):
    assert gate.schema_issues(schema,ROOT)==[]
    assert (gate.BH.EnvironmentSpace, RDFS.subClassOf, gate.GEO.Feature) in schema
    assert (gate.BH.EnvironmentSpace, OWL.disjointWith, gate.GEO.Geometry) in schema
    assert (gate.BH.referencesVessel,RDFS.range,gate.MARITIME.Vessel) in schema
    assert (gate.BH.referencesSpace,RDFS.range,gate.BH.EnvironmentSpace) in schema
    assert set(schema.objects(gate.OGC_ONT,OWL.imports)) == gate.LOCAL_OWL_IMPORTS


def test_positive_has_one_feature_and_two_versioned_distinct_geometry_records(schema,shapes):
    result=gate.validate_fixture(ROOT,gate.POSITIVE,schema,shapes)
    assert result["overall_pass"],result
    g=gate.load_graph(ROOT,gate.POSITIVE)
    features=list(g.subjects(RDF.type,gate.BH.EnvironmentSpace))
    assert len(features)==1
    feature=features[0]
    geoms=list(g.objects(feature,gate.GEO.hasGeometry))
    assert len(geoms)==2 and len(set(geoms))==2
    assert feature not in geoms
    assert all((geom,RDF.type,gate.GEO.Geometry) in g for geom in geoms)
    editions={str(list(g.objects(geom,gate.BH.geometryEditionId))[0])
              for geom in geoms}
    assert editions=={"synthetic-edition-A","synthetic-edition-B"}
    assert not list(g.triples((None,gate.NAV.appliesCOLREGRule,None)))


@pytest.mark.parametrize("filename,expected", list(gate.INVALID.items()))
def test_negative_synthetic_fixture_fails_by_designated_d05_rule(
    filename,expected,schema,shapes
):
    result=gate.validate_fixture(
        ROOT,"tests/spatial/fixtures/invalid/"+filename,schema,shapes)
    assert result["overall_pass"] is False,(filename,result)
    assert any(x.startswith(expected) for x in result["curated_issues"]), (
        "Fixture negative oracle did not reject its intended D05 rule",
        filename,expected,result,
    )


@pytest.mark.parametrize("bad_change",[
    "unsafe_feature_geometry_equivalence",
    "replace_feature_with_geometry",
    "remove_subclass",
    "missing_edition_metadata_property",
    "wrong_vessel_reference_type",
    "external_geosparql_import",
    "operational_colreg_subclass",
    "property_chain_for_derived_colreg",
])
def test_ontology_negative_mutations_fail_closed(schema,bad_change):
    s=clone(schema)
    if bad_change=="unsafe_feature_geometry_equivalence":
        s.add((gate.BH.EnvironmentSpace,OWL.equivalentClass,gate.GEO.Geometry))
    elif bad_change=="replace_feature_with_geometry":
        s.remove((gate.BH.EnvironmentSpace,RDFS.subClassOf,gate.GEO.Feature))
        s.add((gate.BH.EnvironmentSpace,RDFS.subClassOf,gate.GEO.Geometry))
    elif bad_change=="remove_subclass":
        s.remove((gate.BH.EnvironmentSpace,RDFS.subClassOf,gate.GEO.Feature))
    elif bad_change=="missing_edition_metadata_property":
        s.remove((gate.BH.geometryEditionId,RDF.type,OWL.DatatypeProperty))
    elif bad_change=="wrong_vessel_reference_type":
        s.remove((gate.BH.referencesVessel,RDFS.range,gate.MARITIME.Vessel))
        s.add((gate.BH.referencesVessel,RDFS.range,gate.BH.EnvironmentSpace))
    elif bad_change=="external_geosparql_import":
        s.add((gate.OGC_ONT,OWL.imports,
               URIRef("http://www.opengis.net/ont/geosparql")))
    elif bad_change=="operational_colreg_subclass":
        s.add((gate.BH.EnvironmentSpace,RDFS.subClassOf,gate.NAV.COLREGSituation))
    elif bad_change=="property_chain_for_derived_colreg":
        s.add((gate.BH.referencesSpace,OWL.propertyChainAxiom,
               URIRef("https://w3id.org/mass-ontology/p05-01/invalid-rule")))
    else:
        raise AssertionError(bad_change)
    assert gate.schema_issues(s,ROOT),(
        "Unsafe D05 schema mutation evaded independent design acceptance: ",
        bad_change,
    )


def test_shacl_validation_alone_is_not_full_version_or_colreg_oracle(schema,shapes):
    dup=gate.validate_fixture(
        ROOT,"tests/spatial/fixtures/invalid/n07-duplicate-edition.ttl",
        schema,shapes)
    forbidden=gate.validate_fixture(
        ROOT,"tests/spatial/fixtures/invalid/n08-unsupported-colreg.ttl",
        schema,shapes)
    # Independently checked curated-data oracle is required regardless of
    # how a particular RDF/SHACL engine handles entailment.
    assert any("duplicate geometry edition" in x for x in dup["curated_issues"])
    assert any("D05-B04" in x for x in forbidden["curated_issues"])


def test_released_p04_source_and_unresolved_p05_gates_not_included(schema):
    approval=__import__("json").loads((ROOT/gate.APPROVAL).read_text(encoding="utf-8"))
    assert approval["decision_status"]=="CLOSED_APPROVED_ALTERNATIVE_B"
    assert not approval["geo_rdf_owl_import_approved"]
    assert approval["open_adrs"] == ["P05-D04","P05-D06","P05-D07","P05-D08","P05-D09"]
    assert not approval["v050_release_authorized"]
    assert (gate.BH.SemanticBehavior,RDF.type,OWL.Class) not in schema
    assert (gate.BH.InteractionBehavior,RDF.type,OWL.Class) not in schema
