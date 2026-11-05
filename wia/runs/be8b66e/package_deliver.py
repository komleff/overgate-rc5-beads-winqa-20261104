from common import *
import datetime,platform,zipfile,io
assert not (E/'STOP.json').exists(),'actual unresolved STOP remains'
rows=json.loads((E/'results.json').read_bytes());binding=json.loads((E/'source-binding.json').read_bytes())
for item in rows:
 if item['case'] in ['native-global-rewrite','native-count-rewrite'] and 'initial backslash/forward-slash' not in item['method']:
  item['method']+='; initial backslash/forward-slash locator mismatch did not establish effective rewrite; see separate fresh native-effective cases for actual security qualification'
if not any(x['case']=='authenticated GitHub HTTPS/SSH push' for x in rows):
 rows += [dict(case='authenticated GitHub HTTPS/SSH push',ac='auth boundary',result='NOT RUN',method='Explicitly outside packet; native synthetic repo-local helper and local bare transport tested separately',evidence='auth-helper-result.json'),dict(case='WI-B partial-init recovery / final rc.5 acceptance',ac='separate packet',result='NOT RUN',method='Not authorized by this WI-A security packet',evidence='source-binding.json')]
save('results',rows)
native={p.name:json.loads(p.read_bytes()) for p in E.glob('native-*-result.json')}
save('native-publication-summary',native)
save('environment',dict(role='Windows QA',model='Codex GPT-6',time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),os=platform.platform(),python=sys.version,BD_BIN=str(BD),bd_sha256=sha(BD.read_bytes()),runtime_source=PIN))
for n,args in [('git-version',['git','--version']),('bash-version',[BASH,'--version']),('python-version',[sys.executable,'--version']),('node-version',['node','--version'])]:
 if not (E/(n+'.json')).exists():run(n,args)
assert git('final-source-head',['rev-parse','HEAD'],S).decode().strip()==PIN
assert not git('final-source-clean',['status','--porcelain'],S).strip()
table='\n'.join('| '+x['case']+' | '+x['ac']+' | '+x['method'].replace('|','/')+' | '+x['result']+' | [receipt](evidence/'+x['evidence']+') |' for x in rows)
native_table='\n'.join('| '+name.removesuffix('-result.json')+' | '+x['actual_id']+' | '+x['target_fixture_head']+' | '+x['published_sha']+' | null |' for name,x in native.items())
report=f'''# WINDOWS QA → PM / WI-A security affected `be8b66e`

Role/model: Windows QA / Codex GPT-6. Exact source `{PIN}`, base `{BASE}`.
Tree `74dfe1d3ae58b2d81a6e08c1ec7841e1ef51cb00`; full 41-path + 1255-byte CONTRACT Content-Fingerprint `{binding['content_fingerprint']}`. CONTRACT SHA256 `{binding['contract_sha256']}`.
Authority: PR12 [RUN 6645719035](https://github.com/komleff/overgate/pull/12#issuecomment-6645719035), WI-A AC6/AC9, named wrong-remote/legacy downgrade/authorized writer risks.

**Result: PASS scoped for the completed B1/B2/B3 security and auth surfaces; named NOT RUN retained. No actual product FAIL observed.**

Tested paths: scripts/bd-apply-intents.sh, bd-bootstrap.sh, bd-publisher-setup.mjs, bd-wt.sh, bd-sync-common.sh, bd-sync-export.sh, bd-sync-restore.sh, bd-read.sh, lib/bd-env.sh, lib/bd-git-environment.mjs, and invoked managed imports (all under scripts/). Exact full package/source binding and every copied runtime file SHA256 are recorded.

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
{table}

## Native actual publication receipts

Each native row used its own independently initialized disposable project, qualified native bd1.2.2, explicit synthetic task/title/actor, trusted local identity/helper, real+attacker bare and primary/publisher/peer clones. Every claim was confirmed, every full peer object equalled the published snapshot with the same R SHA, and every attacker task ref stayed absent with complete attacker file hashes unchanged. COUNT/PARAMETERS cases exercise the exact remote URL/pushurl inputs; final effective COUNT rewrite/GLOBAL rows additionally prove raw Git fetch+push URLs resolve to attacker before candidate code sanitizes them. The two earlier rewrite rows remain baseline evidence, not effective-rewrite qualification.

| Input | Real task ID | Synthetic target code SHA | Published R = real R = peer R | Attacker R |
|---|---|---|---|---|
{native_table}

## Evidence boundaries and QA fixture corrections

1. Initial source/package and original neutral fixture were checked before any candidate execution: real/attacker same main, task refs absent, no DB/queue/receipts, true clone origins. The exact immutable preflight receipt is included. Original prepared COUNT fixture was then used by the authorized run; other native cases came from the immutable neutral main bundle, not from a mutated prior publication. The old public65f21ed and preparation archives remain immutable.
2. B1 strong downgrade evidence is in eight **b1-effective** cases: before candidate execution, unmodified native Git demonstrably sees true real managed R without override and empty attacker with COUNT/GLOBAL URL rewrite. Fresh unregistered clones have no cached task ref. Candidate wt/export/restore/bootstrap then refuse against true real origin; no task/init/export/import call, no DB/queue; real/attacker bytes and local task/config/index/hooks unchanged. Read-only fetch/object/ref cache changes are listed explicitly and are not labelled task mutations.
3. Original B1 raw fetch probes were not redirected: Git multivalue URL semantics and Windows locator backslash/forward-slash framing invalidated the effective attack precondition. These inputs provide baseline guard coverage only. Dedicated fresh normalized-locator cases establish effective spoof; none is silently claimed as an effective attack. Initial four bootstrap invocations used an absolute backslash script operand, which misframed BASH_SOURCE before security preflight; those are **NOT RUN** security cases. Fresh relative `bash scripts/bd-bootstrap.sh` fixtures contain exact launcher+manifest and reach the intended remote-state STOP. Bootstrap's safe synthetic `bd --version` probe is separated from forbidden task/init/import/export calls.
4. The first B2 QA assertion wrongly treated tracked source `.beads/config.yaml` and metadata as a live DB. Actual shell RC6/no fake Node and full before/after hashes were already captured. Read-only postprocessing corrected that assertion without repeating the native call, retaining QA-HARNESS-STOP and the original raw streams. Unstaged and staged dirty sanitizer cases both stop before Node; original saved bytes/index were explicitly restored in disposable clones.
5. Missing identity uses actual setup CLI. Missing HTTPS helper uses the exact candidate exported preflight API with synthetic HTTPS origin and no external network; actual native Git credential fill selects only the synthetic repo-local helper under candidate clean env. Actual authenticated GitHub HTTPS/SSH push is NOT RUN. Native publication transport is local bare Git. No real credential value was used.

All native stdout/stderr were captured as bytes before display decoding; receipts retain exact argv/cwd/overrides/exit and hashes. Complete target/Git/remote before-after hash maps, queues, source binding, setup plans and frozen control runtime artifacts are included. No product fix, working checkout/DB/hooks/settings, merge/release/finalize, WI-B partial-init recovery or final rc.5 acceptance was performed. Native processes ended after the bounded run; next scope belongs to PM.
'''
(R/'REPORT.md').write_text(report,encoding='utf-8')
repo=Path('D:/CodexArtifacts/overgate-rc5-beads-winqa-20261104/evidence-repo');sub='wia/runs/be8b66e';dest=repo/sub;assert not dest.exists();dest.mkdir(parents=True)
for p in R.iterdir():
 if p.is_file() and (p.suffix in ['.py','.mjs','.config'] or p.name in ['pr-contract.txt','REPORT.md'] or p.name.endswith('-setup.plan.json')):shutil.copyfile(p,dest/p.name)
for n in ['evidence','queues']:shutil.copytree(R/n,dest/n)
for p in R.glob('*-setup.plan.json.artifacts'):shutil.copytree(p,dest/p.name)
inputs=dest/'spy-inputs';inputs.mkdir()
for p in (C/'b1').iterdir():
 if p.is_dir() and p.name.endswith('-fake'):shutil.copytree(p,inputs/p.name)
for p in (C/'b2-auth').iterdir():
 if p.is_dir() and p.name.endswith('-node'):shutil.copytree(p,inputs/p.name)
 elif p.is_file() and (p.name.startswith('synthetic-') or p.name.endswith('.config')):shutil.copyfile(p,inputs/p.name)
def deliver_git(*a):return subprocess.check_output(['git',*a],cwd=repo,stderr=subprocess.STDOUT)
print(deliver_git('switch','-c','qa/wia-env-be8b66e-20261105').decode(),flush=True)
deliver_git('-c','core.autocrlf=false','add','--',sub);deliver_git('commit','-q','-m','evidence: Windows be8b66e native Git env security and auth QA')
head=deliver_git('rev-parse','HEAD').decode().strip();z=zipfile.ZipFile(io.BytesIO(deliver_git('-c','core.autocrlf=false','archive','--format=zip',head+':'+sub)));names=[n for n in z.namelist() if not n.endswith('/')];bad=[n for n in names if z.read(n)!=(dest/n).read_bytes()];assert not bad,bad
print(json.dumps(dict(commit=head,files=len(names),byte_mismatches=len(bad),pass_rows=sum(x['result']=='PASS' for x in rows),not_run_rows=sum(x['result']=='NOT RUN' for x in rows))),flush=True)
print(deliver_git('-c','http.version=HTTP/1.1','push','--porcelain','-u','origin','HEAD').decode(),flush=True)
(R/'delivery.json').write_text(json.dumps(dict(commit=head,files=len(names),byte_mismatches=0,path=sub),indent=2)+'\n',encoding='utf-8')
