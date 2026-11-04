from pathlib import Path
import os,sys,subprocess,json,hashlib,uuid,time
B=Path(__file__).resolve().parent;E=B/'evidence';E.mkdir(exist_ok=True)
BD=Path('D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe')
OLD=Path('D:/CodexArtifacts/overgate-rc5-wic-winqa-20261105/released-source')
OLDPIN='3f3246c3a3b62377fc02aad05283cae1ef5d4e2d'
ORIGIN=B/'origin.git';PRIMARY=B/'fresh-install-pr';PUBLISHER=B/'publisher-after-merge';PEER=B/'peer';LINKED=B/'linked'
ENV=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PATH=str(BD.parent)+';C:\\Program Files\\Git\\bin;C:\\Program Files\\Git\\usr\\bin;'+os.environ['PATH'])
for k in list(ENV):
 if k.startswith(('BEADS_','BD_','DOLT_')) or k in ['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_NAMESPACE','CLAUDE_PROJECT_DIR']:ENV.pop(k,None)
ENV['BD_BIN']=str(BD)
def sha(x):return hashlib.sha256(x).hexdigest()
def save(n,v):(E/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(n,args,cwd=B,data=None,expected=0):
 t=time.time();r=subprocess.run(list(map(str,args)),cwd=cwd,env=ENV,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=240)
 (E/(n+'.stdout.bin')).write_bytes(r.stdout);(E/(n+'.stderr.bin')).write_bytes(r.stderr)
 receipt=dict(argv=list(map(str,args)),cwd=str(cwd),exit_code=r.returncode,expected_exit=expected,seconds=round(time.time()-t,3),stdout=r.stdout.decode('utf-8','replace'),stderr=r.stderr.decode('utf-8','replace'),stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
 save(n,receipt)
 if r.returncode!=expected:save('PREP-STOP',receipt);raise RuntimeError('STOP '+n+' '+str(r.returncode)+' '+receipt['stderr'])
 return r.stdout
def git(n,args,cwd=B,**kw):return run(n,['git',*args],cwd,**kw)
def init(n,root):
 assert not root.exists(),root
 git(n+'-init',['init','--initial-branch=qa/preparation',root])
 git(n+'-name',['config','user.name','Windows WI-B QA'],root);git(n+'-email',['config','user.email','qa-wib@example.invalid'],root)
 (root/'README.md').write_text('Disposable WI-B fixture. No candidate executed.\n',encoding='utf-8')
 git(n+'-add',['add','README.md'],root);git(n+'-commit',['-c','commit.gpgsign=false','commit','-m','fixture: neutral preparation'],root)
def repo_state(n,root):
 return dict(path=str(root),head=git(n+'-head',['rev-parse','HEAD'],root).decode().strip(),common=git(n+'-common',['rev-parse','--path-format=absolute','--git-common-dir'],root).decode().strip(),
  index_sha256=sha(git(n+'-index',['ls-files','-s','-z'],root)),has_dolt=(root/'.beads/dolt').exists())
assert sha(BD.read_bytes())=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de'
version=run('native-bd-version',[BD,'--version']).decode().strip()
assert sha((B/'plan-source.md').read_bytes())=='c4aa4143159b0abceef911a4917c45f47f79a8802eff7a1556de8e7343c50af4'
git('origin-init',['init','--bare','--initial-branch=qa/preparation',ORIGIN])
seed=B/'seed';init('seed',seed);git('seed-origin',['remote','add','origin',ORIGIN],seed);git('seed-push',['push','origin','qa/preparation'],seed)
for n,root in [('fresh',PRIMARY),('publisher',PUBLISHER),('peer',PEER)]:
 git(n+'-clone',['clone','--no-hardlinks','-c','core.autocrlf=false',ORIGIN,root])
 git(n+'-name',['config','user.name','Windows WI-B '+n],root);git(n+'-email',['config','user.email','qa-'+n+'@example.invalid'],root)
git('fresh-pr-branch',['switch','-c','qa/install-fixture'],PRIMARY)
git('linked-worktree',['worktree','add','-b','qa/linked',LINKED,'qa/install-fixture'],PRIMARY)
slots={}
for n in ['no-beads','custom-conflict-rollback','unknown-remote','unavailable-publisher']:
 root=B/n;init(n,root);slots[n]=str(root)
git('unknown-remote-locator',['remote','add','origin',B/'nonexistent-origin.git'],B/'unknown-remote')
custom=B/'custom-conflict-rollback'
owned={'AGENTS.md':'Project-owned WI-B fixture guidance.\n','.agents/project/verify.sh':'#!/bin/sh\nexit 0\n','.memory-bank/project-owned.md':'Project memory: preserve bytes.\n','.claude/settings.local.json':json.dumps({'env':{'WI_B_PROJECT_MARKER':'preserve'}})+'\n'}
for name,data in owned.items():
 target=custom/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(data,encoding='utf-8',newline='\n')
save('project-owned-before',{name:sha((custom/name).read_bytes()) for name in owned})
plans=B/'released-baseline-plans';plans.mkdir()
contract=B/'released-baseline-contract.md';contract.write_text('Synthetic disposable baseline only; preserve project README; candidate WI-B not executed.\n',encoding='utf-8')
PR='https://github.com/example/project/pull/1'
baselines={}
for name,no_beads in [('legacy-empty',False),('legacy-pending',False),('beads-false-upgrade',True)]:
 target=B/name;init(name,target)
 plan=plans/(name+'.plan.json');approval=plans/(name+'.synthetic-approval.json')
 args=[sys.executable,OLD/'scripts/install-overgate.py','plan','--source',OLD,'--source-sha',OLDPIN,'--target',target,'--contract',contract,'--target-pr',PR,'--output',plan]
 if no_beads:args+=['--no-beads']
 run(name+'-released-plan',args);state=json.loads(plan.read_bytes());assert not state['conflicts']
 approval.write_text(json.dumps(dict(verdict='PLAN_READY',plan_sha256=sha(plan.read_bytes()),evidence=PR+'#synthetic-fixture-only'))+'\n',encoding='utf-8')
 run(name+'-released-apply',[sys.executable,OLD/'scripts/install-overgate.py','apply','--plan',plan,'--approval',approval])
 state=json.loads((target/'.overgate/install-state.json').read_bytes());assert state['beads']==(not no_beads) and 'beads_protocol' not in state
 baselines[name]=dict(path=str(target),source=OLDPIN,beads=state['beads'],protocol_field_present=False)
legacy=B/'legacy-pending';legacy_origin=B/'legacy-origin.git'
git('legacy-origin-init',['init','--bare','--initial-branch=qa/preparation',legacy_origin]);git('legacy-origin-add',['remote','add','origin',legacy_origin],legacy)
run('legacy-native-init',[BD,'--sandbox','init','--prefix','wib-qa','--skip-agents','--skip-hooks','--non-interactive','--remote',''],legacy)
def bd(n,args):return json.loads(run(n,[BD,'--sandbox',*args],legacy))
a=bd('legacy-create-owner',['create','--title','WI-B legacy synthetic owner','--type','task','--priority','2','--description','Preserve legacy data\nКириллица','--labels','wib-qa,legacy','--metadata',json.dumps({'phase':'baseline','typed':[1,True,None]}),'--json'])
b=bd('legacy-create-peer',['create','--title','WI-B legacy synthetic peer','--type','bug','--priority','1','--json'])
if isinstance(a,list):a=a[0]
if isinstance(b,list):b=b[0]
bd('legacy-native-comment',['comments','add',a['id'],'Preserve comment\nКомментарий','--json'])
bd('legacy-native-edge',['dep','add',a['id'],b['id'],'--type','discovered-from','--json'])
export=E/'legacy-before.jsonl';run('legacy-native-export',[BD,'--sandbox','export','--all','--output',export],legacy)
# Commit only fixture files; real local embedded DB and pending runtime data stay outside Git.
git('legacy-code-add',['add','--all','--','.',':!.beads',':!.bd-intents',':!.overgate-backups'],legacy)
git('legacy-code-commit',['-c','commit.gpgsign=false','commit','-m','fixture: released rc4.1 legacy payload'],legacy)
git('legacy-code-push',['push','origin','qa/preparation'],legacy)
idx=B/'legacy-snapshot.index';index_env=dict(ENV,GIT_INDEX_FILE=str(idx))
def index_git(n,args,data=None):
 old_env=globals()['ENV'];globals()['ENV']=index_env
 try:return git(n,args,legacy,data=data)
 finally:globals()['ENV']=old_env
index_git('legacy-snapshot-empty-index',['read-tree','--empty'])
blob=index_git('legacy-snapshot-blob',['hash-object','-w','--stdin'],export.read_bytes()).decode().strip()
index_git('legacy-snapshot-index',['update-index','--add','--cacheinfo','100644,'+blob+',.beads/issues.jsonl'])
tree=index_git('legacy-snapshot-tree',['write-tree']).decode().strip()
remote_r=git('legacy-snapshot-commit',['commit-tree',tree,'-m','fixture: legitimate legacy native export'],legacy).decode().strip()
git('legacy-snapshot-push',['push','origin',remote_r+':refs/heads/beads-backup'],legacy)
oldpeer=B/'legacy-old-writer-peer'
git('legacy-peer-clone',['clone','--no-hardlinks','-c','core.autocrlf=false',legacy_origin,oldpeer])
git('legacy-peer-name',['config','user.name','WI-B old writer peer'],oldpeer);git('legacy-peer-email',['config','user.email','qa-old-writer@example.invalid'],oldpeer)
run('legacy-peer-native-init',[BD,'--sandbox','init','--prefix','wib-qa','--skip-agents','--skip-hooks','--non-interactive','--remote',''],oldpeer)
run('legacy-peer-native-import',[BD,'--sandbox','import',export,'--json'],oldpeer)
actor='agent-'+str(uuid.uuid4())
pending=legacy/'.bd-intents/qa-pending.raw.jsonl';pending.parent.mkdir(exist_ok=True)
pending.write_text(json.dumps(dict(intent_id='wib-retained-pending-001',op='update',ref=a['id'],notes='Retain bytes; no silent replay',actor_owner=actor),ensure_ascii=False)+'\n',encoding='utf-8')
receipts=legacy/'.git/bd-receipts';receipts.mkdir(exist_ok=True)
opaque=receipts/'qa-unknown-receipt.json';opaque.write_text(json.dumps(dict(fixture_only=True,owner=actor,queue_sha256=sha(pending.read_bytes()),status='unreconciled-retained'))+'\n',encoding='utf-8')
save('legacy-frozen-inputs',dict(source=OLDPIN,prefix='wib-qa',ids=[a['id'],b['id']],frozen_remote_R=remote_r,export_sha256=sha(export.read_bytes()),pending_sha256=sha(pending.read_bytes()),pending_owner=actor,receipt_sha256=sha(opaque.read_bytes()),
 pending_status='raw/unreconciled fixture data; never submitted/prepared/replayed; future reviewed adoption needed',known_old_writers=[str(legacy),str(oldpeer)]))
states={n:repo_state('prep-'+n,r) for n,r in [('fresh',PRIMARY),('publisher',PUBLISHER),('peer',PEER),('linked',LINKED),('legacy',legacy),('old-writer-peer',oldpeer)]}
manifest=dict(status='PREP READY; candidate WI-B NOT RUN',plan_source='29edf688d7b7fbdad3122785efcabb1d8406845a',plan_blob='5dedca627bf31916b871d85e88c4906551aaf576',runtime_pin=None,
 root=str(B),origin=str(ORIGIN),states=states,slots=slots,released_baselines=baselines,native_bd=dict(path=str(BD),version=version,sha256=sha(BD.read_bytes())),
 candidate_installed=False,candidate_activation=False,candidate_publication=False,temporary_main_established=False,real_project_DB_used=False,
 fresh_Dolt_absent=not (PRIMARY/'.beads').exists(),baseline_legacy_only=True)
assert manifest['fresh_Dolt_absent']
save('prep-ready',manifest);print(json.dumps(dict(prep='READY',candidate='NOT RUN',frozen_legacy_R=remote_r,native_ids=[a['id'],b['id']])))
