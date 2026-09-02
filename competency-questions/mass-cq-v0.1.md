# MASS Ontology Competency Questions v0.1

This document defines the first competency questions for the MASS Ontology MVP.

Competency questions describe what the ontology should be able to answer through RDF/OWL, SHACL 
and SPARQL.

## CQ-01 — MASS vessel operational mode

**Question:**  
Which operational modes are assigned to a MASS vessel?

**Expected answer pattern:**  
MASS vessel → operational mode

**Current ontology support:**  
Supported by `mass:MASSVessel` and `mass:hasOperationalMode`.

**Example data:**  
`ex:own_ship_001 mass:hasOperationalMode ex:autonomous_mode`.

---

## CQ-02 — MASS vessel communication link

**Question:**  
Which communication links are assigned to a MASS vessel?

**Expected answer pattern:**  
MASS vessel → communication link
---

## CQ-09 — Foundation alignment decisions

**Question:**  
Which local ontology entities have foundation alignment decisions?

**Expected answer pattern:**  
Alignment decision → local entity → proposed foundation target → status

**Current ontology support:**  
Supported by `foundation:AlignmentDecision`, `foundation:alignsLocalEntity`, 
`foundation:proposedFoundationTarget` and `foundation:alignmentStatus`.

**SPARQL query:**  
`queries/cq/cq-09-foundation-alignment-decisions.rq`.

---

## CQ-10 — MASS vessel foundation target

**Question:**  
Which foundation target is proposed for `mass:MASSVessel`?

**Expected answer pattern:**  
Alignment decision → proposed foundation target → status

**Current ontology support:**  
Supported by the foundation alignment module.

**SPARQL query:**  
`queries/cq/cq-10-mass-vessel-foundation-target.rq`.

---

## CQ-11 — Draft alignment decisions

**Question:**  
Which alignment decisions currently have draft status?

**Expected answer pattern:**  
Alignment decision → local entity → proposed foundation target

**Current ontology support:**  
Supported by `foundation:alignmentStatus`.

**SPARQL query:**  
`queries/cq/cq-11-draft-alignment-decisions.rq`.

---

## CQ-12 — Navigation alignment decisions

**Question:**  
Which navigation ontology classes already have foundation alignment decisions?

**Expected answer pattern:**  
Alignment decision → navigation class → proposed foundation target → status

**Current ontology support:**  
Supported by foundation alignment decisions for selected `nav:` classes.

**SPARQL query:**  
`queries/cq/cq-12-navigation-alignment-decisions.rq`.
**Current ontology support:**  
Supported by `mass:MASSVessel` and `mass:hasCommunicationLink`.

**Example data:**  
`ex:own_ship_001 mass:hasCommunicationLink ex:link_001`.

---

## CQ-03 — Encounter situation participants

**Question:**  
Which own ship and target ship participate in an encounter situation?

**Expected answer pattern:**  
Encounter situation → own ship → target ship

**Current ontology support:**  
Supported by `nav:EncounterSituation`, `nav:hasOwnShip` and `nav:hasTargetShip`.

**Example data:**  
`ex:encounter_001 nav:hasOwnShip ex:own_ship_001`.  
`ex:encounter_001 nav:hasTargetShip ex:target_ship_001`.

---

## CQ-04 — Encounter CPA and TCPA

**Question:**  
What are the CPA and TCPA values for a given encounter situation?

**Expected answer pattern:**  
Encounter situation → CPA → TCPA

**Current ontology support:**  
Supported by `nav:hasCPA` and `nav:hasTCPA`.

**Example data:**  
`ex:encounter_001 nav:hasCPA 0.4`.  
`ex:encounter_001 nav:hasTCPA 12.0`.

---

## CQ-05 — COLREG rule for encounter

**Question:**  
Which COLREG rule applies to a given encounter situation?

**Expected answer pattern:**  
Encounter situation → COLREG rule

**Current ontology support:**  
Supported by `nav:appliesCOLREGRule`.

**Example data:**  
`ex:encounter_001 nav:appliesCOLREGRule ex:colreg_rule_15`.

---

## CQ-06 — Required maneuver

**Question:**  
Which maneuver is required in a given encounter situation?

**Expected answer pattern:**  
Encounter situation → maneuver

**Current ontology support:**  
Supported by `nav:requiresManeuver`.

**Example data:**  
`ex:encounter_001 nav:requiresManeuver ex:alter_course_to_starboard`.

---

## CQ-07 — Safety requirement verification evidence

**Question:**  
Which verification evidence supports a safety requirement?

**Expected answer pattern:**  
Safety requirement → verification evidence

**Current ontology support:**  
Partially supported by `mass:SafetyRequirement`, `mass:VerificationEvidence` and 
`mass:hasVerificationEvidence`.

**Current limitation:**  
The MVP ontology defines the classes and property, but the example dataset does not yet include 
concrete safety requirements or verification evidence.

---

## CQ-08 — Encounter scenario retrieval

**Question:**  
Which encounter scenarios are currently represented in the graph, including encounter type, 
participants, CPA, TCPA, COLREG rule and required maneuver?

**Expected answer pattern:**  
Encounter situation → type → own ship → target ship → CPA → TCPA → COLREG rule → maneuver

**Current ontology support:**  
Supported by the current navigation module and example scenario.

**SPARQL query:**  
`queries/list-encounter-scenarios.rq`.
