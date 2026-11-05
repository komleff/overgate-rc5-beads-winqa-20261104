from common import *
def main():
 for variant in (sys.argv[1:] or ['count-url','parameters-url','global-rewrite','count-rewrite']):
  effective=variant.startswith('effective-');mode=variant.removeprefix('effective-')
  n='native-'+variant
  if mode=='count-url' and not effective:
   root=PREP;real=root/'real-origin.git';attacker=root/'attacker-origin.git';primary=root/'primary';publisher=root/'publisher';peer=root/'peer'
  else:
   root=C/n;root.mkdir();real=root/'real.git';attacker=root/'attacker.git'
   git(n+'-real',['clone','--bare','--branch','main',PREP/'evidence/neutral-main.bundle',real])
   git(n+'-attacker',['clone','--bare','--no-hardlinks',real,attacker])
   primary=root/'primary';publisher=root/'publisher';peer=root/'peer'
   for role,target in [('primary',primary),('publisher',publisher),('peer',peer)]:
    git(n+'-'+role+'-clone',['clone','--no-hardlinks','-c','core.autocrlf=false',real,target])
    git(n+'-'+role+'-name',['config','user.name','Windows native security QA'],target);git(n+'-'+role+'-email',['config','user.email','qa-native@example.invalid'],target)
  if effective:
   for role,target in [('primary',primary),('publisher',publisher),('peer',peer)]:git(n+'-'+role+'-literal-locator',['remote','set-url','origin',real.as_posix()],target)
  roots={'primary':primary,'publisher':publisher,'peer':peer,'real':real,'attacker':attacker}
  initial=snap(n+'-neutral-before',roots)
  assert refs(n+'-initial-real',real)==refs(n+'-initial-attacker',attacker)
  assert 'beads-backup' not in refs(n+'-initial-real-task-check',real)
  for target in [primary,publisher,peer]:assert not (target/'.beads').exists() and not (target/'.bd-intents').exists()
  # Synthetic fixture promotion only: committed exact candidate helper bytes on disposable main.
  shutil.copytree(S/'scripts',primary/'scripts');shutil.copytree(S/'.claude/tools',primary/'.claude/tools')
  git(n+'-code-add',['-c','core.autocrlf=false','add','--','scripts','.claude/tools'],primary)
  git(n+'-code-commit',['commit','-m','fixture: exact frozen Windows managed helpers'],primary)
  run(n+'-primary-native-init',[BD,'--sandbox','init','--prefix','wqa','--skip-agents','--skip-hooks','--non-interactive','--remote',''],primary)
  fixture_head=git(n+'-fixture-head',['rev-parse','HEAD'],primary).decode().strip()
  git(n+'-real-main',['push','origin','HEAD:refs/heads/main'],primary)
  git(n+'-attacker-main-mirror',['push',attacker,'HEAD:refs/heads/main'],primary)
  for role,target in [('publisher',publisher),('peer',peer)]:
   git(n+'-'+role+'-fetch',['fetch','origin','main'],target)
   git(n+'-'+role+'-checkout',['-c','core.autocrlf=false','checkout','-B','main','origin/main'],target)
   assert git(n+'-'+role+'-head',['rev-parse','HEAD'],target).decode().strip()==fixture_head
  paths=git(n+'-runtime-list',['ls-tree','-r','--name-only',PIN,'--','scripts','.claude/tools'],S).decode().splitlines()
  binding={p:dict(source=sha((S/p).read_bytes()),installed=sha((publisher/p).read_bytes())) for p in paths}
  assert all(v['source']==v['installed'] for v in binding.values());save(n+'-runtime-byte-binding',dict(source=PIN,target=fixture_head,paths=binding))
  helper=root/'synthetic-local-helper.sh';helper.write_text('#!/bin/sh\nif [ "$1" = get ]; then printf "username=windows-qa\\npassword=synthetic-test-only\\n"; fi\n',encoding='utf-8',newline='\n');helper.chmod(0o755)
  git(n+'-local-helper',['config','credential.helper',helper.as_posix()],publisher)
  global_file=R/(n+'-global-rewrite.config');global_file.write_text('[url "'+attacker.as_posix()+'"]\n\tinsteadOf = '+real.as_posix()+'\n',encoding='utf-8',newline='\n')
  overrides={
   'count-url':dict(GIT_CONFIG_COUNT='2',GIT_CONFIG_KEY_0='remote.origin.url',GIT_CONFIG_VALUE_0=attacker.as_posix(),GIT_CONFIG_KEY_1='remote.origin.pushurl',GIT_CONFIG_VALUE_1=attacker.as_posix()),
   'parameters-url':dict(GIT_CONFIG_PARAMETERS="'remote.origin.url="+attacker.as_posix()+"' 'remote.origin.pushurl="+attacker.as_posix()+"'"),
   'global-rewrite':dict(GIT_CONFIG_GLOBAL=str(global_file)),
   'count-rewrite':dict(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='url.'+attacker.as_posix()+'.insteadOf',GIT_CONFIG_VALUE_0=real.as_posix())}
  override=overrides[mode];save(n+'-spoof-input',override)
  if effective:
   raw_origin=git(n+'-effective-raw-fetch-url',['remote','get-url','origin'],publisher,env=override).decode().strip()
   raw_push=git(n+'-effective-raw-push-url',['remote','get-url','--push','origin'],publisher,env=override).decode().strip()
   assert Path(raw_origin).resolve()==attacker.resolve() and Path(raw_push).resolve()==attacker.resolve(),n+' raw Git rewrite precondition failed; candidate not run'
  before=snap(n+'-before-setup',roots);assert 'beads-backup' not in refs(n+'-before-setup-attacker',attacker)
  plan=R/(n+'-setup.plan.json')
  run(n+'-setup-prepare',['node',publisher/'scripts/bd-publisher-setup.mjs','--primary-root',primary,'--publisher-root',publisher,'--qualified-cli',BD,'--output',plan],publisher,env=override)
  prepared=json.loads(plan.read_bytes());assert Path(prepared['origin']['fetch']).resolve()==real.resolve();assert all(Path(p).resolve()==real.resolve() for p in prepared['origin']['push'])
  run(n+'-setup-install',['node',publisher/'scripts/bd-publisher-setup.mjs','--install',plan],publisher,env=override)
  after_setup=snap(n+'-after-setup',roots)
  assert before['real']==after_setup['real'] and before['attacker']==after_setup['attacker']
  state=json.loads(bash(n+'-read-state',publisher/'scripts/bd-apply-intents.sh',['--read-state'],publisher,env=override).stdout);assert state['R']==ZERO
  actor='agent-'+str(uuid.uuid4());pres=publisher/'.git/overgate-bd-managed/preservation';pres.mkdir(parents=True)
  manifest=dict(version=1,base=ZERO,actor=actor,outcome='verified-absent',artifacts={});(pres/'preservation.json').write_text(json.dumps(manifest)+'\n',encoding='utf-8');save(n+'-bootstrap-input',manifest)
  boot=json.loads(bash(n+'-bootstrap',publisher/'scripts/bd-apply-intents.sh',['--bootstrap',pres/'preservation.json'],publisher,env=override).stdout);assert boot['status']=='bootstrapped'
  queues=R/'queues';queues.mkdir(exist_ok=True);raw=queues/(n+'.raw.jsonl');queue=queues/(n+'.v2.jsonl')
  intents=[dict(intent_id=n+'-create',op='create',handle='tmp:task',title='Windows wrong-remote '+variant+' — synthetic task',type='task',priority=2,description='Native pinned Windows source; publish only to real origin.\nКириллица',labels=['windows-qa','synthetic'],metadata={'case':variant,'typed':[1,True,None]}),dict(intent_id=n+'-claim',op='claim',ref='tmp:task')]
  raw.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in intents),encoding='utf-8')
  bash(n+'-prepare-queue',publisher/'scripts/bd-apply-intents.sh',['--prepare','--base',ZERO,'--actor',actor,'--output',queue,raw],publisher,env=override)
  before_pub=snap(n+'-before-publication',roots)
  receipt=json.loads(bash(n+'-native-publish',publisher/'scripts/bd-apply-intents.sh',[queue],publisher,env=override,timeout=240).stdout);save(n+'-publication-receipt',receipt)
  actual=next(x['result']['ref'] for x in receipt['outcomes'] if x['intent_id']==n+'-create');published=receipt['published_sha']
  assert actual.startswith('wqa-') and any(x['id']==actual and x['actor']==actor and x['confirmed'] for x in receipt['claims'])
  real_R=git(n+'-real-R',['rev-parse','refs/heads/beads-backup'],real).decode().strip();assert real_R==published
  assert 'beads-backup' not in refs(n+'-attacker-after-publish',attacker)
  peer_data=json.loads(bash(n+'-peer-read',peer/'scripts/bd-read.sh',['show',actual,'--json'],peer,env=override).stdout)
  if isinstance(peer_data,list):assert len(peer_data)==1;peer_data=peer_data[0]
  peer_R=git(n+'-peer-R',['rev-parse','refs/remotes/origin/beads-backup'],peer).decode().strip();assert peer_R==published
  snapshot=git(n+'-snapshot',['show',published+':.beads/issues.jsonl'],publisher)
  obj=next(json.loads(line) for line in snapshot.splitlines() if json.loads(line).get('id')==actual)
  assert json.dumps(peer_data,ensure_ascii=False,sort_keys=True)==json.dumps(obj,ensure_ascii=False,sort_keys=True)
  assert obj['metadata']==intents[0]['metadata'] and obj['description']==intents[0]['description']
  after=snap(n+'-after-publication-and-peer',roots);assert before_pub['attacker']==after['attacker']
  save(n+'-result',dict(source=PIN,target_fixture_head=fixture_head,actor=actor,actual_id=actual,claims_confirmed=True,published_sha=published,real_R=real_R,peer_R=peer_R,attacker_R=None,peer_full_object_equal=True,attacker_full_bytes_unchanged=True,normal_registered_shell_route=True,override=override,auth_route='actual local bare transport with repo-local identity/helper; authenticated HTTPS push NOT RUN'))
  row(n,'AC6/AC9 B3','PASS','Native qualified setup/bootstrap + normal shell create/claim/publish + full-object peer under isolated inherited spoof; real/peer same R, attacker absent/byte unchanged',n+'-result.json')
 print('NATIVE PUBLICATION COMPLETE',flush=True)
guard(main)
