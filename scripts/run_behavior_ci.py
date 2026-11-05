#!/usr/bin/env python3
"""P04-06: fail-closed, local/CI identical gate for BH-P04 only.

The process exit code is authoritative; PASS in a prior evidence file never
substitutes for a freshly executed test. All reports remain under run/.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_RULES = ('BH-V01', 'BH-V02', 'BH-V03', 'BH-V05', 'BH-V06', 'BH-V11', 'BH-V12')
EXPECTED_CQ = {'BH-CQ-01': 18, 'BH-CQ-02': 9, 'BH-CQ-03': 18}
SOURCE_COMMIT = '6113ed1581a59602be67227ce3ad3730b4e6563d'
ROBOT_VERSION = '1.9.11'
ROBOT_JAR_SHA256 = '53cd275c8e4c0dad1fc2c1c34174876795cd7d6b6926e1444adcbb0cb3c7ab26'
DEPENDENCIES = {'rdflib': '7.6.0', 'pyshacl': '0.40.1', 'pytest': '9.1.1'}


def checksum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def command(args: list[str], *, timeout: int = 30, cwd: Path = ROOT) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, errors='replace', timeout=timeout, check=False)


def preflight(repo: Path) -> list[str]:
    issues = []
    if sys.version_info < (3, 12) or sys.version_info >= (3, 13):
        issues.append('Python 3.12.x required for P04-06')
    for name, expected in DEPENDENCIES.items():
        try:
            observed = version(name)
        except PackageNotFoundError:
            issues.append(f'{name} missing; expected {expected}')
        else:
            if observed != expected:
                issues.append(f'{name} version {observed}; expected {expected}')
    for rel in (
        'scripts/run_behavior_validation.py', 'scripts/run_behavior_cq.py',
        'scripts/t04_pin_external_rdf.py', 'scripts/verify_sysml_kernel_integrity.py',
        'scripts/generate_p04_03_fixture.py', 'scripts/generate_p04_04_fixture.py',
        'tests/test_p04_04_validation.py', 'tests/test_p04_05_behavior_cq.py',
        'docs/standards/T04-external-rdf-lock.json',
        'docs/standards/P04-05-bh-cq-manifest.json',
        'vendor/external-rdf/T04-2026/qudt-unit-3.5.3.ttl',
        'baselines/sysml/MASS-SK-1.0/MASSKernel_v1.0.sysml',
    ):
        if not (repo / rel).is_file():
            issues.append(f'prerequisite missing: {rel}')
    if not (repo / '.venv/bin/python').is_file():
        issues.append('repository Python .venv/bin/python missing')
    if not shutil.which('make'):
        issues.append('make executable missing')
    if not shutil.which('robot'):
        issues.append('ROBOT/HermiT executable missing (BH-V05 would be skipped)')
    else:
        try:
            robot = command(['robot', '--version'], cwd=repo)
            if robot.returncode != 0 or f'ROBOT version {ROBOT_VERSION}' not in robot.stdout:
                issues.append(f'ROBOT version must be {ROBOT_VERSION}: {robot.stdout[:160]}')
        except (OSError, subprocess.TimeoutExpired) as e:
            issues.append(f'ROBOT cannot execute: {e}')
    if not shutil.which('java'):
        issues.append('Java missing')
    else:
        try:
            java = command(['java', '-version'], cwd=repo)
            if java.returncode != 0 or not re.search(r'\bversion "21\.', java.stdout):
                issues.append(f'Java 21 expected: {java.stdout[:180]}')
        except (OSError, subprocess.TimeoutExpired) as e:
            issues.append(f'Java cannot execute: {e}')
    # If a JAR path is explicitly supplied (e.g. GitHub Actions), verify its bytes.
    import os
    jar_path = os.environ.get('ROBOT_JAR')
    if jar_path:
        jar = Path(jar_path)
        if not jar.is_file() or checksum(jar) != ROBOT_JAR_SHA256:
            issues.append('ROBOT_JAR SHA-256 differs from pinned GitHub release')
    if not (repo / '.git').exists():
        issues.append('git metadata missing')
    else:
        try:
            head = command(['git', 'rev-parse', 'HEAD'], cwd=repo)
            ancestry = command(['git', 'merge-base', '--is-ancestor', SOURCE_COMMIT, 'HEAD'], cwd=repo)
            if head.returncode or ancestry.returncode:
                issues.append('P04-05 evidence commit is not a verified ancestor of HEAD (fetch-depth 0 required)')
        except (OSError, subprocess.TimeoutExpired) as e:
            issues.append(f'git unavailable: {e}')
    return issues


def junit_summary(xml_file: Path) -> dict:
    """Reject pytest's success exit code if tests were skipped or not collected."""
    root = ET.parse(xml_file).getroot()
    suites = [root] if root.tag == 'testsuite' else list(root.findall('testsuite'))
    if not suites:
        raise ValueError('pytest JUnit XML has no testsuites')
    out = {key: sum(int(s.get(key, '0')) for s in suites)
           for key in ('tests', 'errors', 'failures', 'skipped')}
    if out['tests'] < 90:
        raise ValueError(f'Expected at least 90 P04 historical tests, collected {out["tests"]}')
    if out['errors'] or out['failures'] or out['skipped']:
        raise ValueError(f'pytest not fully green: {out}')
    return out


def behavior_validation_summary(report: dict, head: str) -> dict:
    """Do not trust process code alone: validate exact required rule set."""
    for rule in REQUIRED_RULES:
        if report.get(rule, {}).get('status') != 'PASS':
            raise ValueError(f'{rule} not PASS: {report.get(rule)}')
    meta = report.get('_meta', {})
    if meta.get('profile') != 'p04' or meta.get('tested_commit') != head:
        raise ValueError('BH validation profile/commit does not match current checkout')
    executions = report.get('legacy_executions', [])
    expected = {'catalog', 'validate', 'cq', 'test', 'kernel'}
    seen = {x.get('command') for x in executions if x.get('status') == 'PASS' and x.get('exit_code') == 0}
    if not expected.issubset(seen):
        raise ValueError(f'BH-V12 legacy executions missing: {sorted(expected-seen)}')
    return {rule: 'PASS' for rule in REQUIRED_RULES}


def cq_summary(report: dict) -> dict:
    if report.get('profile') != 'p04' or report.get('status') != 'PASS':
        raise ValueError('BH-CQ status/profile not PASS/p04')
    if set(report.get('checks', {})) != set(EXPECTED_CQ):
        raise ValueError('BH-CQ-01..03 expected exactly')
    return {cid: {'rows': rows, 'exact_bindings': True} for cid, rows in EXPECTED_CQ.items()
            if (report['checks'][cid].get('status') == 'PASS'
                and report['checks'][cid].get('actual_rows') == rows
                and report['checks'][cid].get('expected_rows') == rows
                and report['checks'][cid].get('exact_bindings') is True)}


def validate_cq(report: dict) -> dict:
    checks = cq_summary(report)
    if len(checks) != len(EXPECTED_CQ):
        raise ValueError('At least one BH-CQ exact binding or row count failed')
    return checks


def run(repo: Path, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    logs = out / 'logs'
    logs.mkdir(exist_ok=True)
    commit = command(['git', 'rev-parse', 'HEAD'], cwd=repo)
    head = commit.stdout.strip() if commit.returncode == 0 else None
    report = {'profile': 'p04', 'status': 'BLOCKED', 'tested_commit': head,
              'executed_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
              'policy': 'fail-closed; all required gates PASS; zero skipped pytest cases',
              'gates': {}, 'BH_rules': {}, 'BH_CQ': {}, 'environment': {
                  'python': sys.version.split()[0], 'pinned_python_packages': DEPENDENCIES,
                  'robot_required': ROBOT_VERSION, 'robot_jar_sha256': ROBOT_JAR_SHA256,
              }}
    issues = preflight(repo)
    report['gates']['preflight'] = {'status': 'BLOCKED' if issues else 'PASS', 'issues': issues}
    if issues:
        for issue in issues:
            print('PREFLIGHT BLOCKED:', issue, flush=True)
        return report

    py = str(repo / '.venv/bin/python')
    commands = [
        ('fixture-p04-03', [py, 'scripts/generate_p04_03_fixture.py', '--check'], 90),
        ('fixture-p04-04', [py, 'scripts/generate_p04_04_fixture.py', '--check'], 90),
        ('catalog', ['make', 'catalog'], 90),
        ('shacl-legacy', ['make', 'validate'], 120),
        ('cq-legacy', ['make', 'cq'], 120),
        ('sysml-kernel', [py, 'scripts/verify_sysml_kernel_integrity.py'], 90),
        ('t04-verify', [py, 'scripts/t04_pin_external_rdf.py', '--repo', str(repo), '--verify'], 180),
        ('pytest', [py, '-m', 'pytest', '-q', '-ra', '--junitxml='+str(out/'pytest.xml'), 'tests'], 300),
        ('behavior-validation', [py, 'scripts/run_behavior_validation.py', '--profile', 'p04', '--legacy',
                                 '--report', str(out/'behavior-validation.json')], 450),
        ('behavior-cq', [py, 'scripts/run_behavior_cq.py', '--profile', 'p04',
                         '--report', str(out/'behavior-cq.json')], 180),
    ]
    for index, (name, argv, timeout) in enumerate(commands, start=1):
        path = logs / f'{index:02d}-{name}.log'
        print(f'GATE {index:02d} {name} RUN', flush=True)
        result = {'status': 'BLOCKED', 'exit_code': None, 'log': str(path.relative_to(out))}
        try:
            proc = command(argv, timeout=timeout, cwd=repo)
            path.write_text(proc.stdout, encoding='utf-8')
            result['exit_code'] = proc.returncode
            if proc.returncode == 0:
                result['status'] = 'PASS'
            else:
                result['status'] = 'FAIL'
                result['reason'] = 'command returned nonzero'
        except subprocess.TimeoutExpired as e:
            path.write_text(str(e), encoding='utf-8')
            result['reason'] = 'command timeout; no PASS claim'
        except OSError as e:
            path.write_text(str(e), encoding='utf-8')
            result['reason'] = f'command unavailable: {e}'
        if result['status'] == 'PASS':
            try:
                if name == 'pytest':
                    result['junit'] = junit_summary(out/'pytest.xml')
                elif name == 'behavior-validation':
                    report['BH_rules'] = behavior_validation_summary(
                        json.loads((out/'behavior-validation.json').read_text()), head)
                elif name == 'behavior-cq':
                    report['BH_CQ'] = validate_cq(json.loads((out/'behavior-cq.json').read_text()))
                elif name == 't04-verify':
                    lock = json.loads((repo/'docs/standards/T04-external-rdf-lock.json').read_text())
                    if lock.get('license_review', {}).get('status') != 'APPROVED_BY_PROJECT_OWNER':
                        raise ValueError('T-04 license owner approval missing')
                elif name == 'sysml-kernel':
                    if 'MASS-SK-1.0 SOURCE INTEGRITY: PASS' not in proc.stdout:
                        raise ValueError('MASS-SK-1.0 integrity confirmation missing')
            except (OSError, ValueError, ET.ParseError, json.JSONDecodeError, KeyError, TypeError) as e:
                result['status'] = 'FAIL'
                result['reason'] = f'semantic oracle: {e}'
        report['gates'][name] = result
        print(f'GATE {index:02d} {name} {result["status"]}' +
              (f': {result["reason"]}' if 'reason' in result else ''), flush=True)
    required = {'preflight', *(name for name, _args, _timeout in commands)}
    if (set(report['gates']) == required and
        all(report['gates'][key]['status'] == 'PASS' for key in required) and
        set(report['BH_rules']) == set(REQUIRED_RULES) and
        set(report['BH_CQ']) == set(EXPECTED_CQ)):
        report['status'] = 'PASS'
    else:
        report['status'] = 'FAIL'
    return report


def write_evidence(out: Path, result: dict) -> None:
    (out / 'report.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    lines = [
        '# P04-06 BH-P04 CI verification', '',
        f'**Status:** {result["status"]}',
        f'**Commit:** `{result.get("tested_commit")}`',
        f'**UTC:** {result.get("executed_utc")}', '',
        '| Gate | Outcome |', '|---|---|',
    ]
    for key, record in result.get('gates', {}).items():
        lines.append(f'| {key} | {record["status"]} |')
    lines.extend(['', 'Required BH rules: ' + ', '.join(result.get('BH_rules', {})),
                  'Required BH queries: ' + ', '.join(result.get('BH_CQ', {})),
                  '', 'P05/P09: DEFERRED (not executed).',
                  'No SysML parser execution or release certification is claimed.', ''])
    (out/'summary.md').write_text('\n'.join(lines), encoding='utf-8')
    files = sorted(p for p in out.rglob('*') if p.is_file() and p.name != 'SHA256SUMS')
    records = [f'{checksum(p)}  {p.relative_to(out).as_posix()}' for p in files]
    (out/'SHA256SUMS').write_text('\n'.join(records)+'\n', encoding='utf-8')


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--profile', required=True, choices=('p04', 'p05', 'p09'))
    ap.add_argument('--report-dir', type=Path, default=Path('run/behavior-ci'))
    ap.add_argument('--repo', type=Path, default=ROOT)
    a = ap.parse_args(argv)
    repo = a.repo.resolve()
    out = (repo / a.report_dir).resolve() if not a.report_dir.is_absolute() else a.report_dir.resolve()
    if not out.is_relative_to(repo) or out == repo:
        print('CI report-dir must be a subdirectory of repository', file=sys.stderr)
        return 2
    if a.profile != 'p04':
        report = {'profile': a.profile, 'status': 'DEFERRED',
                  'reason': 'P05/P09 outside BH-P04 CI profile', 'gates': {}}
        out.mkdir(parents=True, exist_ok=True)
        write_evidence(out, report)
        print(f'{a.profile.upper()} DEFERRED; exit 2')
        return 2
    try:
        report = run(repo, out)
    except Exception as e:
        report = {'profile': 'p04', 'status': 'BLOCKED',
                  'reason': f'{type(e).__name__}: {e}', 'gates': {}}
    write_evidence(out, report)
    print('P04-06 BEHAVIOR-CI:', report['status'], flush=True)
    print('Report:', out/'report.json', flush=True)
    return 0 if report['status'] == 'PASS' else 2


if __name__ == '__main__':
    sys.exit(main())
