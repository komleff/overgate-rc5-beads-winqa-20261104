from qa_common import *
import uuid
zero='0'*40
save('qa-preflight-correction',dict(classification='QA assertion correction; candidate not executed',reason='tracked reference metadata.json is a descriptor, not a legacy store; original false preflight receipt preserved',source=PIN))
check('publisher-store-absent-pre',not any((PUBLISHER/'.beads'/x).exists() for x in ['dolt','redirect','embeddeddolt','dolt-server.pid','dolt-server.port']), 'publisher actual legacy store and endpoint files absent; tracked reference metadata retained unchanged')
run('primary-synthetic-native-init',[BD,'--sandbox','init','--prefix','wqa','--skip-agents','--skip-hooks','--non-interactive','--remote',''],PRIMARY,timeout=180)
prefix=json.loads(run('primary-prefix',[BD,'--readonly','config','list','--json'],PRIMARY).stdout)['issue_prefix']
check('primary-prefix-check',prefix=='wqa',prefix)
check('primary-still-exact-pin',text(git('primary-post-init-head',['rev-parse','HEAD'],PRIMARY))==PIN,'bd init must not move source HEAD')
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
save('setup-result',dict(result='PASS',source=PIN,primary=str(PRIMARY),publisher=str(PUBLISHER),prefix=prefix,actor=actor,bootstrap=boot))
print('SETUP BOOTSTRAP PASS; no task publications')
