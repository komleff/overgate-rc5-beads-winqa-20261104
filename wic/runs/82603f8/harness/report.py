from native_common import *
import sys
fp=json.loads((E/'source-fingerprint.json').read_text(encoding='utf-8'));contract=(R/'pr-contract.txt').read_bytes()
blobs={p:decode(run('fp-blob-'+str(i),['git','-C',SRC,'rev-parse',PIN+':'+p]).stdout).strip() for i,p in enumerate(sorted(fp['files']))}
fingerprint=sha(''.join(p+' '+v+'\n' for p,v in blobs.items()).encode()+contract)
check('expected-source-fingerprint',fingerprint=='013e5ba8cf82940f1732e5c82aa6e294b36ea35d15ac9c1ef19d985f1e744302',fingerprint)
save('source-contract-fingerprint',dict(source=PIN,content_fingerprint=fingerprint,contract_bytes=len(contract),contract_sha256=sha(contract),plan_blob='e56ec8ff7f49e4a85483140ea811dabd42d6de5e',blobs=blobs))
matrix=json.loads((E/'c1-result.json').read_text(encoding='utf-8'));apos=next(x for x in matrix['cases'] if x['case']=='apostrophe')
file=Path(apos['root'])/'.claude/hooks/check-repository-mutation.py'
save('root-failure-context',dict(source=PIN,case='ci-apostrophe-root-read',root=apos['root'],independent_pwd=apos['actual_pwd'],expected_pwd=apos['expected_pwd'],
 actual_guard_file_exists=file.is_file(),actual_guard_file_sha256=sha(file.read_bytes()),source_guard_file_sha256=sha((SRC/'.claude/hooks/check-repository-mutation.py').read_bytes()),
 interpretation='actual hook invocation returns2; native Python tries D:\\d\\... rather than existing D:\\... guard; no Windows Path.resolve comparison involved'))
run('inventory-git',['git','--version']);run('inventory-bash',[BASH,'--version'])
save('inventory-python',dict(executable=sys.executable,version=sys.version))
save('stop-scope',dict(source=PIN,result='FAIL',case='apostrophe root git log through dispatcher',expected_exit=0,actual_exit=2,
 pass_scoped=['exact prior DOS/MSYS alias case in original failed directory','printed same-byte hook replay and actual execution','six-root C1 native matrix'],
 not_run=['spoofed-GIT_DIR/GIT_WORK_TREE own quoted DOS case','new-source C2 sweep','remaining C3/C4 root/outside cases','installer auto/bypass upgrade/custom managed hook conflict','full verifier/live Claude'],
 C5='NOT RUN by Windows; PM permits content-equivalent prior Mac/CI evidence; no inference of Windows runtime PASS',reason='first actual native root-read FAIL -> STOP'))
report='''# Windows QA EXECUTION — WI-C 82603f8 FAIL

Role/model: Windows QA / Codex GPT-6. Source `{source}`.
Full 16-path+contract fingerprint `{fingerprint}`.
Plan blob e56ec8ff7f49e4a85483140ea811dabd42d6de5e;
contract 1060 bytes / SHA256 118a2da8d515cbd809293a8379ecafa7f536b401e419619a521fe76ed36d45a6.

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
| Exact prior failed directory, DOS/MSYS same-root aliases | C1/C3/P3 | New exact settings blob in original failed fixture; old settings bytes backed up, other runtime helper bytes match new source; both commands RC0 | PASS scoped | evidence/exact-old-case-result.json; original-failed-fixture-settings.bin |
| Printed hint replay and real execution | C1 | Exact printed bytes through same hook then actual Bash execution/pwd | PASS | exact-old-printed-*.json/bin |
| C1 six-root matrix | C1 | Native Windows full UTF-8 JSON, ASCII/space/Cyrillic/parentheses/apostrophe/C-drive; printed bytes replayed and executed, independent native pwd matches | PASS 6/6 scoped | evidence/c1-result.json; each *-execute-printed.json, *-root-pwd.json |
| Read command after recovery in apostrophe root | C3/P3 | Native exact entry, payload git log -1 --oneline, actual root cwd | **FAIL**, expected0/actual2 | evidence/ci-apostrophe-root-read.payload.json; .json; .stderr.bin |
| Spoofed Git env own quoted DOS recovery, remaining C2–C4 and installer | C1–C4/C6 | Not reached after first FAIL | NOT RUN | evidence/stop-scope.json |
| C5 names | C5 | Not executed by Windows; PM allows prior content-equivalent Mac/CI | NOT RUN by Windows | packet 6641446269 |

Failing cwd: `{root}`. Independent native pwd: `{pwd}`.
Python stderr names D:\\d\\CodexArtifacts\\...\\project'apostrophe\\.claude\\hooks\\check-repository-mutation.py.
The real guard exists under D:\\CodexArtifacts\\..., and its SHA256 equals the candidate
file; file existence/hash and independent pwd are recorded. Thus this is an actual
dispatcher-to-native-Python script-path failure, independently confirming the first
new CI finding. The second spoofed-Git-env finding remains NOT RUN, not inferred FAIL/PASS.

The original da8b92e FAIL stays immutable. Only its explicitly authorized disposable
ASCII fixture received new settings for exact affected repro; its old settings bytes
are retained here. Source snapshot and all six new checkout roots use exact 82603f8.
These are source-hook native cases, not completed installer smoke/upgrade acceptance.

Git Bash C:/Program Files/Git/bin/bash.exe 5.2.37; Git 2.51.2.windows.1;
native QA/hook Python C:/Python314/python.exe 3.14.0. Full argv, payload JSON, raw binary
stdout/stderr and printed/executed commands are preserved. No helper/env workaround,
source fix, rerun or later product case after FAIL. No working settings/hooks/DB,
merge, release or finalizer touched. WI-A frozen evidence is separate.
'''.format(source=PIN,fingerprint=fingerprint,root=apos['root'],pwd=apos['actual_pwd'])
(R/'REPORT.md').write_text(report,encoding='utf-8')
print(json.dumps(dict(result='FAIL checkpoint saved',source=PIN,content_fingerprint=fingerprint)))
