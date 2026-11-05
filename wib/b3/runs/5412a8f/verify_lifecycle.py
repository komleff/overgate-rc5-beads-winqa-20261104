from common import *
def verify_peer(n,roots,result,tmpdir=None):
 ident=result['id'];published=result['published_sha']
 real=git(n+'-real-R',['rev-parse','refs/heads/beads-backup'],roots['real']).decode().strip();assert real==published
 assert 'beads-backup' not in ref(n+'-attacker-refs',roots['attacker'])
 env={}
 if tmpdir:
  tmpdir.mkdir(parents=True,exist_ok=True);env['TMPDIR']=tmpdir.as_posix()
 before_db=files(roots['peer']/'.beads')
 peer=json.loads(bash(n+'-public-peer-read','scripts/bd-read.sh',['show',ident,'--json'],roots['peer'],env=env).stdout)
 snapshot=git(n+'-published-snapshot',['show',published+':.beads/issues.jsonl'],roots['real'])
 records=[json.loads(line) for line in snapshot.splitlines() if line.strip()];obj=next(x for x in records if x.get('id')==ident)
 assert json.dumps(peer,sort_keys=True,ensure_ascii=False)==json.dumps(obj,sort_keys=True,ensure_ascii=False)
 peer_R=git(n+'-peer-R',['rev-parse','refs/remotes/origin/beads-backup'],roots['peer']).decode().strip();assert peer_R==published and files(roots['peer']/'.beads')==before_db
 save(n+'-peer-proof',dict(id=ident,real_R=real,peer_R=peer_R,attacker_R=None,full_object_equal=True,peer_native_DB_bytes_unchanged=True,temporary_snapshot_dir=str(tmpdir) if tmpdir else None,object=obj,issue_records=sum(x.get('_type','issue')=='issue' for x in records)))
 return obj
def main():
 root=C/"Проект's (QA) space";roots={r:root/r for r in ['primary','publisher','peer']};roots.update(real=root/'real.git',attacker=root/'attacker.git')
 result=json.loads((E/'complex-installed-activation-result.json').read_bytes());work=R/'activation-work/complex';journal=json.loads((work/'activation-checkpoint.json').read_bytes());actor=journal['bound']['actor']
 obj=verify_peer('complex-initial',roots,result,R/'reader-temp'/"Кэш's (QA) space");assert obj['status']=='in_progress' and obj['assignee']==actor
 row('complex-public-reader-check-snapshot','B3 I4/I5','PASS','Public installed bd-read in combined root with combined TMPDIR exercises Node reader check/snapshot operand; full peer object and exact R, peer DB unchanged','complex-initial-peer-proof.json')
 raw=work/'qa-lifecycle.raw.jsonl';queue=work/'qa-lifecycle.v2.jsonl';description='Verified native Windows update\nПроверено'
 intents=[dict(intent_id='qa-win-update',op='update',ref=result['id'],description=description),dict(intent_id='qa-win-close',op='close',ref=result['id'],close_reason='Windows QA verified complete')]
 raw.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in intents),encoding='utf-8')
 bash('complex-lifecycle-prepare','scripts/bd-apply-intents.sh',['--prepare','--base',result['published_sha'],'--actor',actor,'--output',queue,raw],roots['publisher'])
 receipt=json.loads(bash('complex-lifecycle-publish','scripts/bd-apply-intents.sh',[queue],roots['publisher'],timeout=240).stdout);save('complex-lifecycle-receipt',receipt)
 closed=verify_peer('complex-closed',roots,dict(id=result['id'],published_sha=receipt['published_sha']),R/'reader-temp'/"Кэш's (QA) space")
 assert closed['status']=='closed' and closed['description']==description
 save('complex-lifecycle-result',dict(source=PIN,id=result['id'],actor=actor,initial_R=result['published_sha'],closed_R=receipt['published_sha'],peer_R=receipt['published_sha'],attacker_R=None,confirmed_initial_claim=result['claim_confirmed'],status=closed['status'],full_object_equal=True,root=str(root)))
 row('complex-native-create-claim-update-close','B3 I2/I4/I5/I6','PASS','Actual installed activation + typed native update/close; real ID/confirmed claim, full object and exact real/peer R; attacker absent','complex-lifecycle-result.json')
 print('COMPLEX READER/LIFECYCLE PASS',flush=True)
if __name__=='__main__':guard(main)
