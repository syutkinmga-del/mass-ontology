# P04-06 — GitHub Actions CI evidence

**Status:** CI VALIDATION PASS / EVIDENCE READY FOR COMMIT

**Implementation commit:** `68e1c4f454caf85958806d761b3a671b51c7803c`

**Verified workflow run:** https://github.com/syutkinmga-del/mass-ontology/actions/runs/41996276523

**GitHub Actions conclusion:** `success`, `push` on `main`, run #1, attempt 1.

**Original artifact:** https://github.com/syutkinmga-del/mass-ontology/actions/runs/41996276523/artifacts/13400003022

**Archive SHA-256:** `84ad7fa2fce3f7d9d4817229040e018698ed1fb6bd7262035ec908bd76020649`

The complete downloaded source artifact is preserved byte-for-byte in `github-actions-run-41996276523.zip`; it contains all 10 gate logs, `pytest.xml`, the BH-V and BH-CQ JSON reports, the summary, and the original 15-line SHA256SUMS. All 15 original file hashes and the ZIP hash were independently verified. Provider artifact retention is 30 days, while this committed archive remains part of Git history.

## Evidence results

| Control | Outcome |
|---|---|
| Preflight + 10 mandatory gates | **11/11 PASS** |
| JUnit pytest | **115 tests, 0 failures, 0 errors, 0 skipped** |
| BH-V01, V02, V03, V05, V06, V11, V12 | **7/7 PASS** |
| BH-CQ-01, -02, -03 | **18 + 9 + 18 rows, exact bindings PASS** |
| Legacy CQ-01…CQ-14 | **PASS** |
| T-04 external RDF lock | **PASS** |
| MASS-SK-1.0 source byte integrity | **PASS** |

## Immutable hashes

- MASS-SK-1.0: `1701bbb86e24588660ef717f2ff7f276b63c938d8569d4511dc19c42033aa788`.
- T-04 lock: `ebacb2bd81ed836df52fb2915a386fb54daef07d479b9f6bbfd9d84f5278f4af`.
- P04-04 synthetic fixture: `2f73990cd4dc88fd4e21c4694d35c6628d0afac613080434d33deed3f41cf301`.
- ROBOT 1.9.11 JAR: `53cd275c8e4c0dad1fc2c1c34174876795cd7d6b6926e1444adcbb0cb3c7ab26`.

## Execution environment

Ubuntu 24.04.5; Python 3.12.15; Java Temurin 21.0.13+9; ROBOT/HermiT 1.9.11; `rdflib==7.6.0`, `pyshacl==0.40.1`, `pytest==9.1.1`. Python transitive dependencies and exact Java binary are not bytewise pinned.

## Verification

From the repository root:

```bash
shasum -a 256 -c docs/evidence/P04-06/FILES.sha256
python3 docs/evidence/P04-06/verify_evidence.py
```

`artifact-SHA256SUMS` is a verbatim copy of the original ZIP's integrity manifest; its relative paths refer to **entries inside the archived run**, not the repository root.

## Scope boundary

Evidence documents a successful run on the implementation commit. A separate evidence commit triggers a **new** workflow run and must be checked independently. P05/P09 and their BH-V/BH-CQ checks are DEFERRED. No SysML parser execution, real AIS model accuracy, navigation safety certification, BFO/CCO full import validation, or v0.4.0 release is claimed.
