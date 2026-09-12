#!/usr/bin/env python3
"""Run the existing 168 workflow tests and Case Bootstrap tests in isolation.

The adopted workflow is live production input for WorkflowValidatorTests.
AdoptionContractTests exercise PROPOSED -> ADOPTED in disposable Git repos;
this runner explicitly supplies their PROPOSED starting fixture. It does not
change test assertions, validator behavior, production workflow, or the exact
historical test bytes bound by WFADOPTDEC-0001 / WFADOPT-0001.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]


def workflow_suite():
    path=ROOT/'tests/workflows/test_validate_workflow.py'
    spec=importlib.util.spec_from_file_location('test_validate_workflow',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    original=module.AdoptionContractTests.setUp
    def with_proposed_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate=json.loads(module.DEFINITION.read_text())
            candidate['status']='PROPOSED'
            path=Path(directory)/'synthetic-proposed-fixture.json'
            path.write_text(json.dumps(candidate,ensure_ascii=False,indent=2)+'\n')
            with patch.object(module,'DEFINITION',path):
                original(self)
    module.AdoptionContractTests.setUp=with_proposed_fixture
    return unittest.defaultTestLoader.loadTestsFromModule(module)


class Result(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.groups={}
    def startTest(self,test):
        key=test.__class__.__name__
        self.groups[key]=self.groups.get(key,0)+1
        super().startTest(test)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite',choices=['all','workflows','operations'],default='all')
    args=parser.parse_args()
    suite=unittest.TestSuite()
    if args.suite in ('all','workflows'):suite.addTests(workflow_suite())
    if args.suite in ('all','operations'):
        suite.addTests(unittest.defaultTestLoader.discover(str(ROOT/'tests/operations')))
    result=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
    report={'total':result.testsRun,'pass':result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped)-len(result.expectedFailures)-len(result.unexpectedSuccesses),
            'fail':len(result.failures),'error':len(result.errors),'skip':len(result.skipped),'expected_failure':len(result.expectedFailures),'unexpected_success':len(result.unexpectedSuccesses),
            'groups':result.groups,'exit_code':0 if result.wasSuccessful() and not result.skipped and not result.expectedFailures else 1,
            'workflow_fixture_policy':'Only the disposable AdoptionContractTests starting candidate is PROPOSED; live WorkflowValidatorTests use the repository definition.'}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(report['exit_code'])
