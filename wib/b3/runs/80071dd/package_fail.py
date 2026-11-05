from common import *
import datetime,platform,zipfile,io
assert (E/'STOP.json').is_file()
primary=C/"Проект's (QA) space"/'primary'
proof={}
for name in ['scripts/bd-activate.sh','scripts/bd-activate.py','.claude/tools/run-python.sh']:
 proof[name]=dict(installed_exists=(primary/name).is_file(),installed_sha256=sha((primary/name).read_bytes()),source_sha256=sha((S/name).read_bytes()))
 assert proof[name]['installed_sha256']==proof[name]['source_sha256']
save('existing-installed-launcher-proof',dict(source=PIN,actual_primary=str(primary),files=proof,inference='bd-activate shell supplies -I -B before absolute MSYS script path; run-python normalizes only argument1, which is -I; raw native RC2 shows D:/d path, although actual file exists. No replay or source modification.'))
frozen=json.loads((PREP/'evidence/prep-ready.json').read_bytes());drift=[]
for name,case in frozen['cases'].items():
 for role in ['real','attacker']:
  if files(Path(case[role]['path']))!=case[role]['files']:drift.append(name+'/'+role)
 for role,data in case['clones'].items():
  if files(Path(data['root']))!=data['files']:drift.append(name+'/'+role)
assert not drift;save('original-seven-slots-preserved',dict(all_frozen_bytes_equal=True,cases=7,clones=21,drift=drift))
rows=json.loads((E/'results.json').read_bytes())
for name in ['standalone ASCII happy lifecycle','after-peer-init resume','after-publisher-setup resume','after-bootstrap resume','after-push resume','pre-init missing identity','pre-init no HTTPS helper','wrong-remote COUNT','update-close peer lifecycle','resume-origin drift reviewer case','B4 / authenticated GitHub HTTPS SSH']:
 rows.append(dict(case=name,ac='B3 / explicit boundary',result='NOT RUN',method='Stopped at first actual product FAIL; PM PAUSE also received; no further candidate execution',evidence='complex-installed-activation-state.json'))
save('results',rows)
for n,args in [('git-version',['git','--version']),('bash-version',[BASH,'--version']),('python-version',[sys.executable,'--version']),('node-version',['node','--version'])]:run(n,args)
save('environment',dict(role='Windows QA',model='Codex GPT-6',time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),os=platform.platform(),python=sys.version,native_bd_sha256=sha(BD.read_bytes()),native_bd_runtime='version-only; candidate qualification/init not reached'))
state=json.loads((E/'complex-installed-activation-state.json').read_bytes());binding=json.loads((E/'source-binding.json').read_bytes());actual=json.loads((E/'complex-installed-activation.json').read_bytes())
table='\n'.join('| '+x['case']+' | '+x['ac']+' | '+x['method']+' | '+x['result']+' | [receipt](evidence/'+x['evidence']+') |' for x in rows)
report=f'''# WINDOWS QA → PM / QA EXECUTION WI-B B3 `80071dd` — FAIL / STOP

Role/model: Windows QA / Codex GPT-6. Source `{PIN}`, tree `96346205f076398cf6e37340e1a3e0d661588442`, base `{BASE}`.
Content-Fingerprint `{binding['content_fingerprint']}` (25 sorted paths + exact1024-byte CONTRACT; independent match). Synthetic installed target main `{state['target']}`. Authority: PR12#6647173036; superseding PAUSE PR12#6647225874 acknowledged in PR12#6647281879.

**Actual FAIL: public installed `bash scripts/bd-activate.sh ...` returned RC2 in required combined Windows path.** Native Python tried `D:\\d\\CodexArtifacts\\...\\scripts\\bd-activate.py` instead of existing `D:\\CodexArtifacts\\...\\scripts\\bd-activate.py`. Root literal: `{state['literal_root']}`. The current native working directory, exact argv/actor/title/path, raw stderr bytes and exit are frozen in [activation receipt](evidence/complex-installed-activation.json). Raw stderr SHA256 `{actual['stderr_sha256']}`. The launcher and activation scripts are present and byte-identical to exact source, with hashes in [installed-file proof](evidence/existing-installed-launcher-proof.json).

Source call-site evidence: `scripts/bd-activate.sh` passes `-I -B` before absolute MSYS script operand. Integrated `.claude/tools/run-python.sh` normalizes only argv1 when it starts with `/`; argv1 here is `-I`. This is a new public call-surface failure with existing launcher bytes. No product edit, direct-Python workaround, alternate invocation or native activation retry was used.

Preflight source/fingerprint and **all seven frozen original slots** passed before execution. A further fresh disposable complex-path project was created from the immutable neutral bundle; actual installer plan/apply delivered managed-v1 closure with no DB. Installer approval was synthetic test input only. Exact operation allowlist was committed on the install branch and promoted only to disposable target main, with real/attacker main mirrors and standalone publisher/peer at the same target code SHA. No GitHub PR merge or working checkout was involved.

After the first native FAIL, the run stopped. **Complete target/Git + real + attacker before-after hashes equal**, real_R=null, attacker_R=null, peer task ref absent. All three local DBs absent; activation work/queue/checkpoint absent. [Exact state/ref receipt](evidence/complex-installed-activation-state.json). Seven original prepared fixtures remain byte-identical to frozen preparation, [preservation readback](evidence/original-seven-slots-preserved.json). Thus none of the four interruption slots or pre-init negatives was used. Native bd1.2.2 hash was verified, but candidate CLI qualification/init/publication never began.

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
{table}

Evidence includes original raw stdout/stderr captured before decoding, every argv/cwd/exit/hash, source binding, frozen installer plan/approval, complete before-after file maps, existing-file/source proofs and STOP traceback. The QA driver's later traceback rendering hit CP1251 UnicodeEncodeError while printing the already captured native error; this is a secondary QA output issue. Native receipt/raw streams/state/FAIL/STOP JSON were already written in UTF8 and remain intact. It does not change native RC2 or its diagnosis.

Git2.51.2.windows.1 / Git Bash5.2.37 / Python3.14.0 C:/Python314/python.exe / Node24.11.0; scoped bd.exe1.2.2 SHA256 `b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de` (version-only). Actual new task ID/publication SHA N/A. B3 recovery/security/lifecycle remaining NOT RUN; B4 and real authenticated HTTPS/SSH OUT. Source checkout not changed; working Tune-Heroes/U2/OverGate DB/hooks/settings untouched; no merge/release/finalize. Worker exited; preserve this source/fixture for affected recheck only after new exact packet.
'''
(R/'REPORT.md').write_text(report,encoding='utf-8')
repo=Path('D:/CodexArtifacts/overgate-rc5-beads-winqa-20261104/evidence-repo');sub='wib/b3/runs/80071dd';dest=repo/sub;assert not dest.exists();dest.mkdir(parents=True)
for name in ['common.py','preflight.py','installed.py','complex_first.py','package_fail.py','pr-contract.txt','REPORT.md']:shutil.copyfile(R/name,dest/name)
for name in ['evidence','plans']:shutil.copytree(R/name,dest/name)
source_proof=dest/'source-evidence'
for name in proof:
 target=source_proof/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/name,target)
def deliver_git(*args):return subprocess.check_output(['git',*args],cwd=repo,stderr=subprocess.STDOUT)
print(deliver_git('switch','-c','qa/wib-b3-80071dd-fail-20261105').decode(),flush=True)
deliver_git('-c','core.autocrlf=false','add','--',sub);deliver_git('commit','-q','-m','evidence: Windows 80071dd installed complex-path activation FAIL STOP')
head=deliver_git('rev-parse','HEAD').decode().strip();z=zipfile.ZipFile(io.BytesIO(deliver_git('-c','core.autocrlf=false','archive','--format=zip',head+':'+sub)));names=[n for n in z.namelist() if not n.endswith('/')];bad=[n for n in names if z.read(n)!=(dest/n).read_bytes()];assert not bad,bad
print(json.dumps(dict(commit=head,files=len(names),byte_mismatches=len(bad),result='FAIL STOP')),flush=True)
print(deliver_git('-c','http.version=HTTP/1.1','push','--porcelain','-u','origin','HEAD').decode(),flush=True)
(R/'delivery.json').write_text(json.dumps(dict(commit=head,files=len(names),byte_mismatches=0,path=sub),indent=2)+'\n',encoding='utf-8')
