# Governance Decision — P04-00 Normative & Ontology Source Registry

**Decision ID:** DEC-2026-10-28-P04-00-SR
**Decision date:** 2026-10-28
**Status:** **APPROVED (with corrections SR-01…SR-07)**
**Scope:** MASS Ontology Stack, Roadmap v1.1, P04-00 / v0.4.0-dev / BH-P04
**Authority:** Project approval recorded in the conversation on 2026-10-28.
**Reviewed source:** `docs/standards/normative-source-registry.md`, prior Git blob `970451d72ccdc1eadb9338017478e2e4364a3ad9`; supporting [technical review](../reviews/P04-00-source-registry-review-2026-10-28.md).

## 1. Decision

APPROVE the **Normative & Ontology Source Registry** as a **metadata-only** controlled inventory for the MASS Ontology, subject to the seven accepted corrections below. The approved document is [the revised registry](../standards/normative-source-registry.md). Its status does not authorize wholesale external ontology imports, new requirements assertions, vessel-specific legal applicability inference, or any change to immutable `MASSKernel_v1.0.sysml`.

| Correction | Binding project disposition | Release gate |
|---|---|---|
| SR-01 | Register ITU-R M.1371-6 (02/2026) as N-08 for source-specific AIS timestamp and sentinel-value semantics; obey license/access terms | Field-level fixture implementation, P04-03 |
| SR-02 | Identify IMO MASS Code by Resolution MSC.595(111); retain non-mandatory and conditional applicability status | Any normative interpretation, v0.7 |
| SR-03 | Distinguish SOSA/SSN 2017 Recommendation from 2026 Working Draft; do not silently substitute | Exact release choice and RDF artifact before P04-03 |
| SR-04 | Record QUDT 3.5.3 as a candidate, not a locally pinned import | Actual graph set, units, license and SHA-256 before P04-03 / BH-V06 |
| SR-05 | Treat BFO/CCO GitHub repository URLs as **repository links**, not authoritative ontology/version IRIs; prohibit their use as `owl:imports` | BH-V11 and future alignment ADR; protect legacy CQs |
| SR-06 | Keep edition/status, normative applicability, ontology/namespace/version IRI, artifact, license and checksum separate | Source and dependency manifest review |
| SR-07 | Record a deterministic artifact/profile manifest; no live external RDF fetch in CI | Before P04-03 and BH-V11 execution |

## 2. Approved architectural boundaries

1. The presence of a source in the registry is **not** legal applicability or an assertion of compliance.
2. Namespace term reuse is distinct from importing full OWL axiomatizations or their entailments.
3. Exact RDF ontology/version IRIs, distribution artifacts, local paths and SHA-256 checksums remain **PENDING** until verified from actual bytes. A `VERSION_SELECTION_PENDING` entry is not a `PINNED_LOCAL_PROFILE`.
4. The old foundation registry has candidate BFO/CCO values in `foundation:externalOntologyIRI` that point to GitHub repositories. Record the technical debt; do not silently edit the production TTL in this P04-00 decision.
5. Do not alter DCCR-01…04, MASS-OEF, Roadmap v1.1 or production RDF/OWL in this approval.

## 3. Implementation evidence still required

- Resolve exact SOSA/SSN and OWL-Time release selections (2017 is a **recommended candidate**, not yet a ratified local snapshot).
- Select actual QUDT schema/unit/quantitykind/dimension-vector distributions, test the intended unit and quantity-kind mappings, and record SHA-256 and license terms.
- Select PROV-O RDF distribution and a controlled profile; record checksum, namespace/ontology IRI and graph-loading method.
- Capture the ITU-R M.1371-6 controlled source reference and the AIS message-type field rules actually implemented.
- Implement positive and negative BH-V11 checks, preserving all 14 existing CQs and legacy SHACL/catalog behavior.
- Complete the remaining P04-00 baseline/SysML evidence tasks independently of this registry approval.

**Current gate:** Registry governance = **APPROVED**; external dependency pinning = **PENDING**; BH-V11 = **NOT EXECUTED**; overall P04-00 = **IN PROGRESS**.
