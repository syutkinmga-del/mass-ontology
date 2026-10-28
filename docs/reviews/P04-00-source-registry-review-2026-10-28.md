# P04-00 — Normative & Ontology Source Registry: Review

**Project:** MASS Ontology v0.4.0-dev — Observation Core / BH-P04
**Review date:** 2026-10-28
**Review verdict at preparation:** RECOMMEND APPROVAL WITH CORRECTIONS.
**Subsequent governance disposition:** **APPROVED with SR-01…SR-07 on 2026-10-28**; see [approval record](../governance/DEC-2026-10-28-P04-00-source-registry-SR01-SR07.md). This memo preserves pre-approval technical findings; it is not evidence of pinned RDF releases or executed BH-V11.
**Reviewed GitHub baseline:** `docs/standards/normative-source-registry.md` (blob SHA `970451d72ccdc1eadb9338017478e2e4364a3ad9`), `docs/reviews/DCCR-03-ontology-alignment-specification.md`, `docs/reviews/DCCR-04-validation-contract.md`, `docs/architecture/P04-00-terminology-time-policy.md` (APPROVED T-01…T-04).
**Preserve:** approved Roadmap v1.1, DCCR-01…04 and immutable MASS Semantic Kernel; no new OWL axioms and no external `owl:imports` at this review.

## 1. Decision and model of a source

Keep a **metadata-only** source inventory separate from actual, pinned RDF dependencies and from regulatory applicability decisions. A registered source is neither a formal OWL import nor a legally applicable requirement. An exact documentation URL, RDF namespace, ontology IRI, owl:versionIRI, download URL and local artifact checksum are different attributes and must not be conflated.

**Proposed governance states:** `METADATA_VERIFIED`, `VERSION_SELECTION_PENDING`, `PINNED_LOCAL_PROFILE`, `CANDIDATE_ALIGNMENT`, `WATCHLIST`, `DEFERRED`. All external RDF artifact SHA-256 fields remain **PENDING** until files are actually retrieved and hashed. No `BH-V11 PASS` is claimed.

## 2. Normative reference review

| ID | Source | 2026-10-28 verification | Phase and decision |
|---|---|---|---|
| N-01 | IMO MASS Code | **Resolution MSC.595(111)**, adopted May 2026, non-mandatory, effective 2026-07-01; controlled applicability to SOLAS Chapter I cargo ships, wider use encouraged but not universally mandated | `METADATA_VERIFIED`; v0.7 normative applicability model, do not extract requirements into P04 |
| N-02 | SOLAS | Convention and amendments, edition not pinned | `WATCHLIST`, v0.7 |
| N-03 | COLREG 1972 | Convention and amendments, edition not pinned | `WATCHLIST`, v0.5/v0.7, no behavior-label→rule inference |
| N-04 | ISO/TS 23860:2022 | Edition 1, published May 2022, currently under ISO systematic review | `METADATA_VERIFIED`; metadata now, potential terminology review v0.6; copyrighted text not automatically reusable |
| N-05 | ISO/AWI 25922 | Under development; ISO stage 20.00 / approved work item, not a published standard | `WATCHLIST` v0.6; never cite as currently binding |
| N-06 | IHO S-100 | Exact edition and product specification not pinned | `WATCHLIST`, v0.5+ |
| N-07 | IALA S-200 series | Exact member/version not selected | `WATCHLIST`, v0.6 |
| **N-08 (NEW)** | **ITU-R M.1371-6 (02/2026)** | Approved 2026-02-19, **in force**; supersedes M.1371-5 | **P04 source required** for AIS message-field semantics, exceptional/missing codes, time recovery contract T-01/T-02; obtain lawful artifact and record its checksum before field-level validation |

## 3. External RDF vocabulary review

| ID | Vocabulary | Verified state / candidate release | P04 decision |
|---|---|---|---|
| O-01 | SOSA/SSN | W3C Recommendation **2017-10-19** versus newer **Working Draft 2026-10-26** (*2023 Edition* project) | Both recordable, neither should be silently substituted. **Recommend** stable 2017 baseline for initial P04 terms, while separately reviewing newer draft; explicit ADR and immutable artifact required before P04-03. |
| O-02 | QUDT | Official catalog lists **3.5.3**, modified **2026-10-20**: schema, Units, Quantity Kinds, Dimension Vectors | **Recommend candidate 3.5.3** (not yet locally frozen). Capture schema + unit + quantity kind/dimension support profile, licenses, hashes. Use `unit:KN` for knot, `unit:DEG` for angle after checking selected snapshot. |
| O-03 | OWL-Time | W3C **Recommendation 2017-10-19** and **Candidate Recommendation Draft 2022-11-15** | Recommend 2017 as stable normative baseline unless 2022-specific capabilities are justified. Pin exact RDF representation independently. Avoid identifying `bh:TemporalUnit` with `time:TemporalUnit` or `time:ProperInterval`. |
| O-04 | PROV-O | W3C **Recommendation 2013-04-30** | Approved standard as **candidate reuse**; pin RDF profile/version/hash before test. `prov:wasDerivedFrom` ≠ proof of source correctness. |
| O-05 | GeoSPARQL | OGC spatial vocabulary | `DEFERRED` to v0.5, no full import in v0.4 |
| O-06 | BFO 2020 | Current registry incorrectly places repository-homepage URL into `externalOntologyIRI` | `CANDIDATE_ALIGNMENT`; no external imports or equivalentClass. Verify authoritative ontology/version IRI in future ADR. |
| O-07 | CCO | Same repository-homepage-as-IRI problem; exact ontology/release mapping unresolved | `CANDIDATE_ALIGNMENT`; no external imports or equivalentClass. |

## 4. Priority corrections, acceptance boundaries

**SR-01 (high):** Add N-08 ITU-R M.1371-6 to the registry. Check message-specific conventions and license before implementing AIS sentinel-value normalization. Do not reproduce licensed documents in the public repository without permission.

**SR-02 (high):** Update N-01 from general IMO announcement to the authoritative **MSC.595(111)** identifier; keep the Code’s voluntary status and applicability limitations visible.

**SR-03 (high):** Distinguish W3C SOSA/SSN 2017 Recommendation from 2026 Working Draft. Do not adopt the later edition merely because it is newer. Release selection is a pending implementation ADR.

**SR-04 (high):** Propose QUDT **3.5.3** for P04; pin exact schema/Units/Quantity Kinds/Dimension Vector graphs with SHA-256 before BH-V06/BH-V11 pass. Never use a mutable "latest" URL as a reproducible dependency without capturing its bytes/version.

**SR-05 (high):** Keep metadata-only BFO/CCO repository URLs out of `owl:imports`. Existing `foundation:externalOntologyIRI` strings are a technical-debt issue, **not** evidence of a current prohibited `owl:imports` assertion. Future repair must preserve legacy CQ-01…14 semantics or update through controlled change.

**SR-06:** Distinguish normative/document status, legal applicability, RDF profile selection, license and locally computed hash as separate fields. Do not infer that `METADATA_VERIFIED` means `PINNED_LOCAL_PROFILE`.

**SR-07:** Make source-profile selection explicit in P04 fixture and test manifest; record graph-loading/inference semantics (`rdflib` vs `owl:imports`). No network fetch inside CI.

## 5. Registry readiness matrix

| Gate | Evidence | Current finding |
|---|---|---|
| Registry contains justified N/O source inventory | GitHub + external official references | **PARTIAL**, add N-08 and N-01 identifier |
| Publication status authoritative | IMO/ISO/W3C/ITU/QUDT official catalog | **PARTIAL**; key sources verified; IHO/IALA version still future |
| Exact SOSA/SSN baseline selected | Dedicated profile ADR | **PENDING**, recommend 2017 Recommendation |
| Exact QUDT version nominated | QUDT official catalog | **CANDIDATE 3.5.3**, not SHA-pinned |
| OWL-Time / PROV-O artifacts pinned | Local manifest with SHA256 | **PENDING** |
| No unreviewed `owl:imports` | Audit of actual ontology graph | **No BFO/CCO repo-URL import in inspected local registry**; automated BH-V11 still future |
| P04 source registry review | This memo | **RECOMMEND APPROVAL WITH CORRECTIONS**, subject to user approval |

**Review verdict:** Accept the inventory **as a metadata-oriented architecture**, subject to SR-01…SR-07 corrections; do *not* claim all ontology dependencies imported or validated. P04-00 will remain IN PROGRESS until SysML Kernel controlled source is recorded, full local tests/evidence are reconciled, and other P04-00 exit criteria are satisfied.

## 6. Official source links consulted (accessed 2026-10-28)

- IMO MASS Code Resolution MSC.595(111): https://www.imo.org/en/knowledgecentre/indexofimoresolutions/pages/msc-2026-27.aspx
- IMO MASS Code scope/status: https://www.imo.org/en/mediacentre/hottopics/pages/autonomous-shipping.aspx
- ITU-R M.1371-6 (in force): https://www.itu.int/rec/R-REC-M.1371-6-202602-I/en
- ISO/TS 23860:2022: https://www.iso.org/standard/77186.html
- ISO/AWI 25922: https://www.iso.org/standard/92067.html
- W3C SSN 2017: https://www.w3.org/TR/vocab-ssn-2017/
- W3C revised SSN Working Draft: https://www.w3.org/TR/vocab-ssn-2023/
- W3C SSN publication history: https://www.w3.org/standards/history/vocab-ssn-2023/
- QUDT catalog: https://www.qudt.org/catalog/qudt-catalog.html
- QUDT 3.5.3 schema: https://qudt.org/doc/2026/10/DOC_SCHEMA-QUDT.html
- OWL-Time: https://www.w3.org/TR/owl-time/
- OWL-Time history: https://www.w3.org/standards/history/owl-time/
- PROV-O: https://www.w3.org/TR/prov-o/
