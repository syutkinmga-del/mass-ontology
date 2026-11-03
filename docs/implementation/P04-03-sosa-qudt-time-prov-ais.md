# P04-03 — SOSA/SSN Observations, QUDT, OWL-Time, PROV-O, Synthetic AIS Fixture

**Stage:** v0.4.0-dev / BH-P04 Observation Core  
**Status:** IMPLEMENTATION CANDIDATE; external RDF pinning and full validation pending  
**Source implementation baseline (observed GitHub 2026-11-02):** `4d2bc08c050113447b4fd9005809704f858614bc` (P04-02).  
**Design contracts:** DCCR-02/03/04, Roadmap v1.1 §C P04-03, P04-00 approved T-01…T-04 and SR-01…SR-07.  
**P04-01/P04-02:** preserved as immutable integration prerequisites; existing production OWL files are not edited by this package.

## 1. What is implemented

- `05-observation/mass-observation.ttl`: project-local terms for **prevalidated synthetic AIS-like source records**, named observed properties, geodetic position results, explicit receiver/ingestion time metadata, segmentation metadata and coverage-gap evidence. The source records are **not** asserted to be `sosa:Sensor` and no instrument accuracy is inferred.
- `06-quantities/mass-measurement-policy.ttl`: local SOG (`unit:KN`) / COG (`unit:DEG`) unit-reference policy, **not** global QUDT constraints.
- `07-behavior/behavior-observation-bridge.ttl`: defines `bh:supportedByObservation` (physical-state description to SOSA Observation) and `bh:hasQuantityValue` (description to QUDT QuantityValue), preserving separate behavior information and external measurements.
- `tests/observation/fixtures/p04-03-synthetic-input.json`: synthetic, predecoded input with **six source records**, complete event UTC seconds, positions, SOG/COG values, three fixed non-overlapping segments.
- `scripts/generate_p04_03_fixture.py`: generates exactly the same RDF triples byte-for-byte; sorted N-Triples syntax is a valid Turtle subset. **No real NMEA/AIS bitstream decoding** is performed.
- `examples/p04-03-synthetic-ais.ttl`: 370 triples; one generic Vessel and Trajectory, three TemporalUnits, nine concurrent state descriptions, 18 SOSA observations, 12 QUDT QuantityValues, six position results and complete provenance links.
- `docs/standards/p04-03-vocabulary-profile-manifest.json`: source/document candidate selections plus SHA-256 of **project-authored** local profiles. **External ontology release files and SHA-256 are NOT bundled/pinned.**

## 2. Temporal and segmentation policy (T-01, T-03)

Synthetic source event times are supplied as **full UTC seconds**, not recovered from an AIS UTC-second subfield. Each observation has:

- `sosa:phenomenonTime` → explicitly typed `time:Instant` → `time:inXSDDateTimeStamp`, the instant the result applies to;
- `sosa:resultTime` → a timestamp literal for the instant the observation result becomes available, modeled as event+2 seconds in this synthetic processing scenario;
- local `obs:receivedAtTime` and `obs:ingestedAtTime` → source record receipt (event+1s) and ingestion (event+3s) timestamps; these are distinct from each other and from `resultTime`.

There are 3 fixed half-open `[start,end)` segments: **12:00–12:01**, **12:01–12:02**, **12:04–12:05** UTC on 2026-10-28. A sample at 12:01:00 belongs to unit 1, while a source at 12:02:00 (gap start) is rejected. A 2-minute gap is recorded as an `obs:CoverageGap`, not filled with inferred observations. `bh:nextTemporalUnit` has sequence semantics only; no `time:intervalMeets` is asserted. The segmentation run is an explicit `prov:Activity` with method `fixed-boundary-synthetic`, version `1.0.0`, and `[start,end)` policy; source records are retained with derivation links.

## 3. Measurements and unavailable values (T-02)

Each speed/course observation uses `sosa:hasResult` → `qudt:QuantityValue` with `qudt:numericValue` typed `xsd:decimal`, and an explicitly named `qudt:unit`. The local policy allows knots for SOG (`unit:KN`) and angular degrees for true COG (`unit:DEG`); **COG is not heading**. Position observations yield local `obs:PositionResult` with latitude/longitude decimals and explicitly named WGS84/EPSG:4326 CRS, **not GeoSPARQL geometry**.

Unavailable SOG/COG values are represented as `null` + `"unavailable"` in the synthetic input. Such values produce no corresponding quantity/observation, while the source record retains `obs:sourceAvailability`. A non-null numeric value falsely marked unavailable raises an exception. The generator also rejects incomplete timestamps, invalid unit-policy IRIs, unsupported coordinate reference, out-of-range coordinates/COG, samples in the coverage gap, and unapproved segmentation thresholds. **Actual AIS sentinel-code tables and live timestamp reconstruction remain a separate decoder/profile work item under ITU-R M.1371-6.**

## 4. External source reproducibility limitation (T-04, SR-07)

This repository execution environment could not retrieve authoritative external RDF artifacts, so it does **not** claim to have locked the official SOSA/SSN, QUDT, OWL-Time and PROV-O ontology releases. Their **document editions/candidates** are described in `p04-03-vocabulary-profile-manifest.json`, but `selected_rdf_artifact_url`, `ontology_iri_verified`, `version_iri_verified`, `local_snapshot_path` and `snapshot_sha256` remain null until independent verification, licensing review, file acquisition and hashing.

The local adapter module imports **only local MASS ontology IRIs**, resolved through the expanded XML catalog. RDFLib test runners parse these files by explicit local paths; they **do not** dereference external URIs or automatically follow imports. These are *MASS project-authored profiles*, not authoritative RDF snapshots. **BH-V11: BLOCKED** until real standard snapshots and controlled import/profile choices are pinned and audited; do not mark it PASS merely because these tests pass.

## 5. Local tests and release boundary

Execute:

```bash
.venv/bin/python scripts/generate_p04_03_fixture.py --check
.venv/bin/python -m pytest -v tests/test_p04_03_observation.py
make catalog && make validate && make cq && make test
python3 scripts/verify_sysml_kernel_integrity.py
git diff --cached --check
```

The P04-03 pytest suite tests structural links, 3 segment membership, `[start,end)` boundary, documented gap, time semantics, observation/measurement counts, QUDT unit-use, normalized source decimal positions, provenance, missing-value behavior, negative input mutations, deterministic fixture bytes and catalog. These are **implementation checks**, not the official BH-V01/02/03/05/06 SHACL + reasoner acceptance. Official BH-P04 SHACL negative fixtures, external artifact pinning (BH-V11), precise BH-CQ-01…03 SPARQL binding assertions and final CI evidence remain **P04-04 to P04-07**.

**No changes to:** P04-01/02 OWL modules, legacy CQ-01…14, BFO/CCO registry, MASS-SK-1.0, DCCR documents, normative-policy approvals, `OperationalConfiguration` or COLREG inference.

## 6. Architecture review decisions still required

1. Accept project-local `obs:`/`meas:` modules and the choice to keep external RDF axioms unimported until pinned.
2. Confirm `sosa:hasResult` design with typed `qudt:QuantityValue` for SOG/COG, distinct local `PositionResult` for WGS84 position.
3. Confirm explicit distinction of event, result, reception and ingestion time and deterministic synthetic gap and segmentation.
4. Review units/quantitykind external vocabulary release profile and exact local loading/OWL inference mode for P04-04.
5. Collect full-repository test evidence for the commit; no P04-03 acceptance or v0.4.0 release claim without it.
