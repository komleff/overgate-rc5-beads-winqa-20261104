from installed import *
def main():
 n='complex-installed';root=C/"Проект's (QA) space"
 roots,head=install(n,root);work=R/'activation-work/complex';actor='agent-'+str(uuid.uuid4());title='Windows B3 complex-path synthetic actual task'
 args=activation_args(roots,work,actor,title);before=snap(n+'-before-activation',roots)
 q=bash(n+'-activation','scripts/bd-activate.sh',args,roots['primary'],expected=None,timeout=300)
 after=snap(n+'-after-activation',roots)
 refs={role:ref(n+'-after-'+role+'-refs',roots[role]) for role in ['real','attacker','peer']}
 save(n+'-activation-state',dict(source=PIN,target=head,literal_root=str(root),invocation=['bash','scripts/bd-activate.sh',*args],exit_code=q.returncode,refs=refs,work_files=files(work),local_DB_present={role:(roots[role]/'.beads').exists() for role in ['primary','publisher','peer']},before_after_equal=before==after))
 if q.returncode:
  row(n+'-public-activation','B3 I2/I4/I5/I6','FAIL','Actual installed public relative Git Bash activation in required combined Windows path; stop at first actual product failure',n+'-activation.json')
  raise AssertionError('first actual product FAIL: '+n+' activation RC'+str(q.returncode)+' '+q.stderr.decode('utf-8','replace'))
 result=json.loads(q.stdout);assert result['status']=='activated' and result['claim_confirmed'] and result['published_sha']==result['peer_sha']
 save(n+'-activation-result',result);row(n+'-public-activation','B3 I2/I4/I5/I6','PASS','Actual installed public activation in combined path; real ID/confirmed claim/peer same SHA',n+'-activation-result.json')
 print('COMPLEX ACTIVATION PASS',flush=True)
guard(main)
