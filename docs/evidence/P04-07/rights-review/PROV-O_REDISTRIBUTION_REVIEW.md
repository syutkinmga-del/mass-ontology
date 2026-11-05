# P04-07 / RR-05 — PROV-O artifact redistribution review (not a license approval)

**Status:** PARTIALLY DOCUMENTED; FINAL OWNER REVIEW REQUIRED.

## Evidence

- Pinned source artifact: `vendor/external-rdf/T04-2026/prov-o.ttl`, controlled by `docs/standards/T04-external-rdf-lock.json` (SHA-256 `7d203989f67b38bca572253942acc5a1bf24ce3ccfece16f072dcb4be2b79a96`).
- Publisher URI: <https://www.w3.org/ns/prov-o.ttl>.
- Ontology namespace: `http://www.w3.org/ns/prov#`; published W3C Recommendation: <https://www.w3.org/TR/prov-o/> (2013-04-30).
- W3C namespace publication identifies direct Turtle/RDF/XML ontology representations: <https://www.w3.org/ns/prov/generatedAtTime>.
- W3C's public policy allows republishing **unmodified W3C documents with attribution**, subject to applicable copyright conditions: <https://www.w3.org/copyright/intellectual-rights/> and <https://www.w3.org/copyright/document-license-2015/>.
- W3C distinguishes software/doc licenses: <https://www.w3.org/copyright/software-license-2015/>.

## Restriction on conclusion

The archived `prov-o.ttl` ontology header lacks an explicit `dcterms:license`/`owl:versionIRI` licensing assertion. W3C's policy supporting unmodified public documents is strong contextual evidence of permitted redistribution with proper attribution, but **does not by itself identify which license is directly granted to this exact archived RDF representation**. The signed author's decision does not supersede W3C rights.

## Before combined R08 approval

1. Confirm the applicability of W3C document/software conditions to *this exact archived RDF file* against its official source (or obtain a specific permission notice from W3C), documenting the basis.
2. Preserve any required full copyright, disclaimer and short/full notices for W3C/OGC as required by their license(s); source links alone may be insufficient.
3. Review the existing `THIRD_PARTY_NOTICES.md` language and its SHA-256. **Changing that file requires an updated SHA-256 and renewed rights-holder sign-off** because the signed decision names the previous exact bytes.
4. Only after the above review may the combined `DEC-P04-07-rights-approval.json` assert `prov_o_exact_artifact_rights_confirmed=true` with supporting evidence.

This review does not modify the T-04 lock or publisher RDF bytes.
