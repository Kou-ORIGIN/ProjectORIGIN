#!/usr/bin/env python3
"""Read-only Case Bootstrap operational integrity audit."""
import argparse
import json
from case_bootstrap.audit import audit
from case_bootstrap.contextual import load_validator

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository-root',required=True)
    parser.add_argument('--contextual-validator', help='Explicit trusted local module.py:function(root, path, event) returning findings; required for applicable Events')
    args=parser.parse_args()
    try:
        validator=load_validator(args.contextual_validator,args.repository_root) if args.contextual_validator else None
        result=audit(args.repository_root,contextual_validator=validator)
    except (OSError,ValueError,ImportError,AttributeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(1 if result['overall_status']=='FAIL' else 0)
