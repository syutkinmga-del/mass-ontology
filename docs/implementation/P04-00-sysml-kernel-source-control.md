# P04-00 — Source and Integrity Implementation Evidence

**Prepared:** 2026-10-28  
**Scope:** Source registration and byte integrity only.  
**Original project release:** `MASS-SK-1.0` / `MASSKernel_v1.0.sysml`.

## Evidence already verified from supplied project artifacts

- Actual released source SHA-256: `1701bbb86e24588660ef717f2ff7f276b63c938d8569d4511dc19c42033aa788`.
- Original `MASSKernel_v1.0.sha256` includes the identical hash and original filename.
- Original release manifest independently carries the same hash, declares 62 top-level production definitions and historical SK1–SK16 regression results.
- Candidate file differs in release-header comments only, with a distinct SHA-256; it is **not** installed as reference baseline.
- Validation record documents historical Stage 1.2 and CQ1–CQ12 evidence, but the validation record itself calls the source `MASSKernel_v1.0_candidate.sysml` and its status `BASELINE CANDIDATE`; later release/change-control artifacts provide RELEASED status. These reflect separate release stages.
- Exact archived file has leading `Skip to main panel` and a standalone `/` before the SysML `package` line. No standalone Pilot validation was run here.

## Reproduce after installation

From local MASS Ontology repository:

```bash
python3 scripts/verify_sysml_kernel_integrity.py
make test
make catalog && make validate && make cq
```

Expected checksum result: `MASS-SK-1.0 SOURCE INTEGRITY: PASS`. Additional pytest tests check positive identity and negative mutation rejection. Actual user-Mac execution status cannot be asserted before user runs these commands.

## Commit control

Add only this new archival snapshot, documentation, checker, and tests. Do **not** modify `MASSKernel_v1.0.sysml` bytes or DCCR source files. Commit after the validation passes. Avoid auto-running the installer against a dirty tree with conflicting destination paths.

## Exit criteria for source-integrity subtask

- [x] Release source located among the provided project artifacts.
- [x] SHA-256 matched to checksum file and original release manifest.
- [x] Provenance, source issue, archive policy and check implementation documented.
- [ ] Source snapshot installed and committed into target GitHub repo.
- [ ] Local integrity regression and full `make test` result confirmed.
- [ ] Separate standalone SysML Pilot parse result documented or explicitly deferred (not counted as byte-integrity test).

**Important:** Completion of this subtask does not automatically close all P04-00 gates or release BH-P04.
