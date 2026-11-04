# WI-B Windows QA preparation — candidate NOT RUN

Role/model: Windows QA / Codex GPT-6. Authority: PR17 plan-only source
`29edf688d7b7fbdad3122785efcabb1d8406845a`, plan blob
`5dedca627bf31916b871d85e88c4906551aaf576`, B1–B6 / I1–I7.
Runtime source pin: **not issued**. Every candidate case below is **NOT RUN**.

| Case | AC / risk | Prepared fixture / method after exact RUN | Current result |
|---|---|---|---|
| Fresh managed install PR | B1 / I2,I3 | fresh-install-pr branch, byte-exact complete managed closure + managed-v1 state; before/after no DB/Beads init/remote publication | NOT RUN |
| Managed closure omission | B1 / I3 | disposable manifest/import/helper omission negative; installed checker rejects before target write | NOT RUN |
| Fresh --no-beads | B1 / I3 | no-beads neutral root; protocol none, no Beads closure/rule/DB or remote write | NOT RUN |
| rc4 beads:false → none | B1 / I3 | actual released3f3246c --no-beads installed baseline, format2/beads:false/no protocol; candidate retains none/no closure | NOT RUN |
| Local/remote/pending inventory and drift | B2 / I1 | populated legacy, raw pending, separate unknown receipt, nonexistent local origin; frozen R/hashes vs plan/apply; unknown/fetch failure never absent | NOT RUN |
| Path/permission/unknown-context negatives | B2 / I1,I5 | own test roots only; symlink/permission capability first measured, unavailable capability reported honestly | NOT RUN |
| Pre-merge activation denial | B3 / I2 | fresh-install-pr remains named working branch; activation must stop before DB/task write | NOT RUN |
| Trusted-main post-merge activation | B3 / I2,I4,I6 | local origin + primary/publisher/peer standalone clones reserved; only synthetic temporary main promoted after exact source and byte binding | NOT RUN |
| Actual explicit task lifecycle | B3 / I4,I6 | explicit title/actor/prefix from activation-task-input, no implicit sample; real ID/claim/published SHA and peer full objects; update/close | NOT RUN |
| Legacy empty upgrade | B4 / I1 | actual released rc4.1 Beads-enabled empty baseline; default legacy-v0 remains, no implicit activation | NOT RUN |
| Populated legacy/pending preservation | B4 / I1 | two real native1.2.2 stores with same full objects, frozen legacy R, valid raw pending + external owner/hash, no auto prepare/replay | NOT RUN |
| Reviewed retained-pending switch | B4 / I1,I7 | exact immutable inventory + rehearsal + separately accepted synthetic target switch; keep pending bytes/owner, reviewed adoption only | NOT RUN |
| Known old-writer fences | B4 / I7 | legacy-pending + legacy-old-writer-peer share local legacy origin; old-writer candidate before/after first managed publication must refuse; unfenced/unknown writer stops | NOT RUN |
| Rollback boundary | B4 / I1,I7 | before first managed publication byte rollback leaves DB/queue/R; after publication no legacy writer restart, preserve ledger/snapshot | NOT RUN |
| Project-owned conflict/preservation | B5 / I5 | custom AGENTS, project verifier, Memory Bank and local settings marker have frozen hashes; conflict before overwrite; root main/readiness protection retained | NOT RUN |
| Linked/isolated/unavailable publisher | B5 / I4 | linked common-dir prepared, peer/unknown-publisher roots separate; actual result or retained queue/base/actor + precise blocker, no operator routine applier | NOT RUN |
| Native CLI/prefix/platform gate | B3,B6 / I6 | same scoped bd.exe1.2.2 known hash; real wib-qa prefix vs wib_qa DB name, bad hash/prefix/platform denied before task write | NOT RUN |
| Final installed verifier/native/CI | B6 / I1–I7 | exact source+contract fingerprint; installed checker/native Windows separate from Linux/Mac CI; trusted finalize belongs PM | NOT RUN |

Neutral activation topology: local bare origin has only qa/preparation, no main or
beads-backup; fresh-install-pr, publisher-after-merge and peer are independent clones;
linked is a linked worktree. No candidate code is installed or registered there.
Fresh fixture has no .beads. Candidate temporary trusted main does not exist yet.

Historical baselines use **only released rc.4.1** source
`3f3246c3a3b62377fc02aad05283cae1ef5d4e2d`, its actual installer and synthetic test-only
approval. They are not a run of plan-only PR17. Legacy task records are explicitly
synthetic fixtures created with the already qualified native1.2.2 CLI. A v0 snapshot
from the real native export was committed as a test legacy snapshot in local bare
origin. The peer has a separately initialized embedded store imported from it.

Raw pending is unprepared data, not an applied/accepted v2 queue. Its owner and hash
are external; it is never submitted or replayed during preparation. Unknown receipt
is isolated in its own negative fixture, not mixed into retained-pending positive data.
No candidate protocol switch, migration, writer fence, publication or rollback ran.
No working U2/Toon/OverGate DB/settings/hooks were used.
