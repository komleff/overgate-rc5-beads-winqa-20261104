from common import *
def main():
 assert git('source-HEAD',['rev-parse','HEAD'],S).decode().strip()==PIN
 assert git('source-tree',['rev-parse','HEAD^{tree}'],S).decode().strip()=='74dfe1d3ae58b2d81a6e08c1ec7841e1ef51cb00'
 contract=(R/'pr-contract.txt').read_bytes().strip()+b'\n';(R/'pr-contract.txt').write_bytes(contract);assert len(contract)==1255
 paths=git('package-paths',['diff','--name-only',BASE,PIN],S).decode().splitlines()
 blobs={p:git('blob-'+str(i),['rev-parse',PIN+':'+p],S).decode().strip() for i,p in enumerate(sorted(paths))}
 fp=sha(''.join(p+' '+blobs[p]+'\n' for p in sorted(blobs)).encode()+contract)
 assert len(paths)==41 and fp=='414e563edc38f0286382bc1fc4e2c581cf4c7f2d4aa9695dbd802b2a0bf1190c'
 save('source-binding',dict(source=PIN,base=BASE,paths=blobs,contract_bytes=len(contract),contract_sha256=sha(contract),content_fingerprint=fp))
 frozen=json.loads((PREP/'evidence/prep-ready.json').read_bytes());assert frozen['runtime_source_sha'] is None
 mismatches=[]
 for name,data in frozen['origins'].items():
  root=Path(data['path']);now=files(root)
  if now!=data['files']:mismatches.append('origin '+name)
  actual=refs('pre-'+name+'-refs',root);assert actual==data['refs'] and 'beads-backup' not in actual
 for name,data in frozen['clones'].items():
  root=Path(data['path']);now=files(root)
  if now!=data['files']:mismatches.append('clone '+name)
  origin=git('pre-'+name+'-origin',['remote','get-url','origin'],root).decode().strip();assert Path(origin).resolve()==(PREP/'real-origin.git').resolve()
  assert not (root/'.beads').exists() and not (root/'.bd-intents').exists() and not (root/'.git/bd-receipts').exists()
 assert not mismatches,mismatches
 assert sha(BD.read_bytes())=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de'
 run('qualified-bd-version-only',[BD,'--version']);save('preflight-result',dict(source=PIN,fingerprint=fp,frozen_fixture_drift=False,real_R=None,attacker_R=None,local_DB_queues_receipts_absent=True,native_bd_sha256=sha(BD.read_bytes())))
 print('PREFLIGHT PASS',flush=True)
guard(main)
