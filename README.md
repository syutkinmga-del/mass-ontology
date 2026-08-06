# MASS Ontology Stack

Modular ontology stack for Maritime Autonomous Surface Ships (MASS) as System of Systems.

## Purpose

This repository is the source of truth for a research ontology stack supporting:

- MASS architecture modeling
- semantic interoperability
- MBSE / Digital Thread integration
- COLREGs-aware navigation scenarios
- ROC / VTS interaction modeling
- safety, risk, V&V and assurance traceability

## Structure

```text
00-foundation/          Upper and mid-level ontology imports
01-common/              QUDT, PROV-O, GeoSPARQL, SOSA/SSN imports
02-maritime/            IMO / vessel / port / voyage alignment
03-mass-core/           MASS core concepts
04-navigation/          COLREGs, encounter situations, CPA/TCPA
05-safety-assurance/    hazards, STPA, risk controls, V&V evidence
06-project/             example project datasets
shapes/                 SHACL validation rules
competency-questions/   ontology requirements as questions
queries/                SPARQL queries
examples/               example RDF datasets
scripts/                validation and documentation scripts
tests/                  automated tests
docs/                   documentation

```

## Validation

```bash
source .venv/bin/activate
make validate
pytest
```

## Working rule

Git is the source of truth. Protégé is an ontology editor. VS Code is used for TTL, SHACL, SPARQL and code. pySHACL validates constraints. Fuseki demonstrates SPARQL queries.
