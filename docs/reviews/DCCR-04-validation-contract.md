# DCCR-04 — Validation Contract for Ship Behavior Ontology

**Project:** MASS Ontology Stack / MASS Domain Library  
**Date:** 2026-10-27  
**Approval date:** 2026-10-27  
**Status:** **APPROVED — validation specification accepted; implementation and execution pending**  
**Inputs:** DCCR-01 Xiong Ship Behavior Review (APPROVED, 2026-10-26); DCCR-02 Semantic Design Review (APPROVED, 2026-10-26); DCCR-03 Ontology Alignment Specification (APPROVED, 2026-10-27).  
**Reference baselines:** `MASSKernel_v1.0.sysml` / MASS-SK-1.0 (immutable); current MASS Ontology `v0.3.0-dev` OWL/RDF model.  
**Study:** Xiong et al., *Ontology-Guided Multimodal Large Language Model for Semantic Recognition of Ship Navigation Behaviors*, *Journal of Marine Science and Engineering* 14(19), 1859 (2026). DOI: https://doi.org/10.3390/jmse14191859.

> **Approval semantics:** DCCR-04 approval accepts a **test specification**; it does not announce completed SHACL tests, installed external ontologies, successful BH-CQ query executions, actual dataset coverage, BFO/CCO compliance, or deployed ship-behavior production OWL. It must remain distinct from subsequent test-implementation and execution reports.

## 1. Purpose and authoritative scope

Provide repeatable checks proving that the eventual Ship Behavior Ontology implementation is consistent with DCCR-01 to DCCR-03 and does not break the existing repository regressions.

The contract covers:

1. RDF/OWL/Turtle schema parse and identity checks;
2. instance structure, counts and expected class typing (SHACL Core);
3. temporal and sequence coherence (Python/SPARQL + selected SHACL-SPARQL);
4. physical measurement completeness and QUDT dimensional correctness;
5. spatial relation context and GeoSPARQL modeling (v0.5);
6. pre-/post-inference evidence separation, provenance and uncertainty;
7. key semantic non-equivalences and compatibility with MASS Semantic Kernel;
8. BH competency questions and executable regression tests;
9. isolated, deterministic CI and dependency pinning.

**Excluded:** correctness of physical ship motion, navigation safety certification, universal COLREG applicability, full reasoner soundness, MLLM accuracy, real-time performance, ODD/OE numerical evaluation, and independent validation of external BFO/CCO mappings. Absence of these capabilities is not a DCCR-04 failure if outside the chosen implementation profile.

## 2. Model/test profiles and implementation phases

| Profile | Release | In scope | Not yet required |
|---|---|---|---|
| **BH-P04 (Observation Core)** | v0.4.0 | General `maritime:Vessel` identity; `bh:Trajectory`, `bh:TemporalUnit`, `bh:PhysicalBehavior` and Position/Speed/Course variants; SOSA/SSN observations; QUDT values; explicit time extent, links and provenance | Spatial EnvironmentSpace, inferred behavior, operational COLREG bridge |
| **BH-P05 (Spatial + Semantic)** | v0.5.0 | `bh:InteractionBehavior` and Direction/Distance/Topology; `bh:EnvironmentSpace`; GeoSPARQL; interval relationships; `bh:SemanticBehavior`, `bh:BehaviorInterpretation`, pre/post named-graph boundaries | Validated real-time classifier or decision authority |
| **BH-P09 (Recognition Prototype)** | v0.9.0 | model provenance, alternative hypotheses, outcome quality, no temporal leakage, offline vs online causal tests | Safety-certified autonomous navigation |

Profile selection MUST be explicit in the test runner (`--profile p04|p05|p09` or equivalent). No test can silently pass because classes for a later profile do not yet exist. An inapplicable future-profile test is **DEFERRED**, not **PASS**.

## 3. Validation levels and output status

| Level | Technology | Proves | Does not prove |
|---|---|---|---|
| L0 Syntax | RDFLib `Graph.parse` / XML catalog checker | Parses individual TTL and test manifest; local paths exist | Ontology satisfiability, semantically correct usage |
| L1 Structural | pySHACL, SHACL Core | Curated data satisfies required graph shapes | Physical truth or external interoperability |
| L2 Cross-entity/time/unit | Python tests + SPARQL/SHACL-SPARQL | Interval ordering, object linkage, value-type and unit whitelists | Completeness of unseen sensor measurements |
| L3 Ontology semantics | OWL reasoner (pinned profile) + negative regression | No prohibited inferred equivalence/unsatisfiability in test ontology | Universal absence of problematic interpretations |
| L4 Information integrity | RDFLib `Dataset` / named graph tests | Inference input excludes target labels; resulting labels retain evidence | Statistical calibration or prediction quality |
| L5 CQ and legacy regressions | SPARQL result assertions + existing `make cq` | Questions answerable on controlled datasets; legacy checks preserved | Generalization to all ports/vessels |

**Pass/fail/deferred:** A test is PASS only when it executed and satisfied its oracle. FAIL when it executed and violated its oracle. DEFERRED when its profile is not in scope or prerequisites are pending. BLOCKED when execution was expected but tool/config/data unavailable. Do not use PASS for unexecuted rows.

## 4. BH validation-rule matrix (required contract)

| ID | Profile | Rule / expected behavior | Mechanism | Positive fixture | Negative fixture | Acceptance oracle |
|---|---|---|---|---|---|---|
| **BH-V01** | P04 | Each populated `bh:Trajectory` links by `bh:ofVessel` to **exactly one** explicitly typed `maritime:Vessel` | SHACL Core (`minCount=1`, `maxCount=1`, `sh:class`) | `P04-valid` | `N01-no-vessel`; `N01b-two-vessels` | Valid conforms; both invalid fixtures fail with BH-V01 |
| **BH-V02** | P04 | Each `bh:TemporalUnit` links to exactly one parent `bh:Trajectory` and one `time:ProperInterval`; reciprocal `hasTemporalUnit` consistency as a separate dataset check | SHACL Core plus SPARQL/Python | `P04-valid` | `N02-no-extent`; `N02b-mismatched-membership` | Both required links, expected type and reciprocal integrity verified |
| **BH-V03** | P04 | For a trajectory's ordered segments: normalized UTC start/end, start < end, strictly ordered indices; no unapproved overlaps | Python temporal assertions | `P04-valid` | `N03-overlap`; `N03-reversed-bounds` | Negative overlap/reversed bounds detected; timezone and precision policy applied |
| **BH-V04** | P05 | `time:intervalBefore`, `After`, `Meets` are on **ProperIntervals**; `Meets` is valid only when end(A) equals begin(B); `nextTemporalUnit` alone does not entail `Meets` | SHACL Core + Python / SPARQL | `P05-valid` | `N04-false-meets-gap`; `N04-wrong-domain` | False meeting fails; chronological next-with-gap remains valid without `Meets` |
| **BH-V05** | P04 | One unit may have PositionState, SpeedState and CourseState concurrently; no accidental class disjointness or exclusive-state inference | Positive multi-dimension fixture + OWL consistency | `P04-valid` contains all three | `N05-illegal-disjointness` schema mutation | Positive data satisfiable; mutant rejected by reasoner/mutation gate |
| **BH-V06** | P04 | Measurement `bh:hasQuantityValue` leads to `qudt:QuantityValue` with exactly one numeric value and unit; speed uses approved speed units, course approved angular units, distance approved length units | SHACL Core + dimension registry check | Speed in `unit:KN`, course in `unit:DEG` | `N06-speed-in-sec`; `N06-missing-unit`; `N06-nonnumeric` | Each malformed case fails its intended value/unit rule |
| **BH-V07** | P05 | Interaction relation identifies one subject vessel, reference object, appropriate temporal context and source/provenance; spatial relations are not themselves a COLREGSituation | SHACL Core + cross-link checks | `P05-valid` | `N07-no-reference`; `N07-no-time-context` | Invalid fixtures fail; no implicit COLREG class assigned |
| **BH-V08** | P05 | Pre-inference named graph contains **no** target `bh:hasSemanticBehavior`, `bh:hasBehaviorInterpretation` output labels or post-classification result records for the target units | RDFLib `Dataset` scoped SPARQL test; graph allowlist | `P05-pre-valid` | `N08-label-leakage` | Input validation fails on any target label leak; dataset graphs do not union by default |
| **BH-V09** | P05 | Each post-inference `BehaviorInterpretation` references target unit, proposed semantic behavior, evidence and a producing `prov:Activity`; `confidenceScore` optional but if present normalized decimal in [0,1]; hypotheses need explicit review status | SHACL Core, provenance link check | `P05-post-valid` | `N09-no-evidence`; `N09-no-activity`; `N09-score-out-of-range` | Negative fixtures fail, alternative hypotheses remain representable |
| **BH-V10** | P05 | SemanticBehavior is **not automatically equivalent** to ModeOfOperation / OperationalCondition / COLREGSituation / `nav:Maneuver` and does not independently entail a COLREGRule | Reasoner/ontology-mutation tests, explicit non-inference expectations | `P05-valid` | `N10-equivalence-mutant`; `N10-property-chain-mutant` | Mutant axiom makes regression fail; baseline does not produce prohibited entailments |
| **BH-V11** | P04+ | Imports/IRI policy: no GitHub repository home page used as `owl:imports` BFO/CCO ontology IRI; external artifacts resolved reproducibly if selected | catalog lint, URL/IRI registry audit | pinned local vocab profile | `N11-repository-url-import` | Repository URL used as ontology import is rejected; mere candidate registry link not rejected |
| **BH-V12** | P04+ | Existing MASS Ontology `CQ-01`…`CQ-14`, SHACL and catalog remain green; SysML v1.0 source remains unchanged | Existing scripts, git/hash checks | legacy baseline fixture | `N12-legacy-breaking-change` | `make catalog`, `make validate`, `make cq` pass; v1.0 checksum unchanged |

**Caveats:** BH-V05 and BH-V10 cannot be proven by SHACL alone. BH-V08 requires validation against the exact inference-input named graph(s), not a unioned graph that includes output labels. BH-V03 and BH-V04 must use real parsed instants; lexical string comparison is prohibited. BH-V11 does not imply that any full BFO/CCO ontology has been imported.

## 5. SHACL implementation patterns (illustrative — not executed production shapes)

Use **SHACL Core** for type, min/max count, node kind, numeric datatype/range and closed-world presence. Use **SPARQL or Python** for cross-node/time calculations; do not rely on RDFS `domain` statements to reject bad instance types.

### 5.1 Trajectory and TemporalUnit

```turtle
@prefix bh: <https://w3id.org/mass-ontology/behavior#> .
@prefix maritime: <https://w3id.org/mass-ontology/maritime#> .
@prefix time: <http://www.w3.org/2006/time#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

bh:TrajectoryShape a sh:NodeShape ;
    sh:targetClass bh:Trajectory ;
    sh:property [ sh:path bh:ofVessel ; sh:minCount 1 ; sh:maxCount 1 ;
                  sh:class maritime:Vessel ] .

bh:TemporalUnitShape a sh:NodeShape ;
    sh:targetClass bh:TemporalUnit ;
    sh:property [ sh:path bh:partOfTrajectory ; sh:minCount 1 ;
                  sh:maxCount 1 ; sh:class bh:Trajectory ] ;
    sh:property [ sh:path bh:hasTemporalExtent ; sh:minCount 1 ;
                  sh:maxCount 1 ; sh:class time:ProperInterval ] .
```

**Typing policy:** For deterministic P04 fixtures, assert source types explicitly. If SHACL uses RDFS inference, record it; requiring an asserted type is a separate rule. A missing class typing failure can otherwise be hidden by inference in a schema-enhanced graph.

### 5.2 QUDT quantity structural check

```turtle
@prefix bh: <https://w3id.org/mass-ontology/behavior#> .
@prefix qudt: <http://qudt.org/schema/qudt/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

bh:QuantityValueShape a sh:NodeShape ;
    sh:targetClass qudt:QuantityValue ;
    sh:property [ sh:path qudt:numericValue ; sh:minCount 1 ;
                  sh:maxCount 1 ; sh:datatype xsd:decimal ] ;
    sh:property [ sh:path qudt:unit ; sh:minCount 1 ; sh:maxCount 1 ;
                  sh:nodeKind sh:IRI ] .
```

This is a **strict MVP ingestion profile**, not a claim that QUDT globally restricts `qudt:numericValue` to `xsd:decimal`. The dimension-aware validation must additionally bind the result to its `SpeedState`/`CourseState`/distance context and check a controlled unit registry or QUDT quantity-kind/dimension vector. A global rule `sh:in (unit:KN)` is **not** appropriate for all QUDT QuantityValues. Verify unit identifiers and lock the selected QUDT release (e.g., `unit:KN` is knot, `unit:KiloN` is kilonewton).

### 5.3 Temporal instance check: requirement, not a naïve OWL cardinality

For each `bh:TemporalUnit` extract `bh:hasTemporalExtent` → `time:ProperInterval` → exactly one `time:hasBeginning` and one `time:hasEnd` → `time:Instant` → suitable parsed `time:inXSDDateTimeStamp`. For this implementation profile require timezone-aware, canonical parseable instants. Compare actual UTC instants. Do not treat a missing field as zero duration, and do not treat AIS observation gap as continuous temporal coverage.

### 5.4 Provenance and classification check

Post-inference `bh:BehaviorInterpretation` must link to evidence and producing `prov:Activity`, with proposed behavior explicitly linked. The DCCR-03 `bh:reviewStatus` vocabulary, category modeling strategy (SKOS vs OWL class), confidence calibration and policy for multiple hypotheses remain **design gates**. A final production shape cannot be frozen until they are resolved. The safety/COLREG bridge cannot assert equivalences from high-level behavior alone.

## 6. BH competency questions and evidence-oriented expected assertions

**Namespace:** `BH-CQ` is separate from legacy OWL `CQ-01…14` and from SysML Kernel `CQ1…12`. Do not reuse IDs in the old `expected-cq-results.json` without a deliberate migration. Each BH-CQ will have a query file, a fixed positive dataset and an **expected bindings** assertion; row counts alone are insufficient.

| BH-CQ | Competency question | Target bindings / observable result | Profile | Primary validations |
|---|---|---|---|---|
| **BH-CQ-01** | Which vessel, trajectory, source observations and times are represented? | Vessel IRI, trajectory IRI, observation IRI, phenomenon/result time | P04 | BH-V01, V02 |
| **BH-CQ-02** | Which `TemporalUnit`, time extent and movement states belong to trajectory T? | Unit IRI, interval IRI, physical-state IRIs, ordered indices | P04 | BH-V02, V03, V05 |
| **BH-CQ-03** | Which positions/speeds/courses and QUDT units support the physical description? | state kind, quantity IRI, numeric value, unit IRI, source observation | P04 | BH-V05, V06 |
| **BH-CQ-04** | Which spatial context and direction/distance/topology relations characterize a unit? | unit, relation kind, reference space, reference frame/time | P05 | BH-V07 |
| **BH-CQ-05** | Which units/intervals are consecutive, and which temporal intervals actually meet? | U1, U2, I1, I2, order, meets truth value and boundary instants | P05 | BH-V03, V04 |
| **BH-CQ-06** | What semantic classification was produced from which evidence by which method? | unit, candidate behavior, evidence, provenance activity, review status | P05 | BH-V09 |
| **BH-CQ-07** | Are target behavior labels absent from input-to-inference graphs? | zero prohibited triples / deterministic boolean true | P05 | BH-V08 |
| **BH-CQ-08** | Can the same described physical motion occur under distinct operating modes? | movement context + independently supplied operating mode; no inferred equivalence | P05 | BH-V10 |
| **BH-CQ-09** | What independent encounter evidence supports any COLREGSituation classification? | spatial/nav situation and source observations, not just behavior label | P05 | BH-V10 |
| **BH-CQ-10** | Which alternative behavior hypotheses, confidence scores and statuses can be retrieved? | ordered candidate interpretations and evidence; uncertain proposals distinguished from accepted | P05/P09 | BH-V09 |

**Oracle format recommended:** canonicalized SPARQL solutions (selected variable names and literal datatypes, sorted) checked against checked-in JSON/CSV, plus a separate expected cardinality. A query returning the right number of **wrong rows** MUST fail. CQ-07 is a negative-result question and must use a scoped graph check rather than a generic row-count fixture.

## 7. Fixture package and test-isolation policy

Proposed repository layout **after** DCCR-04 approval and when implementation begins:

```text
07-behavior/ship-behavior.ttl                 # production only after implementation decision
shapes/ship-behavior.shacl.ttl                # validation shapes
competency-questions/behavior-cq.md
queries/behavior/bh-cq-01.rq ... bh-cq-10.rq
tests/behavior/
  manifest.json                              # profile, target check ID, expected outcome
  fixtures/
    p04-valid.ttl
    p05-pre-valid.trig                        # explicit named graphs
    p05-post-valid.trig
    invalid/
      n01-no-vessel.ttl
      n02-no-extent.ttl
      n03-overlap.ttl
      n04-false-meets-gap.ttl
      n05-illegal-disjointness.ttl
      n06-speed-in-sec.ttl
      n07-no-reference.ttl
      n08-label-leakage.trig
      n09-no-evidence.trig
      n10-equivalence-mutant.ttl
      n11-repository-url-import.ttl
      n12-legacy-breaking-change.ttl
  expected/
    bh-cq-01.json ... bh-cq-10.json
scripts/run_behavior_validation.py
```

File names are illustrative. A negative fixture should alter **one intended property** relative to a positive baseline. It passes the meta-test only if the validator rejects it **for the expected BH-V rule**, not because of unrelated syntax or missing files. A malformed RDF file is a syntax-test case, not a satisfactory negative SHACL fixture.

**Named graphs:** Use `rdflib.Dataset` (not `Graph`) for pre/post datasets, with explicit graph IRIs such as `.../graph/pre` and `.../graph/post`. Disable default-union reasoning for leakage checks. Check all allowed input graphs and upstream preprocessing artefacts for target labels. Keep schema graph or vocabulary terms separate from instance output: mere mention of class IRIs in ontology schema must not count as data-label leakage.

**Repeatability:** pin Python and package versions, external RDF releases by checksum, geometry/CRS assumptions, graph names, time-zone and temporal precision, inference mode, fixture version and hash, expected-query-binding files, and deterministic sorting/rounding of output values. No live web retrieval during CI.

## 8. CI gates and existing repository integration

At DCCR-04 acceptance, **nothing new is yet executed**. During v0.4/v0.5 implementation, add a separate `make behavior-test` target, avoiding modifications to current `make cq` expected-count semantics before a deliberate migration.

Existing repository commands to preserve:

```bash
make catalog
make validate
make cq
```

Expected future invocation (planned, not currently available):

```bash
.venv/bin/python scripts/run_behavior_validation.py --profile p04
.venv/bin/python scripts/run_behavior_validation.py --profile p05
```

**Proposed CI ordering:**

1. Lint JSON/Turtle/TriG and local catalog before any inference.
2. Execute standard legacy catalog/SHACL/CQ gates (14 legacy ontology CQs).
3. Validate positive behavior fixture(s) against active profile; they MUST conform.
4. Execute negative fixtures, verifying **expected, rule-specific violations** (and syntax errors only in a designated syntax suite).
5. Execute script-level temporal/unit/graph-split checks.
6. Execute BH-CQ expected-binding regression on positive fixture(s).
7. Execute separately designated reasoner/mutation tests and check no forbidden entailments.
8. Write a machine-readable CI report with profile, environment, PASS/FAIL/DEFERRED/BLOCKED and fixture hashes.

`v0.4` release gate: all P04 tests implemented and PASS, legacy gates PASS, no P04 BLOCKED. P05 tests are DEFERRED and must be listed in the report. `v0.5` gate: all P04 and P05 tests implemented and PASS; P09 remains DEFERRED. DCCR-04 document approval alone does **not** satisfy these gates.

## 9. Cross-document traceability

| Source decision | DCCR-03 terms | BH rules | BH queries | Release |
|---|---|---|---|---|
| DCCR-02-D01 trajectory as representation | `bh:Trajectory`, `bh:ofVessel`, `bh:hasTemporalUnit` | V01, V02 | CQ01, CQ02 | v0.4 |
| DCCR-02-D02 segment ≠ interval | `bh:TemporalUnit`, `bh:hasTemporalExtent`, `time:ProperInterval` | V02, V03, V04 | CQ02, CQ05 | v0.4/v0.5 |
| DCCR-02-D03 physical-state descriptions | `bh:PhysicalBehavior`, `SpeedState`, `CourseState`, `qudt:QuantityValue` | V05, V06 | CQ03 | v0.4 |
| DCCR-02-D04 interaction description | `bh:InteractionBehavior`, `EnvironmentSpace`, `geo:Feature` | V07 | CQ04 | v0.5 |
| DCCR-02-D05 inferred behavior description | `bh:SemanticBehavior`, `bh:BehaviorInterpretation` | V08, V09, V10 | CQ06, CQ07, CQ08, CQ10 | v0.5 |
| DCCR-02-D06 Allen relations on extents | `time:intervalBefore`, `After`, `Meets` | V04 | CQ05 | v0.5 |
| MASS-SK-1.0 immutability / MASS CQ baseline | SK source, legacy modules and catalogs | V10, V11, V12 | CQ08, CQ09 + legacy 01..14 | all |

## 10. Implementation acceptance checklist (after document approval)

**The following approved requirements must be satisfied and evidenced by the implementation team. Unchecked items are not failed approval conditions; they await implementation verification:**

- [ ] BH-V01…BH-V12 each has an identified profile, input data and pass/fail oracle;
- [ ] BH-CQ-01…BH-CQ-10 are traceable to constraints and proposed evidence bindings;
- [ ] pre-/post-inference graph segregation is defined and testable;
- [ ] temporal interval vs information record distinction is enforced;
- [ ] QUDT validation is dimension/context aware and its vocabulary version is frozen before implementation;
- [ ] positive and negative fixtures are defined for each appropriate rule, including special schema-mutation tests;
- [ ] known open questions (SKOS vs OWL taxonomy, review status model, generic Vessel, segmentation tolerance) are documented as implementation gates, not silently answered;
- [ ] legacy OWL CQ-01…14 and immutable MASS-SK-1.0 are preserved;
- [ ] no DCCR documentation claims actual tests PASS before execution.

### Decisions to defer to implementation design / ADR

1. Exact `maritime:Vessel` migration and link to `mass:MASSVessel`, `nav:TargetShip`.
2. `bh:SemanticBehavior` OWL classes vs SKOS categories vs dual representation.
3. BehaviorInterpretation status vocabulary and confidence-score calibration.
4. Timestamp precision, gap threshold and segmentation configuration.
5. Exact pinned external ontology artifacts and import strategy (no GitHub URL as ontology IRI).
6. SHACL inference regime on shapes and fixture sets; strict type assertions vs RDFS-entailment permissiveness.
7. OWL reasoner and supported semantic profile for regression/mutation tests.

## 11. Verification reference sources

- W3C SHACL Recommendation: https://www.w3.org/TR/shacl/ — shapes, `sh:minCount`, `sh:maxCount`, SHACL-SPARQL and `sh:conforms`.
- W3C OWL-Time: https://www.w3.org/TR/owl-time/ — proper intervals, interval relation domain/range and Allen relations.
- W3C SOSA/SSN (2023 edition): https://www.w3.org/TR/vocab-ssn-2023/ — observations, `phenomenonTime` vs `resultTime`.
- QUDT catalogue: https://www.qudt.org/catalog/qudt-catalog.html — versioned schema/unit vocabularies.
- OGC GeoSPARQL 1.1: https://docs.ogc.org/is/22-047r1/22-047r1.html — feature, geometry and spatial relations.
- W3C PROV-O: https://www.w3.org/TR/prov-o/ — provenance entities and activities.

## 12. Review conclusion

**DCCR-04 status: APPROVED on 2026-10-27 — validation contract accepted as an engineering specification; tests not yet implemented or executed.**

The contract specifies how the staged Ship Behavior Ontology *will* be evaluated and how unacceptable semantic conflations and regression failures are to be detected. It **does not yet implement** the behavior schema, shapes, fixtures, query runner or a green CI result. This approval authorizes preparation of a test implementation plan; actual release acceptance remains contingent on executing the test suite against checked-in artifacts.

**Approved document location:** `docs/reviews/DCCR-04-validation-contract.md`; register the approved specification in `docs/index.md` while keeping test implementation status separate.
