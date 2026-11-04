from qa_common import *
import uuid,re
life=json.loads((E/'lifecycle-complete.json').read_text(encoding='utf-8'))
current=json.loads((E/'lost-receipt-result.json').read_text(encoding='utf-8'))
child=life['id'];parent=life['parent'];actor_a='agent-'+str(uuid.uuid4());actor_b='agent-'+str(uuid.uuid4());q=R/'queues'
def prepare(name,intents,base,actor):
 raw=q/(name+'.raw.jsonl');out=q/(name+'.v2.jsonl')
 raw.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in intents),encoding='utf-8')
 bash(name+'-prepare',['scripts/bd-apply-intents.sh','--prepare','--base',base,'--actor',actor,'--output',out,raw])
 return out
snapshot=git('race-before-snapshot',['show',current['published_sha']+':.beads/issues.jsonl']).stdout
row_parent=next(json.loads(x) for x in snapshot.splitlines() if json.loads(x).get('id')==parent)
check('race-valid-unclaimed-parent',row_parent['status']=='open' and not row_parent.get('assignee'),row_parent)
anchor_queue=prepare('race-anchor',[dict(intent_id='win-0a-race-anchor',op='create',handle='tmp:race-anchor',title='Isolated AC3 graph-race anchor',type='task',priority=3)],current['published_sha'],actor_a)
anchor_receipt=json.loads(bash('race-anchor-native-create',['scripts/bd-apply-intents.sh',anchor_queue],timeout=240).stdout);save('race-anchor-receipt',anchor_receipt)
anchor=next(x['result']['ref'] for x in anchor_receipt['outcomes'] if x['intent_id']=='win-0a-race-anchor');base=anchor_receipt['published_sha']
save('race-fixture-precondition',dict(reason='one isolated native graph node is necessary to avoid pre-existing typed edges/cycles; not a repetition of create qualification',anchor=anchor,parent_before=row_parent,base=base))
winner=prepare('race-winning',[
 dict(intent_id='win-0a-race-title-A',op='update',ref=child,title='AC3 winning title'),
 dict(intent_id='win-0a-race-claim-A',op='claim',ref=parent),
 dict(intent_id='win-0a-race-edge-A',op='dep_add',ref='wqa-z5e',blocked_by=anchor,dep_type='blocks')],base,actor_a)
loser=prepare('race-losing',[
 dict(intent_id='win-0a-race-title-B',op='update',ref=child,title='AC3 losing title'),
 dict(intent_id='win-0a-race-claim-B',op='claim',ref=parent)],base,actor_b)
graph=prepare('race-graph-cycle',[
 dict(intent_id='win-0a-race-edge-B',op='dep_add',ref=anchor,blocked_by='wqa-z5e',dep_type='blocks')],base,actor_b)
hashes={str(p.name):sha(p.read_bytes()) for p in [winner,loser,graph]}
first=json.loads(bash('race-winner-native-publish',['scripts/bd-apply-intents.sh',winner],timeout=240).stdout);save('race-winner-receipt',first)
check('race-winner-claim-confirmed',any(c['id']==parent and c['actor']==actor_a and c['confirmed'] for c in first['claims']),first)
blocked_graph=bash('race-graph-native-dry-run-refusal',['scripts/bd-apply-intents.sh','--dry-run',graph],expected=(2,))
check('race-graph-cycle-cause',bool(re.search(r'cycle|цикл',decode(blocked_graph.stderr),re.I)),decode(blocked_graph.stderr))
rejected=bash('race-losing-native-apply-refusal',['scripts/bd-apply-intents.sh',loser],expected=(8,),timeout=120)
conflicts=[]
for line in decode(rejected.stderr).splitlines():
 try:
  obj=json.loads(line)
  if isinstance(obj,dict) and 'conflicts' in obj:conflicts=obj['conflicts']
 except ValueError:pass
conflict_ids={x.get('intent_id') for x in conflicts}
check('race-both-title-and-claim-conflict',{'win-0a-race-title-B','win-0a-race-claim-B'}<=conflict_ids,conflicts)
remote=text(git('race-published-sha-unchanged',['ls-remote','--heads','origin','beads-backup'])).split()[0]
check('race-winning-r-and-all-queues-retained',remote==first['published_sha'] and hashes=={str(p.name):sha(p.read_bytes()) for p in [winner,loser,graph]},dict(remote=remote,winner=first['published_sha'],queue_hashes=hashes))
snap=git('race-final-snapshot',['show',remote+':.beads/issues.jsonl']).stdout
rows=[json.loads(x) for x in snap.splitlines()]
for i,row in enumerate(rows):
 peer=json.loads(bash('race-peer-object-'+str(i),['scripts/bd-read.sh','show',row['id'],'--json'],B/'isolated-reader').stdout)
 if isinstance(peer,list):peer=peer[0]
 check('race-peer-equality-'+str(i),peer==row,dict(published=row,peer=peer))
check('race-peer-same-sha',text(git('race-peer-last-sha',['rev-parse','origin/beads-backup'],B/'isolated-reader'))==remote,remote)
save('races-result',dict(result='PASS scoped',source=PIN,base=base,published_sha=remote,actor_winner=actor_a,actor_loser=actor_b,anchor_id=anchor,conflicts=conflicts,queue_hashes=hashes,
 methods={'same_field_and_claim':'two actors prepared on same frozen R; winner native publishes, loser actual native apply rejects RC8; terminal conflict/queues retained',
 'graph':'two actors prepared opposing edges on same R; winner native adds first edge; loser trusted native --dry-run rejects cycle before CLI/publication'},
 not_run=['simultaneous OS processes/CAS network race','native graph apply after terminal title/claim conflict'],
 not_run_reason='one sequential worker; current terminal conflict and losing queue preserved, no unreviewed resolution/new fixture created'))
print(json.dumps(dict(races='PASS scoped',published_sha=remote,conflicts=len(conflicts),terminal_queue_retained=True)))
