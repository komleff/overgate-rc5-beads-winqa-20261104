from common import *
import datetime,platform,zipfile,io
assert (E/'STOP.json').is_file()
state=json.loads((E/'complex-installed-activation-state.json').read_bytes());binding=json.loads((E/'source-binding.json').read_bytes());actual=json.loads((E/'complex-installed-activation.json').read_bytes());diag=json.loads((E/'read-only-encoding-diagnostic.stdout.bin').read_bytes())
assert actual['exit_code']==1 and 'trusted root mismatch' in actual['stderr']
assert diag['utf8_path_equals_root'] and not diag['default_text_path_equals_root'] and diag['preferred_encoding']=='cp1251'
primary=C/"Проект's (QA) space"/'primary';proof={}
for name in ['scripts/bd-activate.sh','scripts/bd-activate.py','.claude/tools/run-python.sh']:
 proof[name]=dict(installed_exists=(primary/name).is_file(),installed_sha256=sha((primary/name).read_bytes()),source_sha256=sha((S/name).read_bytes()));assert proof[name]['installed_sha256']==proof[name]['source_sha256']
save('existing-installed-source-proof',proof)
frozen=json.loads((PREP/'evidence/prep-ready.json').read_bytes());drift=[]
for name,case in frozen['cases'].items():
 for role in ['real','attacker']:
  if files(Path(case[role]['path']))!=case[role]['files']:drift.append(name+'/'+role)
 for role,data in case['clones'].items():
  if files(Path(data['root']))!=data['files']:drift.append(name+'/'+role)
assert not drift;save('original-seven-slots-preserved',dict(all_frozen_bytes_equal=True,cases=7,clones=21,drift=drift))
rows=json.loads((E/'results.json').read_bytes())
for name in ['origin-drift negative after peer-init','positive same-origin after-peer-init resume','after-publisher-setup resume','after-bootstrap resume','after-push resume','pre-init missing identity','pre-init no HTTPS helper','wrong-remote COUNT','create-claim-update-close peer lifecycle','B4 / authenticated GitHub HTTPS SSH']:
 rows.append(dict(case=name,ac='B3 / boundary',result='NOT RUN',method='Stopped at first actual product FAIL on fresh required complex-path case; no further candidate execution',evidence='complex-installed-activation-state.json'))
save('results',rows)
for n,args in [('git-version',['git','--version']),('bash-version',[BASH,'--version']),('python-version',[sys.executable,'--version']),('node-version',['node','--version'])]:run(n,args)
save('environment',dict(role='Windows QA',model='Codex GPT-6',time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),os=platform.platform(),python=sys.version,native_bd_sha256=sha(BD.read_bytes()),native_bd_runtime='version-only; candidate init/qualification not reached'))
table='\n'.join('| '+x['case']+' | '+x['ac']+' | '+x['method']+' | '+x['result']+' | [receipt](evidence/'+x['evidence']+') |' for x in rows)
report=f'''# WINDOWS QA → PM / QA EXECUTION WI-B B3 `c6ab0ff` — FAIL / STOP

Role/model: Windows QA / Codex GPT-6. Source `{PIN}`, tree `1122c8fd8426fe7635526dc1ab1f38f570c6aba8`, base `{BASE}`.
Full 25-path + 1024-byte CONTRACT Content-Fingerprint `{binding['content_fingerprint']}` independently matched. Synthetic installed target main `{state['target']}`. Authority PR12#6647695601; preliminary FAIL/STOP PR12#6647775117.

**Actual native public installed activation FAIL RC1: `STOP: trusted root mismatch`.** The previous source80071dd RC2 path-to-script error is closed: public relative `bash scripts/bd-activate.sh` now enters Python successfully. In fresh root `{state['literal_root']}`, activation stops in trusted-root check before CLI/init/control/queue/task operations. Source/installed entry, Python script and integrated launcher are present and byte-identical, [proof](evidence/existing-installed-source-proof.json). Actual raw stdout/stderr/argv/cwd/RC in [receipt](evidence/complex-installed-activation.json), raw stderr SHA256 `{actual['stderr_sha256']}`.

**Read-only cause evidence:** no candidate module or activation was imported/replayed. A separate isolated native Python `-I -B` probe performed only `git rev-parse --show-toplevel`, capturing bytes and default text output. Git emits the actual path in UTF8: UTF8-decoded path equals actual root. Native Python reports utf8_mode=0, preferred encoding **cp1251**; subprocess default text decoding corrupts the Cyrillic path and that decoded path does not equal root. [Native diagnostic/raw hex and both decoded strings](evidence/read-only-encoding-diagnostic.json), [diagnostic stdout JSON](evidence/read-only-encoding-diagnostic.stdout.bin). Full target bytes remained equal after the read-only probe. Candidate `bd-activate.py call()` uses `capture_output=True,text=True` without explicit encoding, and `trusted()` constructs Path from that text.

Initial SHA/tree/fingerprint plus all7 frozen slots/21 clones passed before execution. One further fresh complex-path project was created from the immutable neutral main bundle; actual installer plan/apply delivered managed-v1/byte-exact closure with no DB. Synthetic approval is disposable-test input only. The exact allowlisted payload/state was committed and promoted only in local disposable target main, then real/attacker main mirrored and peer/publisher updated. No working checkout or real PR merge.

**Preservation:** complete before/after primary/publisher/peer/Git/real/attacker hashes equal; real task R=null, attacker R=null, peer task ref absent; all local DB absent, private activation work/queue/checkpoint absent. [Exact state](evidence/complex-installed-activation-state.json). Seven original PREP slots remain byte-identical, [readback](evidence/original-seven-slots-preserved.json). Old80071dd FAIL fixture/archive unchanged. No task ID/publication SHA; native bd.exe qualification/init not reached (version/hash preflight only).

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
{table}

Git2.51.2.windows.1 / Git Bash5.2.37 / Python3.14.0 C:/Python314/python.exe / Node24.11.0. Scoped actual bd.exe1.2.2 SHA256 `b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de` verified. Source code not changed; no direct-Python activation workaround, forced UTF8 product override, native activation retry, init/store deletion, queue reset or repaired source. Only QA-driver stdout/stderr rendering was made UTF8-safe between source packets; the product public entry still runs its own `-I -B` interpreter. An initial shell-quoting attempt to launch the **read-only diagnostic** failed before it ran; the diagnostic was then invoked through an explicit QA script. No extra candidate invocation.

Remaining B3 lifecycle, origin-drift and all fault/resume negatives NOT RUN after first actual FAIL. B4/real authenticated HTTPS/SSH OUT. Working Tune-Heroes/U2/OverGate DB/hooks/settings untouched; merge/release/finalize not performed. Raw native streams captured before decoding, full source binding, installer plans/synthetic approval, before-after hashes and STOP preserved. Native worker ended; await new exact-SHA affected packet while PR monitor stays active.
'''
(R/'REPORT.md').write_text(report,encoding='utf-8')
repo=Path('D:/CodexArtifacts/overgate-rc5-beads-winqa-20261104/evidence-repo');sub='wib/b3/runs/c6ab0ff';dest=repo/sub;assert not dest.exists();dest.mkdir(parents=True)
for p in R.iterdir():
 if p.is_file() and (p.suffix=='.py' or p.name in ['pr-contract.txt','REPORT.md']):shutil.copyfile(p,dest/p.name)
for n in ['evidence','plans']:shutil.copytree(R/n,dest/n)
for n in proof:
 target=dest/'source-evidence'/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/n,target)
def dg(*args):return subprocess.check_output(['git',*args],cwd=repo,stderr=subprocess.STDOUT)
print(dg('switch','-c','qa/wib-b3-c6ab0ff-fail-20261105').decode(),flush=True)
dg('-c','core.autocrlf=false','add','--',sub);dg('commit','-q','-m','evidence: Windows c6ab0ff trusted-root cp1251 activation FAIL STOP')
head=dg('rev-parse','HEAD').decode().strip();z=zipfile.ZipFile(io.BytesIO(dg('-c','core.autocrlf=false','archive','--format=zip',head+':'+sub)));names=[n for n in z.namelist() if not n.endswith('/')];bad=[n for n in names if z.read(n)!=(dest/n).read_bytes()];assert not bad,bad
print(json.dumps(dict(commit=head,files=len(names),byte_mismatches=len(bad),result='FAIL STOP')),flush=True)
print(dg('-c','http.version=HTTP/1.1','push','--porcelain','-u','origin','HEAD').decode(),flush=True)
(R/'delivery.json').write_text(json.dumps(dict(commit=head,files=len(names),byte_mismatches=0,path=sub),indent=2)+'\n',encoding='utf-8')
