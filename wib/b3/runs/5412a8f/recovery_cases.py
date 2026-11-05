from installed import *
from verify_lifecycle import verify_peer
def native_store(root):
 mode=json.loads((root/'.beads/metadata.json').read_bytes())['dolt_mode']
 return root/'.beads'/dict(embedded='embeddeddolt',server='dolt')[mode]
def checkpoint_case(n,point,negative=False):
 root=C/n;work=R/'activation-work'/n;journal_file=work/'activation-checkpoint.json'
 if (E/(n+'-fault-work.json')).exists():
  from types import SimpleNamespace
  roots={r:root/r for r in ['primary','publisher','peer']};roots.update(real=root/'real.git',attacker=root/'attacker.git');journal=json.loads(journal_file.read_bytes());head=journal['bound']['head'];actor=journal['bound']['actor'];args=activation_args(roots,work,actor,journal['bound']['title'])
  before=json.loads((E/(n+'-before-fault.json')).read_bytes());after_fault=json.loads((E/(n+'-after-fault.json')).read_bytes());receipt=json.loads((E/(n+'-injected-stop.json')).read_bytes());failed=SimpleNamespace(returncode=receipt['exit_code'],stderr=(E/(n+'-injected-stop.stderr.bin')).read_bytes())
  assert {r:files(p) for r,p in roots.items()}==after_fault and files(work)==json.loads((E/(n+'-fault-work.json')).read_bytes())['files']
  save(n+'-QA-resume-captured-checkpoint',dict(native_fault_repeated=False,all_captured_target_work_bytes_equal=True,reason='QA store path now follows metadata dolt_mode=embedded rather than hardcoded dolt directory'))
 else:
  roots,head=install(n,root);actor='agent-'+str(uuid.uuid4());args=activation_args(roots,work,actor,'Windows B3 '+n+' synthetic task');before=snap(n+'-before-fault',roots)
  failed=bash(n+'-injected-stop','scripts/bd-activate.sh',args,roots['primary'],env={'OVERGATE_BD_ACTIVATE_TEST_FAIL_AT':point},expected=None,timeout=300)
  after_fault=snap(n+'-after-fault',roots);journal=json.loads(journal_file.read_bytes()) if journal_file.exists() else {};save(n+'-fault-work',dict(files=files(work),journal=journal))
 expected={'after-peer-init':'peer-init','after-setup':'setup','after-bootstrap':'bootstrapped','after-push':'published'}[point]
 assert failed.returncode==1 and ('injected activation stop after '+point).encode() in failed.stderr,n+' unexpected product failure before intended fault'
 assert journal['stage']==expected and journal['bound']['actor']==actor and journal['binary_sha256']=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de'
 raw=work/'raw-intents.jsonl';raw_bytes=raw.read_bytes();raw_ino=raw.stat().st_ino;metadata={r:(roots[r]/'.beads/metadata.json').read_bytes() for r in ['primary','peer']};store_ino={r:native_store(roots[r]).stat().st_ino for r in ['primary','peer']}
 assert after_fault['attacker']==before['attacker']
 real_fault=ref(n+'-real-at-fault',roots['real']);assert ('beads-backup' in real_fault)==(point=='after-push')
 prepared=work/'prepared.v2.jsonl';prepared_bytes=prepared.read_bytes() if prepared.exists() else None
 if negative:
  drift=root/'drift-attacker.git';git(n+'-clone-attacker-after-checkpoint',['clone','--bare','--no-hardlinks',roots['real'],drift]);roots['drift-attacker']=drift
  assert 'beads-backup' not in ref(n+'-drift-attacker-empty',drift)
  for role in ['primary','publisher','peer']:
   git(n+'-'+role+'-drift-fetch',['remote','set-url','origin',drift.as_posix()],roots[role]);git(n+'-'+role+'-drift-push',['remote','set-url','--push','origin',drift.as_posix()],roots[role])
   git(n+'-'+role+'-read-drift-config',['config','--local','--get-regexp','^remote\\.origin\\.(url|pushurl)$'],roots[role])
  before_resume=snap(n+'-before-negative-resume',roots);work_before=files(work)
  refused=bash(n+'-negative-resume','scripts/bd-activate.sh',[*args,'--resume'],roots['primary'],expected=None,timeout=300)
  after_resume=snap(n+'-after-negative-resume',roots)
  assert refused.returncode==1 and b'activation checkpoint origin changed' in refused.stderr,n+' wrong negative result'
  assert before_resume==after_resume and files(work)==work_before,n+' negative changed retained state'
  assert raw.read_bytes()==raw_bytes and raw.stat().st_ino==raw_ino
  assert all((roots[r]/'.beads/metadata.json').read_bytes()==metadata[r] and native_store(roots[r]).stat().st_ino==store_ino[r] for r in ['primary','peer'])
  save(n+'-result',dict(source=PIN,target=head,stage=expected,refusal_rc=1,real_R=None,attacker_R=None,drift_attacker_R=None,all_resume_target_remote_work_bytes_unchanged=True,raw_sha256=sha(raw_bytes),actor=actor,binary_sha256=journal['binary_sha256'],original_origin_sha256=journal['bound']['origin_sha256'],journal_preserved=True,metadata_preserved=True,no_store_recreate=True))
  row(n,'B3 I2/I4/I5','PASS','After peer-init clone real bare, change all3 repo-local fetch+push origins; public --resume refuses before any further DB/control/queue/task write; exact full bytes unchanged',n+'-result.json')
  return
 before_resume=snap(n+'-before-positive-resume',roots)
 resumed=bash(n+'-positive-resume','scripts/bd-activate.sh',[*args,'--resume'],roots['primary'],expected=None,timeout=300)
 after_resume=snap(n+'-after-positive-resume',roots)
 assert resumed.returncode==0,n+' actual resume product FAIL: '+resumed.stderr.decode('utf-8','replace')
 result=json.loads(resumed.stdout);assert result['status']=='activated' and result['claim_confirmed'] and result['peer_sha']==result['published_sha']
 completed=json.loads(journal_file.read_bytes());assert completed['stage']=='complete' and completed['bound']==journal['bound'] and completed['binary_sha256']==journal['binary_sha256']
 assert raw.read_bytes()==raw_bytes and raw.stat().st_ino==raw_ino
 assert all((roots[r]/'.beads/metadata.json').read_bytes()==metadata[r] and native_store(roots[r]).stat().st_ino==store_ino[r] for r in ['primary','peer'])
 if prepared_bytes is not None:assert prepared.read_bytes()==prepared_bytes
 if point=='after-push':assert result['published_sha']==journal['published']['published_sha'] and real_fault==ref(n+'-real-after-resume',roots['real'])
 assert before_resume['attacker']==after_resume['attacker']
 for role in ['primary','publisher','peer']:
  for p in ['.git/HEAD','.git/index','.overgate/install-state.json']:assert before[role][p]==after_resume[role][p]
 obj=verify_peer(n,roots,result);assert obj['status']=='in_progress' and obj['assignee']==actor
 proof=json.loads((E/(n+'-peer-proof.json')).read_bytes());assert proof['issue_records']==1
 save(n+'-result',dict(source=PIN,target=head,fault=point,initial_stage=expected,completed_stage='complete',id=result['id'],actor=actor,claim_confirmed=True,published_sha=result['published_sha'],peer_sha=result['peer_sha'],attacker_R=None,raw_queue_preserved=True,raw_queue_sha256=sha(raw_bytes),raw_queue_inode_preserved=True,prepared_queue_preserved=prepared_bytes is not None,metadata_and_store_directory_inode_preserved=True,same_bound_journal_actor_binary=True,HEAD_index_install_state_preserved=True,task_records=1,postpush_R_unchanged=(point=='after-push')))
 row(n,'B3 I4/I5/I6','PASS','Separate public injected fault then same-args --resume; raw queue/actor/CLI/metadata/store dirs preserved; one real task/confirmed claim; peer exact full object/R; after-push no R advance',n+'-result.json')
def main():
 assert not (E/'STOP.json').exists()
 checkpoint_case('origin-drift-negative','after-peer-init',True)
 for n,point in [('resume-peer-init','after-peer-init'),('resume-publisher-setup','after-setup'),('resume-bootstrap','after-bootstrap'),('resume-push','after-push')]:checkpoint_case(n,point)
 print('RECOVERY CASES COMPLETE',flush=True)
guard(main)
