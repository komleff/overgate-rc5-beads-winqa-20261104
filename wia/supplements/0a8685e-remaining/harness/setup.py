from qa_common import *
import uuid
ORIGIN=B/'origin.git'
ISOLATED=B/'isolated-reader'
OLDORIGIN=Path('D:/CodexArtifacts/overgate-rc5-wia-winqa-20261105/origin.git')
SEED='b4e8a10366dc205dbae2aef32a0a8487a35588f3'
check('cli-hash',sha(BD.read_bytes())=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de',str(BD))
run('cli-version',[BD,'--version'],B)
for p in [ORIGIN,PRIMARY,PUBLISHER,LINKED,ISOLATED]:assert not p.exists(),p
git('origin-init',['init','--bare','--initial-branch=main',ORIGIN],B)
git('primary-init',['init','--initial-branch=main',PRIMARY],B)
git('primary-add-origin',['remote','add','origin',ORIGIN],PRIMARY)
git('source-fetch-full',['fetch','--no-tags','https://github.com/komleff/overgate.git',PIN],PRIMARY)
git('source-main',['-c','core.autocrlf=false','checkout','-b','main',PIN],PRIMARY)
git('primary-name',['config','user.name','Windows QA actor A'],PRIMARY)
git('primary-email',['config','user.email','qa-a@example.invalid'],PRIMARY)
run('native-primary-init',[BD,'--sandbox','init','--prefix','wqa','--skip-agents','--skip-hooks','--non-interactive','--remote',''],PRIMARY,timeout=180)
target=text(git('fixture-main-head',['rev-parse','HEAD'],PRIMARY))
changed=text(git('fixture-project-state-diff',['diff','--name-only',PIN,target],PRIMARY)).splitlines()
check('fixture-state-only',all(x.startswith('.beads/') or x=='.gitignore' for x in changed),changed)
git('fixture-publish-main',['push','origin','HEAD:refs/heads/main'],PRIMARY)
git('fetch-immutable-task-seed',['fetch',OLDORIGIN,'refs/heads/beads-backup:refs/qa/seed'],PRIMARY)
check('seed-sha',text(git('seed-ref',['rev-parse','refs/qa/seed'],PRIMARY))==SEED,'immutable previous legitimate task history copied; no task publication rerun')
git('copy-task-seed-to-new-fixture',['push','origin',SEED+':refs/heads/beads-backup'],PRIMARY)
for name,root in [('publisher',PUBLISHER),('isolated',ISOLATED)]:
 git(name+'-clone',['clone','--no-hardlinks','-c','core.autocrlf=false',ORIGIN,root],B)
 git(name+'-name',['config','user.name','Windows QA '+name],root)
 git(name+'-email',['config','user.email','qa-'+name+'@example.invalid'],root)
git('linked-add',['worktree','add','-b','qa/linked',LINKED,'main'],PRIMARY)
git('primary-fetch-main',['fetch','origin','main'],PRIMARY)
for name,root in [('primary',PRIMARY),('publisher',PUBLISHER)]:
 check(name+'-trusted-main',text(git(name+'-head',['rev-parse','HEAD'],root))==text(git(name+'-origin-main',['rev-parse','origin/main'],root))==target,'HEAD == origin/main == '+target)
files=text(git('source-changed-paths',['diff','--name-only','3f3246c3a3b62377fc02aad05283cae1ef5d4e2d',PIN])).splitlines()
inventory={p:sha(git('source-blob-'+str(i),['show',PIN+':'+p]).stdout) for i,p in enumerate(files)}
check('source-bytes-match',all(sha((PUBLISHER/p).read_bytes())==h for p,h in inventory.items()),'exact candidate bytes for all PR changed paths')
save('source-fingerprint',dict(source=PIN,target=target,files=inventory,inventory_sha256=sha(json.dumps(inventory,sort_keys=True,separators=(',',':')).encode()),scripts_tree=text(git('source-scripts-tree',['rev-parse',PIN+':scripts']))))
plan=R/'setup-plan.json'
run('setup-prepare',['node','scripts/bd-publisher-setup.mjs','--primary-root',PRIMARY,'--publisher-root',PUBLISHER,'--qualified-cli',BD,'--output',plan])
run('setup-install',['node','scripts/bd-publisher-setup.mjs','--install',plan])
state=json.loads(bash('read-seeded-published-state',['scripts/bd-apply-intents.sh','--read-state']).stdout)
check('seed-preserved',state['R']==SEED and state['records']==1 and state['managed'],state)
actor='agent-'+str(uuid.uuid4())
pres=PUBLISHER/'.git/overgate-bd-managed/preservation'
pres.mkdir(parents=True)
manifest=dict(version=1,base=SEED,actor=actor,outcome='verified-absent',artifacts={})
(pres/'preservation.json').write_text(json.dumps(manifest)+'\n',encoding='utf-8')
save('bootstrap-manifest',manifest)
boot=json.loads(bash('bootstrap',['scripts/bd-apply-intents.sh','--bootstrap',pres/'preservation.json']).stdout)
check('bootstrap-pass',boot['status']=='bootstrapped' and boot['outcome']=='verified-absent',boot)
save('setup-result',dict(result='PASS',source=PIN,target=target,actor=actor,prefix='wqa',seed=SEED,bootstrap=boot))
print(json.dumps(dict(setup='PASS',source=PIN,target=target,seed=SEED,actor=actor)))
