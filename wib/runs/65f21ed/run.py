from pathlib import Path
import os,sys,subprocess,json,hashlib,base64,time,shutil,importlib.util,traceback
R=Path(__file__).resolve().parent; S=R/'source'; E=R/'evidence'; P=R/'plans'; C=R/'cases'
for p in (E,P,C):p.mkdir(exist_ok=True)
PREP=Path('D:/CodexArtifacts/overgate-rc5-wib-winqa-20261105')
PIN='65f21ed72b6cbc85cd7b5ed41502e3a84a464739'; BASE='3096e550bfd6f4ff73c987812a2dda2c7d339669'
BD=Path('D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe')
ENV=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',PATH='C:/Program Files/Git/bin;C:/Program Files/Git/usr/bin;'+os.environ['PATH'])
for k in list(ENV):
 if k.startswith(('BEADS_','BD_','DOLT_')) or k in ['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_NAMESPACE','CLAUDE_PROJECT_DIR']:ENV.pop(k,None)
ENV['BD_BIN']=str(BD)
RESULTS=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,obj):
 p=E/(n+'.json');p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return p
def run(n,args,cwd=R,expected=0,data=None):
 t=time.time();q=subprocess.run(list(map(str,args)),cwd=cwd,env=ENV,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
 (E/(n+'.stdout.bin')).write_bytes(q.stdout);(E/(n+'.stderr.bin')).write_bytes(q.stderr)
 def decode(b):
  try:return b.decode('utf-8')
  except UnicodeDecodeError:return b.decode('cp1251',errors='replace')
 receipt=dict(argv=list(map(str,args)),cwd=str(cwd),exit_code=q.returncode,expected=expected,seconds=round(time.time()-t,3),stdout=decode(q.stdout),stderr=decode(q.stderr),stdout_sha256=sha(q.stdout),stderr_sha256=sha(q.stderr))
 save(n,receipt)
 if expected is not None and q.returncode!=expected:raise AssertionError('unexpected native exit: '+n+' '+str(q.returncode)+' '+receipt['stderr'])
 return q
def git(n,args,cwd=R,expected=0,data=None):return run(n,['git',*args],cwd,expected,data).stdout
def tree(root):
 if not root.exists():return {'absent':True}
 d={}
 for p in sorted(root.rglob('*')):
  key=p.relative_to(root).as_posix()
  if p.is_symlink():d[key]={'symlink':os.readlink(p)}
  elif p.is_file():d[key]={'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size,'mode':p.stat().st_mode & 0o777}
  elif p.is_dir():d[key]={'directory':True}
  else:d[key]={'unknown':True}
 return d
def snapshot(n,target,remote=None):
 obj={'target':str(target),'files':tree(target),'backup':tree(target/'.overgate-backups'),'remote':str(remote) if remote else None,'remote_files':tree(remote) if remote else None}
 save(n,obj);return obj
def unchanged(n,before,after):
 assert before==after,'target/backup/remote byte drift: '+n
 save(n,{'equal':True,'before_sha256':sha(json.dumps(before,sort_keys=True).encode()),'after_sha256':sha(json.dumps(after,sort_keys=True).encode())})
def row(n,ac,result,method,evidence):
 RESULTS.append(dict(case=n,ac=ac,result=result,method=method,evidence=evidence));save('results',RESULTS);print(n+': '+result,flush=True)
def clone(n,remote=None):
 target=C/n;remote=remote or PREP/'origin.git'
 git(n+'-clone',['clone','--no-hardlinks','-c','core.autocrlf=false',remote,target])
 git(n+'-branch',['switch','-c','qa/'+n],target)
 git(n+'-name',['config','user.name','Windows WI-B QA'],target);git(n+'-email',['config','user.email','qa-wib@example.invalid'],target)
 return target
def plan(n,target,no_beads=False):
 path=P/(n+'.plan.json');args=[sys.executable,S/'scripts/install-overgate.py','plan','--source',S,'--source-sha',PIN,'--target',target,'--contract',R/'pr-contract.txt','--target-pr','https://github.com/example/project/pull/1','--output',path]
 if no_beads:args+=['--no-beads']
 run(n+'-plan',args)
 return path,json.loads(path.read_bytes())
def approval(n,path):
 p=P/(n+'.synthetic-approval.json');p.write_text(json.dumps(dict(verdict='PLAN_READY',plan_sha256=sha(path.read_bytes()),evidence='https://github.com/example/project/pull/1#synthetic-disposable-fixture-only'))+'\n',encoding='utf-8');return p
def apply(n,path,expected=0):return run(n+'-apply',[sys.executable,S/'scripts/install-overgate.py','apply','--plan',path,'--approval',approval(n,path)],expected=expected)
def rejected(n,target,remote=None,expected_reason=None):
 before=snapshot(n+'-before',target,remote);path,p=plan(n,target)
 unchanged(n+'-plan-readonly',before,snapshot(n+'-after-plan',target,remote))
 assert p['beads_inventory']['blocked'],n+' inventory not blocked'
 if expected_reason:assert expected_reason in json.dumps(p['beads_inventory']),n+' wrong reason'
 q=apply(n,path,1);assert b'preservation required' in q.stderr,n+' wrong apply refusal'
 unchanged(n+'-apply-readonly',before,snapshot(n+'-after-apply',target,remote))
 row(n,'B2','PASS','Actual plan records blocked inventory; approved apply RC1; full target/Git/backup/remote hashes unchanged',n+'-apply-readonly.json')
def main():
 assert git('source-pin',['rev-parse','HEAD'],S).decode().strip()==PIN
 contract=(R/'pr-contract.txt').read_bytes()
 # Text patch transport may append a blank line; use exactly the shared CONTRACT normalization.
 contract=contract.strip()+b'\n';(R/'pr-contract.txt').write_bytes(contract)
 assert len(contract)==1024 and sha(contract)=='32b9d90893e2a686506b3210403857c43e4b422b091d4fce0cbe11426834c795'
 paths=git('fingerprint-paths',['diff','--name-only',BASE,PIN],S).decode().splitlines()
 blobs={p:git('fingerprint-blob-'+str(i),['rev-parse',PIN+':'+p],S).decode().strip() for i,p in enumerate(sorted(paths))}
 fp=sha(''.join(p+' '+blobs[p]+'\n' for p in sorted(blobs)).encode()+contract)
 save('source-binding',dict(source=PIN,base=BASE,paths=blobs,contract_bytes=len(contract),contract_sha256=sha(contract),content_fingerprint=fp,plan_blob=git('plan-blob',['rev-parse',PIN+':docs/plans/2026-11-05-v4.0.0-rc.5-install-activation.md'],S).decode().strip()))
 assert len(paths)==5 and fp=='f51ba29323722d0732c4aa93213b70fad906129541c7c96b83f6c3c750a9c9ff'
 shutil.copyfile(S/'docs/plans/2026-11-05-v4.0.0-rc.5-install-activation.md',R/'plan-source.md')
 assert sha(BD.read_bytes())=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de'
 run('bd-version-only',[BD,'--version']);run('git-version',['git','--version']);run('bash-version',['C:/Program Files/Git/bin/bash.exe','--version']);run('python-version',[sys.executable,'--version']);run('node-version',['node','--version'])
 m=json.loads((S/'.agents/distribution-manifest.json').read_bytes());beads_entries=[e for e in m['files'] if e.get('component')=='beads']
 save('beads-closure',beads_entries)
 remote=PREP/'origin.git'
 target=clone('fresh')
 before=snapshot('fresh-before',target,remote);path,p=plan('fresh',target)
 unchanged('fresh-plan-readonly',before,snapshot('fresh-after-plan',target,remote))
 assert not p['conflicts'] and not p['beads_inventory']['blocked'] and p['beads_protocol']=='managed-v1'
 apply('fresh',path)
 state=json.loads((target/'.overgate/install-state.json').read_bytes());assert state['beads'] is True and state['beads_protocol']=='managed-v1' and state['source_sha']==PIN
 comparison={e['target']:{'source':sha((S/e['source']).read_bytes()),'installed':sha((target/e['target']).read_bytes())} for e in beads_entries}
 assert all(v['source']==v['installed'] for v in comparison.values())
 assert not (target/'.beads').exists() and not (target/'.bd-intents').exists() and not (target/'.git/overgate-bd-managed').exists()
 after=snapshot('fresh-after-apply',target,remote);assert before['remote_files']==after['remote_files'] and before['files']['README.md']==after['files']['README.md']
 save('fresh-result',dict(source=PIN,target_head=git('fresh-target-head',['rev-parse','HEAD'],target).decode().strip(),closure=comparison,state=state,no_local_beads=True,no_managed_registration=True,remote_byte_unchanged=True))
 run('fresh-installed-checker',[sys.executable,target/'scripts/check-reference.py','--root',target])
 row('fresh-managed-closure-no-init','B1','PASS','Native plan/apply + all Beads source/target SHA256; installed checker; no .beads/registration/queue; origin byte unchanged','fresh-result.json')
 for name,legacy in [('no-beads',False),('old-beads-false',True)]:
  target=clone(name)
  if legacy:
   shutil.copytree(PREP/'beads-false-upgrade',target,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.git','.overgate-backups'))
   old=json.loads((target/'.overgate/install-state.json').read_bytes());assert old['beads'] is False and 'beads_protocol' not in old
  before=snapshot(name+'-before',target,remote);path,p=plan(name,target,no_beads=not legacy)
  unchanged(name+'-plan-readonly',before,snapshot(name+'-after-plan',target,remote))
  assert p['beads'] is False and p['beads_protocol']=='none' and not p['conflicts'] and not p['beads_inventory']['blocked']
  apply(name,path)
  state=json.loads((target/'.overgate/install-state.json').read_bytes());assert state['beads'] is False and state['beads_protocol']=='none'
  absent=[e['target'] for e in beads_entries if not (target/e['target']).exists()];assert len(absent)==len(beads_entries)
  assert b'<!-- overgate:beads -->' not in (target/'AGENTS.md').read_bytes() and not (target/'.beads').exists()
  after=snapshot(name+'-after-apply',target,remote);assert before['remote_files']==after['remote_files']
  run(name+'-installed-checker',[sys.executable,target/'scripts/check-reference.py','--root',target,'--no-beads'])
  save(name+'-result',dict(source=PIN,state=state,absent_beads_closure=absent,remote_byte_unchanged=True))
  row(name,'B1','PASS','Actual native plan/apply/checker; none; complete Beads closure absent; prior false upgrade has no --no-beads override',name+'-result.json')
 # Existing real native store stays in place; candidate may only inventory and refuse.
 rejected('local-native-legacy',PREP/'legacy-pending',PREP/'legacy-origin.git','.beads: retained state')
 target=clone('pending-only');q=target/'.bd-intents/raw.jsonl';q.parent.mkdir();shutil.copyfile(PREP/'legacy-pending/.bd-intents/qa-pending.raw.jsonl',q)
 rejected('pending-only',target,remote,'.bd-intents: retained state')
 target=clone('unknown-receipt');p=target/'.git/bd-receipts';p.mkdir();shutil.copyfile(PREP/'unknown-receipt/.git/bd-receipts/qa-unknown-receipt.json',p/'opaque.json')
 rejected('unknown-receipt',target,remote,'git/bd-receipts: retained state')
 target=clone('remote-present',PREP/'legacy-origin.git')
 # Clone carries legacy managed payload/state; valid original bytes remain, no local native DB.
 rejected('remote-present',target,PREP/'legacy-origin.git','remote beads-backup present')
 target=clone('remote-unavailable');missing=C/'nonexistent-origin.git'
 git('unavailable-origin',['remote','set-url','origin',missing],target)
 rejected('remote-unavailable',target,None,'unavailable')
 target=clone('local-drift');path,p=plan('local-drift',target);assert not p['beads_inventory']['blocked']
 d=target/'.bd-intents';d.mkdir();(d/'arrived.jsonl').write_bytes(b'{"fixture":"new pending after plan"}\n')
 before=snapshot('local-drift-before-apply',target,remote);q=apply('local-drift',path,1);assert b'plan drift' in q.stderr
 unchanged('local-drift-apply-readonly',before,snapshot('local-drift-after-apply',target,remote))
 row('local-plan-apply-drift','B2','PASS','Exact approved plan then new pending; actual apply RC1 drift before target/backup write','local-drift-apply-readonly.json')
 advance=C/'advance-origin.git';git('advance-origin-clone',['clone','--bare','--no-hardlinks',PREP/'legacy-origin.git',advance])
 target=clone('remote-advance',advance)
 old=git('advance-old-R',['rev-parse','refs/heads/beads-backup'],advance).decode().strip()
 tr=git('advance-tree',['rev-parse',old+'^{tree}'],advance).decode().strip()
 nxt=git('advance-object',['-c','user.name=WI-B fixture','-c','user.email=qa@example.invalid','commit-tree',tr,'-p',old,'-m','fixture: remote advance, no task mutation'],advance).decode().strip()
 path,p=plan('remote-advance',target);assert p['beads_inventory']['remote']['R']==old
 git('advance-fault',['update-ref','refs/heads/beads-backup',nxt,old],advance)
 before=snapshot('remote-advance-before-apply',target,advance);q=apply('remote-advance',path,1);assert b'plan drift' in q.stderr
 unchanged('remote-advance-apply-readonly',before,snapshot('remote-advance-after-apply',target,advance))
 save('remote-advance-result',dict(planned_R=old,injected_R=nxt,method='synthetic local bare ref advance to same-tree commit; not managed publisher execution'))
 row('remote-R-advance','B2','PASS','Synthetic known local remote advance; actual approved apply refuses exact frozen-R drift, preserves injected remote','remote-advance-result.json')
 target=clone('symlink');external=C/'external-beads';external.mkdir();(external/'sentinel').write_bytes(b'do not read/write through symlink\n')
 try:os.symlink(external,target/'.beads',target_is_directory=True)
 except OSError as ex:
  save('symlink-capability',dict(available=False,error=str(ex)));row('symlink','B2','NOT RUN','Native Windows symlink creation unavailable; no emulation','symlink-capability.json')
 else:
  save('symlink-capability',dict(available=True,path=str(target/'.beads'),target=str(external)))
  external_before=tree(external);rejected('symlink',target,remote,'symlink');assert tree(external)==external_before
 # Isolated projection mutation calls candidate's actual validator without changing source commit or runtime target.
 probe=R/'closure-negative.py'
 before=snapshot('closure-negative-before',C/'fresh',remote)
 run('closure-negative',[sys.executable,probe,S,PIN,E])
 unchanged('closure-negative-target-unchanged',before,snapshot('closure-negative-after',C/'fresh',remote))
 row('missing-managed-import','B1/I3','PASS','Exact-source exported validator with one manifest import dependency omitted in memory; actual checker refuses projected temp closure; source/installed target untouched','closure-negative-result.json')
 row('permissions-negative','B2','NOT RUN','No reliable denied-access fixture established under current Windows account; no mock substituted','results.json')
 row('activation-switch-fence-publication','B3/B4','NOT RUN','Explicitly excluded by early B1/B2 packet','results.json')
 save('complete',dict(status='bounded B1/B2 complete',source=PIN,candidate_activation=False,candidate_publication=False,results=RESULTS));print('BOUNDED COMPLETE',flush=True)
if __name__=='__main__':
 try:main()
 except BaseException as ex:
  save('STOP',dict(source=PIN,error=str(ex),traceback=traceback.format_exc(),results=RESULTS));print(traceback.format_exc(),flush=True);raise
