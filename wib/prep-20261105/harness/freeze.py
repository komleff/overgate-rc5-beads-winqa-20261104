from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parent;E=B/'evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
root=B/'frozen-legacy-stores';root.mkdir()
frozen={}
for name in ['legacy-pending','legacy-old-writer-peer']:
 source=B/name/'.beads';dest=root/name
 shutil.copytree(source,dest)
 before={str(p.relative_to(source)):sha(p) for p in source.rglob('*') if p.is_file()}
 after={str(p.relative_to(dest)):sha(p) for p in dest.rglob('*') if p.is_file()}
 assert before==after
 controls={}
 for label,path in [('git-config',B/name/'.git/config'),('git-index',B/name/'.git/index'),('install-state',B/name/'.overgate/install-state.json')]:
  controls[label]=dict(path=str(path),sha256=sha(path))
  shutil.copyfile(path,root/(name+'-'+label+'.bin'))
 hook=B/name/'.git/hooks/pre-push'
 controls['pre-push']=dict(path=str(hook),present=hook.exists(),sha256=sha(hook) if hook.is_file() else None)
 if hook.is_file():shutil.copyfile(hook,root/(name+'-pre-push.bin'))
 frozen[name]=dict(source=str(source),frozen_copy=str(dest),files=before,controls=controls,full_byte_copy_verified=True)
(E/'frozen-legacy-store-inventory.json').write_text(json.dumps(frozen,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(frozen='READY',stores=len(frozen),byte_copy_equal=True,candidate='NOT RUN')))
