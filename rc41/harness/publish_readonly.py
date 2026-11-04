import json,hashlib,shutil
from pathlib import Path
from publish_failure import B,E,R,cmd
assert cmd(['git','branch','--show-current'])=='qa/rc41-evidence'
assert not cmd(['git','status','--porcelain'])
dest=R/'rc41'
for p in E.glob('readonly-*'):shutil.copyfile(p,dest/'receipts'/p.name)
shutil.copyfile(E/'capture-correction.md',dest/'receipts/capture-correction.md')
for name in ['hotfix_qa.py','read_only_diagnostic.py','publish_readonly.py']:shutil.copyfile(B/name,dest/'harness'/name)
index={str(p.relative_to(dest)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.rglob('*') if p.is_file() and p!=dest/'SHA256SUMS.json'}
(dest/'SHA256SUMS.json').write_text(json.dumps(index,indent=2),encoding='utf-8',newline='\n')
cmd(['git','add','rc41']);cmd(['git','diff','--cached','--check','--','rc41/harness'])
cmd(['git','commit','-m','docs: record authorized read-only Windows rev-path diagnostic'])
cmd(['git','push','origin','qa/rc41-evidence'])
sha=cmd(['git','rev-parse','HEAD']);(E/'readonly-evidence-sha.txt').write_text(sha,encoding='utf-8')
print(json.dumps({'evidence_commit':sha,'files':len(index)}))
