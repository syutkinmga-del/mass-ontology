# P04-00 — Baseline & Architecture Readiness

**Project:** MASS Ontology Stack
**Plan:** MASS Ontology Roadmap v1.1 (APPROVED 2026-10-27)
**Review date:** 2026-10-28
**Status:** IN PROGRESS — remote baseline inspected; local execution evidence PENDING
**Next work package:** P04-01 — General Maritime Vessel

## 1. Purpose and change boundary

Freeze an auditable source baseline, establish the current regression gate and prepare controlled terminology, temporal modeling and normative source registry *before* editing ontology classes for v0.4.0-dev. This is a documentation and baseline exercise. It does not add production OWL, assert BFO/CCO equivalence, rewrite `mass:MASSVessel`, or implement `OperationalConfiguration`.

## 2. Observed remote baseline (GitHub connector, 2026-10-28)

- Repository: `syutkinmga-del/mass-ontology`.
- Latest observed default-branch commit: `44d7131fac9c0827fa973e06067200e5b31f3328`.
- Commit message: `Adopt MASS-OEF and approve integrated roadmap v1.1`.
- Commit page: https://github.com/syutkinmga-del/mass-ontology/commit/44d7131fac9c0827fa973e06067200e5b31f3328
- README labels development line `v0.3.0-dev` (this is a README label, not proof of a release tag).
- Approved controls: `docs/roadmap.md`, `docs/reviews/DCCR-01*`…`DCCR-04*`, `docs/governance/DEC-2026-10-27-mass-oef-roadmap-v1.1.md`.
- Tooling present in `Makefile`: `make catalog`, `make validate`, `make cq`, also `make test`; Python interpreter path `.venv/bin/python`.
- Data validation uses `pyshacl.validate(inference="rdfs")` in `scripts/run_shacl.py`.
- Ontology CQ runner expects row counts for `CQ-01`…`CQ-14` in `tests/expected-cq-results.json`, but row counts alone do not prove value-level correctness.
- Ontology catalog `catalog-v001.xml` presently lists five local ontology IRI mappings.
- Draft foundation layer contains nine alignment decisions. No verified BFO/CCO import is claimed.
- `mass:MASSVessel rdfs:subClassOf common:EngineeredSystem` exists.
- `nav:OwnShip rdfs:subClassOf mass:MASSVessel` exists, whereas `nav:TargetShip` currently has no declared general maritime-vessel superclass.
- `00-foundation/external-ontology-registry.ttl` currently uses GitHub repository URLs as `foundation:externalOntologyIRI` for BFO and CCO. This is an **audit item**, not permission to import those repository URLs as ontology IRI.

## 3. Evidence remaining to collect locally

The GitHub review above does **not** show the user's current working tree, virtualenv dependencies, command return codes, or content hash of `MASSKernel_v1.0.sysml` if outside this repository. Run `python3 scripts/capture_p04_baseline.py` in the repository with `.venv` configured, and retain the evidence JSON/logs outside the repository. Its snapshot includes local HEAD, Git branch, worktree state, package versions, availability of the SysML Kernel file, and real exit codes of the legacy commands.

The script does not install dependencies, commit files, change ontology definitions, or claim that absent prerequisites PASS. It compares local HEAD to the *remote SHA observed above*; if the remote branch advances, explicitly reconcile the new baseline rather than silently overwriting it.

### Validation gate (execution outcomes are PENDING)

| Check | Command / evidence | Required outcome before P04-00 close |
|---|---|---|
| BL-01 | `git rev-parse HEAD` | Record actual local SHA and compare with freeze SHA |
| BL-02 | `git status --porcelain=v1` | Record any local edits; document any baseline deviations |
| BL-03 | `make catalog` | PASS (exit 0 + retained log) |
| BL-04 | `make validate` | PASS (exit 0 + retained log) |
| BL-05 | `make cq` | PASS (exit 0 + retained log); 14 legacy CQ cases retained |
| BL-06 | `make test` (additional assurance) | Record result; treat failing previously tracked tests as a blocker or justified exception |
| BL-07 | SysML baseline hash | Record SHA256 of `MASSKernel_v1.0.sysml` if present locally; otherwise NOT AVAILABLE, seek controlled source |
| BL-08 | DCCR / roadmap documents | Present and unchanged by new behavior ontology work |
| BL-09 | source metadata registry | source titles, issuers, versions, evidence URLs and mapping status recorded |
| BL-10 | terminology/time/segmentation | reviewed policy is accepted or issues documented and assigned before P04-01 |

**Test-state vocabulary:** `PASS` = executed and met oracle; `FAIL` = executed and violated oracle; `BLOCKED` = required execution unavailable; `DEFERRED` = outside active profile; `PENDING` = not executed yet. `IN PROGRESS` is not equivalent to `APPROVED`.

## 4. Selected P04-00 decision proposals

| ID | Subject | Proposed disposition | Status |
|---|---|---|---|
| P04-00-D01 | `maritime:Vessel` and target ships | Generic vessel category; no premature `owl:equivalentClass`; review subclass and compatibility in P04-01 | PROPOSED |
| P04-00-D02 | `Trajectory` / `TemporalUnit` | Both information representations; a time interval is a distinct OWL-Time object | APPROVED IN DCCR-02/03 |
| P04-00-D03 | Time | UTC ISO 8601 with explicit offset; separate observed/event, AIS reception, result/processing times | PROPOSED IMPLEMENTATION POLICY |
| P04-00-D04 | Segmentation | Manual/algorithm-versioned *explicit* segments for P04 synthetic fixture; no universal gap threshold chosen | PROPOSED |
| P04-00-D05 | Standards | Metadata-only registry with publication-status/IRI/edition and license/import decision | APPROVED 2026-10-28 — SR-01…SR-07; RDF artifact pinning PENDING |
| P04-00-D06 | `OperationalConfiguration` | Document future role as temporally scoped integration context at v0.6; do not implement in P04 | DEFERRED |
| P04-00-D07 | BFO/CCO | Candidate mapping only; exact superclass and normative ontology IRI not yet accepted | OPEN |

See `docs/architecture/P04-00-terminology-time-policy.md`, `docs/standards/normative-source-registry.md`, and `docs/architecture/operational-configuration-adr.md`.

## 5. P04-00 exit criteria

- [ ] Remote SHA / local HEAD reconciliation recorded.
- [ ] Legacy regression commands executed and logs linked from evidence report.
- [ ] `MASSKernel_v1.0.sysml` immutability evidenced by hash, or controlled-source location identified.
- [ ] Source registry reviewed; none of the metadata-only entries accidentally used as `owl:imports`.
- [ ] Term/IRI/time/segmentation decisions accepted or assigned open implementation gates.
- [ ] OperationalConfiguration future boundary accepted without implementation.
- [ ] P04-01 may start with a reviewed general-vessel migration proposal.

**Current verdict:** P04-00 STARTED; cannot mark COMPLETE until local command evidence and decision review are available.

## 6. Source registry approval follow-up (2026-10-28)

The P04-00 [Normative & Ontology Source Registry](../standards/normative-source-registry.md) was **APPROVED** with SR-01…SR-07, as recorded in [the governance decision](../governance/DEC-2026-10-28-P04-00-source-registry-SR01-SR07.md). The metadata architecture is approved, while dependency artifacts, licenses, checksums and BH-V11 execution remain pending before P04-03. Existing P04-00 exit criteria and kernel/test evidence requirements remain open.
