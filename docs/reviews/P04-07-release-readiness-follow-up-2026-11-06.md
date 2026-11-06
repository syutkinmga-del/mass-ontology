# P04-07 — Follow-up Formal Release Readiness Review for v0.4.0 (BH-P04)

**Review stage:** Follow-up review following PR #1 (signed R10 registration) and PR #3 (RR-05-2026-02 corrected notices).  
**Review date:** 2026-11-06  
**Last known merged `main` baseline:** `2dbd3e849e5dc2807d7df2786fb905ac17089722`  
**Candidate under this review:** Exact HEAD of the PR #4 branch, to be recorded at execution; **not** the old signed R10 SHA.  
**Provisional recommendation:** **NO-GO FOR TAGGING** until an explicit separate authorization binds the exact final release candidate, with all technical gates and final GitHub Actions verified.  
**Source historical review:** [P04-07 original formal RRR, 2026-11-05](P04-07-release-readiness-review.md), which remains unchanged and documents the earlier NO-GO at its own review date.

## A. Scope and policy

Scope is solely **MASS Ontology v0.4.0 / BH-P04 Observation Core** (synthetic AIS-like, SOSA/QUDT/OWL-Time/PROV-O, trajectory/temporal units and Position/Speed/Course state representations). BH-P05 and BH-P09 remain **DEFERRED**. This review does not claim verified real AIS decoding, navigation safety, COLREG reasoning, production ROC/VTS, full BFO/CCO import/equivalence, or SysML v2 parsing.

The prior signed R10 [P04-07-R10-2026-01](../governance/DEC-P04-07-v0.4.0-release.md) **APPROVED FOR RELEASE** only the exact Git SHA `81b33951cbed446ebff5192099125f56ff474fb0`. It does not, by implication, authorize newer documentation-only commits, the RR-05 replacement merge, or PR #4. The decision itself and all historical DCCR/Roadmap/P04-06 evidence must remain immutable.

The corrected notices edition has explicit owner **text** approval `P04-07-RR05-2026-02` for SHA-256 `7387ce9b98911917bb02ea9f3228fad2942fe65c8c7974d2f9890e01620f8ce5` via [registration](../governance/DEC-P04-07-RR05-2026-02-chat-approval.md) and [machine-readable record](../governance/DEC-P04-07-RR05-2026-02-approval.json). **This is not an electronic signature or signed PDF**; the prior signed RR-05-2026-01 remains a separate historical approval of different exact bytes. Changes to this corrected file would need new exact-byte authorization.

## B. Verified existing evidence (not a new formal script execution)

The post-PR #3 merged `main` commit `2dbd3e849e5dc2807d7df2786fb905ac17089722` has both GitHub Actions workflows completed `success`:
- [Validate MASS Ontology, 42209855912](https://github.com/syutkinmga-del/mass-ontology/actions/runs/42209855912)
- [BH-P04 Behavior Validation, 42209855875](https://github.com/syutkinmga-del/mass-ontology/actions/runs/42209855875)

The latter recorded the ten executed behavior validation steps (GATE 01–10) as PASS and the explicit RR-05 verifier as PASS with `findings: []`, `vendor_files_checked: 8` and SHA-256 `7387ce9b98911917bb02ea9f3228fad2942fe65c8c7974d2f9890e01620f8ce5`. These are **post-merge CI facts for that baseline SHA**, not an assertion of GitHub Actions success on the eventual PR #4 HEAD. The historical P04-06 evidence contains eleven acceptance gates; do not conflate that archived count with the ten named execution stages printed by the more recent runner.

## C. Formal R01–R10 acceptance matrix

The statuses below are the **review entry criteria**, not fabricated results from an execution on PR #4. The definitive per-gate result comes from the machine-readable report uploaded by GitHub Actions on the exact PR HEAD.

| Gate | Acceptance evidence required | Status before PR #4 execution |
|---|---|---|
| R01 SOURCE_BASELINE | Full Git ancestry contains P04-06 accepted evidence commit `11491acb...` | TO VERIFY ON PR HEAD |
| R02 DESIGN_SCOPE | DCCR-01…04 and Integrated Roadmap v1.1 unchanged since evidence baseline | TO VERIFY ON PR HEAD |
| R03 CI_EVIDENCE | Published original P04-06 acceptance file and archived 11-gate evidence valid | TO VERIFY ON PR HEAD |
| R04 INTEGRITY | Immutable MASS-SK-1.0, T-04 lock, P04-04 fixture, archive hash verifier | TO VERIFY ON PR HEAD |
| R05 VERSION | `VERSION` and `pyproject.toml` both `0.4.0` | TO VERIFY ON PR HEAD |
| R06 DOCS | README/index current, accurate and syntactically balanced | TO VERIFY ON PR HEAD |
| R07 CHANGELOG | Versioned v0.4.0 history present and syntactically balanced | TO VERIFY ON PR HEAD |
| R08 LICENSE_NOTICES | Apache-2.0 author license; separately approved corrected notices exact SHA; eight frozen external RDF snapshots; explicit owner approval record | TO VERIFY ON PR HEAD |
| R09 RELEASE_NOTES | BH-P04 research scope and deferrals explicit; release not falsely marked as issued | TO VERIFY ON PR HEAD |
| R10 OWNER_APPROVAL | Explicit owner authorization for **exact proposed release SHA**, not merely existence of an earlier approval record | **BLOCKED** for PR #4 until new exact-SHA authorization |

**Release decision:** **NO-GO / authorization boundary unresolved**. An all-green R01–R09 technical evaluation does not supersede the explicit R10 SHA restriction.

## D. Executable follow-up review

The legacy `scripts/review_release_p04.py` reads and verifies recorded technical evidence but its R10 check only looks for named, dated approval text. Consequently it could return a misleading `GO` on a later SHA when the registered approval is actually bound to an earlier commit. The new `scripts/review_release_p04_candidate.py` reuses the historical R01–R10 assessments, additionally requires:

1. Unique, explicit 40-hex R10 `Approved commit SHA` equals actual reviewed Git `HEAD`.
2. `scripts/verify_p04_rr05_notices.py --require-approval` succeeds on exact current notices bytes and newly recorded RR-05 approval.
3. Complete Git ancestry is available, original integrity/evidence baselines are preserved, and **all ten formal gates PASS** before `decision=GO`.

Run locally with a full Git clone:

```bash
python3 scripts/review_release_p04_candidate.py --report run/release-review/p04-07-follow-up.json
```

The dedicated [P04-07 Release Readiness Review](../../.github/workflows/release-readiness.yml) workflow runs against the **PR head SHA** (rather than GitHub's temporary PR merge ref), uploads the JSON even on `NO_GO`, and intentionally returns a failed gate when R10 is not matched. That expected red release gate is an **authorization BLOCK**, not evidence that BH-P04 functional CI is broken. The existing BH-P04 and SHACL workflows must still be checked separately on the same PR head.

## E. Dispositions required before an actual v0.4.0 tag

- Review and merge PR #4 only after its content changes pass the normal workflows; **do not treat a green engineering CI as authorization to tag**.
- Fix any formal review R01–R09 failure on the target revision and re-run the exact relevant workflows after the last change.
- Freeze and identify the final SHA intended for `v0.4.0`, and obtain the project owner's **new exact-SHA R10 release decision** for that candidate. Register its dated decision **without altering the approved candidate bytes** (a later archival/registration commit is not the signed release target).
- Independently verify GitHub Actions on the actual proposed tag SHA; confirm original signed RR-05 record, current RR-05-2026-02 text approval, `THIRD_PARTY_NOTICES.md` hash and all eight pinned RDF hashes.
- Only after all conditions hold, create the **annotated `v0.4.0` tag on the owner-approved exact candidate SHA**, publish GitHub Release and record its URL. No tag or release is issued by this review or PR.

**Authority limitation:** A script, a Pull Request merge and a passing workflow cannot sign an owner decision or broaden the scope of an existing signed document.
