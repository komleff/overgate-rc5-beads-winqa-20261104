from pathlib import Path
import os,sys,subprocess,json,hashlib,time,zipfile,shutil,uuid,platform
R=Path(__file__).resolve().parent;E=R/'evidence';E.mkdir(exist_ok=True);C=R/'cases';C.mkdir(exist_ok=True);I=R/'inputs';I.mkdir(exist_ok=True)
OLD=Path('D:/CodexArtifacts/overgate-rc5-wib-winqa-20261105');PLAN=Path('D:/CodexArtifacts/overgate-rc5-wib-b3-5412a8f-winqa-20261105/source/docs/plans/2026-11-05-v4.0.0-rc.5-install-activation.md');BD=Path('D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe')
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0')
for k in list(ENV):
 if k.startswith(('BEADS_','BD_','DOLT_','GIT_CONFIG','GIT_AUTHOR_','GIT_COMMITTER_')) or k in ['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_NAMESPACE']:ENV.pop(k,None)
ENV.update(BD_BIN=str(BD),GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_NOSYSTEM='1',BD_DISABLE_METRICS='1',DOLT_METRICS_DISABLED='1')
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,v):(E/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(n,args,cwd=R,data=None,expected=0):
 t=time.time();q=subprocess.run(list(map(str,args)),cwd=cwd,env=ENV,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
 for kind,b in [('stdout',q.stdout),('stderr',q.stderr)]:(E/(n+'.'+kind+'.bin')).write_bytes(b)
 def dec(b):
  try:return b.decode('utf-8')
  except UnicodeDecodeError:return b.decode('cp1251','replace')
 save(n,dict(argv=list(map(str,args)),cwd=str(cwd),exit_code=q.returncode,seconds=round(time.time()-t,3),stdout=dec(q.stdout),stderr=dec(q.stderr),stdout_sha256=sha(q.stdout),stderr_sha256=sha(q.stderr)))
 assert q.returncode==expected,n+': '+str(q.returncode)+' '+dec(q.stderr)
 return q.stdout
def git(n,args,cwd=R,**kw):return run(n,['git',*args],cwd,**kw)
def files(root):return {p.relative_to(root).as_posix():dict(sha256=sha(p.read_bytes()),bytes=p.stat().st_size,mode=p.stat().st_mode & 0o777) for p in sorted(root.rglob('*')) if p.is_file()}
def normalize(value):
 value=dict(value);value.setdefault('_type','issue')
 for field in ['labels','comments','dependencies']:
  if isinstance(value.get(field),list):value[field]=sorted(value[field],key=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False))
 return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def models(data):return sorted(normalize(json.loads(line)) for line in data.splitlines() if line.strip())
baseline=OLD/'evidence/legacy-baseline.bundle';raw_zip=OLD/'evidence/frozen-legacy-stores.zip';logical=(OLD/'evidence/legacy-before.jsonl').read_bytes()
assert sha(baseline.read_bytes())=='1f37139e3a382750ebfc4eded5758268bbae612e0c7262446ee007be0edc793d'
assert sha(raw_zip.read_bytes())=='7063b0a27bca5d749e2b1cad594a22dac6e20457bd47198c6aea8312d08b941b'
assert sha(logical)=='0909265e470355b457ddf0cea4b477bfd32433ac18f63d76d4b92b5beea31952'
assert sha(BD.read_bytes())=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de'
assert sha(PLAN.read_bytes())=='c4aa4143159b0abceef911a4917c45f47f79a8802eff7a1556de8e7343c50af4';shutil.copyfile(PLAN,R/'plan-source.md')
version=run('bd-version',[BD,'--version']).decode().strip();frozen_parent='aa42f389fa93eea88583d74010579ecc920528c0';code='9fc388d80ededf26710876478142391885e0e956'
native_rows=[json.loads(x) for x in logical.splitlines() if x.strip()];ids=[x['id'] for x in native_rows if x.get('_type','issue')=='issue'];assert len(ids)==2 and all(x.startswith('wib-qa-') for x in ids)
def copy_native_store(target):
 db=target/'.beads';db.mkdir(exist_ok=True)
 with zipfile.ZipFile(raw_zip) as archive:
  for name in archive.namelist():
   if not name.startswith('legacy-pending/') or name.endswith('/'):continue
   relative=Path(name.removeprefix('legacy-pending/'));dest=db/relative;assert dest.resolve().is_relative_to(db.resolve())
   dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(archive.read(name))
cases={}
for name in ['clean-populated','retained-pending','unknown-unupgraded']:
 root=C/name;root.mkdir();real=root/'real.git';attacker=root/'attacker.git'
 git(name+'-real-clone',['clone','--bare','--branch','qa/preparation',baseline,real]);git(name+'-main-ref',['update-ref','refs/heads/main',code],real);git(name+'-head',['symbolic-ref','HEAD','refs/heads/main'],real)
 tree=git(name+'-legacy-tree',['rev-parse',frozen_parent+'^{tree}'],real).decode().strip()
 tip=git(name+'-second-legacy-history-point',['-c','user.name=Windows B4 fixture','-c','user.email=qa-b4@example.invalid','commit-tree',tree,'-p',frozen_parent,'-m','fixture: second legacy snapshot '+name],real).decode().strip()
 git(name+'-legacy-ref',['update-ref','refs/heads/beads-backup',tip,frozen_parent],real)
 assert git(name+'-frozen-snapshot',['show',tip+':.beads/issues.jsonl'],real)==logical
 git(name+'-attacker-clone',['clone','--bare','--single-branch','--branch','main','--no-hardlinks',real,attacker])
 assert git(name+'-attacker-no-task',['for-each-ref','--format=%(refname) %(objectname)','refs/heads/beads-backup'],attacker)==b''
 roles=['target','old-writer-a','old-writer-b','publisher','peer']+(['unupgraded-old-writer'] if name=='unknown-unupgraded' else [])
 root_paths={};exports={}
 for role in roles:
  target=root/role;root_paths[role]=target;git(name+'-'+role+'-clone',['clone','--no-hardlinks','-c','core.autocrlf=false',real.as_posix(),target]);git(name+'-'+role+'-name',['config','user.name','Windows B4 '+role],target);git(name+'-'+role+'-email',['config','user.email','qa-b4-'+role+'@example.invalid'],target)
  state=json.loads((target/'.overgate/install-state.json').read_bytes());assert state['source_sha']=='3f3246c3a3b62377fc02aad05283cae1ef5d4e2d' and state['beads'] is True and 'beads_protocol' not in state
  if role in ['target','old-writer-a','old-writer-b','unupgraded-old-writer']:
   copy_native_store(target);assert (target/'.beads/embeddeddolt').is_dir()
   cfg=json.loads(run(name+'-'+role+'-native-prefix',[BD,'--readonly','--sandbox','config','list','--json'],target));assert cfg['issue_prefix']=='wib-qa'
   export=E/(name+'-'+role+'-native-export.jsonl');run(name+'-'+role+'-native-export',[BD,'--readonly','--sandbox','export','--all','--output',export],target);assert models(export.read_bytes())==models(logical)
   exports[role]=dict(path=str(export),sha256=sha(export.read_bytes()),full_objects_equal=True,project_prefix=cfg['issue_prefix'],native_store=str(target/'.beads/embeddeddolt'),store_directory_inode=(target/'.beads/embeddeddolt').stat().st_ino)
  else:assert not (target/'.beads/embeddeddolt').exists() and not (target/'.beads/dolt').exists()
  if role in ['old-writer-a','old-writer-b','unupgraded-old-writer']:
   hook=target/'.git/hooks/pre-push';hook.write_text('#!/bin/sh\n# Synthetic project-owned '+role+' hook; preserve these bytes.\nexit 0\n',encoding='utf-8',newline='\n');hook.chmod(0o755)
 if name=='retained-pending':
  pending=root_paths['target']/'.bd-intents/b4-retained.raw.jsonl';pending.parent.mkdir();owner='agent-'+str(uuid.uuid4());pending.write_text(json.dumps(dict(intent_id='b4-retained-001',op='update',ref=ids[0],notes='Retain exact bytes; never silently replay'),ensure_ascii=False)+'\n',encoding='utf-8')
  save(name+'-pending-owner',dict(path=str(pending),sha256=sha(pending.read_bytes()),owner=owner,status='unprepared raw intent; ownership metadata is external test input; reviewed adoption still required',candidate_prepared=False,replayed=False))
 if name=='unknown-unupgraded':
  receipt=root_paths['target']/'.git/bd-receipts/opaque-unknown.json';receipt.parent.mkdir();receipt.write_text(json.dumps(dict(fixture_only=True,status='unknown-unreconciled',owner='agent-'+str(uuid.uuid4())))+'\n',encoding='utf-8');save(name+'-negative-input',dict(opaque_receipt=str(receipt),receipt_sha256=sha(receipt.read_bytes()),unupgraded_old_writer=str(root_paths['unupgraded-old-writer']),candidate_upgraded=False,expected='stop unknown receipt/unupgraded enumerated writer before switch; exact candidate API not selected'))
 linked=None
 if name=='clean-populated':
  linked=root/'old-writer-a-linked';git(name+'-linked',['worktree','add','-b','qa/b4-linked',linked,'main'],root_paths['old-writer-a']);root_paths['linked']=linked
 inventories={}
 for role,target in root_paths.items():
  common=git(name+'-'+role+'-common',['rev-parse','--path-format=absolute','--git-common-dir'],target).decode().strip();head=git(name+'-'+role+'-head',['rev-parse','HEAD'],target).decode().strip();index=git(name+'-'+role+'-index',['ls-files','-s','-z'],target);status=git(name+'-'+role+'-status',['status','--porcelain=v1','-z'],target)
  fetch=git(name+'-'+role+'-fetch-url',['remote','get-url','origin'],target).decode().strip();pushes=git(name+'-'+role+'-all-push',['remote','get-url','--push','--all','origin'],target).decode().splitlines();assert fetch==real.as_posix() and pushes==[real.as_posix()]
  remote=git(name+'-'+role+'-frozen-R',['ls-remote','--heads','origin','refs/heads/beads-backup'],target).decode().split()[0];assert remote==tip
  inventories[role]=dict(path=str(target),HEAD=head,index_entries_sha256=sha(index),status_sha256=sha(status),status_raw_hex=status.hex(),git_common_dir=common,fetch_url=fetch,all_push_urls=pushes,remote_R=remote,files=files(target),runtime_store_present=(target/'.beads/embeddeddolt').is_dir(),native_cli_called=(role in exports))
 refs=git(name+'-real-refs',['for-each-ref','--format=%(refname) %(objectname)'],real).decode();fake_refs=git(name+'-attacker-refs',['for-each-ref','--format=%(refname) %(objectname)'],attacker).decode()
 input_data=dict(case=name,baseline_only=True,runtime_source_sha=None,real_R=tip,attacker_R=None,known_legacy_capable_store_roots=[str(root_paths[r]) for r in ['target','old-writer-a','old-writer-b']],authorized_old_writer_clones=[str(root_paths[r]) for r in ['old-writer-a','old-writer-b']],target_store_in_inventory=True,positive_enumeration_must_cover_target_store_as_well=True,push_divergence_negative=dict(fetch=real.as_posix(),future_push=attacker.as_posix(),status='prepared locator only, not configured'),linked_marker_only_negative=str(linked) if linked else None,hook_modes='NTFS does not provide POSIX executable-bit disable semantics; byte/mode/read-only inventory captured',unknown_negative=(name=='unknown-unupgraded'))
 (I/(name+'.json')).write_text(json.dumps(input_data,indent=2)+'\n',encoding='utf-8')
 cases[name]=dict(real=dict(path=str(real),refs=refs,R=tip,files=files(real)),attacker=dict(path=str(attacker),refs=fake_refs,R=None,files=files(attacker)),legacy_parent=frozen_parent,main=code,snapshot_sha256=sha(logical),native_exports=exports,roots=inventories,input_sha256=sha((I/(name+'.json')).read_bytes()))
save('prep-ready',dict(role='Windows QA',model='Codex GPT-6',os=platform.platform(),authority='PR12#6649803748',status='PREP READY ONLY',plan_source='5412a8f25fe94f2e6c313357e556717469514f14',plan_blob='5dedca627bf31916b871d85e88c4906551aaf576',plan_sha256=sha(PLAN.read_bytes()),runtime_source_sha=None,baseline_payload_source='3f3246c3a3b62377fc02aad05283cae1ef5d4e2d',baseline_code_commit=code,native_bd=dict(path=str(BD),version=version,sha256=sha(BD.read_bytes())),prefix='wib-qa',database_name='wib_qa',actual_ids=ids,cases=cases,candidate_code_executed=False,fence=False,protocol_switch=False,migration=False,pending_prepared=False,pending_replayed=False,managed_publication=False,real_project_used=False))
(R/'REPORT.md').write_text('# WINDOWS QA → PM / B4 legacy-fence PREP READY ONLY\n\nWindows QA / Codex GPT-6. Authority PR12#6649803748, frozen plan B4/I1/I7 blob5dedca6 at accepted541. Candidate runtime pin not issued; 5c checkpoint not run.\n\nThree independent fresh legacy projects: clean-populated (with actual linked worktree), retained-pending, unknown-unupgraded. Each has real bare legacy history with two identical native-export snapshot commits, attacker bare same code main/no task ref, two separate authorized old-writer clones, isolated populated target, uninitialized publisher/peer metadata-only clones. Target is also explicitly inventoried as a known legacy-capable store root, so final enumerated writer scope must not silently omit it. Unknown group has an additional unupgraded clone and opaque receipt; retained raw queue has external owner/hash, never prepared/replayed.\n\nOnly immutable synthetic legacy baseline was copied: released rc.4.1 payload3f3246c and offline native DB copies from frozen old test pack. Separate physical stores, no hardlinks/shared DB path. Actual qualified native bd1.2.2 readonly config+export proved complete two-task object equality for every populated root; prefix wib-qa differs from DBname wib_qa. IDs wib-qa-05l/wib-qa-jtu. The extra legacy snapshot commit is explicit Git fixture construction, not a claim to qualify the old export helper. No init/import/task mutation, direct Dolt write, candidate packet/fence/switch/migration or managed publication ran.\n\nAll DB/queue/receipt/config/hook bytes+mode, HEAD/index/status, canonical common-dir, fetch+all push URLs and frozen R recorded. Hooks are explicit synthetic project-owned pre-push fixtures. NTFS cannot meaningfully simulate POSIX execute-bit removal; this negative is NOT RUN, not emulated. Linked clone had no native bd call. Candidate-specific unknown-writer/fence/packet/snapshot negative interfaces will bind only to forthcoming exact RUN. All baseline Git/native actions stayed inside new test roots. Working Tune-Heroes/U2/OverGate checkouts/DB/settings/hooks and all previous immutable QA archives untouched.\n',encoding='utf-8')
print(json.dumps(dict(status='PREP READY ONLY',cases=list(cases),prefix='wib-qa',native_ids=ids,frozen_R={n:d['real']['R'] for n,d in cases.items()},candidate='NOT RUN')),flush=True)
