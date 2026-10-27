# Governance Decision — MASS-OEF adoption and Roadmap v1.1 approval

**Decision date:** 2026-10-27  
**Status:** APPROVED  
**Context:** MASS Ontology Stack, MASS Semantic Kernel v1.0, DCCR-01…04 (approved)  

## Decisions

1. **ADOPT** *Ontology Engineering Framework for MASS (MASS-OEF)* as the project-wide methodological framework for modular, socio-technical, operational-context and assurance-oriented ontology engineering.
2. **APPROVE** *MASS Ontology Integrated Roadmap v1.1 (MASS-OEF Aligned)* as the governing release roadmap, superseding the previously proposed roadmap dated 2026-10-27.
3. Maintain **BH-P04 / v0.4.0-dev — Observation Core** as the immediate implementation focus with **no scope expansion**. Start with P04-00 (Baseline & Architecture Readiness).
4. Preserve `MASSKernel_v1.0.sysml` (`MASS-SK-1.0`) as immutable; do not change approved DCCR-01…04 through this decision.
5. Distinguish **approval of planning and specifications** from **implementation, test execution, release tagging, compliance demonstration or certification**.

## Execution gate (BH-P04)

Before v0.4.0 release, establish passing evidence for BH-V01, BH-V02, BH-V03, BH-V05, BH-V06, BH-V11 and BH-V12; implement BH-CQ-01…03 with exact expected results, and preserve legacy catalog/SHACL/CQ tests. Future-profile checks are DEFERRED, not PASS.

## Controlled documentation

- `docs/architecture/mass-oef-methodology.md` — adopted MASS-OEF methodology (repository-renderable copy; editorial diagram normalization).
- `docs/architecture/source/mass-oef-original-export.md` — unchanged research source archival copy.
- `docs/roadmap.md` — approved Integrated Roadmap v1.1.
- `docs/reviews/DCCR-01…04` — approved scope/semantics/mappings/validation requirements.

**Note:** Publishing these documents to GitHub requires a separate local Git commit/push (or approved connector action); the files furnished here do not automatically modify the repository.
