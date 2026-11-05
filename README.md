# MASS Ontology Stack

Modular RDF/OWL research ontology for **Maritime Autonomous Surface Ships (MASS)** as systems of systems.

**Current release status: v0.4.0 — RELEASE CANDIDATE, NOT RELEASED.**
The last published version tag may be older; this label names the P04-07 candidate and does **not** assert that a GitHub Release or tag has been issued. Release remains subject to rights review and an explicit project-owner decision.

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

The previously published P04-06 GitHub Actions results on commit `11491acb0685e69c0aed6ec749eea4d138162b30` were successful; that evidence does not itself replace fresh testing of the release candidate.

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

The project license is **pending explicit rights-holder selection and approval**. Third-party vocabularies remain governed by their own licenses. Do not interpret public source availability as permission to redistribute project-authored material under a license not yet selected. See `THIRD_PARTY_NOTICES.md`, `docs/implementation/P04-07-remediation-implementation.md` and the P04-07 governance templates.

## Documentation

- [Integrated Roadmap v1.1](docs/roadmap.md)
- [MASS-OEF methodology](docs/architecture/mass-oef-methodology.md)
- [DCCR-04 validation contract](docs/reviews/DCCR-04-validation-contract.md)
- [P04-07 release readiness review](docs/reviews/P04-07-release-readiness-review.md)
- [Release candidate notes](docs/releases/v0.4.0-release-notes.md)
- [Changelog](CHANGELOG.md)
