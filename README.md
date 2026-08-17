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

## Current status: MVP v0.2.0

The current version of the MASS Ontology repository is an early but testable ontology engineering 
MVP.

It includes:

- MASS Core ontology draft;
- Navigation ontology draft;
- example encounter scenario;
- SHACL validation rules;
- competency questions;
- SPARQL queries for competency questions;
- automated CQ query runner;
- GitHub Actions validation pipeline.

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

## Validation workflow

The repository supports two local validation commands.

Run SHACL validation:

```bash
make validatpytest
```

## Working rule

Git is the source of truth. Protégé is an ontology editor. VS Code is used for TTL, SHACL, SPARQL and code. pySHACL validates constraints. Fuseki demonstrates SPARQL queries.

## Competency questions

The first competency questions are stored in:

```text

competency-questions/mass-cq-v0.1.md

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
