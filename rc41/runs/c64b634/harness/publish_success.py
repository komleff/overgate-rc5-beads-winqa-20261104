import os,sys,json,re,hashlib,shutil,subprocess,zipfile,io
from pathlib import Path
B=Path(__file__).resolve().parent;SHA='c64b634ea1b3425647b0d44323ac997bbb8b7c28';S=B/'source-c64b634';E=B/'runs/c64b634/evidence'
R=B.parent/'overgate-rc5-beads-winqa-20261104/evidence-repo';relative='rc41/runs/c64b634';D=R/relative
def cmd(args,cwd=R,input=None):
    p=subprocess.run([str(x) for x in args],cwd=cwd,input=input,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
    return p.stdout.strip()
def read(n):return json.loads((E/(n+'.json')).read_text(encoding='utf-8'))
def put(n,v):(E/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
def main():
    cases={h:read(n) for h,n in {'H1':'H1-result','H2':'H2-empty-result','H3':'H3-populated-result','H4':'H4-result','H5':'H5-result'}.items()}
    assert all(v['result']=='PASS' and v['source_sha']==SHA for v in cases.values()) and not(E/'STOP.json').exists()
    assert 'Ran 1 test' in read('H5-existing-installed-doc-fixture')['stderr'] and 'skipped' not in read('H5-existing-installed-doc-fixture')['stderr']
    source=read('H3-populated-source-data')
    for i,(iid,expected) in enumerate(source['shows'].items()):
        actual=json.loads(read('H3-populated-clone-show-'+str(i))['stdout'])[0]
        assert json.dumps(expected,sort_keys=True,ensure_ascii=False)==json.dumps(actual,sort_keys=True,ensure_ascii=False)
    assert cmd(['git','rev-parse','HEAD'],S)==SHA and not cmd(['git','status','--porcelain'],S)
    assert cmd(['gh','pr','view','15','-R','komleff/overgate','--json','headRefOid','--jq','.headRefOid'],B)==SHA
    bd=Path('D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe');bdhash=hashlib.sha256(bd.read_bytes()).hexdigest();assert bdhash=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de'
    tools=json.loads((B/'evidence/workspace-ready.json').read_text(encoding='utf-8'))['tools']
    packet=json.loads(cmd(['gh','api','repos/komleff/overgate/issues/comments/6635128301'],B));put('PM-RUN-packet',packet)
    paths=['scripts/bd-bootstrap.sh','scripts/bd-sync-common.sh','scripts/bd-sync-export.sh','scripts/bd-sync-restore.sh','scripts/lib/bd-env.sh','.claude/tools/run-python.sh','.agents/distribution-manifest.json','.agents/HOW_TO_USE.md','.claude/rules/beads.md','scripts/install-overgate.py','scripts/tests/install-distribution.test.py']
    blobs={p:cmd(['git','rev-parse',SHA+':'+p],S) for p in paths};fp=hashlib.sha256(''.join(p+' '+blobs[p]+'\n' for p in sorted(blobs)).encode()+packet['body'].encode()).hexdigest()
    put('source-fingerprint',{'source_sha':SHA,'tree':cmd(['git','rev-parse',SHA+'^{tree}'],S),'source_clean':True,'tested_paths':blobs,'contract_comment':6635128301,'fingerprint':fp,'method':'sorted path SP Git blob LF + exact PM RUN body UTF8'})
    put('final-summary',{'source_sha':SHA,'binary_path':str(bd),'binary_sha256_before_after':bdhash,'tools':tools,'cases':cases,'source_clean':True,'PR_HEAD_matches':True,'H3_strict_JSON_types_equal':True,'original_failed_run_825_preserved':True,'result':'PASS for H1-H5 scoped Windows packet; H6/H7/overall acceptance not asserted'})
    for h in ['H2','H3']:
        root=Path(cases[h]['clone']);put(h+'-final-local-refs',{'head':cmd(['git','rev-parse','HEAD'],root),'remote_refs':cmd(['git','ls-remote','--heads','origin'],root),'lastSeen':cmd(['git','config','--local','--get','beads-sync.lastSeen'],root)})
        for file in ['metadata.json','config.yaml']:(E/(h+'-preserved-'+file)).write_bytes((root/'.beads'/file).read_bytes())
    report=f'''## WINDOWS QA → PM / FINAL AFFECTED QA — c64b634

**PASS for the assigned H1–H5 Windows packet only.** Role/model: Windows QA / Codex GPT-6 (exact preset unavailable). Source/PR15 HEAD `{SHA}`, clean detached source checkout. Tested-content fingerprint `{fp}`: [paths/blobs/contract](source-fingerprint.json). Contract [RUN6635128301](https://github.com/komleff/overgate/pull/12#issuecomment-6635128301). One sequential run, first case H2 empty; all candidate cases succeeded, no retry/repair/force.

Native binary `{bd}`, bd1.2.2 (6c124203e), SHA256 before/after `{bdhash}`. Native Windows11/Git for Windows2.51.2/Git Bash5.2.37/Python3.14.0; [environment and results](final-summary.json). Codex0.154.0 availability only: no H6 live claim by Windows.

| H | PASS/FAIL/NOT RUN | Actual method | Exact evidence |
|---|---|---|---|
| H2 empty, including fresh bootstrap | PASS | New primary/bare origin; Beads-only init commit, untracked sentinel retained, actual prefixbig-heroes, active config pin committed/pushed; second clone before any issue restores empty snapshot | [case result](H2-empty-result.json), [primary call](H2-empty-primary-bootstrap.json), [clone call](H2-empty-clone-bootstrap.json) |
| H2 invariants | PASS | Export exactly0bytes; R=lastSeen; metadata/project_id/config/index/HEAD/origin refs preserved; no Dolt remote | [before](H2-empty-clone-before.json), [after](H2-empty-clone-after.json), [export raw](H2-empty-clone-export.json), [final refs](H2-final-local-refs.json) |
| H3 populated | PASS | Separate new primary/bare origin; two synthetic IDs, description/design/acceptance/notes/labels/typed metadata and discovered-from edge; fresh clone full JSONL+show readback equal, including strict JSON types | [case](H3-populated-result.json), [source data](H3-populated-source-data.json), [clone call](H3-populated-clone-bootstrap.json), [export](H3-populated-clone-export.json) |
| H3 invariants | PASS | Actual prefixbig-heroes, R=lastSeen, no Dolt remote, tracked bytes/index/HEAD/origin preserved | [before](H3-populated-before.json), [after](H3-populated-after.json), [final refs](H3-final-local-refs.json) |
| H1 canonical staged sentinel | PASS | Actual bootstrap STOP before init, exact index/HEAD/sentinel/origin preserved, .beads absent | [result](H1-canonical-result.json), [raw call](H1-canonical-bootstrap.json), before/after receipts |
| H1 alternate GIT_INDEX_FILE | PASS | Clean alternate index plus staged canonical sentinel; controlled STOP, both indexes and all observations unchanged, no DB | [result](H1-alternate-result.json), [raw call](H1-alternate-bootstrap.json) |
| H4 absent tracked active pin | PASS | New clone has committed config without active pin; STOP before DB/publication, snapshots unchanged | [result](H4-no-tracked-pin-result.json), [raw](H4-no-tracked-pin-bootstrap.json) |
| H4 forged caller receipt | PASS | Forged prefix JSON+matching caller hash cannot authorize restore; STOP before DB/publication, snapshots unchanged | [result](H4-forged-receipt-result.json), [raw](H4-forged-receipt-bootstrap.json) |
| H4 corrupt nonempty no-namespace R | PASS | Separate synthetic bare origin with nonempty memory-only snapshot; STOP before DB; HEAD/index/metadata/config/refs preserved | [result](H4-nonempty-no-namespace-result.json), [raw](H4-nonempty-no-namespace-bootstrap.json) |
| H5 installed links/version | PASS | Existing candidate-controlled native installer integration fixture: installed HOW_TO_USE local links exist, manifest/rule1.2.2, no stale1.0.2 rule | [test receipt](H5-existing-installed-doc-fixture.json), [scope](H5-result.json) |
| H6 live Codex / H7 CI/finalize / overall rc.4.1 acceptance | NOT RUN by Windows | Outside this packet; Mac/PM own respective gates | No readiness/merge/release claim |

H2 frozen empty R `{cases['H2']['frozen_R']}`; primary project pin commit `{cases['H2']['project_pin_commit']}`. H3 frozen populated R `{cases['H3']['frozen_R']}`, IDs `{cases['H3']['ids'][0]}` and `{cases['H3']['ids'][1]}`. Actual roots are under `D:/CodexArtifacts/overgate-rc41-winqa-20261104/runs/c64b634/cases`; H1 used the earlier prepared clean local clones with no prior candidate/Beads. Every origin is local disposable bare Git; working U2/Toon/OverGate stores and the old failing peer were untouched.

H5 method boundary: one existing `InstallTests.test_fresh_installed_how_to_use_links_and_beads_version` ran natively on candidate test code. Its controlled fixture creates a synthetic source commit and installs candidate payload bytes; this is an installed docs/version integration fixture, not a literal QUICKSTART or an install-state source-SHA claim for a real target project. H5 coverage is changed installed HOW_TO_USE links and manifest/rule version; no unrelated Markdown/link audit was added.

Raw stdout/stderr `.bin` files and SHA256s are captured before display decoding for all candidate helper calls in this run. The historical H2 FAIL on825c0b9 and its capture limitation remain in [previous report](https://github.com/komleff/overgate/pull/12#issuecomment-6634300269); [read-only diagnosis](https://github.com/komleff/overgate/pull/12#issuecomment-6634530838) is separate. No old receipt was rewritten or failure renamed PASS. No full rc.5 qualification, unrelated variants, source fix, merge, release or finalizer was run.
'''
    (E/'FINAL-WINDOWS-QA.md').write_text(report,encoding='utf-8',newline='\n')
    assert cmd(['git','branch','--show-current'])=='qa/rc41-evidence' and not cmd(['git','status','--porcelain'])
    (D/'receipts').mkdir(parents=True);(D/'harness').mkdir()
    (D/'.gitattributes').write_text('receipts/** -text\nharness/** -text\n',encoding='utf-8',newline='\n')
    for p in E.iterdir():
        if p.is_file():shutil.copyfile(p,D/'receipts'/p.name)
    for name in ['hotfix_qa.py','publish_success.py']:shutil.copyfile(B/name,D/'harness'/name)
    index={str(p.relative_to(D)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in D.rglob('*') if p.is_file()}
    (D/'SHA256SUMS.json').write_text(json.dumps(index,indent=2),encoding='utf-8',newline='\n')
    cmd(['git','-c','core.autocrlf=false','add',relative]);cmd(['git','diff','--cached','--check','--',relative+'/harness'])
    cmd(['git','commit','-m','docs: report scoped RC4.1 Windows native acceptance c64b634'])
    cmd(['git','push','origin','qa/rc41-evidence']);commit=cmd(['git','rev-parse','HEAD'])
    archive=subprocess.run(['git','-c','core.autocrlf=false','archive','--format=zip',commit+':'+relative],cwd=R,capture_output=True,check=True).stdout
    with zipfile.ZipFile(io.BytesIO(archive)) as z:bad=[p for p,h in index.items() if hashlib.sha256(z.read(p)).hexdigest()!=h]
    assert not bad,bad
    assert cmd(['git','ls-remote','origin','refs/heads/qa/rc41-evidence']).split()[0]==commit
    root='https://github.com/komleff/overgate-rc5-beads-winqa-20261104/blob/'+commit+'/'+relative+'/'
    publication=re.sub(r'\]\(([A-Za-z0-9_.-]+\.json)\)',lambda m:']('+root+'receipts/'+m.group(1)+')',report)
    publication+='\nImmutable [full report]('+root+'receipts/FINAL-WINDOWS-QA.md), [SHA256 index]('+root+'SHA256SUMS.json): '+str(len(index))+' files verified against published Git archive,0mismatch, including raw byte streams.\n'
    publisher=B.parent/'overgate-rc4-winqa-20261103/source-ac58c96';envp=os.environ.copy();envp['PYTHONUTF8']='1'
    p=subprocess.run([sys.executable,str(publisher/'.claude/tools/publish-pr-comment.py'),'12','-'],cwd=publisher,env=envp,input=publication,capture_output=True,text=True,encoding='utf-8')
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
    put('publication',{'evidence_commit':commit,'files_verified':len(index),'report_url':p.stdout.strip()});print(json.dumps({'evidence_commit':commit,'files':len(index),'report_url':p.stdout.strip()}))
if __name__=='__main__':main()
