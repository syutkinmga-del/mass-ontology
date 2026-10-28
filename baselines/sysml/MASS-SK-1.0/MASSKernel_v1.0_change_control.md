# MASS Semantic Kernel v1.0 — Change-Control & Baseline Release

## 1. Baseline Identification

**Baseline ID:** MASS-SK-1.0  
**Baseline Name:** MASS Semantic Kernel v1.0  
**SysML Package:** `MASSKernel`  
**Language:** SysML v2  
**Validation Environment:** OMG SysML v2 Pilot Implementation  

Initial status:

**BASELINE CANDIDATE**

Target status after successful completion of this procedure:

**RELEASED**

---

# 2. Purpose of Change Control

The purpose of baseline change control is to preserve the validated semantic properties of `MASSKernel` while allowing controlled evolution of the MASS Digital Engineering Framework.

Once MASS-SK-1.0 is released, the baseline source shall not be edited in place.

Any subsequent semantic modification shall result in a new controlled version of the kernel.

The released baseline therefore acts as:

- a stable semantic reference;
- a regression reference;
- an integration contract for the MASS Domain Library;
- a traceable starting point for subsequent architecture, safety and analysis models.

---

# 3. Controlled Baseline Artifacts

The MASS-SK-1.0 release consists of the following controlled artifacts.

### 3.1 Production SysML source

`MASSKernel_v1.0.sysml`

Contains the released `MASSKernel` SysML v2 package.

---

### 3.2 Baseline Content Manifest

`MASSKernel_v1.0_manifest.md`

Records the production definitions included in the baseline.

Baseline inventory:

**62 top-level production definitions**

No E4, CQ or other test packages are included in the production namespace.

---

### 3.3 Validation and Evidence Record

`MASSKernel_v1.0_validation_record.md`

Records:

- Stage 1.2 semantic validation;
- SK1–SK16 validation;
- K-GAP-01 through K-GAP-04 closure;
- CQ1–CQ12 validation;
- E4-A through E4-D final regression evidence.

---

### 3.4 Scope Boundary

`MASSKernel_v1.0_scope_boundary.md`

Records:

- in-scope Semantic Kernel semantics;
- explicitly out-of-scope capabilities;
- deferred Domain Library gaps;
- boundary between Semantic Kernel and Stage 2.

---

### 3.5 Change-Control Record

`MASSKernel_v1.0_change_control.md`

Defines the rules for maintaining and changing the released baseline.

---

# 4. Release Preconditions

MASS-SK-1.0 may be released only if all Stage 1 validation gates are satisfied.

| Gate | Result |
|---|---|
| 1.4-A Baseline Identification | PASS |
| 1.4-B Baseline Content Manifest | PASS |
| 1.4-C Validation & Evidence Record | PASS |
| 1.4-D Scope Boundary & Deferred Gaps | PASS |
| Stage 1.2 SysML v2 Semantic Validation | PASS |
| SK1–SK16 Regression | PASS |
| E4-A Structural / Namespace Review | PASS |
| E4-B Invariant Regression | PASS |
| E4-C Cross-Semantic Contradiction Review | PASS |
| E4-D CQ1–CQ12 Regression | 12/12 PASS |
| Kernel gaps K-GAP-01–04 | CLOSED |
| Kernel-blocking unresolved gaps | NONE |

All release preconditions are satisfied.

---

# 5. Baseline Immutability Rule

After release, the file:

`MASSKernel_v1.0.sysml`

shall be treated as immutable.

It shall not be used as the working file for Stage 2 development.

New work shall be performed either:

1. in packages importing `MASSKernel`, or
2. in a new kernel development version if the Semantic Kernel itself must change.

This provides the distinction:

```text
Released baseline
MASSKernel_v1.0.sysml
        │
        │  DO NOT MODIFY
        ▼
stable semantic contract


Development
        │
        ├── MASS Domain Library
        ├── Reference Architecture
        ├── Operational Models
        ├── STPA Models
        └── future MASSKernel versions
```

---

# 6. What Constitutes a Baseline Change

A baseline change occurs if the semantics of `MASSKernel` are modified.

Examples include:

- adding or removing a definition;
- changing specialization;
- changing a definition type;
- changing multiplicity;
- changing containment or reference semantics;
- changing `part`, `ref`, `item`, `action`, `state`, `occurrence`, `connection`, or `requirement` relationships;
- changing a constraint expression;
- changing constraint bindings;
- changing assignment semantics;
- changing performer, supervisor or authority-holder semantics;
- changing ODD/OE semantics;
- changing remote-operation identity semantics;
- changing COLREG semantics;
- changing collision-risk traceability;
- changing safety-applicability semantics;
- changing the interpretation of an existing competency question.

Any such modification requires a new kernel version and regression validation.

---

# 7. Changes That Do Not Alter Kernel Semantics

The following changes do not by themselves constitute a semantic modification:

- correcting comments;
- improving documentation;
- correcting spelling inside comments;
- adding explanatory comments;
- updating external Markdown documentation;
- changing formatting that does not affect SysML syntax or semantics.

Such changes must still be traceable but do not require a new semantic baseline version unless the released source artifact itself is replaced.

---

# 8. Versioning Policy

The following project versioning policy applies to the MASS Semantic Kernel.

## 8.1 Patch Version

Example:

`1.0 → 1.0.1`

Use for non-breaking corrective changes that do not change the conceptual meaning or public semantic contract of the kernel.

Examples may include:

- correction of a non-semantic source defect;
- clarification required for tool compatibility;
- minor corrective adjustment proven not to change intended semantics.

Required validation shall be determined from the affected construct, with full regression required whenever semantic behavior may have changed.

---

## 8.2 Minor Version

Example:

`1.0 → 1.1`

Use when new backward-compatible Semantic Kernel capability is added while existing concepts and validated contracts remain valid.

Examples:

- introducing a new kernel concept;
- adding a new invariant;
- adding a new competency question;
- adding a new traceability relationship without invalidating existing semantics.

A minor Semantic Kernel release requires full baseline regression.

---

## 8.3 Major Version

Example:

`1.x → 2.0`

Use for breaking semantic changes.

Examples:

- changing the meaning of an existing concept;
- changing the Agent hierarchy incompatibly;
- changing the Mode / OperationalCondition separation;
- replacing assignment semantics;
- changing multiplicities that invalidate existing models;
- removing a production concept;
- changing CQ interpretation incompatibly;
- changing a semantic contract relied upon by the MASS Domain Library.

A major release requires complete revalidation of the Semantic Kernel and impact analysis of dependent models.

---

# 9. Regression Policy

## 9.1 Documentation-Only Change

If no SysML semantics change:

**Required:**

- source load sanity check if the SysML source file itself changed.

Full SK/CQ regression is not required.

---

## 9.2 Semantic Change to MASSKernel

For any semantic change to `MASSKernel`:

**Required:**

1. SysML v2 load / semantic validation;
2. relevant structural validation;
3. SK1–SK16 regression;
4. cross-semantic contradiction review;
5. CQ1–CQ12 regression;
6. gap review;
7. update of Baseline Manifest;
8. update of Validation Record;
9. update of Scope Boundary if applicable.

The default policy is:

**any Semantic Kernel change triggers full kernel regression.**

---

## 9.3 Stage 2 Domain-Library Extension

If a new Stage 2 package merely imports MASS-SK-1.0 and `MASSKernel` remains unchanged:

a new Semantic Kernel version is not required.

Instead, integration validation shall demonstrate that the Domain Library does not contradict the kernel semantic contracts.

---

# 10. Regression Protection Rules

Future changes shall preserve the following architectural decisions unless a new major baseline explicitly supersedes them:

1. `ModeOfOperation` and `OperationalCondition` are separate semantic dimensions.

2. `DegradedState` and `FallbackState` are not subtypes of `ModeOfOperation`.

3. `COLREGSituation` is modeled as an occurrence.

4. ODD and Operational Envelope are operational specifications, not physical vessel parts.

5. ANS is a technical Agent capable of acting as a performer.

6. `ModeFunctionAssignment` explicitly distinguishes:
   - performer;
   - supervisor;
   - authority holder;
   - effective ODD.

7. Collision-risk result remains traceable to its assessment context.

8. Safety constraint remains traceable to:
   - constrained subject;
   - applicability context.

9. Remote-operation session identity remains traceable to:
   - MASS;
   - ROC;
   - RemoteOperator;
   - relevant functions;
   - remote-operation context.

10. Kernel-level changes must not silently invalidate CQ1–CQ12.

---

# 11. Deferred Gaps Do Not Trigger Baseline Reopening

The following currently deferred gaps do not invalidate MASS-SK-1.0:

- DL-GAP-01 — violation-specific fallback strategies;
- DL-GAP-02 — detailed maritime collision-risk evidence;
- DL-GAP-03 — concrete safety-applicability rules.

Their implementation in Stage 2 does not require modification of MASS-SK-1.0 unless implementation reveals a genuine deficiency in the Semantic Kernel itself.

If such a deficiency is discovered, it shall be recorded as a new kernel gap and processed through formal change control.

---

# 12. Release Decision

The MASS Semantic Kernel has completed:

- concept definition;
- relationship and multiplicity definition;
- SysML v2 semantic validation;
- kernel consistency validation;
- invariant regression;
- competency-question validation;
- contradiction review;
- kernel gap closure;
- scope-boundary definition.

No known unresolved kernel-blocking semantic gap remains.

Therefore the baseline is eligible for release as:

**MASS Semantic Kernel v1.0**

**Baseline ID: MASS-SK-1.0**

---

# 13. Release Status

Upon completion of the final source-file release procedure:

**Status: RELEASED**

This establishes MASS-SK-1.0 as the semantic foundation for:

**Stage 2 — MASS Domain Library**

and subsequent MASS Digital Engineering Framework stages.
