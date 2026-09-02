# MASS Ontology

**MASS Ontology** is a lightweight modular ontology stack for Maritime Autonomous Surface Ships 
considered as Systems of Systems.

The current repository is an early research MVP. It demonstrates how RDF/OWL, SHACL and SPARQL can 
be used to represent and check basic MASS concepts, navigation encounter scenarios, COLREG-related 
references and verification-oriented model data.

## Development line: v0.3.0-dev

After the `v0.2.0` competency questions release, the project entered the `v0.3.0-dev` development line.

The purpose of this development line is to introduce foundation alignment.

The current draft foundation layer includes:

```text
00-foundation/foundation-alignment.ttl
01-common/common-core.ttl

Добавь раздел:

```markdown

## Foundation alignment competency questions

The foundation alignment layer is checked by CQ-09 ... CQ-12.

These competency questions answer:

- which local ontology entities have foundation alignment decisions;
- which foundation target is proposed for `mass:MASSVessel`;
- which alignment decisions currently have draft status;
- which navigation classes already have foundation alignment decisions.

The corresponding SPARQL queries are stored in:

```text
queries/cq/

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

## MVP v0.2.0

The current MVP demonstrates a minimal ontology engineering pipeline for MASS-oriented MBSE and 
digital engineering workflows.

The pipeline includes:

```text
MASS Core ontology
→ Navigation ontology
→ example encounter scenario
→ SHACL validation
→ competency questions
→ SPARQL queries
→ automated expected-result checks
→ GitHub Actions

Добавь раздел:

```markdown
## Competency Questions

The MVP uses competency questions to define what the ontology should be able to answer.

The current competency questions cover:

- operational modes of a MASS vessel;
- communication links of a MASS vessel;
- own ship and target ship in an encounter;
- CPA and TCPA values;
- applicable COLREG rule;
- required maneuver;
- safety requirement verification evidence;
- retrieval of represented encounter scenarios.

The CQ definitions are stored in:

```text
competency-questions/mass-cq-v0.1.md

## Local validation

Run structural validation:

```bash
make validate
