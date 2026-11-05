# P04-06 — BH-P04 CI Integration

**Project:** MASS Ontology / MASS-OEF v1.1.
**Input baseline:** P04-05 implementation + evidence, commit `6113ed1581a59602be67227ce3ad3730b4e6563d`.
**Status:** IMPLEMENTATION CANDIDATE — CI execution and publication evidence required.
**Scope:** BH-P04; P05/P09 DEFERRED. No production-ontology, SysML, historical P04-03 or pinned T-04 snapshots changed.

## Architecture and command contract

The existing `.github/workflows/validate.yml` remains unchanged. A separate
`.github/workflows/behavior-validation.yml` runs on pushes/PRs targeting `main`
and can be manually dispatched. The single source of execution truth is:

```bash
make behavior-test
```

`Makefile` adds that target without modifying existing `catalog`, `validate`, `cq`, or `test` recipes.
It runs `scripts/run_behavior_ci.py --profile p04 --report-dir run/behavior-ci` in the project venv.
The runner is fail-closed: only a **fresh** status PASS for every gate yields exit code 0.
Prior P04-04/05 evidence is a source-traceability baseline, not substituted for newly executed tests.

## Mandatory P04 gates

1. Verify Python 3.12, `rdflib==7.6.0`, `pyshacl==0.40.1`, `pytest==9.1.1`, Java 21, ROBOT 1.9.11 and verified source ancestor P04-05.
2. Byte-regenerate P04-03 and P04-04 fixtures in `--check` mode only.
3. `make catalog`, `make validate`, `make cq` (unchanged CQ-01…CQ-14).
4. Confirm immutable MASS-SK-1.0 SHA-256 and archived companion evidence.
5. Offline T-04 `--verify`, including owner license approval; no external RDF network fetch.
6. Run all Python tests with JUnit XML. Enforce zero failures, zero errors and **zero skipped** (including independent HermiT and SHACL tests). At least 90 previously published P04 tests expected; the P04-06 meta-tests are additive.
7. Re-run BH-V01/V02/V03/V05/V06/V11/V12 with `--legacy`; assert explicit PASS for every required ID, checked commit SHA and complete legacy subprocess evidence.
8. Re-run BH-CQ-01…03; assert `exact_bindings=true` and (18, 9, 18) expected/actual rows, not just successful process exit.

**P04 exclusions:** BH-V04/V07/V08/V09/V10 and BH-CQ-04..10 are future-profile rules; they are **DEFERRED**, never PASS. Passing this CI does not validate real AIS, ship motion safety or current SysML parser semantics.

## Reproducibility and source integrity

- GitHub-hosted `ubuntu-24.04`, Python 3.12 and Temurin Java 21.
- The four GitHub Actions are pinned to verified immutable commit hashes (documented in workflow comments).
- ROBOT v1.9.11 downloaded from official `ontodev/robot` GitHub release and SHA-256 checked against `ci/robot-v1.9.11.sha256` **before execution**.
  Hash from GitHub release asset API: `53cd275c8e4c0dad1fc2c1c34174876795cd7d6b6926e1444adcbb0cb3c7ab26`.
- Python direct dependencies pinned in `ci/requirements-behavior-ci.txt`, matching published P04-05 environment. **Transitive Python dependencies and exact Temurin patch build are not bytewise pinned**. P04-06 provides version-constrained automation, not a fully hermetic build; a future locked dependency set is needed for strict long-term binary reproducibility.
- External ontologies remain locally pinned by T-04 RDF SHA-256. No `owl:imports` are introduced in MASS production files.
- Workflow requests only `contents: read`, does not use `pull_request_target` and saves artifacts even on test failure.

## Evidence semantics

`run/behavior-ci/` is ignored by Git (`run/` is already in `.gitignore`) and uploaded as a GitHub Actions artifact for each invocation. It contains:

```text
report.json               # gate statuses, git commit, environment
summary.md                # short human-readable table
pytest.xml                # test execution, with skipped count
behavior-validation.json  # formal BH-V result statuses
behavior-cq.json          # exact SPARQL binding test status
logs/                     # stdout and stderr by gate
SHA256SUMS                # hashes of all generated evidence files
```

A workflow green check is **not** available until GitHub Actions itself executes the published implementation and all conditions PASS. The implementation commit must be distinct from the follow-on acceptance/evidence commit. For P04-07, preserve the GitHub Actions run URL, source commit, workflow SHA and downloaded evidence digest in `docs/evidence/P04-06/`.

## Local execution (after install)

```bash
cd ~/Projects/mass-ontology
.venv/bin/python -m pytest -v tests/test_p04_06_ci.py
make behavior-test
cat run/behavior-ci/summary.md
cd run/behavior-ci && shasum -a 256 -c SHA256SUMS
```

Local Make target requires exact documented package versions and ROBOT 1.9.11 in PATH. A wrong version or missing reasoner is BLOCKED, not a green/skip.

## GitHub acceptance checklist

1. Implementation commit with only workflow, runner, tests, docs, pins and Make target.
2. GitHub Actions run `BH-P04 Behavior Validation` on `main`: all required gates PASS; no SKIPPED; JUnit XML present.
3. Preserve evidence artifact; record run URL, conclusion `success`, triggering commit and artifact SHA-256.
4. Publish a **separate** evidence commit. Any new push retriggers workflow; ensure latest evidence commit also has a successful run. P04-07 release review remains pending.
