from common import *
def main():
 rows=json.loads((E/'results.json').read_bytes());save('QA-initial-results-before-bootstrap-path-correction',rows)
 for item in rows:
  if item['case'].startswith('b1-') and item['case'].endswith('bd-bootstrap'):
   item.update(result='NOT RUN',method='QA invocation used absolute Windows backslash script operand; BASH_SOURCE path resolved wrong directory before security preflight; not a product security result')
 save('results',rows)
 root=C/'b1';real=root/'real.git';attacker=root/'attacker.git';frozen='37a7d061bba28944163dfd4115aadd3c6552f659'
 global_file=root/'rewrite-global.config'
 variants={
  'count-url':dict(GIT_CONFIG_COUNT='2',GIT_CONFIG_KEY_0='remote.origin.url',GIT_CONFIG_VALUE_0=attacker.as_posix(),GIT_CONFIG_KEY_1='remote.origin.pushurl',GIT_CONFIG_VALUE_1=attacker.as_posix()),
  'parameters-url':dict(GIT_CONFIG_PARAMETERS="'remote.origin.url="+attacker.as_posix()+"' 'remote.origin.pushurl="+attacker.as_posix()+"'"),
  'count-rewrite':dict(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='url.'+attacker.as_posix()+'.insteadOf',GIT_CONFIG_VALUE_0=real.as_posix()),
  'global-rewrite':dict(GIT_CONFIG_GLOBAL=str(global_file))}
 for variant,override in variants.items():
  n='b1-bootstrap-relative-'+variant;target=root/n
  git(n+'-clone',['clone','--single-branch','--branch','main','--no-hardlinks','-c','core.autocrlf=false',real,target])
  assert git(n+'-no-cache',['branch','-r','--list','origin/beads-backup'],target)==b''
  shutil.copytree(S/'scripts',target/'scripts');shutil.copytree(S/'.claude/tools',target/'.claude/tools');(target/'.agents').mkdir();shutil.copyfile(S/'.agents/distribution-manifest.json',target/'.agents/distribution-manifest.json')
  fake=root/(n+'-fake');fake.mkdir();log=fake/'forbidden-call.log';versionlog=fake/'version-only.log'
  (fake/'bd').write_text('#!/bin/sh\nif [ "$1" = --version ]; then echo version >> "'+versionlog.as_posix()+'"; echo "bd version 1.2.2 (synthetic-version-probe)"; exit 0; fi\necho "$*" >> "'+log.as_posix()+'"\nexit 93\n',encoding='utf-8',newline='\n');(fake/'bd').chmod(0o755)
  (fake/'bd.cmd').write_text('@echo off\r\nif "%~1"=="--version" (\r\necho version >> "'+str(versionlog)+'"\r\necho bd version 1.2.2 ^(synthetic-version-probe^)\r\nexit /b 0\r\n)\r\necho %* >> "'+str(log)+'"\r\nexit /b 93\r\n',encoding='utf-8',newline='')
  before=snap(n+'-before',{'target':target,'real':real,'attacker':attacker})
  q=bash(n+'-actual','scripts/bd-bootstrap.sh',[],target,env=dict(override,BD_BIN=str(fake/'bd'),PATH=str(fake)+';'+ENV['PATH']),expected=None)
  after=snap(n+'-after',{'target':target,'real':real,'attacker':attacker})
  assert q.returncode==1 and b'remote Beads state exists' in q.stderr,n+' did not reach intended preflight'
  assert versionlog.exists() and not log.exists() and not (target/'.beads').exists(),n+' unexpected task operation'
  assert before==after,n+' project/Git/remote byte drift'
  save(n+'-result',dict(source=PIN,invocation='bash scripts/bd-bootstrap.sh',exit_code=q.returncode,version_only_called=True,task_init_export_import_calls=False,all_bytes_unchanged=True,real_R=frozen,attacker_R=None,fixture_correction='new fresh clone, exact launcher+manifest present; original raw invocation failures preserved and marked NOT RUN'))
  row(n,'AC6/AC9 B1','PASS','Actual relative shell entry reaches remote-state STOP; synthetic version probe only, zero task/init/import/export calls; full target/Git/remote bytes unchanged',n+'-result.json')
 print('BOOTSTRAP RELATIVE COMPLETE',flush=True)
guard(main)
