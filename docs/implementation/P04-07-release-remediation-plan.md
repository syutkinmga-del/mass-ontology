# P04-07 — Remediation and Controlled Release Procedure

**Baseline reviewed:** `11491acb0685e69c0aed6ec749eea4d138162b30`.  
**Status:** Review package ready; release v0.4.0 **NOT YET APPROVED**.

## Phase A — publish an independent NO-GO review (no source edits)

Install the P04-07 review files, run:

```bash
.venv/bin/python -m pytest -v tests/test_p04_07_release_review.py
.venv/bin/python scripts/review_release_p04.py --repo "$PWD"
# Expected: NO_GO, exit code 2. This is an expected policy result, not an ontology regression.
```

Stage **only** the new review documents, template, draft, test and script; `git diff --cached --check`; commit as `Record P04-07 release readiness review (NO-GO)` and push. Dedicated BH-P04 CI must continue passing. The script creates a review report under ignored `run/release-review/`; optionally copy that JSON into a dated directory under `docs/evidence/P04-07/` for the review commit, without editing historical evidence.

## Phase B — resolve release packaging findings (separate PR/commit)

1. **RR-04 owner choice FIRST:** Determine copyright holder and a legally appropriate project license; confirm coverage of the authored OWL, scripts, examples and documentation. A public repository is not the same thing as an explicit reuse grant. Do not fill `LICENSE` with a guessed license.
2. **RR-05:** Prepare a vetted `THIRD_PARTY_NOTICES.md`. Record QUDT.org CC BY 4.0 credits/link and unchanged snapshots; preserve W3C + OGC rights notices and applicable terms; inspect OWL-Time/PROV-O actual source notices. Keep T-04 byte locks unchanged. Use the bundled template as an **editorial checklist**, not as approved final legal text.
3. **RR-02:** Update README and `docs/index.md` to the actual BH-P04 scope; correct the executable example to `make behavior-test`, explicitly include `make catalog`, `make validate`, `make cq`, fixture limitations and P05/P09 DEFERRED. Close all Markdown code fences.
4. **RR-03:** Record a new v0.4.0 section in `CHANGELOG.md`, retaining historical entries; record generic Vessel, trajectory, observations, QUDT v3.5.3 migration, reasoner validation, 3 strict BH-CQs, CI and evidence. Close the existing Markdown fence.
5. **RR-01:** Reconcile `VERSION` and `pyproject.toml` to `0.4.0` only as part of the controlled release candidate. Version labels are project metadata, **not** proof that a GitHub release was published.
6. **RR-06:** Copy/edit `docs/releases/v0.4.0-release-notes-DRAFT.md` into a final `docs/releases/v0.4.0-release-notes.md` after review. Retain scope and limitations.

## Phase C — release candidate verification

```bash
make behavior-test
.venv/bin/python scripts/review_release_p04.py --repo "$PWD"
```

The second command will return NO_GO until the **explicit owner decision** is recorded. This is expected. Publish the candidate changes as a separate implementation/release-preparation commit. Require successful new GitHub Actions runs on that commit, no skipped tests, complete evidence and a clean working tree before approval.

## Phase D — approval (owner-only) and release

Review P04-07 formal findings, rights, license, public docs, candidate SHA and fresh GitHub Actions run URL. Fill a **new** `docs/governance/DEC-P04-07-v0.4.0-release.md` from the bundled governance template and obtain an actual dated owner decision; never pre-populate `APPROVED FOR RELEASE` before approval.

Once the decision itself is published, rerun the readiness script and ensure all 10 gates PASS. Check the GitHub Actions run for the decision commit. Then, and only then, tag the final commit:

```bash
# ONLY AFTER THE SIGNED GO AND ALL PASS
# git fetch origin --tags
# git status --porcelain
# git tag -a v0.4.0 -m "MASS Ontology v0.4.0 — BH-P04 Observation Core"
# git push origin v0.4.0
```

The commands are commented intentionally: the review package does **not** create a release tag or GitHub Release. The project owner makes the release decision.

## Explicit boundaries

P04 success is demonstrated against a controlled synthetic AIS-like dataset. This release cannot claim real AIS decoding, actual ship movement predictive performance, COLREG decision safety, Roc/VTS control, production certification, resolved BFO/CCO axioms, external `owl:imports`, or fresh SysML semantic parser validation. Deferred profiles are **BH-P05** and **BH-P09**.
