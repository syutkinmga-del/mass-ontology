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

## Current development status: v0.3.0-dev

The current development line extends the MASS Ontology MVP beyond the `v0.2.0` competency questions 
release.

The main focus of `v0.3.0-dev` is foundation alignment.

This means that the project now includes an explicit draft layer for connecting MASS ontology modules 
with upper and common ontologies such as BFO and CCO.

Current `v0.3.0-dev` additions include:

- `01-common/common-core.ttl` — lightweight MASS common vocabulary;
- `00-foundation/foundation-alignment.ttl` — draft alignment decisions;
- foundation alignment links from MASS Core to the common layer;
- foundation alignment links from Navigation to the common layer;
- CQ-09 ... CQ-12 for checking foundation alignment decisions;
- expected result checks for the new foundation alignment competency questions.

The project still does not claim to be fully aligned with BFO or CCO. The current layer records draft 
alignment decisions and prepares the ontology for controlled future imports.

The project is not yet a complete MASS ontology stack. It is a working research sandbox for 
developing and validating a modular ontology architecture for Maritime Autonomous Surface Ships.

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
## Architecture direction

The intended ontology stack is:

```text
BFO / CCO
→ MASS Common
→ MASS Core
→ Navigation
→ Sensor observations
→ Quantities and units
→ Geospatial representation
→ COLREGs extension
→ Safety / V&V evidence

## Validation workflow

The repository supports two local validation commands.

Run SHACL validation:

```bash
make validatpytest
```

## Working rule

Git is the source of truth. Protégé is an ontology editor. VS Code is used for TTL, SHACL, SPARQL and code. pySHACL validates constraints. Fuseki demonstrates SPARQL queries.

## Competency Questions

The ontology is checked through competency questions and SPARQL queries.

Current competency question groups:

```text
CQ-01 ... CQ-08
→ MASS Core and navigation encounter scenario

CQ-09 ... CQ-12
→ foundation alignment decisions

## Releases

### v0.2.0 — Competency Questions MVP

This release adds competency questions, SPARQL CQ queries, the automated CQ runner, expected CQ 
result checks, and CI execution of CQ queries.

### v0.1.0 — Initial MASS Ontology MVP

This release established the initial MASS Core draft, Navigation draft, example encounter 
scenario, SHACL validation, basic SPARQL query and GitHub Actions SHACL validation.

See:

```text
CHANGELOG.md
