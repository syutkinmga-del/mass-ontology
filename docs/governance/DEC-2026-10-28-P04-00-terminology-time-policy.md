# Governance Decision — P04-00 Terminology & Time Policy

**Decision date:** 2026-10-28  
**Status:** APPROVED  
**Reference:** [Terminology, IRI, Time and Segmentation Policy](../architecture/P04-00-terminology-time-policy.md)  
**Authority:** Project owner approval in conversation, 2026-10-28

## Decision

Approve the P04-00 Terminology & Time Policy with all four clarifications:

- **T-01:** Separate observed/event, result and receiver times; document AIS event-time uncertainty and any reconstruction.
- **T-02:** Reject AIS unavailable/sentinel values before creating valid QUDT measurements; preserve raw codes.
- **T-03:** Use versioned deterministic segmentation for P04 synthetic data, `[start,end)` sample ownership and explicit coverage gaps.
- **T-04:** Pin SOSA/SSN, QUDT, OWL-Time and PROV-O artifacts/version/IRIs/checksums before P04-03 and BH-V11 acceptance.

## Boundaries

- Valid for v0.4.0-dev / BH-P04 Observation Core synthetic fixture and conceptual time policy.
- **Not approved:** full external ontology imports; real AIS timestamp reconstruction method; empirically chosen AIS segmentation thresholds; BFO/CCO formal alignment; v0.5 InteractionBehavior / SemanticBehavior; v0.6 OperationalConfiguration.
- DCCR-01…04 and MASSKernel_v1.0.sysml remain unchanged.
- P04-00 completion additionally requires evidence for legacy tests, controlled SysML source/hash and remaining architecture/source registry gates.

## Implementation follow-up

Check P04 fixture metadata and negative cases against T-01…T-04. Record source snapshot checksums in `docs/standards/normative-source-registry.md` when selected, without falsely marking still-pending choices PASS.
