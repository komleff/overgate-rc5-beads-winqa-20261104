from common import *
def main():
 assert git('source-head',['rev-parse','HEAD'],S).decode().strip()==PIN
 assert git('source-tree',['rev-parse','HEAD^{tree}'],S).decode().strip()=='d4741fe7744ea1da0bd86fba2b1b6bbbe0dff2d4'
 contract=(R/'pr-contract.txt').read_bytes().strip()+b'\n';(R/'pr-contract.txt').write_bytes(contract);assert len(contract)==1024
 paths=git('source-paths',['diff','--name-only',BASE,PIN],S).decode().splitlines();blobs={p:git('source-blob-'+str(i),['rev-parse',PIN+':'+p],S).decode().strip() for i,p in enumerate(sorted(paths))}
 fp=sha(''.join(p+' '+blobs[p]+'\n' for p in sorted(blobs)).encode()+contract)
 assert len(paths)==29 and fp=='e0987f00495fbda3047784afc29c67ec66dae10d568cef2458408754a04d05d2'
 save('source-binding',dict(source=PIN,tree='d4741fe7744ea1da0bd86fba2b1b6bbbe0dff2d4',base=BASE,paths=blobs,contract_bytes=len(contract),contract_sha256=sha(contract),content_fingerprint=fp))
 frozen=json.loads((PREP/'evidence/prep-ready.json').read_bytes());mismatches=[]
 for name,case in frozen['cases'].items():
  for role in ['real','attacker']:
   data=case[role];root=Path(data['path'])
   if files(root)!=data['files']:mismatches.append(name+'/'+role)
   assert ref('pre-'+name+'-'+role,root)==data['refs'] and 'beads-backup' not in data['refs']
  for role,data in case['clones'].items():
   root=Path(data['root'])
   if files(root)!=data['files']:mismatches.append(name+'/'+role)
   assert git('pre-'+name+'-'+role+'-origin',['remote','get-url','origin'],root).decode().strip()==data['origin']
   assert all(not (root/p).exists() for p in data['runtime_paths_absent'])
 assert not mismatches,mismatches
 assert sha(BD.read_bytes())=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de'
 run('bd-version-only',[BD,'--version'])
 save('preflight-result',dict(source=PIN,fingerprint=fp,frozen_slots_verified=7,standalone_clones_verified=21,drift=False,task_refs_local_DB_queue_control='absent',native_bd_sha256=sha(BD.read_bytes())))
 print('PREFLIGHT PASS',flush=True)
guard(main)
