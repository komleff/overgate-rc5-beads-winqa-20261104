from native_common import *
settings=(SRC/'.claude/settings.json').read_bytes()
entries=[h for e in json.loads(settings)['hooks']['PreToolUse'] if e.get('matcher')=='Bash' for h in e['hooks']]
check('one-managed-entry',len(entries)==1 and entries[0]['timeout']==600,entries)
entry=entries[0]['command'];cases=R/'cases';cases.mkdir()
roots=[('ascii',cases/'project-ascii'),('space',cases/'project with space'),('cyrillic',cases/'проект-кириллица'),
       ('parentheses',cases/'project(parens)'),('apostrophe',cases/"project'apostrophe"),('c-drive',Path('C:/work/og-wic-82603f8'))]
results=[]
for label,root in roots:
 assert not root.exists(),root
 run(label+'-clone',['git','clone','--no-hardlinks','--no-checkout','-c','core.autocrlf=false',SRC,root])
 run(label+'-checkout',['git','-C',root,'-c','core.autocrlf=false','checkout','--detach',PIN])
 sub=root/'own-subdir/deep';sub.mkdir(parents=True)
 denied=hook(label+'-ls-denied',entry,'ls',sub,2)
 stderr=denied.stderr.decode('utf-8')
 marker='Восстановление: '
 check(label+'-printed-recovery-present',marker in stderr,stderr)
 printed=stderr.split(marker,1)[1].splitlines()[0]
 printed_bytes=printed.encode('utf-8');(E/(label+'-printed-command.bin')).write_bytes(printed_bytes)
 hook(label+'-same-byte-hook-replay',entry,printed,sub)
 command=printed_bytes+b' && pwd -P'
 (E/(label+'-executed-command.bin')).write_bytes(command)
 actual=run(label+'-execute-printed',[BASH,'-c',command.decode('utf-8')],sub).stdout.decode('utf-8').strip()
 expected=run(label+'-root-pwd',[BASH,'-c','pwd -P'],root).stdout.decode('utf-8').strip()
 check(label+'-actual-root-equality',actual==expected,dict(actual_pwd=actual,expected_pwd=expected,method='both values from native Git Bash pwd -P, never Windows Path(/c/...).resolve()'))
 check(label+'-entry-bytes',sha((root/'.claude/settings.json').read_bytes())==sha(settings),'exact managed settings bytes')
 results.append(dict(case=label,root=str(root),source=PIN,printed=printed,printed_sha256=sha(printed_bytes),actual_pwd=actual,expected_pwd=expected,result='PASS'))
save('c1-result',dict(result='PASS',source=PIN,entry_sha256=sha(entry.encode()),settings_sha256=sha(settings),cases=results,
 method='native Windows subprocess [Git bash.exe,-c,exact entry], full UTF-8 JSON; exact printed bytes replayed then executed; actual pwd -P compared to independent same-tool root pwd'))
print(json.dumps(dict(result='PASS C1',cases=len(results),source=PIN)))
