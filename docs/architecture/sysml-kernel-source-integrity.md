# P04-00 — SysML Semantic Kernel Source & Integrity Control

**Control record date:** 2026-10-28  
**Baseline ID:** `MASS-SK-1.0`  
**Reference SysML package:** `MASSKernel`  
**Current result:** SOURCE IDENTITY / BYTES VERIFIED; final repository installation and independent SysML tool validation must be evidenced separately.  
**Relation to roadmap:** Required source-integrity reference for P04-00 and BH-V12; does not change v0.4 ontological scope.

## 1. Controlled location in MASS Ontology

Repository-relative reference snapshot:

`baselines/sysml/MASS-SK-1.0/`

This is a **read-only, byte-for-byte archival copy** of the released Semantic Kernel supplied with project artifacts. It is not an additional live source tree, not an OWL module, not a SysML build target, and not permission to edit MASS-SK-1.0 in place.

The original external system of record (if separately maintained) **has not been independently verified**. This repository reference copy is the source-of-truth *snapshot for the MASS Ontology integration and tests*, identified by checksum.

## 2. Controlled artifacts

| Artifact | Purpose |
|---|---|
| `MASSKernel_v1.0.sysml` | Released source baseline; immutable reference |
| `MASSKernel_v1.0.sha256` | Original named-source SHA-256 checksum |
| `MASSKernel_v1.0_manifest.md` | Declared 62 production definitions / SK1–SK16 inventory |
| `MASSKernel_v1.0_validation_record.md` | Historical Pilot Implementation semantic and CQ evidence (candidate phase) |
| `MASSKernel_v1.0_scope_boundary.md` | Stage 1 / Stage 2 boundary and deferred capabilities |
| `MASSKernel_v1.0_change_control.md` | Release and change-governance policy |
| `artifact-integrity-manifest.json` | File hashes, sizes, provenance and controlled snapshot metadata |

## 3. Exact released bytes

- Released SHA-256: `1701bbb86e24588660ef717f2ff7f276b63c938d8569d4511dc19c42033aa788`
- Released source size: **18,796 bytes**.
- Verified against **both** original `MASSKernel_v1.0.sha256` and the release manifest in the supplied project artifacts.
- Candidate source (`MASSKernel_v1.0_candidate.sysml`) has SHA-256 `0a9a2440c490daf23dce0735f61a3383b85e3280bf0c72626979522e56eb6d81` and is **not** the released baseline. Only release-status comments differ in an observed candidate-versus-release diff.
- Individual hashes for all control documents appear in `artifact-integrity-manifest.json`.

## 4. Evidence levels — do not conflate

| Claim | Evidence | Status |
|---|---|---|
| Exact source bytes equal supplied released file | SHA-256 independent recalculation | **PASS** in preparation environment, 2026-10-28 |
| Matching original SHA file / baseline manifest | Hash comparisons | **PASS** |
| Historical SysML invariants SK1–SK16, CQ1–CQ12 | Released project validation record | **DOCUMENTED HISTORICALLY**, not rerun here |
| Exact archived file accepted by SysML v2 Pilot Implementation today | New tool execution needed | **NOT VERIFIED** |
| Git repository copy and regression check in user Mac | Install, commit, push and local test logs | **PENDING** until executed |

**Known concern SK-SRC-01:** the originally supplied released file begins with a literal `Skip to main panel` line and a standalone `/` at line 7 before `package MASSKernel`. These are not being silently deleted. They may obstruct parsing of the exact file as standalone SysML text. Verify with the tool; preserve original release hash and use a separately named diagnostic derivative or formally versioned corrective release if needed. The old validation record names the *candidate* source; although source diff shows only release-header comment changes, independent re-validation of the actual release bytes is not claimed.

## 5. Change-control contract

1. Never edit `baselines/sysml/MASS-SK-1.0/MASSKernel_v1.0.sysml` in place.
2. Do not alter original companion documents when adding new evidence; add dated evidence separately.
3. Any intentional byte change requires a **new** versioned source and decision record; changing comments also changes the source SHA.
4. Use `python3 scripts/verify_sysml_kernel_integrity.py` to verify the committed archival copy.
5. `pytest` verifies the positive baseline and that mutated content is rejected; this checks **identity and bytes**, not SysML semantic validity.
6. Never map SysML runtime-generated UUIDs to persistent baseline identifiers; use controlled package/definition names and explicit mappings as designed in DCCR.
7. `MASSKernel` source is a reference; v0.4's RDF/OWL ontology modules are independently versioned and must not mutate the SysML baseline.

## 6. Continuation into P04-01 / P04-07

- P04-01 may reference the stable generic `MASSKernel::Vessel` without modifying this source; the concrete OWL mapping remains a design decision.
- BH-V12 may assert the hash equals `1701bbb86e24588660ef717f2ff7f276b63c938d8569d4511dc19c42033aa788` and the legacy ontology tests remain green.
- The release gate must **not** transform a historical Pilot Implementation PASS into a current tool execution PASS.
- The original source byte/syntax concern SK-SRC-01 stays explicitly registered for reproducibility work outside source-identity verification.

**Decision record:** [`DEC-2026-10-28-P04-00-sysml-kernel-source-control.md`](../governance/DEC-2026-10-28-P04-00-sysml-kernel-source-control.md).
