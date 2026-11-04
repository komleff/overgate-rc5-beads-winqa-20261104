from pathlib import Path
import os,sys,subprocess,json,hashlib,time,platform
R=Path(__file__).resolve().parent;E=R/'evidence';E.mkdir(exist_ok=True);I=R/'inputs';I.mkdir(exist_ok=True)
REAL=R/'real-origin.git';ATTACK=R/'attacker-origin.git';BD=Path('D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe')
ENV=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0')
for k in list(ENV):
 if k.startswith(('BEADS_','BD_','DOLT_','GIT_CONFIG')) or k in ['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_NAMESPACE','CLAUDE_PROJECT_DIR']:ENV.pop(k,None)
ENV['BD_BIN']=str(BD)
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,obj):(E/(n+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(n,args,cwd=R):
 t=time.time();q=subprocess.run(list(map(str,args)),cwd=cwd,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
 for kind,data in [('stdout',q.stdout),('stderr',q.stderr)]:(E/(n+'.'+kind+'.bin')).write_bytes(data)
 save(n,dict(argv=list(map(str,args)),cwd=str(cwd),exit_code=q.returncode,seconds=round(time.time()-t,3),stdout=q.stdout.decode('utf-8','replace'),stderr=q.stderr.decode('utf-8','replace'),stdout_sha256=sha(q.stdout),stderr_sha256=sha(q.stderr)))
 assert q.returncode==0,n+': '+q.stderr.decode('utf-8','replace')
 return q.stdout
def git(n,args,cwd=R):return run(n,['git',*args],cwd)
def files(root):
 return {p.relative_to(root).as_posix():dict(sha256=sha(p.read_bytes()),bytes=p.stat().st_size,mode=p.stat().st_mode & 0o777) for p in sorted(root.rglob('*')) if p.is_file()}
assert sha(BD.read_bytes())=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de'
version=run('native-bd-version-only',[BD,'--version']).decode().strip()
git('real-init',['init','--bare','--initial-branch=main',REAL])
seed=R/'seed';git('seed-init',['init','--initial-branch=main',seed]);git('seed-name',['config','user.name','Windows wrong-remote fixture'],seed);git('seed-email',['config','user.email','qa-windows@example.invalid'],seed)
(seed/'README.md').write_bytes(b'Neutral disposable Windows wrong-remote fixture. Candidate NOT RUN.\n')
git('seed-add',['add','README.md'],seed);git('seed-commit',['commit','-m','fixture: neutral main, no candidate or task state'],seed)
main=git('seed-head',['rev-parse','HEAD'],seed).decode().strip();git('seed-origin',['remote','add','origin',REAL],seed);git('seed-push',['push','origin','main'],seed)
git('attacker-mirror',['clone','--mirror','--no-hardlinks',REAL,ATTACK])
clones={}
for name in ['primary','publisher','peer']:
 root=R/name;git(name+'-clone',['clone','--no-hardlinks','-c','core.autocrlf=false',REAL,root]);git(name+'-name',['config','user.name','Windows '+name],root);git(name+'-email',['config','user.email',name+'@example.invalid'],root)
 actual=git(name+'-head',['rev-parse','HEAD'],root).decode().strip();assert actual==main
 origin=git(name+'-origin',['remote','get-url','origin'],root).decode().strip();assert Path(origin).resolve()==REAL.resolve()
 assert not (root/'.beads').exists() and not (root/'.bd-intents').exists()
 common=git(name+'-common',['rev-parse','--path-format=absolute','--git-common-dir'],root).decode().strip()
 clones[name]=dict(path=str(root),head=actual,origin=origin,git_common_dir=common,files=files(root),local_DB='absent',queues='absent',receipts='absent',managed_registration='absent')
real_refs=git('real-refs',['for-each-ref','--format=%(refname) %(objectname)'],REAL).decode();attack_refs=git('attacker-refs',['for-each-ref','--format=%(refname) %(objectname)'],ATTACK).decode()
assert real_refs==attack_refs=='refs/heads/main '+main+'\n'
global_file=I/'attacker-global.gitconfig';global_file.write_text('[remote "origin"]\n\turl = '+ATTACK.as_posix()+'\n\tpushurl = '+ATTACK.as_posix()+'\n',encoding='utf-8',newline='\n')
env_inputs={
 'COUNT':{'GIT_CONFIG_COUNT':'2','GIT_CONFIG_KEY_0':'remote.origin.url','GIT_CONFIG_VALUE_0':ATTACK.as_posix(),'GIT_CONFIG_KEY_1':'remote.origin.pushurl','GIT_CONFIG_VALUE_1':ATTACK.as_posix()},
 'PARAMETERS':{'GIT_CONFIG_PARAMETERS':"'remote.origin.url="+ATTACK.as_posix()+"' 'remote.origin.pushurl="+ATTACK.as_posix()+"'"},
 'GLOBAL':{'GIT_CONFIG_GLOBAL':str(global_file)},
 'status':'PREPARED INPUTS ONLY; never set in any executed child; global-vs-local precedence has not been qualified'}
(I/'spoof-env-inputs.json').write_text(json.dumps(env_inputs,indent=2)+'\n',encoding='utf-8')
git('neutral-main-bundle',['bundle','create',E/'neutral-main.bundle','refs/heads/main'],REAL);git('neutral-main-bundle-verify',['bundle','verify',E/'neutral-main.bundle'],REAL)
manifest=dict(role='Windows QA',model='Codex GPT-6',status='PREP READY; candidate runtime NOT RUN',os=platform.platform(),runtime_source_sha=None,neutral_fixture_main=main,
 origins={'real':dict(path=str(REAL),refs=real_refs,files=files(REAL),beads_backup='absent'),'attacker':dict(path=str(ATTACK),refs=attack_refs,files=files(ATTACK),beads_backup='absent')},clones=clones,
 native_bd=dict(path=str(BD),version=version,sha256=sha(BD.read_bytes())),input_hashes={p.name:sha(p.read_bytes()) for p in I.iterdir() if p.is_file()},
 candidate_installed=False,publisher_setup=False,bd_init=False,task_calls=False,spoof_inputs_executed=False,activation=False,publication=False,working_project_used=False,
 next='Exact WI-A source/fingerprint RUN required; COUNT/PARAMETERS/GLOBAL actual native tests then; B3 partial-init recovery separate')
save('prep-ready',manifest)
(R/'REPORT.md').write_text('# WINDOWS QA → PM / wrong-remote fixture PREP READY\n\nWindows QA / Codex GPT-6. Authority: PR12#6644267687. No candidate runtime source pin issued.\n\nNew isolated real/attacker bare origins mirror only neutral synthetic main `'+main+'`; both beads-backup refs absent. Three independent primary/publisher/peer clones point to real origin, no local DB/queues/receipts/registration. Complete native Git raw outputs and per-file SHA256/modes frozen in evidence/prep-ready.json; self-contained neutral-main.bundle verified. Native bd1.2.2 executable SHA256 verified; only --version executed.\n\nCOUNT/KEY/VALUE, PARAMETERS and GLOBAL inputs prepared as test data, not executed; no claim about GLOBAL/local precedence or native security result. New source setup/bootstrap, actual task mutation, publisher execution, activation, security negative, partial-init recovery and publication: **NOT RUN**. Prior 65f21ed immutable archive remains unchanged.\n\nNext: await PM exact WI-A SHA/fingerprint bounded RUN; actual native Windows negative must keep attacker R absent and bind real R/peer exact. No working U2/Toon/OverGate state or hooks/settings, merge/release/finalize used.\n',encoding='utf-8')
print(json.dumps(dict(status='PREP READY',neutral_main=main,source='NOT ISSUED',candidate='NOT RUN',real_R=None,attacker_R=None,db='absent',clones=list(clones))),flush=True)
