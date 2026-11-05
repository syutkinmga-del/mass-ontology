# MASS Ontology — Research Documentation

**Release status: v0.4.0 — RELEASE CANDIDATE, NOT RELEASED.**
**Active validated profile:** BH-P04, Observation Core.
**Methodology:** MASS-OEF; [approved Integrated Roadmap v1.1](roadmap.md).

## Current implemented scope

The ontology models generic maritime vessels and their synthetic AIS-like observation histories using `bh:Trajectory`, `bh:TemporalUnit`, OWL-Time intervals, concurrent physical state descriptions, SOSA/SSN observations, QUDT 3.5.3 speed/course values and PROV-O source evidence. Its `TemporalUnit` is an **information segment**, not a `time:ProperInterval` or ship motion process.

The synthetic profile uses six source records, 18 observations, three temporal units, a two-minute coverage gap and a versioned QUDT-corrected 370-triple fixture. The historical P04-03 fixture is retained unchanged.

### Verification

```bash
make catalog
make validate
make cq
make test
make behavior-test
```

On the published P04-06 evidence baseline the CI recorded 115 tests without errors, failures or skips; BH-V01/02/03/05/06/11/12 PASS and BH-CQ-01/02/03 exact bindings PASS. The release candidate must be retested after any changes.

- [P04-06 CI evidence](evidence/P04-06/README.md)
- [P04-07 release readiness review](reviews/P04-07-release-readiness-review.md)
- [P04-07 remediation](implementation/P04-07-remediation-implementation.md)
- [v0.4.0 candidate notes](releases/v0.4.0-release-notes.md)

## Design authority and traceability

| Reference | Role |
|---|---|
| [DCCR-01](reviews/DCCR-01-xiong-ship-behavior-review.md) | Domain concept inventory and release allocation |
| [DCCR-02](reviews/DCCR-02-semantic-design-review.md) | Information-vs-physical semantics, Trajectory/TemporalUnit/PhysicalBehavior |
| [DCCR-03](reviews/DCCR-03-ontology-alignment-specification.md) | Project IRI, local modules and external vocabulary strategy |
| [DCCR-04](reviews/DCCR-04-validation-contract.md) | Validation profiles, BH-V01…12, BH-CQ-01…10 and acceptance rules |
| [MASS-OEF](architecture/mass-oef-methodology.md) | Development framework |
| [Roadmap v1.1](roadmap.md) | Versioned staged scope and gates |

DCCR decisions remain historical approvals of **design contracts**, not retrospective declarations of test success. Executed test evidence is recorded separately. No BFO/CCO external equivalence or complete import alignment has been asserted.

## Future scope — not included in BH-P04

BH-P05 spatial relations and interpretation/graph-segregation tests and BH-P09 recognition tests remain **DEFERRED**. The present implementation does not perform live AIS decoding, collision-risk assessment, navigation safety certification, ROC/VTS operational control or fresh SysML v2 parser validation. Only MASS-SK-1.0 **source bytes and manifest integrity** are checked.

## Distribution status

Public release requires explicit project-owner approval of a license for project-authored files, external RDF notices and final release scope. See the root `THIRD_PARTY_NOTICES.md` and the governance decision templates. The `VERSION`/`pyproject.toml` candidate number is **not** itself an issued GitHub tag or Release.

Earlier project releases `v0.1.0` and `v0.2.0` remain separate historical milestones; see [CHANGELOG](../CHANGELOG.md).
