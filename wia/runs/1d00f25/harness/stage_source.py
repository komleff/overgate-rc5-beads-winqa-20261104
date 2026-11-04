from qa_common import *
check('cli-hash',sha(BD.read_bytes())=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de',str(BD))
run('cli-version',[BD,'--version'])
git('source-fetch-complete-history',['fetch','--unshallow','--no-tags','https://github.com/komleff/overgate.git',PIN])
save('fixture-prep-transport-note',dict(classification='QA fixture transport, not product FAIL',original_receipt='source-to-local-main.json',reason='shallow fetch cannot be transferred to non-shallow bare origin',resolution='fetch complete source ancestry before fixture main publication',setup_run=False,task_mutations=0))
git('source-to-local-main-complete-history',['push','origin',PIN+':refs/heads/main'])
git('publisher-main',['-c','core.autocrlf=false','checkout','-b','main',PIN])
git('publisher-fetch-main',['fetch','origin','main'])
git('primary-fetch-main',['fetch','origin','main'],PRIMARY)
git('primary-main',['-c','core.autocrlf=false','checkout','-b','main','origin/main'],PRIMARY)
for name,root in [('primary',PRIMARY),('publisher',PUBLISHER)]:
 head=text(git(name+'-head',['rev-parse','HEAD'],root))
 remote=text(git(name+'-origin-main',['rev-parse','origin/main'],root))
 actual=text(git(name+'-remote-main',['ls-remote','--heads','origin','main'],root)).split()[0]
 check(name+'-trusted-main',head==remote==actual==PIN,dict(head=head,origin_main=remote,remote_main=actual))
 check(name+'-clean',not git(name+'-status',['status','--porcelain'],root).stdout,'exact source clean before setup')
paths=text(git('source-tree',['ls-tree','-r','--name-only','HEAD'])).splitlines()
files=[p for p in paths if p.startswith('scripts/lib/bd-') or p in ['AGENTS.md','.agents/HOW_TO_USE.md','scripts/bd-publisher-setup.mjs','scripts/bd-apply-intents.sh','scripts/bd-read.sh','scripts/bd-wt.sh','scripts/bd-sync-export.sh','scripts/bd-sync-restore.sh','docs/plans/2026-11-03-v4.0.0-rc.5-beads.md']]
inventory={p:sha(git('blob-'+str(i),['show',PIN+':'+p]).stdout) for i,p in enumerate(files)}
check('source-worktree-bytes',all(sha((PUBLISHER/p).read_bytes())==h for p,h in inventory.items()),'canonical source bytes match working files (core.autocrlf=false)')
save('source-fingerprint',dict(source=PIN,files=inventory,sha256=sha(json.dumps(inventory,sort_keys=True,separators=(',',':')).encode())))
print('SOURCE READY: '+PIN)
