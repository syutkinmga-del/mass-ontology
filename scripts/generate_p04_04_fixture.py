#!/usr/bin/env python3
"""Versioned migration of the P04-03 synthetic fixture to pinned QUDT 3.5.3.

The original P04-03 generator, fixture, source manifest and T-04 byte lock
remain untouched. The new BH-P04 validation profile uses this successor fixture.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
from rdflib import Namespace

ROOT = Path(__file__).resolve().parents[1]
LEGACY_GENERATOR = ROOT / 'scripts/generate_p04_03_fixture.py'
INPUT = ROOT / 'tests/observation/fixtures/p04-03-synthetic-input.json'
OUTPUT = ROOT / 'examples/p04-04-synthetic-ais-qudt353.ttl'
QUDT = Namespace('http://qudt.org/schema/qudt/')


def generate_bytes():
    spec = importlib.util.spec_from_file_location('p04_03_frozen_generator', LEGACY_GENERATOR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    g = mod.build_graph(json.loads(INPUT.read_text(encoding='utf-8')))
    old = list(g.subject_objects(QUDT.unit))
    if len(old) != 12:
        raise ValueError(f'expected 12 obsolete QUDT unit arcs, found {len(old)}')
    if list(g.triples((None, QUDT.hasUnit, None))):
        raise ValueError('source already contains qudt:hasUnit; migration needs review')
    for value, unit in old:
        g.remove((value, QUDT.unit, unit))
        g.add((value, QUDT.hasUnit, unit))
    if len(g) != 370 or list(g.triples((None, QUDT.unit, None))):
        raise ValueError('versioned migration cardinality/unit predicate mismatch')
    lines = sorted(s.strip() for s in g.serialize(format='nt').splitlines() if s.strip())
    header = ('# P04-04 REVISED SYNTHETIC AIS; QUDT v3.5.3 property migration.\n'
              '# Original P04-03 data and published SHA256 preserved as historical baseline.\n'
              '# Generated deterministically from the frozen P04-03 source JSON.\n')
    return (header+'\n'.join(lines)+'\n').encode('utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    b = generate_bytes()
    if a.check:
        if not OUTPUT.is_file() or OUTPUT.read_bytes() != b:
            raise SystemExit('P04-04 fixture reproducibility FAIL')
        print('P04-04 fixture reproducibility PASS; SHA-256:', hashlib.sha256(b).hexdigest())
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(b)
        print('P04-04 fixture generated; SHA-256:', hashlib.sha256(b).hexdigest())


if __name__ == '__main__':
    main()
