from common import *
def main():
 root=C/'b1';root.mkdir();real=root/'real.git';attacker=root/'attacker.git'
 git('b1-real-clone',['clone','--bare','--no-hardlinks',PREP/'real-origin.git',real])
 git('b1-attacker-clone',['clone','--bare','--no-hardlinks',PREP/'attacker-origin.git',attacker])
 frozen='37a7d061bba28944163dfd4115aadd3c6552f659'
 old=Path('D:/CodexArtifacts/overgate-rc5-wia-0a8685e-winqa-20261105/origin.git')
 git('b1-copy-valid-managed-snapshot',['fetch','--no-tags',old,frozen+':refs/heads/beads-backup'],real)
 marker=git('b1-managed-marker',['show',frozen+':.beads/overgate-managed-v1.json'],real);assert marker.strip()
 save('b1-managed-fixture-source',dict(task_data_commit=frozen,method='Git object copy of immutable previous legitimate native managed publication; no previous source code or publisher executed',marker_sha256=sha(marker)))
 global_config=root/'rewrite-global.config';global_config.write_text('[url "'+attacker.as_posix()+'"]\n\tinsteadOf = '+real.as_posix()+'\n',encoding='utf-8',newline='\n')
 overrides={
  'count-url':dict(GIT_CONFIG_COUNT='2',GIT_CONFIG_KEY_0='remote.origin.url',GIT_CONFIG_VALUE_0=attacker.as_posix(),GIT_CONFIG_KEY_1='remote.origin.pushurl',GIT_CONFIG_VALUE_1=attacker.as_posix()),
  'parameters-url':dict(GIT_CONFIG_PARAMETERS="'remote.origin.url="+attacker.as_posix()+"' 'remote.origin.pushurl="+attacker.as_posix()+"'"),
  'count-rewrite':dict(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='url.'+attacker.as_posix()+'.insteadOf',GIT_CONFIG_VALUE_0=real.as_posix()),
  'global-rewrite':dict(GIT_CONFIG_GLOBAL=str(global_config))}
 for variant,override in overrides.items():
  for script in ['bd-wt.sh','bd-sync-export.sh','bd-sync-restore.sh','bd-bootstrap.sh']:
   n='b1-'+variant+'-'+script.removesuffix('.sh');target=root/n
   git(n+'-clone',['clone','--single-branch','--branch','main','--no-hardlinks','-c','core.autocrlf=false',real,target])
   assert git(n+'-no-cache',['branch','-r','--list','origin/beads-backup'],target)==b''
   shutil.copytree(S/'scripts',target/'scripts');shutil.copytree(S/'.claude/tools',target/'.claude/tools')
   fake=root/(n+'-fake');fake.mkdir();log=fake/'calls.log'
   (fake/'bd').write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "'+log.as_posix()+'"\nexit 93\n',encoding='utf-8',newline='\n');(fake/'bd').chmod(0o755)
   (fake/'bd.cmd').write_text('@echo off\r\necho %* >> "'+str(log)+'"\r\nexit /b 93\r\n',encoding='utf-8',newline='')
   injected=dict(override,BD_BIN=str(fake/'bd'),PATH=str(fake)+';'+ENV['PATH'])
   raw=run(n+'-raw-git-spoof-probe',['git','ls-remote','--heads','origin','refs/heads/beads-backup'],target,env=override)
   # Record effective Git framing; multivalue remote.url precedence differs by Git build.
   save(n+'-spoof-precondition',dict(override=override,raw_ls_remote=raw.stdout.decode(),real_R=frozen,attacker_R=None,effective_fetch_redirected=not raw.stdout.strip()))
   roots={'target':target,'real':real,'attacker':attacker};before=snap(n+'-before',roots)
   args=['update','wqa-z5e','--claim'] if script=='bd-wt.sh' else []
   q=bash(n+'-actual',target/'scripts'/script,args,target,env=injected,expected=None)
   after=snap(n+'-after',roots)
   assert q.returncode!=0,n+' accepted forbidden route'
   assert not log.exists(),n+' invoked native/fake bd: '+(log.read_text() if log.exists() else '')
   assert before['real']==after['real'] and before['attacker']==after['attacker'],n+' remote changed'
   assert task_surface(before['target'])==task_surface(after['target']),n+' project/task/config/index/hooks changed'
   assert not (target/'.beads').exists() and not (target/'.bd-intents').exists(),n+' task DB/queue created'
   changes=[p for p in set(before['target'])|set(after['target']) if before['target'].get(p)!=after['target'].get(p)]
   save(n+'-result',dict(source=PIN,exit_code=q.returncode,real_R=frozen,attacker_R=None,no_bd_call=True,task_config_index_hooks_unchanged=True,remote_byte_unchanged=True,observed_git_read_cache_changes=changes))
   row(n,'AC6/AC9 B1','PASS','Fresh unregistered/no-cache native Git Bash refusal; logging fake bd never invoked; remote/task/config/index/hooks unchanged; Git fetch cache changes recorded',n+'-result.json')
 print('B1 COMPLETE',flush=True)
guard(main)
