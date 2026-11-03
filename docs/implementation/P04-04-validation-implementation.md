# P04-04 — BH-P04 SHACL / Python / OWL validation implementation

**Baseline:** `baf84cdbd5732d5f243c0625705fce77f2cb5cc3` (published T-04); DCCR-04 approved contract.  
**Status:** IMPLEMENTATION CANDIDATE; real Mac run, independent OWL reasoner, and full regression evidence required.

## Migration / controlled source integrity

The published P04-03 source generator, 370-triple file, documentation, source profile manifest and T-04 lock **remain byte-identical**. Changing them would invalidate the existing recorded P04-03 SHA-256 and T-04 `local_profile_check` control. `generate_p04_04_fixture.py` derives a new *current validation fixture* using `qudt:hasUnit` (QUDT 3.5.3); it records a new SHA-256 and 370 RDF triples while preserving original P04-03 as a historical test baseline. This is a versioned correction to the earlier `qudt:unit` assumption in DCCR-04 §5.2, not a retroactive amendment to approved DCCR. For production ingestion, transition to `qudt:hasUnit` in the future implementation; the P04-03 generator is historical only.

## Validation mapping

- **BH-V01**: SHACL min/max and class, plus explicit `maritime:Vessel` assertion and reciprocal link (not inferred typing).
- **BH-V02**: SHACL parent/extent counts; Python reciprocal membership, no stray units, distinct interval object.
- **BH-V03**: Python strictly parsed offset-aware UTC time intervals, ordered contiguous segment indices, nonoverlap, next links and documented coverage gap.
- **BH-V05**: coexistence of PositionState / SpeedState / CourseState as three descriptions per unit, prohibited disjointness check; **independent ROBOT/HermiT reasoner** must succeed on the imported-free local Behavior schema plus P04-04 positive data, and fail on a genuine contradiction mutation, otherwise BLOCKED.
- **BH-V06**: SHACL `qudt:numericValue` xsd:decimal + exactly one `qudt:hasUnit` + explicit forbidden legacy predicate; Python evidence links to observation and unit policy; QUDT 3.5.3 pinned unit and quantity-kind **dimension-vector** comparison for `KN`→`Speed` and `DEG`→`Angle` using local source snapshots.
- **BH-V11**: execute pinned T-04 `verify(...require_approved=True)` offline, audit exact local ontology catalog/import closure, reject external/repository-homepage OWL imports. References to external vocabulary terms are permitted, but **external ontologies are NOT imported into MASS OWL in P04**. Tests must reject SHA tampering and catalog/import mutants.
- **BH-V12**: execute legacy `make catalog`, `make validate`, `make cq`, complete `pytest` separately and SysML integrity script. The `--legacy` CLI option executes catalog/validate/cq + SysML integrity; `make test` remains an explicit independent command to prevent recursion. Full BH-V12 PASS requires logs of all four.

**Deferred:** BH-CQ-01…03 strict SPARQL expected bindings (P04-05), CI integration (P04-06), release acceptance (P04-07); P05/P09 tests are DEFERRED.

## Commands

```bash
.venv/bin/python scripts/generate_p04_04_fixture.py --check
.venv/bin/python -m pytest -v tests/test_p04_04_validation.py
.venv/bin/python scripts/run_behavior_validation.py --profile p04 --legacy --report docs/evidence/P04-04/latest-validation.json
make catalog && make validate && make cq && make test
python3 scripts/verify_sysml_kernel_integrity.py
```

Use `--robot /path/to/robot` if executable not on PATH. Robot HermiT must be installed; do not count OWL-RL syntax/axiom lint alone as an independent DL reasoner. If ROBOT/HermiT or a verified vendor artifact is unavailable, BH-V05 is BLOCKED and overall acceptance is not PASS. If T-04 vendor graphs missing/modified, BH-V06 and BH-V11 are BLOCKED/FAIL, not PASS. The original MASS-SK-1.0 source remains unchanged.

**Gate rules:** PASS means executed with positive and rule-specific negative evidence. BLOCKED means dependency missing. FAIL means actual conformance violation or negative mutant was not detected. Test runner does not claim all BH-CQ or v0.4 release PASS.
