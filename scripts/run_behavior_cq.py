#!/usr/bin/env python3
"""P04-05: exact, offline, bag-aware BH-CQ-01..03 SPARQL bindings oracle.

A passing row count is NEVER sufficient. The checked-in oracle asserts every
IRI, literal lexical form, RDF datatype, and unbound (omitted) field.
Does not run or change legacy MASS CQ-01..14.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

from rdflib import Graph
from rdflib.term import URIRef, Literal, BNode

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'docs/standards/P04-05-bh-cq-manifest.json'
BASELINE_FIXTURE = 'examples/p04-04-synthetic-ais-qudt353.ttl'
CQ_IDS = ('BH-CQ-01', 'BH-CQ-02', 'BH-CQ-03')


class CQValidationError(Exception):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def controlled_file(repo: Path, relative: str, digest: str) -> Path:
    # Only files under repo, never URLs, symlinks or parent traversal.
    if (not isinstance(relative, str) or not relative or
        '\\' in relative or '://' in relative or
        Path(relative).is_absolute() or '..' in Path(relative).parts):
        raise CQValidationError(f'unsafe relative path: {relative!r}')
    path = repo / relative
    if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(repo.resolve()):
        raise CQValidationError(f'missing/invalid controlled file: {relative}')
    actual = sha256(path)
    if actual != digest:
        raise CQValidationError(f'SHA-256 mismatch: {relative}: expected {digest}, actual {actual}')
    return path


def term_binding(term):
    """SPARQL Results JSON-like binding, preserving lexical form and datatype."""
    if isinstance(term, URIRef):
        return {'type': 'uri', 'value': str(term)}
    if isinstance(term, Literal):
        out = {'type': 'literal', 'value': str(term)}
        if term.language is not None:
            out['xml:lang'] = term.language
        elif term.datatype is not None:
            out['datatype'] = str(term.datatype)
        return out
    if isinstance(term, BNode):
        raise CQValidationError('blank-node bindings are nondeterministic in P04-05 profile')
    raise CQValidationError(f'unrecognized SPARQL term: {term!r}')


def result_for(graph: Graph, query: str) -> dict:
    result = graph.query(query)
    if result.type != 'SELECT':
        raise CQValidationError('only SELECT queries are accepted')
    variables = [str(x) for x in result.vars]
    if len(variables) != len(set(variables)):
        raise CQValidationError('duplicate SELECT variable')
    rows = []
    for row in result:
        record = {}
        for var, value in zip(variables, row):
            if value is not None:  # Unbound is omitted, not a fabricated null/0.
                record[var] = term_binding(value)
        rows.append(record)
    return {'variables': variables, 'rows': rows}


def row_key(row: dict) -> str:
    return json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def compare_exact(actual: dict, expected: dict) -> dict:
    """Bag equality: detects missing, surplus and duplicated rows; ignores row order."""
    if actual['variables'] != expected['variables']:
        return {'status': 'FAIL', 'reason': 'VARIABLES_MISMATCH',
                'expected_variables': expected['variables'], 'actual_variables': actual['variables']}
    a = Counter(row_key(x) for x in actual['rows'])
    e = Counter(row_key(x) for x in expected['rows'])
    missing = list((e - a).elements())
    extra = list((a - e).elements())
    if missing or extra:
        return {'status': 'FAIL', 'reason': 'EXACT_BINDINGS_MISMATCH',
                'actual_rows': len(actual['rows']), 'expected_rows': len(expected['rows']),
                'missing_count': len(missing), 'unexpected_count': len(extra),
                'missing_examples': [json.loads(x) for x in missing[:2]],
                'unexpected_examples': [json.loads(x) for x in extra[:2]]}
    return {'status': 'PASS', 'actual_rows': len(actual['rows']),
            'expected_rows': len(expected['rows']), 'exact_bindings': True}


def validate_manifest(repo: Path) -> tuple[dict, dict]:
    manifest_path = repo / MANIFEST
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise CQValidationError(f'missing manifest: {MANIFEST}')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('schema_version') != 'P04-05-BH-CQ-lock-v1' or manifest.get('profile') != 'p04':
        raise CQValidationError('manifest profile/schema mismatch')
    if manifest.get('baseline_commit') != 'f70a120e78b99808b8d1340b08e652ff33313dab':
        raise CQValidationError('unreviewed P04-04 baseline')
    fixture = manifest.get('fixture', {})
    if fixture.get('path') != BASELINE_FIXTURE:
        raise CQValidationError('unexpected fixture path')
    controlled_file(repo, fixture['path'], fixture['sha256'])
    if tuple(manifest.get('cqs', {}).keys()) != CQ_IDS:
        raise CQValidationError('expected exactly BH-CQ-01..03 in order')
    expected = {}
    for cq_id in CQ_IDS:
        spec = manifest['cqs'][cq_id]
        qexpected = f'queries/behavior/{cq_id.lower()}.rq'
        gexpected = f'tests/behavior/expected/{cq_id.lower()}.json'
        if spec.get('query_path') != qexpected or spec.get('expected_path') != gexpected:
            raise CQValidationError(f'{cq_id}: query/oracle location mismatch')
        controlled_file(repo, spec['query_path'], spec['query_sha256'])
        golden = controlled_file(repo, spec['expected_path'], spec['expected_sha256'])
        exp = json.loads(golden.read_text(encoding='utf-8'))
        if exp.get('schema_version') != 'BH-CQ-exact-bindings-v1' or exp.get('cq_id') != cq_id:
            raise CQValidationError(f'{cq_id}: oracle identity incorrect')
        if not exp.get('rows') or not exp.get('variables'):
            raise CQValidationError(f'{cq_id}: empty oracle is disallowed')
        if exp.get('expected_row_count') != len(exp['rows']):
            raise CQValidationError(f'{cq_id}: oracle row count inconsistent')
        if len(set(map(row_key, exp['rows']))) != len(exp['rows']):
            raise CQValidationError(f'{cq_id}: oracle has unexpected duplicate rows')
        if spec['rows'] != len(exp['rows']):
            raise CQValidationError(f'{cq_id}: manifest row count mismatch')
        for row in exp['rows']:
            if not set(row).issubset(exp['variables']):
                raise CQValidationError(f'{cq_id}: oracle uses undeclared variables')
        expected[cq_id] = exp
    return manifest, expected


def run_suite(repo: Path, *, graph: Graph | None = None,
              query_overrides: dict | None = None) -> dict:
    manifest, golden = validate_manifest(repo)
    if graph is None:
        graph = Graph()
        graph.parse(repo / BASELINE_FIXTURE, format='turtle')
    if not graph:
        raise CQValidationError('empty RDF graph')
    q_overrides = query_overrides or {}
    if set(q_overrides) - set(CQ_IDS):
        raise CQValidationError('unknown query override ID')
    checks = {}
    for cq_id in CQ_IDS:
        spec = manifest['cqs'][cq_id]
        query = q_overrides.get(cq_id)
        if query is None:
            query = (repo / spec['query_path']).read_text(encoding='utf-8')
        try:
            actual = result_for(graph, query)
            checks[cq_id] = compare_exact(actual, golden[cq_id])
        except Exception as exc:
            checks[cq_id] = {'status': 'FAIL', 'reason': 'QUERY_EXECUTION_ERROR',
                             'detail': f'{type(exc).__name__}: {exc}'}
    ok = all(checks[cid]['status'] == 'PASS' for cid in CQ_IDS)
    return {
        'profile': 'p04',
        'baseline_commit': manifest['baseline_commit'],
        'fixture_sha256': manifest['fixture']['sha256'],
        'manifest_sha256': sha256(repo / MANIFEST),
        'rdf_triples': len(graph),
        'status': 'PASS' if ok else 'FAIL',
        'checks': checks,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, default=ROOT)
    p.add_argument('--profile', choices=('p04', 'p05', 'p09'), required=True)
    p.add_argument('--report', type=Path, default=None)
    args = p.parse_args(argv)
    if args.profile != 'p04':
        print(f'{args.profile.upper()} DEFERRED: only BH-P04 queries are implemented')
        return 2
    repo = args.repo.resolve()
    try:
        report = run_suite(repo)
        code = 0 if report['status'] == 'PASS' else 1
    except Exception as exc:
        code = 2
        report = {'profile': 'p04', 'status': 'BLOCKED', 'reason':
                  f'{type(exc).__name__}: {exc}'}
    report['executed_utc'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
    for cq_id, result in report.get('checks', {}).items():
        print(f'{cq_id} {result["status"]}  rows={result.get("actual_rows", "?")}')
        if result['status'] != 'PASS':
            print(' ', result.get('reason', ''), result.get('missing_examples', []),
                  result.get('unexpected_examples', []))
    print('P04-05 EXACT BINDINGS:', report['status'])
    if args.report is not None:
        dest = (repo / args.report) if not args.report.is_absolute() else args.report
        if not dest.resolve().is_relative_to(repo):
            print('Report must be stored inside repository', file=sys.stderr)
            return 2
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print('Report:', dest)
    return code


if __name__ == '__main__':
    raise SystemExit(main())
