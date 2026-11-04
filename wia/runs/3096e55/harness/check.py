from qa_common import *
import shutil
SRC=B/'source-3096e55'
assert not SRC.exists()
git('source-init',['init','--initial-branch=qa/source',SRC],B)
git('source-fetch',['-C',SRC,'fetch','--no-tags','https://github.com/komleff/overgate.git',PIN],B)
git('source-checkout',['-C',SRC,'-c','core.autocrlf=false','checkout','--detach',PIN],B)
check('native-binary-hash',sha(BD.read_bytes())=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de',str(BD))
run('native-bd-version',[BD,'--version'],B)
run('native-node-version',['node','--version'],B)
tampered=B/'bd-tampered.exe';shutil.copyfile(BD,tampered)
with tampered.open('ab') as f:f.write(b'\nOverGate synthetic fingerprint negative\n')
save('tampered-binary-hash',dict(path=str(tampered),sha256=sha(tampered.read_bytes()),executed=False))
before={str(p.relative_to(SRC/'.beads')):sha(p.read_bytes()) for p in (SRC/'.beads').rglob('*') if p.is_file()}
run('native-qualify-matrix',['node',B/'qualify.mjs',BD,tampered,E/'qualification-result.json'],B)
after={str(p.relative_to(SRC/'.beads')):sha(p.read_bytes()) for p in (SRC/'.beads').rglob('*') if p.is_file()}
check('no-store-or-task-write',before==after and not (SRC/'.beads/dolt').exists() and not (B/'.beads').exists(),dict(before=before,after=after))
changed=text(git('source-diff-since-accepted',['-C',SRC,'diff','--name-only','0a8685ed072fece134418a1d18ed11d8a53759a3',PIN],B)).splitlines()
check('only-qualifier-runtime-changed',{p for p in changed if not p.startswith(('.github/','scripts/tests/'))}=={'scripts/lib/bd-managed-cli.mjs'},changed)
git('qualifier-affected-diff',['-C',SRC,'diff','0a8685ed072fece134418a1d18ed11d8a53759a3',PIN,'--','scripts/lib/bd-managed-cli.mjs'],B)
paths=['scripts/lib/bd-publisher-push-guard.mjs','scripts/lib/bd-managed-read-check.mjs','scripts/lib/bd-managed-contract.mjs','scripts/lib/bd-managed-git.mjs','scripts/lib/bd-managed-journal.mjs','scripts/lib/bd-managed-transaction.mjs','scripts/bd-read.sh','scripts/bd-wt.sh','scripts/bd-apply-intents.sh','scripts/bd-publisher-setup.mjs']
equivalence={}
for i,p in enumerate(paths):
 old=text(git('old-runtime-blob-'+str(i),['-C',SRC,'rev-parse','0a8685ed072fece134418a1d18ed11d8a53759a3:'+p],B))
 new=text(git('new-runtime-blob-'+str(i),['-C',SRC,'rev-parse',PIN+':'+p],B))
 equivalence[p]=dict(old_blob=old,new_blob=new,equal=old==new)
check('accepted-runtime-equivalent',all(x['equal'] for x in equivalence.values()),equivalence)
save('runtime-equivalence',dict(source=PIN,accepted_source='0a8685ed072fece134418a1d18ed11d8a53759a3',paths=equivalence,
 frozen_checkpoint='0ccd30cf63896db09f41d9e2a8e19c71c0b120bd',frozen_supplement='08168676eb58fbe44cae1ca56ce3bf752abc30ea',full_lifecycle_repeated=False))
print('Affected native Windows qualification/tamper/platform matrix + runtime equivalence PASS; no DB/task writes')
