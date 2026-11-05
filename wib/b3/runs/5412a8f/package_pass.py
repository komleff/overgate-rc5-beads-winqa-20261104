from common import *
import datetime,platform,zipfile,io
assert not (E/'STOP.json').exists()
binding=json.loads((E/'source-binding.json').read_bytes());assert (R/'current-pr-contract.txt').read_bytes().strip()+b'\n'==(R/'pr-contract.txt').read_bytes()
rows=json.loads((E/'results.json').read_bytes());assert len(rows)==11 and all(x['result']=='PASS' for x in rows)
rows.extend([dict(case='B4 legacy/fence/migration',ac='OUT',result='NOT RUN',method='Separate packet; no legacy or real DB used',evidence='source-binding.json'),dict(case='authenticated GitHub HTTPS/SSH, full verifier/CI and final rc.5 readiness by this QA',ac='OUT',result='NOT RUN',method='Synthetic origins only; full verifier/CI/finalization belong separate PM evidence',evidence='source-binding.json')]);save('results',rows)
assert git('final-source-head',['rev-parse','HEAD'],S).decode().strip()==PIN
assert not git('final-source-clean',['status','--porcelain'],S).strip()
for n,args in [('git-version',['git','--version']),('bash-version',[BASH,'--version']),('python-version',[sys.executable,'--version']),('node-version',['node','--version'])]:run(n,args)
locale_json=json.loads(run('isolated-native-locale',[sys.executable,'-I','-B','-c','import locale,sys,json;print(json.dumps(dict(preferred=locale.getpreferredencoding(False),utf8_mode=sys.flags.utf8_mode)))']).stdout)
save('environment',dict(role='Windows QA',model='Codex GPT-6',time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),os=platform.platform(),python=sys.version,native_bd_sha256=sha(BD.read_bytes()),qualified_native_version='1.2.2',public_entry='bash scripts/bd-activate.sh',no_product_UTF8_env_override=('PYTHONUTF8' not in ENV and 'PYTHONIOENCODING' not in ENV),isolated_python_locale=locale_json))
frozen=json.loads((PREP/'evidence/prep-ready.json').read_bytes());drift=[]
for name,case in frozen['cases'].items():
 for role in ['real','attacker']:
  if files(Path(case[role]['path']))!=case[role]['files']:drift.append(name+'/'+role)
 for role,data in case['clones'].items():
  if files(Path(data['root']))!=data['files']:drift.append(name+'/'+role)
assert not drift;save('original-seven-slots-preserved',dict(all_frozen_bytes_equal=True,cases=7,clones=21,drift=drift,runtime_cases='fresh independent copies from frozen neutral bundle'))
summary={}
complex=json.loads((E/'complex-lifecycle-result.json').read_bytes());complex['target']=json.loads((E/'complex-installed-installed-binding.json').read_bytes())['target'];complex['final_R']=complex['closed_R'];summary['complex-lifecycle']=complex
for n in ['resume-peer-init','resume-publisher-setup','resume-bootstrap','resume-push','inherited-COUNT-spoof']:
 d=json.loads((E/(n+'-result.json')).read_bytes());d['final_R']=d.get('published_sha',d.get('real_R'));summary[n]=d
save('publication-summary',summary)
# Raw success checkpoints/control/config/metadata are small and self-contained; DB files stay preserved locally and have full before-after hash inventories.
pack=E/'frozen-checkpoints-controls.zip';inventory={}
with zipfile.ZipFile(pack,'w',compression=zipfile.ZIP_DEFLATED) as archive:
 def add(p,name):
  data=p.read_bytes();archive.writestr(name,data);inventory[name]=dict(sha256=sha(data),bytes=len(data),mode=p.stat().st_mode & 0o777)
 for p in (R/'activation-work').rglob('*'):
  if p.is_file():add(p,'activation-work/'+p.relative_to(R/'activation-work').as_posix())
 for case in C.iterdir():
  if not case.is_dir():continue
  for role in ['primary','publisher','peer']:
   base=case/role
   if not base.is_dir():continue
   for rel in ['.beads/metadata.json','.beads/config.yaml','.git/config','.git/index','.git/HEAD','.git/info/exclude','.overgate/install-state.json']:
    p=base/rel
    if p.is_file():add(p,case.name+'/'+role+'/'+rel)
   for rel in ['.git/overgate-bd-managed','.git/overgate-bd-publisher-control','.git/hooks']:
    folder=base/rel
    if folder.is_dir():
     for p in folder.rglob('*'):
      if p.is_file() and not p.name.endswith('.sample'):add(p,case.name+'/'+role+'/'+p.relative_to(base).as_posix())
with zipfile.ZipFile(pack) as archive:assert set(archive.namelist())==set(inventory) and all(sha(archive.read(n))==v['sha256'] for n,v in inventory.items())
save('frozen-checkpoints-controls-manifest',dict(zip_sha256=sha(pack.read_bytes()),zip_bytes=pack.stat().st_size,files=inventory,every_byte_verified=True,raw_native_DB_files='retained in local fixtures; full independent per-file before-after hashes in evidence; empty native exports/checkpoint metadata/queue/control included'))
table='\n'.join('| '+x['case']+' | '+x['ac']+' | '+x['method']+' | '+x['result']+' | [receipt](evidence/'+x['evidence']+') |' for x in rows)
pubtable='\n'.join('| '+n+' | '+v['id']+' | '+v['target']+' | '+v['final_R']+' | null |' for n,v in summary.items())
report=f'''# WINDOWS QA → PM / QA EXECUTION B3 `5412a8f` — scoped PASS

Role/model: Windows QA / Codex GPT-6. Exact source `{PIN}`, tree `d4741fe7744ea1da0bd86fba2b1b6bbbe0dff2d4`, base `{BASE}`. Full29-path+1024-byte CONTRACT Content-Fingerprint `{binding['content_fingerprint']}` independently matched; final source clean/HEAD unchanged and current GitHub CONTRACT independently read back byte-equal. Authority PR12#6649142086.

**Completed native Windows B3 packet: scoped PASS. No actual product FAIL observed on this source.** Original80071dd/c6/682 FAIL archives and partial-state ZIP remain immutable. No release/final readiness claim.

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
{table}

## Native ID and SHA receipts

| Case | Actual task ID | Synthetic installed target code SHA | Final real R = peer R | Attacker R |
|---|---|---|---|---|
{pubtable}

Every positive activation used public relative `bash scripts/bd-activate.sh`, pinned native bd1.2.2, explicit synthetic title/prefix/unique actor, installed byte-exact managed-v1 closure and exact disposable trusted main. Claims were confirmed; full peer objects equal the authoritative snapshot at the exact R SHA. The complex task was typed-updated and closed with Unicode description preserved; public installed bd-read also used a TMPDIR with Cyrillic/space/parentheses/apostrophe to exercise reader/check and snapshot path conversion without direct Node bypass. The actual isolated interpreter still reports `{locale_json}`; no PYTHONUTF8/PYTHONIOENCODING product override was supplied.

Origin-drift negative is separate from positive same-origin peer-init resume: after injected peer-init, a new attacker bare was cloned from the real same-main/no-R origin and all three local fetch/push URLs changed. Same-args --resume returned the expected origin-changed STOP **before** further DB/control/queue/journal/remote write; all bytes remained equal, both R absent. The negative fixture remains retained with its injected origins and was not reset for a positive run. Four other independent projects each covered one positive interruption after peer-init/setup/bootstrap/push. Same raw queue file/bytes/inode, actor/binary/journal bound fields and native metadata/store directory identities survived resume; HEAD/index/install-state preserved. Each completed with exactly one task. After-push R stayed identical, not rolled back or republished.

Missing identity and synthetic HTTPS helper cases used the actual public activation entry. For HTTPS, only all three push destinations were synthetic HTTPS while fetch stayed the local real bare, so no external authenticated network was attempted. Both returned actionable STOP before bd init/control/task write; private queue/journal remained queued. COUNT URL/pushurl probe first proved unsanitized native Git would select attacker push URL, while activation published only to real and peer, with attacker full-byte snapshot unchanged.

All runtime cases were new independent copies from the immutable neutral bundle; all seven original PREP slots/21 clones still byte-identical. Installer approvals and target-main promotions are synthetic test inputs/actions only, not real operator/PR approvals or merges. Every source/target closure, task ref, native raw argv/cwd/env/RC, before-after Git/DB/control file hash and public peer snapshot is retained. Raw success work/queues/checkpoints/setup/control/config/metadata are in frozen-checkpoints-controls.zip with per-file hash manifest; raw DB files remain intact in the local fixtures and have independent complete file hash inventories. No cleanup/re-init/delete or replay of prior failed stores.

**QA-only correction:** after the first intended peer-init fault, a directory-inode assertion assumed `.beads/dolt`; actual metadata states embedded and native bd1.2.2 uses `.beads/embeddeddolt`. QA-HARNESS-STOP is preserved. The already captured fault checkpoint/targets/work were hash-verified unchanged, and the QA driver continued from that checkpoint without repeating its native fault invocation or changing product code. Store path now derives from native metadata. This was not a product FAIL or a reset.

Native environment: Git2.51.2.windows.1 / Git Bash5.2.37 / Python3.14.0 C:/Python314/python.exe / Node24.11.0; qualified Windows bd.exe1.2.2 SHA256 `b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de`. No full local verifier/CI/finalizer executed by this QA; PM's checks are separate. B4 legacy/fence/migration, real authenticated GitHub HTTPS/SSH and full rc.5 readiness NOT RUN here. Working Tune-Heroes/U2/OverGate checkouts/DB/hooks/settings untouched. Native workers exited, PR monitor remains active awaiting next bounded scope.
'''
(R/'REPORT.md').write_text(report,encoding='utf-8')
repo=Path('D:/CodexArtifacts/overgate-rc5-beads-winqa-20261104/evidence-repo');sub='wib/b3/runs/5412a8f';dest=repo/sub;assert not dest.exists();dest.mkdir(parents=True)
for p in R.iterdir():
 if p.is_file() and (p.suffix=='.py' or p.name in ['pr-contract.txt','current-pr-contract.txt','REPORT.md']):shutil.copyfile(p,dest/p.name)
for n in ['evidence','plans']:shutil.copytree(R/n,dest/n)
def dg(*args):return subprocess.check_output(['git',*args],cwd=repo,stderr=subprocess.STDOUT)
print(dg('switch','-c','qa/wib-b3-5412a8f-pass-20261105').decode(),flush=True)
dg('-c','core.autocrlf=false','add','--',sub);dg('commit','-q','-m','evidence: Windows 5412a8f installed B3 lifecycle and recovery scoped PASS')
head=dg('rev-parse','HEAD').decode().strip();z=zipfile.ZipFile(io.BytesIO(dg('-c','core.autocrlf=false','archive','--format=zip',head+':'+sub)));names=[n for n in z.namelist() if not n.endswith('/')];bad=[n for n in names if z.read(n)!=(dest/n).read_bytes()];assert not bad,bad
print(json.dumps(dict(commit=head,files=len(names),byte_mismatches=len(bad),result='scoped PASS',native_publications=summary)),flush=True)
print(dg('-c','http.version=HTTP/1.1','push','--porcelain','-u','origin','HEAD').decode(),flush=True)
(R/'delivery.json').write_text(json.dumps(dict(commit=head,files=len(names),byte_mismatches=0,path=sub),indent=2)+'\n',encoding='utf-8')
