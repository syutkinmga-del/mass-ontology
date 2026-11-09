# P05-00 — Spatial + Semantic Domain Design Contract (BH-P05 / v0.5.0)

**Status:** APPROVED DESIGN BASELINE WITH OPEN ADRs — design contract only; production axioms and BH-P05 runtime still unapproved/unimplemented. See [separate owner-directed decision](../governance/DEC-P05-00-2026-11-09-design-approval.md).  
**Date prepared:** 2026-11-09.  
**Controlled input:** [Integrated Roadmap v1.1](../roadmap.md), [DCCR-01](DCCR-01-xiong-ship-behavior-review.md), [DCCR-02](DCCR-02-semantic-design-review.md), [DCCR-03](DCCR-03-ontology-alignment-specification.md), [DCCR-04](DCCR-04-validation-contract.md), [P04 terminology/time policy](../architecture/P04-00-terminology-time-policy.md).  
**Immutable published source baseline:** `v0.4.0` at commit `d0f2368df4268cfe3c6079a1681502cad0b867fb`, governed by separate R10-2026-02.  
**Development branch baseline at P05-00 start:** `d45607432c313a566c7b50d385779391cf48fa1c`.  
**Owner decision for P05-00:** APPROVED DESIGN BASELINE WITH OPEN ADRs, 2026-11-09; explicit owner-directed chat instruction, **not an electronic signature**. Exact pre-registration design source commit: `a73a7c8c5bc5f11a789405abd6d94da870d295b3`. All BH-P05 runtime gates remain DEFERRED.

## 1. Boundary and purpose

This document instantiates the Roadmap's **v0.5.0 / BH-P05 spatial + semantic layer** as a traceable implementation contract. Its technical purpose is to provide a *qualified description* of maritime spatial context around observed vessel trajectories, then separate observed/context information from computed relations and inferred semantic interpretation.

**In scope:** `bh:EnvironmentSpace`, GeoSPARQL feature/geometry alignment, `bh:InteractionBehavior` with Direction/Distance/Topology relation descriptions, `bh:SemanticBehavior`, `bh:BehaviorInterpretation`, time/adjacency, explicit pre/context/post named graph boundaries and evidence provenance.

**Out of scope:** changing P04 observations, source AIS decoding, production risk computation, actual COLREG compliance/rule selection, autonomous navigation actuation, ROC lost-link authority/handover (v0.6), safety certification (v0.7), GeoSPARQL-based ODD applicability conclusions without reviewed ODD evidence, and BH-P09 MLLM accuracy/recognition.

**P05-00 deliverable is design, NOT newly deployed OWL classes, GeoSPARQL vendor RDF, SHACL shapes, SPARQL answers, positive/negative fixture execution or `BH-P05 PASS`.** Required runtime work begins at P05-01, subject to approvals below. The source DCCR decisions remain unchanged.

## 2. Canonical concept inventory and meaning

Terms under `bh:` are existing reserved candidates from DCCR-03, not declarations made by this document. Do not create these OWL classes until approved production ontology design and negative tests are available. The concept inventory follows DCCR-01's classes **C08–C13**, maintaining the article name **InteractionBehavior** (not InteractiveBehavior).

| ID | Proposed term / IRI | Type / definition in MASS information layer | Origin / authority | Owner | CQ | Earliest release | Example instance (illustrative only) |
|---|---|---|---|---|---|---|---|
| C08 | `bh:InteractionBehavior` | Time-scoped *information description* of spatial relation subject vessel ↔ identified reference feature/vessel; not the relation predicate itself, an encounter event, or a COLREG determination | DCCR-01 C08, DCCR-02 D04, DCCR-03 | MASS P05 ontology | 04, 05 | 0.5 | `ex:relationAt1200` |
| C09 | `bh:DirectionRelation` | Contextualized direction/bearing description with frame of reference and time; may coexist with distance/topology | DCCR-01 C09, DCCR-02 D04 | MASS P05 ontology | 04 | 0.5 | `ex:directionAt1200` |
| C10 | `bh:DistanceRelation` | Actual or computed separation description with geometry source, timestamp and unit; **not** `nav:hasCPA` or a predicted closest approach | DCCR-01 C10, DCCR-02 D04 | MASS P05 ontology | 04 | 0.5 | `ex:distanceAt1200` |
| C11 | `bh:TopologyRelation` | Reified information description of topological relation supported by geometry; GeoSPARQL predicates are referenced as *spatial semantics*, not the same individual | DCCR-01 C11, DCCR-03 | MASS P05 ontology | 04 | 0.5 | `ex:withinZoneAt1200` |
| C12 | `bh:SemanticBehavior` | Inferred behavior **description/result**, not a ship's actual action, OperationalMode, OperationalCondition, COLREGSituation, or maneuver command | DCCR-01 C12, DCCR-02 D05 | MASS P05 ontology | 06–10 | 0.5 | `ex:semanticCandidateAt1200` |
| C13 | `bh:EnvironmentSpace` | Identifiable geographical/environmental *feature or zone*, with separately maintained geometry/validity; not ODD/OE specification or `geo:Geometry` individual | DCCR-01 C13, DCCR-03 | MASS P05 ontology | 04 | 0.5 | `ex:approachZone` |
| M01 | `bh:BehaviorInterpretation` | MASS-proposed information/assessment record connecting unit, proposed behavior, evidence, generating `prov:Activity`, and review status | DCCR-02 D05 / DCCR-03, **not** source article class | MASS P05 ontology | 06, 10 | 0.5 | `ex:interpretation01` |
| X01 | `geo:Feature` | External OGC term describing a feature; candidate superclass for EnvironmentSpace subject to exact external term/version and local ontology review | OGC GeoSPARQL 1.1 | OGC, reused | 04 | 0.5 | `ex:approachZone` |
| X02 | `geo:Geometry` | External OGC geometry *representation* of a feature, distinct from Vessel, Trajectory, EnvironmentalZone, and physical/geographic referent | OGC GeoSPARQL 1.1 | OGC, reused | 04 | 0.5 | `ex:approachZoneGeometry` |
| P04 | `bh:Trajectory`, `bh:TemporalUnit` | Previously implemented information records; preserve their identity and linked `time:ProperInterval` extents | Frozen BH-P04 | MASS existing | 04–05 | 0.4 | `ex:trajectory17`, `ex:u17` |

Namespace candidates from DCCR-03: `bh: <https://w3id.org/mass-ontology/behavior#>`, `maritime: <https://w3id.org/mass-ontology/maritime#>`, `geo: <http://www.opengis.net/ont/geosparql#>`, `time: <http://www.w3.org/2006/time#>`, `prov: <http://www.w3.org/ns/prov#>`. Namespace publication/dereferencing has **not** been independently demonstrated.

## 3. Relationship inventory and semantic design rules

| Design key | Proposed link or reuse | Semantic contract and boundary | Gate |
|---|---|---|---|
| D-P05-01 | `bh:hasInteractionBehavior` | `TemporalUnit → InteractionBehavior`; zero-or-many relation descriptions; not an `EncounterSituation` identity | BH-V07 |
| D-P05-02 | `bh:hasSubjectVessel` | `InteractionBehavior → maritime:Vessel`; exactly one *in a curated assertion* | BH-V07 |
| D-P05-03 | `bh:referencesSpace` | `InteractionBehavior → EnvironmentSpace` when environment reference; if other vessel is reference, model separate reviewed role rather than coercing vessel into EnvironmentSpace | BH-V07 |
| D-P05-04 | `bh:hasReferenceFrame` | Direction/bearing requires true/relative/magnetic/geodetic frame; default and numeric bearing convention remain explicit decision | BH-V07 |
| D-P05-05 | `geo:hasGeometry`, `geo:asWKT` | Feature has a separately identified geometry with declared CRS, temporal applicability and provenance; Geometry is not Trajectory | P05 geometry validation |
| D-P05-06 | `time:intervalBefore/After/Meets` | Apply only to `time:ProperInterval` extents. `bh:nextTemporalUnit` expresses segmentation order **without** implying Meets; exact touching interval boundaries required | BH-V04 |
| D-P05-07 | `bh:hasSemanticBehavior`, `bh:hasBehaviorInterpretation` | Post-inference only; none in source/pre/context input graphs | BH-V08 |
| D-P05-08 | `bh:proposesBehavior`, `prov:wasDerivedFrom`, `prov:wasGeneratedBy` | Each interpretation has a unit, candidate, enumerated source evidence and producing activity; review status explicit | BH-V09 |
| D-P05-09 | `bh:confidenceScore`, `bh:reviewStatus` | Score optional, if present finite decimal [0,1]; calibration not implied. Status controlled and explicit; hypothesis must not silently become accepted fact | BH-V09 |
| D-P05-10 | Reuse `geo:sf*` predicates / `geof:*` functions as supported | Topological predicates and computed geometry functions are distinct from local time-scoped `TopologyRelation` descriptions | BH-V07 |
| D-P05-11 | No `owl:equivalentClass` or implicit chains | SemanticBehavior, navigation mode, COLREG situation and BFO/CCO are not automatically equivalent or entailed | BH-V10 |

**Information vs physical:** `bh:InteractionBehavior`, `bh:SemanticBehavior`, `bh:Trajectory` and `bh:TemporalUnit` are information descriptions/records. The vessel and geographic zone are *referents*; a `geo:Geometry` is their geometric representation. It is not legitimate to call all of them a physical motion process.

**Two-vessel extension:** DCCR-01 proposes but does not approve a `VesselVesselInteraction` extension. It requires an explicit reference-vessel role and subject/reference identities; for P05-00 retain it as an **OPEN ADR**, not an already committed class.

## 4. Required CQ and validation traceability

The BH-P05 contract is inherited from DCCR-04, not new ad hoc numbering:

| ID | Query objective (not yet implemented) | Proposed oracle / bindings | Depends on |
|---|---|---|---|
| BH-CQ-04 | Spatial context, reference feature, directional/distance/topological information associated with a TemporalUnit | Unit IRI, relation IRI/type, reference-object IRI, frame/CRS, time, evidence IRI | BH-V07 |
| BH-CQ-05 | Consecutive units versus truly meeting temporal intervals | Unit pair, distinct ProperInterval pair, normalized boundaries, meets boolean; contiguous and gap cases | BH-V04 |
| BH-CQ-06 | Inferred candidate and the evidence + activity that produced it | Unit, candidate, activity, source observations, method version, review status | BH-V09 |
| BH-CQ-07 | Absence of forbidden labels in source input | scoped `ASK`/zero-prohibited-triples over named *allowed input* graphs only, no default union | BH-V08 |
| BH-CQ-08 | Same observed movement under independently supplied operating modes | no automatic equivalence; explicit context/evidence identity, mutation oracle | BH-V10 |
| BH-CQ-09 | Independent evidence required before asserting any COLREGSituation | no derived COLREG type from behavior label alone; no claimed compliance | BH-V10 |
| BH-CQ-10 | Concurrent alternate hypotheses and their review status | candidate IRI, optional decimal score, status and provenance; explicit deterministic order/oracle | BH-V09 |

Corresponding executable rules are **BH-V04, BH-V07, BH-V08, BH-V09, BH-V10**, plus existing P04 BH-V01–V03, V05–V06, V11–V12 and all legacy CQ-01…14. Do not mark unexecuted P05 tests PASS. The `BH-CQ-10` behavior taxonomy experiment may be refined in BH-P09; its basic provenance/query contract belongs here.

For every query, later deliver a versioned `queries/behavior/bh-cq-04..10.rq`, correct exact-binding oracle including types, positive fixture and rule-specific negative fixture where applicable, and explicit profile-runner status. **P05-00 files are not those runtime deliverables.**

## 5. Spatial, temporal and evidence separation

The *proposed* CRS, geometry, temporal and named-graph contracts are detailed in [P05-00 spatial/graph policy](../architecture/p05-00-spatial-graph-crs-policy.md). Core acceptance principles:

1. GeoSPARQL **1.1 (OGC 22-047r1)** is the selected **documentation baseline candidate**, not an approved or locally vendored RDF import. Exact ontology artifact/version IRI, hash, license and runtime-function support remain P05-02 release-blocking review items.
2. Candidate `geo:asWKT` serializes `geo:wktLiteral` with **CRS84 lon latitude** (or a distinct explicit CRS; never silently transpose EPSG:4326 coordinate tuples).
3. `EnvironmentSpace` retains feature identity separate from `geo:Geometry` and from ODD geographic applicability specifications.
4. Source observations, contextual geodata, computed interaction descriptions and inferred semantic labels must be separately named, provenance-traceable graphs. Schema graph is not evidence of an asserted classification in instance data.
5. No derived label may occur in the pre-inference graph(s) for a run; no automatic promotion of post-inference assertions to observed graph.
6. Spatial relations require explicit **time compatibility** and source geometry lineage. Calculating a distance from two stale positions does not prove contemporaneous physical separation or CPA.
7. No `time:intervalMeets` without actual equality of normalized instants; P04 policy's 1-second-resolution input does not create a tolerance permitting interpolation across gaps.

## 6. P05-00 decisions and explicit blockers

| Decision | Proposed disposition | Status |
|---|---|---|
| P05-D01 | Reuse DCCR-01 C08–C13 / DCCR-03 local `bh:` IRIs, avoid unnecessary invented duplicates | DESIGN CANDIDATE |
| P05-D02 | Default WKT point geometry: explicit OGC CRS84, longitude then latitude; use separate CRS transformation when necessary | DESIGN CANDIDATE |
| P05-D03 | Named graphs `source/observed`, `context`, `derived/interactions`, `inferred/semantic`, `provenance` with explicit allowlists | DESIGN CANDIDATE |
| P05-D04 | Standard GeoSPARQL Feature/Geometry and topology functions where actual engine support is proven; 1.1 source edition candidate | PENDING RDF/ENGINE/RIGHTS VERIFICATION |
| P05-D05 | Exact semantics for `EnvironmentSpace` and optional vessel-as-reference role | OPEN ADR |
| P05-D06 | `SemanticBehavior` OWL subclasses versus SKOS concepts versus dual model/punning | OPEN ADR |
| P05-D07 | `BehaviorInterpretation` status vocabulary, score semantics and multiple-hypothesis handling | OPEN ADR |
| P05-D08 | Geometry validity window, distance computation/units, bearing reference frames and synchronization window | OPEN ADR |
| P05-D09 | Evaluation harness: precise P05-PASS vs DEFERRED/BLOCKED status and isolation of P04 release gates | REQUIRED BEFORE P05 IMPLEMENTATION |

No blanket assumption of a future `EnvironmentSpace rdfs:subClassOf geo:Feature` axiom before the P05 design decision. No production P05 RDF is written in this stage. No external ontology artifact is imported without independent license, version, IRI and checksum controls.

## 7. Completion criteria for P05-00 (design only)

- [ ] Concept inventory includes definitions, source/origin, owner, CQs, target release and example instances; owner accepts unresolved proposals.
- [ ] Seven BH-CQ (04–10) have planned exact-binding or negative ASK oracles with BH-V links.
- [ ] BH-V04/V07/V08/V09/V10 are assigned positive/negative design fixtures, implementation owners and pass/fail mechanisms.
- [ ] Spatial CRS/WKT, time-validity and explicit graph partition contracts are reviewed.
- [ ] GeoSPARQL version candidate, concrete ontology artifact selection and licensing **open tasks** are documented; no fake pinning.
- [ ] P05-01/P05-02 implementation gates and non-inference of COLREG safety claims reviewed.
- [x] Design checker executed and archived: [P05-00 design CI #42596892643](https://github.com/syutkinmga-del/mass-ontology/actions/runs/42596892643), PASS, `failures: []`; this constitutes **P05-00 design-contract integrity only**, not ontology runtime validation.
- [x] Project-owner instruction registered as a **separate design-only text decision** with six explicitly OPEN ADRs; no digital signature or v0.5.0 release approval claimed.

Owner-directed approval was recorded separately on 2026-11-09. **P05-00 is APPROVED AS A DESIGN BASELINE WITH OPEN ADRs, not approved as a working P05 ontology.** Its merge into `main` does not implement or resolve the six open ADRs; P05-D05 blocks production `EnvironmentSpace` axioms until a separate decision.

## 8. Implementation follow-on (separate PRs)

**P05-01:** select `EnvironmentSpace` feature semantics/identity and implement a narrow, non-overpromising RDF module.  
**P05-02:** pin GeoSPARQL 1.1 RDF (verified bytes/licenses), support WKT/CRS; demonstrate actual engine functions and negative geometry tests.  
**P05-03:** implement qualified interaction descriptions for environment reference and, only if approved, vessel-vessel reference.  
**P05-04:** implement candidate semantic interpretations with evidence/status; no unapproved COLREG inference.  
**P05-05:** materialize explicit named-graph separation per contract and closed-world label leakage checks.  
**P05-06:** execute P05 and P04 regression validation; archive exact-binding CQs and negative oracle evidence.  
**P05-07:** controlled release review and new exact-SHA owner authorization for v0.5.0.

**Sources:** Roadmap v1.1 §§A–E; DCCR-01 §§A/C/G; DCCR-02 D04/D05; DCCR-03 §§3–6; DCCR-04 §§2/4/6/7; [OGC GeoSPARQL 1.1](https://docs.ogc.org/is/22-047r1/22-047r1.html); [W3C SPARQL 1.1 datasets](https://www.w3.org/TR/sparql11-query/#rdfDataset).

## 9. Owner-directed approval registration addendum — 2026-11-09

**Source document preserved at approved SHA** `a73a7c8c5bc5f11a789405abd6d94da870d295b3`; the status update here belongs to a later governance registration commit and does **not** retroactively change that approved source snapshot.

- Decision: [DEC-P05-00-2026-11-09-01](../governance/DEC-P05-00-2026-11-09-design-approval.md) — `APPROVED_DESIGN_BASELINE_WITH_OPEN_ADRS`.
- Evidence: owner's exact instruction in the ChatGPT conversation, a **text registration** (not a signed PDF, digital signature or independently authenticated identity).
- Accepted planning directions: P05-D01 (DCCR terminology reuse), P05-D02 (CRS84/WKT lon-lat convention), P05-D03 (named-graph separation); they are not yet executable P05 ontology axioms.
- **Unresolved ADRs:** P05-D04 GeoSPARQL artifact/rights/engine; P05-D05 EnvironmentSpace identity and other-vessel role; P05-D06 OWL/SKOS behavior representation; P05-D07 interpretation status/score/hypotheses; P05-D08 temporal synchronization/geodetic calculations/bearing; P05-D09 fail-closed P05 implementation validator. None is made resolved by this approval.
- **Allowed next action:** initiate P05-01 `EnvironmentSpace` **design/ADR** work in a new PR. P05-D05 must be closed before committing production class axioms that depend on its final semantics.
- Runtime status: `BH-V04/V07/V08/V09/V10 = DEFERRED`, `BH-CQ-04…10 = DEFERRED`; BH-P04 regression preserved; v0.5.0 release remains unauthorized.
