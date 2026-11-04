from qa_common import *
import shutil
fp=json.loads((E/'source-fingerprint.json').read_text(encoding='utf-8'))
contract=(R/'pr-contract.txt').read_bytes()
inventory={p:text(git('fp-blob-'+str(i),['rev-parse',PIN+':'+p])) for i,p in enumerate(sorted(fp['files']))}
fingerprint=sha(''.join(p+' '+blob+'\n' for p,blob in inventory.items()).encode()+contract)
save('contract-fingerprint',dict(source=PIN,target=fp['target'],plan_blob='ceefa86186c62b4c754a59841710128a1ee9bbce',contract_sha256=sha(contract),contract_bytes=len(contract),
 content_fingerprint=fingerprint,algorithm='LC_ALL=C sorted changed paths as path SP Git blob LF, followed by normalized CONTRACT bytes',blobs=inventory,scripts_tree=fp['scripts_tree']))
check('expected-common-fingerprint',fingerprint=='95b731c6e64270128739781b042ca91b2dd08c58c661175dfa106b9e1f6f369f',fingerprint)
for name,root in [('primary',PRIMARY),('publisher',PUBLISHER),('linked',LINKED),('isolated',B/'isolated-reader')]:
 git('checkpoint-'+name+'-refs',['show-ref'],root)
 git('checkpoint-'+name+'-status',['status','--porcelain'],root)
 git('checkpoint-'+name+'-index',['ls-files','-s','-z'],root)
state=json.loads((E/'lifecycle-complete.json').read_text(encoding='utf-8'))
git('checkpoint-remote',['ls-remote','origin'])
git('checkpoint-published-ledger',['show',state['published_sha']+':.beads/overgate-outcomes-v1.json'])
shutil.copytree(PUBLISHER/'.git/overgate-bd-managed',R/'preserved-managed-control')
report='''# Windows QA — WI-A native checkpoint, source 0a8685e

Role/model: Windows QA / Codex GPT-6. Source: `{source}`.
Trusted fixture main: `{target}`. Source code untouched; exact 35 PR paths match candidate.
Contract/content fingerprint: `{fingerprint}` (35 path/blob records + 1255 CONTRACT bytes).
Native bd 1.2.2 SHA256: b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de.
Binary: D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe.

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
| Trusted source/binary/setup/bootstrap | AC6/9 precondition | Exact candidate bytes, local bare/two standalone clones; verified-absent local publisher store | PASS scoped | evidence/setup-result.json; source-fingerprint.json |
| Forged stale expected.title | AC4/6 | Actual installed native pre-push refused; isolated peer bd-read.sh refused custom forged ref; original remote/queue unchanged | PASS | evidence/ac4-result.json; ac4-real-pre-push-refusal.json; ac4-peer-reader-stale-refusal.json |
| Native create + claim + comment + typed graph | AC1/5/9 subset | Parent + nested child, actual IDs, claims.confirmed, same-SHA peer full object | PASS scoped | evidence/initial-receipt.json; initial-peer-full-object.json; initial-typed-edges.json |
| Native update/close/reopen/reassign | AC1/5/9 subset | Separate typed native publications and full-object peer comparison after each, untouched fields retained | PASS scoped | evidence/lifecycle-complete.json; lifecycle-*-receipt/peer-full-object/untouched-full-object.json |
| Legitimate unrelated-field stale-base rebase | AC3/4 | Notes queue frozen before independent title/metadata update; rebased publication retains current title | PASS | evidence/unrelated-notes-receipt.json; unrelated-notes-untouched-full-object.json |
| Remaining B1/B2/B3 negatives; linked/isolated queue handoff; wider race/retry | AC3–6/9 | Pending after this safe checkpoint | NOT RUN | Separate WI-C packet now queued by PM; not a whole WI-A acceptance claim |

Parent `{parent}`, nested issue `{id}`. Initial actor `{actor}`; reassigned actor `{reassigned}`.
Initial confirmed-claim publication `f34d37c107851309ff414e1239b206bbac4f660e`.
Latest publication and peer SHA `{published}`. Each per-step receipt records its exact SHA.
Fields include Unicode/multiline description, acceptance, notes/design, priority/type, due date,
external ref, nested typed metadata, labels, a native comment, parent-child and discovered-from edges.
Untouched field comparisons preserve all previously present fields, with set semantics only
for labels/comments/dependency order; metadata array order stays significant.

This new isolated bare origin was seeded with the prior immutable legitimate task history
`b4e8a10366dc205dbae2aef32a0a8487a35588f3` to run the AC4 negative before new task publication.
That was a Git object copy, not a rerun of old native publication. New source validates that
history, and all new lifecycle publications run through the registered new-source publisher.
The forged object never replaced the bare origin task branch: the peer fetched it as a
custom data ref; both actual pre-push and peer rejected stale preconditions.

No product failure observed in these scoped cases. Remaining VC cases are NOT RUN here.
No working U2/Toon/OverGate DB, merge, release, finalization or real migration.
One sequential worker; WI-C uses another root and evidence path. Raw binary stdout/stderr,
queues, exact JSON payloads, Git refs/index and publisher control journal are retained.
'''.format(source=PIN,target=fp['target'],fingerprint=fingerprint,parent=state['parent'],id=state['id'],actor=state['original_actor'],reassigned=state['reassigned_actor'],published=state['published_sha'])
(R/'REPORT.md').write_text(report,encoding='utf-8')
print(json.dumps(dict(checkpoint='saved',source=PIN,content_fingerprint=fingerprint,published_sha=state['published_sha'])))
