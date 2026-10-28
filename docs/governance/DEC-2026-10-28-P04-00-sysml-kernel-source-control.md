# P04-00 — SysML Semantic Kernel Source and Integrity Decision

**Decision date:** 2026-10-28  
**Baseline:** `MASS-SK-1.0`  
**Decision scope:** Controlled-source reference and integrity verification for MASS Ontology integration  
**Implementation status:** Prepared; GitHub publication and local passing tests require confirmation

## Controlled-source decision

1. Archive the **unchanged** released `MASSKernel_v1.0.sysml` bytes and five original companion artifacts under `baselines/sysml/MASS-SK-1.0/` in the MASS Ontology repository.
2. Pin released source SHA-256: `1701bbb86e24588660ef717f2ff7f276b63c938d8569d4511dc19c42033aa788`; verify the checksum file and JSON manifest. Commit and Git history are transport/version evidence, not substitutes for checksum matching.
3. Keep the semantic kernel release independent of OWL/RDF behavior modules and immutable in the `MASS-SK-1.0` versioned archive; evolve via versioned successors or explicitly approved mappings.
4. Add automated **positive and mutation-negative** checks for kernel file integrity, and retain the existing 14 RDF competency question checks.
5. Classify the original `Skip to main panel` and solitary `/` at the file start as a **documented potential SysML parser issue** (SK-SRC-01); do not silently sanitize the released source or claim the exact file compiled in this session.
6. Historical Stage 1.2 / SK1–SK16 / CQ1–CQ12 PASS statements are evidence in the supplied prior validation record; **not contemporary re-executed results**.
7. Existing `MASSKernel_v1.0_candidate.sysml` is not the released reference. Its different hash is recorded for provenance but is not substituted in the archive.

## Exit boundary

**Passes currently evidenced:** reproducible SHA comparison against released original and its original checksum; provenance document existence; candidate-vs-release header-only diff.

**Pending until local execution:** installation of reference snapshot in the user's repository, `verify_sysml_kernel_integrity.py` PASS, `make test` PASS and `git push`.

**Not included in this decision:** approving new SysML semantics, re-running the SysML v2 Pilot, accepting external OWL imports, or declaring complete BH-P04 or the entire P04-00 governance gate.

See [SysML Kernel Source & Integrity Control](../architecture/sysml-kernel-source-integrity.md).
