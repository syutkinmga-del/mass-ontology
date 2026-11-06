# P04-07 — RR-05 notice status clarification

**Historical status record:** The statements below describe the discrepancy as documented before PR #3. **Superseded for current status** by the distinct owner text decision [RR-05-2026-02](DEC-P04-07-RR05-2026-02-chat-approval.md) and its exact-byte replacement of `THIRD_PARTY_NOTICES.md` on 2026-11-06. See the dated closure entry at the end; this document is not a current release blocker.

**Recorded:** 2026-11-06

The header of `THIRD_PARTY_NOTICES.md` says **OWNER SIGN-OFF PENDING**, while [signed RR-05 decision P04-07-RR05-2026-01](DEC-P04-07-RR05-third-party-notices-approval.md) and [rights approval JSON](DEC-P04-07-rights-approval.json) register owner approval dated 2026-11-06. The pending header is a stale pre-approval status; the separate signed decision is the approval record. This clarification documents the contradiction without altering the approved artifact.

The approved and retained `THIRD_PARTY_NOTICES.md` SHA-256 is:

`fdcdcaaa2c4e47914f575b26ed6aef0513324957b09e1286ca6012b532022fc4`

Neither the notices nor the RR-05 hash is changed by R10 registration. The original RR-05 signed PDF digest, rights records, LICENSE and eight frozen publisher RDF artifacts remain unchanged. No new redistribution terms are inferred.

**Outstanding:** a corrected notices edition must be separately approved by the rights holder with its exact new bytes and SHA-256 before replacement. No approval of a new edition has been supplied. [R10](DEC-P04-07-v0.4.0-release.md) authorizes its exact source SHA and does not waive this requirement or approve later commits.

`scripts/review_release_p04.py` checks exact notices/rights hashes in R08; it does not reject the stale header. R10 checks the presence of an explicit dated named approval, but does not validate the signed PDF, candidate SHA or candidate CI runs. Thus a GO result is a script result, not proof that this discrepancy is resolved or that a later commit is owner-approved. The checker and its acceptance rules are unchanged.

## Closure addendum — 2026-11-06 (not a revision to the signed RR-05-2026-01 record)

The project owner issued an **explicit text approval** P04-07-RR05-2026-02 for the corrected notices SHA-256 `7387ce9b98911917bb02ea9f3228fad2942fe65c8c7974d2f9890e01620f8ce5`. The approval was recorded as a ChatGPT conversation statement, **not an electronic signature** or a new signed PDF. [PR #3](https://github.com/syutkinmga-del/mass-ontology/pull/3) merged the exact approved bytes and associated approval/integrity records into `main` at `2dbd3e849e5dc2807d7df2786fb905ac17089722`.

GitHub Actions runs [42209855912](https://github.com/syutkinmga-del/mass-ontology/actions/runs/42209855912) and [42209855875](https://github.com/syutkinmga-del/mass-ontology/actions/runs/42209855875) completed with `success`; the required RR-05 verifier passed with zero findings on all eight T-04 artifacts and the exact new notices SHA-256. The original signed RR-05-2026-01 remains intact as evidence for its earlier SHA-256 `fdcdcaaa2c4e47914f575b26ed6aef0513324957b09e1286ca6012b532022fc4`.

**Disposition:** Historical RR-05 stale-header discrepancy **CLOSED**. A separate v0.4.0 release-target approval question remains: the signed R10 still authorizes only `81b33951cbed446ebff5192099125f56ff474fb0`, not the newer `main` or any prospective PR merge commit.
