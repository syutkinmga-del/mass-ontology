# P04-07 / RR-05-2026-02 — registration of explicit owner text approval

**Decision number:** P04-07-RR05-2026-02  
**Decision:** APPROVED — corrected third-party notices, limited to the exact SHA-256  
**Approved by (asserted project rights holder):** Сюткин Андрей Вениаминович  
**Approval date (as stated by owner):** 2026-11-06  
**Evidence type:** Explicit text confirmation in the project's ChatGPT conversation, **not an electronic signature**.  
**Independently authenticated signature:** NO  
**Private signed scan supplied for RR-05-2026-02:** NO

## Exact owner statement

> УТВЕРЖДАЮ исправленную редакцию THIRD_PARTY_NOTICES.md по решению P04-07-RR05-2026-02 от 06.11.2026 с SHA-256 `7387ce9b98911917bb02ea9f3228fad2942fe65c8c7974d2f9890e01620f8ce5`. Разрешаю регистрировать моё явное текстовое решение и подготовить отдельный PR для замены действующей редакции с сохранением проверок целостности. Понимаю, что подтверждение в чате не является электронной подписью.

This is an explicit in-chat owner **statement**, not a cryptographically authenticated, handwritten or independently signed legal instrument. It should not be described in other records as a signed RR-05-2026-02 PDF. The project owner retains responsibility for verifying and legally recognizing their authority and this evidence according to project governance.

## Exact artifact binding and permitted change

- Approved corrected `THIRD_PARTY_NOTICES.md` **SHA-256**: `7387ce9b98911917bb02ea9f3228fad2942fe65c8c7974d2f9890e01620f8ce5`.
- Previous **signed RR-05-2026-01** approved notices SHA-256: `fdcdcaaa2c4e47914f575b26ed6aef0513324957b09e1286ca6012b532022fc4`.
- Source of exactly reviewed proposal bytes: `docs/governance/proposals/RR05-2026-02/THIRD_PARTY_NOTICES.proposed.md` at commit `3b1073a5c7263733d568178abf9bbb10799dc700` on branch `docs/rr05-notices-corrigendum-proposal` (draft PR #2).
- The original 2026-11-06 signed RR-05-2026-01 record remains historically intact and continues to identify its own approved bytes.
- Scope: editorial reconciliation of the obsolete RR-05 status header and its approval-process explanation **only**; unchanged third-party license obligations, attribution/source links, all eight pinned T-04 RDF snapshots and their hashes, original Apache-2.0 author-owned project grant.

## Release and evidence boundaries

The text approval permits the described **exact-byte notices replacement** and registration in a new PR; it is **not** a consent to merge without CI review, alter any third-party license, change the underlying ontology semantics, or publish a release.

Previously signed R10 P04-07-R10-2026-01 remains bound solely to release candidate `81b33951cbed446ebff5192099125f56ff474fb0`. Neither this notices edit nor a future merge expands its approval to another commit. The previous signed RR-05 PDF is not published or modified. No new signed PDF is asserted.

## Integrity gate

The companion record `DEC-P04-07-RR05-2026-02-approval.json` and `DEC-P04-07-rights-approval.json` must retain the same approved SHA-256 and owner/date/decision facts. The fail-closed `scripts/verify_p04_rr05_notices.py --require-approval` must verify the actual bytes, original prior digest, both approval records, eight T-04 vendor hashes and LICENSE without loosening existing tests.
