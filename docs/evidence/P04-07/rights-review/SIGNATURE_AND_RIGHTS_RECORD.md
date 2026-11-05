# P04-07 — Registration of signed author rights/license decision

**Record status:** SIGNED AUTHOR DECISION REGISTERED LOCALLY; PUBLIC GIT COMMIT PENDING.

- Document: P04-07-RIGHTS-2026-01, dated 2026-11-05.
- Author and asserted rights holder: Сюткин Андрей Вениаминович.
- Scope: only original author-owned MASS Ontology OWL/RDF, scripts, SHACL, SPARQL, tests, examples and documentation.
- License selected: `Apache-2.0` (root `LICENSE`); recorded exact bytes SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
- Signed scan SHA-256: `fdc68b4e393b03535be896c4d3ebd0357d9aba64ca1aa03d48283d7f0e68e19e` (2 pages). The image displays a handwritten signature; its authenticity has not been independently authenticated.
- The signed PDF **is not included in this public Git commit** to avoid publishing a handwritten signature. The rights holder must retain the original paper and signed scan privately.
- Third-party notice source: `THIRD_PARTY_NOTICES.md`; exact SHA-256 `c908a4adedc9a1fbe70f9df27dfcbdf361d82a2795658f7c08089da62d384d6f`.
- `vendor/external-rdf/T04-2026/` publisher snapshots are **excluded** from the authored-material Apache-2.0 license.
- The signed document explicitly does **not** authorize release `v0.4.0`.

## Distinct gates

- RR-04: author's *choice of project license* and signed decision are evidenced after the root `LICENSE` is installed and the registration commit is published. This is not independent validation of all contributors' rights.
- RR-05: **PENDING** full review of third-party rights, particularly the exact `prov-o.ttl` file and upstream notices; signed decision states that notices are confirmed *after separate review*.
- R08: **BLOCKED**. The required **combined** `docs/governance/DEC-P04-07-rights-approval.json` must not claim `APPROVED` until third-party review is actually completed and documented.
- R10: **BLOCKED**. Release owner approval must be separate.

## Hash integrity

From repository root:

```sh
shasum -a 256 -c docs/evidence/P04-07/rights-review/approved-license.sha256
python3 scripts/verify_p04_author_license_decision.py
```

This records the exact signed source's SHA-256 but does not record or certify its legally effective signature; the rights holder maintains original evidence outside public Git.
