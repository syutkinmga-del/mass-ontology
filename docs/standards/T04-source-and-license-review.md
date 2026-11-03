# T-04 — Controlled RDF Snapshot and Licensing Review

**Project:** MASS Ontology / BH-P04 Observation Core  
**Status:** T-04 COMPLETE — RDF BYTE/IRI/TERMS VERIFIED; LICENSES APPROVED BY PROJECT OWNER; BH-V11 PENDING.
**Input:** Approved T-04, SR-03/SR-04/SR-06/SR-07; P04-03 source manifest, no changes to DCCR.

## Controlled choices

| ID | Selected data artifact URL (request `Accept: text/turtle`) | Controlled edition / IRI | License evidence |
|---|---|---|---|
| SOSA-2017 | `https://www.w3.org/ns/sosa/2017` | SOSA/SSN 2017 Recommendation; namespace `http://www.w3.org/ns/sosa/`, 2017 edition version IRI | W3C + OGC license declarations within 2017 ontology: W3C 2015 software/document and OGC software |
| SSN-2017 | `https://www.w3.org/ns/ssn/2017` | SOSA/SSN 2017 Recommendation; namespace `http://www.w3.org/ns/ssn/`, 2017 edition version IRI | Same dual W3C/OGC notices |
| QUDT-SCHEMA-3.5.3 | `https://qudt.org/3.5.3/schema/qudt` | QUDT OWL schema, versioned graph 3.5.3 | QUDT CC BY 4.0; credit QUDT.org |
| QUDT-UNITS-3.5.3 | `https://qudt.org/3.5.3/vocab/unit` | Unit graph 3.5.3 | QUDT CC BY 4.0 |
| QUDT-QUANTITYKIND-3.5.3 | `https://qudt.org/3.5.3/vocab/quantitykind` | Quantity-kind graph 3.5.3 | QUDT CC BY 4.0 |
| QUDT-DIMENSIONVECTOR-3.5.3 | `https://qudt.org/3.5.3/vocab/dimensionvector` | Dimension-vector graph 3.5.3 | QUDT CC BY 4.0 |
| OWL-TIME | `https://www.w3.org/2006/time` | W3C 2017 Recommendation vocabulary with possible maintenance updates; inspect actual `owl:versionIRI` and RDF identity; do not silently claim exact 2017 bytes | Applicable W3C software/document terms must be checked against RDF work |
| PROV-O | `https://www.w3.org/ns/prov-o.ttl` | W3C PROV-O Recommendation 2013; namespace `http://www.w3.org/ns/prov#` | Applicable W3C software/document terms must be checked against RDF work |

Sources: https://www.w3.org/TR/vocab-ssn-2017/ ; https://www.w3.org/TR/vocab-ssn-2023/ ; https://www.qudt.org/catalog/qudt-catalog.html ; https://www.w3.org/standards/history/owl-time/ ; https://www.w3.org/TR/prov-o/ ; https://qudt.org/ ; https://www.w3.org/copyright/software-license-2015/ ; https://www.w3.org/2015/spatial/wiki/Ontology_rights_and_licence.html

**Fallback for the 2017 SOSA/SSN pair:** if W3C permanent version URL cannot be retrieved/parsed, the acquisition script may select the official W3C `w3c/sdw` source at the immutable commit `f3171647f6437b73e1caf871f056d233feb4a9da`. It verifies the exact upstream Git blob SHA-1 (Git identity), then records SHA-256 of the same bytes. The lock includes the actual selected `resolved_url` and never silently treats the fallback as the original W3C version endpoint.

## Policy: license and attribution

- W3C/OGC 2017 ontology: preserve all original notices and include link to both W3C and OGC applicable licensing terms. W3C 2015 Software and Document License requires retained notice and attribution for any redistribution; OGC terms also apply.
- QUDT.org CC BY 4.0: credit QUDT.org, include https://creativecommons.org/licenses/by/4.0/, indicate any modifications. RDF snapshots are preserved unmodified; no derived/editable snapshot is substituted.
- OWL-Time/PROV-O: document the copyright and exact license notice found in the downloaded work. A general W3C website statement is **not** proof that each retrieved RDF file uses a specific software license; review source terms before redistribution.
- Explicit owner acknowledgment is required before marking license review approved. Approval is recorded by executing `--approve-licenses` only after reading and accepting the above.
- The lock file contains original byte hashes and graph identity; **never normalize Turtle** after pinning. To upgrade, use an explicit new lock/snapshot version rather than overwrite in place.

## Loading policy and scope

P04-03 has only local `owl:imports`. External IRIs in data are used as *vocabulary references*; do not introduce live external `owl:imports` into production OWL or change XML catalog in T-04. P04-04 BH-V11 must verify that all referenced RDF snapshot paths resolve locally, none use GitHub repo homepage as ontology IRI, and negative import tests reject invalid inputs. QUDT dimension-aware validation should use unit, quantitykind and dimensionvector graphs together, in addition to the project-local speed/course unit policy. Full BFO/CCO, GeoSPARQL and 2026 draft SOSA/SSN imports remain out of scope.

## Exit criteria

1. All eight source artifacts download from allowlisted publisher hosts and parse as RDF.
2. Ontology IRIs, selected version metadata, required terms and final URLs recorded. If no explicit `owl:versionIRI`, report *absent*, do not invent it.
3. Byte SHA-256, sizes and triples recorded in `T04-external-rdf-lock.json`; files stored in `vendor/external-rdf/T04-2026/`.
4. Local project source profiles still equal P04-03 hashes.
5. Licensing and attribution owner review performed. `--verify` is offline and returns PASS only with approval.
6. BH-V11 remains NOT CLAIMED until formal P04-04 checks are executed.
