"""Read-only canonical reference checks and explicit contextual capability wiring.

A caller-supplied validator is trusted executable code, not Human authority.
The CLI accepts an explicitly selected local Python module and function.
"""
import importlib.util
from pathlib import Path
from . import storage as s


def references(value):
    if isinstance(value,dict):
        if 'ref_id' in value and 'artifact_type' in value:
            yield value
        for key in sorted(value):
            yield from references(value[key])
    elif isinstance(value,list):
        for item in value:
            yield from references(item)


def check_reference(ops,reference):
    ops.contracts.validate_definition('artifactReference',reference)
    path=reference.get('repository_path'); digest=reference.get('sha256')
    if not path or not digest or not reference.get('artifact_id'):
        s.reject('CANONICAL_REFERENCE_EVIDENCE_INSUFFICIENT')
    raw=s.read_bytes(ops.root,path)
    if s.sha256(raw)!=digest:
        s.reject('REFERENCE_FIXITY_MISMATCH',path)
    target=s.parse_json(raw)
    # Use explicit logical identity fields; a coincidental text occurrence is not identity.
    identities=[v for k,v in target.items() if k in ('artifact_id','record_id','event_id','case_id','asset_id','audit_id','research_id','master_id','transaction_id','recovery_determination_id')]
    if reference['artifact_id'] not in identities:
        s.reject('REFERENCE_IDENTITY_MISMATCH',path)
    if 'artifact_type' in target and target['artifact_type']!=reference['artifact_type']:
        s.reject('REFERENCE_IDENTITY_MISMATCH',path)
    if 'artifact_version' in reference and target.get('artifact_version',target.get('version'))!=reference['artifact_version']:
        s.reject('REFERENCE_IDENTITY_MISMATCH',path)
    return target


def check_manifest(ops,path,value,required_events=()):
    case=path.split('/')[1]
    if value.get('case_id')!=case or not isinstance(value.get('artifact_references'),list):
        s.reject('MANIFEST_STRUCTURE_INVALID')
    for reference in value['artifact_references']:
        check_reference(ops,reference)
    refs=list(references(value))
    for reference in refs:
        check_reference(ops,reference)
    for event in required_events:
        matches=[r for r in refs if r.get('artifact_id')==event['event_id']]
        if not matches:
            s.reject('MANIFEST_REQUIRED_EVENT_MISSING')
        for reference in matches:
            target=check_reference(ops,reference)
            if target.get('event_type')!=event['event_type'] or target.get('record_ref')!=event['record_ref']:
                s.reject('MANIFEST_EVENT_BINDING_MISMATCH')


def check_event(ops,path,event):
    ops.contracts.validate_event(event,s.read_bytes(ops.root,path))
    case=path.split('/')[1]
    s.validate_id(event['event_id'],'EVT',case)
    if path!='cases/'+case+'/semantic-events/'+event['event_id']+'.json':
        s.reject('SEMANTIC_EVENT_IDENTITY_MISMATCH')
    for reference in references(event):
        check_reference(ops,reference)
    if ops.contextual_validator is None:
        s.reject('CONTEXTUAL_EVENT_VALIDATION_UNAVAILABLE')
    try:
        findings=ops.contextual_validator(path,event)
    except Exception as exc:
        s.reject('CONTEXTUAL_EVENT_VALIDATOR_FAILURE',type(exc).__name__)
    if not isinstance(findings,list):
        s.reject('CONTEXTUAL_EVENT_VALIDATOR_RESULT_INVALID')
    for finding in findings:
        if finding.get('severity','ERROR')=='ERROR' or finding.get('blocking',False):
            s.reject(finding.get('code','CONTEXTUAL_EVENT_INVALID'))
    return findings


def integrity(ops,path,kind,required_events=()):
    result={'target_path':path,'status':'VALID','sha256':None,'findings':[]}
    try:
        raw=s.read_bytes(ops.root,path);result['sha256']=s.sha256(raw)
        value=s.parse_json(raw)
        if kind=='MANIFEST':
            check_manifest(ops,path,value,required_events)
        else:
            check_event(ops,path,value)
            for required in required_events:
                if required['event_id']==value['event_id'] and any(required[k]!=value[k] for k in ('event_type','record_ref')):
                    s.reject('SEMANTIC_EVENT_BINDING_MISMATCH')
    except OSError as exc:
        result.update(status='UNAVAILABLE',findings=[type(exc).__name__])
    except (s.OperationalError,ValueError,KeyError,TypeError) as exc:
        code=getattr(exc,'code',type(exc).__name__)
        result.update(status='UNAVAILABLE' if code=='CONTEXTUAL_EVENT_VALIDATION_UNAVAILABLE' else 'INVALID',findings=[code])
    return result


def load_validator(selection,root):
    """Load explicitly selected trusted module.py:function(root, path, event)."""
    path,separator,name=selection.rpartition(':')
    if not separator or not Path(path).is_file():
        raise ValueError('Expected existing local module.py:function')
    spec=importlib.util.spec_from_file_location('projectorigin_contextual_validator',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    function=getattr(module,name)
    if not callable(function):
        raise ValueError('Contextual validator must be callable')
    return lambda path,event:function(Path(root).resolve(),path,event)
