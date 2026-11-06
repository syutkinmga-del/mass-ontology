# MASS Ontology — Research Documentation

**Release status: v0.4.0 — APPROVED FOR RELEASE; PUBLICATION NOT RECORDED.**
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

On the published P04-06 evidence baseline the CI recorded 115 tests without errors, failures or skips; BH-V01/02/03/05/06/11/12 PASS and BH-CQ-01/02/03 exact bindings PASS. Both candidate workflows also succeeded on `bf024c1698787d22979bb61289d57200f8220a59` (2026-11-06). The owner reports runs 42194345291 and 42194345375 as SUCCESS for R10-approved `81b33951cbed446ebff5192099125f56ff474fb0`. Later registration-branch CI is separate evidence.

- [P04-06 CI evidence](evidence/P04-06/README.md)
- [P04-07 historical readiness review (2026-11-05)](reviews/P04-07-release-readiness-review.md)
- [P04-07 follow-up readiness review (2026-11-06)](reviews/P04-07-release-readiness-follow-up-2026-11-06.md)
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

The project owner approved Apache-2.0 for original author-owned work and the eight external RDF notices in separate RR-04/RR-05 decisions (2026-11-06). See `LICENSE`, `THIRD_PARTY_NOTICES.md` and `docs/governance/DEC-P04-07-rights-approval.json`. [Signed R10 P04-07-R10-2026-01](governance/DEC-P04-07-v0.4.0-release.md) approves exactly `81b33951cbed446ebff5192099125f56ff474fb0` on 2026-11-06. This registration commit is not that SHA; no GitHub tag or Release publication is claimed. The corrected `THIRD_PARTY_NOTICES.md` was expressly approved in the distinct [RR-05-2026-02 text decision](governance/DEC-P04-07-RR05-2026-02-chat-approval.md) and merged in PR #3 with SHA-256 `7387ce9b98911917bb02ea9f3228fad2942fe65c8c7974d2f9890e01620f8ce5`; this text decision is **not an electronic signature**. The original signed RR-05-2026-01 remains a historical approval of different bytes. The registered R10 still applies only to candidate SHA `81b33951cbed446ebff5192099125f56ff474fb0`, not current `main`.

Earlier project releases `v0.1.0` and `v0.2.0` remain separate historical milestones; see [CHANGELOG](../CHANGELOG.md).
