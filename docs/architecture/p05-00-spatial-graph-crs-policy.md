# P05-00 — Spatial / CRS / RDF Named-Graph Data Contract (DRAFT)

**Date:** 2026-11-09  
**Status:** PROPOSED; not a production data pipeline, approved external import or claim of executed GeoSPARQL conformance.  
**Authority inputs:** Roadmap v1.1, DCCR-01 C08–C13, DCCR-02 D04/D05 and interval semantics, DCCR-03 external-alignment design, DCCR-04 BH-V04/V07/V08/V09/V10, approved P04-00 time policy.  
**Related review:** [P05-00 design baseline](../reviews/P05-00-design-baseline.md).

## A. GeoSPARQL geometry representation and CRS contract

**Candidate standard:** OGC GeoSPARQL **1.1**, OGC 22-047r1, https://docs.ogc.org/is/22-047r1/22-047r1.html. The official GeoSPARQL standards page lists this as a published standard; GeoSPARQL Next is **not** an automatically approved replacement. The exact RDF ontology artifact, version metadata, license and SHA-256 are **NOT PINNED** at P05-00. Do not use `owl:imports` or claim function support until P05-02's evidence review.

**Default modelling policy (design proposal):**
- A vessel `maritime:Vessel` is a material maritime subject, not itself a `geo:Geometry`. A position observation yields an **observation-specific geometry record** or snapshot with `sosa`/`prov` source and event time. A continuously moving vessel must not be given one permanent point with uncontrolled temporal semantics.
- An environmental zone is a persistent/revisable identified feature `bh:EnvironmentSpace`, **not** its polygon representation. `geo:hasGeometry` links a feature to `geo:Geometry`; `geo:asWKT` describes that representation; `geo:Feature` as a superclass of `EnvironmentSpace` is a candidate design decision for P05-01.
- The example profile uses explicit **OGC CRS84** `<http://www.opengis.net/def/crs/OGC/1.3/CRS84>` for WKT, with tuple order **longitude latitude** in decimal degrees; `POINT(12.35 54.40)` means longitude 12.35°, latitude 54.40°. In GeoSPARQL 1.1 the CRS84 IRI is the default for WKT with no prefix, but the pilot **SHOULD explicitly prefix** each WKT literal with the CRS IRI so the assumption is auditable.
- Do **not** silently treat EPSG:4326 WKT coordinates as CRS84 tuple order; coordinate axis order follows the referenced CRS. Any reprojection, unit conversion, precision or axis reordering must be an explicit `prov:Activity` with algorithm/version and input/output geometry records.
- WKT literals use `geo:wktLiteral` and a checked lexical grammar. Do not encode marine bearings/courses as geometric coordinate axes. COG, heading, true bearing, magnetic bearing and relative bearing are different quantities and frames.
- Spatial `sfWithin`, `sfIntersects` etc. and `geof:` calculations have their official GeoSPARQL meaning; a local contextualized `TopologyRelation` instance is **evidence about** such a relation, not the topological predicate itself.
- Distance between observed points must state computation method (e.g. geodesic vs planar), input CRS/geometry, output unit, timestamps, precision and source observations. No fixed distance threshold or closeness criterion is approved here. `unit:N-Mile`/nautical-mile compatibility and conversion are to be reviewed against pinned QUDT 3.5.3. **Actual current separation ≠ CPA/DCPA/TCPA predictions.**

Example *illustration only*, **not** a new ontology or accepted fixture:

```turtle
@prefix ex: <https://w3id.org/mass-ontology/examples/p05#> .
@prefix bh: <https://w3id.org/mass-ontology/behavior#> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .

ex:approachZone a bh:EnvironmentSpace ;
  geo:hasGeometry ex:approachZoneGeom .

ex:approachZoneGeom a geo:Geometry ;
  geo:asWKT "<http://www.opengis.net/def/crs/OGC/1.3/CRS84> POLYGON((12.30 54.35, 12.40 54.35, 12.40 54.45, 12.30 54.45, 12.30 54.35))"^^geo:wktLiteral .
```

Geometry example is deliberately synthetic, not a charted or legally valid navigational area.

## B. Temporal validity and synchronization

- All P04 instant provenance remains in UTC, with explicit timezone, parsed comparisons and original input resolution. `bh:TemporalUnit` remains distinct from `time:ProperInterval`.
- `bh:nextTemporalUnit` does not imply a contiguous temporal interval. Only `time:ProperInterval` individuals may appear in `time:intervalBefore`/`time:intervalAfter`/`time:intervalMeets`. `Meets` requires **exact UTC boundary equality** at recorded precision.
- A geographic feature may be persistent while a particular *geometry representation* or source snapshot is valid only for a defined time range or chart edition; provenance must identify data edition, measurement/valid time and processing time.
- Two positions from different vessels are not ipso facto co-temporal. Before creating a time-qualified `InteractionBehavior` comparison, require an explicitly selected synchronization/evidence window. Its numeric threshold remains **OPEN** in P05-00. Incompatible observations must be rejected, flagged `INDETERMINATE` or held as unverified candidates, not treated as simultaneous facts.
- AIS source observation event time vs receiver time vs processing/inference time are distinct; do not infer complete UTC timestamp from AIS second field without documented reconstruction.

## C. Proposed named-graph topology (candidate not deployed)

Use RDFLib `Dataset(default_union=False)` with explicit graph identifiers. **The graph IRI is a partitioning identifier, not proof of truth or authorization; the software must enforce graph allowlists.**

| Graph role | Proposed IRI | May contain | Prohibited content / checks |
|---|---|---|---|
| Observed / input | `https://w3id.org/mass-ontology/graph/p05/observed` | P04 observations, source-linked position/speed/course, observed units; source `prov:Entity` | Semantic target labels, `bh:hasSemanticBehavior`, `bh:hasBehaviorInterpretation`, classifier output |
| Context | `https://w3id.org/mass-ontology/graph/p05/context` | Spatial features, geometry snapshots, CRS/version and contextual attribution | Classifier output and post-inference labels; unqualified COLREG compliance assertions |
| Derived interaction | `https://w3id.org/mass-ontology/graph/p05/derived-interaction` | Computed relation descriptions and their explicit source observations/geometries/time | Automatic safety/authority conclusions; unproven crossing/collision risk |
| Inferred semantic | `https://w3id.org/mass-ontology/graph/p05/inferred-semantic` | `SemanticBehavior`, `BehaviorInterpretation`, hypotheses and qualified results with link to `prov:Activity` | Raw observations re-cast as truth; unauthorized reclassification of operational modes |
| Provenance | `https://w3id.org/mass-ontology/graph/p05/provenance` | Source, derivation, algorithm/processing activity, model version, graph-run metadata and named graph identity | Unexplained derived labels without owning source lineage |
| Schema / vocabulary | **separate ontology inputs, NOT inference source data** | Definitions, classes, shapes, term registries | Do not confuse appearance of a label class IRI in schema with a result type asserted in pre-inference instance data |

**Proposed graph contract:**
1. The *inference-input graph set* is an explicit allowlist of `observed`, `context`, and only pre-authorized `derived-interaction` results. `inferred-semantic` is **never** part of the same run's input.
2. For BH-V08, inspect **every named inference-input graph** with scoped `GRAPH` queries; `Dataset(default_union=False)` alone is insufficient if the code accidentally queries the wrong active graph. Pre-graph leakage includes forbidden `bh:hasSemanticBehavior`, `bh:hasBehaviorInterpretation`, type assertions for `bh:SemanticBehavior`/descendants when used as target labels, and post-classification `bh:BehaviorInterpretation` instances, but **not** legitimate OWL class declarations in schema.
3. During the same run, the output `inferred-semantic` graph records candidate IDs, source `TemporalUnit`, `prov:wasDerivedFrom` inputs, `prov:wasGeneratedBy` typed `prov:Activity`, algorithm/version and review status. Confidence scores are optional and must not be falsely represented as calibrated probabilities.
4. Named-graph identifiers are a **contracted partition**; an external RDF reasoner/SPARQL store may merge graphs under specific entailment settings. The implementation must explicitly configure query dataset, inference mode, default-graph behavior and type assertion policy; tests must fail on leakage or unnoticed graph collapse.
5. Provenance metadata for named graphs can be recorded as triples in a dedicated provenance graph; one must not assume RDF Dataset semantics automatically grants source authority or epistemic truth to graph names.
6. Derived topology and semantic results may be recalculated only with an explicit pipeline-run and input geometry/observation version. Re-running a newer model or altered chart produces a new named result/version, not a silent update of accepted historical evidence.
7. No inferred behavior is directly propagated into `nav:COLREGSituation`, `mass:OperationalMode`, `ModeOfOperation`, `OperationalCondition`, `nav:Maneuver`, a safety claim or control action.

**Graph access:** the source observation P04 graph may remain a physical legacy file for reproducibility. Importing it as one of the named `observed` P05 graphs is an explicit versioned **derived dataset construction** operation; no rewriting of frozen P04 Turtle files.

## D. Validation and negative-case design

| Test/design ID | Positive condition | Negative mutant/observable rejection | Scope |
|---|---|---|---|
| P05-G01 | GeoSPARQL `Feature` and `Geometry` separate, CRS84 lon/lat WKT legal | reversed/unknown axes or missing CRS policy, invalid or unclosed polygon | P05-02 |
| P05-G02 | Two compared points have compatible event times, declared reference frame and cited source | unsynchronized vessel positions, no reference vessel/frame | P05-03 |
| P05-G03 | Topology relation has source geometries and GeoSPARQL function/engine semantics | geometry URI with no geodetic data, unsupported engine function falsely marked PASS | P05-03 |
| BH-V04 | Genuine `time:intervalMeets` on proper extents | false meeting across P04 gap or asserted directly between TemporalUnits | P05-06 |
| BH-V07 | One relation has subject, reference, temporal context and provenance | reference object/time missing; `nav:COLREGSituation` substituted | P05-06 |
| BH-V08 | Pre-graph input labels absent, output graph separate | leaked `bh:hasSemanticBehavior`, post-result `rdf:type` in input named graph | P05-05/06 |
| BH-V09 | Every inferred result has source evidence, `prov:Activity`, status | missing source/activity; invalid score or silent acceptance | P05-04/06 |
| BH-V10 | No OWL equivalence/unsafe conclusion from label | introduced `owl:equivalentClass`/property chain implying operational mode or COLREG | P05-06 |

These are **future test requirements**, not runtime PASS. P05 shall include both positive and rule-isolated negative fixtures, fail-closed status and exact-binding BH-CQ-04…10 query oracles. P04 legacy CQ-01…14 and `make behavior-test` must remain functional. An engine that does not support a claimed GeoSPARQL function must report **BLOCKED** or a deliberately documented external computational fallback, never PASS.

## E. External source controls and open decisions

OGC GeoSPARQL 1.1 standard: https://docs.ogc.org/is/22-047r1/22-047r1.html  
OGC standard landing / official artifacts: https://www.ogc.org/standards/geosparql/  
RDF 1.1 dataset semantics: https://www.w3.org/TR/rdf11-datasets/  
SPARQL 1.1 `GRAPH` behavior: https://www.w3.org/TR/sparql11-query/#queryDataset  

**Open before implementation:** publisher RDF artifact/version/ontology IRI/checksum/license, OGC CRS84 versus external geometry CRS policy, geometry validity/version, distance function units/geodesic rule, synchronization tolerance, reference object identity, geometry engine compatibility, taxonomy SKOS/OWL choice, status vocabulary and confidence semantics, named graph metadata/provenance policy, and potential vessel-vessel extension. See [GeoSPARQL source-candidate registry](../standards/P05-00-external-spatial-source-register.json).

**P05-00 gate:** this file is a design document only. Project-owner review and subsequent implementation tests are required to turn the candidate rules into a release acceptance claim.
