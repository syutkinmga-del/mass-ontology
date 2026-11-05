# P04-07 — Remediation of release findings RR-01…RR-06

**Repository baseline:** `d6fc03c5b95e36e809cd1012390d16b7b1d1a0c6` (published NO-GO review).
**Target:** `v0.4.0` BH-P04 **release candidate**, NOT a released/tagged version.
**Status:** Candidate documentation and control updates prepared; project rights and release authorization pending.

## Evidence and decision table

| Finding | Remediation delivered | Closure status |
|---|---|---|
| RR-01 | Align `VERSION` and `[project].version` in `pyproject.toml` to `0.4.0`; candidate label clearly distinguished from actual Git tag/release | Technical change ready for candidate CI |
| RR-02 | Fully revise `README.md` and `docs/index.md` to implemented BH-P04; valid code fences and `make behavior-test` | Technical change ready for candidate CI |
| RR-03 | Add `## v0.4.0 — release candidate` Changelog history and balance Markdown fences, retaining previous release history | Technical change ready for candidate CI |
| RR-04 | Supply full **Apache-2.0 license candidate** for explicit owner choice and hash-bound, dated rights-approval template; **root LICENSE remains empty** | **BLOCKED: license and rights holder not approved** |
| RR-05 | Prepare eight-snapshot `THIRD_PARTY_NOTICES.md` with W3C/OGC and QUDT attributions; capture factual OWL-Time CC BY 4.0 and unresolved PROV-O source rights; strengthen R08 gate requiring a real owner rights-approval record tied to both exact file SHA-256 hashes | **BLOCKED: owner and legal review pending** |
| RR-06 | Prepare final-format release notes containing **NOT RELEASED** status and explicit P05/P09 DEFERRED boundaries; retain owner authorization template | Notes ready; **release GO not authorized** |

## Rights and release control

Project-authored files currently have an empty `LICENSE`. The candidate license is provided at `docs/releases/LICENSE-Apache-2.0-CANDIDATE.txt`, not automatically copied to root. There is no assumption of who holds copyright or whether all contributors transferred rights. The project owner may instead choose another appropriate license, but must record the actual SPDX identifier, rights-holder identity and exact approved bytes.

`docs/governance/DEC-P04-07-rights-approval-TEMPLATE.json` contains placeholders and **does not** authorize use. The approved record, only after external rights/attribution review, must be saved to `docs/governance/DEC-P04-07-rights-approval.json` and include SHA-256 hashes of the actual `LICENSE` and `THIRD_PARTY_NOTICES.md`, a named approver, date, project license identifier, rights holder, third-party scope exclusion and explicit resolution of the OWL-Time/PROV-O observations. An approver's identity and legal authority still require project governance; a script cannot independently prove that authority.

The P04-07 runner `scripts/review_release_p04.py` is strengthened: **R08 is BLOCKED** without this signed-off record, even when a nonempty license and a notice document exist. Changed notice/license bytes after sign-off cause **R08 FAIL**. Old tests are updated to reject dummy rights approvals and include a hash-tampering regression.

`docs/governance/P04-07-release-decision-TEMPLATE.md` remains an **unapproved** template. The eventual distinct `docs/governance/DEC-P04-07-v0.4.0-release.md` must only be created after separate release authorization, candidate GitHub CI success and documented SHA. Neither a license choice nor a release decision is inferred from this package.

## Verification and gates

Run locally on the candidate commit:

```bash
.venv/bin/python -m pytest -q tests/test_p04_07_release_review.py tests/test_p04_07_remediation.py
make behavior-test
.venv/bin/python scripts/review_release_p04.py --repo "$PWD"
```

**Expected prior to owner sign-off:** `R05_VERSION`, `R06_DOCS`, `R07_CHANGELOG`, `R09_RELEASE_NOTES` PASS; `R08_LICENSE_NOTICES` and `R10_OWNER_APPROVAL` BLOCKED; overall `NO_GO` exit code 2. All original BH-P04 validation/CI remain mandatory. A successful GitHub Actions run on the candidate commit must be checked independently; do not cite an older run as a new result.

Do not set the R08/R10 statuses to PASS by editing the JSON report. Once actual approvals are recorded, re-run the gate and the full CI; only after **all ten** release gates PASS and reviewed GitHub Actions results may an annotated `v0.4.0` tag be authorized.

## Unmodified sources

No DCCR-01…04, MASS-OEF roadmap, SysML kernel source/manifest, vendor RDF snapshots, T-04 lock, ontology files, existing BH-V/BH-CQ queries or evidence are edited by remediation. Original Git history and previously accepted evidence remain independently auditable.
