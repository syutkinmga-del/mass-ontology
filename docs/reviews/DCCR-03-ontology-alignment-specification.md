# DCCR-03 — Ontology Alignment Specification: Ship Behavior Ontology

**Project:** MASS Ontology Stack / MASS Domain Library  
**Date:** 2026-10-27  
**Approval date:** 2026-10-27  
**Status:** **APPROVED — design contract; implementation and definitive external mappings pending**  
**Inputs:** DCCR-01 (APPROVED, 2026-10-26); DCCR-02 (APPROVED, 2026-10-26).  
**Baseline:** `MASS-SK-1.0` (`MASSKernel_v1.0.sysml`, immutable); `mass-ontology` current development line `v0.3.0-dev` as inspected through the connected GitHub repository (2026-10-27).  
**Source study:** Xiong, Wang, Wu, Chen, “Ontology-Guided Multimodal Large Language Model for Semantic Recognition of Ship Navigation Behaviors,” *Journal of Marine Science and Engineering* 14(19), 1859 (2026), https://doi.org/10.3390/jmse14191859.

> This approved specification records **design-level engineering mappings**. Approval does not establish production OWL axioms, adopted external imports, a verified BFO/CCO mapping, or deployed w3id.org resolution. The source's ontology terms are indicated explicitly. The additional architecture and validation proposals originate with MASS Ontology design.

## 1. Scope, non-goals, consistency contract

DCCR-03 converts approved semantic boundaries into a proposed formal OWL/RDF contract for a separately modularized Ship Behavior Ontology. Its purpose is to identify **namespaces, class identity, relation direction, standard reuse, closed-world validation, release sequencing, and pending alignment decisions**. It does not modify `MASSKernel_v1.0.sysml`, change the existing `v0.3.0` tag, or publish inferred behavior classes as ground truth.

**Source-derived layer (Xiong et al.):** Vessel → Trajectory → TemporalUnit, three behavior dimensions, spatial/environment links and before/after/meets temporal semantics. Source explicitly separates graph construction before high-level behavior inference from post-inference labeling.

**MASS design additions:** distinguish physical vessel motion from its information records and inferred labels; use OWL-Time on temporal extents; preserve provenance, uncertainty, review status and named-graph separation; connect to MASS operational/decision/safety models only through auditable and separately justified relations.

**Invariant boundary:** `SemanticBehavior` ≠ `ModeOfOperation` ≠ `OperationalCondition` ≠ `COLREGSituation` ≠ `nav:Maneuver`. Do not assert global `owl:equivalentClass` or `owl:disjointWith` without explicit ontological justification.

## 2. Proposed module and IRI policy

### 2.1 Prefixes

| Prefix | Proposed / standard namespace | Status |
|---|---|---|
| `bh:` | `https://w3id.org/mass-ontology/behavior#` | **RESERVED / PROPOSED**, not published |
| `maritime:` | `https://w3id.org/mass-ontology/maritime#` | **PROPOSED** future general-vessel module |
| `common:` | `https://w3id.org/mass-ontology/common#` | EXISTING local ontology |
| `mass:` | `https://w3id.org/mass-ontology/core#` | EXISTING local ontology |
| `nav:` | `https://w3id.org/mass-ontology/navigation#` | EXISTING local ontology |
| `sosa:` | `http://www.w3.org/ns/sosa/` | Standard vocabulary |
| `ssn:` | `http://www.w3.org/ns/ssn/` | Standard vocabulary |
| `time:` | `http://www.w3.org/2006/time#` | Standard vocabulary |
| `qudt:` | `http://qudt.org/schema/qudt/` | Standard vocabulary |
| `unit:` | `http://qudt.org/vocab/unit/` | Standard vocabulary |
| `geo:` | `http://www.opengis.net/ont/geosparql#` | Standard vocabulary |
| `prov:` | `http://www.w3.org/ns/prov#` | Standard vocabulary |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | Standard vocabulary |

**Ontology IRI proposal:** `https://w3id.org/mass-ontology/behavior` (without `#`). Avoid claiming URL resolution before registering/testing it. RDFLib does not automatically honor `catalog-v001.xml` or follow `owl:imports`; manual data graph loading must continue until a deterministic import-loading mechanism is implemented.

### 2.2 Proposed repository partition

```text
02-maritime/                     # general Vessel, optional candidate module
05-observation/                  # v0.4 SOSA / SSN usage + AIS/Radar examples
06-quantities/                   # v0.4 QUDT measurement patterns
07-behavior/                     # Behavior Ontology under staged development
  ship-behavior.ttl
shapes/ship-behavior.shacl.ttl    # DCCR-04 implementation
examples/behavior-trajectory.ttl
queries/behavior/bh-cq-*.rq
competency-questions/behavior-cq.md
docs/reviews/DCCR-03-ontology-alignment-specification.md
```

These are **suggested paths**, not pre-existing checked-in files. The numeric ordering may be adjusted to current repo conventions after implementation review. Modules from `v0.5` must not be imported into `v0.4` MVP if their term availability would create brittle dependencies.

## 3. Proposed class mapping matrix (all 13 source core classes)

**Mapping status keys:** `EXISTING-SK`, `NARROWER-OWL`, `ADD-v0.4`, `ADD-v0.5`, `DEFER`, `DRAFT-ALIGNMENT`; these are proposed implementation dispositions, not truth of OWL equivalence.

| ID | Xiong class | Proposed local IRI | Proposed local upper class / external link | Mapping decision and constraint | Phase |
|---|---|---|---|---|---|
| C01 | `Vessel` | `maritime:Vessel` | New general maritime vessel class; future `mass:MASSVessel rdfs:subClassOf maritime:Vessel` after review | `MASSKernel::Vessel` exists; current OWL `mass:MASSVessel` is narrower; do not classify all targets as MASS | v0.4 |
| C02 | `Trajectory` | `bh:Trajectory` | `bh:BehaviorInformationEntity` → candidate local `common:InformationArtifact` | Information record, not motion process, route plan or `geo:Geometry` | v0.4 |
| C03 | `TemporalUnit` | `bh:TemporalUnit` | `bh:BehaviorInformationEntity`; linked to but not identical with `time:TemporalEntity` | Sequence segment and an associated time extent are distinct | v0.4 |
| C04 | `PhysicalBehavior` | `bh:PhysicalBehavior` | `bh:BehaviorDescription` → `bh:BehaviorInformationEntity` | Information-based description of observed movement, not guaranteed to be a BFO process | v0.4 |
| C05 | `PositionState` | `bh:PositionState` | `rdfs:subClassOf bh:PhysicalBehavior` | Position/geometry-derived descriptive dimension | v0.4 |
| C06 | `SpeedState` | `bh:SpeedState` | `rdfs:subClassOf bh:PhysicalBehavior` | SOG, speed variation, speed statistics | v0.4 |
| C07 | `CourseState` | `bh:CourseState` | `rdfs:subClassOf bh:PhysicalBehavior` | COG and course variation; separate heading/bearing | v0.4 |
| C08 | `InteractionBehavior` | `bh:InteractionBehavior` | `rdfs:subClassOf bh:BehaviorDescription` | Descriptive, contextualized relation; not encounter occurrence | v0.5 |
| C09 | `DirectionRelation` | `bh:DirectionRelation` | `rdfs:subClassOf bh:InteractionBehavior` | Reified direction description; reference frame required for numeric bearings | v0.5 |
| C10 | `DistanceRelation` | `bh:DistanceRelation` | `rdfs:subClassOf bh:InteractionBehavior` | Current/computed distance, not forecast CPA/DCPA | v0.5 |
| C11 | `TopologyRelation` | `bh:TopologyRelation` | `rdfs:subClassOf bh:InteractionBehavior`; GeoSPARQL used for spatial predicate evidence | Reified relation statement ≠ GeoSPARQL predicate | v0.5 |
| C12 | `SemanticBehavior` | `bh:SemanticBehavior` | `rdfs:subClassOf bh:BehaviorDescription` | Inferred characterization; provenance/review separated | v0.5 |
| C13 | `EnvironmentSpace` | `bh:EnvironmentSpace` | Candidate `rdfs:subClassOf geo:Feature` | A spatial feature, **not** ODD/OE; feature/geometry separated | v0.5 |

**Additional proposed mediator classes, not source-extracted:** `bh:BehaviorInformationEntity`, `bh:BehaviorDescription`, `bh:BehaviorInterpretation`; optional later `bh:VesselMotionOccurrence`, `bh:VesselVesselInteraction`.

**Current local-common relationship (proposed):** `bh:BehaviorInformationEntity rdfs:subClassOf common:InformationArtifact`. All listed records/descriptions may specialize this mediating type; the commitment is a **local modeling hypothesis**, not acceptance of any exact BFO/CCO superclass. Review whether `Trajectory` and `TemporalUnit` should instead specialize a separately named record/dataset intermediary before committing OWL assertions.

**General-vessel migration hazard:** existing `nav:OwnShip rdfs:subClassOf mass:MASSVessel` and `nav:TargetShip` has no existing declared `rdfs:subClassOf` general Vessel. The desired `maritime:Vessel` integration requires a dedicated compatibility change and the existing 14 ontology-CQ checks; don't silently rewrite `mass:MASSVessel` to be synonymous with general Vessel.

## 4. Proposed object property mappings (source R01–R09)

| ID | Source relationship | Proposed property / mapping | Domain → Range (candidate) | OWL commitment | DCCR-04 validation |
|---|---|---|---|---|---|
| R01 | `hasTrajectory` | `bh:hasTrajectory` plus optional inverse `bh:ofVessel` | `maritime:Vessel` → `bh:Trajectory` | ObjectProperty, optional `owl:inverseOf` after review | populated trajectory one vessel |
| R02 | `hasTemporalUnit` | `bh:hasTemporalUnit` plus `bh:partOfTrajectory` | `bh:Trajectory` → `bh:TemporalUnit` | ObjectProperty, inverse candidate | each populated unit one trajectory; consistent order |
| R03 | `hasPhysicalBehavior` | `bh:hasPhysicalBehavior` | `bh:TemporalUnit` → `bh:PhysicalBehavior` | ObjectProperty | multiple coexisting state dimensions allowed |
| R04 | `hasInteractionBehavior` | `bh:hasInteractionBehavior` | `bh:TemporalUnit` → `bh:InteractionBehavior` | ObjectProperty | relation descriptions linked to valid unit |
| R05 | `referencesSpace` | `bh:referencesSpace` | `bh:InteractionBehavior` → `bh:EnvironmentSpace` | ObjectProperty | spatial reference object and evidence present |
| R06 | `hasSemanticBehavior` | `bh:hasSemanticBehavior` | `bh:TemporalUnit` → `bh:SemanticBehavior` | ObjectProperty **POST-INFERENCE ONLY** | absent from input graph; supported by classification evidence |
| R07 | `before` | `time:intervalBefore` | `time:ProperInterval` → `time:ProperInterval` | **REUSE standard**, not local predicate | end(I1) < begin(I2) |
| R08 | `after` | `time:intervalAfter` | `time:ProperInterval` → `time:ProperInterval` | **REUSE standard**, not local predicate | begin(I1) > end(I2) |
| R09 | `meets` | `time:intervalMeets` | `time:ProperInterval` → `time:ProperInterval` | **REUSE standard**, not local predicate | end(I1) = begin(I2), within selected precision; no inferred continuity across gaps |

**Critical:** The paper's temporal links conceptually connect `TemporalUnit` records, but W3C OWL-Time `intervalBefore`/`After`/`Meets` require **proper intervals** as both domain and range. We must map these relationships through `bh:hasTemporalExtent`, not assert them between TemporalUnit individuals.

## 5. MASS-specific relationships and data properties (proposed, not source-extracted)

| Property | Proposed domain → range | Purpose / semantic qualification | Phase |
|---|---|---|---|
| `bh:ofVessel` | Trajectory → `maritime:Vessel` | Identity of recorded subject vessel | v0.4 |
| `bh:partOfTrajectory` | TemporalUnit → Trajectory | Segment membership; only one parent in curated version | v0.4 |
| `bh:hasTemporalExtent` | TemporalUnit → `time:TemporalEntity` | Distinct interval or instant resource; segment datasets normally require `time:ProperInterval` | v0.4 |
| `bh:nextTemporalUnit` | TemporalUnit → TemporalUnit | Sequence adjacency; must belong to same trajectory; does not imply `intervalMeets` | v0.4 |
| `bh:hasQuantityValue` | PhysicalBehavior → `qudt:QuantityValue` | Motion feature value accompanied by unit | v0.4 |
| `bh:supportedByObservation` | PhysicalBehavior → `sosa:Observation` | Source observations for description | v0.4 |
| `bh:hasSubjectVessel` | InteractionBehavior → `maritime:Vessel` | Subject of calculated spatial relation | v0.5 |
| `bh:hasReferenceFrame` | DirectionRelation → controlled reference-system concept | True/magnetic/relative, geodetic, coordinate frame | v0.5 |
| `bh:hasBehaviorInterpretation` | TemporalUnit → `bh:BehaviorInterpretation` | Proposed label(s), evidence and review status | v0.5 |
| `bh:proposesBehavior` | BehaviorInterpretation → SemanticBehavior | Candidate behavioral characterization | v0.5 |
| `bh:behaviorCategory` | SemanticBehavior → `skos:Concept` | Stable category vocabulary (PROPOSED CHOICE, still under review) | v0.5 |
| `bh:confidenceScore` | BehaviorInterpretation → `xsd:decimal` | Normalized and explicitly defined [0,1] only; not generic logit | v0.5 |
| `bh:supportScore` | BehaviorInterpretation → `xsd:decimal` | Uncalibrated model support score, algorithm-dependent | v0.9 |
| `bh:reviewStatus` | BehaviorInterpretation → controlled status individual | proposed/reviewed/accepted/rejected; semantics and range pending | v0.5 |
| `prov:wasDerivedFrom` | `prov:Entity` → `prov:Entity` | Evidence derivation, datasets or earlier result records | v0.4+ |
| `prov:wasGeneratedBy` | `prov:Entity` → `prov:Activity` | Processing/segmentation/inference provenance | v0.4+ |

**Open-world discipline:** A broad `rdfs:domain` on a property is an *inference commitment*. It does not validate that the subject has the intended type; it often infers the intended type. Do not use OWL domain/range as substitutes for SHACL closed-world data checks. Use these domains/ranges only after verifying every intended usage path; avoid blanket `owl:FunctionalProperty` or exact cardinality axioms until identity models stabilize.

**Non-conflict:** Do not define domain-specific `bh:before`/`bh:after` as an unreviewed synonym of the OWL-Time relations. Link a sequence segment to its temporal extent instead.

## 6. Mapping to external vocabularies

| Ontology | Verified external terms (canonical namespace) | Recommended reuse | Non-equivalence / caution |
|---|---|---|---|
| SOSA/SSN | `sosa:Observation`, `sosa:Sensor`, `sosa:hasFeatureOfInterest`, `sosa:observedProperty`, `sosa:hasResult`, `sosa:phenomenonTime`, `sosa:resultTime` | Tie vessel feature measurements, their sensors, observation times, results | Observation ≠ SemanticBehavior; `resultTime` ≠ `phenomenonTime` |
| QUDT | `qudt:QuantityValue`, `qudt:numericValue`, `qudt:unit`; e.g. `unit:KN` | Represent numeric SOG/distance/angle with explicit units | QuantityValue does not by itself identify sensor, property, timestamp or quality |
| OWL-Time | `time:ProperInterval`, `time:Instant`, `time:intervalBefore`, `time:intervalAfter`, `time:intervalMeets` | Time extent and Allen-style interval semantics | TemporalUnit is **not** a ProperInterval |
| GeoSPARQL 1.1 | `geo:Feature`, `geo:Geometry`, `geo:hasGeometry`, spatial topological relations | EnvironmentSpace and spatial evidence | InteractionBehavior description is **not** equivalent to a spatial predicate or geometry |
| PROV-O | `prov:Entity`, `prov:Activity`, `prov:wasDerivedFrom`, `prov:wasGeneratedBy`, `prov:used` | Provenance of derived states and interpretations | Provenance link does not establish epistemic correctness |
| SKOS | `skos:Concept`, `skos:ConceptScheme`, `skos:prefLabel` | Provisional reusable behavior category vocabulary | Source Xiong class/subclass taxonomy not yet formally replaced by SKOS |
| BFO / CCO | **No approved concrete target class IRIs** | Keep candidate registry and draft alignment decision records | Do not use `owl:equivalentClass`, `owl:sameAs`, `rdfs:subClassOf` to BFO/CCO before pinned version + reviewed target IRIs |

**Version rule:** for implementation pin downloadable ontology artifacts/releases plus their import IRIs and checksums. External vocabularies being *referenced* is different from importing their full OWL axiomatizations. Some deployments may only need prefixes and curated profile files.

**Registry technical debt found during review:** existing `foundation:externalOntologyIRI` for BFO/CCO currently holds GitHub repository URLs, which are **not evidence of the authoritative OWL ontology IRIs**. Treat those strings as registry placeholders, do not use them in `owl:imports`, and create a corrective registry change after authoritative ontology/version IRI review.

## 7. BFO/CCO alignment decision candidates (not axioms)

| Local class | Plausible upper/mid-level interpretation | Reason to defer assertion |
|---|---|---|
| `bh:Trajectory` | Information content / dataset representation | Need to distinguish track record from movement process and data carrier |
| `bh:TemporalUnit` | Information segment / temporal-coverage description | A segment-record is not a BFO temporal region by identity |
| `bh:PhysicalBehavior` | Motion-state description about a process/quality | Information representation ≠ physical process/quality |
| `bh:InteractionBehavior` | Relation assertion / measurement-derived information artifact | Spatial relation itself and assertion about it have different identities |
| `bh:SemanticBehavior` | Behavioral classification content/result | Classifier output ≠ actual action, role or mental intention |
| `bh:EnvironmentSpace` | Geospatial region or feature depending referent | A chart object, real geographic feature and geometry representation are distinct |
| `maritime:Vessel` | Physical artifact/system | Need pin exact material object/system/function-bearer modeling |

No exact BFO/CCO IRI is approved in DCCR-03 draft. Mapping status for all rows: `candidate / draft`.

## 8. Proposed ontology shape commitments vs closed-world constraints

**OWL/RDFS (schema and inference):** declare class hierarchies and object property kinds; include carefully reviewed domain/range; do not collapse operational/behavioral taxonomies; no hard disjointness across PositionState, SpeedState, CourseState or relation dimensions; no automatic `SemanticBehavior`→`COLREGSituation` entailment; do not assert strong BFO/CCO mappings.

**SHACL (data validation, DCCR-04):** 

| ID | Condition to validate | Expected enforcement | Failure example |
|---|---|---|---|
| BH-V01 | Populated Trajectory has exactly one linked subject Vessel | `sh:minCount 1`, `sh:maxCount 1`, class | 0 or 2 vessels |
| BH-V02 | TemporalUnit has exactly one trajectory and temporal extent | SHACL property shapes | missing interval |
| BH-V03 | TemporalUnit order is consistent per trajectory | SPARQL-based SHACL / script | later unit starting earlier |
| BH-V04 | `intervalMeets` is used only for coincident boundaries | compare time values with explicit precision policy | interval declared meets despite gap |
| BH-V05 | A unit may have Position/Speed/Course simultaneously | positive multi-state test + OWL reasoner | accidental mutual exclusion |
| BH-V06 | Quantity values have relevant units | quantity-value `qudt:unit` and kind-specific unit checks | speed in seconds |
| BH-V07 | Relation description identifies vessel/reference/time and provenance | SHACL classes and counts | missing reference geometry |
| BH-V08 | Pre-recognition graph has zero `hasSemanticBehavior` target triples for target unit | Dataset named-graph SPARQL test | target label leakage |
| BH-V09 | Post-inference behavior has evidence and generation provenance | SHACL + provenance check | unsupported classification |
| BH-V10 | No unintended SemanticBehavior ⇒ Mode/COLREG entailments | OWL regression test with negative fixture | incorrect superclass/equivalence/property chain |

**Do not use OWL's open-world interpretation of `owl:cardinality` alone as proof that data with absent values fail.** Maintain positive *and* negative test fixtures. External standard imports and inferred graphs can affect SHACL evaluation: record the inference regime and whether types are asserted/inferred.

## 9. Non-normative illustrative RDF instance (not production ontology)

Example vocabulary choices require ratification under DCCR-03/DCCR-04. The external IRIs are standard, while `bh:` and `maritime:` are *reserved proposals*.

```turtle
@prefix bh:       <https://w3id.org/mass-ontology/behavior#> .
@prefix maritime: <https://w3id.org/mass-ontology/maritime#> .
@prefix ex:       <https://w3id.org/mass-ontology/examples/behavior#> .
@prefix time:     <http://www.w3.org/2006/time#> .
@prefix sosa:     <http://www.w3.org/ns/sosa/> .
@prefix qudt:     <http://qudt.org/schema/qudt/> .
@prefix unit:     <http://qudt.org/vocab/unit/> .
@prefix prov:     <http://www.w3.org/ns/prov#> .
@prefix xsd:      <http://www.w3.org/2001/XMLSchema#> .

ex:vessel07 a maritime:Vessel .
ex:trajectory17 a bh:Trajectory ;
    bh:ofVessel ex:vessel07 ;
    bh:hasTemporalUnit ex:u17 .

ex:u17 a bh:TemporalUnit ;
    bh:partOfTrajectory ex:trajectory17 ;
    bh:hasTemporalExtent ex:interval17 ;
    bh:hasPhysicalBehavior ex:speed17 .

ex:interval17 a time:ProperInterval ;
    time:hasBeginning ex:t0 ; time:hasEnd ex:t1 .
ex:t0 a time:Instant ;
    time:inXSDDateTimeStamp "2026-10-27T09:00:00Z"^^xsd:dateTimeStamp .
ex:t1 a time:Instant ;
    time:inXSDDateTimeStamp "2026-10-27T09:05:00Z"^^xsd:dateTimeStamp .

ex:speed17 a bh:SpeedState ;
    bh:supportedByObservation ex:observation17 ;
    bh:hasQuantityValue ex:sogValue17 ;
    prov:wasDerivedFrom ex:observation17 .

ex:sogValue17 a qudt:QuantityValue ;
    qudt:numericValue "5.0"^^xsd:decimal ;
    qudt:unit unit:KN .

ex:observation17 a sosa:Observation ;
    sosa:hasFeatureOfInterest ex:vessel07 ;
    sosa:observedProperty ex:SpeedOverGround ;
    sosa:resultTime "2026-10-27T09:00:01Z"^^xsd:dateTime .
```

The example **does not** assert `bh:hasSemanticBehavior`. It belongs to a *pre-inference* dataset. A future **post-inference** graph will introduce separate inference records and their provenance. Example values are synthetic.

## 10. First ontology competency question mapping

| BH-CQ | Planned query target | Earliest test |
|---|---|---|
| 01 | vessel, trajectory, source observations, times | v0.4 |
| 02 | temporal unit, explicit time extent and physical state descriptions | v0.4 |
| 03 | derived physical values, QUDT units, supporting observations | v0.4 |
| 04 | environmental reference, direction/distance/topology relations | v0.5 |
| 05 | consecutive units and correctly inferred interval ordering/meets | v0.5 |
| 06 | candidate semantic classification, activity, evidence, model version | v0.5/v0.9 |
| 07 | absence of candidate labels in pre-inference graph | v0.5/v0.9 |
| 08 | independence of observed motion and operating mode | v0.5 |
| 09 | independent evidence for COLREG class and risk assessment | v0.5/v0.7 |
| 10 | alternative candidate labels and scores on a unit | v0.5/v0.9 |

**Namespace policy:** BH-CQ-xx is distinct from SysML Kernel `SK-CQ01…SK-CQ12` and the existing MASS Ontology `CQ-01…CQ-14`.

## 11. Approved design directions and open implementation questions

| Decision | Design disposition | Status after approval |
|---|---|---|
| DCCR-03-D01 | Reserve `bh:` IRI and behavior module | APPROVED AS DESIGN |
| DCCR-03-D02 | Introduce local `BehaviorInformationEntity` / `BehaviorDescription` intermediates | APPROVED AS DESIGN |
| DCCR-03-D03 | Introduce generic `maritime:Vessel`; specialize MASS and target ship | APPROVED AS DESIGN — requires compatibility CQ regression |
| DCCR-03-D04 | `TemporalUnit` is **not** `time:ProperInterval`; link via temporal-extent property | APPROVED AS DESIGN, consistent with DCCR-02 |
| DCCR-03-D05 | Separate `SemanticBehavior` information entity from `BehaviorInterpretation` result record | APPROVED AS DESIGN |
| DCCR-03-D06 | Use SKOS behavior categories for first implementation while preserving the source class-subclass mapping as documentation | OPEN — category modeling alternative remains |
| DCCR-03-D07 | External SOSA/SSN, QUDT, OWL-Time, GeoSPARQL, PROV-O terms referenced by pinned version/profile | APPROVED AS DESIGN; imports deferred |
| DCCR-03-D08 | No direct BFO/CCO axioms or concrete target IRI claims | APPROVED SAFEGUARD |
| DCCR-03-D09 | Pre/post named graph separation and provenance are part of classification contract | APPROVED AS DESIGN |
| DCCR-03-D10 | Make missing measurements/data gaps explicit; do not fabricate temporal continuity | APPROVED AS DESIGN |

**Outstanding:** precision policy for temporal interval adjacency; segmentation algorithm stability/version identifiers; whether a single observation is represented by its own `TemporalUnit` or by an observation with a `time:Instant`; behavior category SKOS vs OWL subclass decision; confidence calibration, competing hypotheses and acceptance criteria; exact external ontology release checksums; authoritative BFO/CCO source IRI and pinned mappings; re-use of an existing general maritime vessel term vs new local `maritime:Vessel`.

## 12. Acceptance / release sequence

1. DCCR-03 **APPROVED on 2026-10-27** as a design contract; this approval does not authorize unreviewed production TTL merges.
2. DCCR-04 delivers exact SHACL shapes, `BH-CQ`, positive/negative RDF fixtures, automated tests, and expected counts/results.
3. v0.4 branch introduces minimal observation/measurement/time/trajectory/physical-state subset; no dependency on unimplemented GeoSPARQL or recognition algorithm.
4. v0.5 branch adds spatial-interaction/semantic-behavior schema and applies separate tests for graph contamination and inappropriate COLREG inferences.
5. All existing `make catalog`, `make validate`, `make cq` remain green; `BH-CQ` gets its own namespace and tests.
6. Never modify immutable `MASSKernel_v1.0.sysml`; new integration uses versioned domain library modules.

**Review verdict:** **DCCR-03 APPROVED (DESIGN LEVEL), 2026-10-27**. The design direction is accepted; outstanding choices explicitly marked OPEN remain unresolved. No production OWL/Turtle, SHACL, published mappings, or immutable SysML baseline changed by this approval.

## 13. Official standard references

- Xiong et al. source: https://doi.org/10.3390/jmse14191859
- W3C SOSA/SSN: https://www.w3.org/TR/vocab-ssn-2023/
- W3C OWL-Time: https://www.w3.org/TR/owl-time/
- QUDT: https://www.qudt.org/ ; schema vocabulary base URI `http://qudt.org/schema/qudt/`
- OGC GeoSPARQL 1.1: https://www.ogc.org/standards/geosparql/
- W3C PROV-O: https://www.w3.org/TR/prov-o/
- W3C SKOS: https://www.w3.org/TR/skos-reference/
