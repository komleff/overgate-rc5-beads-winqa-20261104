from installed import *
from verify_lifecycle import verify_peer
def main():
 assert not (E/'STOP.json').exists()
 for n in ['pre-init-no-identity','pre-init-no-HTTPS-helper','inherited-COUNT-spoof']:
  root=C/n;roots,head=install(n,root);work=R/'activation-work'/n;actor='agent-'+str(uuid.uuid4());args=activation_args(roots,work,actor,'Windows B3 '+n+' synthetic task');override={}
  if n=='pre-init-no-identity':
   for key in ['user.name','user.email']:git(n+'-remove-'+key,['config','--local','--unset-all',key],roots['publisher'])
   assert git(n+'-identity-absent',['config','--local','--get-regexp','^user\\.(name|email)$'],roots['publisher'],expected=1)==b''
  elif n=='pre-init-no-HTTPS-helper':
   for role in ['primary','publisher','peer']:git(n+'-'+role+'-synthetic-pushurl',['remote','set-url','--push','origin','https://b3-synthetic.example.invalid/project.git'],roots[role])
   assert git(n+'-helper-absent',['config','--local','--get-all','credential.helper'],roots['publisher'],expected=1)==b''
  else:
   attacker=roots['attacker'];override=dict(GIT_CONFIG_COUNT='2',GIT_CONFIG_KEY_0='remote.origin.url',GIT_CONFIG_VALUE_0=attacker.as_posix(),GIT_CONFIG_KEY_1='remote.origin.pushurl',GIT_CONFIG_VALUE_1=attacker.as_posix())
   raw_push=git(n+'-raw-push-spoof',['remote','get-url','--push','origin'],roots['primary'],env=override).decode().strip();assert Path(raw_push).resolve()==attacker.resolve()
  before=snap(n+'-before',roots)
  q=bash(n+'-public-activation','scripts/bd-activate.sh',args,roots['primary'],env=override,expected=None,timeout=300)
  after=snap(n+'-after',roots);save(n+'-work',dict(files=files(work),journal=json.loads((work/'activation-checkpoint.json').read_bytes()) if (work/'activation-checkpoint.json').exists() else None))
  if n!='inherited-COUNT-spoof':
   wanted=b'publisher Git identity unavailable' if n=='pre-init-no-identity' else b'publisher HTTPS authentication unavailable'
   assert q.returncode==1 and wanted in q.stderr,n+' unexpected negative failure'
   assert before==after,n+' target/remote bytes changed before identity/helper refusal'
   assert all(not (roots[r]/'.beads').exists() and not (roots[r]/'.git/overgate-bd-publisher-control').exists() for r in ['primary','publisher','peer'])
   journal=json.loads((work/'activation-checkpoint.json').read_bytes());assert journal['stage']=='queued'
   save(n+'-result',dict(source=PIN,target=head,exit_code=1,actionable_reason=wanted.decode(),before_init_control_task_write=True,all_target_remote_bytes_equal=True,real_R=None,attacker_R=None,private_queue_retained=True,journal_stage='queued',actor=actor))
   row(n,'B3 I2/I5/I6','PASS','Actual public installed pre-init refusal with private queue retained, before native init/control/task write; all target/remote bytes unchanged',n+'-result.json')
  else:
   assert q.returncode==0,n+' actual COUNT activation failure: '+q.stderr.decode('utf-8','replace')
   result=json.loads(q.stdout);assert result['status']=='activated' and result['claim_confirmed'] and result['published_sha']==result['peer_sha']
   assert before['attacker']==after['attacker']
   obj=verify_peer(n,roots,result);assert obj['assignee']==actor and obj['status']=='in_progress'
   save(n+'-result',dict(source=PIN,target=head,id=result['id'],actor=actor,claims_confirmed=True,real_R=result['published_sha'],peer_R=result['peer_sha'],attacker_R=None,attacker_all_bytes_unchanged=True,raw_pushurl_spoof_proved=True,full_peer_object_equal=True,override=override))
   row(n,'B3 I2/I4/I6','PASS','Actual qualified activation under exact COUNT URL/pushurl spoof; real task/claim+peer exact R/full object, attacker absent/byte unchanged',n+'-result.json')
 print('PREINIT/COUNT CONTROLS COMPLETE',flush=True)
guard(main)
