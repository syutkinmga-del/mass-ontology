"""P04-06 meta-acceptance: executed tests cannot be skipped or replaced by counts."""
from __future__ import annotations
import hashlib
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = spec_from_file_location('bh_p04_ci', ROOT/'scripts/run_behavior_ci.py')
ci = module_from_spec(spec)
spec.loader.exec_module(ci)


def xml_at(tmp_path, *, tests=100, failures=0, errors=0, skipped=0):
    p = tmp_path/'result.xml'
    p.write_text(f'<testsuites><testsuite name="all" tests="{tests}" '
                 f'failures="{failures}" errors="{errors}" skipped="{skipped}"/>'
                 f'</testsuites>')
    return p


def test_junit_positive_minimum_and_zero_skips(tmp_path):
    assert ci.junit_summary(xml_at(tmp_path, tests=96))['tests'] == 96


@pytest.mark.parametrize('values', [
    {'tests': 96, 'skipped': 1},
    {'tests': 96, 'failures': 1},
    {'tests': 96, 'errors': 1},
    {'tests': 89},
    {'tests': 0},
])
def test_junit_non_green_fails_closed(tmp_path, values):
    with pytest.raises(ValueError):
        ci.junit_summary(xml_at(tmp_path, **values))


def valid_bh(head):
    record = {id: {'status': 'PASS', 'issues': []} for id in ci.REQUIRED_RULES}
    record['_meta'] = {'profile': 'p04', 'tested_commit': head}
    record['legacy_executions'] = [
        {'command': id, 'status': 'PASS', 'exit_code': 0}
        for id in ('catalog', 'validate', 'cq', 'test', 'kernel')
    ]
    return record


def test_bh_v_gates_all_pass():
    assert set(ci.behavior_validation_summary(valid_bh('abc'), 'abc')) == set(ci.REQUIRED_RULES)


@pytest.mark.parametrize('bad_rule', ci.REQUIRED_RULES)
def test_bh_v_blocked_or_failed_rejected(bad_rule):
    data = valid_bh('abc')
    data[bad_rule]['status'] = 'BLOCKED'
    with pytest.raises(ValueError, match=bad_rule):
        ci.behavior_validation_summary(data, 'abc')


def test_bh_wrong_commit_or_legacy_omission_rejected():
    with pytest.raises(ValueError, match='commit'):
        ci.behavior_validation_summary(valid_bh('abc'), 'different')
    data = valid_bh('abc')
    data['legacy_executions'] = data['legacy_executions'][:-1]
    with pytest.raises(ValueError, match='legacy'):
        ci.behavior_validation_summary(data, 'abc')


def valid_cq():
    return {'profile':'p04', 'status':'PASS', 'checks': {
        id: {'status':'PASS', 'actual_rows':n, 'expected_rows':n, 'exact_bindings':True}
        for id,n in ci.EXPECTED_CQ.items()}}


def test_exact_cq_bindings_accepted():
    assert len(ci.validate_cq(valid_cq())) == 3


@pytest.mark.parametrize('mutation', ('not-exact', 'wrong-count', 'missing-cq', 'future-profile', 'blocked'))
def test_exact_cq_mutations_rejected(mutation):
    data = valid_cq()
    if mutation == 'not-exact': data['checks']['BH-CQ-02']['exact_bindings'] = False
    if mutation == 'wrong-count': data['checks']['BH-CQ-03']['actual_rows'] = 18 + 1
    if mutation == 'missing-cq': del data['checks']['BH-CQ-01']
    if mutation == 'future-profile': data['profile'] = 'p05'
    if mutation == 'blocked': data['status'] = 'BLOCKED'
    with pytest.raises(ValueError): ci.validate_cq(data)


def test_ci_controlled_config_and_robot_pin():
    wf = (ROOT/'.github/workflows/behavior-validation.yml').read_text(encoding='utf-8')
    make = (ROOT/'Makefile').read_text(encoding='utf-8')
    digest = (ROOT/'ci/robot-v1.9.11.sha256').read_text().split()[0]
    assert digest == ci.ROBOT_JAR_SHA256
    assert 'sha256sum -c' in wf
    assert 'pull_request:' in wf and 'push:' in wf
    assert 'make behavior-test' in wf
    assert 'fetch-depth: 0' in wf
    assert 'actions/upload-artifact@b7c566a772e6b6bfb58ed0dc250532a479d7789f' in wf
    assert 'behavior-test:' in make
    assert 'scripts/run_behavior_ci.py --profile p04' in make
    assert 'P04-06' not in (ROOT/'catalog-v001.xml').read_text()


def test_runner_explicitly_defers_future_profile(tmp_path):
    assert ci.main(['--repo', str(tmp_path), '--profile', 'p05', '--report-dir', 'run/behavior-ci']) == 2
    assert json.loads((tmp_path/'run/behavior-ci/report.json').read_text())['status'] == 'DEFERRED'


def test_report_path_must_stay_inside_repo(tmp_path):
    assert ci.main(['--repo', str(tmp_path), '--profile', 'p04',
                    '--report-dir', str(tmp_path.parent)]) == 2


def test_evidence_hashes_verifiable(tmp_path):
    out = tmp_path/'run'
    out.mkdir()
    result = {'status':'BLOCKED', 'profile':'p04', 'tested_commit':'abc',
              'gates': {'preflight': {'status':'BLOCKED','issues':['robot unavailable']}},
              'BH_rules':{},'BH_CQ':{}}
    ci.write_evidence(out, result)
    assert json.loads((out/'report.json').read_text())['status'] == 'BLOCKED'
    for line in (out/'SHA256SUMS').read_text().splitlines():
        digest, rel = line.split('  ', 1)
        assert hashlib.sha256((out/rel).read_bytes()).hexdigest() == digest
