# P05-01 — Implemented D05 local EnvironmentSpace OWL/SHACL profile

**Implementation date:** 2026-11-10  
**Target release:** v0.5.0 / BH-P05 (**not released**)  
**Owner architecture decision:** [DEC-P05-D05-2026-11-09-01](../governance/DEC-P05-D05-2026-11-09-alternative-b-approval.md), **CLOSED / Alternative B**; owner text is not an authenticated electronic signature.  
**Scope:** D05-approved *feature identity and geometry edition records only*. This is a production **local ontology module**, not complete BH-P05 ontology conformance.

## 1. Implemented elements and evidence

| ID | Requirement / owner condition | Implemented artifact | Local acceptance |
|---|---|---|---|
| D05-B01 | `bh:EnvironmentSpace rdfs:subClassOf geo:Feature`, not equivalence and not geometry | [`environment-space-p05.ttl`](../../07-behavior/environment-space-p05.ttl) | OWL structural checks and SHACL `P05EnvironmentSpaceShape` |
| D05-B02 | Separate `geo:Geometry` records with edition source, no unqualified default | `bh:geometryEditionId`, `geo:hasGeometry`, `prov:wasDerivedFrom`, [local SHACL shapes](../../shapes/environment-space-p05.shacl.ttl) | Positive two-edition fixture; negatives N01–N07 |
| D05-B03 | `bh:referencesVessel` independent from `bh:referencesSpace` | Two distinct OWL ObjectProperty IRIs with corresponding ranges | Structural schema tests. **InteractionBehavior instances and XOR role validation remain P05-03** |
| D05-B04 | No automatic COLREG, risk, maneuvers or control | No equivalence, chains, operational rules or COLREG axioms | Schema mutation checks and negative fixture N08 |

Local ontology IRI: `https://w3id.org/mass-ontology/environment-space`, added to [local catalog](../../catalog-v001.xml) with **only local imports** of the P04 `behavior` and `maritime` ontologies. External `geo:` and `prov:` terms are **referenced by IRI only**, not imported, downloaded, redistributed or asserted to be a vendor-pinned ontology.

## 2. Synthetic data semantics and limits

[Positive fixture](../../tests/spatial/fixtures/p05-01-environmentspace-valid.ttl) contains **one clearly synthetic identified environmental zone**, two **different** geo:Geometry IRIs with source-edition IDs `synthetic-edition-A` and `synthetic-edition-B`, two explicit provenance `prov:Entity` sources and WKT strings tagged with CRS84 longitude–latitude coordinate convention. A separately typed `maritime:Vessel` is present without EnvironmentSpace typing. The geometries are examples, **not legally valid areas, sea charts or evidence of navigation risk**.

- **SHACL Core** checks explicit feature/geometry separation, at least one geometry, each geometry's explicit type, a single nonempty edition ID, a single explicitly typed source entity, typed WKT, no unqualified default or `owl:sameAs`.
- **Curated Python oracle** independently checks explicit source types, unique edition identifiers per zone, feature/geometry identity separation and absence of unsupported zone-level COLREG/operational assertions. It does **not** infer the real-world accuracy or validity of asserted source identities.
- **8 negative Turtle fixtures** are stored in `tests/spatial/fixtures/invalid`; the Python/SHACL composite harness requires each to be rejected by its expected D05 condition. **8 independent OWL mutation tests** exercise incorrect hierarchy, property ranges, forbidden imports, equivalence and COLREG chains.
- **No automatic GeoSPARQL `geof:` invocation, geometric ring closure/topology checks, coordinate transform, chart edition authenticity, temporal validity selection, bearings or geodesic calculations**. The `geo:wktLiteral` datatype check means *only that a literal is marked with the expected RDF datatype*; it is not a guarantee of valid WKT geometry, axis order or area membership.

## 3. Distinguishing local P05-01 results from full BH-P05

The new [runner](../../scripts/validate_p05_01_environmentspace.py) returns a profile called `P05-01-D05-LOCAL`; it is **not** `p05` and must not be surfaced as **BH-P05 PASS**. The dedicated [workflow](../../.github/workflows/p05-01-environmentspace-implementation.yml) runs with pinned direct Python dependencies in a separate CI job; existing P04 runner and legacy CQ evidence stay untouched.

**Formal BH-CQ-04…10 and BH-V04/V07/V08/V09/V10: DEFERRED.**

| ADR | Status after this implementation | Meaning |
|---|---|---|
| **P05-D05** | **CLOSED** | Alternative B source model approved, and narrow local OWL/SHACL implementation presented here |
| P05-D04 | OPEN | Choose exact GeoSPARQL publisher RDF/version/licensing/IRI/SHA and demonstrate real engine capabilities |
| P05-D06 | OPEN | SemanticBehavior representation and taxonomy policy |
| P05-D07 | OPEN | Provenance/status/confidence for behavior interpretations |
| P05-D08 | OPEN | Geometry selection/time validity/synchronization/metric and bearing policy |
| P05-D09 | OPEN | Complete P05 fail-closed validation runner, CQs, positive/negative evidence and release gates |

The Geometry edition identifier is **not** a timestamp or a guarantee that the geometry edition is valid for any observed position; that determination is pending P05-D08. Reusing `geo:Feature` as an external class IRI is not a test of external publisher ontology conformance; that requires P05-D04.

## 4. Acceptance requirements for this PR

**Must pass:** dedicated local P05-01 source/fixtures/SHACL/mutations check, P05-D05 owner source approval check, original P05-00 design checks, and independent P04 legacy/CQ/SHACL/BH-P04 regression CI.

**Must remain absent:** unreviewed publisher GeoSPARQL `owl:imports` or new vendored RDF, any change to frozen v0.4.0 tag/source, historical DCCR/owner approvals, MASS-SK-1.0, P04 AIS fixture or existing release notes, and any assertion that v0.5.0 may be released.

**Next after this scope:** review and close P05-D04 (official GeoSPARQL RDF and engine evidence), and separately address P05-D08 (geometry/time/metric policy) before spatial computation and BH-P05 full acceptance. P05-03 will exercise `InteractionBehavior` reference roles (XOR/self-reference) independently.
