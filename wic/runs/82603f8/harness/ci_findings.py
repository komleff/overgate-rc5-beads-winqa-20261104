from native_common import *
matrix=json.loads((E/'c1-result.json').read_text(encoding='utf-8'))
roots={x['case']:x for x in matrix['cases']}
entry=next(h['command'] for x in json.loads((SRC/'.claude/settings.json').read_bytes())['hooks']['PreToolUse'] if x.get('matcher')=='Bash' for h in x['hooks'])
root=Path(roots['apostrophe']['root'])
hook('ci-apostrophe-root-read',entry,'git log -1 --oneline',root)
save('ci-apostrophe-root-read-result',dict(result='PASS',source=PIN,root=str(root),independent_pwd=roots['apostrophe']['actual_pwd']))
croot=Path(roots['c-drive']['root']);sub=croot/'own-subdir/deep'
env=dict(ENV,GIT_DIR=str(SRC/'.git'),GIT_WORK_TREE=str(SRC),CLAUDE_PROJECT_DIR=str(SRC))
command="cd '"+croot.as_posix()+"'"
hook('ci-spoofed-git-own-dos-quoted',entry,command,sub,env=env)
save('ci-spoofed-git-own-dos-quoted-result',dict(result='PASS',source=PIN,root=str(croot),command=command,independent_pwd=roots['c-drive']['actual_pwd']))
print('Both expanded CI findings PASS independently')
