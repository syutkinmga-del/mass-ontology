# P04-07 / RR-05-2026-02 — proposed editorial notices corrigendum (DRAFT)

**Decision number:** P04-07-RR05-2026-02  
**Decision status:** DRAFT — PENDING EXPRESS PROJECT-OWNER APPROVAL; NOT SIGNED  
**Approver:** Project rights holder (to approve separately)  
**Proposed file:** `docs/governance/proposals/RR05-2026-02/THIRD_PARTY_NOTICES.proposed.md`

## Exact reviewed bytes and control

- **Originally signed RR-05 edition SHA-256:** `fdcdcaaa2c4e47914f575b26ed6aef0513324957b09e1286ca6012b532022fc4`.
- **Proposed corrected edition SHA-256:** `0d21cb67c2d908269a4896b4b7ee9364394fb8bbafd5e54c14ef7834dbf51d30`.
- **Scope of proposed change:** Correct pre-approval RR-05 status text and governance/sign-off language **only**.
- **Excluded from this change:** The eight T-04 frozen RDF bytes, publisher identity/attribution, license rules, LICENSE, ontology semantic modules, BH-P04 validation baselines and R10 target SHA.

The proposed edition is not the currently approved `THIRD_PARTY_NOTICES.md` and must not replace it until a separate explicit and dated rights-holder decision approves **the exact proposed SHA-256**. No signature, owner approval or revised hash binding is inferred from the preparation of this file or the draft PR.

## Decision for the rights holder to issue separately

> I have reviewed the exact proposed corrected `THIRD_PARTY_NOTICES.md` edition with SHA-256 `0d21cb67c2d908269a4896b4b7ee9364394fb8bbafd5e54c14ef7834dbf51d30`. I approve its replacement of the previously signed RR-05 edition with SHA-256 `fdcdcaaa2c4e47914f575b26ed6aef0513324957b09e1286ca6012b532022fc4`, limited to the stated editorial corrections. This approval does not authorize changes to upstream RDF or extend R10 to a new release candidate.

**Owner's decision:** PENDING  
**Approval date:** PENDING  
**Private signed source SHA-256 (if applicable):** PENDING  
**Public registration of the actual approval:** PENDING

## After formal approval

1. Verify the candidate's SHA-256 against the actual proposed bytes and independently record the owner's approval.
2. Replace the root `THIRD_PARTY_NOTICES.md` **only after** approval of these exact bytes.
3. Update `docs/governance/DEC-P04-07-rights-approval.json` with the new approved notice SHA and cite the approval record; preserve the original signed RR-05 decision unchanged.
4. Update exact hash checks in `scripts/verify_p04_rr05_notices.py` and any other fail-closed R08 gates to match the newly approved bytes. Do not weaken or remove the checks.
5. Run the entire CI suite, release review R01–R10 and assess whether a changed release-target SHA needs new R10 authorization.
6. Use a separately reviewed PR for replacement; do not merge this proposal as an effective license change.
