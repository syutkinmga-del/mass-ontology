# P04-01 — General Maritime Vessel: Implementation and Compatibility Contract

**Implementation stage:** v0.4.0-dev / BH-P04
**Status:** IMPLEMENTATION CANDIDATE — local test evidence must be collected; not yet a release
**Sources:** approved `docs/roadmap.md` section C, DCCR-03 C01 and General-vessel migration hazard; DCCR-04 BH-V01/BH-V12; approved P04-00 Terminology & Time Policy.
**Baseline:** immutable `MASS-SK-1.0`, existing MASS OWL legacy modules and CQ-01…14.

## Design decision and identity

`maritime:Vessel` (IRI `https://w3id.org/mass-ontology/maritime#Vessel`) represents a physical maritime vessel regardless of autonomy and navigation role. Its **local** superclass is `common:EngineeredSystem` (not a BFO/CCO mapping). This architectural design choice should receive an explicit review before release; `common:PhysicalArtifact` has not been asserted as an additional superclass pending upper-ontology alignment.

The narrower class `mass:MASSVessel` is a subclass of `maritime:Vessel`.
The existing context-role class `nav:TargetShip` is a subclass of `maritime:Vessel` **only**. It is **not** a subclass/equivalent of `mass:MASSVessel`.
The existing `nav:OwnShip rdfs:subClassOf mass:MASSVessel` is deliberately unchanged; it therefore reaches general `maritime:Vessel` transitively.

```text
common:EngineeredSystem
        └── maritime:Vessel
              ├── mass:MASSVessel
              │     └── nav:OwnShip (legacy)
              └── nav:TargetShip (legacy contextual role class)
```

This diagram indicates subclass inheritance, **not disjointness**. A vessel can participate under different encounter roles; the legacy classes are not temporally reified as roles. A future role/context modeling design must not retroactively change this compatibility contract without tests.

## Modular boundary

- `02-maritime/maritime-core.ttl`: generic maritime vocabulary, locally imports MASS Common.
- `02-maritime/vessel-compatibility.ttl`: isolated bridge with two subclass links and local ontology imports.
- `catalog-v001.xml`: two new local mappings. RDFLib does not automatically follow catalog mappings or `owl:imports`; P04-01 tests explicitly load modules. P04-02/P04-03 behavior validation runner must load bridge explicitly or resolve the import closure.
- No modifications to `03-mass-core/mass-core.ttl`, `04-navigation/navigation-situation.ttl`, `examples/example-encounter-scenario.ttl`, SysML Kernel, `scripts/run_cq_queries.py`, `scripts/run_shacl.py`, or the old CQ expected-result file.

## Local acceptance and limitations

Execute `python3 -m pytest -q tests/test_p04_01_maritime.py` with the project's `.venv` (or `make test`). The suite asserts ontology IRI/catalog mapping, subclass hierarchy, current example inference by transitive RDFS, absence of generic→MASS and target→MASS paths, and three mutation-negative cases. The test scope is the actual checked-in graph, not proof about arbitrary future imported ontologies.

Then execute `make catalog && make validate && make cq && make test` and `python3 scripts/verify_sysml_kernel_integrity.py` (if present). All must PASS before accepting P04-01; preserve logs, git SHA and versions as evidence. The full BH-V01 requires `bh:Trajectory` and a fixture from P04-02/03, thus **DEFERRED** until P04-04; all BH-CQ-01..03 are also **DEFERRED**.

**Not included:** `bh:Trajectory`, observation profiles, BFO/CCO alignment, degree-of-autonomy model, role reification, COLREG inference, `OperationalConfiguration`, or production `v0.4.0` release approval.

**Review decisions to record:** (1) `maritime:Vessel` local subclass of `common:EngineeredSystem`; (2) compatibility bridge separate from legacy source; (3) contextual role vs intrinsic vessel identity; (4) catalog registration and explicit data loading; (5) test results and repository commit. The two modules establish intended IRI identifiers, but do not prove w3id.org URL dereferencing is configured.
