from pathlib import Path
import json,shutil,platform,sys,hashlib,datetime
R=Path(__file__).resolve().parent;E=R/'evidence'
rows=json.loads((E/'results.json').read_bytes())
binding=json.loads((E/'source-binding.json').read_bytes())
stopped=json.loads((E/'STOP.json').read_bytes()) if (E/'STOP.json').exists() else None
if stopped:rows.append(dict(case='execution stop',ac='B1/B2',method=stopped['error'],result='FAIL',evidence='STOP.json'))
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
env=dict(time_utc=stamp,role='Windows QA',model='Codex GPT-6',os=platform.platform(),win32_ver=platform.win32_ver(),python=sys.version,source=binding['source'],runtime_limit='B1/B2 only; no activation/publication')
(E/'environment.json').write_text(json.dumps(env,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
table='\n'.join('| '+r['case']+' | '+r['ac']+' | '+r['method'].replace('|','/')+' | '+r['result']+' | [receipt](evidence/'+r['evidence']+') |' for r in rows)
text=f'''# WINDOWS QA → PM / WI-B early B1/B2 `65f21ed`

Role/model: Windows QA / Codex GPT-6. UTC: {stamp}.
Commit: `{binding['source']}`; base `{binding['base']}`.
Content-Fingerprint: `{binding['content_fingerprint']}` (5 paths + exact 1024-byte CONTRACT).
Plan blob: `{binding['plan_blob']}`; CONTRACT SHA256 `{binding['contract_sha256']}`.
Source: PR12 [bounded RUN 6643640897](https://github.com/komleff/overgate/pull/12#issuecomment-6643640897), PR17 B1/B2/I1/I3.

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
{table}

All native subprocess outputs were captured as raw `.stdout.bin` / `.stderr.bin` before decoding. Each JSON receipt records exact argv/cwd/exit, hashes and displayed output. Plans and approvals are frozen in `plans/`; approvals are **synthetic disposable-test inputs only**, not real project/operator approvals. Before/after snapshots include every target file, Git metadata, backup directories, remote file/object/ref hashes, and symlink identity where supported. Plan/apply refusals preserved the exact captured target/backup/remote bytes.

The fresh and no-Beads targets are new independent disposable clones of the prepared local bare origin. The old `beads:false` case copies the actual released rc.4.1 `3f3246c` baseline payload/state into a new disposable clone, then upgrades with no no-Beads override. Original frozen preparation stores remain intact; the real native legacy store was inventoried read-only, not opened by bd. `bd --version` only, known scoped binary1.2.2 SHA256 `b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de`; Git2.51.2.windows.1, Git Bash5.2.37, Python3.14.0, Node24.11.0. Full raw version receipts are included.

The remote advance is an explicit local fixture injection: a new same-tree Git commit advances only the disposable `beads-backup` ref between plan/apply. It is not a managed task publication or activation. The missing-import negative calls the exact source validator against an in-memory manifest omission and records the actual projected checker refusal; source SHA stays pinned. No synthetic alternate source commit is claimed qualified.

Target SHA is the synthetic fixture code HEAD recorded in `fresh-result.json`; task publication SHA/actual new task ID are **N/A**. There was no task lifecycle run. B3 activation/trusted-main writes, B4 migration/protocol switch/old-writer fence/publication/rollback-after-publication, live Claude/Codex sessions, full local verifier/CI qualification and whole WI-B/release verdict are **NOT RUN here**. No working U2/Toon/OverGate checkout/DB/hooks/settings, merge/release or finalize were used.
'''
(R/'REPORT.md').write_text(text,encoding='utf-8')
repo=Path('D:/CodexArtifacts/overgate-rc5-beads-winqa-20261104/evidence-repo')
dest=repo/'wib/runs/65f21ed';assert not dest.exists();dest.mkdir(parents=True)
for name in ['run.py','closure-negative.py','package_report.py','pr-contract.txt','plan-source.md','REPORT.md']:
 shutil.copyfile(R/name,dest/name)
for name in ['evidence','plans']:shutil.copytree(R/name,dest/name)
print(json.dumps(dict(destination=str(dest),status='FAIL stop' if stopped else 'bounded complete',rows=len(rows),files=sum(p.is_file() for p in dest.rglob('*')))))
