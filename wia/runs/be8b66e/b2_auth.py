from common import *
def main():
 root=C/'b2-auth';root.mkdir(exist_ok=True);bare=root/'source.git'
 if not bare.exists():
  git('b2-source-bare',['clone','--bare','--no-hardlinks',S,bare]);git('b2-main-ref',['update-ref','refs/heads/main',PIN],bare);git('b2-bare-head',['symbolic-ref','HEAD','refs/heads/main'],bare)
 # Read-only correction of the already captured first case; no candidate rerun.
 n='b2-dirty-worktree';pub=root/n
 before=json.loads((E/(n+'-before.json')).read_bytes());after=json.loads((E/(n+'-after.json')).read_bytes());actual=json.loads((E/(n+'-actual.json')).read_bytes())
 assert actual['exit_code']==6 and 'tooling' in actual['stderr'] and before==after
 assert not (root/(n+'-node')/'node-called.log').exists() and not (pub/'.beads/dolt').exists() and not (pub/'.beads/embeddeddolt').exists()
 original=(E/(n+'-original.bin')).read_bytes();module=pub/'scripts/lib/bd-git-environment.mjs'
 save(n+'-result',dict(source=PIN,exit_code=6,no_node_call=True,no_DB=True,all_bytes_unchanged=True,dirty_module_sha256=sha(module.read_bytes()),qa_correction='tracked .beads config/metadata are not an embedded DB; original native call and snapshots reused without rerun'))
 (E/'STOP.json').rename(E/'QA-HARNESS-STOP.json')
 module.write_bytes(original);save(n+'-restore',dict(restored_sha256=sha(original),method='explicit saved original bytes; no native replay'))
 row(n,'AC6/AC9 B2','PASS','Already captured native shell RC6/no fake Node; full before-after equal; read-only QA correction distinguishes tracked metadata from DB',n+'-result.json')
 for staged in [True]:
  n='b2-dirty-'+('staged' if staged else 'worktree');pub=root/n
  git(n+'-clone',['clone','--single-branch','--branch','main','--no-hardlinks','-c','core.autocrlf=false',bare,pub])
  module=pub/'scripts/lib/bd-git-environment.mjs';original=module.read_bytes();(E/(n+'-original.bin')).write_bytes(original);module.write_bytes(original+b'\n// QA synthetic tracked sanitizer drift\n')
  if staged:git(n+'-stage',['-c','core.autocrlf=false','add','--','scripts/lib/bd-git-environment.mjs'],pub)
  fake=root/(n+'-node');fake.mkdir();log=fake/'node-called.log';(fake/'node').write_text('#!/bin/sh\necho invoked > "'+log.as_posix()+'"\nexit 97\n',encoding='utf-8',newline='\n');(fake/'node').chmod(0o755)
  before=snap(n+'-before',{'publisher':pub,'origin':bare})
  q=bash(n+'-actual',pub/'scripts/bd-apply-intents.sh',['--read-state'],pub,env={'PATH':str(fake)+';'+ENV['PATH']},expected=None)
  after=snap(n+'-after',{'publisher':pub,'origin':bare})
  assert q.returncode==6 and ('tooling'.encode() in q.stderr),n+' wrong refusal'
  assert not log.exists() and not (pub/'.beads/dolt').exists() and not (pub/'.beads/embeddeddolt').exists(),n+' Node/task write'
  assert before==after,n+' unexpected target or remote write'
  save(n+'-result',dict(source=PIN,exit_code=q.returncode,no_node_call=True,no_DB=True,all_bytes_unchanged=True,dirty_module_sha256=sha(module.read_bytes())))
  module.write_bytes(original)
  if staged:git(n+'-restore-index',['-c','core.autocrlf=false','add','--','scripts/lib/bd-git-environment.mjs'],pub)
  assert module.read_bytes()==original;save(n+'-restore',dict(restored_sha256=sha(original),method='explicit saved original bytes; exact original index restored for staged case'))
  row(n,'AC6/AC9 B2','PASS','Native shell actual RC6 before logging fake Node; tracked dirty sanitizer retained, task/remote bytes unchanged; explicit saved-byte restoration',n+'-result.json')
 primary=root/'identity-primary';pub=root/'identity-publisher'
 for n,target in [('auth-primary',primary),('auth-publisher',pub)]:
  git(n+'-clone',['clone','--single-branch','--branch','main','--no-hardlinks','-c','core.autocrlf=false',bare,target])
 assert git('identity-absent',['config','--local','--get-regexp','^user\\.(name|email)$'],pub,expected=1)==b''
 output=R/'missing-identity-plan.json';before=snap('identity-before',{'primary':primary,'publisher':pub,'origin':bare})
 q=run('missing-identity-actual',['node',pub/'scripts/bd-publisher-setup.mjs','--primary-root',primary,'--publisher-root',pub,'--qualified-cli',BD,'--output',output],pub,expected=1)
 assert b'identity unavailable' in q.stderr and not output.exists()
 after=snap('identity-after',{'primary':primary,'publisher':pub,'origin':bare});assert before==after
 row('missing-repo-local-identity','AC6/AC9 B3','PASS','Actual native setup CLI actionable STOP before plan/control/DB/remote write; explicit absent local/service identity','missing-identity-actual.json')
 git('auth-local-name',['config','user.name','Windows synthetic auth QA'],pub);git('auth-local-email',['config','user.email','qa-auth@example.invalid'],pub)
 before=snap('https-auth-before',{'publisher':pub,'origin':bare})
 run('https-auth-missing-helper',['node',R/'auth-probe.mjs','missing',pub],pub)
 after=snap('https-auth-after',{'publisher':pub,'origin':bare});assert before==after
 row('missing-HTTPS-local-helper','AC6/AC9 B3','PASS','Exact candidate exported auth preflight with synthetic HTTPS push URL rejects before setup writes; no external network or authenticated push','https-auth-missing-helper.json')
 helper=root/'synthetic-helper.sh';helper_log=root/'synthetic-helper.log'
 helper.write_text('#!/bin/sh\nprintf "%s\\n" "$1" >> "'+helper_log.as_posix()+'"\nif [ "$1" = get ]; then printf "username=windows-qa\\npassword=synthetic-test-only\\n"; fi\n',encoding='utf-8',newline='\n');helper.chmod(0o755)
 git('auth-local-helper',['config','credential.helper',helper.as_posix()],pub)
 global_file=root/'global-helper-spoof.config';global_file.write_text('[credential]\n\thelper = !printf "username=wrong\\npassword=wrong\\n"\n',encoding='utf-8',newline='\n')
 run('auth-helper-native-fill',['node',R/'auth-probe.mjs','helper',pub,global_file],pub)
 assert helper_log.read_text().strip()=='get'
 save('auth-helper-result',dict(source=PIN,helper_invoked=True,helper_log_sha256=sha(helper_log.read_bytes()),synthetic_only=True,authenticated_push='NOT RUN',global_helper_excluded=True))
 row('synthetic-local-credential-helper','AC6/AC9 B3','PASS','Candidate clean Git env + actual native git credential fill uses owned repo-local helper; global spoof excluded; no external write','auth-helper-result.json')
 print('B2/AUTH COMPLETE',flush=True)
guard(main)
