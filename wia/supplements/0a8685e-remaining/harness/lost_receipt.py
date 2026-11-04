from qa_common import *
import shlex
state=json.loads((E/'routes-result.json').read_text(encoding='utf-8'))
id=state['id'];actor=state['actor'];base=state['published_sha']
raw=R/'queues/lost-receipt.raw.jsonl';prepared=R/'queues/lost-receipt.v2.jsonl'
raw.write_text(json.dumps(dict(intent_id='win-0a-lost-receipt',op='update',ref=id,notes='AC4 lost transport receipt — one outcome only'),ensure_ascii=False)+'\n',encoding='utf-8')
bash('lost-receipt-prepare',['scripts/bd-apply-intents.sh','--prepare','--base',base,'--actor',actor,'--output',prepared,raw])
queue_hash=sha(prepared.read_bytes())
trace=R/'lost-receive-pack.trace';gittrace=R/'lost-git-trace2.jsonl';wrapper=R/'lost-receive-pack.sh'
script='#!/bin/sh\ngit receive-pack "$@"\nqa_rc=$?\nif [ "$qa_rc" -eq 0 ]; then\n  printf "receive-pack succeeded; forced transport exit73\\n" >> '+shlex.quote(trace.as_posix())+'\n  git --git-dir="$1" rev-parse refs/heads/beads-backup >> '+shlex.quote(trace.as_posix())+'\n  exit 73\nfi\nexit "$qa_rc"\n'
wrapper.write_text(script,encoding='utf-8',newline='\n')
git('lost-receipt-configure-local-fault',['config','--local','remote.origin.receivepack','sh '+wrapper.as_posix()])
try:
 first=json.loads(bash('lost-receipt-native-apply',['scripts/bd-apply-intents.sh',prepared],timeout=240,env=dict(ENV,GIT_TRACE2_EVENT=gittrace.as_posix())).stdout)
 save('lost-receipt-first-confirmed',first)
finally:
 git('lost-receipt-remove-local-fault',['config','--local','--unset','remote.origin.receivepack'])
check('lost-receipt-real-server-accepted-then-failed',trace.exists() and b'forced transport exit73' in trace.read_bytes(),decode(trace.read_bytes()) if trace.exists() else 'missing trace')
events=[json.loads(x) for x in gittrace.read_text(encoding='utf-8').splitlines()]
failed_children=[e for e in events if e.get('event')=='child_exit' and e.get('code')==73]
check('lost-receipt-actual-child-exit73',bool(failed_children),failed_children)
published=first['published_sha']
check('lost-receipt-first-one-mutation',first['status']=='published' and first['mutations']==1,first)
ledger_before=git('lost-receipt-ledger-before-retry',['show',published+':.beads/overgate-outcomes-v1.json']).stdout
retry=json.loads(bash('lost-receipt-same-queue-retry',['scripts/bd-apply-intents.sh',prepared],timeout=120).stdout)
save('lost-receipt-retry-receipt',retry)
remote=text(git('lost-receipt-remote-after-retry',['ls-remote','--heads','origin','beads-backup'])).split()[0]
ledger_after=git('lost-receipt-ledger-after-retry',['show',remote+':.beads/overgate-outcomes-v1.json']).stdout
check('lost-receipt-idempotent',retry['mutations']==0 and retry['published_sha']==published==remote and retry['outcomes']==first['outcomes'] and ledger_before==ledger_after and sha(prepared.read_bytes())==queue_hash,dict(first=first,retry=retry,queue_sha256=queue_hash,ledger_sha256=sha(ledger_after)))
peer=json.loads(bash('lost-receipt-peer-read',['scripts/bd-read.sh','show',id,'--json'],B/'isolated-reader').stdout)
if isinstance(peer,list):peer=peer[0]
check('lost-receipt-peer-notes',peer['notes']=='AC4 lost transport receipt — one outcome only',peer)
save('lost-receipt-result',dict(result='PASS',source=PIN,id=id,published_sha=published,queue_sha256=queue_hash,first_mutations=1,retry_mutations=0,
 method='Actual local receive-pack accepted branch; fixture transport wrapper then exited73; Git trace confirms child exit; publisher readback confirmed outcome; identical queue retry preserved R/ledger/outcomes',row=peer))
print(json.dumps(dict(lost_receipt='PASS',published_sha=published,retry_mutations=retry['mutations'])))
