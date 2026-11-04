from qa_common import *
import uuid
state=json.loads((E/'lifecycle-state.json').read_text(encoding='utf-8'))
id=state['id'];actor=state['actor'];q=R/'queues';peerroot=B/'isolated-reader'
def prepare(name,intents,base):
 raw=q/(name+'.raw.jsonl');out=q/(name+'.v2.jsonl')
 raw.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in intents),encoding='utf-8')
 bash(name+'-prepare',['scripts/bd-apply-intents.sh','--prepare','--base',base,'--actor',actor,'--output',out,raw])
 return out
def value(k,v):
 if k in ['labels','comments','dependencies'] and isinstance(v,list):return sorted(json.dumps(x,sort_keys=True,ensure_ascii=False) for x in v)
 return v
def apply(name,queue,previous,allowed,wanted):
 receipt=json.loads(bash(name+'-apply',['scripts/bd-apply-intents.sh',queue],timeout=240).stdout);save(name+'-receipt',receipt)
 snap=git(name+'-snapshot',['show',receipt['published_sha']+':.beads/issues.jsonl']).stdout
 row=next(json.loads(x) for x in snap.splitlines() if json.loads(x).get('id')==id)
 peer=json.loads(bash(name+'-peer',['scripts/bd-read.sh','show',id,'--json'],peerroot).stdout)
 if isinstance(peer,list):peer=peer[0]
 check(name+'-peer-full-object',row==peer,dict(published=row,peer=peer))
 check(name+'-same-sha',text(git(name+'-peer-sha',['rev-parse','origin/beads-backup'],peerroot))==receipt['published_sha'],receipt['published_sha'])
 changes={k:dict(before=v,after=row.get(k)) for k,v in previous.items() if k not in allowed and (k not in row or value(k,v)!=value(k,row[k]))}
 check(name+'-untouched-full-object',not changes,changes)
 check(name+'-wanted-fields',all(value(k,row.get(k))==value(k,v) for k,v in wanted.items()),dict(wanted=wanted,actual={k:row.get(k) for k in wanted}))
 return row,receipt['published_sha']
row=state['row'];base=state['published_sha']
pending=prepare('unrelated-notes',[dict(intent_id='win-0a-unrelated-notes',op='update',ref=id,notes='Rebased notes\nСохранить актуальный title')],base)
updated_metadata={**row['metadata'],'phase':'updated'}
update=prepare('lifecycle-update',[dict(intent_id='win-0a-update',op='update',ref=id,title='Updated Windows native task',priority=1,design='Design\nДизайн',metadata=updated_metadata,add_labels=['updated'],remove_labels=['windows-qa'])],base)
row,base=apply('lifecycle-update',update,row,{'title','priority','design','metadata','labels','updated_at'},dict(title='Updated Windows native task',priority=1,metadata=updated_metadata,design='Design\nДизайн',labels=['synthetic','updated']))
row,base=apply('unrelated-notes',pending,row,{'notes','updated_at'},dict(title='Updated Windows native task',notes='Rebased notes\nСохранить актуальный title'))
close=prepare('lifecycle-close',[dict(intent_id='win-0a-close',op='close',ref=id,close_reason='Synthetic QA done — готово')],base)
row,base=apply('lifecycle-close',close,row,{'status','close_reason','closed_at','updated_at'},dict(status='closed',close_reason='Synthetic QA done — готово'))
reopen=prepare('lifecycle-reopen',[dict(intent_id='win-0a-reopen',op='update',ref=id,status='open')],base)
row,base=apply('lifecycle-reopen',reopen,row,{'status','close_reason','closed_at','updated_at'},dict(status='open'))
actor_b='agent-'+str(uuid.uuid4())
reassign=prepare('lifecycle-reassign',[dict(intent_id='win-0a-reassign',op='update',ref=id,assignee=actor_b,status='in_progress')],base)
row,base=apply('lifecycle-reassign',reassign,row,{'status','assignee','started_at','updated_at'},dict(status='in_progress',assignee=actor_b))
save('lifecycle-complete',dict(result='PASS',source=PIN,id=id,parent=state['parent'],original_actor=actor,reassigned_actor=actor_b,published_sha=base,row=row,
 cases=['native create/claim/update/close/reopen/reassign','legitimate unrelated-field stale-base rebase','per-step independent peer full-object equality and same-SHA','untouched full-field preservation']))
print(json.dumps(dict(result='PASS lifecycle and unrelated-field rebase',id=id,published_sha=base,reassigned_actor=actor_b)))
