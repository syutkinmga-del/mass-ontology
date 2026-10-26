# DCCR-01 — Domain Concept Completeness Review
## Xiong et al. (2026) → MASS Semantic Kernel v1.0 → MASS Ontology v0.3.0-dev

**Date:** 2026-10-26  
**Approval date:** 2026-10-26  
**Status:** APPROVED — DCCR-01 concept inventory and planning dispositions. Formal OWL mappings remain unapproved pending DCCR-02/DCCR-03.  
**Source paper:** Xiong, Wang, Wu, Chen, *Ontology-Guided Multimodal Large Language Model for Semantic Recognition of Ship Navigation Behaviors*, *Journal of Marine Science and Engineering*, 14(19), 1859, 2026. https://doi.org/10.3390/jmse14191859  
**Source ontology coverage:** Table 1 (schema) and Table 3 (experimental behavior classes).  
**Compared baselines:** `MASSKernel_v1.0.sysml` (uploaded); GitHub `syutkinmga-del/mass-ontology` default-branch `common-core.ttl`, `mass-core.ttl`, `navigation-situation.ttl`, `foundation-alignment.ttl` (read 2026-10-26).  
**Scope:** domain concept completeness only. Does not assert BFO/CCO equivalences, perform full MASS-SK/OWL gap analysis, or change production files.

### Classification rules
- **Existing** — semantically appropriate term already available.
- **Broader** — only a more general, provisionally related term is available.
- **Narrower** — available term refers to a proper subset or more specialized scope.
- **Missing** — no semantically adequate term is implemented.
- **Algorithm-specific** — artifact or control of the experimental recognition method, not required as a core domain ontology class.
Decisions: **Reuse / Specialize / Add / Defer / Reject**. `Missing` is not automatically a defect in a deliberately scoped baseline.

## A. Schema concept matrix — all 13 principal classes in Xiong Table 1

| ID | Xiong concept | Closest MASS-SK / OWL concept | Status | Decision | Target release / semantic guardrail |
|---|---|---|---|---|---|
| C01 | `Vessel` | MASS-SK `Vessel`; OWL `mass:MASSVessel`, `nav:OwnShip` (MASS-specific) | **Existing** (SK); OWL only **Narrower** | **Reuse** | Reuse SK Vessel; plan a general maritime `Vessel` in maritime module; do not treat every vessel as MASS |
| C02 | `Trajectory` | No time-ordered trajectory class; `nav:EncounterSituation` is not a trajectory | **Missing** | **Add** | v0.4 minimal; v0.5 spatial geometry; distinguishes track from a voyage/route |
| C03 | `TemporalUnit` | Operational snapshots/contexts are not equivalent to trajectory intervals | **Missing** | **Add** | v0.4 interval/time boundaries; consider OWL-Time; segment only by explicit criteria |
| C04 | `PhysicalBehavior` | `common:Process` is broadly related but not a confirmed supertype for observation-derived state descriptions | **Missing** | **Add** | v0.4; distinguish actual motion process from evidence or descriptive state |
| C05 | `PositionState` | No corresponding behavior-state class | **Missing** | **Add** | v0.4; recorded/derived position and geometric attributes |
| C06 | `SpeedState` | No corresponding behavior-state class | **Missing** | **Add** | v0.4; support SOG level/variation; units via QUDT |
| C07 | `CourseState` | No corresponding behavior-state class | **Missing** | **Add** | v0.4; COG/change/turning; distinguish heading from COG |
| C08 | `InteractionBehavior` | `nav:EncounterSituation` is related to vessel encounters, but is not equivalent to vessel–environment spatial relations | **Missing** | **Add** | v0.5; do not equate an encounter occurrence with a relation description |
| C09 | `DirectionRelation` | No dedicated spatial relation observation/entity | **Missing** | **Add** | v0.5; qualify subject, reference object, interval, frame of reference |
| C10 | `DistanceRelation` | `nav:hasCPA` is a predicted encounter metric, not a general distance relation | **Missing** | **Add** | v0.5; actual separation ≠ CPA/DCPA |
| C11 | `TopologyRelation` | No GeoSPARQL relation implementation | **Missing** | **Add** | v0.5; reuse GeoSPARQL vocab/semantics rather than invent duplicates |
| C12 | `SemanticBehavior` | `mass:OperationalMode`, `common:OperationalState`, `nav:Maneuver` have distinct meanings | **Missing** | **Add** | Minimal class/relationship schema by v0.5; instances only after interpretation |
| C13 | `EnvironmentSpace` | ODD/OE are operational specifications, not environmental geometry | **Missing** | **Add** | v0.5; GeoSPARQL Feature/Geometry candidate (pending exact modeling) |

**Naming:** the source code/name is `InteractionBehavior` (not `InteractiveBehavior`, which occurs in narrative description).  
**Semantic warning:** `PhysicalBehavior` / `PositionState` are author-defined descriptive layers, not automatically BFO processes or qualities. External BFO/CCO mapping must remain `draft` pending clarification.

## B. Application-specific semantic classes — five experimental labels from Table 3

| ID | Behavior class | Status | Decision | Why |
|---|---|---|---|---|
| A01 | `Transit` | **Missing** | **Defer** | Relevant to harbor-traffic profile; define criteria before hard-coding universal behavior hierarchy |
| A02 | `Manoeuvring` | **Missing** | **Defer** | Not automatically `nav:Maneuver`: interval behavior label ≠ individual maneuver occurrence/command |
| A03 | `Waiting` | **Missing** | **Defer** | Low speed alone cannot distinguish waiting from anchor/berth |
| A04 | `AtAnchor` | **Missing** | **Defer** | Needs contextual or corroborating evidence; AIS low-speed is insufficient proof |
| A05 | `Moored` | **Missing** | **Defer** | Spatially near a berth ≠ verified mooring state |

These five are task-dependent labels. They are **domain behavior classes in an experimental application**, not purely MLLM-architecture concepts; they are not all to be rejected as `Algorithm-specific`. Decide during behavior taxonomy review.

## C. Object-relation matrix — all 9 relations in Xiong Table 1

| ID | Source relation (domain → range) | Existing comparison | Status | Decision | Implementation note |
|---|---|---|---|---|---|
| R01 | `hasTrajectory`: Vessel → Trajectory | No equivalent; MASS has mode/communication associations | **Missing** | **Add** | v0.4; vessel track association |
| R02 | `hasTemporalUnit`: Trajectory → TemporalUnit | No interval grouping | **Missing** | **Add** | v0.4; preserve order, bounds and source provenance |
| R03 | `hasPhysicalBehavior`: TemporalUnit → PhysicalBehavior | Snapshots are not this relation | **Missing** | **Add** | v0.4; permit multiple concurrent dimension states |
| R04 | `hasInteractionBehavior`: TemporalUnit → InteractionBehavior | `nav:hasTargetShip` is encounter participation, not spatial interaction | **Missing** | **Add** | v0.5; reference appropriate participants |
| R05 | `referencesSpace`: InteractionBehavior → EnvironmentSpace | ODD/OE references are not spatial geometries | **Missing** | **Add** | v0.5; valid reference environmental geometry |
| R06 | `hasSemanticBehavior`: TemporalUnit → SemanticBehavior | No recognition-result link | **Missing** | **Add** | v0.5 schema; **do not populate pre-inference graph** |
| R07 | `before`: TemporalUnit → TemporalUnit | No temporal relation module | **Missing** | **Reuse** | v0.5: prefer vetted OWL-Time interval relation; often derive from ordered indices |
| R08 | `after`: TemporalUnit → TemporalUnit | No temporal relation module | **Missing** | **Reuse** | v0.5: OWL-Time or derived inverse ordering |
| R09 | `meets`: TemporalUnit → TemporalUnit | No temporal adjacency module | **Missing** | **Reuse** | v0.5: OWL-Time intervalMeets candidate; assert only for truly contiguous intervals |

**Source distinction:** article materializes `meets` for adjacent units; nonadjacent `before`/`after` may be derived from unit indices/reachability instead of stored as every possible triple.

## D. Descriptive-property groups (source P) — completeness check

| Group from paper | Current status | Decision / standard |
|---|---|---|
| Spatial-position: position, displacement, path scale, geometry/extent | Missing at behavior layer | Add observation-derived quantities, later GeoSPARQL geometries |
| Speed: level, change, stability/statistics | Missing | Add derived SpeedState attributes, QUDT quantities |
| Course: COG, change, turning, stability | Missing | Add CourseState attributes; distinguish heading, COG and bearing |
| Spatial relation: direction, distance, topology | Missing | Add v0.5; measurements and GeoSPARQL |
| EnvironmentSpace: type and geometry | Missing | Add v0.5 via spatial feature/geometry model |
| TemporalUnit: start/end | Missing | Add v0.4, consider OWL-Time |

Unlike these groups, the existing `nav:hasCPA` and `nav:hasTCPA` do not constitute a general behavior measurement layer and have no units in current v0.3.0-dev.

## E. Axiom, constraint and workflow review (source A)

| Source commitment | Treatment | Recommended verification |
|---|---|---|
| Three-layer behavior taxonomy, subclasses | Add/specialize under domain module | Hierarchy and expected types in OWL |
| Domain and range for object relations | Add | RDFS/OWL schema plus SHACL class/path checks |
| Concurrent Position/Speed/Course and Direction/Distance/Topology dimensions | Preserve | Do not assert `owl:disjointWith` across these dimensions; positive multi-instance SHACL fixture |
| Temporal order/adjacency | Reuse temporal vocabulary | Check start/end, within one trajectory, strict order, true adjacency; distinguish missing AIS time gaps |
| Physical/spatial interaction and semantic-label consistency | Defer domain-specific rules | Acceptance review of SHACL/SPARQL/rules and invalid fixtures |
| Temporal segmentation on changes of categorical states/relations | Algorithm-specific data construction | Pipeline test; not an OWL class axiom |
| SemanticBehavior only after recognition | Ontology contract + pipeline invariant | Pre-inference graph contains no result `hasSemanticBehavior` triples; post-inference includes evidence and method |
| MLLM prompt, local-neighborhood radius `h`, trajectory-motion image, class-token output | Algorithm-specific | **Defer** to v0.9.0 prototype, not part of core schema |

## F. Proposed additions *not asserted by Xiong et al. as core schema*

For auditable recognition, consider:
- `BehaviorInterpretation` / `BehaviorAssessment` with candidate class, confidence, evidence, inference timestamp and algorithm provenance;
- `VesselVesselInteraction` extension to the paper's mainly vessel–environment scope;
- separation of actual navigation motion, derived state-description and inferred behavioral label;
- rules against classifying COLREG applicability solely from behavior class or geometry.

These are **MASS design proposals**, not source-extracted concepts. Assess in a separate design decision.

## G. Candidate behavior competency questions

| ID | Question | Earliest target |
|---|---|---|
| BH-CQ-01 | Which AIS/radar observations describe a vessel during a specified time interval? | v0.4 |
| BH-CQ-02 | Which physical states and their measurement units belong to this TemporalUnit? | v0.4 |
| BH-CQ-03 | Which reference spaces and spatial relations apply to the vessel during this interval? | v0.5 |
| BH-CQ-04 | Which adjacent TemporalUnits express an interaction transition, and is temporal adjacency valid? | v0.5 |
| BH-CQ-05 | Which inferred SemanticBehavior is linked to an interval, and from which evidence? | v0.5 / v0.9 |
| BH-CQ-06 | Can the pre-recognition graph be shown not to contain the target labels? | v0.5 / v0.9 |
| BH-CQ-07 | How does a recognized behavior relate to, but remain distinct from, ModeOfOperation and OperationalCondition? | v0.5 |
| BH-CQ-08 | Is a COLREGSituation interpretation independently justified instead of inferred directly from a high-level behavior label? | v0.5 |

Prefix **BH-CQ** avoids confusion between SysML Kernel CQ1–12 and existing OWL `CQ-01` through `CQ-14`.

## H. Proposed modular roadmap

- **v0.3.0**: preserve released foundation-alignment baseline; record DCCR only. Do not edit `MASSKernel_v1.0.sysml`.
- **v0.4.0 SOSA/SSN + QUDT**: implement observations and measurement values; start Vessel–Trajectory–TemporalUnit and PhysicalBehavior scaffold with unit/time checks.
- **v0.5.0 GeoSPARQL + COLREGs**: implement EnvironmentSpace, spatial relations, InteractionBehavior, temporal adjacency, basic SemanticBehavior classification schema and bridge to encounter/safety.
- **v0.6–v0.8**: connect behavior evidence to ROC/VTS and safety/function models without redefining existing modes/assignments.
- **v0.9.0**: experimental MLLM recognition pipeline, offline/online validation boundary and provenance-driven acceptance.

## I. Proposed DCCR acceptance gates

1. Confirm all **13** Table 1 classes, **9** Table 1 object relations, and **5** Table 3 behavior labels were considered.
2. Separate `Source concept`, `Proposed MASS entity`, `Mapping status`, `Decision`, `Release`, and `Evidence`.
3. No premature `owl:equivalentClass` or BFO/CCO alignment.
4. No conflation of SemanticBehavior / ModeOfOperation / OperationalCondition / COLREGSituation.
5. No use of post-inference labels as evidence in a pre-inference graph.
6. At least one valid and one invalid fixture for observation units, temporal intervals and relation references.
7. Accept/reject class candidates before committing the behavior schema.

**Decision:** **DCCR-01 APPROVED** as the controlled concept inventory and preliminary disposition baseline. Next: DCCR-02 semantic design review for `Trajectory`, `TemporalUnit`, `PhysicalBehavior`, `InteractionBehavior` and `SemanticBehavior`. This approval does not authorize direct insertion of new production TTL classes or `owl:equivalentClass` mappings without subsequent design and validation.

