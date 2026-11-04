from native_common import *
old=Path('D:/CodexArtifacts/overgate-rc5-wic-winqa-20261105/run-da8b92e/cases/project-ascii')
sub=old/'own-subdir/deep'
settings=(SRC/'.claude/settings.json').read_bytes();before=(old/'.claude/settings.json').read_bytes()
(R/'original-failed-fixture-settings.bin').write_bytes(before)
files=[p for folder in ['hooks','tools'] for p in (SRC/'.claude'/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
check('old-fixture-runtime-byte-equivalence',all((old/p.relative_to(SRC)).read_bytes()==p.read_bytes() for p in files),dict(source=PIN,files=len(files),settings_before_sha256=sha(before),settings_new_sha256=sha(settings)))
(old/'.claude/settings.json').write_bytes(settings)
entry=next(h['command'] for x in json.loads(settings)['hooks']['PreToolUse'] if x.get('matcher')=='Bash' for h in x['hooks'])
dos='cd '+old.as_posix();msys='cd /d'+old.as_posix()[2:]
hook('exact-old-case-dos-alias',entry,dos,sub)
hook('exact-old-case-msys-alias',entry,msys,sub)
denied=hook('exact-old-case-ls-denied',entry,'ls',sub,2)
printed=denied.stderr.decode('utf-8').split('Восстановление: ',1)[1].splitlines()[0]
(E/'exact-old-printed-command.bin').write_bytes(printed.encode())
hook('exact-old-printed-hook-replay',entry,printed,sub)
actual=run('exact-old-printed-execution',[BASH,'-c',printed+' && pwd -P'],sub).stdout.decode('utf-8').strip()
expected=run('exact-old-root-independent-pwd',[BASH,'-c','pwd -P'],old).stdout.decode('utf-8').strip()
check('exact-old-actual-root',actual==expected,dict(actual=actual,expected=expected,dos=dos,msys=msys,printed=printed))
save('exact-old-case-result',dict(result='PASS',source=PIN,original_fixture=str(old),old_settings_sha256=sha(before),new_settings_sha256=sha(settings),dos=dos,msys=msys,printed=printed,actual_pwd=actual,expected_pwd=expected))
print('Exact prior failed directory: DOS/MSYS/printed execution PASS on new entry')
