# DCCR-02 — Semantic Design Review: Ship Behavior Ontology
**Project:** MASS Ontology Stack / MASS Domain Library  
**Review date:** 2026-10-26  
**Approval date:** 2026-10-26  
**Status:** APPROVED — semantic design principles and planning decisions only; no production OWL or BFO/CCO mapping approved  
**Input decision:** `DCCR-01-xiong-ship-behavior-review.md`, APPROVED 2026-10-26  
**Reference baselines:** immutable `MASSKernel_v1.0.sysml` (MASS-SK-1.0); MASS Ontology v0.3.0-dev (GitHub source read 2026-10-26)  
**Source article:** Yu Xiong et al., *Ontology-Guided Multimodal Large Language Model for Semantic Recognition of Ship Navigation Behaviors*, *J. Mar. Sci. Eng.* 2026, 14(19), 1859, https://doi.org/10.3390/jmse14191859

## 0. Scope and provenance of design choices

**Directly from Xiong et al.** The ontology has `Vessel`, `Trajectory`, `TemporalUnit`, `EnvironmentSpace`; three layers `PhysicalBehavior`, `InteractionBehavior`, `SemanticBehavior`; physical subclasses `PositionState`, `SpeedState`, `CourseState`; interaction subclasses `DirectionRelation`, `DistanceRelation`, `TopologyRelation`; relations `hasTrajectory`, `hasTemporalUnit`, `hasPhysicalBehavior`, `hasInteractionBehavior`, `referencesSpace`, `hasSemanticBehavior`, `before`, `after`, `meets`. A TemporalUnit covers a time interval with unchanged *discrete* state/relation category, even while continuous values vary. `SemanticBehavior` is NOT inserted into the pre-inference graph; it is added following recognition. Temporal transitions (e.g., entering/leaving) are derived by comparing relations across successive units.

**MASS-specific proposals in this review**, NOT claims made by Xiong: distinguish a real-world motion process from observation-derived information descriptions; represent temporal segments separately from OWL-Time intervals; preserve observation and model provenance, uncertainty, classification status; add explicit behavioral assessment provenance; optionally represent human-reviewed classifications; extend spatial interactions to vessel–vessel encounters; make prevention of label leakage an explicit validation gate; decouple safety/COLREG classification from behavior labels.

**Existing assets:** `MASSKernel_v1.0.sysml` defines `Vessel`, `MaritimeAutonomousSurfaceShip`, `ModeOfOperation`, `OperationalCondition`, `OperationalModeSnapshot`, `OperationalFunctionSnapshot`, `COLREGSituation`, `CollisionRiskAssessment`, `SafetyConstraint`, etc. Current MASS OWL includes `common:InformationArtifact`, `common:Process`, `common:OperationalSituation`, `mass:MASSVessel`, `mass:OperationalMode`, `nav:EncounterSituation`, `nav:Maneuver`, and scalar `nav:hasCPA` / `nav:hasTCPA`. Neither baseline has already implemented the five reviewed behavior concepts. Note `common:InformationArtifact` is a **local** category still awaiting BFO/CCO alignment.

**Identity rule:** Physical occurrence, an information record of that occurrence, a state/relation description, and an inferred classification are not the same individual by default.

## 1. Five concept decision records

### DCCR-02-D01 — `Trajectory`

- **Source meaning:** Time-ordered sequence of trajectory observations belonging to a particular vessel over a defined period.
- **Proposed definition:** A versioned information representation of an observed/constructed, time-ordered history of one vessel's locations and motion measurements in a stated temporal coverage. A trajectory is **not** a route plan, voyage, actual movement process, or GeoSPARQL geometry.
- **Ontological category:** provisional `InformationArtifact` or dataset/sequence description; **not** `common:Process`. Exact BFO/CCO target unapproved.
- **Identity:** unique trajectory record/dataset version + subject vessel + source dataset/segmentation run; multiple trajectories of same vessel across windows are allowed.
- **Relations:** `ofVessel` (exactly one in a closed-world dataset), `hasTemporalUnit` (0..* generally; >=1 for validated populated trajectory), `prov:wasDerivedFrom` observation collections, optional geometry representation.
- **Constraints:** units in time order, interval coverage within trajectory, no required continuous positions when AIS gaps exist; track segment and predicted route are distinct.
- **Decision:** **ADD / proposed for v0.4**.
- **Do not do:** `Trajectory owl:equivalentClass geo:Geometry` or `Trajectory rdfs:subClassOf common:Process` without a new review.

### DCCR-02-D02 — `TemporalUnit`

- **Source meaning:** A segmented element of one trajectory, whose discrete physical-state and/or spatial-relation category combination remains unchanged; continuous values may vary.
- **Proposed definition:** A versioned information-segment individual organizing descriptions and observations for one temporal extent of one trajectory. Its **time extent** is a distinct `time:Interval`/`time:ProperInterval` individual (candidate OWL-Time mapping).
- **Ontological category:** segment/record (`InformationArtifact` candidate); **NOT** an instant, interval, or `OperationalModeSnapshot` itself. A snapshot may refer to a time within that unit.
- **Identity:** trajectory + segmentation method/version + segment index or stable interval ID.
- **Relations:** `partOfTrajectory` exactly one in the MVP dataset; `hasTemporalExtent` exactly one; `hasPhysicalBehavior` multiple; `hasInteractionBehavior` multiple; `hasSemanticBehavior` only after inference; `nextTemporalUnit` optional for ordered adjacency.
- **Constraints:** a segmentation-specific sequence index must be unique within trajectory; start < end for interval-valued units; no overlaps among disjoint segmentation units of the same track; `nextTemporalUnit` links only successive units. An AIS gap must not be labelled as continuous evidence.
- **Important correction to DCCR-01:** W3C `time:intervalBefore`, `time:intervalAfter`, `time:intervalMeets` have **time:ProperInterval** domain and range. Because our `TemporalUnit` is a segment record rather than a literal temporal interval, use these OWL-Time relations on associated **interval individuals**, **not directly on TemporalUnit records**. Otherwise RDFS/OWL domain axioms may mistakenly entail that the segment record is a `time:ProperInterval`. Keep an explicit `nextTemporalUnit` if needed.
- **Decision:** **ADD / proposed for v0.4**; temporal alignment in DCCR-03.

### DCCR-02-D03 — `PhysicalBehavior`

- **Source meaning:** Physical behavior describes the vessel's own motion, structured into `PositionState`, `SpeedState`, `CourseState`. The source describes these as information dimensions generated from measured motion.
- **Proposed definition:** A typed, evidence-bearing description of one dimension of a vessel's observed or derived movement state within a TemporalUnit, optionally containing aggregated statistics.
- **Ontological category:** local descriptor / information entity **candidate**, not asserted as a BFO `process` or `quality` in this phase. The underlying vessel motion is a **different real process** (`VesselMotionOccurrence` future optional class).
- **Classification:** `PositionState`, `SpeedState`, `CourseState` specialize the descriptive `PhysicalBehavior`. They are *concurrent dimensions*, not disjoint alternative operational modes.
- **Relations:** each descriptor concerns a vessel/unit, `derivedFromObservation`, `observedProperty`, `hasQuantityValue` QUDT or `hasResult` when aligned to SOSA/SSN; possible `prov:wasGeneratedBy`.
- **Constraints:** speed has correct velocity unit, course/bearing has angular unit; distinguish heading from COG and instantaneous velocity from interval summary; retain observation vs estimate/calculation distinction.
- **Decision:** **ADD / proposed for v0.4**; **DEFER** exact upper-ontology superclass to DCCR-03.
- **Do not do:** `PhysicalBehavior owl:equivalentClass common:Process` or model PositionState, SpeedState, CourseState as three mutually exclusive states.

### DCCR-02-D04 — `InteractionBehavior`

- **Source meaning:** Vessel–environment spatial relationships by direction, distance and topology; changes between adjacent TemporalUnits yield approaching, moving away, entering, leaving.
- **Proposed definition:** A temporally scoped information characterization of a spatial relation between a subject vessel and an identified reference object (usually `EnvironmentSpace` in Xiong), computed from observed location and spatial reference data.
- **Ontological category:** contextualized n-ary relation description / computed information entity; **not the GeoSPARQL relation predicate itself**, **not** a `COLREGSituation`.
- **Specializations:** `DirectionRelation`, `DistanceRelation`, `TopologyRelation` as *relation descriptions* (per source hierarchy) with subject, reference, unit and optional value/qualitative category. They may coexist.
- **Relations:** `hasSubjectVessel`, `referencesSpace`, `appliesToTemporalUnit`, `hasReferenceFrame`, `hasRelationValue`, `wasDerivedFrom`.
- **Constraints:** exactly one subject vessel and reference object per *relation assertion* in the MVP; time context required; measured distance ≠ future CPA/DCPA; geo topological predicate inference needs geometry provenance and CRS; explicit local/true/magnetic direction distinction if used.
- **Future extension:** `VesselVesselInteraction` with reference vessel, NOT automatically equated to encounter/COLREG semantic types. Not a class asserted by Xiong's core ontology.
- **Decision:** **ADD / proposed for v0.5**. GeoSPARQL alignment in DCCR-03.

### DCCR-02-D05 — `SemanticBehavior`

- **Source meaning:** High-level interpretation inferred from PhysicalBehavior, InteractionBehavior, temporal and navigation context. Xiong defines `SemanticBehavior` subclasses for target behavior classes (in harbor setting: Transit, Manoeuvring, Waiting, AtAnchor, Moored).
- **Proposed definition:** A typed *inferred semantic characterization* of vessel behavior during a specific TemporalUnit, created only after a recognition/assessment activity, with supporting evidence and provenance.
- **Ontological category:** a semantic **description / classification assertion** in the information layer; the real behavior/action/process is modeled independently if necessary. Exact OWL/BFO/CCO alignment remains draft.
- **OWL modeling alternatives:**
  - A: Preserve the paper's superclass `SemanticBehavior` with subtype classes such as `Transit` *when their definitions are approved*; each inferred result is an **individual** of the appropriate subtype linked from `TemporalUnit`.
  - B: Use one `BehaviorInterpretation` individual with a property to a `skos:Concept` category; easier for taxonomy revision and model outputs but diverges from the paper's literal class/subclass strategy.
  - **Recommendation:** dual structure at the information layer if justified: `SemanticBehavior` result individual and provenance-bearing `BehaviorInterpretation`/assessment record; behavior category may be an OWL class or SKOS concept depending on the downstream reasoning requirement. Do not make unapproved classes both OWL individuals and OWL classes without explicit punning policy.
- **Relations:** `hasSemanticBehavior` only in a separate post-inference graph; `prov:wasDerivedFrom` evidence; `prov:wasGeneratedBy` recognition activity; optional confidence and model version. Attribution of result to a time unit must be explicit.
- **Constraints:** no semantic answer label in the pre-inference evidence graph of the same run; possible concurrent or conflicting candidate labels must be recorded as **hypotheses**, not silently cast to validated truths; human-reviewed vs inferred status separate. Do not automatically infer `ModeOfOperation`, `OperationalCondition` or COLREG rule applicability from the high-level behavior label.
- **Decision:** **ADD schema / proposed for v0.5**; **DEFER label taxonomy acceptance** until a behavior taxonomy review and **DEFER MLLM algorithm** until v0.9.

## 2. Semantic-level separation and interfaces

| Real-world or system concept | Representation in DCCR-02 | Boundary |
|---|---|---|
| Vessel motion, maneuver execution | Actual occurrence / future `VesselMotionOccurrence` | Not equal to `Trajectory` / `PhysicalBehavior` record |
| AIS sensor process | `sosa:Observation` and result | Observation ≠ factually confirmed intent |
| Versioned movement record | `Trajectory` | Not itself a voyage or route plan |
| Interval-level dataset segment | `TemporalUnit` | Not identical to `time:ProperInterval` |
| Position, speed, course interpretation | `PhysicalBehavior` subclasses | Not automatically SysML OperationalCondition |
| Spatial relation to port zone or another vessel | `InteractionBehavior` subclasses | Not automatically `nav:EncounterSituation` |
| Inferred type of navigation activity | `SemanticBehavior`/BehaviorInterpretation | Not `ModeOfOperation`, not `COLREGSituation`, not direct safety determination |
| Navigational encounter | `nav:EncounterSituation`; SysML `COLREGSituation` | Separate maritime operational context subject to rule evidence |
| Operational mode and condition | MASS-SK `ModeOfOperation`, `OperationalCondition`; `mass:OperationalMode` | Internal function/authority/ODD semantics |
| Risk assessment result | SysML `CollisionRiskResult`, and future OWL | Inference from justified evidence; not distance relation alone |

**Proposed disjointness:** no global `owl:disjointWith` commitments yet. Definitional non-equivalence should be recorded as design rule first; BFO/CCO final upper categories may later permit stronger formal constraints. In particular, avoid casually declaring disjointness among physical/interaction dimensions that naturally co-occur.

## 3. Relations: semantic typing recommendations

| Relation | Proposed subject → object | Modeling decision |
|---|---|---|
| `hasTrajectory` | Vessel → Trajectory | Keep; link to general vessel concept (not MASS-only) |
| `hasTemporalUnit` | Trajectory → TemporalUnit | Keep; ordering is separate from membership |
| `hasPhysicalBehavior` | TemporalUnit → PhysicalBehavior | Keep; multiple states permitted |
| `hasInteractionBehavior` | TemporalUnit → InteractionBehavior | Keep; different reference spaces/relations permitted |
| `referencesSpace` | InteractionBehavior → EnvironmentSpace | Keep; `EnvironmentSpace` is a spatial feature, not ODD |
| `hasSemanticBehavior` | TemporalUnit → SemanticBehavior instance | Use only post-recognition |
| `before` / `after` | Temporal extents via `time:intervalBefore` / `time:intervalAfter` | Map **time extent** to standard relations; not segment records |
| `meets` | Temporal extents via `time:intervalMeets` | Require end(A) == start(B) (with chosen temporal precision); absence of gaps |
| `nextTemporalUnit` (**new**) | TemporalUnit → TemporalUnit | Local sequence organization property, independent of intervalMeets |
| `wasDerivedFrom` (**new/reuse**) | Info record → source observation / dataset | PROV-O provenance |
| `wasGeneratedBy` (**new/reuse**) | Classification record → recognition activity | PROV-O provenance |

Source relation names and directions remain traceable. Proposed extra relationships are not misattributed to the source.

## 4. Candidate OWL information-layer hierarchy (design sketch only)

```text
Local common:InformationArtifact                 [DRAFT future subclass assertions]
  ├── Trajectory
  ├── TemporalUnit
  ├── PhysicalBehavior
  │     ├── PositionState
  │     ├── SpeedState
  │     └── CourseState
  ├── InteractionBehavior
  │     ├── DirectionRelation
  │     ├── DistanceRelation
  │     └── TopologyRelation
  └── SemanticBehavior
        └── (domain-approved behavior subclasses)

Real-world activity/occurrence (separate, optional)
  └── VesselMotionOccurrence : ... Process candidate [DRAFT]
```

This is an **information-representation** interpretation of the paper's schema, not proof that all source classes belong under BFO/CCO Information Content Entity. Final alignments require DCCR-03 and authoritative target IRIs.

## 5. Temporal and observation discipline

- Do not use OWL-Time `time:intervalBefore`, `time:intervalAfter`, or `time:intervalMeets` directly between `TemporalUnit` **record individuals** when they are not instances of `time:ProperInterval`. Their domain/range are proper intervals.
- Associate `TemporalUnit` with time-extent interval I via an explicitly defined property; the time ontology class is used for I.
- For non-zero segments, require `start < end`; singleton AIS observations are point-time events and should not be forcibly typed as proper intervals.
- Select precision/tolerance policy for interval adjacency. `time:intervalMeets` is *exact* boundary coincidence, not merely consecutive sample indices; AIS data gaps need explicit recording.
- Separate `sosa:phenomenonTime` (when observation applies) from `sosa:resultTime` (when result is generated). For AIS reception/processing, message acquisition/ingestion time may differ again.
- Keep provenance of aggregate/calculated state properties. E.g., speed stability is *derived* from multiple SOG measurements and is not directly observed as a single sensor value.
- Segment construction depends on categorical-state/relation changes in Xiong's experiment. In v0.4 it is a **pipeline/data construction rule**, not an intrinsic universal property of all trajectories.
- No use of future samples for online causal behavioral recognition; Xiong's reported technique is primarily offline/non-causal.

Authoritative references:
- W3C OWL-Time: https://www.w3.org/TR/owl-time/
- W3C SOSA/SSN (2023 edition): https://www.w3.org/TR/vocab-ssn-2023/
- QUDT Schema: https://www.qudt.org/doc/2026/01/DOC_SCHEMA-QUDT.html
- OGC GeoSPARQL 1.1: https://docs.ogc.org/is/22-047r1/22-047r1.html
- W3C PROV-O: https://www.w3.org/TR/prov-o/

## 6. Worked semantic example (conceptual, not production RDF)

Observation at t1: SOG 5 knots, COG 085 degrees, vessel located outside harbor-basin zone.
Observation at t2: SOG 3 knots, COG 120 degrees, increasing curvature.
An algorithm creates TemporalUnit U17 that aggregates interval observations and assigns PositionState P17, SpeedState S17 and CourseState C17.
A spatial calculation assigns TopologyRelation TR17 (outside basin) and DistanceRelation DR17.
After inferencing, a separate classification record B17 claims `Manoeuvring` with evidence {S17, C17, TR17, DR17}; confidence=0.72, status=provisional, algorithm version=... .
None of this on its own determines a `COLREGSituation`, operational authority, or safety-rule applicability.

**Source/interpretation distinction:** observed SOG/COG values are hypothetical. `Manoeuvring` is a candidate interpretation, not ground truth. `0.72` is an arbitrary illustrative confidence value, not from Xiong's dataset.

## 7. Proposed verification contract for DCCR-04

| ID | Rule / test | Positive fixture | Negative fixture |
|---|---|---|---|
| BH-V01 | Trajectory has exactly one subject vessel *in curated dataset* | 1 vessel | 0 or 2 vessel links |
| BH-V02 | Each populated TemporalUnit has a reference trajectory and interval | Both present | No temporal extent |
| BH-V03 | Distinct consecutive units have strictly ordered interval boundaries | U1.end ≤ U2.start | U2.start < U1.start |
| BH-V04 | `time:intervalMeets` asserted only for touching intervals | end(U1.interval) = start(U2.interval) | Explicit AIS coverage gap |
| BH-V05 | PhysicalBehavior supports simultaneous position/speed/course descriptions | Three linked state dimensions | Misdeclared as exclusive by OWL class disjointness |
| BH-V06 | QuantityValue has permissible units | SOG with knot, distance with nautical mile | SOG with seconds |
| BH-V07 | Each contextualized relation has vessel/reference object and time extent | Complete `DirectionRelation` | Missing reference |
| BH-V08 | No target behavior class appears in pre-recognition input named graph | pre graph unlabeled | injected target label |
| BH-V09 | Every inferred behavior has traceable evidence and generation/provenance | inference record + evidence | isolated unsupported inferred class |
| BH-V10 | SemanticBehavior does not entail ModeOfOperation or COLREGSituation automatically | distinct classifications | misused equivalence or property chain |

Validation technologies: SHACL/SPARQL, RDFLib-based graph split tests, ontology reasoner consistency checks as needed. OWL's open-world semantics means absence/completeness requirements must be checked through SHACL or a deliberately closed-world test harness.

## 8. Competency Questions refined for future implementation

- **BH-CQ-01:** Which vessel, source observations, and times constitute trajectory T?
- **BH-CQ-02:** Which time interval and state descriptors belong to TemporalUnit U?
- **BH-CQ-03:** Which speed/course/position measurements, quantity values and units support each PhysicalBehavior description?
- **BH-CQ-04:** Which reference objects and computed direction/distance/topology relations characterize U?
- **BH-CQ-05:** Which two intervals actually *meet*, and which only follow one another with data gaps?
- **BH-CQ-06:** What inferred SemanticBehavior is assigned after recognition, based on which evidence, with which status/model version?
- **BH-CQ-07:** Does the pre-inference input graph exclude all target semantic labels for the target interval?
- **BH-CQ-08:** Can the same physical behavior be described while the ModeOfOperation differs?
- **BH-CQ-09:** What independent evidence supports COLREGSituation rather than deriving a COLREG label solely from SemanticBehavior?
- **BH-CQ-10:** Can alternative candidate interpretations and uncertainty be retrieved for a single temporal unit?

## 9. Decisions: approved design direction and outstanding implementation gates

| Record | Design choice | Decision | Confidence | Next gate |
|---|---|---|---|---|
| DCCR-02-D01 | Trajectory is an information representation | APPROVED DESIGN; ADD PENDING | High | DCCR-03 ontological mapping |
| DCCR-02-D02 | TemporalUnit is a segment record associated with an interval | APPROVED DESIGN; ADD PENDING | High | DCCR-03 OWL-Time mapping |
| DCCR-02-D03 | PhysicalBehavior is a description of measured/derived states, not itself the process | APPROVED DESIGN; ADD PENDING | Medium: BFO target unresolved | DCCR-03 |
| DCCR-02-D04 | InteractionBehavior is a contextualized spatial-relation description | APPROVED DESIGN; ADD PENDING | High | DCCR-03 GeoSPARQL |
| DCCR-02-D05 | SemanticBehavior is an inferred characterization with provenance | APPROVED DESIGN; ADD PENDING | Medium: class vs concept taxonomy unresolved | DCCR-03 + taxonomy decision |
| DCCR-02-D06 | OWL-Time Allen relations apply to temporal extents, not segment record individuals | APPROVED DESIGN; REUSE PENDING | High | DCCR-03 |
| DCCR-02-D07 | Do not make v1.0 SysML Kernel changes | PRESERVE | High | All stages |
| DCCR-02-D08 | Split pre- vs post-inference knowledge, preserve evidence | APPROVED DESIGN; ADD PENDING | High | DCCR-04 |

**Open design questions requiring decision prior to production TTL:**
1. Will `SemanticBehavior` behavior labels be OWL subclasses, SKOS concepts, or both with formally defined boundaries?
2. Should `PhysicalBehavior`/`InteractionBehavior` be subclasses of local `common:InformationArtifact`, or should a new more precise `BehaviorDescription` superclass mediate until BFO/CCO commitments?
3. What are accepted segment granularity, interval-boundary, gap and causal-online policies?
4. Which generic maritime `Vessel` IRI will be used, so target ships are not incorrectly inferred as MASS vessels?
5. Are classification alternatives captured as multiple results, or one assessment object with candidate scores?

## 10. Release integration

- **v0.3.0 foundation:** DCCR records only. Do not mutate released SysML Kernel or tag.
- **v0.4.0 SOSA/SSN + QUDT:** start `Trajectory`, `TemporalUnit`, `PhysicalBehavior` information layer and observations; unit/time tests.
- **v0.5.0 GeoSPARQL + COLREGs:** start `InteractionBehavior`, `EnvironmentSpace`, semantic behavior classification schema, temporal transition relations, vessel–vessel bridge.
- **v0.6–v0.8:** link to ROC/VTS, safety and function traceability without conflating behavior with operating mode.
- **v0.9.0 LLM/KG prototype:** implement recognition agent, offline/online split, evidence tracing and evaluation.
- **v1.0.0 stable:** publish accepted vocabulary, competency-question and SHACL test corpus, cross-version compatibility records.

## 11. Formal review result

**Status: APPROVED (2026-10-26).**  
Approved as a semantic design review and as the planning basis for DCCR-03 alignment specification and DCCR-04 validation contract. Accepted design decisions remain subject to the explicitly recorded open questions, mapping choices and implementation gates. This approval does **not** mean that OWL classes, formal BFO/CCO equivalences, implementation details or test results are already accepted. No source ontologies are modified by this document.
