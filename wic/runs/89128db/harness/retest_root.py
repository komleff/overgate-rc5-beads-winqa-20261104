from native_common import *
old=Path("D:/CodexArtifacts/overgate-rc5-wic-82603f8-winqa-20261105/run-82603f8/cases/project'apostrophe")
launcher=old/'.claude/tools/run-python.sh'
before=launcher.read_bytes();candidate=(SRC/'.claude/tools/run-python.sh').read_bytes()
(R/'original-failed-launcher.bin').write_bytes(before)
check('exact-root-settings-equivalence',(old/'.claude/settings.json').read_bytes()==(SRC/'.claude/settings.json').read_bytes(),'unchanged exact settings blob from 82603f8')
launcher.write_bytes(candidate)
entry=next(h['command'] for x in json.loads((SRC/'.claude/settings.json').read_bytes())['hooks']['PreToolUse'] if x.get('matcher')=='Bash' for h in x['hooks'])
pwd=run('exact-root-independent-pwd',[BASH,'-c','pwd -P'],old).stdout.decode('utf-8').strip()
save('exact-root-binding',dict(source=PIN,fixture=str(old),native_pwd=pwd,old_launcher_sha256=sha(before),new_launcher_sha256=sha(candidate),actual_guard_exists=(old/'.claude/hooks/check-repository-mutation.py').is_file()))
hook('exact-apostrophe-root-read',entry,'git log -1 --oneline',old)
actual=run('exact-root-command-execution',[BASH,'-c','git log -1 --oneline'],old).stdout.decode('utf-8').strip()
save('exact-root-result',dict(result='PASS',source=PIN,root=str(old),native_pwd=pwd,command='git log -1 --oneline',hook_exit=0,actual_git_log=actual,launcher_sha256=sha(candidate)))
print('Exact prior apostrophe root read PASS on candidate launcher')
