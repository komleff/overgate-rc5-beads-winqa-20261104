from native_common import *
import sys,shlex
OLD=Path('D:/CodexArtifacts/overgate-rc5-wic-winqa-20261105/released-source')
OLDPIN='3f3246c3a3b62377fc02aad05283cae1ef5d4e2d'
INSTALLER=SRC/'scripts/install-overgate.py'
PR='https://github.com/example/project/pull/1'
plans=R/'installer-plans';plans.mkdir()
contract=R/'installer-contract.md';contract.write_text('Synthetic disposable QA only. Preserve README. No Beads. Frozen rc4.1 auto/bypass settings upgrade; exact native runtime; custom managed hook conflict before writes.\n',encoding='utf-8')
check('installer-old-source-pin',decode(run('installer-old-head',['git','-C',OLD,'rev-parse','HEAD']).stdout).strip()==OLDPIN,OLDPIN)
def snapshot(root):return {str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}
def init(name):
 root=R/'installed'/name;assert not root.exists();root.mkdir(parents=True)
 run(name+'-git-init',['git','init','--initial-branch=qa/installer',root])
 (root/'README.md').write_text('Project-owned QA README must stay byte-identical.\n',encoding='utf-8')
 run(name+'-git-add',['git','-C',root,'add','README.md'])
 run(name+'-git-commit',['git','-C',root,'-c','user.name=Windows QA','-c','user.email=qa@example.invalid','-c','commit.gpgsign=false','commit','-m','fixture baseline'])
 return root
def plan(name,source,pin,target,mode=None):
 file=plans/(name+'.plan.json')
 args=[sys.executable,INSTALLER,'plan','--source',source,'--source-sha',pin,'--target',target,'--contract',contract,'--target-pr',PR,'--output',file,'--no-beads']
 if mode:args+=['--mode',mode]
 run(name+'-plan',args,timeout=180)
 return file,json.loads(file.read_text(encoding='utf-8'))
def approve_apply(name,file,expected=0):
 approval=plans/(name+'.synthetic-approval.json')
 approval.write_text(json.dumps(dict(verdict='PLAN_READY',plan_sha256=sha(file.read_bytes()),evidence=PR+'#synthetic-fixture-only'))+'\n',encoding='utf-8')
 run(name+'-apply',[sys.executable,INSTALLER,'apply','--plan',file,'--approval',approval],expected=(expected,),timeout=180)
results=[]
for mode in ['auto','bypass']:
 label='installer-'+mode
 target=init(mode+" Проект's (QA) space");readme=(target/'README.md').read_bytes()
 file,data=plan(label+'-baseline',OLD,OLDPIN,target,mode)
 check(label+'-baseline-no-conflict',not data['conflicts'],data['conflicts']);approve_apply(label+'-baseline',file)
 old_settings=(target/'.claude/settings.json').read_bytes()
 old_mode=json.loads(old_settings)['permissions']['defaultMode']
 check(label+'-baseline-mode',old_mode==('auto' if mode=='auto' else 'bypassPermissions'),old_mode)
 file,data=plan(label+'-upgrade',SRC,PIN,target)
 check(label+'-upgrade-no-conflict',not data['conflicts'],data['conflicts']);approve_apply(label+'-upgrade',file)
 wanted=(SRC/'.claude/settings.json').read_bytes()
 if mode=='bypass':wanted=wanted.replace(b'"defaultMode": "auto"',b'"defaultMode": "bypassPermissions"')
 current=(target/'.claude/settings.json').read_bytes()
 check(label+'-known-settings-byte-upgrade',current==wanted,dict(actual_sha256=sha(current),expected_sha256=sha(wanted),mode=mode))
 check(label+'-project-readme-preserved',(target/'README.md').read_bytes()==readme,sha(readme))
 state=json.loads((target/'.overgate/install-state.json').read_bytes())
 check(label+'-installed-source-state',state['source_sha']==PIN and state['beads'] is False and state['mode']==mode,state)
 for path in ['.claude/hooks/pre-bash.sh','.claude/tools/run-python.sh']:
  check(label+'-runtime-'+Path(path).stem,(target/path).read_bytes()==(SRC/path).read_bytes(),path)
 run(label+'-installed-closure',[sys.executable,target/'scripts/check-reference.py','--root',target,'--no-beads'],target,timeout=120)
 entry=next(h['command'] for x in json.loads(current)['hooks']['PreToolUse'] if x.get('matcher')=='Bash' for h in x['hooks'])
 hook(label+'-installed-root-read',entry,'git log -1 --oneline',target)
 hook(label+'-installed-readiness-refusal',entry,'gh pr comment 1 --body "ready to merge"',target,2)
 sub=target/'nested';sub.mkdir()
 denied=hook(label+'-installed-subdir-ls',entry,'ls',sub,2)
 printed=denied.stderr.decode('utf-8').split('Восстановление: ',1)[1].splitlines()[0]
 (E/(label+'-printed.bin')).write_bytes(printed.encode())
 hook(label+'-installed-hint-replay',entry,printed,sub)
 actual=run(label+'-installed-hint-execute',[BASH,'-c',printed+' && pwd -P'],sub).stdout.decode('utf-8').strip()
 pwd=run(label+'-installed-independent-pwd',[BASH,'-c','pwd -P'],target).stdout.decode('utf-8').strip()
 check(label+'-installed-pwd',actual==pwd,dict(actual=actual,expected=pwd,printed=printed))
 results.append(dict(mode=mode,target=str(target),source=PIN,settings_sha256=sha(current),launcher_sha256=sha((target/'.claude/tools/run-python.sh').read_bytes()),executed_pwd=actual,result='PASS'))
 save('installer-progress',results)
custom=init('custom-conflict');p=custom/'.claude/settings.json';p.parent.mkdir()
old=json.loads((OLD/'.claude/settings.json').read_bytes());old['hooks']['PreToolUse'][0]['hooks'][0]['command']+=' ; true';p.write_text(json.dumps(old,ensure_ascii=False)+'\n',encoding='utf-8')
before=snapshot(custom)
file,data=plan('installer-custom-conflict',SRC,PIN,custom)
check('installer-custom-hook-plan-refusal',any('custom managed runtime hook' in x for x in data['conflicts']),data['conflicts'])
approve_apply('installer-custom-conflict',file,1)
check('installer-custom-target-unchanged',snapshot(custom)==before and not (custom/'.overgate-backups').exists(),dict(before=before,after=snapshot(custom)))
save('installer-result',dict(result='PASS scoped',source=PIN,baseline_payload_source=OLDPIN,installer_code_source=PIN,synthetic_fixture_approval=True,real_project_approval=False,
 upgrades=results,custom_hook_conflict_preserved=True,beads_used=False))
print(json.dumps(dict(installer='PASS',upgrades=2,custom_conflict='PASS',source=PIN)))
