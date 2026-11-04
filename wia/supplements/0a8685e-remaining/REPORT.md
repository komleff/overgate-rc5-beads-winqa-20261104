# Windows QA — WI-A native checkpoint, source 0a8685e

Role/model: Windows QA / Codex GPT-6. Source: `0a8685ed072fece134418a1d18ed11d8a53759a3`.
Trusted fixture main: `ae1fbcc4aa463b312c0dce30771b239902edf1e9`. Source code untouched; exact 35 PR paths match candidate.
Contract/content fingerprint: `95b731c6e64270128739781b042ca91b2dd08c58c661175dfa106b9e1f6f369f` (35 path/blob records + 1255 CONTRACT bytes).
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

Parent `wqa-jax`, nested issue `wqa-jax.1`. Initial actor `agent-76e0e949-325c-4c9e-b6b8-2564b582df0c`; reassigned actor `agent-37e43435-33ac-49e4-8fb5-49a2336c34a3`.
Initial confirmed-claim publication `f34d37c107851309ff414e1239b206bbac4f660e`.
Latest publication and peer SHA `0b25f2996748cc7322f90de445ce7a8268245d8d`. Each per-step receipt records its exact SHA.
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
