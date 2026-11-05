from pathlib import Path
import os,sys,subprocess,json,hashlib,time,platform
R=Path(__file__).resolve().parent;E=R/'evidence';E.mkdir(exist_ok=True);I=R/'inputs';I.mkdir(exist_ok=True);C=R/'cases';C.mkdir(exist_ok=True)
BD=Path('D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe')
ENV=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0')
for k in list(ENV):
 if k.startswith(('BEADS_','BD_','DOLT_','GIT_CONFIG','GIT_AUTHOR_','GIT_COMMITTER_')) or k in ['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_NAMESPACE','CLAUDE_PROJECT_DIR']:ENV.pop(k,None)
ENV.update(BD_BIN=str(BD),GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_NOSYSTEM='1')
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,v):(E/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(n,args,cwd=R,expected=0):
 t=time.time();q=subprocess.run(list(map(str,args)),cwd=cwd,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
 for kind,b in [('stdout',q.stdout),('stderr',q.stderr)]:(E/(n+'.'+kind+'.bin')).write_bytes(b)
 save(n,dict(argv=list(map(str,args)),cwd=str(cwd),exit_code=q.returncode,seconds=round(time.time()-t,3),stdout=q.stdout.decode('utf-8','replace'),stderr=q.stderr.decode('utf-8','replace'),stdout_sha256=sha(q.stdout),stderr_sha256=sha(q.stderr)))
 assert q.returncode==expected,n+': '+str(q.returncode)+' '+q.stderr.decode('utf-8','replace')
 return q.stdout
def git(n,args,cwd=R,expected=0):return run(n,['git',*args],cwd,expected)
def files(root):return {p.relative_to(root).as_posix():dict(sha256=sha(p.read_bytes()),bytes=p.stat().st_size,mode=p.stat().st_mode & 0o777) for p in sorted(root.rglob('*')) if p.is_file()}
assert sha(BD.read_bytes())=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de'
version=run('bd-version-only',[BD,'--version']).decode().strip()
base=R/'neutral-origin.git';git('base-init',['init','--bare','--initial-branch=main',base])
seed=R/'seed';git('seed-init',['init','--initial-branch=main',seed]);git('seed-name',['config','user.name','Windows B3 recovery fixture'],seed);git('seed-email',['config','user.email','qa-b3@example.invalid'],seed)
(seed/'README.md').write_bytes(b'Neutral Windows B3 recovery fixture. No candidate code, DB or task.\n')
git('seed-add',['add','README.md'],seed);git('seed-commit',['commit','-m','fixture: neutral main for B3 recovery preparation'],seed)
main=git('seed-head',['rev-parse','HEAD'],seed).decode().strip();git('seed-origin',['remote','add','origin',base.as_posix()],seed);git('seed-push',['push','origin','main'],seed)
git('neutral-bundle',['bundle','create',E/'neutral-main.bundle','refs/heads/main'],base);git('neutral-bundle-verify',['bundle','verify',E/'neutral-main.bundle'],base)
scenarios={
 'after-peer-init':'Interrupt after candidate peer-init, before first publication; verify documented bounded recovery on exact source',
 'after-publisher-setup':'Interrupt after candidate publisher setup; preserve exact control/config/store and test reviewed recovery',
 'after-bootstrap':'Interrupt after candidate bootstrap; preserve exact queue/base/actor and test reviewed recovery',
 'after-push':'Interrupt after real remote advancement; preserve R/ledger/receipt and test exact-SHA readback/retry without duplicate mutation',
 'pre-init-no-identity':'Publisher intentionally lacks repo-local user identity; candidate must STOP before control/DB write',
 'pre-init-no-https-helper':'No credential helper; synthetic HTTPS auth preflight input only, no external authenticated push',
 'wrong-remote-count':'Inherited COUNT URL+pushurl attacker inputs; candidate must bind true real origin, preserve attacker absence'}
manifest={};runtime_paths=['.beads','.bd-intents','.git/bd-receipts','.git/bd-apply.lock.d','.git/overgate-bd-managed','.git/overgate-bd-publisher-control']
for name,expected in scenarios.items():
 root=C/name;root.mkdir();real=root/'real.git';attacker=root/'attacker.git'
 git(name+'-real',['clone','--bare','--no-hardlinks',base,real]);git(name+'-attacker',['clone','--bare','--no-hardlinks',real,attacker])
 clones={}
 for role in ['primary','publisher','peer']:
  target=root/role;git(name+'-'+role+'-clone',['clone','--no-hardlinks','-c','core.autocrlf=false',real.as_posix(),target])
  identity=not (name=='pre-init-no-identity' and role=='publisher')
  if identity:
   git(name+'-'+role+'-name',['config','user.name','Windows B3 '+role],target);git(name+'-'+role+'-email',['config','user.email','qa-b3-'+role+'@example.invalid'],target)
  head=git(name+'-'+role+'-head',['rev-parse','HEAD'],target).decode().strip();assert head==main
  index=git(name+'-'+role+'-index',['ls-files','-s','-z'],target);status=git(name+'-'+role+'-status',['status','--porcelain=v1','-z'],target);assert not status
  origin=git(name+'-'+role+'-origin',['remote','get-url','origin'],target).decode().strip();assert origin==real.as_posix()
  absent={p:not (target/p).exists() for p in runtime_paths};assert all(absent.values())
  clones[role]=dict(root=str(target),head=head,index_sha256=sha(index),status_sha256=sha(status),status='clean',origin=origin,local_identity_present=identity,runtime_paths_absent=absent,files=files(target))
 real_refs=git(name+'-real-refs',['for-each-ref','--format=%(refname) %(objectname)'],real).decode();attacker_refs=git(name+'-attacker-refs',['for-each-ref','--format=%(refname) %(objectname)'],attacker).decode();assert real_refs==attacker_refs=='refs/heads/main '+main+'\n'
 inputs=dict(case=name,expected_checkpoint=expected,interruption_mechanism='NOT SELECTED: bind to forthcoming exact source/API; no candidate executed',spoof_env=dict(GIT_CONFIG_COUNT='2',GIT_CONFIG_KEY_0='remote.origin.url',GIT_CONFIG_VALUE_0=attacker.as_posix(),GIT_CONFIG_KEY_1='remote.origin.pushurl',GIT_CONFIG_VALUE_1=attacker.as_posix()),synthetic_https_origin='https://b3-synthetic.example.invalid/project.git',candidate_status='NOT RUN')
 (I/(name+'.json')).write_text(json.dumps(inputs,indent=2)+'\n',encoding='utf-8')
 manifest[name]=dict(purpose=expected,real=dict(path=str(real),refs=real_refs,task_R=None,files=files(real)),attacker=dict(path=str(attacker),refs=attacker_refs,task_R=None,files=files(attacker)),clones=clones,input_sha256=sha((I/(name+'.json')).read_bytes()))
save('prep-ready',dict(role='Windows QA',model='Codex GPT-6',authority='PR12#6646261824',os=platform.platform(),status='PREP READY ONLY',runtime_source_sha=None,neutral_main=main,native_bd=dict(path=str(BD),version=version,sha256=sha(BD.read_bytes())),cases=manifest,candidate_installed=False,bd_init=False,activation=False,interruption=False,recovery=False,publication=False,spoof_inputs_executed=False,working_project_used=False))
table='\n'.join('| '+n+' | '+p+' | PREP READY / runtime NOT RUN |' for n,p in scenarios.items())
(R/'REPORT.md').write_text('# WINDOWS QA → PM / WI-B B3 recovery PREP READY\n\nWindows QA / Codex GPT-6. Authority PR12#6646261824. Candidate exact SHA/fingerprint has not been issued.\n\nSeven completely independent real+attacker bare pairs and 21 standalone clones share neutral synthetic main `'+main+'`; every task ref, local DB/queue/receipt/control absent; every HEAD/index/status/origin and per-file SHA256 frozen in evidence/prep-ready.json. Publisher local identity is intentionally absent only in its dedicated negative slot. No candidate file was copied and no source script/setup/bootstrap/activation/fault/recovery/publication ran. Only native bd --version and executable hash qualification.\n\n| Fixture | Intended bounded checkpoint after exact RUN | Current result |\n|---|---|---|\n'+table+'\n\nLogical fault labels are input data, not guessed candidate flags. Mechanisms and expected recovery will bind to the forthcoming source contract; B4 legacy/fence remains separate. COUNT URL/pushurl and synthetic HTTPS inputs are unexecuted; no real credential or network write. Native origin locators use consistent forward-slash literal spelling. Original WI-A archive52693ea and prior preparation archives remain immutable. No working Tune-Heroes/U2/OverGate DB/settings/hooks, merge/release/finalize used.\n',encoding='utf-8')
print(json.dumps(dict(status='PREP READY ONLY',cases=len(manifest),standalone_clones=3*len(manifest),neutral_main=main,candidate='NOT RUN',runtime_pin=None)),flush=True)
