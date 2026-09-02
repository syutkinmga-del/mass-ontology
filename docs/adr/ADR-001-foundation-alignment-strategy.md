# ADR-001: Foundation Alignment Strategy

## Status

Accepted for v0.3.0-dev.

## Date

2026-09-02

## Context

The MASS Ontology project aims to develop a modular ontology stack for Maritime Autonomous Surface Ships.

The intended long-term architecture includes alignment with upper and common ontologies such as BFO and 
CCO.

However, direct early import of BFO and CCO may introduce unnecessary complexity before the MASS domain 
model is stable.

The current ontology already includes:

- MASS Core module;
- Navigation module;
- example encounter scenario;
- SHACL validation;
- competency questions;
- foundation alignment draft;
- MASS Common module.

The project needs a controlled strategy for connecting local MASS concepts to upper-level ontology 
concepts.

## Decision

The project will not import BFO and CCO directly at the early MVP stage.

Instead, the project will first introduce a lightweight local common layer:

- `01-common/common-core.ttl`

and a draft foundation alignment layer:

- `00-foundation/foundation-alignment.ttl`

The local common layer defines intermediate concepts such as:

- `common:System`;
- `common:EngineeredSystem`;
- `common:InformationArtifact`;
- `common:Requirement`;
- `common:Rule`;
- `common:VerificationArtifact`;
- `common:OperationalSituation`;
- `common:OperationalState`;
- `common:Process`;
- `common:Decision`;
- `common:CommunicationChannel`.

The foundation alignment layer records explicit alignment decisions using:

- `foundation:AlignmentDecision`;
- `foundation:alignsLocalEntity`;
- `foundation:proposedFoundationTarget`;
- `foundation:alignmentStatus`.

This allows the project to document candidate mappings to BFO/CCO before committing to full external 
ontology imports.

## Rationale

The main reason for this decision is to reduce modelling risk.

BFO and CCO are powerful, but they require careful ontological commitments. If they are imported too 
early, the MASS Ontology may become harder to understand, harder to validate, and harder to refactor.

The intermediate common layer gives the project a stable local modelling vocabulary while preserving the 
possibility of future alignment.

This is especially important for concepts whose upper-ontology interpretation is not yet final, for 
example:

- `mass:MASSVessel`;
- `mass:OperationalMode`;
- `mass:CommunicationLink`;
- `mass:SafetyRequirement`;
- `mass:VerificationEvidence`;
- `nav:EncounterSituation`;
- `nav:Maneuver`;
- `nav:COLREGRule`.

## Consequences

### Positive consequences

- The project remains lightweight and understandable.
- Local MASS modelling can continue without waiting for final BFO/CCO decisions.
- Alignment assumptions become explicit and reviewable.
- SHACL can validate the structure of alignment decisions.
- SPARQL competency questions can check that alignment decisions are queryable.
- Future BFO/CCO imports can be introduced in a controlled way.

### Negative consequences

- The project is not yet fully BFO/CCO-compliant.
- Some classes may need to be refactored later.
- The common layer may temporarily duplicate concepts that will later be replaced or aligned with 
external ontology terms.

## Alternatives considered

### Alternative 1: Import BFO and CCO immediately

Rejected for the current stage.

This would provide strong ontological grounding, but it would also increase complexity before the MASS 
Core and Navigation modules are stable.

### Alternative 2: Avoid BFO/CCO completely

Rejected.

The project aims to support semantic interoperability and future reuse. Avoiding upper/common ontology 
alignment would limit the long-term value of the MASS Ontology.

### Alternative 3: Use only informal documentation

Rejected.

Informal notes are not enough. Alignment decisions should be represented as RDF data, checked by SHACL, 
queried by SPARQL, and versioned in Git.

## Current implementation

The current `v0.3.0-dev` implementation includes:

- `01-common/common-core.ttl`;
- `00-foundation/foundation-alignment.ttl`;
- `shapes/foundation-alignment.shacl.ttl`;
- CQ-09 ... CQ-12 for foundation alignment;
- expected CQ result checks.

The current alignment decisions are still marked as:

- `draft`

and should not be interpreted as final BFO/CCO mappings.

## Open questions

The following modelling questions remain open:

- Should `mass:MASSVessel` be treated primarily as an engineered system, physical artifact, or material 
entity?
- Should `mass:OperationalMode` be treated as a state, disposition, role, or process profile?
- Should `mass:CommunicationLink` represent a physical communication channel, information channel, 
communication process, or all of them in different contexts?
- Should `mass:VerificationEvidence` be modelled as an information artifact, document, dataset, 
simulation result, or broader evidence entity?
- Should `nav:EncounterSituation` be modelled as an operational situation, process aggregate, event, or 
scenario?
- Should `nav:Maneuver` be represented as a process, planned action, control action, or commanded 
behavior?
- Should `nav:COLREGRule` be represented as a rule, directive information artifact, legal norm, or safety 
constraint?

## Validation strategy

The foundation alignment layer must remain machine-checkable.

The repository should continue to pass:

- SHACL validation;
- competency question SPARQL checks;
- expected CQ result checks;
- GitHub Actions validation.

The expected local validation commands are:

- `make validate`;
- `make cq`.

## Versioning impact

This ADR belongs to the `v0.3.0-dev` development line.

It should be included in the future `v0.3.0` release if the foundation alignment layer remains part of 
the ontology architecture.

## Decision summary

The MASS Ontology will use a controlled, staged foundation alignment strategy:

MASS Common first, explicit alignment decisions second, full BFO/CCO imports later.
