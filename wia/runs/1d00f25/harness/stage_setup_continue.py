from qa_common import *
zero='0'*40
target=text(git('fixture-init-head',['rev-parse','HEAD'],PRIMARY))
changes=text(git('fixture-init-paths',['diff','--name-only',PIN,target],PRIMARY)).splitlines()
check('fixture-init-only-project-state',all(p.startswith('.beads/') or p=='.gitignore' for p in changes),changes)
save('fixture-target-binding-note',dict(source=PIN,target=target,reason='native bd init created its own Git commit; RUN packet requires exact candidate helper bytes and fixture HEAD==origin/main, not synthetic commit==source SHA',initialization_receipt='primary-synthetic-native-init.json',source_scripts_changed=False,task_mutations=0))
git('fixture-publish-native-init',['push','origin','HEAD:refs/heads/main'],PRIMARY)
git('fixture-primary-fetch',['fetch','origin','main'],PRIMARY)
git('fixture-publisher-fetch',['fetch','origin','main'])
git('fixture-publisher-fast-forward',['-c','core.autocrlf=false','merge','--ff-only','origin/main'])
for name,root in [('primary',PRIMARY),('publisher',PUBLISHER)]:
 check(name+'-target-main-current',text(git(name+'-target-head',['rev-parse','HEAD'],root))==text(git(name+'-target-origin-main',['rev-parse','origin/main'],root))==target,'fixture trusted main '+target)
inventory=json.loads((E/'source-fingerprint.json').read_text())['files']
check('fixture-target-candidate-byte-equivalence',all(sha((PUBLISHER/p).read_bytes())==h for p,h in inventory.items()),'all bound candidate helper/docs bytes unchanged after native init')
plan=R/'setup-plan.json'
run('setup-prepare',['node','scripts/bd-publisher-setup.mjs','--primary-root',PRIMARY,'--publisher-root',PUBLISHER,'--qualified-cli',BD,'--output',plan])
run('setup-install',['node','scripts/bd-publisher-setup.mjs','--install',plan])
state=json.loads(bash('publisher-read-zero',['scripts/bd-apply-intents.sh','--read-state']).stdout)
check('publisher-zero-check',state['R']==zero and state['records']==0 and not state['managed'],state)
actor=json.loads((B/'evidence/workspace-ready.json').read_text())['actors'][0]['actor_id']
pres=PUBLISHER/'.git/overgate-bd-managed/preservation'
pres.mkdir(parents=True)
manifest=dict(version=1,base=zero,actor=actor,outcome='verified-absent',artifacts={})
(pres/'preservation.json').write_text(json.dumps(manifest)+'\n',encoding='utf-8')
save('bootstrap-manifest',manifest)
boot=json.loads(bash('publisher-bootstrap',['scripts/bd-apply-intents.sh','--bootstrap',pres/'preservation.json']).stdout)
check('bootstrap-outcome',boot['status']=='bootstrapped' and boot['outcome']=='verified-absent',boot)
save('setup-result',dict(result='PASS',source=PIN,target=target,primary=str(PRIMARY),publisher=str(PUBLISHER),prefix='wqa',actor=actor,bootstrap=boot))
print('SETUP BOOTSTRAP PASS; no task publications')
