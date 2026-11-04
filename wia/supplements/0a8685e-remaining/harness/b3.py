from qa_common import *
def store_hash():
 root=PRIMARY/'.beads'
 return {str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
current=text(git('b3-before-remote',['ls-remote','--heads','origin','beads-backup'])).split()[0]
git('b3-primary-cache-current',['fetch','origin','refs/heads/beads-backup:refs/remotes/origin/beads-backup'],PRIMARY)
check('b3-cache-managed-marker',bool(git('b3-cache-marker',['show',current+':.beads/overgate-managed-v1.json'],PRIMARY).stdout),current)
before=store_hash();save('b3-before-primary-store-hashes',before)
origin=B/'origin.git'
git('b3-backup-valid-task-ref',['--git-dir='+str(origin),'update-ref','refs/qa/saved-b3-valid',current],B)
git('b3-fault-remove-fixture-branch',['--git-dir='+str(origin),'update-ref','-d','refs/heads/beads-backup',current],B)
passed=False
try:
 git('b3-confirm-remote-absent',['ls-remote','--exit-code','--heads','origin','beads-backup'],expected=(2,))
 for kind in ['export','restore']:
  refusal=bash('b3-legacy-'+kind+'-refusal',['scripts/bd-sync-'+kind+'.sh'],PRIMARY,expected=(1,))
  check('b3-'+kind+'-managed-cause',any(x in decode(refusal.stderr).lower() for x in ['managed','last-seen','cached','кэш','marker']),decode(refusal.stderr))
  check('b3-'+kind+'-no-database-change',store_hash()==before,'entire primary .beads file byte hashes unchanged')
  check('b3-'+kind+'-no-branch-recreation',not text(git('b3-'+kind+'-remote-stays-absent',['ls-remote','--heads','origin','beads-backup'])),'remote task branch remains absent')
 passed=True
finally:
 found=text(git('b3-post-test-remote',['ls-remote','--heads','origin','beads-backup']))
 if not found:
  git('b3-restore-own-fixture-fault',['--git-dir='+str(origin),'update-ref','refs/heads/beads-backup',current,'0'*40],B)
 else:
  save('b3-unexpected-head-preserved',dict(found=found,original=current,note='Do not overwrite unexpected state; original retained under refs/qa/saved-b3-valid'))
if passed:
 check('b3-original-branch-restored',text(git('b3-restored-remote',['ls-remote','--heads','origin','beads-backup'])).split()[0]==current,current)
 save('b3-result',dict(result='PASS',source=PIN,original_published_sha=current,export_refused=True,restore_refused=True,primary_store_unchanged=True,branch_recreated_by_legacy=False,own_fault_restored=True))
 print('B3 cached managed marker + disappeared remote: export/restore both refuse before DB change/recreation PASS')
