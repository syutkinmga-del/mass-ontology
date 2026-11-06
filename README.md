# MASS Ontology Stack

Modular RDF/OWL research ontology for **Maritime Autonomous Surface Ships (MASS)** as systems of systems.

**Current release status: v0.4.0 — APPROVED FOR RELEASE; PUBLICATION NOT RECORDED.**
Signed R10 P04-07-R10-2026-01 (2026-11-06) approves exactly `81b33951cbed446ebff5192099125f56ff474fb0`. See [R10 registration](docs/governance/DEC-P04-07-v0.4.0-release.md); this later registration commit is not the approved SHA. This status does **not** assert publication of a GitHub Release or tag.

## BH-P04 Observation Core (v0.4.0 candidate)

The implemented and tested *observation* profile represents:

- Generic `maritime:Vessel`, with a controlled compatibility bridge to `mass:MASSVessel` and `nav:TargetShip` without equating target ships with autonomous vessels.
- `bh:Trajectory` and `bh:TemporalUnit` **information records**; each unit's `time:ProperInterval` is a separate temporal object.
- Concurrent `bh:PositionState`, `bh:SpeedState`, and `bh:CourseState` descriptions; temporal ordering and explicit coverage gaps.
- SOSA/SSN observations, source and process provenance through PROV-O, and QUDT 3.5.3 speed/course quantity values using `qudt:hasUnit`.
- Deterministic **synthetic AIS-like** input with six source records, 18 SOSA observations, three temporal units, and a deliberate two-minute gap. This is not a raw AIS decoder and is not real-world navigation validation.

The P04-04 versioned fixture is `examples/p04-04-synthetic-ais-qudt353.ttl`; the earlier P04-03 fixture remains frozen as a historical source baseline.

## Verification

Requires Python **3.12**, a repository `.venv`, Java **21** and ROBOT/HermiT **1.9.11** in `PATH`. See `ci/requirements-behavior-ci.txt` for the direct Python dependency pins.

```bash
make catalog
make validate
make cq
make test
make behavior-test
```

`make behavior-test` is the common fail-closed local/GitHub Actions profile gate. It enforces 7 BH-V rules, 3 BH-CQ questions with **exact RDF bindings**, 14 historical competency questions, all pytest cases with **zero skipped**, T-04 RDF integrity and immutable MASS-SK-1.0 byte integrity.

The P04-06 evidence commit `11491acb0685e69c0aed6ec749eea4d138162b30` passed its acceptance gates. Both GitHub Actions workflows also succeeded on rights-approved candidate commit `bf024c1698787d22979bb61289d57200f8220a59` (runs 42190651882 and 42190652017). For the R10-approved SHA `81b33951cbed446ebff5192099125f56ff474fb0`, the owner reports runs 42194345291 and 42194345375 as SUCCESS. Registration-branch checks are separate evidence.

## Architecture and controlled resources

| Path | Content |
|---|---|
| `00-foundation/`, `01-common/` | Draft common/foundation alignment; **not** verified BFO/CCO equivalence |
| `02-maritime/`, `03-mass-core/`, `04-navigation/` | Maritime and existing MASS/navigation concepts |
| `05-observation/`, `06-quantities/`, `07-behavior/` | BH-P04 observations, quantities and ship-behavior descriptions |
| `vendor/external-rdf/T04-2026/` | Eight fixed external RDF snapshots controlled by T-04 |
| `shapes/`, `queries/cq/`, `queries/behavior/` | Validation shapes and legacy/behavior competency questions |
| `docs/reviews/`, `docs/evidence/` | Approved DCCR contracts and published acceptance evidence |
| `baselines/sysml/MASS-SK-1.0/` | Immutable SysML v2 kernel **source** and integrity manifests |

## Release and research boundaries

**BH-P05** (GeoSPARQL spatial/semantic behavior) and **BH-P09** (recognition prototype) are **DEFERRED**. The current research ontology does not certify vessel safety, enforce COLREG compliance, execute ROC/VTS controls, validate live AIS prediction, import BFO/CCO axioms or prove SysML v2 parser semantics. The `https://w3id.org/mass-ontology/` redirect/dereferencing is not independently verified by the current test suite.

The rights holder approved **Apache-2.0 for author-owned original work** (RR-04) and separately approved the reviewed eight third-party RDF notices (RR-05; 2026-11-06). Publisher-owned T-04 RDF snapshots remain outside the author's Apache-2.0 grant and retain their own conditions. See `LICENSE`, `THIRD_PARTY_NOTICES.md` and `docs/governance/DEC-P04-07-rights-approval.json`. R10 is now registered for its exact approved SHA; publication is not recorded. The corrected notices edition was explicitly approved by owner text decision [RR-05-2026-02](docs/governance/DEC-P04-07-RR05-2026-02-chat-approval.md) and merged through [PR #3](https://github.com/syutkinmga-del/mass-ontology/pull/3). The actual `THIRD_PARTY_NOTICES.md` SHA-256 is `7387ce9b98911917bb02ea9f3228fad2942fe65c8c7974d2f9890e01620f8ce5`; the preceding signed RR-05-2026-01 approval remains preserved for its original bytes. The 2026-02 approval was an explicit in-chat text statement, **not an electronic signature**. A new R10 decision is required before tagging any commit other than the exact previously approved `81b33951cbed446ebff5192099125f56ff474fb0`.

## Documentation

- [Integrated Roadmap v1.1](docs/roadmap.md)
- [MASS-OEF methodology](docs/architecture/mass-oef-methodology.md)
- [DCCR-04 validation contract](docs/reviews/DCCR-04-validation-contract.md)
- [Original P04-07 release readiness review (2026-11-05)](docs/reviews/P04-07-release-readiness-review.md)
- [Follow-up P04-07 release readiness review (2026-11-06)](docs/reviews/P04-07-release-readiness-follow-up-2026-11-06.md)
- [Release candidate notes](docs/releases/v0.4.0-release-notes.md)
- [Changelog](CHANGELOG.md)
