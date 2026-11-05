# RR-05 — PROV-O publisher licensing and original-byte traceability review

**Status:** PUBLISHER LICENSE BASIS DOCUMENTED / OWNER APPROVAL PENDING.  
**Scope:** frozen `vendor/external-rdf/T04-2026/prov-o.ttl` (SHA-256 `7d203989f67b38bca572253942acc5a1bf24ce3ccfece16f072dcb4be2b79a96`).  
**Date:** 2026-11-05.  
**Project baseline:** `ebd0d54756bd32876ab1aad031170e4278f83580`.

## Source-derived evidence

1. The frozen T-04 lock identifies a publisher original at https://www.w3.org/ns/prov-o.ttl and the ontology namespace `http://www.w3.org/ns/prov#`. The in-repository RDF has an `owl:Ontology` statement but **does not contain an explicit `dcterms:license` or equivalent license assertion for the ontology**. Its checksum is a byte identity for the frozen repository copy; it is **not** a proof that the publisher's currently served bytes are identical.
2. W3C Recommendation *PROV-O: The PROV Ontology*, dated **30 April 2013**, links the OWL encoding directly from the normative text: https://www.w3.org/TR/prov-o/ . See the official namespace page https://www.w3.org/ns/prov/ for W3C presentation and RDF serialization of the PROV namespace.
3. Official W3C Software and Document License (2015), https://www.w3.org/copyright/software-license-2015/, grants redistribution with the complete notice, preserved pre-existing notices/disclaimers and modification notices where appropriate. W3C expressly said in its 2015 announcement https://www.w3.org/news/2015/w3c-adopts-new-software-and-document-license/ that previous W3C-software-licensed works were also made available under the new license.
4. W3C's Intellectual Rights FAQ https://www.w3.org/copyright/intellectual-rights/ states that W3C software can be redistributed with source and license attribution, full notice and modification status. These publisher sources support a **reasoned reuse basis** for the official W3C-published PROV-O OWL/RDF encoding; they are not an extra ontology triple or a separate private legal opinion.
5. The packaged `docs/licenses/third-party/W3C-20150513-LICENSE.txt` supplies the full accompanying W3C software/document notice. `THIRD_PARTY_NOTICES.md` identifies PROV-O separately, the original source and unchanged status.

## Explicit inference and residual limits

**Licensing assessment:** unmodified re-distribution of the official publisher PROV-O RDF under the general W3C Software and Document reuse conditions is a defensible reading of the above publisher policies. However, the frozen RDF does **not** itself declare that license, and the live W3C-provided bytes were not independently shown identical to the archived SHA-256 in this review. This is a documented editorial/legal inference using authoritative publisher policy, not an unqualified direct per-file license assertion.

**Owner choice:** after reviewing that evidence, the rights holder may either (a) accept the attribution and W3C license conditions for the eight unchanged files, record an explicitly dated written approval for this updated notice, and only then mark `prov_o_exact_artifact_rights_confirmed=true`; or (b) hold RR-05 pending legal/publisher clarification or an alternative distribution policy. No automatic approval is implied.

## Preservation requirements

- Do not change the frozen T-04 `prov-o.ttl` bytes, the `T04-external-rdf-lock.json` or prior P04 evidence.
- Do not equate a generic W3C website copyright notice to an embedded RDF assertion.
- Do not mislabel the eight publisher snapshots as Apache-2.0 project works.
- Record the exact SHA-256 of **revised** `THIRD_PARTY_NOTICES.md` in the new owner decision; the old signed decision carries a different, prior SHA-256.
- Keep a signed copy of the newly approved owner notice decision outside the public repository and publish only its digest and machine-readable approval metadata.
