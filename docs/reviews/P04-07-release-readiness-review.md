# P04-07 — Formal Release Readiness Review: MASS Ontology v0.4.0 (BH-P04)

**Project:** MASS Ontology Stack / MASS-OEF v1.1  
**Review date:** 2026-11-05  
**Reviewed GitHub branch:** `main`  
**Evidence baseline:** `11491acb0685e69c0aed6ec749eea4d138162b30`  
**Status:** **REVIEW COMPLETE / TECHNICAL GATES PASS / RELEASE DECISION NO-GO PENDING CORRECTIONS**  
**Approval boundary:** This review is a recommendation and defect register, **not** the owner's authorization to publish/tag v0.4.0.

## 1. Review authority and release scope

Authoritative scope: [Integrated Roadmap v1.1](../roadmap.md) §B/C, [DCCR-01](DCCR-01-xiong-ship-behavior-review.md), [DCCR-02](DCCR-02-semantic-design-review.md), [DCCR-03](DCCR-03-ontology-alignment-specification.md), [DCCR-04](DCCR-04-validation-contract.md), P04-00 Terminology/Time Policy, the pinned T-04 source/rights review, and recorded P04-01…06 implementation/evidence.

The v0.4.0 target is the **research Observation Core / BH-P04**: generic maritime vessel, representation of trajectory and temporal units, Position/Speed/Course physical-state descriptions, SOSA observations, QUDT 3.5.3 values for speed and course, OWL-Time intervals, PROV-O provenance and synthetic AIS-like input. The profile is not the whole end-to-end MASS ontology and not evidence of on-board validation, operational safety, real AIS stream accuracy or SysML semantic parser conformance.

DCCR approvals are **historical design approvals** and retain their dated statements that subsequent implementations were pending. Current implementation/test acceptance is established through separately published evidence; do not rewrite the approved DCCR decisions to retrospectively mark test status PASS.

## 2. Confirmed engineering gates (source-derived)

| Gate | Observed evidence at source commit | Verdict |
|---|---|---|
| Controlled source | P04-06 evidence commit `11491ac…` on `main`; earlier P04-05 evidence `6113ed1…` | PASS |
| CI execution | [BH-P04 GitHub Actions run 41998316090](https://github.com/syutkinmga-del/mass-ontology/actions/runs/41998316090) for **evidence commit**; conclusion `success` | PASS |
| Legacy CI | [Run 41998315794](https://github.com/syutkinmga-del/mass-ontology/actions/runs/41998315794); conclusion `success` | PASS |
| Archived formal CI artifact | P04-06 `docs/evidence/P04-06/` retains original run 41996276523 ZIP, verification script and hash manifests | PASS |
| Test suite | P04-06 report: **115 tests, zero errors, failures or skips** | PASS |
| BH-P04 rules | BH-V01, V02, V03, V05, V06, V11, V12 **7/7 PASS** | PASS |
| BH-P04 queries | BH-CQ-01 **18**; BH-CQ-02 **9**; BH-CQ-03 **18** exact-binding rows | PASS |
| Legacy behavior | `catalog`, `validate`, `cq` (CQ-01…14), full pytest regressions | PASS |
| External RDF | T-04 eight locally pinned publisher snapshots, SHA-256, ontology identity, selected terms, owner-approved rights review; BH-V11 | PASS *for T-04 control* |
| SysML kernel | Immutable MASS-SK-1.0 SHA-256 `1701bbb86e24588660ef717f2ff7f276b63c938d8569d4511dc19c42033aa788` | PASS (byte integrity only) |
| P04 data | 370 triples in current synthetic AIS fixture; six synthetic messages, 18 SOSA observations, three temporal units, gap 12:02–12:04 UTC; QUDT v3.5.3 `qudt:hasUnit` | PASS *for fixture and stated scope* |

This verdict is based on **the published GitHub repository, workflows, source files and evidence**. It is not a new execution of the full ontology test suite by the reviewer.

## 3. DCCR cross-document traceability

| Approved design/control | Implemented location | Formal gate | Status / boundary |
|---|---|---|---|
| DCCR-01 inventory and profile split | `docs/reviews/DCCR-01…`; `docs/roadmap.md` | P04 scope vs future-profile deferral | PASS for P04 subset; source's 13 classes/9 relations are not all implemented |
| DCCR-02 D01 `Trajectory` information record | `07-behavior/ship-behavior.ttl` | BH-V01/V02, BH-CQ-01/02 | PASS |
| DCCR-02 D02 `TemporalUnit` ≠ `ProperInterval` | `07-behavior/ship-behavior.ttl`; synthetic fixture | BH-V02/V03, BH-CQ-02 | PASS |
| DCCR-02 D03 concurrent Position/Speed/Course | `07-behavior/ship-behavior.ttl` | BH-V05/V06, BH-CQ-03 | PASS |
| DCCR-03 generic `maritime:Vessel` | `02-maritime/maritime-core.ttl`, `vessel-compatibility.ttl` | BH-V01, legacy regressions | PASS; local class hierarchy, no asserted BFO equivalence |
| DCCR-03 SOSA/SSN, QUDT, Time and PROV reference | `05-observation`, `06-quantities`, `07-behavior/behavior-observation-bridge.ttl` | BH-V06/V11, BH-CQ-01/03 | PASS for referenced vocabulary profile; no live external `owl:imports` |
| DCCR-04 positive and negative checks | `shapes/ship-behavior-p04.shacl.ttl`, `tests/behavior/fixtures/invalid/`, `tests/test_p04_04_validation.py` | BH-V01/02/03/05/06/11/12 | PASS |
| DCCR-04 exact SPARQL solutions | `queries/behavior/bh-cq-01..03.rq`, `tests/behavior/expected/`, hash-locked manifest | BH-CQ-01…03 | PASS; multiset, IRI and datatype identity |
| DCCR-04 CI / regression | `scripts/run_behavior_ci.py`, `make behavior-test`, dedicated GitHub Actions workflow | 11 fail-closed gates | PASS |
| P05/P09 future work | Roadmap; DCCR-04 profile table | BH-V04/V07–V10 and BH-CQ-04…10 | **DEFERRED**, never PASS |

## 4. Findings requiring resolution before a v0.4.0 tag

| Finding | Priority | Observed fact | Required disposition | Verification |
|---|---|---|---|---|
| **RR-01 — Release metadata** | **BLOCKER** | Root `VERSION` is `0.1.0`, and `[project].version` in `pyproject.toml` is `0.1.0`. | After owner confirms release candidate, consistently set both to `0.4.0`; record candidate commit and re-run CI. | P04-07 R05 |
| **RR-02 — Public documentation** | **BLOCKER** | `README.md` describes `v0.3.0-dev`; `docs/index.md` is still a v0.3 research MVP. README has unclosed Markdown code fences and an invalid `make validatpytest` command. | Rewrite these documents for actual BH-P04 scope, correct local/CI commands, release boundaries and version without overstating functionality. | P04-07 R06 |
| **RR-03 — Changelog** | **BLOCKER** | `CHANGELOG.md` has no v0.4.0 section and ends with an unclosed Markdown fence. | Record P04-01…06 changes, frozen external dependencies, fixes from `qudt:unit` to `qudt:hasUnit`, regression results and limitations. | P04-07 R07 |
| **RR-04 — Project distribution license** | **BLOCKER for a reusable public research release** | Repository root `LICENSE` is **0 bytes**. T-04 external vocabulary approval does **not** grant a license to original MASS project files. | Project owner selects and authorizes a license for project-authored content; record rights holder(s), file scope and any exceptions. Do **not** invent a license automatically. | P04-07 R08 |
| **RR-05 — Redistribution attribution** | **BLOCKER under the proposed publication policy** | `vendor/external-rdf/T04-2026/` includes W3C/OGC and QUDT snapshots; T-04 rights review exists but no dedicated top-level third-party release notice was found. | Verify upstream per-artifact copyright/licensing notices and publish a vetted `THIRD_PARTY_NOTICES.md` with credit, links and unchanged/modified status. This is an **additional P04-07 release-control choice**, not a finding that T-04 itself failed. | P04-07 R08 |
| **RR-06 — Release notes and approval** | **BLOCKER** | No signed v0.4.0 project-owner release decision or final v0.4.0 notes in the reviewed source. | Final release notes, owner decision with date, evidence commit, commit/CI review and then annotated tag. | P04-07 R09/R10 |

### Recorded, nonblocking limitations

- **LIM-01:** Python direct dependencies are pinned; transitive wheel hashes and exact JDK binary are not pinned. GitHub CI is version-controlled and successful, but not hermetic.
- **LIM-02:** P04 is based on synthetic prevalidated AIS-like records; no raw AIS decoder, real-time AIS integration, accuracy metrics or production capability is claimed.
- **LIM-03:** The cited `https://w3id.org/mass-ontology/` namespace is not demonstrated to be publicly dereferenceable by the current tests; this must not be claimed in release notes without an additional live resolver check.
- **LIM-04:** BFO/CCO choices are candidate mappings, not external equivalence or imported reasoner validation; GeoSPARQL / semantic behavior / COLREG inference/ROC/VTS are future releases.
- **LIM-05:** MASS-SK-1.0 passes byte/manifest integrity checks; this is **not** an execution of a SysML v2 parser on the immutable source.
- **LIM-06:** Some historical P04-02/03/04/05 implementation documents still use their original dated `IMPLEMENTATION CANDIDATE` status. Do not rewrite history; current stage status is stated by current CI/evidence and release review.

## 5. Acceptance policy and decision

**Current review recommendation: NO-GO for tagging/publishing v0.4.0.** This is a **release-package governance result**, *not* a failure of the executed BH-P04 ontology rules. The active scope has passed its technical gate.

Before GO, close RR-01…RR-06; run `python3 scripts/review_release_p04.py --repo "$PWD"` and require **all 10 release-readiness gates PASS**. Re-run `make behavior-test`, verify GitHub Actions on the release-candidate commit, and record owner approval in `docs/governance/DEC-P04-07-v0.4.0-release.md`. Do not claim new implementation evidence without actually executing tests on that candidate.

The owner must explicitly approve the public license, third-party notices, release scope and version. The report produced by the P04-07 script is audit evidence, not a substitute for approval. After an owner-approved GO, an annotated `v0.4.0` tag may be issued on the verified release commit, followed by a GitHub Release entry. Do not issue the tag now.

**Future work:** after accepted v0.4.0 release, resume the roadmap with v0.5.0 / BH-P05. P04 release cannot silently pass P05/P09 tests.
