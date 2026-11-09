# DEC-P05-D05-2026-11-09-01 — approval of Alternative B for EnvironmentSpace

**Decision ID:** `DEC-P05-D05-2026-11-09-01`  
**Decision date:** 2026-11-09  
**Stage:** P05-01 / P05-D05, v0.5.0 / BH-P05  
**Disposition:** **APPROVED — P05-D05 CLOSED / ALTERNATIVE B**  
**Exact approved ADR source commit:** `c4e9e7537b625dc5582b9505af232a959309c622` (PR #9 merge commit; **not** this registration commit)  
**Evidence kind:** `EXPLICIT_OWNER_CHAT_TEXT_NOT_ELECTRONIC_SIGNATURE` — the user expressly approved Alternative B in the project conversation; this is **not** an authenticated digital signature, signed PDF, or independent legal identity verification.  
**Other ADRs:** P05-D04, P05-D06, P05-D07, P05-D08 and P05-D09 remain **OPEN**.  
**v0.5.0 release authorization:** NO.

## 1. Exact owner's approval text

> утверждаю  альтернативу B с условиями: `EnvironmentSpace` как `geo:Feature`, отдельные версионируемые `geo:Geometry`, самостоятельная роль `referencesVessel` и отсутствие автоматических COLREG-выводов.

This is the verbatim owner approval supplied on 2026-11-09, preserved without asserting an independently authenticated electronic signature. This decision registers only the specified P05-D05 model **and its four explicit conditions**. It does not infer authorization for any other architectural design decision.

## 2. Approved architectural disposition

The owner approves [Alternative B of ADR-P05-D05](../architecture/ADR-P05-D05-environmentspace-feature-reference.md), as previously proposed and tested at the exact commit above, subject to:

| ID | Approved constraint | Implementation boundary |
|---|---|---|
| D05-B01 | `bh:EnvironmentSpace` is modeled as a domain-scoped specialization of `geo:Feature` | Use `rdfs:subClassOf geo:Feature` in the later reviewed ontology module. **Do not** use `owl:equivalentClass`; a geographic feature is not inherently an ODD/OE, encounter or geometry individual |
| D05-B02 | `geo:Geometry` instances are **distinct, versioned representations**, not the environmental feature itself | Connect via `geo:hasGeometry`; preserve separate geometry IRIs, source/edition, validity/provenance where supplied; prevent silent replacement. P05-D08 still governs temporal selection and calculations |
| D05-B03 | `bh:referencesVessel` is an **independent reference-object role**, distinct from `bh:referencesSpace` | A relation description may refer to a separate `maritime:Vessel` without typing it as `EnvironmentSpace`. The existing ADR proposes a curated XOR-reference validation rule and exclusion of self-reference; implementation tests occur in P05-03 |
| D05-B04 | **No automatic COLREG conclusions** arise from feature/geometry/reference relations | No automatic `nav:Crossing`, `nav:COLREGRule`, collision-risk conclusion, maneuver, operational authority or safety-certification claim from the D05 axioms |

**Terminology:** Approval of `EnvironmentSpace` as a `geo:Feature` means *specialization* under GeoSPARQL, **not** equivalence of all GeoSPARQL features to this maritime domain concept. Approved `geo:Geometry` versioning describes record/representation identity and provenance; it is not itself a claim that real-world zone boundaries remain continuously valid.

The proposed `bh:referencesVessel` name and separation of roles can be implemented in their appropriate P05 profile module, with SHACL constraints specifying cardinality and reference-role exclusivity. **No assertion that `maritime:Vessel` is globally a subclass of `geo:Feature` is authorized.**

## 3. Evidence, immutable source and non-self-reference

The approved design is exactly the historical, pre-registration commit:

- `c4e9e7537b625dc5582b9505af232a959309c622` — merged [PR #9](https://github.com/syutkinmga-del/mass-ontology/pull/9).
- Original ADR blob: `docs/architecture/ADR-P05-D05-environmentspace-feature-reference.md` at Git blob `1c3177e15da6e5d0bfd11760dbeea6630bc48910`.
- Original machine design record: `docs/standards/P05-01-environmentspace-adr-candidate.json` at Git blob `1c8269d568689393cdf42d121fb0f42630b72f59`.
- [P05-01 ADR Design Gate #42605359691](https://github.com/syutkinmga-del/mass-ontology/actions/runs/42605359691): `success` on the above commit; 14 design-only pytest cases, no BH-P05 runtime claim.
- Six successful workflows on the PR #9 merged commit; these establish review of the *proposal*, **not** a post-registration electronic signature.

The prior [P05-00 design decision](DEC-P05-00-2026-11-09-design-approval.md) and candidate ADR predate this authorization. Their `OPEN` labels reflect their historical **as-of** state and must not be silently rewritten; this later document is the **authoritative D05 status transition**, registered independently.

The separate machine-readable approval [P05-D05-owner-approval.json](../standards/P05-D05-owner-approval.json) records current D05 status and the earlier immutable source/blob IDs. This approval file and future governance merge have *different* Git SHAs. Neither retroactively changes which ADR version the owner approved.

## 4. Authorized next scope and unresolved dependencies

**Authorized next engineering activity:** a separate, reviewed **P05-01 implementation PR** can introduce the narrow `bh:EnvironmentSpace` / `geo:Feature` feature-identity module and its local shapes and synthetic positive/negative fixtures, with regression tests. Only the D05-scoped properties are approved. Do not change P04 historic data/claims.

**Explicitly not approved:**

- Importing or redistributing unreviewed GeoSPARQL publisher RDF before **P05-D04** (exact artifact/version/IRI, rights, SHA-256, runtime support) is resolved. Referencing OGC terms as IRIs in local vocabulary **does not** imply an OWL import or GeoSPARQL engine conformance.
- Treating geometry edition, validity/synchronization, distance computation or bearings as verified before **P05-D08**.
- Resolving OWL/SKOS taxonomy (**P05-D06**), semantic hypotheses/confidence (**P05-D07**) or P05 runtime acceptance harness (**P05-D09**) by this decision.
- Stating BH-P05 tests are `PASS` before their tests actually execute; BH-CQ-04…10 and BH-V04/V07/V08/V09/V10 remain `DEFERRED` at this governance registration.
- Publishing, tagging or approving v0.5.0; modifying v0.4.0 tag `9da6a854d663d8c3b455f96521ea87d3579646cc` / target `d0f2368df4268cfe3c6079a1681502cad0b867fb`.

## 5. Status

**P05-D05: CLOSED — APPROVED ALTERNATIVE B**, subject to the four constraints above. **P05-D04/D06/D07/D08/D09: OPEN**. P05-01 *design approval* is complete; production OWL/SHACL and functional validation are a separate pending implementation task. The approval evidence is a text instruction, not an electronic signature.
