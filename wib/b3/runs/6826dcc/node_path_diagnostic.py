from common import *
root=C/"Проект's (QA) space";roles={r:root/r for r in ['primary','publisher','peer']};before={r:files(p) for r,p in roles.items()}
probe_root=R/'read-only-probe'/"Проект's (QA) space";probe_root.mkdir(parents=True)
probe=probe_root/'probe.mjs';probe.write_text('console.log(JSON.stringify({diagnosticOnly:true,candidateImported:false}));\n',encoding='utf-8')
msys=run('node-path-diagnostic-cygpath',[BASH,'-c','cygpath -u "$1"','qa-diagnostic',probe.as_posix()]).stdout.decode().strip()
bad=run('node-path-diagnostic-msys',[BASH,'-c','node "$1"','qa-diagnostic',msys],expected=None)
good=run('node-path-diagnostic-native',[BASH,'-c','node "$1"','qa-diagnostic',probe.as_posix()])
assert json.loads(good.stdout)['candidateImported'] is False
after={r:files(p) for r,p in roles.items()};assert before==after
save('node-path-diagnostic-result',dict(method='independent inert Node module under separate owned diagnostic path; no candidate module imported, no source activation/bootstrap/transaction replay',msys_operand=msys,native_operand=probe.as_posix(),msys_exit=bad.returncode,native_exit=good.returncode,probe_sha256=sha(probe.read_bytes()),failed_fixture_all_bytes_unchanged=True,conclusion='inert absolute MSYS Node operand fails but actual native operand succeeds' if bad.returncode else 'both inert operand forms succeed; nested failure cause not established'))
print(json.dumps(dict(msys_exit=bad.returncode,native_exit=good.returncode,failed_fixture_unchanged=True)))
