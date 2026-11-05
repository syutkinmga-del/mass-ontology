# Third-party RDF notices — BH-P04 / T-04 (release candidate)

**Status: RIGHTS-HOLDER REVIEW REQUIRED BEFORE PUBLIC v0.4.0 RELEASE.**

This notice documents the exact snapshots referenced by `docs/standards/T04-external-rdf-lock.json` and preserved *byte-for-byte* in `vendor/external-rdf/T04-2026/`. It is prepared for project-owner approval, not a legal conclusion, not a transfer of rights, and not a license for MASS-authored files. Existing T-04 `APPROVED_BY_PROJECT_OWNER` source acquisition/licensing evidence is retained unchanged. No standard RDF file has been edited for this remediation.

## Per-file provenance, licensing and attribution

| Vendored file (under `vendor/external-rdf/T04-2026/`) | Publisher/attribution | Selected release | Licensing source / review |
|---|---|---|---|
| `sosa-2017.ttl` | W3C/OGC Spatial Data on the Web Working Group; Copyright 2017 W3C/OGC | W3C SOSA 2017 | In-file `dcterms:license` links to W3C 2015 Software & Document and OGC Software License |
| `ssn-2017.ttl` | W3C/OGC Spatial Data on the Web Working Group; Copyright 2017 W3C/OGC | W3C SSN 2017 | In-file dual W3C 2015 Software & Document and OGC Software License links |
| `qudt-schema-3.5.3.ttl` | QUDT.org | QUDT 3.5.3 | CC BY 4.0, attribution to QUDT.org |
| `qudt-unit-3.5.3.ttl` | QUDT.org | QUDT 3.5.3 | CC BY 4.0, attribution to QUDT.org |
| `qudt-quantitykind-3.5.3.ttl` | QUDT.org | QUDT 3.5.3 | CC BY 4.0, attribution to QUDT.org |
| `qudt-dimensionvector-3.5.3.ttl` | QUDT.org | QUDT 3.5.3 | CC BY 4.0, attribution to QUDT.org |
| `owl-time.ttl` | W3C and OGC; Copyright © 2006–2017 W3C, OGC | Pinned OWL-Time RDF, not an assertion of unchanged 2017 specification bytes | **In the pinned RDF, `dct:license` explicitly identifies CC BY 4.0.** Retain W3C/OGC copyright and usage notices. The T-04 review described W3C software/document terms; reconcile the different description before final approval. |
| `prov-o.ttl` | W3C Provenance Working Group | PROV-O | The pinned RDF contains an `owl:Ontology` declaration but no explicit per-ontology license triple in its opening metadata. T-04 cites W3C Software & Document terms. Verify applicability for this *specific* redistributed file and preserve associated copyright notices before sign-off. |

### Upstream links

- W3C/OGC SOSA: https://www.w3.org/ns/sosa/2017
- W3C/OGC SSN: https://www.w3.org/ns/ssn/2017
- W3C Software and Document License (2015): https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
- OGC Software License: https://www.ogc.org/about/policies/
- QUDT.org licensing and credit: https://qudt.org/ ; https://qudt.org/doc/DOC_SCHEMA-QUDT.html
- Creative Commons Attribution 4.0 International: https://creativecommons.org/licenses/by/4.0/
- OWL-Time: https://www.w3.org/2006/time
- PROV-O: https://www.w3.org/ns/prov-o.ttl ; https://www.w3.org/TR/prov-o/

## Modifications and license separation

The **eight T-04 publisher RDF snapshots have not been modified**. They are referenced by their canonical vocabulary terms and verified against the byte hashes in `T04-external-rdf-lock.json`. MASS-authored `examples/p04-04-synthetic-ais-qudt353.ttl` is a distinct derived *project-owned synthetic fixture*, not a rewritten publisher QUDT ontology.

The project license selected for MASS-authored OWL, examples, documentation and scripts **must not be represented as licensing these third-party files**. This notice and all upstream copyright declarations must be preserved when the snapshots are redistributed. For QUDT and pinned OWL-Time CC BY 4.0, include attribution, license URL, and a statement that upstream RDF files are unchanged.

## Final legal/owner controls — pending

1. Verify the pinned OWL-Time `dct:license=CC BY 4.0` against the earlier T-04 W3C-license summary, including required copyright/usage notices.
2. Determine the applicable redistributable license/notice for the exact pinned `prov-o.ttl` file rather than inferring it solely from the broader W3C website.
3. Verify that both W3C and OGC attribution and license terms for 2017 SOSA/SSN are retained.
4. Record actual project-owner approval of all eight notices and any residual rights risks in `docs/governance/DEC-P04-07-rights-approval.json`, including the SHA-256 of this file and the selected project `LICENSE`.
5. Until that explicit review is recorded and validated, **RR-05 remains PENDING** and R08 must not be reported PASS.
