from pathlib import Path
import xml.etree.ElementTree as ET
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
CATALOG_FILE = ROOT / "catalog-v001.xml"

CATALOG_NS = {"cat": "urn:oasis:names:tc:entity:xmlns:xml:catalog"}

EXPECTED_ENTRIES = {
    "https://w3id.org/mass-ontology/common",
    "https://w3id.org/mass-ontology/foundation-alignment",
    "https://w3id.org/mass-ontology/core",
    "https://w3id.org/mass-ontology/navigation",
}


def main():
    if not CATALOG_FILE.exists():
        raise SystemExit(f"Catalog file not found: {CATALOG_FILE}")

    tree = ET.parse(CATALOG_FILE)
    root = tree.getroot()

    uri_entries = root.findall("cat:uri", CATALOG_NS)

    if not uri_entries:
        raise SystemExit("No URI entries found in catalog-v001.xml")

    mapping = {}

    print("Checking catalog-v001.xml")
    print("=========================")

    for entry in uri_entries:
        name = entry.attrib.get("name")
        uri = entry.attrib.get("uri")

        if not name or not uri:
            raise SystemExit("Catalog entry must have both name and uri attributes.")

        if name in mapping:
            raise SystemExit(f"Duplicate catalog entry for ontology IRI: {name}")

        mapping[name] = uri

    missing_entries = EXPECTED_ENTRIES - set(mapping)

    if missing_entries:
        print("Missing expected catalog entries:")
        for item in sorted(missing_entries):
            print(f"- {item}")
        raise SystemExit(1)

    for ontology_iri, relative_path in sorted(mapping.items()):
        file_path = ROOT / relative_path

        print(f"{ontology_iri}")
        print(f"  -> {relative_path}")

        if not file_path.exists():
            raise SystemExit(f"Mapped file does not exist: {relative_path}")

        graph = Graph()
        graph.parse(file_path, format="turtle")

        print(f"  OK, triples: {len(graph)}")

    print()
    print("Catalog OK: all mapped ontology files exist and parse as Turtle.")


if __name__ == "__main__":
    main()
