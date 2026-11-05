from pathlib import Path
import os,sys,subprocess,json,hashlib,zipfile,io,shutil,datetime,platform
R=Path(__file__).resolve().parent;E=R/'evidence';manifest=json.loads((E/'prep-ready.json').read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,v):(E/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0')
for k in list(env):
 if k.startswith(('BEADS_','BD_','DOLT_','GIT_CONFIG')) or k in ['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_NAMESPACE']:env.pop(k,None)
env.update(GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_NOSYSTEM='1')
def git(n,args,cwd,allowed=(0,)):
 q=subprocess.run(['git',*map(str,args)],cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
 (E/(n+'.stdout.bin')).write_bytes(q.stdout);(E/(n+'.stderr.bin')).write_bytes(q.stderr);save(n,dict(argv=['git',*map(str,args)],cwd=str(cwd),exit_code=q.returncode,stdout=q.stdout.decode('utf-8','replace'),stderr=q.stderr.decode('utf-8','replace')))
 assert q.returncode in allowed,n
 return q.stdout
paths=[];hook_inventory={}
for name,case in manifest['cases'].items():
 real=Path(case['real']['path']);bundle=E/(name+'-legacy.bundle');git(name+'-bundle',['bundle','create',bundle,'refs/heads/main','refs/heads/beads-backup'],real);git(name+'-bundle-verify',['bundle','verify',bundle],real)
 for role,data in case['roots'].items():
  root=Path(data['path']);configured=git(name+'-'+role+'-configured-hooks',['config','--local','--get','core.hooksPath'],root,(0,1)).decode().strip() or None
  effective=git(name+'-'+role+'-effective-hook',['rev-parse','--path-format=absolute','--git-path','hooks/pre-push'],root).decode().strip();hook=Path(effective)
  common=Path(data['git_common_dir']);gitdir=git(name+'-'+role+'-git-dir',['rev-parse','--path-format=absolute','--git-dir'],root).decode().strip()
  hook_inventory[name+'/'+role]=dict(configured_hooksPath=configured,effective_pre_push=effective,exists=hook.is_file(),sha256=sha(hook.read_bytes()) if hook.is_file() else None,mode=hook.stat().st_mode & 0o777 if hook.is_file() else None,git_dir=gitdir,git_common_dir=str(common),common_fence_marker_absent=not (common/'overgate-bd-legacy-fence.json').exists(),native_bd_used=data['native_cli_called'])
  for rel in ['.beads','.bd-intents']:
   base=root/rel
   if base.is_dir():
    for p in base.rglob('*'):
     if p.is_file():paths.append((p,name+'/'+role+'/'+p.relative_to(root).as_posix()))
  if (root/'.git').is_file():paths.append((root/'.git',name+'/'+role+'/.git'))
  else:
   for rel in ['.git/config','.git/index','.git/HEAD','.git/info/exclude','.git/hooks/pre-push','.overgate/install-state.json']:
    p=root/rel
    if p.is_file():paths.append((p,name+'/'+role+'/'+rel))
   receipt=root/'.git/bd-receipts'
   if receipt.is_dir():
    for p in receipt.rglob('*'):
     if p.is_file():paths.append((p,name+'/'+role+'/'+p.relative_to(root).as_posix()))
save('effective-hooks-common-dir',hook_inventory)
pack=E/'frozen-b4-pre-state.zip';entries={}
with zipfile.ZipFile(pack,'w',compression=zipfile.ZIP_DEFLATED) as archive:
 for p,n in paths:
  b=p.read_bytes();archive.writestr(n,b);entries[n]=dict(sha256=sha(b),bytes=len(b),mode=p.stat().st_mode & 0o777)
with zipfile.ZipFile(pack) as archive:assert set(archive.namelist())==set(entries) and all(sha(archive.read(n))==v['sha256'] for n,v in entries.items())
save('frozen-b4-pre-state-manifest',dict(files=entries,zip_sha256=sha(pack.read_bytes()),zip_bytes=pack.stat().st_size,every_byte_verified=True,candidate='NOT RUN'))
save('environment',dict(role='Windows QA',model='Codex GPT-6',time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),os=platform.platform(),python=sys.version,candidate_source_sha=None))
repo=Path('D:/CodexArtifacts/overgate-rc5-beads-winqa-20261104/evidence-repo');sub='wib/b4/prep-20261105';dest=repo/sub;assert not dest.exists();dest.mkdir(parents=True)
for name in ['prepare.py','freeze_deliver.py','REPORT.md','plan-source.md']:shutil.copyfile(R/name,dest/name)
for name in ['evidence','inputs']:shutil.copytree(R/name,dest/name)
def dg(*args):return subprocess.check_output(['git',*args],cwd=repo,stderr=subprocess.STDOUT)
print(dg('switch','-c','qa/wib-b4-prep-20261105').decode(),flush=True)
dg('-c','core.autocrlf=false','add','--',sub);dg('commit','-q','-m','evidence: Windows B4 populated legacy writer and negative fixtures PREP ONLY')
head=dg('rev-parse','HEAD').decode().strip();z=zipfile.ZipFile(io.BytesIO(dg('-c','core.autocrlf=false','archive','--format=zip',head+':'+sub)));names=[n for n in z.namelist() if not n.endswith('/')];bad=[n for n in names if z.read(n)!=(dest/n).read_bytes()];assert not bad,bad
print(json.dumps(dict(commit=head,files=len(names),byte_mismatches=len(bad),frozen_native_files=len(entries),zip_sha256=sha(pack.read_bytes()),candidate='NOT RUN')),flush=True)
print(dg('-c','http.version=HTTP/1.1','push','--porcelain','-u','origin','HEAD').decode(),flush=True)
(R/'delivery.json').write_text(json.dumps(dict(commit=head,files=len(names),byte_mismatches=0,path=sub),indent=2)+'\n',encoding='utf-8')
