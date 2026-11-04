from pathlib import Path
import sys,importlib.util,json,copy,hashlib
sys.dont_write_bytecode=True
S=Path(sys.argv[1]);PIN=sys.argv[2];E=Path(sys.argv[3])
spec=importlib.util.spec_from_file_location('candidate_installer',S/'scripts/install-overgate.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
manifest,payload=m.load_manifest(S,PIN,True)
negative=copy.deepcopy(manifest);omitted='scripts/lib/bd-managed-git.mjs'
negative['files']=[e for e in negative['files'] if e['target']!=omitted]
assert len(negative['files'])==len(manifest['files'])-1
try:m.validate_payload(negative,payload,True)
except m.InstallError as error:
 result=dict(source=PIN,method='actual candidate validate_payload against in-memory manifest omission; unchanged frozen Git source; no CLI synthetic source SHA',omitted=omitted,error=str(error),refused=True)
 assert 'payload preflight failed' in str(error) and omitted in str(error),str(error)
 (E/'closure-negative-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
else:raise AssertionError('missing managed import was accepted')
