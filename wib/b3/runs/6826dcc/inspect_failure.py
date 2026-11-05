from common import *
root=C/"Проект's (QA) space";out={}
for role in ['primary','publisher','peer']:
 base=root/role/'.git/overgate-bd-managed'
 out[role]={'managed_files':list(files(base)),'DB_present':(root/role/'.beads').exists()}
 for name in ['active.json','bootstrap.json','registration.json']:
  p=base/name
  if p.is_file():out[role][name]=json.loads(p.read_bytes())
 for p in base.rglob('*.json') if base.is_dir() else []:
  if p.name in ['state.json','journal.json']:
   out[role][p.relative_to(base).as_posix()]=json.loads(p.read_bytes())
save('read-only-failure-inspection',out)
print(json.dumps(out,ensure_ascii=True,indent=2))
