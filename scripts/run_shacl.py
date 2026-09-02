from pathlib import Path
from rdflib import Graph
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]

data_files = [
    ROOT / "01-common" / "common-core.ttl",
    ROOT / "00-foundation" / "foundation-alignment.ttl",
    ROOT / "03-mass-core" / "mass-core.ttl",
    ROOT / "04-navigation" / "navigation-situation.ttl",
    ROOT / "examples" / "example-encounter-scenario.ttl",
    ROOT / "00-foundation" / "external-ontology-registry.ttl",
]

shape_files = [
    ROOT / "shapes" / "mass-core.shacl.ttl",
    ROOT / "shapes" / "foundation-alignment.shacl.ttl",
]

data_graph = Graph()
for file in data_files:
    print(f"Loading data: {file.relative_to(ROOT)}")
    data_graph.parse(file, format="turtle")

shapes_graph = Graph()
for file in shape_files:
    print(f"Loading shapes: {file.relative_to(ROOT)}")
    shapes_graph.parse(file, format="turtle")

conforms, report_graph, report_text = validate(
    data_graph=data_graph,
    shacl_graph=shapes_graph,
    inference="rdfs",
    abort_on_first=False,
    allow_infos=True,
    allow_warnings=True,
)

print("\nSHACL validation report")
print("=======================")
print(report_text)

if not conforms:
    raise SystemExit(1)

print("Validation OK: data conforms to SHACL shapes.")
