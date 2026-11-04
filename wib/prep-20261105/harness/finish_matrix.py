from pathlib import Path
import json
code=(Path(__file__).parent/'prepare.py').read_text(encoding='utf-8')
exec(code.split('assert sha(BD.read_bytes())',1)[0])
legacy=B/'legacy-pending';peer=B/'legacy-old-writer-peer'
out=E/'legacy-peer-before.jsonl'
run('legacy-peer-frozen-export',[BD,'--sandbox','export','--all','--output',out],peer)
def canonical_rows(raw):
 rows=[json.loads(x) for x in raw.splitlines() if x.strip()]
 for row in rows:
  if row.get('_type')=='issue':row.pop('_type')
  for key in ['labels','comments','dependencies']:
   if isinstance(row.get(key),list):row[key]=sorted(row[key],key=lambda v:json.dumps(v,sort_keys=True,ensure_ascii=False))
 return sorted(rows,key=lambda r:r['id'])
same=canonical_rows((E/'legacy-before.jsonl').read_bytes())==canonical_rows(out.read_bytes())
save('legacy-peer-baseline-equivalence',dict(result='PASS' if same else 'FAIL',method='full native export objects, unordered labels/comments/dependency representation only; metadata array order retained'))
assert same,'Native legacy peer fixture differs'
save('legacy-metadata',json.loads((legacy/'.beads/metadata.json').read_bytes()))
cfg=json.loads(run('legacy-authoritative-prefix',[BD,'--readonly','config','list','--json'],legacy))
assert cfg['issue_prefix']=='wib-qa'
git('fresh-origin-refs',['ls-remote','--heads',ORIGIN])
git('fresh-no-main-or-backup',['ls-remote','--heads',ORIGIN,'main','beads-backup'])
manifest=json.loads((E/'prep-ready.json').read_text(encoding='utf-8'))
manifest['legacy_peer_full_object_equal']=same
manifest['legacy_authoritative_prefix']=cfg['issue_prefix']
manifest['test_matrix']='test-matrix.md'
manifest['pending_owner_is_external_to_raw_queue']=True
save('prep-ready',manifest)
actor='agent-'+str(uuid.uuid4())
save('activation-task-input',dict(title='WI-B Windows disposable activation acceptance',actor=actor,project_prefix='wib-qa',status='NOT SUBMITTED; no candidate runtime pin'))
save('plan-contract-binding',dict(plan_source=manifest['plan_source'],plan_blob=manifest['plan_blob'],plan_sha256=sha((B/'plan-source.md').read_bytes()),contract_sha256=sha((B/'pr-contract.txt').read_bytes()),runtime_pin=None))
print(json.dumps(dict(prep='READY',legacy_peer_full_object_equal=same,authoritative_prefix=cfg['issue_prefix'],candidate='NOT RUN')))
