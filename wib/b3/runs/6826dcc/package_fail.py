from common import *
import datetime,platform,zipfile,io
assert (E/'STOP.json').is_file()
root=C/"Проект's (QA) space";work=R/'activation-work/complex';state=json.loads((E/'complex-installed-activation-state.json').read_bytes());binding=json.loads((E/'source-binding.json').read_bytes());actual=json.loads((E/'complex-installed-activation.json').read_bytes());journal=json.loads((work/'activation-checkpoint.json').read_bytes());diag=json.loads((E/'node-path-diagnostic-result.json').read_bytes())
assert actual['exit_code']==1 and journal['stage']=='setup' and not any('beads-backup' in state['refs'][role] for role in ['real','attacker','peer'])
assert diag['msys_exit']==1 and diag['native_exit']==0 and diag['failed_fixture_all_bytes_unchanged']
before=json.loads((E/'complex-installed-before-activation.json').read_bytes());after=json.loads((E/'complex-installed-after-activation.json').read_bytes())
assert before['real']==after['real'] and before['attacker']==after['attacker']
for role in ['primary','publisher','peer']:
 for p in ['.git/HEAD','.git/index','.overgate/install-state.json']:assert before[role][p]==after[role][p]
save('partial-state-invariants',dict(source=PIN,real_attacker_remote_all_bytes_unchanged=True,all_HEAD_index_install_state_unchanged=True,journal_stage=journal['stage'],raw_queue_sha256=sha((work/'raw-intents.jsonl').read_bytes()),actor=journal['bound']['actor'],binary_sha256=journal['binary_sha256'],primary_peer_DB_present=True,publisher_DB_absent=True,first_push_occurred=False))
frozen=json.loads((PREP/'evidence/prep-ready.json').read_bytes());drift=[]
for name,case in frozen['cases'].items():
 for role in ['real','attacker']:
  if files(Path(case[role]['path']))!=case[role]['files']:drift.append(name+'/'+role)
 for role,data in case['clones'].items():
  if files(Path(data['root']))!=data['files']:drift.append(name+'/'+role)
assert not drift;save('original-seven-slots-preserved',dict(all_frozen_bytes_equal=True,cases=7,clones=21,drift=drift))
# Quiescent raw native state pack. No Git/BD/source replay, no reset or deletion.
pack=E/'frozen-partial-state.zip';inventory={}
with zipfile.ZipFile(pack,'w',compression=zipfile.ZIP_DEFLATED) as archive:
 def add(p,name):
  data=p.read_bytes();archive.writestr(name,data);inventory[name]=dict(sha256=sha(data),bytes=len(data),mode=p.stat().st_mode & 0o777)
 for p in work.rglob('*'):
  if p.is_file():add(p,'work/'+p.relative_to(work).as_posix())
 for role in ['primary','publisher','peer']:
  base=root/role
  for rel in ['.beads','.git/overgate-bd-managed','.git/overgate-bd-publisher-control','.git/overgate-bd-activation','.git/hooks']:
   folder=base/rel
   if folder.is_dir():
    for p in folder.rglob('*'):
     if p.is_file():add(p,role+'/'+p.relative_to(base).as_posix())
  for rel in ['.git/config','.git/index','.git/HEAD','.git/info/exclude','.overgate/install-state.json']:
   p=base/rel
   if p.is_file():add(p,role+'/'+rel)
with zipfile.ZipFile(pack) as archive:
 assert set(archive.namelist())==set(inventory)
 assert all(sha(archive.read(n))==data['sha256'] for n,data in inventory.items())
save('frozen-partial-state-manifest',dict(zip_sha256=sha(pack.read_bytes()),zip_bytes=pack.stat().st_size,files=inventory,verified_every_byte=True,source=PIN,stage='setup',no_source_replayed=True))
rows=json.loads((E/'results.json').read_bytes())
for name in ['origin-drift negative after peer-init','positive after-peer-init resume','after-publisher-setup resume','after-bootstrap resume','after-push resume','pre-init missing identity','pre-init no HTTPS helper','wrong-remote COUNT','full create-claim-update-close peer lifecycle','B4 / authenticated GitHub HTTPS SSH']:
 rows.append(dict(case=name,ac='B3 / boundary',result='NOT RUN',method='First actual product FAIL during complex-path bootstrap; no retry/resume or further candidate execution',evidence='complex-installed-activation-state.json'))
save('results',rows)
for n,args in [('git-version',['git','--version']),('bash-version',[BASH,'--version']),('python-version',[sys.executable,'--version']),('node-version',['node','--version'])]:run(n,args)
save('environment',dict(role='Windows QA',model='Codex GPT-6',time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),os=platform.platform(),python=sys.version,native_bd_sha256=sha(BD.read_bytes()),native_bd_runtime='qualified by public activation, native primary+peer empty embedded init reached',product_utf8_env_override=False))
table='\n'.join('| '+x['case']+' | '+x['ac']+' | '+x['method']+' | '+x['result']+' | [receipt](evidence/'+x['evidence']+') |' for x in rows)
report=f'''# WINDOWS QA → PM / QA EXECUTION B3 `6826dcc` — FAIL / STOP

Role/model: Windows QA / Codex GPT-6. Source `{PIN}`, tree `54b843d2ff2e6455f7df04148dcb1d960cd05375`, base `{BASE}`. Full25-path+1024-byte CONTRACT Content-Fingerprint `{binding['content_fingerprint']}` independently matched. Synthetic installed target main `{state['target']}`. Authority PR12#6648334066; preliminary FAIL/STOP PR12#6648428542.

**Actual public installed activation FAIL RC1:** `trusted managed apply failed (exit 1); queue/base/actor retained`. The first required fresh complex-path case progressed past previous RC2 and c6 trusted-root errors: qualified native Windows bd, empty primary+peer native init, peer registration and publisher setup completed. The private journal is retained at **stage setup**, with raw queue SHA256 `{journal['bound']['raw_sha256']}`, actor `{journal['bound']['actor']}`, binary SHA256 `{journal['binary_sha256']}`. First managed bootstrap failed before acknowledgement/prepared queue/publication. Actual public relative entry, argv/cwd/exit and raw stderr are in [receipt](evidence/complex-installed-activation.json). Literal root `{state['literal_root']}`.

The outer product Python helper captures and discards the nested managed-shell stderr, exposing only exit1. Therefore this report does not claim the discarded inner error as observed fact. A separate **inert Node path control** provides a matching native path-resolution failure: under an independent diagnostic-only path with the same required characters, `node /d/.../probe.mjs` returned1 while `node D:/.../probe.mjs` returned0, with identical inert file bytes. No candidate module imported/executed, no activation/bootstrap replay, failed fixture byte hashes unchanged. [Native diagnostic result](evidence/node-path-diagnostic-result.json), raw [MSYS stderr](evidence/node-path-diagnostic-msys.stderr.bin), [native success](evidence/node-path-diagnostic-native.json). Candidate bd-apply-intents.sh launches Node with absolute MSYS SCRIPT_DIR entry path; this source/control correspondence is a **cause inference**, not a captured inner traceback. The analogous reader path was not executed or claimed failed.

**Preserved state:** real_R=null, attacker_R=null, peer task ref absent. All real+attacker file hashes unchanged by activation. All three HEAD/index and installed state bytes unchanged. Primary+peer native stores and configs are newly initialized, publisher task store absent. Publisher/primary control/config/hooks, peer reader registration, private work/journal/raw queue and bootstrap preservation manifest are retained; do not label whole local before/after equal. No first push, task ID or publication SHA. [Exact state](evidence/complex-installed-activation-state.json), [invariants](evidence/partial-state-invariants.json).

Complete quiescent raw native DB/config/index/control/hooks/private work bytes are frozen in [partial state ZIP](evidence/frozen-partial-state.zip) with per-file SHA/mode [manifest](evidence/frozen-partial-state-manifest.json); `{len(inventory)}` files, ZIP SHA256 `{sha(pack.read_bytes())}`, every archived byte verified. Seven original reserved PREP slots remain byte-identical [readback](evidence/original-seven-slots-preserved.json); both previous source FAIL fixtures/archives unchanged. No deletion, reset, re-init, retry or resume.

Source/frozen preflight passed; actual installer plan/apply delivered managed-v1 exact closure with synthetic approval and disposable main promotion only. No direct-Python/product environment override: public shell wrapper ran its own isolated Python, and QA removed PYTHONUTF8/PYTHONIOENCODING from native child env. Native versions: Git2.51.2.windows.1, Git Bash5.2.37, Python3.14.0 C:/Python314/python.exe, Node24.11.0, qualified bd.exe1.2.2 hash `b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de`.

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
{table}

First actual product FAIL stopped all remaining B3 cases. The native init/setup progression is scoped observation, not successful activation/recovery or full B3 acceptance. B4/real authenticated GitHub HTTPS/SSH/final rc.5 OUT. Source not modified, native worker exited. Working Tune-Heroes/U2/OverGate DB/hooks/settings, merge/release/finalize untouched. Raw stdout/stderr were captured before decoding; exact source binding, plans, argv and before-after hashes retained. Await next exact-SHA affected packet while PR monitor stays active.
'''
(R/'REPORT.md').write_text(report,encoding='utf-8')
repo=Path('D:/CodexArtifacts/overgate-rc5-beads-winqa-20261104/evidence-repo');sub='wib/b3/runs/6826dcc';dest=repo/sub;assert not dest.exists();dest.mkdir(parents=True)
for p in R.iterdir():
 if p.is_file() and (p.suffix=='.py' or p.name in ['pr-contract.txt','REPORT.md']):shutil.copyfile(p,dest/p.name)
for n in ['evidence','plans']:shutil.copytree(R/n,dest/n)
for name in ['scripts/bd-activate.sh','scripts/bd-activate.py','scripts/bd-apply-intents.sh','scripts/bd-read.sh','.claude/tools/run-python.sh']:
 target=dest/'source-evidence'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/name,target)
for p in (R/'read-only-probe').rglob('*.mjs'):
 target=dest/'diagnostic-source'/p.relative_to(R/'read-only-probe');target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
def dg(*args):return subprocess.check_output(['git',*args],cwd=repo,stderr=subprocess.STDOUT)
print(dg('switch','-c','qa/wib-b3-6826dcc-fail-20261105').decode(),flush=True)
dg('-c','core.autocrlf=false','add','--',sub);dg('commit','-q','-m','evidence: Windows 6826dcc bootstrap FAIL with frozen partial native state')
head=dg('rev-parse','HEAD').decode().strip();z=zipfile.ZipFile(io.BytesIO(dg('-c','core.autocrlf=false','archive','--format=zip',head+':'+sub)));names=[n for n in z.namelist() if not n.endswith('/')];bad=[n for n in names if z.read(n)!=(dest/n).read_bytes()];assert not bad,bad
print(json.dumps(dict(commit=head,files=len(names),byte_mismatches=len(bad),result='FAIL STOP',frozen_native_files=len(inventory))),flush=True)
print(dg('-c','http.version=HTTP/1.1','push','--porcelain','-u','origin','HEAD').decode(),flush=True)
(R/'delivery.json').write_text(json.dumps(dict(commit=head,files=len(names),byte_mismatches=0,path=sub),indent=2)+'\n',encoding='utf-8')
