# P04-01 — Local Validation Evidence

**Recorded UTC:** 2026-11-02T09:34:12.395401+00:00
**Overall result:** **PASS**
**Implementation commit:** `18f1dc21e786368a2bf0156961610e6c892e646a`
**Tested Git HEAD:** `18f1dc21e786368a2bf0156961610e6c892e646a`
**Kernel SHA-256:** `1701bbb86e24588660ef717f2ff7f276b63c938d8569d4511dc19c42033aa788`
**Kernel reference SHA-256:** `1701bbb86e24588660ef717f2ff7f276b63c938d8569d4511dc19c42033aa788`

## Executed checks

| Check | Status | Exit code | Log |
|---|---|---:|---|
| P04-01-8-tests | **PASS** | 0 | [P04-01-8-tests.log](./P04-01-8-tests.log) |
| LEGACY-catalog | **PASS** | 0 | [LEGACY-catalog.log](./LEGACY-catalog.log) |
| LEGACY-validate | **PASS** | 0 | [LEGACY-validate.log](./LEGACY-validate.log) |
| LEGACY-cq14 | **PASS** | 0 | [LEGACY-cq14.log](./LEGACY-cq14.log) |
| FULL-pytest | **PASS** | 0 | [FULL-pytest.log](./FULL-pytest.log) |
| KERNEL-integrity | **PASS** | 0 | [KERNEL-integrity.log](./KERNEL-integrity.log) |

## Evidence integrity

Each log SHA-256 is recorded in `validation-results.json`.
Git implementation SHA is captured **before** creating this evidence record.
The future evidence-documentation commit has a different SHA by design.

## Scope limits

This evidence verifies the P04-01 local test suite, legacy commands and immutable MASS-SK-1.0 source. It does not establish full BH-V01 or BH-CQ-01..03 PASS; these require the later Observation Core implementation and test fixtures. It is not a rerun of the SysML v2 Pilot Implementation.
