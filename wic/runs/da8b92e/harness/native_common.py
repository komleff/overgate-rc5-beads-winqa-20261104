from pathlib import Path
import os,subprocess,json,hashlib,time
B=Path(__file__).resolve().parent
PIN='da8b92e5b83dab0951775f117f0241b84d5a4f76'
SRC=B/'source-da8b92e'
R=B/'run-da8b92e'
E=R/'evidence';E.mkdir(parents=True,exist_ok=True)
BASH='C:/Program Files/Git/bin/bash.exe'
ENV=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PATH='C:\\Program Files\\Git\\bin;C:\\Program Files\\Git\\usr\\bin;'+os.environ['PATH'])
for k in list(ENV):
 if k.startswith(('BEADS_','BD_','DOLT_')) or k in ['CLAUDE_PROJECT_DIR','GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','OVERGATE_COMMIT_GATE_TEST_MAX_SECONDS']:ENV.pop(k,None)
def sha(x):return hashlib.sha256(x).hexdigest()
def decode(x):
 try:return x.decode('utf-8')
 except UnicodeDecodeError:return x.decode('cp1251',errors='replace')
def save(n,x):(E/(n+'.json')).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(n,args,cwd=R,data=None,expected=(0,),env=None,timeout=90):
 t=time.time();p=subprocess.run(list(map(str,args)),cwd=cwd,env=env or ENV,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
 (E/(n+'.stdout.bin')).write_bytes(p.stdout);(E/(n+'.stderr.bin')).write_bytes(p.stderr)
 receipt=dict(argv=list(map(str,args)),cwd=str(cwd),exit_code=p.returncode,expected_exit=list(expected),seconds=round(time.time()-t,3),stdout=decode(p.stdout),stderr=decode(p.stderr),stdout_sha256=sha(p.stdout),stderr_sha256=sha(p.stderr))
 save(n,receipt)
 if p.returncode not in expected:
  save('STOP-'+n,receipt);raise RuntimeError('STOP '+n+' '+str(p.returncode)+' '+receipt['stderr'])
 return p
def check(n,condition,detail):
 save(n,dict(result='PASS' if condition else 'FAIL',details=detail))
 if not condition:raise RuntimeError('STOP '+n)
def hook(n,entry,command,cwd,expected=0,env=None):
 payload=json.dumps(dict(tool_name='Bash',tool_input=dict(command=command),cwd=str(cwd)),ensure_ascii=False).encode('utf-8')
 (E/(n+'.payload.json')).write_bytes(payload)
 return run(n,[BASH,'-c',entry],cwd,payload,(expected,),env=env)
