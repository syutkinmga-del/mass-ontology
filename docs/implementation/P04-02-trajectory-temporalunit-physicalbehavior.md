# P04-02 — Trajectory, TemporalUnit and PhysicalBehavior

**Stage:** `v0.4.0-dev` / BH-P04 Observation Core  
**Status:** IMPLEMENTATION CANDIDATE; local full-repository evidence and architectural acceptance pending  
**Design authority:** approved DCCR-02 D01–D03; DCCR-03 C02–C07 / R01–R03; DCCR-04; approved P04-00 time/segmentation policy T-01…T-04.  
**Prerequisite:** P04-01 general maritime vessel and compatibility bridge.  
**Observed source baseline:** GitHub commit `599f3e7b10b33df49271ca824abfe1c36c02045d` (P04-01 validation-evidence commit, observed 2026-11-02); later commits require reconciliation.

## 1. Definitions, ontology category, and boundaries

| Term | Local definition | Category and prohibited identity | Later evidence |
|---|---|---|---|
| `bh:BehaviorInformationEntity` | Local information representation of movement | Subclass of local `common:InformationArtifact`; not a BFO/CCO equivalence | DCCR-02/03 and P04-02 review |
| `bh:Trajectory` | Versionable record of one vessel's temporal movement history | Not `common:Process`, route plan, vessel journey occurrence or geometry | `bh:ofVessel` + observations P04-03 |
| `bh:TemporalUnit` | Information segment belonging to a trajectory | Not a `time:ProperInterval` or `time:Instant` | `bh:hasTemporalExtent` |
| `bh:BehaviorDescription` | Locally mediated description of a state | Not an operational mode or a motion process | DCCR-03 |
| `bh:PhysicalBehavior` | Information about one physical-motion dimension | Not inferred high-level `SemanticBehavior` | observation/quantity provenance P04-03 |
| `bh:PositionState` | Position description | May coexist with other dimensions | observations P04-03 |
| `bh:SpeedState` | Speed description | May coexist with other dimensions | QUDT speed P04-03 |
| `bh:CourseState` | Course-over-ground description | May coexist with other dimensions, distinct from heading | QUDT angle P04-03 |

**Engineering choice requiring review:** `bh:BehaviorInformationEntity rdfs:subClassOf common:InformationArtifact` is a LOCAL modeling commitment, **not** externally verified BFO/CCO alignment. Inherited `rdfs:subClassOf` links are assertions on classes, not SHACL constraints on instance counts. If the chosen local mediator is revised, use a versioned ADR and regression evidence. The exact availability of `w3id.org` redirects is not assumed.

## 2. Directional relations

| Property | Domain → range | Closed-world fixture expectation |
|---|---|---|
| `bh:hasTrajectory` | `maritime:Vessel → bh:Trajectory` | Reciprocal link with `bh:ofVessel` |
| `bh:ofVessel` | `bh:Trajectory → maritime:Vessel` | Exactly 1 explicitly typed subject vessel |
| `bh:hasTemporalUnit` | `bh:Trajectory → bh:TemporalUnit` | Corresponds to `bh:partOfTrajectory` |
| `bh:partOfTrajectory` | `bh:TemporalUnit → bh:Trajectory` | Exactly 1 parent in P04 dataset |
| `bh:hasTemporalExtent` | `bh:TemporalUnit → time:TemporalEntity` | Exactly 1 **separate** explicitly typed `time:ProperInterval` |
| `bh:hasPhysicalBehavior` | `bh:TemporalUnit → bh:PhysicalBehavior` | Three state dimensions permitted simultaneously |
| `bh:nextTemporalUnit` | `bh:TemporalUnit → bh:TemporalUnit` | Ordered segmentation adjacency, **not** `time:intervalMeets` |
| `bh:segmentIndex` | `bh:TemporalUnit → xsd:nonNegativeInteger` | One unique zero-based index per trajectory in P04 example |

No `owl:inverseOf`, `owl:equivalentClass`, `owl:disjointWith`, OWL cardinality restrictions, special `time:intervalMeets` assertions, or BFO/CCO axioms are added in P04-02. These constraints require deliberate SHACL and/or reasoner treatment later. `bh:segmentIndex` is a **MASS-local** ordering property, not a term extracted from Xiong et al.

## 3. Scope and example

`07-behavior/ship-behavior.ttl` imports **local** common and maritime modules (ontologies are loaded explicitly by tests; RDFLib does not resolve imports automatically). It **references** the official OWL-Time vocabulary IRIs as property range and example terms without importing the external OWL-Time artifact. T-04 version/IRI/SHA-256 pinning precedes any controlled external RDF import at P04-03. `catalog-v001.xml` resolves the **local** behavior ontology IRI only.

`examples/p04-02-structural-trajectory.ttl` is a **synthetic structural demonstration, not AIS**:

- One explicitly typed generic vessel and a trajectory containing three temporal units.
- Three proper intervals: 12:00–12:01, 12:01–12:02, **12:04–12:05 UTC**, demonstrating a 2-minute gap.
- Independently typed time:Instant resources with timezone-aware `xsd:dateTimeStamp`, start < end, half-open `[start,end)` assignment policy as ingestion convention.
- Three coexisting descriptions (position, speed, course) for each unit. No fabricated numeric speed, geographic coordinate, sensor provenance, ontology-level segmentation threshold, or behavior inference.
- `bh:nextTemporalUnit` asserts sequence only: it does not assert that the second and third proper intervals meet.

## 4. Test evidence and gates

New targeted tests are under `tests/test_p04_02_behavior_core.py`: ontology identity, class/property taxonomy, no forbidden axioms, local catalog mapping, reciprocal links, actual parsed time comparison, gap handling, state coexistence, P04-01 compatibility and deliberate negative mutations. These are **local P04-02 implementation tests** and **not** the full certified BH-V01/V02/V03/V05 acceptance or negative SHACL/reasoner tests.

Run:

```bash
.venv/bin/python -m pytest -v tests/test_p04_02_behavior_core.py
make catalog && make validate && make cq && make test
python3 scripts/verify_sysml_kernel_integrity.py
git diff --check
```

**Required before P04-02 accepted:** executable test logs, observed commit SHA and compatibility with P04-01; reviewer acceptance of local information-artifact mediator, state interpretation, segment index and OWL-Time *reference-without-import* strategy.

**P04-03:** define actual SOSA/SSN `Observation`, QUDT quantities, PROV-O provenance, source AIS timestamp quality, deterministic segmentation algorithm identity and version; pin referenced external ontology artifacts. **P04-04:** add SHACL positive/negative fixtures, robust temporal/dimension checks and OWL reasoner mutant tests. **P04-05:** BH-CQ-01…03 exact binding oracles. **BH-P04 release:** still not PASS.

**Preserved unchanged:** `03-mass-core`, `04-navigation`, legacy CQ-01…14 fixture, P04-01 OWL and tests, `MASSKernel_v1.0.sysml`, accepted DCCR and P04-00 policy documents.
