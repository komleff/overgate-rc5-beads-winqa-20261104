from pathlib import Path
import os,sys,subprocess,json,hashlib,time,shutil,uuid,traceback
sys.stdout.reconfigure(encoding='utf-8',errors='backslashreplace');sys.stderr.reconfigure(encoding='utf-8',errors='backslashreplace')
R=Path(__file__).resolve().parent;S=R/'source';E=R/'evidence';E.mkdir(exist_ok=True);P=R/'plans';P.mkdir(exist_ok=True);C=R/'cases';C.mkdir(exist_ok=True)
PREP=Path('D:/CodexArtifacts/overgate-rc5-wib-b3-recovery-prep-winqa-20261105')
PIN='5412a8f25fe94f2e6c313357e556717469514f14';BASE='be8b66e7875ac5843e6f40f6e042593fa2f1ebb2';ZERO='0'*40
BD=Path('D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe');BASH='C:/Program Files/Git/bin/bash.exe'
ENV=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',PATH=str(BD.parent)+';C:/Program Files/Git/bin;C:/Program Files/Git/usr/bin;'+os.environ['PATH'])
for k in list(ENV):
 if k.startswith(('BEADS_','BD_','DOLT_','GIT_CONFIG','GIT_AUTHOR_','GIT_COMMITTER_')) or k in ['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_NAMESPACE','CLAUDE_PROJECT_DIR']:ENV.pop(k,None)
ENV.pop('PYTHONUTF8',None);ENV.pop('PYTHONIOENCODING',None)
ENV.update(BD_BIN=str(BD),GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_NOSYSTEM='1')
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,v):(E/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(n,args,cwd=R,expected=0,env=None,data=None,timeout=180):
 qenv=dict(ENV);qenv.update(env or {});t=time.time();q=subprocess.run(list(map(str,args)),cwd=cwd,env=qenv,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
 for k,b in [('stdout',q.stdout),('stderr',q.stderr)]:(E/(n+'.'+k+'.bin')).write_bytes(b)
 def dec(b):
  try:return b.decode('utf-8')
  except UnicodeDecodeError:return b.decode('cp1251','replace')
 save(n,dict(argv=list(map(str,args)),cwd=str(cwd),env_overrides=env or {},exit_code=q.returncode,expected=expected,seconds=round(time.time()-t,3),stdout=dec(q.stdout),stderr=dec(q.stderr),stdout_sha256=sha(q.stdout),stderr_sha256=sha(q.stderr)))
 if expected is not None and q.returncode!=expected:raise AssertionError('native exit '+n+': '+str(q.returncode)+' '+dec(q.stderr))
 return q
def git(n,args,cwd=R,**kw):return run(n,['git',*args],cwd,**kw).stdout
def bash(n,script,args,cwd,**kw):return run(n,[BASH,script,*args],cwd,**kw)
def files(root):
 if not root.exists():return {}
 return {p.relative_to(root).as_posix():dict(sha256=sha(p.read_bytes()),bytes=p.stat().st_size,mode=p.stat().st_mode & 0o777) for p in sorted(root.rglob('*')) if p.is_file()}
def snap(n,roots):
 v={k:files(root) for k,root in roots.items()};save(n,v);return v
def ref(n,root):return git(n,['for-each-ref','--format=%(refname) %(objectname)'],root).decode()
def row(n,ac,result,method,evidence):
 p=E/'results.json';v=json.loads(p.read_bytes()) if p.exists() else [];v.append(dict(case=n,ac=ac,result=result,method=method,evidence=evidence));save('results',v);print(n+': '+result,flush=True)
def guard(main):
 try:main()
 except BaseException as ex:save('STOP',dict(source=PIN,error=str(ex),traceback=traceback.format_exc()));print(traceback.format_exc(),flush=True);raise
