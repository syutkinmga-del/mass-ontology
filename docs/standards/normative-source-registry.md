# P04-00 — Normative and Ontology Source Registry (metadata-only)

**Date created:** 2026-10-28
**Status:** DRAFT / CANDIDATE SOURCES — no normative requirement ingestion or ontology imports approved

## 1. Rules for the registry

Every source entry stores: document/ontology, issuer, observed version/edition/status, authoritative metadata link, intended use, implementation phase, license/access condition, local artifact checksum once captured, and review disposition. A source appearing here is not automatically applicable to any vessel or legally mandatory. Publication and `owl:imports` require separate validation of canonical ontology IRI, exact release/version, license, checksum, and semantic compatibility.

## 2. Maritime/normative sources

| ID | Source | Issuer / edition-status evidence | Intended use | Phase | Import/applicability status |
|---|---|---|---|---|---|
| N-01 | International Code of Safety for MASS (MASS Code) | IMO press release 2026-05-22; initial non-mandatory Code effective 2026-07-01; https://www.imo.org/en/mediacentre/pressbriefings/pages/imo-adopts-mass-code.aspx | Future source-aware applicability model | v0.7 | METADATA ONLY; obtain definitive adopted text/identifier before rule extraction |
| N-02 | SOLAS | IMO; edition/amendments to be selected; https://www.imo.org/en/ourwork/safety/pages/summaryofsolasconvention.aspx | Vessel safety requirement context | v0.7 | WATCHLIST; no applicability inference |
| N-03 | COLREG 1972 (as amended) | IMO; consolidated edition/amendments to select; https://www.imo.org/en/about/conventions/pages/colreg.aspx | Navigation rule contexts | v0.5 / v0.7 | WATCHLIST; no blanket mapping from behavior label |
| N-04 | ISO/TS 23860:2022 | ISO technical specification, edition 1 published 2022-05; https://www.iso.org/standard/77186.html | Autonomous-ship vocabulary | P04 metadata / v0.6 ontology review | METADATA; licensed standard text must be checked before quoting definitions |
| N-05 | ISO/AWI 25922 | ISO project, working draft status as previously identified; verify actual ISO stage when used; https://www.iso.org/standard/92067.html | Capabilities/role allocation terminology candidate | v0.6 | WATCHLIST; not published normative requirement here |
| N-06 | IHO S-100 | IHO; exact edition and product spec to pin; https://iho.int/en/s-100-universal-hydrographic-data-model | Hydrographic/spatial reference models | v0.5+ | WATCHLIST |
| N-07 | IALA S-200 series | IALA; exact product specification/version to pin; https://www.iala.int | VTS/port data concepts | v0.6 | WATCHLIST |

## 3. Ontology/technical standards

| ID | Vocabulary | Canonical documentation URL / namespace | Purpose | Version/import gate |
|---|---|---|---|---|
| O-01 | SOSA / SSN | https://www.w3.org/TR/vocab-ssn-2023/ ; `http://www.w3.org/ns/sosa/`, `http://www.w3.org/ns/ssn/` | Observations, observed property, phenomenon/result time | Select exact RDF snapshot and verify specification status; P04 |
| O-02 | QUDT | https://www.qudt.org/ ; `http://qudt.org/schema/qudt/`; `http://qudt.org/vocab/unit/` | Quantities and unit kinds (e.g. knot, degree) | Pin schema + unit vocabulary version and checksum; P04 |
| O-03 | OWL-Time | https://www.w3.org/TR/owl-time/ ; `http://www.w3.org/2006/time#` | Intervals and temporal relations | Pin W3C ontology artifact/version; P04 |
| O-04 | PROV-O | https://www.w3.org/TR/prov-o/ ; `http://www.w3.org/ns/prov#` | Provenance of observations, segmentation and assessment | Pin vocabulary release; P04 |
| O-05 | GeoSPARQL | https://www.ogc.org/standard/geosparql/ ; `http://www.opengis.net/ont/geosparql#` | Spatial features and relations | Deferred v0.5 |
| O-06 | BFO 2020 | https://github.com/BFO-ontology/BFO-2020 | Upper-ontology alignment candidate | Candidate only; do NOT use GitHub repository URL as `owl:imports` ontology IRI |
| O-07 | Common Core Ontologies | https://github.com/CommonCoreOntology/CommonCoreOntologies | Mid-level alignment candidate | Candidate only; exact authoritative ontology/release IRI unresolved |

## 4. Discovered registry issue and action

The local `00-foundation/external-ontology-registry.ttl` currently records BFO/CCO **GitHub repository home URLs** in `foundation:externalOntologyIRI`, and separately repeats them in `foundation:externalOntologyRepository`. The registry field name overclaims semantic identity. At P04-00, **record the issue only**. Before BH-V11 can PASS in production, decide whether to replace the ontology-IRI value with a verified canonical IRI or introduce an explicit unresolved-IRI status; keep all changes compatible with legacy `CQ-01…14` and the catalog.

## 5. Source metadata acceptance checklist

- [ ] Exact source version and publisher verified for each P04 dependency (SOSA/SSN, QUDT, OWL-Time, PROV-O).
- [ ] Local release artifact path/checksum/semantic profile recorded if needed for deterministic CI.
- [ ] Access/license reviewed and citation instructions documented.
- [ ] Registry issue for BFO/CCO ontologyIRI assigned with an owner and decision gate.
- [ ] Distinct normative publication vs applicability vs technical-vocabulary reuse reflected in all source records.

This file is a metadata inventory, **not** imported regulatory text, a compliance matrix, or a formal assertion that norms apply to an operational configuration.
