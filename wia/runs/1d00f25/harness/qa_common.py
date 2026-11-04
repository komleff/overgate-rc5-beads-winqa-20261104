from pathlib import Path
import hashlib,json,os,subprocess,time
B=Path(__file__).resolve().parent
PIN='1d00f257202dbced5894b841e97f1945dad7a158'
R=B/'run-1d00f25'
E=R/'evidence'
E.mkdir(parents=True,exist_ok=True)
PRIMARY=B/'actor-a'
PUBLISHER=B/'actor-b'
LINKED=B/'linked'
BD=Path('D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe')
BASH='C:/Program Files/Git/bin/bash.exe'
ENV=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',BD_BIN=str(BD),
 PATH='C:\\Program Files\\Git\\bin;C:\\Program Files\\Git\\usr\\bin;'+os.environ['PATH'])
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_NAMESPACE','CLAUDE_PROJECT_DIR']:
 ENV.pop(k,None)
for k in list(ENV):
 if k.startswith(('BEADS_','BD_','DOLT_','OTEL_')):ENV.pop(k,None)
ENV['BD_BIN']=str(BD)
def sha(b):return hashlib.sha256(b).hexdigest()
def decode(b):
 try:return b.decode('utf-8')
 except UnicodeDecodeError:return b.decode('cp1251',errors='replace')
def save(name,value):
 (E/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(label,args,cwd=PUBLISHER,input=None,expected=(0,),timeout=120,env=None):
 start=time.time()
 p=subprocess.run(list(map(str,args)),cwd=cwd,env=env or ENV,input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
 (E/(label+'.stdout.bin')).write_bytes(p.stdout)
 (E/(label+'.stderr.bin')).write_bytes(p.stderr)
 value=dict(argv=list(map(str,args)),cwd=str(cwd),exit_code=p.returncode,expected_exit=list(expected),seconds=round(time.time()-start,3),
  stdout_sha256=sha(p.stdout),stderr_sha256=sha(p.stderr),stdout=decode(p.stdout),stderr=decode(p.stderr))
 save(label,value)
 if p.returncode not in expected:
  save('FIRST-FAIL',dict(case=label,source=PIN,reason='unexpected exit',receipt=value))
  raise RuntimeError(f'STOP {label}: rc={p.returncode}, stderr={value["stderr"]}')
 return p
def git(label,args,cwd=PUBLISHER,**kw):return run(label,['git',*args],cwd,**kw)
def bash(label,args,cwd=PUBLISHER,**kw):return run(label,[BASH,*args],cwd,**kw)
def text(p):return decode(p.stdout).strip()
def check(label,condition,details):
 save(label,dict(result='PASS' if condition else 'FAIL',details=details))
 if not condition:
  save('FIRST-FAIL',dict(case=label,source=PIN,reason=details))
  raise RuntimeError('STOP '+label)
