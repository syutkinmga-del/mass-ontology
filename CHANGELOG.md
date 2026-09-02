# Changelog

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
