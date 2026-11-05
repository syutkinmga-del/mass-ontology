# MASS Ontology — third-party RDF notices (T-04 / BH-P04)

**Status:** RR-05 SOURCE/NOTICE REVIEW PREPARED; **OWNER SIGN-OFF PENDING**.  
**Review baseline:** `ebd0d54756bd32876ab1aad031170e4278f83580` (P04-07 signed author-license registration).  
**Distribution policy:** the project-authored material is licensed separately under Apache-2.0; the eight upstream RDF snapshots below are **excluded** from that author-granted license. Each continues under the applicable provider terms.

The following RDF snapshots are vendored **unchanged** under `vendor/external-rdf/T04-2026/` and validated by exact SHA-256 in `docs/standards/T04-external-rdf-lock.json`. The URLs in this notice identify the publishers and original works; they are not permissions to replace the frozen copies with live downloads. Publisher attribution does not imply endorsement.

## Complete upstream inventory

| Pinned RDF artifact | Original publisher / copyright | Exact identified licensing basis | Original source |
|---|---|---|---|
| `sosa-2017.ttl` | W3C/OGC Spatial Data on the Web Working Group; copyright 2017 W3C/OGC | W3C Software and Document License (2015) **and** OGC Software License 1.0, as cited by two in-file `dcterms:license` triples | https://www.w3.org/ns/sosa/2017 |
| `ssn-2017.ttl` | W3C/OGC Spatial Data on the Web Working Group; copyright 2017 W3C/OGC | W3C Software and Document License (2015) **and** OGC Software License 1.0, as cited by two in-file `dcterms:license` triples | https://www.w3.org/ns/ssn/2017 |
| `qudt-schema-3.5.3.ttl` | QUDT.org | Creative Commons Attribution 4.0 International (CC BY 4.0) | https://qudt.org/3.5.3/schema/qudt |
| `qudt-unit-3.5.3.ttl` | QUDT.org | CC BY 4.0 | https://qudt.org/3.5.3/vocab/unit |
| `qudt-quantitykind-3.5.3.ttl` | QUDT.org | CC BY 4.0 | https://qudt.org/3.5.3/vocab/quantitykind |
| `qudt-dimensionvector-3.5.3.ttl` | QUDT.org | CC BY 4.0 | https://qudt.org/3.5.3/vocab/dimensionvector |
| `owl-time.ttl` | W3C / OGC; copyright 2006–2017 W3C/OGC | **CC BY 4.0, explicitly stated in the pinned RDF as `dct:license`**. Earlier T-04 narrative referred generally to W3C conditions; the pinned graph's specific licensing assertion takes precedence for this review | https://www.w3.org/2006/time |
| `prov-o.ttl` | W3C Provenance Working Group; W3C PROV-O Recommendation (2013-04-30) | **W3C Software and Document License (2015), publisher-policy based**: official PROV-O Recommendation links its OWL encoding; W3C's software policy permits redistribution of its software, and in 2015 W3C expressly extended the new license to software previously under its old license. **The pinned RDF itself has no explicit license triple**; this attribution is a *documented project licensing assessment*, not an asserted RDF fact or proof that the live publisher file has identical bytes | https://www.w3.org/ns/prov-o.ttl |

**All eight publisher artifacts are unmodified.** Neither MASS's authored ontology nor its tests or synthetic AIS examples are represented as an upstream publisher work. No changes to the publisher RDF were made as part of P04-07.

## Redistribution obligations and complete notice texts

- **W3C Software and Document License (2015):** full notice and disclaimers copied as a separate accompanying document `docs/licenses/third-party/W3C-20150513-LICENSE.txt`; preserve original copyright and disclaimer text, identify the original work and disclose modifications, if any. Official license: https://www.w3.org/copyright/software-license-2015/ . W3C's 2015 announcement explicitly extends this license to previously W3C-software-licensed works: https://www.w3.org/news/2015/w3c-adopts-new-software-and-document-license/ .
- **OGC Software License 1.0 (SOSA/SSN):** full notice/disclaimers copied as `docs/licenses/third-party/OGC-1.0-LICENSE.txt`; retain original W3C/OGC notices and note modifications (there are none). Official text: https://www.ogc.org/about/policies/software-licenses/ogc-software-license-1-0/ . The ontology's `http://www.opengeospatial.org/ogc/Software` link denotes the upstream software license, not an invitation to infer the currently listed Apache 2.0 alternative.
- **CC BY 4.0 (QUDT and pinned OWL-Time):** credit the identified creators, link the precise original works and the license `https://creativecommons.org/licenses/by/4.0/`, and indicate no modifications. Official QUDT license: https://github.com/qudt/qudt-public-repo/blob/main/LICENSE.md ; QUDT project site https://qudt.org/ .

The W3C namespace/Recommendation references and copyright provenance for the W3C-PROV-O license assessment are recorded in `docs/evidence/P04-07/rights-review/RR05-PROV-O-EVIDENCE.md`.

## Frozen snapshot control: original bytes

Each upstream file listed below must retain the SHA-256 established by T-04:

| Pinned RDF artifact | SHA-256 |
|---|---|
| `sosa-2017.ttl` | `c70b0d1c843c0047e4c98e0a89392e46a05752ff6365bda7f7f55303905a0392` |
| `ssn-2017.ttl` | `184d86189191146e314cc52b1bceb96fca11e70aacbc160d71588102a5153eb9` |
| `qudt-schema-3.5.3.ttl` | `807b5b03a8759670a6412822c7624cc6180c5e80ff7b9b3b8e4bee98e1c1c882` |
| `qudt-unit-3.5.3.ttl` | `89df26d7f8ebb54a80d6bd4e03f3268b16a7acdc7b90490346273c03817971d4` |
| `qudt-quantitykind-3.5.3.ttl` | `730052a9a760f0f70ac389e8d7e493a729bc8ea2e5f226af68a4b279e7232d81` |
| `qudt-dimensionvector-3.5.3.ttl` | `eaa321908ce06afa5176c5cbdf375aef4e3176390f18db663a628a96aa9678a3` |
| `owl-time.ttl` | `251bd6970b0d7a5efa97ff681afe81a297df85deab3d860fa4f8eeba72d8f16c` |
| `prov-o.ttl` | `7d203989f67b38bca572253942acc5a1bf24ce3ccfece16f072dcb4be2b79a96` |

**No change permitted to pinned snapshots:** modifying a publisher RDF requires a separately versioned T-04 lock and re-execution of all BH-P04 gates.

## Governance and sign-off boundary

The signed author decision `P04-07-RIGHTS-2026-01` binds the **previous** `THIRD_PARTY_NOTICES.md` SHA-256 (`c908a4adedc9a1fbe70f9df27dfcbdf361d82a2795658f7c08089da62d384d6f`). This revised notice has **different bytes** and therefore requires a **new and explicitly dated author/owner approval**. No current evidence authorizes silently carrying the old signed notice hash to this revision.

The repository's `DEC-P04-07-rights-approval.json` must not be created with `APPROVED` or the `owl_time_cc_by_4_reconciled` / `prov_o_exact_artifact_rights_confirmed` flags set to `true` until the owner has reviewed the accompanying PROV-O evidence, confirmed the complete license notices and signed a new hash-bound approval. The local package provides an approval draft but **does not** issue that approval. This notice alone does **not** authorize release `v0.4.0`; R10 remains separate.
