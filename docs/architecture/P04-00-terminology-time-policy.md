# P04-00 — Terminology, IRI, Time and Segmentation Policy

**Date:** 2026-10-28
**Status:** PROPOSED FOR P04-00 ACCEPTANCE (not a change to DCCR-01…04)

## 1. Scope

This policy prepares v0.4.0 Observation Core. It does not authorize `v0.5` InteractionBehavior, SemanticBehavior, GeoSPARQL geometry, ODD inference, COLREG reasoning or ROC authority in P04.

## 2. Names and identity

- Namespace proposals preserved from approved DCCR-03: `bh: <https://w3id.org/mass-ontology/behavior#>`, `maritime: <https://w3id.org/mass-ontology/maritime#>` (verify exact `maritime:` prefix in the approved DCCR-03 prior to production), while `common:`, `mass:` and `nav:` are existing namespaces.
- Ontology IRI for Behavior is *proposed*: `https://w3id.org/mass-ontology/behavior` without the fragment. The namespace has not been verified as resolvable.
- Class names are singular `UpperCamelCase`: `Trajectory`, `TemporalUnit`, `PhysicalBehavior`, `SpeedState`.
- Properties use `lowerCamelCase`: `hasTrajectory`, `hasTemporalUnit`, `ofVessel`, `hasTemporalExtent`, `supportedByObservation`.
- One unambiguous English `rdfs:label` + `rdfs:comment`/`skos:definition` (as appropriate), source citation and version ownership per class, along with target BH-CQ and example instance.
- `maritime:Vessel` is a generic real vessel class; `mass:MASSVessel` is narrower; `nav:TargetShip` is a context role, NOT a claim of autonomy. P04-01 decides exactly how to avoid type confusion.
- `Trajectory` is an information record, NOT a vessel motion process or route plan. `TemporalUnit` is an information segment, NOT `time:ProperInterval`. `PositionState`, `SpeedState`, `CourseState` are concurrent descriptive dimensions and may coexist.
- No production `owl:equivalentClass`, `owl:disjointWith` or BFO/CCO equivalence without ADR + reasoner and regression evidence.

## 3. Temporal data conventions (P04 proposal)

| Aspect | Proposed rule |
|---|---|
| Canonical processing time | UTC instants with an explicit `Z`/numeric offset, normalized before comparison |
| RDF serialization | `xsd:dateTimeStamp` for OWL-Time `time:inXSDDateTimeStamp` on `time:Instant`; `xsd:dateTime` allowed only where vocabulary property explicitly permits and offset is always present |
| Precision in synthetic fixture | 1-second input timestamps; preserve original input resolution and provenance; no fabricated subseconds |
| Observed/phenomenon time | `sosa:phenomenonTime` for temporal applicability of an observation |
| Result time | `sosa:resultTime` for result generation time, distinct from phenomenon time |
| AIS acquisition/receipt | separate ingestion timestamp with explicitly named local property or processing provenance; not inferred from incomplete AIS UTC-second field |
| TemporalUnit extent | `bh:hasTemporalExtent` links to distinct `time:ProperInterval`; no `rdf:type time:ProperInterval` on the unit record |
| Interval validity | begin < end, normalized to UTC; no zero-length ProperInterval |
| Segment data ownership | Adopt `[start,end)` in ingestion algorithm for assigning samples to segments; this is an implementation convention, not an OWL-Time endpoint axiom |
| `nextTemporalUnit` | sequence adjacency is defined by segmentation order and may allow a coverage gap |
| `time:intervalMeets` | assert on **interval individuals only**, when normalized end of first equals start of second exactly; never infer it just from sequence adjacency |
| Missing data | explicit missingness and gap metadata; never interpolate across unknown intervals by default |

**Required design decision before P04-03:** confirm whether incoming AIS records include a trusted complete UTC time. If only the AIS second field is present, record a separate receiver timestamp and reconstruct event time only with an explicitly documented source/rule and uncertainty. Also define whether the fixture demonstrates multiple non-overlapping units or a single unit; prefer 2-3 for BH-V03.

## 4. Segmentation policy (P04 synthetic dataset only)

- Segmentation is **not** equivalent to classification of real-world behavior or COLREG situations.
- The P04 fixture will use predetermined non-overlapping segments with a segmentation identifier, index and derivation/source metadata. Segmentation algorithm/version are recorded explicitly.
- Initial policy: deterministic boundaries with no interpolation and no classification-based boundary discovery. Keep a gap visible if missing samples or skipped periods make a segment discontinuous.
- No physical threshold for changes of SOG/COG or automatic inactivity gap (e.g. 30/60/180 seconds) is asserted as a general truth. Threshold selection is an *open empirical decision* for real AIS inputs and later inference work.
- Observation samples at exactly a segment boundary follow the ingestion convention `[start,end)` in the fixture; record this in fixture README and test cases.
- All temporal ordering checks must parse actual datetime values and normalize offsets, not lexically compare timestamp strings.

## 5. Quantity and spatial placeholders

- P04 uses QUDT `qudt:QuantityValue`, `qudt:numericValue`, `qudt:unit` for SOG/COG. Candidate units: `unit:KN` (knot, speed) and `unit:DEG` (angle); exact QUDT artifact version/IRI and permitted quantity kinds must be pinned before tests are marked PASS.
- Distinguish Course Over Ground (COG) from true heading or compass bearing; state the frame/reference (true/geodetic) in fixture metadata.
- If using positions, store latitude/longitude with a known WGS84/CRS convention, but **do not** infer GeoSPARQL geometry / spatial topological relations in P04 (reserved v0.5).

## 6. Decision to be recorded

**Proposed acceptance:** P04-00 adopts these conventions for v0.4 synthetic fixture; exact imports/releases, AIS timestamp recovery, real-data segmentation thresholds, operational configurations and behavior taxonomies remain separate later decisions. Acceptance requires a reviewer and a dated commit/decision record.
