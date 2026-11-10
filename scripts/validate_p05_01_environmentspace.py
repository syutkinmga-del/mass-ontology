#!/usr/bin/env python3
"""D05-authorized, *local* P05-01 OWL/SHACL and synthetic fixture validation.

Checks a real EnvironmentSpace production module but deliberately does NOT
claim the complete BH-P05 profile, GeoSPARQL function conformance, actual
geometry topology, AIS tracking accuracy or COLREG compliance. No RDF network
requests or publisher ontology imports are made.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD, URIRef
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "07-behavior/environment-space-p05.ttl"
SHAPES = "shapes/environment-space-p05.shacl.ttl"
POSITIVE = "tests/spatial/fixtures/p05-01-environmentspace-valid.ttl"
CATALOG = "catalog-v001.xml"
APPROVAL = "docs/standards/P05-D05-owner-approval.json"
BH = Namespace("https://w3id.org/mass-ontology/behavior#")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
MARITIME = Namespace("https://w3id.org/mass-ontology/maritime#")
NAV = Namespace("https://w3id.org/mass-ontology/navigation#")
PROV = Namespace("http://www.w3.org/ns/prov#")
MASS = Namespace("https://w3id.org/mass-ontology/core#")
OGC_ONT = URIRef("https://w3id.org/mass-ontology/environment-space")
LOCAL_OWL_IMPORTS = {
    URIRef("https://w3id.org/mass-ontology/behavior"),
    URIRef("https://w3id.org/mass-ontology/maritime"),
}
BAD_ENTAILMENTS = {
    NAV.COLREGSituation, NAV.COLREGRule, NAV.CrossingSituation,
    NAV.EncounterSituation, MASS.OperationalMode,
}
BAD_PREDICATES = {
    NAV.appliesCOLREGRule, NAV.requiresManeuver, NAV.hasCPA, NAV.hasTCPA,
    MASS.hasOperationalMode,
}
INVALID = {
    "n01-feature-also-geometry.ttl": "D05-B01",
    "n02-missing-geometry-edition.ttl": "D05-B02",
    "n03-missing-provenance-source.ttl": "D05-B02",
    "n04-invalid-wkt-datatype.ttl": "D05-B02",
    "n05-unqualified-default-geometry.ttl": "D05-B02",
    "n06-untyped-geometry.ttl": "D05-B02",
    "n07-duplicate-edition.ttl": "D05-B02",
    "n08-unsupported-colreg.ttl": "D05-B04",
}


def load_graph(root: Path, rel: str) -> Graph:
    p = root / rel
    if not p.is_file():
        raise FileNotFoundError(rel)
    return Graph().parse(p, format="turtle")


def schema_issues(schema: Graph, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    def issue(ok: bool, msg: str) -> None:
        if not ok:
            errors.append(msg)
    issue((OGC_ONT, RDF.type, OWL.Ontology) in schema, "D05-SCHEMA: ontology IRI absent")
    imports = set(schema.objects(OGC_ONT, OWL.imports))
    issue(imports == LOCAL_OWL_IMPORTS, "D05-D04: unexpected or external owl:imports")
    issue(not any(str(s).startswith("http://www.opengis.net") for s in
                  schema.subjects(OWL.imports, None)),
          "D05-D04: external ontology must not be imported")
    issue((BH.EnvironmentSpace, RDF.type, OWL.Class) in schema
          and (BH.EnvironmentSpace, RDFS.subClassOf, GEO.Feature) in schema,
          "D05-B01: EnvironmentSpace must be a geo:Feature subclass")
    issue((BH.EnvironmentSpace, OWL.disjointWith, GEO.Geometry) in schema,
          "D05-B01: EnvironmentSpace must remain separate from geo:Geometry")
    issue(not list(schema.triples((None, OWL.equivalentClass, None)))
          and not list(schema.triples((None, OWL.sameAs, None)))
          and not list(schema.triples((None, OWL.propertyChainAxiom, None))),
          "D05-B01/D05-B04: unsafe equivalence, identity or property-chain axiom")
    issue((MARITIME.Vessel, RDFS.subClassOf, GEO.Feature) not in schema
          and (MARITIME.Vessel, RDFS.subClassOf, BH.EnvironmentSpace) not in schema,
          "D05-B03: vessel incorrectly typed as geospatial feature/space")
    issue((BH.geometryEditionId, RDF.type, OWL.DatatypeProperty) in schema
          and (BH.geometryEditionId, RDFS.domain, GEO.Geometry) in schema
          and (BH.geometryEditionId, RDFS.range, XSD.string) in schema,
          "D05-B02: edition record datatype property absent")
    for pred, expected_range in (
        (BH.referencesVessel, MARITIME.Vessel),
        (BH.referencesSpace, BH.EnvironmentSpace),
    ):
        issue((pred, RDF.type, OWL.ObjectProperty) in schema
              and (pred, RDFS.range, expected_range) in schema,
              "D05-B03: independent reference role absent or mis-typed: " + str(pred))
    issue(BH.referencesSpace != BH.referencesVessel
          and not any((BH.referencesVessel, pred, BH.referencesSpace) in schema
                      for pred in (OWL.equivalentProperty, RDFS.subPropertyOf)),
          "D05-B03: vessel and space reference roles conflated")
    issue(not any(object_ in BAD_ENTAILMENTS
                  for subject, pred, object_ in schema
                  if pred in (RDFS.subClassOf, RDFS.range, RDFS.domain)),
          "D05-B04: ontology automatically injects a COLREG or operational classification")
    issue(not any(pred in BAD_PREDICATES for _, pred, _ in schema),
          "D05-B04: unexpected COLREG/MASS operational rule property in local OWL")
    namespace = "{urn:oasis:names:tc:entity:xmlns:xml:catalog}"
    catalog = ET.parse(root / CATALOG).getroot()
    entries = [(e.attrib.get("name"),e.attrib.get("uri"))
               for e in catalog.findall(namespace + "uri")]
    issue(entries.count((str(OGC_ONT), SCHEMA)) == 1,
          "D05-CATALOG: local EnvironmentSpace OWL not mapped exactly once")
    if (root / APPROVAL).is_file():
        approval=json.loads((root / APPROVAL).read_text(encoding="utf-8"))
        issue(approval.get("decision_status") == "CLOSED_APPROVED_ALTERNATIVE_B"
              and approval.get("approved_source_commit_sha") ==
                  "c4e9e7537b625dc5582b9505af232a959309c622"
              and approval.get("geo_rdf_owl_import_approved") is False
              and approval.get("v050_release_authorized") is False,
              "D05-GOVERNANCE: approved source/rights/release boundary mismatch")
        issue(approval.get("open_adrs") ==
              ["P05-D04","P05-D06","P05-D07","P05-D08","P05-D09"],
              "D05-GOVERNANCE: other ADRs cannot be closed by local implementation")
    else:
        errors.append("D05-GOVERNANCE: missing approved decision")
    return errors


def fixture_issues(data: Graph) -> list[str]:
    """Closed-world curated-data oracle; no spatial math/CRS parser."""
    errors: list[str] = []
    features = set(data.subjects(RDF.type, BH.EnvironmentSpace))
    if not features:
        return ["D05-B01: no explicitly typed EnvironmentSpace in fixture"]
    for feature in sorted(features, key=str):
        if not isinstance(feature, URIRef):
            errors.append("D05-B01: feature must have independent IRI")
        if (feature, RDF.type, GEO.Geometry) in data or \
                (feature, RDF.type, MARITIME.Vessel) in data:
            errors.append("D05-B01: geographic feature equals Geometry/Vessel type")
        if list(data.objects(feature, GEO.hasDefaultGeometry)):
            errors.append("D05-B02: unqualified default geometry not allowed")
        if list(data.objects(feature, OWL.sameAs)):
            errors.append("D05-B01: feature equivalence to geometry not allowed")
        geoms = list(data.objects(feature, GEO.hasGeometry))
        if not geoms:
            errors.append("D05-B02: feature has no geometry representation")
        edition_ids = set()
        for geom in geoms:
            if not isinstance(geom, URIRef) or geom == feature:
                errors.append("D05-B02: geometry must have distinct IRI")
            if (geom, RDF.type, GEO.Geometry) not in data or \
                    (geom, RDF.type, BH.EnvironmentSpace) in data:
                errors.append("D05-B02: geometry missing explicit separate class")
            ed = list(data.objects(geom, BH.geometryEditionId))
            if len(ed) != 1 or not isinstance(ed[0], Literal) or \
                    ed[0].datatype != XSD.string or not str(ed[0]).strip():
                errors.append("D05-B02: missing/invalid edition identifier")
            elif str(ed[0]) in edition_ids:
                errors.append("D05-B02: duplicate geometry edition within same feature")
            else:
                edition_ids.add(str(ed[0]))
            wkt = list(data.objects(geom, GEO.asWKT))
            if len(wkt) != 1 or not isinstance(wkt[0], Literal) or \
                    wkt[0].datatype != GEO.wktLiteral:
                errors.append("D05-B02: explicit typed WKT missing or invalid datatype")
            sources = list(data.objects(geom, PROV.wasDerivedFrom))
            if len(sources) != 1 or not isinstance(sources[0], URIRef) or \
                    (sources[0], RDF.type, PROV.Entity) not in data:
                errors.append("D05-B02: one explicitly typed provenance source required")
        for pred in BAD_PREDICATES:
            if list(data.objects(feature, pred)):
                errors.append("D05-B04: forbidden operational or COLREG assertion on space")
        if any((feature, RDF.type, cls) in data for cls in BAD_ENTAILMENTS):
            errors.append("D05-B04: forbidden operational classification of space")
    return errors


def validate_fixture(root: Path, fixture: str, schema: Graph | None = None,
                     shapes: Graph | None = None) -> dict:
    schema = schema if schema is not None else load_graph(root, SCHEMA)
    shapes = shapes if shapes is not None else load_graph(root, SHAPES)
    data = load_graph(root, fixture)
    # pySHACL uses only local file graphs; no owl:imports are followed.
    conforms, report, report_text = validate(
        data_graph=data, shacl_graph=shapes, ont_graph=schema,
        inference="rdfs", abort_on_first=False, allow_infos=False,
        allow_warnings=False, advanced=False, meta_shacl=False,
    )
    curated = fixture_issues(data)  # Explicit typing, not inferred typing.
    return {
        "fixture": fixture,
        "shacl_conforms": bool(conforms),
        "curated_issues": curated,
        "overall_pass": bool(conforms) and not curated,
        "shacl_report": report_text if not conforms else "",
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=ROOT)
    p.add_argument("--report", type=Path,
                   default=Path("run/p05-01/environmentspace-validation.json"))
    args = p.parse_args()
    root=args.repo.resolve()
    report=(root / args.report).resolve()
    if not report.is_relative_to(root):
        p.error("Report must be stored inside repo")
    errors=[]
    checks={}
    try:
        schema=load_graph(root, SCHEMA)
        shapes=load_graph(root, SHAPES)
        errors.extend(schema_issues(schema,root))
        positive=validate_fixture(root,POSITIVE,schema,shapes)
        checks["positive"] = {k:v for k,v in positive.items() if k!="shacl_report"}
        if not positive["overall_pass"]:
            errors.append("D05-POSITIVE: valid synthetic feature/geometry graph rejected")
        checks["negative"]=[]
        for name,expected in INVALID.items():
            check=validate_fixture(
                root,"tests/spatial/fixtures/invalid/"+name,schema,shapes)
            matched=not check["overall_pass"] and (
                any(e.startswith(expected) for e in check["curated_issues"])
                or (expected=="D05-B02" and not check["shacl_conforms"])
            )
            checks["negative"].append({
                "case":name,"expected":expected,"rejected":not check["overall_pass"],
                "expected_rule_found":bool(matched),
            })
            if not matched:
                errors.append("D05-NEGATIVE: expected mutation not rejected by correct rule: "+name)
    except (OSError,ValueError,TypeError,ET.ParseError) as exc:
        errors.append(type(exc).__name__+": "+str(exc))
    evidence={
        "schema_version":"P05-01-environmentspace-local-owl-shacl-v1",
        "executed_at_utc":datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "profile":"P05-01-D05-LOCAL",
        "status":"PASS" if not errors else "FAIL",
        "errors":errors,
        "checks":checks,
        "d05_owl_shacl_fixture_scope":True,
        "geosparql_publisher_rdf_imported":False,
        "geosparql_function_conformance":"NOT_TESTED",
        "spatial_geometry_validity_and_crs_math":"NOT_TESTED",
        "full_BH_P05_acceptance":"DEFERRED_NOT_EXECUTED",
        "v050_release_authorized":False,
    }
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(evidence,indent=2,ensure_ascii=False),flush=True)
    return 0 if not errors else 2


if __name__=="__main__":
    raise SystemExit(main())
