# ADR (Proposed) — OperationalConfiguration as a Future Integration Context

**Status:** PROPOSED / DEFERRED TO v0.6.0 — NOT APPROVED FOR OWL IMPLEMENTATION
**Registered:** 2026-10-28
**Context:** MASS-OEF and Roadmap v1.1, P04-00 scope preservation

## Context

MASS-OEF proposes an operational-configuration context connecting Vessel, ModeOfOperation, FunctionAllocation, ODD, HumanOversight, Connectivity and ApplicableRules. The approved SysML MASS-SK-1.0 already defines mode, condition, ODD, agent/authority and mode-function-assignment concepts with distinct meanings. A separately versioned OWL integration layer is required; we do not overwrite SysML semantics or equate a behavior label with an operational mode.

## Proposed decision (future v0.6)

Model `OperationalConfiguration` as a *temporally qualified information/integration context* referring to a vessel and effective operating situation. Capture the identity and time validity of performer, supervisor and authority-holder roles, applicable ODD, link availability, functions and regulatory applicability. Review whether a snapshot, planned configuration, approved configuration and observed runtime configuration need distinct kinds and explicit provenance.

## Design boundaries

- `OperationalConfiguration` is **not** `bh:TemporalUnit`, `ModeOfOperation`, `OperationalCondition` or `nav:EncounterSituation`.
- Do not assert that an ODD automatically conforms to the observed conditions; require an evidence-bearing assessment.
- `Connectivity` status does not itself grant or transfer command authority.
- `ApplicableRules` should be linked through conditional applicability assessment, not implied globally by a class restriction.
- Use explicit temporal qualification of function allocations and authority transitions (handover/takeover).
- Runtime decisions/control actuation are outside an OWL inference engine's authority.
- Detailed schema and class mappings require a later DCCR/ADR + relevant competency questions and scenario fixtures.

## Pilot trace

The future loss-of-ROC-link encounter scenario is sliced by roadmap: P04 sensor/track data → P05 spatial interaction → v0.6 operational configuration and communication failure → v0.7 safety/requirements/evidence → v0.8 versioned system model → v0.9 research ML/simulation. P04 only records this trace.

## Current disposition

**NO implementation in P04.** Keep this as a proposed design record; revisit for v0.6 architecture review, scope and provenance decision. Any future `owl:Class OperationalConfiguration` requires an explicitly approved specification and tests.
