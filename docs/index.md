# MASS Ontology

**MASS Ontology** is a lightweight modular ontology stack for Maritime Autonomous Surface Ships 
considered as Systems of Systems.

The current repository is an early research MVP. It demonstrates how RDF/OWL, SHACL and SPARQL can 
be used to represent and check basic MASS concepts, navigation encounter scenarios, COLREG-related 
references and verification-oriented model data.

## Current scope

The current MVP includes:

- core MASS ontology module;
- navigation encounter ontology module;
- example encounter scenario;
- SHACL validation rules;
- SPARQL query for retrieving encounter scenarios;
- local Fuseki demonstration workflow;
- Git-based source of truth.

## Repository structure

```text
mass-ontology/
├── 03-mass-core/
│   └── mass-core.ttl
├── 04-navigation/
│   └── navigation-situation.ttl
├── examples/
│   └── example-encounter-scenario.ttl
├── shapes/
│   └── mass-core.shacl.ttl
├── queries/
│   └── list-encounter-scenarios.rq
├── scripts/
│   └── run_shacl.py
├── docs/
│   └── index.md
└── Makefile
