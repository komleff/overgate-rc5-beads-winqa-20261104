from common import *
def main():
 rows=json.loads((E/'results.json').read_bytes());save('QA-results-before-effective-spoof-correction',rows)
 for item in rows:
  if item['case'].startswith('b1-') and item['result']=='PASS':
   item['method']+='; original raw fetch probe was not redirected (locator framing/multivalue precedence), so this is guard/input coverage, not effective fetch-spoof qualification'
 save('results',rows)
 root=C/'b1';real=root/'real.git';attacker=root/'attacker.git';frozen='37a7d061bba28944163dfd4115aadd3c6552f659'
 global_file=R/'b1-effective-global.config';global_file.write_text('[url "'+attacker.as_posix()+'"]\n\tinsteadOf = '+real.as_posix()+'\n',encoding='utf-8',newline='\n')
 variants={'count-rewrite':dict(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='url.'+attacker.as_posix()+'.insteadOf',GIT_CONFIG_VALUE_0=real.as_posix()),'global-rewrite':dict(GIT_CONFIG_GLOBAL=str(global_file))}
 for variant,override in variants.items():
  for script in ['bd-wt.sh','bd-sync-export.sh','bd-sync-restore.sh','bd-bootstrap.sh']:
   n='b1-effective-'+variant+'-'+script.removesuffix('.sh');target=root/n
   git(n+'-clone',['clone','--single-branch','--branch','main','--no-hardlinks','-c','core.autocrlf=false',real,target]);git(n+'-literal-locator',['remote','set-url','origin',real.as_posix()],target)
   assert git(n+'-no-cache',['branch','-r','--list','origin/beads-backup'],target)==b''
   shutil.copytree(S/'scripts',target/'scripts');shutil.copytree(S/'.claude/tools',target/'.claude/tools');(target/'.agents').mkdir();shutil.copyfile(S/'.agents/distribution-manifest.json',target/'.agents/distribution-manifest.json')
   fake=root/(n+'-fake');fake.mkdir();log=fake/'forbidden.log';versionlog=fake/'version.log'
   (fake/'bd').write_text('#!/bin/sh\nif [ "$1" = --version ]; then echo version >> "'+versionlog.as_posix()+'"; echo "bd version 1.2.2 (synthetic)"; exit 0; fi\necho "$*" >> "'+log.as_posix()+'"\nexit 93\n',encoding='utf-8',newline='\n');(fake/'bd').chmod(0o755)
   (fake/'bd.cmd').write_text('@echo off\r\nif "%~1"=="--version" (\r\necho version >> "'+str(versionlog)+'"\r\necho bd version 1.2.2 ^(synthetic^)\r\nexit /b 0\r\n)\r\necho %* >> "'+str(log)+'"\r\nexit /b 93\r\n',encoding='utf-8',newline='')
   control=git(n+'-control-real',['ls-remote','--heads','origin','refs/heads/beads-backup'],target);assert control.decode().startswith(frozen+'\t')
   spoof=git(n+'-control-spoof',['ls-remote','--heads','origin','refs/heads/beads-backup'],target,env=override);assert not spoof.strip(),n+' fixture failed to redirect; no candidate run'
   before=snap(n+'-before',{'target':target,'real':real,'attacker':attacker})
   args=['update','wqa-z5e','--claim'] if script=='bd-wt.sh' else []
   q=bash(n+'-actual','scripts/'+script,args,target,env=dict(override,BD_BIN=str(fake/'bd'),PATH=str(fake)+';'+ENV['PATH']),expected=None)
   after=snap(n+'-after',{'target':target,'real':real,'attacker':attacker})
   assert q.returncode!=0 and (b'managed' in q.stderr or b'remote Beads state exists' in q.stderr),n+' wrong preflight refusal'
   assert not log.exists() and not (target/'.beads').exists(),n+' native task/init/export/import call'
   assert before['real']==after['real'] and before['attacker']==after['attacker'] and task_surface(before['target'])==task_surface(after['target'])
   save(n+'-result',dict(source=PIN,exit_code=q.returncode,raw_git_spoof_effective=True,real_R=frozen,attacker_R=None,no_task_init_export_import=True,version_probe_only=versionlog.exists(),remote_task_config_index_hooks_unchanged=True,git_fetch_cache_changes=[p for p in set(before['target'])|set(after['target']) if before['target'].get(p)!=after['target'].get(p)]))
   row(n,'AC6/AC9 B1','PASS','Fresh normalized exact locator; raw Git demonstrably redirects to empty attacker, candidate relative shell route refuses against true managed origin before task/init/export/import',n+'-result.json')
 print('EFFECTIVE SPOOF NEGATIVES COMPLETE',flush=True)
guard(main)
