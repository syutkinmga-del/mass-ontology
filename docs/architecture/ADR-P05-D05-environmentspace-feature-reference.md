# ADR-P05-D05 — EnvironmentSpace / GeoSPARQL Feature / Vessel as Reference (P05-01)

**ADR status:** PROPOSED_FOR_OWNER_DESIGN_DECISION; **P05-D05 remains OPEN**.  
**Stage:** P05-01 (v0.5.0 / BH-P05), design and analysis **only**.  
**Date:** 2026-11-09.  
**Branch baseline:** `b43b9423cc24075bc67010d5b04f47f58161260f` (approved P05-00 registration).  
**Approval required:** separate explicit owner decision before production `bh:EnvironmentSpace` TTL or asserted `rdfs:subClassOf geo:Feature` is committed.  
**No new release/tag/permission:** `v0.4.0` remains immutable; BH-P05 functional gates DEFERRED.

## A. Architectural question

How should a maritime spatial zone / environmental feature (`bh:EnvironmentSpace`) be identified and represented in GeoSPARQL, without turning its geometry, source dataset, route, ODD/OE specification or a nearby vessel into that same object? Which relation role should link a time-qualified `InteractionBehavior` to another vessel?

**Normative / prior decisions:** DCCR-01 C08–C13 (C13 says not ODD/OE), DCCR-02-D04 (time-qualified information description and proposed vessel reference extension), DCCR-03 C13 + R05 (candidate feature subclass, not an approved import), DCCR-04 BH-V07 / BH-CQ-04 (subject/reference/time/provenance), P05-00 design approval DEC-P05-00-2026-11-09-01 (P05-D05 specifically OPEN and blocking production TTL).

**External source:** OGC GeoSPARQL 1.1, OGC 22-047r1, [§8.2.2 Feature](https://docs.ogc.org/is/22-047r1/22-047r1.html#_class_geofeature), [§8.4.1 hasGeometry](https://docs.ogc.org/is/22-047r1/22-047r1.html#_property_geohasgeometry), [§10.6.1 Geometry](https://docs.ogc.org/is/22-047r1/22-047r1.html#_class_geogeometry). The standard specifies `geo:Feature rdfs:subClassOf geo:SpatialObject`, `geo:Feature owl:disjointWith geo:Geometry`; `geo:hasGeometry` ranges over geometry representations and a feature may have multiple. `geo:hasDefaultGeometry` is not globally functionally/cardinality constrained and can lead to inconsistent query interpretations if different defaults coexist. These are standards claims; the **local modeling choices below are MASS proposals**, not OGC requirements.

## B. Alternatives and decision analysis

| Alternative | Pattern | Benefit | Problem / decision |
|---|---|---|---|
| A | `bh:EnvironmentSpace rdfs:subClassOf geo:Geometry` | Direct access to WKT | **REJECT**: conflates a spatially referenced feature with its representation, conflicts with GeoSPARQL Feature–Geometry disjointness if also typed as Feature; invalidates change/version separation |
| B | `bh:EnvironmentSpace rdfs:subClassOf geo:Feature`, `geo:hasGeometry` → `geo:Geometry` | Native reuse; separate identity, extent, metadata; interoperable GeoSPARQL | **RECOMMENDED FOR APPROVAL** with local scope and identity/validity constraints, not yet an actual axiom |
| C | `bh:EnvironmentSpace owl:equivalentClass geo:Feature` | Apparently simple | **REJECT**: implies every geospatial feature is an EnvironmentSpace; wrongly expands domain |
| D | `bh:EnvironmentSpace` as `ODD` / `OperationalEnvelope` / `nav:EncounterSituation` | Convenience for operations | **REJECT**: normative operational limits and encounters are descriptions/situations, not the geographic feature represented |
| E | `bh:EnvironmentSpace rdfs:subClassOf geo:SpatialObject` only | Weak compatibility without Feature commitment | **FALLBACK** if a demonstrable disjointness/category conflict emerges under imported ontology, with explicit re-review; insufficient feature typing for intended pilot |

**Proposed D05 disposition:** select B as the **recommended implementation design**, subject to owner approval and independent OGC artifact/engine review (P05-D04). No `owl:equivalentClass`, `owl:sameAs` (feature–geometry, zone–ODD), upper BFO/CCO equivalence, automatic COLREG classification or changed P04 triples. The term `EnvironmentSpace` denotes the stable *domain reference feature or delineated geographic/environmental zone* in the application universe of discourse; it is not a universal ontological category for all physical 3D space or arbitrary map geometry.

## C. Identity policy

- **Same feature, changing geometry:** a durable identity (e.g. `ex:approachZone`) can have revisions (`ex:approachZone-geom-chartA-2026`, `ex:approachZone-geom-chartB-2027`). The geometry revision is separately identified by source, chart edition, CRS, validity interval and precision.
- **Feature identity is not location equality:** two different buoy areas, zones or named areas can have identical polygon coordinates without becoming `owl:sameAs`. Conversely, one named area can change its outline without becoming a new object (subject to explicit identifier authority/edition rules).
- **Kinds of feature:** a reference can be an anchored spatial feature, a dynamic/environmental area (e.g. weather region), or a human-delimited feature from a chart; do not assume a source polygon describes an unchanging physical object. An invented research zone is not a legally defined chart, prohibited area or ODD limit.
- **Identity ownership:** a specific issuer/dataset/authority and feature ID; a local synthetic fixture uses `ex:` IRIs. No external real-world maritime area is asserted without reviewed source identity, license, version and provenance.
- **Multiple geometries:** `geo:hasGeometry` may point to multiple versioned geometry individuals. **No unconditional `geo:hasDefaultGeometry` in v0.5 pilot**; a chosen geometry must be selected explicitly by edition + valid time + pipeline method. If default geometries are added, their scope/uniqueness must be enforced by closed-world validation, not assumed from GeoSPARQL OWL.
- **Open temporal detail P05-D08:** representing geometry valid-time/transaction-time, source edition, synchronization and distance/bearing computation needs a separate design decision. The current ADR is only an identity and reference-role decision, not a distance algorithm.

## D. Reference-vessel role — separate from EnvironmentSpace

**DCCR-02-D04** proposes vessel–environment interaction as the source core, and *potentially* an additional vessel–vessel extension. MASS shall not turn `maritime:Vessel` or `nav:TargetShip` into an `EnvironmentSpace` merely to reuse `bh:referencesSpace`.

**Recommended locally scoped relation contracts for later P05-03 (not declared here):**

| Role | Subject | Object | Rule |
|---|---|---|---|
| `bh:hasSubjectVessel` | `bh:InteractionBehavior` | `maritime:Vessel` | Exactly one in a curated relation record |
| `bh:referencesSpace` | `bh:InteractionBehavior` | `bh:EnvironmentSpace` | Environmental-reference alternative |
| `bh:referencesVessel` **(proposed new local role)** | `bh:InteractionBehavior` | `maritime:Vessel` | Vessel-reference alternative; may be same real-world vessel as `nav:TargetShip` in an independently established encounter, **without asserting equivalence of classes** |
| `bh:appliesToTemporalUnit` | `bh:InteractionBehavior` | `bh:TemporalUnit` | Temporal segment information record, not time interval literal |
| `prov:wasDerivedFrom` and linked `prov:Activity` | derived description | observation + chart/source geometries | Source/provenance and method must be traceable |

**Curated-data XOR shape proposal:** exactly one **reference role** (`referencesSpace` OR `referencesVessel`), exactly one reference object, exactly one subject vessel, `subject ≠ referenceVessel`, exactly one TemporalUnit and valid source lineage. If a compound vessel+zone relationship is needed, represent **two separate relation description records** with their own roles rather than putting both references into one record. Do not enforce domain/range through `owl:unionOf` in P05-01.

An ordinary `maritime:Vessel` could *independently* be spatially described by a separate GeoSPARQL Feature/snapshot interface in P05-02/03; **no global axiom `maritime:Vessel rdfs:subClassOf geo:Feature` is authorized** here. If a temporary position feature is used, its URI and event time distinguish it from the persistent vessel. Its `geo:Geometry` must be observation-derived rather than a permanent vessel location.

**No safety inference:** a `referencesVessel` link alone is not an encounter, collision risk, COLREGRule or crossing classification; `nav:hasCPA` does not define instantaneous DistanceRelation.

## E. Illustrative RDF pattern — **NOT production Turtle**

This is an **example only**, located in Markdown to avoid being loaded by the existing ontology catalog or CI. It makes no import or automatic spatial computation claim.

```turtle
@prefix bh:   <https://w3id.org/mass-ontology/behavior#> .
@prefix geo:  <http://www.opengis.net/ont/geosparql#> .
@prefix ex:   <https://w3id.org/mass-ontology/examples/p05-01#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

# The subclass statement is the RECOMMENDED AXIOM, NOT YET APPROVED:
# bh:EnvironmentSpace rdfs:subClassOf geo:Feature .

# A hypothetical, explicitly synthetic research area:
ex:syntheticApproachArea a bh:EnvironmentSpace ;
    geo:hasGeometry ex:syntheticApproachArea-geometry-chartA .

ex:syntheticApproachArea-geometry-chartA a geo:Geometry ;
    geo:asWKT "<http://www.opengis.net/def/crs/OGC/1.3/CRS84> POLYGON((12.30 54.35, 12.40 54.35, 12.40 54.45, 12.30 54.45, 12.30 54.35))"^^geo:wktLiteral ;
    prov:wasDerivedFrom ex:syntheticChartRevisionA .

# A different edition/geometry may later represent the SAME area feature,
# without changing its IRI, geometry individual identity or origin records.
```

**Important:** `ex:syntheticChartRevisionA` must be registered as a source entity in an eventual fixture; it is a placeholder here. No WKT lexical or polygon-topology result is counted as a runtime conformance test by this ADR.

## F. Prospective P05-01 design oracles (not BH-P05 runtime PASS)

| ID | Positive expectation | Negative mutant / failure | Future gate |
|---|---|---|---|
| D05-T01 | `EnvironmentSpace` as distinct `geo:Feature` specialization, `geo:Geometry` different resource | feature same URI as geometry or class `owl:equivalentClass geo:Geometry` | SHACL + OWL consistency, P05-02 |
| D05-T02 | Same stable area feature with two attributable geometry editions | a new geometry silently overwrites earlier source bytes or declares `owl:sameAs` | provenance/graph checks, P05-02 |
| D05-T03 | Synthetic area with explicit CRS84 WKT (lon lat) | missing/ambiguous source CRS; EPSG:4326 axis transposition | geometry lexical + engine, P05-02 |
| D05-T04 | Environmental-reference relation has only `referencesSpace`, one subject, valid TemporalUnit, source evidence | `referencesSpace` points to a vessel or ODD/OE; missing reference | BH-V07, P05-03 |
| D05-T05 | Vessel-reference relation has only `referencesVessel`, another `maritime:Vessel` as object | both reference roles, self-reference or vessel misclassified as space | BH-V07, P05-03 |
| D05-T06 | Distinct feature identity and geometry selected from source/valid-time context | two conflicting unqualified default geometries; absent chart edition | closed-world context, P05-02 |
| D05-T07 | No COLREG, ODD applicability, risk or maneuver conclusion derived solely from topology/reference | rule mutant infers `nav:Crossing`, `nav:COLREGRule` or `mass:OperationalMode` | BH-V10, P05-06 |

**P05-01 acceptance of *this design artifact*:** a static ADR checker validates decision scope and traceability; P04 regression remains green; owner explicitly selects a specific D05 disposition and records any amendments in a **separate** governance record. Only after that may a following PR implement a narrow production `EnvironmentSpace` OWL module, and still without unapproved GeoSPARQL RDF imports. P05-D04, P05-D06…D09 remain independent OPEN tasks.

## G. Formal decision pending

**Proposed text for a separate owner decision:**

> Approve P05-D05, Alternative B, for the P05-01 implementation: model `bh:EnvironmentSpace` as a scoped subclass of `geo:Feature`, keep `geo:Geometry` and geometry editions distinct, do not equate EnvironmentSpace with ODD/OE or another vessel, and reserve a separate `bh:referencesVessel` role with XOR reference validation. Do not authorize unreviewed GeoSPARQL RDF imports, automated COLREG inference or v0.5.0 release. All remaining P05-D04/D06…D09 stay open.

This is **proposed**, not a statement already made or approved by the owner. Until a separate decision is received, the approval state is `PENDING_OWNER_DECISION` and the production `EnvironmentSpace` TTL gate stays **BLOCKED**.

## H. References and evidence

- Internal DCCR-01 C08–C13/R04–R05; DCCR-02-D04; DCCR-03 C13/R05; DCCR-04 BH-V07 / BH-CQ-04; P05-00 contract and [owner-directed approval](../governance/DEC-P05-00-2026-11-09-design-approval.md).
- External OGC GeoSPARQL 1.1: https://docs.ogc.org/is/22-047r1/22-047r1.html , clauses 8.2.2, 8.4.1–8.4.2, 10.6.1. This normative text was reviewed to derive feature/geometry distinctions; its publisher RDF ontology was **not** vendored, licensed, hashed or imported.
