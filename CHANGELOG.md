# Changelog

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
