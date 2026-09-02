import json
from pathlib import Path
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]

DATA_FILES = [
    ROOT / "01-common" / "common-core.ttl",
    ROOT / "00-foundation" / "foundation-alignment.ttl",
    ROOT / "03-mass-core" / "mass-core.ttl",
    ROOT / "04-navigation" / "navigation-situation.ttl",
    ROOT / "examples" / "example-encounter-scenario.ttl",
    ROOT / "00-foundation" / "external-ontology-registry.ttl",
]

QUERY_DIR = ROOT / "queries" / "cq"
EXPECTED_RESULTS_FILE = ROOT / "tests" / "expected-cq-results.json"


def short(value):
    text = str(value)

    prefixes = [
        "https://w3id.org/mass-ontology/example#",
        "https://w3id.org/mass-ontology/navigation#",
        "https://w3id.org/mass-ontology/core#",
        "http://www.w3.org/2001/XMLSchema#",
    ]

    for prefix in prefixes:
        text = text.replace(prefix, "")

    if "#" in text:
        return text.split("#")[-1]

    if "/" in text:
        return text.rstrip("/").split("/")[-1]

    return text


def load_expected_results():
    if not EXPECTED_RESULTS_FILE.exists():
        raise SystemExit(
            f"Expected results file not found: "
            f"{EXPECTED_RESULTS_FILE.relative_to(ROOT)}"
        )

    return json.loads(EXPECTED_RESULTS_FILE.read_text(encoding="utf-8"))


def main():
    graph = Graph()

    print("Loading RDF data")
    print("================")

    for file in DATA_FILES:
        print(f"Loading: {file.relative_to(ROOT)}")
        graph.parse(file, format="turtle")

    print()
    print(f"Total triples: {len(graph)}")
    print()

    expected_results = load_expected_results()
    query_files = sorted(QUERY_DIR.glob("cq-*.rq"))

    if not query_files:
        raise SystemExit("No CQ query files found in queries/cq/")

    print("Running competency question queries")
    print("===================================")

    failed = False

    for query_file in query_files:
        query_name = query_file.name

        print()
        print(f"Query: {query_file.relative_to(ROOT)}")
        print("-" * 80)

        query = query_file.read_text(encoding="utf-8")
        rows = list(graph.query(query))
        actual_count = len(rows)

        expected_count = expected_results.get(query_name)

        if expected_count is None:
            print(f"ERROR: no expected row count defined for {query_name}")
            failed = True
            continue

        print(f"Rows: {actual_count}")
        print(f"Expected rows: {expected_count}")

        for row in rows:
            print(" | ".join(short(value) for value in row))

        if actual_count != expected_count:
            print(
                f"ERROR: {query_name} returned {actual_count} rows, "
                f"but expected {expected_count}."
            )
            failed = True

    extra_expected = set(expected_results) - {file.name for file in query_files}

    if extra_expected:
        print()
        print("ERROR: expected results are defined for missing query files:")
        for query_name in sorted(extra_expected):
            print(f"- {query_name}")
        failed = True

    if failed:
        raise SystemExit(1)

    print()
    print("All competency question queries returned expected results.")


if __name__ == "__main__":
    main()


    
