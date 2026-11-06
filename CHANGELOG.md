# Changelog

## v0.4.0 — Observation Core (APPROVED FOR RELEASE; PUBLICATION NOT RECORDED)

Candidate prepared under MASS-OEF Roadmap v1.1, BH-P04 validation profile. The project-owned Apache-2.0 license and eight third-party RDF notices were approved under RR-04/RR-05. Signed R10 P04-07-R10-2026-01 dated 2026-11-06 approves exactly `81b33951cbed446ebff5192099125f56ff474fb0`. This later registration commit is not the approved SHA. No v0.4.0 tag/GitHub Release publication is claimed.

### Added

- Generic `maritime:Vessel` and compatibility with existing `mass:MASSVessel`, `nav:TargetShip`.
- `bh:Trajectory`, `bh:TemporalUnit`, distinct `time:ProperInterval` extents and concurrent position/speed/course descriptions.
- SOSA/SSN observations, PROV-O provenance, OWL-Time and QUDT 3.5.3 speed/course measurements.
- Deterministic 370-triple **synthetic AIS-like** demonstration, three time segments and documented coverage gap.
- SHACL/Python/ROBOT-HermiT positive/negative checks (BH-V01/02/03/05/06/11/12); BH-CQ-01/02/03 with exact IRI/typed-literal bindings.
- `make behavior-test`, separate fail-closed GitHub Actions workflow, locked T-04 external RDF references and published P04-06 evidence.

### Changed

- Introduced versioned fixture `examples/p04-04-synthetic-ais-qudt353.ttl` with QUDT 3.5.3 `qudt:hasUnit`; original P04-03 fixture remains frozen and unchanged.
- Retained historical 14 CQ checks, all DCCR-01…04 contracts, Roadmap v1.1 and immutable MASS-SK-1.0 source bytes.
- Updated release-candidate public documentation and external vocabulary notices as P04-07 remediation.

### Verification and boundaries

- Source P04-06 GitHub CI: 11/11 mandatory gates; 115 tests without failures/errors/skips; 7 BH-V PASS, 3 BH-CQ exact-binding PASS. Both GitHub Actions workflows subsequently succeeded on commit `bf024c1698787d22979bb61289d57200f8220a59` (runs 42190651882 and 42190652017); the owner reports R10 candidate runs 42194345291 and 42194345375 as SUCCESS on `81b33951cbed446ebff5192099125f56ff474fb0`. Registration-branch validation is separate.
- BH-P05 spatial/semantic classification and BH-P09 recognition are **DEFERRED**.
- No real AIS decoder/accuracy, navigation safety certification, BFO/CCO formal import alignment or new SysML v2 parser proof is claimed.
- RR-04 Apache-2.0 author-owned license decision and RR-05 eight third-party RDF notices are **approved and recorded**; [signed R10 is registered](docs/governance/DEC-P04-07-v0.4.0-release.md) for its exact approved SHA. The historical [RR-05 status discrepancy](docs/governance/P04-07-RR05-notice-status-clarification.md) was resolved by the separate [RR-05-2026-02 owner text approval](docs/governance/DEC-P04-07-RR05-2026-02-chat-approval.md) and merged PR #3. The corrected root notices SHA-256 is `7387ce9b98911917bb02ea9f3228fad2942fe65c8c7974d2f9890e01620f8ce5`; original signed RR-05-2026-01 evidence remains intact. The new owner approval is an in-chat text decision, not a signed PDF. Current `main` is not automatically authorized as the R10 release target.


### Post-R10 governance follow-up (2026-11-06)

- PR #1 registered the historical signed R10 authorization without changing the signed target SHA.
- PR #3 installed the owner text-approved RR-05-2026-02 corrected notices edition and strengthened fail-closed CI verification; the eight upstream RDF snapshots were unchanged.
- The post-merge `main` CI runs [42209855912](https://github.com/syutkinmga-del/mass-ontology/actions/runs/42209855912) and [42209855875](https://github.com/syutkinmga-del/mass-ontology/actions/runs/42209855875) succeeded on `2dbd3e849e5dc2807d7df2786fb905ac17089722`.
- A follow-up formal R01–R10 review and a new exact-SHA R10 authorization are required before tagging a newer release candidate.

## Unreleased — v0.3.0-dev

### Added

- MASS Common ontology draft:
  - `01-common/common-core.ttl`.
- Foundation alignment draft:
  - `00-foundation/foundation-alignment.ttl`.
- Draft alignment decisions for selected MASS Core and Navigation classes.
- Common-layer superclass links for MASS Core classes.
- Common-layer superclass links for Navigation classes.
- Foundation alignment competency questions:
  - CQ-09 — foundation alignment decisions;
  - CQ-10 — MASS vessel foundation target;
  - CQ-11 — draft alignment decisions;
  - CQ-12 — navigation alignment decisions.
- SPARQL queries for CQ-09 ... CQ-12.
- Expected CQ result checks for foundation alignment queries.
- Architecture Decision Record for foundation alignment strategy:
  - `docs/adr/ADR-001-foundation-alignment-strategy.md`.
- Local ontology catalog mapping:
  - `catalog-v001.xml`.
- Catalog validation script:
  - `scripts/check_catalog.py`.
- `make catalog` command for checking local ontology IRI mappings.
- GitHub Actions step for catalog validation.

### Changed

- SHACL and CQ runner input data now include the common and foundation alignment modules.
- The project has moved from a navigation-focused MVP toward a foundation-aligned ontology architecture.

### Meaning

This development line prepares the MASS Ontology for controlled future alignment with BFO and CCO.

The current status is still exploratory. The repository records draft alignment decisions, but does not 
yet claim full BFO/CCO compliance.

All notable changes to the MASS Ontology project will be documented in this file.

The project follows an iterative research-oriented versioning approach:

- `v0.x.x` versions are exploratory MVP releases;
- `v1.0.0` will indicate a stable ontology stack suitable for publication and reuse.

---

## v0.2.0 — Competency Questions MVP

Release date: 2026-08-17

### Added

- Competency questions document for the MASS Ontology MVP.
- SPARQL queries for CQ-01 ... CQ-08.
- Automated competency question query runner:
  - `scripts/run_cq_queries.py`.
- `make cq` command for local execution of all competency question queries.
- Safety requirement and verification evidence example:
  - `mass:SafetyRequirement`;
  - `mass:VerificationEvidence`;
  - `mass:hasVerificationEvidence`.
- SHACL validation rule for safety requirement verification evidence.
- GitHub Actions step for running competency question SPARQL queries.

### Changed

- CQ-01 and CQ-02 were updated to support subclass-aware querying.
- The MVP now checks not only structural conformance through SHACL, but also answerability of 
competency questions through SPARQL.

### Validation

The release is expected to pass:

```bash
make validate
make cq
```
