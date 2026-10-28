# MASS Semantic Kernel v1.0 — Scope Boundary & Deferred Gaps

## 1. Baseline Identification

**Baseline ID:** MASS-SK-1.0  
**Baseline Name:** MASS Semantic Kernel v1.0  
**SysML Package:** `MASSKernel`  
**Status:** BASELINE CANDIDATE  

---

# 2. Purpose of the Scope Boundary

The purpose of the MASS Semantic Kernel is to provide a minimal, coherent and validated semantic 
foundation for subsequent MASS domain modeling.

The Semantic Kernel is not intended to represent the complete MASS domain, detailed vessel architecture, 
executable navigation algorithms, complete COLREG reasoning, or full safety-analysis semantics.

MASS-SK-1.0 establishes the concepts and semantic relationships required to support:

- MASS system identity;
- technical and human agents;
- operational functions;
- modes of operation;
- operational conditions;
- Operational Design Domains;
- Operational Envelopes;
- function assignments;
- performer, supervisor and authority-holder roles;
- remote-operation contexts;
- COLREG encounter semantics;
- collision-risk assessment traceability;
- safety applicability;
- semantic invariants;
- competency-question answering.

---

# 3. In-Scope Semantics for MASS-SK-1.0

The following semantic areas are included in the baseline.

## 3.1 System and Agent Foundation

Included:

- `System`
- `Vessel`
- `MaritimeAutonomousSurfaceShip`
- `Agent`
- `HumanAgent`
- `TechnicalAgent`
- `AutonomousNavigationSystem`
- `RemoteOperationsCentre`
- `RemoteOperator`

The kernel establishes the basic distinction between:

- systems;
- vessels;
- technical agents;
- human agents.

---

## 3.2 MASS Functions

Included:

- `MASSFunction`
- `NavigationFunction`
- `CollisionAvoidanceFunction`

The kernel establishes MASS functions as assignable behavioral entities.

Detailed navigation algorithms and implementation logic are outside the baseline.

---

## 3.3 Operational Modes

Included:

- `ModeOfOperation`
- `RemoteOperation`
- `SupervisedAutonomy`
- `AutonomousOperation`
- `MASSOperationalMode`

The kernel represents operational modes as a semantic dimension independent from operational condition.

---

## 3.4 Operational Conditions

Included:

- `OperationalCondition`
- `NormalCondition`
- `DegradedState`
- `FallbackState`
- `MASSOperationalCondition`

The kernel explicitly separates:

**Mode of Operation**

from:

**Operational Condition**

For example:

`RemoteOperation`

is not a subtype of:

`DegradedState`

and vice versa.

---

## 3.5 Operational Design Domain and Operational Envelope

Included:

- `OperationalDesignDomain`
- `OperationalEnvelope`
- relationships between ANS, ODD and MASS Operational Envelope.

The kernel establishes the semantic identity and containment relationships required for ODD/OE reasoning.

Detailed environmental predicates are deferred.

---

## 3.6 Mode–Function Assignment

Included:

- `ModeFunctionAssignment`
- `AutonomousModeFunctionAssignment`

The kernel explicitly represents:

- mode;
- function;
- performer;
- supervisor;
- authority holder;
- effective ODD.

This enables the kernel to express different allocations for the same function under different operating 
modes.

---

## 3.7 Operational Assessment Context

Included:

- `OperationalAssessmentContext`
- `OperationalAssessmentContextIdentity`
- `OperationalConditionAssessment`

These concepts provide traceability between:

MASS  
→ function assignment  
→ effective ODD  
→ operational assessment  
→ required operational condition.

---

## 3.8 Operational Snapshots

Included:

- `OperationalModeSnapshot`
- `OperationalFunctionSnapshot`
- `RemoteOperationSnapshot`

Snapshots represent observations or assertions about operational state at a particular operational 
context.

They do not constitute a complete runtime execution engine.

---

## 3.9 Remote Operation

Included:

- `MASSOperationalSystem`
- `ROCAssociation`
- `RemoteOperationSession`
- `RemoteOperationContext`
- `RemoteOperationContextIdentity`

The baseline supports explicit identification of:

- MASS;
- ROC;
- RemoteOperator;
- remotely operated function;
- session;
- operational snapshot.

---

## 3.10 COLREG Encounter Semantics

Included:

- `COLREGSituation`
- `CrossingSituation`
- `HeadOnSituation`
- `OvertakingSituation`

The kernel can represent the semantic classification of an encounter.

Automatic classification from vessel geometry or trajectories is not part of MASS-SK-1.0.

---

## 3.11 Collision-Risk Semantics

Included:

- `CollisionRiskAssessment`
- `CollisionRiskLevel`
- `AssessmentEvidence`
- `CollisionRiskResult`

The kernel supports traceability:

COLREG Situation  
→ Risk Assessment  
→ Evidence  
→ Risk Level  
→ Result.

The baseline does not define a complete collision-risk algorithm.

---

## 3.12 Control and Safety Semantics

Included:

- `ControlAction`
- `SafetyApplicabilityContext`
- `SafetyConstraint`

The kernel supports:

- identification of the constrained subject;
- identification of the operational context in which a safety constraint applies.

Detailed STPA semantics are deferred.

---

# 4. Explicitly Out-of-Scope for MASS-SK-1.0

The following capabilities are intentionally excluded from the Semantic Kernel baseline.

Their absence is not considered a defect of MASS-SK-1.0.

---

## 4.1 Detailed ODD Environmental Semantics

MASS-SK-1.0 does not yet formally represent detailed ODD dimensions such as:

- wind;
- wave height;
- visibility;
- sea state;
- traffic density;
- bathymetry;
- communication availability;
- GNSS availability;
- sensor performance;
- geographical restrictions.

Current ODD/OE constraints are semantic placeholders.

### Deferred to

MASS Domain Library — Stage 2.

---

## 4.2 Automatic ODD Membership Evaluation

The baseline does not automatically calculate:

`functionWithinODD`

or:

`massWithinOE`.

These values are currently supplied as assessment results to the semantic model.

MASS-SK-1.0 defines the meaning and consequences of those values, rather than the algorithms that 
calculate them.

### Deferred to

Domain Library / analysis and simulation layers.

---

# 5. Deferred Domain-Library Gaps

## DL-GAP-01 — Violation-Specific Fallback Strategies

### Current Kernel Capability

MASS-SK-1.0 can determine that an Operational Envelope violation requires a `FallbackState`.

### Missing Domain Detail

The kernel does not define which fallback strategy shall be selected for a particular violation.

Future semantics may distinguish, for example:

- reduced speed;
- stop;
- loiter;
- safe anchoring;
- remote-control request;
- return to safe area;
- minimum-risk maneuver.

### Classification

**DEFERRED — NOT A BASELINE BLOCKER**

### Target

Stage 2 — MASS Domain Library.

---

## DL-GAP-02 — Maritime Collision-Risk Evidence

### Current Kernel Capability

The kernel supports:

`COLREGSituation`
→ `CollisionRiskAssessment`
→ `AssessmentEvidence`
→ `CollisionRiskLevel`
→ `CollisionRiskResult`.

### Missing Domain Detail

`AssessmentEvidence` is intentionally generic.

Future MASS domain semantics should introduce maritime evidence such as:

- DCPA;
- TCPA;
- CPA;
- relative bearing;
- relative velocity;
- vessel heading;
- speed over ground;
- course over ground;
- AIS observations;
- radar observations;
- sensor-source identity;
- timestamp;
- uncertainty;
- confidence;
- prediction horizon;
- risk algorithm provenance.

### Classification

**DEFERRED — NOT A BASELINE BLOCKER**

### Target

Stage 2 — MASS Domain Library and later Analysis & Simulation stages.

---

## DL-GAP-03 — Concrete Safety Applicability Rules

### Current Kernel Capability

`SafetyConstraint` identifies:

- its constrained subject;
- its applicability context.

`SafetyApplicabilityContext` can reference:

- `COLREGSituation`;
- `MASSFunction`;
- `ControlAction`.

### Missing Domain Detail

The kernel does not yet define detailed rules such as:

- give-way vessel obligations;
- stand-on vessel obligations;
- COLREG-rule applicability;
- navigation hazards;
- unsafe control actions;
- loss scenarios;
- causal factors;
- system-level safety constraints.

### Classification

**DEFERRED — NOT A BASELINE BLOCKER**

### Target

Stage 2 and Stage 7 — Safety Engineering / STPA integration.

---

# 6. Additional Deferred Capabilities

The following limitations are also intentionally deferred.

## 6.1 Automatic COLREG Classification

MASS-SK-1.0 can represent:

- `CrossingSituation`;
- `HeadOnSituation`;
- `OvertakingSituation`.

It does not infer the situation automatically from:

- relative bearing;
- heading;
- trajectories;
- vessel geometry.

**Deferred.**

---

## 6.2 Runtime State Transitions

MASS-SK-1.0 defines operational states but does not model or execute a complete transition machine 
between:

- normal;
- degraded;
- fallback;

or between:

- autonomous;
- supervised;
- remote operation.

State transitions and transition guards are deferred.

---

## 6.3 Automatic Function Activation

The kernel can represent an active function through an `OperationalFunctionSnapshot`.

It does not automatically infer function activation from:

- current mode;
- assignment;
- mission state;
- operational conditions.

**Deferred.**

---

## 6.4 Automatic Remote-Operation Activation

The kernel can represent:

`remoteOperationActive`.

It does not automatically derive that value from the current `ModeOfOperation`.

**Deferred.**

---

## 6.5 Automatic Assignment-to-Snapshot Derivation

`ModeFunctionAssignment`

and:

`OperationalFunctionSnapshot`

are semantically related, but the kernel does not automatically generate one from the other.

**Deferred.**

---

## 6.6 Detailed ControlAction Semantics

`ControlAction` provides a minimal semantic representation of:

- issuing agent;
- affected system.

Detailed control-flow semantics, commands, feedback, timing and STPA-compatible control structures are 
deferred.

---

## 6.7 STPA Integration

MASS-SK-1.0 does not yet provide complete semantics for:

- Loss;
- Hazard;
- System-Level Constraint;
- Controller;
- Controlled Process;
- Unsafe Control Action;
- Feedback;
- causal scenario.

These concepts will be evaluated against the SysML v2 STPA library during later safety-model development.

---

# 7. Kernel vs. Domain Library Boundary

The architectural separation is:

```text
MASS Semantic Kernel
        │
        │ defines stable semantic primitives
        ▼
MASS Domain Library
        │
        │ adds maritime-domain specialization
        ▼
Reference Architecture
        │
        ▼
Operational / Autonomy Models
        │
        ▼
Safety / STPA Models
        │
        ▼
Analysis & Simulation
```

The Semantic Kernel therefore answers:

> What fundamental concepts and relationships must exist?

The MASS Domain Library will answer:

> What concrete maritime concepts, values, rules, measurements and specializations populate those 
relationships?

---

# 8. Baseline Release Criterion for Deferred Gaps

A deferred gap does not block MASS-SK-1.0 if all of the following are true:

1. the missing capability belongs to domain specialization rather than kernel semantics;
2. its absence does not introduce a contradiction into the current kernel;
3. its absence does not invalidate an existing semantic invariant;
4. the kernel provides an extension point for adding the capability later;
5. CQ1–CQ12 remain answerable at the intended Semantic Kernel abstraction level.

All currently identified deferred gaps satisfy these criteria.

---

# 9. Scope Decision

The following kernel-blocking gaps have been closed:

- K-GAP-01 — CLOSED
- K-GAP-02 — CLOSED
- K-GAP-03 — CLOSED
- K-GAP-04 — CLOSED

The following gaps are formally deferred:

- DL-GAP-01 — DEFERRED
- DL-GAP-02 — DEFERRED
- DL-GAP-03 — DEFERRED

Additional executable and domain-detail capabilities identified in Section 6 are also deferred to later 
development stages.

No currently identified deferred capability prevents release of the MASS Semantic Kernel baseline.

---

# 10. Stage 1.4-D Conclusion

The scope boundary of MASS-SK-1.0 is explicitly defined.

MASS-SK-1.0 represents a:

**minimal validated semantic foundation**

and not a:

**complete executable MASS domain model**.

The distinction between Semantic Kernel responsibilities and subsequent MASS Domain Library 
responsibilities is therefore established.

**Stage 1.4-D — Scope Boundary & Deferred Gaps: PASS**

The baseline remains:

**BASELINE CANDIDATE**

pending completion of Stage 1.4-E.
