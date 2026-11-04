from pathlib import Path
import json
text=(Path(__file__).parent/'prepare.py').read_text(encoding='utf-8')
# Restore only helper definitions, never repeat released install or native task creation.
exec(text.split('assert sha(BD.read_bytes())',1)[0])
legacy=B/'legacy-pending';legacy_origin=B/'legacy-origin.git'
a=json.loads((E/'legacy-create-owner.stdout.bin').read_bytes());b=json.loads((E/'legacy-create-peer.stdout.bin').read_bytes())
if isinstance(a,list):a=a[0]
if isinstance(b,list):b=b[0]
export=E/'legacy-before.jsonl'
slots={n:str(B/n) for n in ['no-beads','custom-conflict-rollback','unknown-remote','unavailable-publisher']}
unknown=B/'unknown-receipt';init('unknown-receipt',unknown);slots['unknown-receipt']=str(unknown)
baselines={}
for name in ['legacy-empty','legacy-pending','beads-false-upgrade']:
 state=json.loads((B/name/'.overgate/install-state.json').read_bytes())
 baselines[name]=dict(path=str(B/name),source=OLDPIN,beads=state['beads'],protocol_field_present='beads_protocol' in state)
version=(E/'native-bd-version.stdout.bin').read_bytes().decode().strip()
save('qa-prep-git-pathspec-note',dict(reason='QA git add exclude pathspec encountered ignored backup directory; use explicit released manifest target allowlist',candidate_executed=False,original_receipt='legacy-code-add.json',released_installs_and_native_creates_not_repeated=True))
manifest=json.loads((OLD/'.agents/distribution-manifest.json').read_bytes())
files=[e['target'] for e in manifest['files'] if (legacy/e['target']).is_file()]
files+=['README.md','.overgate/install-state.json']
git('legacy-code-add-explicit',['-c','core.autocrlf=false','add','--',*sorted(set(files))],legacy)
cached=git('legacy-code-index-safety',['ls-files','-z'],legacy).decode().split('\0')
assert not any(p.startswith(('.beads/dolt/','.beads/embeddeddolt/','.overgate-backups/','.bd-intents/')) for p in cached)
git('legacy-code-commit',['-c','commit.gpgsign=false','commit','-m','fixture: released rc4.1 legacy payload'],legacy)
tail="git('legacy-code-push'"+text.split("git('legacy-code-push'",1)[1]
tail=tail.replace(',actor_owner=actor','')
tail=tail.replace("receipts=legacy/'.git/bd-receipts'","receipts=unknown/'.git/bd-receipts'")
tail=tail.replace('receipt_sha256=sha(opaque.read_bytes()),','receipt_fixture=str(unknown),receipt_sha256=sha(opaque.read_bytes()),')
exec(tail)
