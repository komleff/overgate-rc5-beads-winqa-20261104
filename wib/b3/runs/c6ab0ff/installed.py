from common import *
def install(n,root,existing=False):
 if not existing:
  root.mkdir(parents=True);real=root/'real.git';attacker=root/'attacker.git'
  git(n+'-real',['clone','--bare','--branch','main',PREP/'evidence/neutral-main.bundle',real]);git(n+'-attacker',['clone','--bare','--no-hardlinks',real,attacker])
  for role in ['primary','publisher','peer']:
   target=root/role;git(n+'-'+role+'-clone',['clone','--no-hardlinks','-c','core.autocrlf=false',real.as_posix(),target])
   git(n+'-'+role+'-name',['config','user.name','Windows B3 QA '+role],target);git(n+'-'+role+'-email',['config','user.email','qa-b3-'+role+'@example.invalid'],target)
 else:real=root/'real.git';attacker=root/'attacker.git'
 primary=root/'primary';publisher=root/'publisher';peer=root/'peer';roots={'primary':primary,'publisher':publisher,'peer':peer,'real':real,'attacker':attacker}
 snap(n+'-neutral',roots)
 assert 'beads-backup' not in ref(n+'-neutral-real-refs',real) and 'beads-backup' not in ref(n+'-neutral-attacker-refs',attacker)
 assert all(not (root/'.beads').exists() for root in [primary,publisher,peer])
 git(n+'-install-branch',['switch','-c','qa/install-fixture'],primary)
 plan=P/(n+'.plan.json');approval=P/(n+'.synthetic-approval.json')
 run(n+'-install-plan',[sys.executable,S/'scripts/install-overgate.py','plan','--source',S,'--source-sha',PIN,'--target',primary,'--contract',R/'pr-contract.txt','--target-pr','https://github.com/example/project/pull/1','--output',plan])
 data=json.loads(plan.read_bytes());assert not data['conflicts'] and data['beads_protocol']=='managed-v1' and not data['beads_inventory']['blocked']
 approval.write_text(json.dumps(dict(verdict='PLAN_READY',plan_sha256=sha(plan.read_bytes()),evidence='https://github.com/example/project/pull/1#synthetic-disposable-approval'))+'\n',encoding='utf-8')
 run(n+'-install-apply',[sys.executable,S/'scripts/install-overgate.py','apply','--plan',plan,'--approval',approval])
 assert all(not (target/'.beads').exists() for target in [primary,publisher,peer])
 git(n+'-install-add',['-c','core.autocrlf=false','add','--',*[x['target'] for x in data['operations']],'.overgate/install-state.json'],primary)
 git(n+'-install-commit',['commit','-m','fixture: accepted installed payload; synthetic target main promotion'],primary)
 # Disposable fixture main promotion, not a real-project merge or GitHub PR action.
 git(n+'-fixture-main',['branch','-M','main'],primary);git(n+'-real-main',['push','origin','HEAD:refs/heads/main'],primary);git(n+'-attacker-code-mirror',['push',attacker,'HEAD:refs/heads/main'],primary)
 head=git(n+'-target-head',['rev-parse','HEAD'],primary).decode().strip()
 for role,target in [('publisher',publisher),('peer',peer)]:
  git(n+'-'+role+'-fetch',['fetch','origin','main'],target);git(n+'-'+role+'-main',['-c','core.autocrlf=false','checkout','-B','main','origin/main'],target)
  assert git(n+'-'+role+'-head',['rev-parse','HEAD'],target).decode().strip()==head
  assert not git(n+'-'+role+'-clean',['status','--porcelain','--untracked-files=no'],target).strip()
 state=json.loads((primary/'.overgate/install-state.json').read_bytes());assert state['source_sha']==PIN and state['beads_protocol']=='managed-v1'
 beads=[x for x in json.loads((S/'.agents/distribution-manifest.json').read_bytes())['files'] if x.get('component')=='beads' and x.get('policy')=='managed']
 binding={x['target']:{'source':sha((S/x['source']).read_bytes()),'installed':sha((primary/x['target']).read_bytes())} for x in beads}
 assert all(v['source']==v['installed'] for v in binding.values());save(n+'-installed-binding',dict(source=PIN,target=head,paths=binding,all_local_DB_absent=all(not (target/'.beads').exists() for target in [primary,publisher,peer])))
 return roots,head
def activation_args(roots,work,actor,title):
 return ['--publisher-root',roots['publisher'].as_posix(),'--peer-root',roots['peer'].as_posix(),'--bd-bin',BD.as_posix(),'--prefix','wibqa','--actor',actor,'--title',title,'--work-dir',work.as_posix()]
