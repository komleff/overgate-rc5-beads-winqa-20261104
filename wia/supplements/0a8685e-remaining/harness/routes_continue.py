from qa_common import *
import uuid
state=json.loads((E/'lifecycle-complete.json').read_text(encoding='utf-8'));id=state['id']
raw=LINKED/'.bd-intents/windows-qa-linked.raw.jsonl'
raw.parent.mkdir(exist_ok=True)
save('linked-queue-directory-prep-note',dict(kind='QA fixture directory preparation',reason='data directory absent in linked checkout; created before queue handoff; no product case rerun',previous_reads_and_refusals='PASS'))
payload=dict(intent_id='win-0a-linked-notes',op='update',ref=id,notes='Linked agent queue\nПередано как данные в trusted publisher')
raw.write_text(json.dumps(payload,ensure_ascii=False)+'\n',encoding='utf-8')
actor='agent-'+str(uuid.uuid4());out=R/'queues/linked.v2.jsonl'
bash('linked-data-prepare-by-publisher',['scripts/bd-apply-intents.sh','--prepare','--base',state['published_sha'],'--actor',actor,'--output',out,raw])
receipt=json.loads(bash('linked-data-native-apply',['scripts/bd-apply-intents.sh',out],timeout=240).stdout)
save('linked-publication-receipt',receipt)
snapshot=git('linked-published-snapshot',['show',receipt['published_sha']+':.beads/issues.jsonl']).stdout
row=next(json.loads(x) for x in snapshot.splitlines() if json.loads(x).get('id')==id)
peer=json.loads(bash('linked-data-isolated-peer',['scripts/bd-read.sh','show',id,'--json'],B/'isolated-reader').stdout)
if isinstance(peer,list):peer=peer[0]
check('linked-data-peer-full-object',peer==row,dict(published=row,peer=peer))
check('linked-data-note-published',row['notes']==payload['notes'] and row['title']==state['row']['title'] and row['assignee']==state['reassigned_actor'],row)
check('linked-data-peer-sha',text(git('linked-data-peer-sha-read',['rev-parse','origin/beads-backup'],B/'isolated-reader'))==receipt['published_sha'],receipt['published_sha'])
save('routes-result',dict(result='PASS',source=PIN,id=id,actor=actor,published_sha=receipt['published_sha'],raw_queue_path=str(raw),raw_queue_sha256=sha(raw.read_bytes()),
 methods=['linked and isolated managed read','both direct mutation refusals before primary DB change','raw typed queue from linked to registered trusted publisher','native publish and isolated same-SHA full-object peer'],row=row))
print(json.dumps(dict(routes='PASS',id=id,published_sha=receipt['published_sha'])))
