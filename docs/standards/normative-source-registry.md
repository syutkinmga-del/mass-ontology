# P04-00 — Normative and Ontology Source Registry (metadata-only)

**Reviewed:** 2026-10-28
**Status:** **APPROVED — metadata-only source governance, corrections SR-01…SR-07 (2026-10-28)**
**Inputs:** Approved MASS-OEF / Roadmap v1.1, DCCR-03 / DCCR-04, approved Terminology & Time Policy T-01…T-04.
**Rule:** Registration ≠ source applicability ≠ ontology term reuse ≠ `owl:imports` ≠ data/engineering validation.

## 1. Metadata protocol

For each source identify: stable registry ID; title; issuer; reference/document ID; publication status and checked date; official landing URL; approved project purpose/scope; release-phase gate; license/access rights; and reviewer/owner. For RDF dependencies also record **namespace IRI**, **ontology IRI**, **version IRI**, **immutable download artifact URL/path**, **SHA-256 computed from downloaded bytes**, **loading/import policy**, and **inference/validation profile**. Unknowns are marked `PENDING`, never filled by guesses.

Statuses: `METADATA_VERIFIED`, `WATCHLIST`, `VERSION_SELECTION_PENDING`, `PINNED_LOCAL_PROFILE`, `CANDIDATE_ALIGNMENT`, `DEFERRED`. Each status applies to its specific field or task, not necessarily the whole ontology.

## 2. Normative and maritime source register

| ID | Source / edition | Verification / primary source | Intended role | Disposition |
|---|---|---|---|---|
| N-01 | IMO **International Code of Safety for MASS**, **Resolution MSC.595(111)**, adopted 2026-05, non-mandatory, effective 2026-07-01 | [IMO resolution index](https://www.imo.org/en/knowledgecentre/indexofimoresolutions/pages/msc-2026-27.aspx), [IMO FAQ](https://www.imo.org/en/mediacentre/hottopics/pages/autonomous-shipping.aspx) | Regulatory applicability and safety evidence, v0.7 | `METADATA_VERIFIED`; obtain controlled full text and applicability profile before rule extraction |
| N-02 | SOLAS, edition and amendments `PENDING` | [IMO SOLAS](https://www.imo.org/en/ourwork/safety/pages/summaryofsolasconvention.aspx) | Requirements and convention interaction v0.7 | `WATCHLIST` |
| N-03 | COLREG 1972 as amended, exact text `PENDING` | [IMO COLREG](https://www.imo.org/en/about/conventions/pages/colreg.aspx) | v0.5 spatial/nav; v0.7 applicability | `WATCHLIST`; no direct behavior-label-to-COLREG inference |
| N-04 | **ISO/TS 23860:2022**, first edition, published 2022-05, currently under systematic review | [ISO](https://www.iso.org/standard/77186.html) | Terminology metadata now; functional/operational semantics v0.6 | `METADATA_VERIFIED`; license/quotation review |
| N-05 | **ISO/AWI 25922**, approved work item stage **20.00**, under development | [ISO](https://www.iso.org/standard/92067.html) | Human/MASS responsibility allocation, v0.6 | `WATCHLIST`; not a published mandatory standard |
| N-06 | IHO S-100, edition/product spec `PENDING` | [IHO](https://iho.int/en/s-100-universal-hydrographic-data-model) | v0.5+ spatial data and hydrographic modeling | `WATCHLIST` |
| N-07 | IALA S-200 series, relevant sub-spec and edition `PENDING` | [IALA](https://www.iala.int/) | ROC/VTS concepts v0.6 | `WATCHLIST` |
| **N-08** | **Recommendation ITU-R M.1371-6 (02/2026)**, approved **2026-02-19**, in force (supersedes M.1371-5) | [ITU](https://www.itu.int/rec/R-REC-M.1371-6-202602-I/en) | AIS message formats, timestamp and sentinel codes, T-01/T-02, P04 | `METADATA_VERIFIED`, exact lawful artifact/edition to pin for field-level validations; avoid unlicensed redistribution |

No entry is a universal claim of legal applicability. The non-mandatory MASS Code scope and any national/classification implementation must be examined in a later applicability model.

## 3. Ontology source register

| ID | Source | Official version evidence | Proposed BH-P04 disposition |
|---|---|---|---|
| O-01 | **SOSA/SSN**, `sosa: <http://www.w3.org/ns/sosa/>`, `ssn: <http://www.w3.org/ns/ssn/>` | W3C [2017 Recommendation](https://www.w3.org/TR/vocab-ssn-2017/) and **2026-10-26 Working Draft** [2023 Edition](https://www.w3.org/TR/vocab-ssn-2023/) | `VERSION_SELECTION_PENDING`: prefer 2017 Recommendation as stable candidate for MVP; 2026 draft as future compatibility review, not automatically approved |
| O-02 | **QUDT**, `qudt: <http://qudt.org/schema/qudt/>`, `unit: <http://qudt.org/vocab/unit/>` | [October 2026 catalog: **3.5.3**](https://www.qudt.org/catalog/qudt-catalog.html), versioned graphs `http://qudt.org/3.5.3/schema/qudt`, `http://qudt.org/3.5.3/vocab/unit`, quantitykind, dimensionvector | **Candidate 3.5.3**; pin exact minimum graph selection, hashes, licenses, test a dimension-aware `unit:KN`/`unit:DEG` whitelist; no unreviewed full imports |
| O-03 | **OWL-Time**, `time: <http://www.w3.org/2006/time#>` | [2017 Recommendation](https://www.w3.org/standards/history/owl-time/), [2022 Candidate Recommendation Draft](https://www.w3.org/TR/owl-time/) | `VERSION_SELECTION_PENDING`; prefer 2017 stable baseline unless later revision required; `bh:TemporalUnit` ≠ `time:TemporalUnit` ≠ `time:ProperInterval` |
| O-04 | **PROV-O**, `prov: <http://www.w3.org/ns/prov#>` | [W3C Recommendation 2013-04-30](https://www.w3.org/TR/prov-o/) | Stable semantic vocabulary; selected RDF artifact/version/path/hash `PENDING` |
| O-05 | GeoSPARQL `geo: <http://www.opengis.net/ont/geosparql#>` | [OGC](https://www.ogc.org/standard/geosparql/) | `DEFERRED` v0.5 |
| O-06 | BFO 2020 | [GitHub project](https://github.com/BFO-ontology/BFO-2020), canonical ontology/version IRI not accepted | `CANDIDATE_ALIGNMENT`, no formal import or equivalence in P04 |
| O-07 | Common Core Ontologies | [GitHub project](https://github.com/CommonCoreOntology/CommonCoreOntologies), canonical ontology/version IRI not accepted | `CANDIDATE_ALIGNMENT`, no formal import or equivalence in P04 |

**QUDT:** The published catalog labels 3.5.3 (2026-10-20). This is **not yet** a verified local snapshot; do not invent SHA256. Note that previous snapshots such as 3.5.2 may appear in search engines; trust the explicitly versioned catalog, not nonversioned 'latest' downloads.

**SOSA/SSN:** W3C's 2026 revision is still a Working Draft as of this review. The old Recommendation and new draft should not be silently mixed.

**BFO/CCO technical debt:** `00-foundation/external-ontology-registry.ttl` uses repository homepages in `foundation:externalOntologyIRI`. Keep this registered as a repair item; no direct `owl:imports` currently established by those literals. A future correction must retain legacy CQ regressions.

## 4. Pending P04 dependency manifest (not an import catalog)

| Resource | Project candidate | Local artifact | SHA-256 | Exact import/profile |
|---|---|---|---|---|
| SOSA/SSN | W3C 2017 Recommendation (recommended, not approved) | `PENDING` | `PENDING` | SOSA observation minimal profile to define |
| QUDT schema | 3.5.3 candidate | `PENDING` | `PENDING` | Verify minimal QuantityValue schema/profile |
| QUDT Units | 3.5.3 candidate | `PENDING` | `PENDING` | Ensure unit:KN and unit:DEG available |
| QUDT Quantity Kinds / Dimension Vectors | 3.5.3 candidate | `PENDING` | `PENDING` | Needed for dimension-aware BH-V06; full/import-lite policy to decide |
| OWL-Time | 2017 Recommendation candidate | `PENDING` | `PENDING` | Time interval/instant profile to define |
| PROV-O | 2013 Recommendation | `PENDING` | `PENDING` | Minimal provenance profile to define |
| ITU-R M.1371-6 AIS message profile | In-force 02/2026 | `PENDING` (controlled, license review) | `PENDING` | No wholesale contents in public ontology repository |

## 5. BH-V11 and implementation gates

1. Before P04-03, resolve O-01 and O-03 version choices, nominate exact QUDT graph set and PROV-O artifact; record local checksums and licensing decisions.
2. Maintain distinct metadata fields for GitHub repository homepage, authoritative ontology IRI and version IRI; never create an `owl:imports` to a GitHub repo URL.
3. Add positive `P04-valid` and negative `N11-repository-url-import` fixtures for BH-V11. The invalid fixture must be rejected because of **that** error, not generic parsing issues.
4. Keep legacy `make catalog`, `make validate`, `make cq` green; add separate profile-aware `make behavior-test` later, not now.
5. No live RDF fetching from the network during CI; reproducible local artifacts and explicit graph loading only.

## 6. Approval decision and outstanding implementation gates

**Decision (2026-10-28):** APPROVED as the metadata-only source registry for MASS Ontology v0.4.0-dev, including corrections **SR-01…SR-07**. The changes and their traceability are recorded in [P04-00 Source Registry Approval Decision](../governance/DEC-2026-10-28-P04-00-source-registry-SR01-SR07.md) and the [technical review](../reviews/P04-00-source-registry-review-2026-10-28.md).

- **SR-01:** Add N-08 (ITU-R M.1371-6), with message-specific timestamp and missing-value semantics; licensed text not republished.
- **SR-02:** Use MSC.595(111) for N-01 MASS Code metadata, keeping its non-mandatory scope explicit.
- **SR-03:** Separate SOSA/SSN 2017 Recommendation from 2026 Working Draft; release selection remains pending.
- **SR-04:** Register QUDT 3.5.3 as a **candidate**, not a checksum-pinned installation.
- **SR-05:** Never equate GitHub BFO/CCO project URLs with authoritative ontology import IRIs.
- **SR-06:** Keep source publication, legal applicability, license, ontology identity, version and checksum as distinct fields.
- **SR-07:** Maintain a machine-readable [BH-P04 dependency manifest](p04-external-dependency-manifest.json) with all downloaded artifacts and hashes **PENDING** until individually verified. No live network retrieval is permitted during CI.

**Not yet approved:** Specific external RDF artifact imports, local snapshot SHA-256 values, BFO/CCO mappings, AIS field-level normalization without an authoritative message profile, or regulatory applicability inference.

**Status of wider P04-00 package:** IN PROGRESS. This document's approval does not establish BH-V11 PASS or close the overall work package.
