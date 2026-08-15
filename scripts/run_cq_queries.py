from pathlib import Path
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]

DATA_FILES = [
    ROOT / "03-mass-core" / "mass-core.ttl",
    ROOT / "04-navigation" / "navigation-situation.ttl",
    ROOT / "examples" / "example-encounter-scenario.ttl",
]

QUERY_DIR = ROOT / "queries" / "cq"


def short(value):
    text = str(value)
    if "#" in text:
        return text.split("#")[-1]
    if "/" in text:
        return text.rstrip("/").split("/")[-1]
    return text


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

    query_files = sorted(QUERY_DIR.glob("*.rq"))

    if not query_files:
        raise SystemExit("No CQ query files found in queries/cq/")

    print("Running competency question queries")
    print("===================================")

    for query_file in query_files:
        print()
        print(f"Query: {query_file.relative_to(ROOT)}")
        print("-" * 80)

        query = query_file.read_text(encoding="utf-8")
        rows = list(graph.query(query))

        print(f"Rows: {len(rows)}")

        if not rows:
            print("No results.")
            continue

        for row in rows:
            print(" | ".join(short(value) for value in row))


if __name__ == "__main__":
    main()
