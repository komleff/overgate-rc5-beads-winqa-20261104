"""Publish the already-stopped QA receipt; never rerun bootstrap/restore."""
import os,sys,json,hashlib,subprocess,shutil
from pathlib import Path
B=Path(__file__).resolve().parent;E=B/'evidence';S=B/'source-825c0b9'
R=B.parent/'overgate-rc5-beads-winqa-20261104/evidence-repo'
SHA='825c0b9d9e2ad7fe61182836649008a47a34c0c4';BRANCH='qa/rc41-evidence'
def cmd(args,cwd=R,input=None):
    p=subprocess.run([str(x) for x in args],cwd=cwd,input=input,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
    return p.stdout.strip()
def read(n):return json.loads((E/n).read_text(encoding='utf-8'))
def main():
    result=read('H2-empty-result.json');before=read('H2-empty-clone-before.json');after=read('H2-empty-clone-after.json');env=read('workspace-ready.json')
    assert result['result']=='FAIL' and cmd(['git','rev-parse','HEAD'],S)==SHA and not cmd(['git','status','--porcelain'],S)
    raw=cmd(['gh','api','repos/komleff/overgate/issues/comments/6633997887'],B)
    (E/'run-packet.json').write_text(raw,encoding='utf-8',newline='\n');contract=json.loads(raw)['body']
    paths=['scripts/bd-bootstrap.sh','scripts/bd-sync-common.sh','scripts/bd-sync-export.sh','scripts/bd-sync-restore.sh','scripts/lib/bd-env.sh','.claude/tools/run-python.sh','.agents/distribution-manifest.json']
    blobs={p:cmd(['git','rev-parse',SHA+':'+p],S) for p in paths}
    fingerprint=hashlib.sha256((''.join(p+' '+blobs[p]+'\n' for p in sorted(blobs))).encode()+contract.encode()).hexdigest()
    clone=Path(result['clone']);Rtip=result['frozen_R']
    diag={'remote_tracking_R':cmd(['git','rev-parse','refs/remotes/origin/beads-backup'],clone),'snapshot_tree':cmd(['git','ls-tree','-rl',Rtip,'--','.beads/issues.jsonl'],clone),'method':'Read-only Git object inspection after STOP; no bootstrap/restore retry'}
    (E/'H2-readonly-diagnostic.json').write_text(json.dumps(diag,indent=2),encoding='utf-8',newline='\n')
    (E/'source-fingerprint.json').write_text(json.dumps({'source_sha':SHA,'source_tree':cmd(['git','rev-parse',SHA+'^{tree}'],S),'blobs':blobs,'contract_comment':6633997887,'fingerprint':fingerprint,'method':'sorted path SP Git blob LF, then exact PM RUN body UTF8 bytes'},indent=2),encoding='utf-8',newline='\n')
    report=f'''## WINDOWS QA → PM / QA EXECUTION — RC4.1 H2 empty FAIL

Role/model: Windows QA / Codex GPT-6 (exact preset unavailable). Source `{SHA}`, clean detached clone; PM RUN6633997887 + start6634028533. Tested-content fingerprint `{fingerprint}` ([exact blobs/contract method](source-fingerprint.json)). Binary `{env['tools']['bd']['path']}`, `bd1.2.2 (6c124203e)`, SHA256 `{env['tools']['bd']['sha256']}`. Git2.51.2.windows.1, native Git Bash5.2.37, Python3.14.0. Codex0.154.0 availability only, H6 not executed.

**H2 empty FAIL. Run stopped at its first real failure; no retry or source repair.**

| H | PASS/FAIL/NOT RUN | Actual method / observation | Exact evidence |
|---|---|---|---|
| H2 fresh primary substeps | PASS scoped substeps | Actual Git Bash bootstrap exit0; Beads-only init commit; untracked sentinel preserved; effective prefixbig-heroes; active pin created, then project commit/push | [primary call](H2-empty-primary-bootstrap.json), [case checks](H2-empty-result.json), project-pin commit/push receipts |
| H2 empty second clone | FAIL | Tracked metadata+pin, no local DB, frozen empty snapshot. Actual bootstrap exit1 in bd-sync-restore child; DB created before STOP | [failing argv/stdout/stderr](H2-empty-clone-bootstrap.json), [full result](H2-empty-result.json) |
| H2 preservation facts | PASS scoped observations | HEAD/index/README/metadata/config/origin refs unchanged; DB absent→present | [before](H2-empty-clone-before.json), [after](H2-empty-clone-after.json) |
| H3 populated | NOT RUN | First-FAIL stop rule | RUN6633997887 |
| H1 staged / alternate index | NOT RUN | First-FAIL stop rule | Prepared baseline only, no candidate case invoked |
| H4 tracked prefix / forged receipt / corrupt snapshot | NOT RUN | First-FAIL stop rule | No candidate negative case invoked |
| H5 installed links/version | NOT RUN | First-FAIL stop rule | No installer fixture invoked |
| H6 / overall rc.4.1 acceptance / merge/release/finalize | NOT RUN | Outside this Windows packet | No readiness claim |

Primary: `{result['primary']}`. Clone: `{result['clone']}`. Frozen `beads-backup R={Rtip}`. Clone HEAD `{before['head']}`, exact index SHA256 `{before['index_sha256']}` unchanged. Metadata SHA256 `{before['files']['.beads/metadata.json']}` and config SHA256 `{before['files']['.beads/config.yaml']}` unchanged. No real project DB or GitHub production ref used; origin is a new local bare repository.

The failed call is exactly native `bash scripts/bd-bootstrap.sh` from the clone root, with `BD_BOOTSTRAP_EXPECTED_R={Rtip}`. It exits1 after approximately3s; nested failure names `C:\\Program Files\\Git\\usr\\bin\\bash.exe scripts/bd-sync-restore.sh` and `origin/beads-backup`. The pinned restore source has the matching missing-snapshot diagnostic at line51. Read-only Git inspection confirms the clone's remote-tracking ref equalsR and `.beads/issues.jsonl` exists as zero-byte blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`: [diagnostic](H2-readonly-diagnostic.json). Underlying cause is not asserted by QA.

Capture limit: the harness decoded native stderr as UTF8 with replacement; Cyrillic characters in the nested diagnostic are garbled in the recorded text. ASCII argv, exit code and state observations are intact. Original undecoded stderr bytes were not retained for this completed invocation; no rerun was made to improve the log. The receipt is exact captured text, not a claim of byte-exact original stderr. Future native capture needs raw-byte preservation; this does not turn the observed nonzero runtime result into PASS.

User-requested PM_ERR/DOC_PR self-check: target remains a working OverGate install/clone for the new project. My earlier passive notification setup did not perform active PM follow-up; I also spent excess time packaging evidence. The present H2 failure directly violates the requested clone acceptance. Minimal next action is Developer triage/fix via PM, then only affected Windows recheck on a new explicit pin. No expanded product guarantee, reviewer swarm, policy rewrite or source fix by QA.

Both source and all disposable roots/bare origin are retained. No cleanup, reset, force, alternate invocation, helper replay or additional candidate run followed the refusal. Remaining cases stay NOT RUN. [Prepared environment/baselines](workspace-ready.json).
'''
    (E/'H2-failure-report.md').write_text(report,encoding='utf-8',newline='\n')
    assert not cmd(['git','status','--porcelain'])
    cmd(['git','switch','-c',BRANCH])
    dest=R/'rc41';(dest/'receipts').mkdir(parents=True);(dest/'harness').mkdir()
    for p in E.iterdir():
        if p.is_file():shutil.copyfile(p,dest/'receipts'/p.name)
    for name in ['prepare_workspace.py','hotfix_qa.py','publish_failure.py','QA-PREPARATION.md']:shutil.copyfile(B/name,dest/'harness'/name)
    index={str(p.relative_to(dest)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.rglob('*') if p.is_file()}
    (dest/'SHA256SUMS.json').write_text(json.dumps(index,indent=2),encoding='utf-8',newline='\n')
    cmd(['git','add','rc41']);cmd(['git','diff','--cached','--check','--','rc41/harness'])
    cmd(['git','commit','-m','docs: preserve RC4.1 Windows empty-clone failure'])
    cmd(['git','push','-u','origin',BRANCH])
    sha=cmd(['git','rev-parse','HEAD']);(E/'failure-evidence-sha.txt').write_text(sha,encoding='utf-8')
    import re
    url='https://github.com/komleff/overgate-rc5-beads-winqa-20261104/blob/'+sha+'/rc41/'
    publication=re.sub(r'\]\(([A-Za-z0-9_.-]+\.json)\)',lambda m:']('+url+'receipts/'+m.group(1)+')',report)
    publication+='\nImmutable [full report]('+url+'receipts/H2-failure-report.md), [SHA256 map]('+url+'SHA256SUMS.json).\n'
    source=B.parent/'overgate-rc4-winqa-20261103/source-ac58c96';envp=os.environ.copy();envp['PYTHONUTF8']='1'
    p=subprocess.run([sys.executable,str(source/'.claude/tools/publish-pr-comment.py'),'12','-'],cwd=source,env=envp,input=publication,text=True,encoding='utf-8',capture_output=True)
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
    (E/'failure-report-url.txt').write_text(p.stdout.strip(),encoding='utf-8');print(json.dumps({'evidence':sha,'files':len(index),'report_url':p.stdout.strip()}))
if __name__=='__main__':main()
