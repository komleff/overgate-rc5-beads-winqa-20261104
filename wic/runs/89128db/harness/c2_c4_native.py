from native_common import *
import shlex,sys
data=json.loads((E/'c1-result.json').read_text(encoding='utf-8'))
entry=next(h['command'] for x in json.loads((SRC/'.claude/settings.json').read_bytes())['hooks']['PreToolUse'] if x.get('matcher')=='Bash' for h in x['hooks'])
roots={x['case']:x for x in data['cases']};primary=roots['space'];root=Path(primary['root']);sub=root/'own-subdir/deep'
sentinel=R/'C2-SENTINEL';check('sentinel-initially-absent',not sentinel.exists(),str(sentinel))
touch='touch '+shlex.quote(sentinel.as_posix());printed=primary['printed'];target=primary['actual_pwd']
commands={'semicolon-tail':printed+'; '+touch,'and-tail':printed+' && '+touch,'newline-tail':printed+'\n'+touch,
 'substitution':'cd "$('+touch+'; printf %s '+shlex.quote(target)+')"',
 'backtick':'cd `'+touch+'`','variable':'cd $WIC_TARGET','glob':'cd '+(root.parent.as_posix())+'/*',
 'second-cd':printed+' '+printed,'relative':'cd ..',
 'other-dispatcher-checkout':roots['ascii']['printed'],'drive-relative':'cd D:other','other-drive':'cd C:/other'}
env=dict(ENV,WIC_TARGET=target)
for name,command in commands.items():
 hook('c2-'+name,entry,command,sub,2,env)
 check('c2-'+name+'-no-side-effect',not sentinel.exists(),str(sentinel))
git_spoof=dict(ENV,GIT_DIR=str(SRC/'.git'),GIT_WORK_TREE=str(SRC))
hook('ci-spoofed-git-own-canonical',entry,printed,sub,env=git_spoof)
hook('ci-spoofed-git-foreign-canonical-denied',entry,roots['ascii']['printed'],sub,2,git_spoof)
spoof=dict(ENV,CLAUDE_PROJECT_DIR=roots['ascii']['root'])
hook('c2-project-dir-spoof',entry,roots['ascii']['printed'],sub,2,spoof)
for case in ['apostrophe','cyrillic','parentheses']:
 x=roots[case];hook('c2-'+case+'-tail',entry,x['printed']+'; '+touch,Path(x['root'])/'own-subdir/deep',2)
 check('c2-'+case+'-tail-no-side-effect',not sentinel.exists(),'sentinel absent')
for case in ['ascii','c-drive']:
 x=roots[case];cwd=Path(x['root'])/'own-subdir/deep'
 hook('c2-'+case+'-dos-same-root',entry,'cd '+Path(x['root']).as_posix(),cwd)
 hook('c2-'+case+'-msys-same-root',entry,'cd '+x['actual_pwd'],cwd)
 other=roots['c-drive' if case=='ascii' else 'ascii']
 hook('c2-'+case+'-other-real-drive-checkout',entry,'cd '+Path(other['root']).as_posix(),cwd,2)
missing=R/'cases/missing-dispatcher';missing.mkdir()
run('c2-missing-git-init',['git','init','--initial-branch=qa/preparation',missing])
(missing/'sub').mkdir()
hook('c2-missing-dispatcher',entry,'cd '+missing.as_posix(),missing/'sub',2)
outside=R/'outside-no-git';outside.mkdir()
run('outside-not-git',['git','rev-parse','--is-inside-work-tree'],outside,expected=(1,128))
denied=hook('c4-outside-ls-denied',entry,'ls',outside,2)
check('c4-honest-root-session-guidance','Восстановление: cd' not in decode(denied.stderr) and 'новую сессию' in decode(denied.stderr),decode(denied.stderr))
hook('c3-outside-legacy-simple-cd',entry,'cd '+Path(roots['ascii']['root']).as_posix(),outside)
hook('c4-outside-complex-cd-refused',entry,roots['space']['printed'],outside,2)
hook('c3-root-main-mutation-denied',entry,'git push origin main',Path(roots['ascii']['root']),2)
hook('c3-root-readiness-denied',entry,'gh pr comment 1 --body "ready to merge"',Path(roots['ascii']['root']),2)
run('c3-existing-native-root-scenarios',[sys.executable,SRC/'scripts/tests/pre-bash-dispatch.test.py','RootScenarios'],SRC,timeout=120)
check('c2-final-no-sentinel',not sentinel.exists(),'all native negatives completed without sentinel')
save('c2-c4-result',dict(result='PASS scoped',source=PIN,negative_cases=list(commands),sentinel_absent=True,
 extra=['apostrophe/cyrillic/parentheses tails','DOS and MSYS same-root spelling on C and D','real other drive checkout refused','missing dispatcher','CLAUDE_PROJECT_DIR spoof refused','outside-Git legacy simple cd','honest outside guidance','root mutation/readiness/test gate scenarios']))
print('C2/C3/C4 native targeted cases PASS; no sentinel')
