from qa_common import *
import re
setup=json.loads((E/'setup-result.json').read_text(encoding='utf-8'))
result_file=R/'forged-stale.json'
run('ac4-build-stale-candidate',['node',B/'forge-stale.mjs',result_file,setup['actor']])
forged=json.loads(result_file.read_text(encoding='utf-8'))
initial_hash=sha(result_file.read_bytes())
rejected=git('ac4-real-pre-push-refusal',['push','origin',forged['candidate']+':refs/heads/beads-backup'],expected=(1,))
check('ac4-guard-exact-cause',bool(re.search(r'precondition|conflict|applicable',decode(rejected.stderr),re.I)),decode(rejected.stderr))
isolated=B/'isolated-reader'
git('ac4-peer-fetch-data-only',['fetch',PUBLISHER,'refs/heads/qa/forged-stale:refs/qa/forged-stale'],isolated)
env=dict(ENV,BD_READ_REF='refs/qa/forged-stale')
peer=bash('ac4-peer-reader-stale-refusal',['scripts/bd-read.sh','show',forged['id'],'--json'],isolated,expected=(2,),env=env)
check('ac4-peer-exact-cause',not peer.stdout and bool(re.search(r'precondition|conflict|applicable',decode(peer.stderr),re.I)),dict(stdout=decode(peer.stdout),stderr=decode(peer.stderr)))
remote=text(git('ac4-remote-still-original',['ls-remote','--heads','origin','beads-backup'])).split()[0]
check('ac4-base-and-queue-preserved',remote==forged['base'] and sha(result_file.read_bytes())==initial_hash,dict(remote=remote,base=forged['base'],queue_sha256=initial_hash))
good=json.loads(bash('ac4-peer-original-readback',['scripts/bd-read.sh','show',forged['id'],'--json'],isolated).stdout)
if isinstance(good,list):good=good[0]
check('ac4-original-title-preserved',good['title']!='Forged',good)
save('ac4-result',dict(result='PASS',source=PIN,base=forged['base'],forged_candidate=forged['candidate'],guard='native installed pre-push refused',peer='native bd-read.sh custom data ref refused',original_id=forged['id'],queue_sha256=initial_hash))
print('AC4 exact forged stale precondition: guard + peer PASS; no task publication')
