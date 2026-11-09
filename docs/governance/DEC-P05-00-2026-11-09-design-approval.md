# DEC-P05-00-2026-11-09 — owner-directed approval of design baseline with open ADRs

**Decision ID:** DEC-P05-00-2026-11-09-01  
**Decision date:** 2026-11-09  
**Scope:** MASS Ontology Stack / v0.5.0 — BH-P05, design stage **P05-00 only**  
**Disposition:** **APPROVED_DESIGN_BASELINE_WITH_OPEN_ADRS**  
**Authorized design baseline (immutable prior commit):** `a73a7c8c5bc5f11a789405abd6d94da870d295b3`  
**Evidence channel:** explicit user instruction within the ChatGPT project conversation; **text-based owner-directed registration, not an electronic signature or a signed PDF**.  
**Signed original supplied:** NO. **Independent identity/signature authentication:** NOT PERFORMED.  
**Release/tag authorization:** NONE.

## 1. Owner instruction and its evidentiary scope

The project owner instructed the assistant in the conversation on 2026-11-09:

> переходим к регистрации отдельного решения владельца об утверждении проектного контракта P05-00 с перечнем открытых ADR

This is the **verbatim user instruction**. The approved-design-baseline disposition in this record is the governance registration **requested by that instruction**; it is not a fabricated longer quoted statement, a cryptographic signature, or an instruction to waive unresolved design gates.

A repository PR and GitHub checks record successful integration/verification; neither independently authenticates who typed this text. If stronger signature or formal institutional authorization is later needed, that requires separate evidence.

## 2. Specifically approved for P05-00 design governance

The owner-directed disposition accepts the **P05-00 design baseline as a planning and verification contract**, with the following strictly limited deliverables, as they existed at the immutable baseline commit above:

- [Design baseline and DCCR traceability](../reviews/P05-00-design-baseline.md) (`docs/reviews/P05-00-design-baseline.md`).
- [Spatial/graph/CRS proposal](../architecture/p05-00-spatial-graph-crs-policy.md) (`docs/architecture/p05-00-spatial-graph-crs-policy.md`).
- [Machine-readable CQ/rule/graph contract](../standards/P05-00-bh-p05-design-contract.json) (`docs/standards/P05-00-bh-p05-design-contract.json`).
- [External spatial source candidate register](../standards/P05-00-external-spatial-source-register.json) (`docs/standards/P05-00-external-spatial-source-register.json`).
- Fail-closed static design lint, its tests and [GitHub Actions #42596892643](https://github.com/syutkinmga-del/mass-ontology/actions/runs/42596892643): `PASS` with `failures: []`, **BH-P05 runtime tests DEFERRED**, and the historical `owner_approval: PENDING` before this separate registration.
- P04 technical regression on this same design-baseline SHA: [BH-P04 Behavior Validation #42596892696](https://github.com/syutkinmga-del/mass-ontology/actions/runs/42596892696), [Validate MASS Ontology #42596892684](https://github.com/syutkinmga-del/mass-ontology/actions/runs/42596892684); both `success`.

**Accepted as design directions, not automatically as axioms or verified implementations:**
- **P05-D01:** reuse DCCR-01 C08–C13 and DCCR-03 reserved local `bh:` vocabulary; preserve `Trajectory`/temporal information semantics.
- **P05-D02:** explicit GeoSPARQL WKT / OGC CRS84 (**longitude latitude**) as a candidate profile convention; no automatic EPSG:4326 transposition.
- **P05-D03:** separation of source/observed, environmental context, derived interaction, inferred semantic descriptions and provenance named graphs, with no inference-label leakage.

These three decisions are **ACCEPTED_FOR_DESIGN_CONTRACT**; implementing and verifying their actual code, assertions, geometry engine and data remain separate work.

## 3. OPEN architectural decision records (not resolved by approval)

| ID | Status | Outstanding decision / evidence required | Dependency gate |
|---|---|---|---|
| **P05-D04** | OPEN / BLOCKED_FOR_EXTERNAL_IMPORT | Choose publisher's exact **GeoSPARQL 1.1** RDF artifact, ontology and version IRIs, redistribution terms, SHA-256; verify supported query-engine functions and loading strategy. No unverified `owl:imports` or vendored RDF. | P05-02, before external RDF loading and runtime spatial conformance claims |
| **P05-D05** | OPEN / BLOCKS_PRODUCTION_ENVIRONMENTSPACE | Resolve physical geographic feature vs zone identity, proposed `bh:EnvironmentSpace rdfs:subClassOf geo:Feature`, separate `geo:Geometry`, source/chart edition and validity; determine *whether/how* another vessel can occupy a reference-object role (not by incorrectly typing it `EnvironmentSpace`). | **P05-01 production TTL**, and P05-03 vessel-vessel extensions |
| **P05-D06** | OPEN / BLOCKS_BEHAVIOR_TAXONOMY | Determine whether `SemanticBehavior` uses OWL classes, SKOS concepts or reviewed dual representation, including punning policy and named-graph leakage semantics. | P05-04 semantic implementation |
| **P05-D07** | OPEN / BLOCKS_INFERENCE_ASSESSMENT | Define `BehaviorInterpretation` controlled review-status vocabulary, multiple competing hypotheses, scoring semantics/calibration and acceptance thresholds; don't portray uncalibrated scores as probabilities. | P05-04 and BH-V09 |
| **P05-D08** | OPEN / BLOCKS_QUANTIFIED_RELATIONS | Approve geometry validity intervals, observation synchronization rule/tolerance, CRS transform provenance, geodesic/planar distance method, QUDT units and relative/true/magnetic bearing frame. | P05-02/03 before computed relationship claims |
| **P05-D09** | OPEN / BLOCKS_P05_GATE_PASS | Implement independent fail-closed `--profile p05` runner, GeoSPARQL engine capability reporting, SHACL/Python/OWL tests, positive/negative fixtures, exact-binding BH-CQ-04…10 assertions, and P04 regression. | P05-06, before any `BH-P05 PASS` or v0.5.0 release |

**Scope of open ADRs:** P05-D04…D09 remain OPEN. None is implicitly accepted because the P05-00 baseline is approved.

## 4. Conditions for transition to P05-01

**Authorized:** start the **P05-01 design/ADR analysis** of `EnvironmentSpace` (definitions, scope, alternatives and review of exact superclass/geometry treatment) in a **new PR**.

**NOT authorized by this decision alone:** writing production `EnvironmentSpace` TTL axiom commitments **before P05-D05 is resolved**, selecting unreviewed external GeoSPARQL imports, inserting semantic inference labels into input graphs, claiming execution of P05 runtime tests, or releasing/tagging v0.5.0. P05-D04 and D08 must be resolved before any affected external geometry calculations are marked valid. D06/D07 must be resolved before post-inference behavior classes/interpretations are implemented as an accepted profile.

## 5. Invariants and non-equivalences

Preserve the 2026-10-27 approved Roadmap v1.1, historical DCCR-01…04, immutable MASS-SK-1.0 and published annotated `v0.4.0` tag (source commit `d0f2368df4268cfe3c6079a1681502cad0b867fb`). Do not modify `THIRD_PARTY_NOTICES.md` / approved RR-05 source snapshots without a separate rights decision.

`bh:EnvironmentSpace` ≠ ODD/OE specification or `geo:Geometry`; `bh:InteractionBehavior` ≠ a GeoSPARQL topological predicate or actual encounter; `bh:TemporalUnit` ≠ `time:ProperInterval`; `bh:SemanticBehavior` ≠ operational mode, vessel action or COLREG compliance/situation. Never assert COLREG inference from behavior class alone. BH-P09 remains DEFERRED.

## 6. Provenance and verification

The *approved design source* is exactly **`a73a7c8c5bc5f11a789405abd6d94da870d295b3`**, the PR #7 merge commit. This separate governance record and its eventual merge have different SHAs and **do not retroactively replace the approved source revision**. For reproducibility, the machine-readable [design approval registration](../standards/P05-00-design-approval.json) contains exact source blob hashes and the static CI execution IDs. Further edits to the design contract require a new review rather than silent extension of this approval.

**Execution status:** Design contract integrity `PASS`; owner-directed design registration `APPROVED_DESIGN_BASELINE_WITH_OPEN_ADRS`; BH-P05 implementation tests `DEFERRED_NOT_EXECUTED`; v0.5.0 Release Readiness Review `NOT_STARTED`.
