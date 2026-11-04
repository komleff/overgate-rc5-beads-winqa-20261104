# Windows QA — remaining WI-A supplement on 0a8685e

Role/model: Windows QA / Codex GPT-6.
Source: `0a8685ed072fece134418a1d18ed11d8a53759a3`.
Fixture trusted main: `ae1fbcc4aa463b312c0dce30771b239902edf1e9`.
Content/contract fingerprint: `95b731c6e64270128739781b042ca91b2dd08c58c661175dfa106b9e1f6f369f`.
Native bd 1.2.2 SHA256 `b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de`.
This supplements the immutable native lifecycle checkpoint `0ccd30cf63896db09f41d9e2a8e19c71c0b120bd`;
that checkpoint and all earlier-source reports remain unchanged.

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
| B1 no-outcome issue loss/same-count rewrite | AC5/6 | Actual installed pre-push refuses both; isolated bd-read.sh on forged data refs refuses both; origin R unchanged | PASS | evidence/b1-result.json, b1-*-actual-prepush.json, b1-*-peer-reader.json |
| B2 malformed whitespace vs empty | AC5 | Exact source parser rejects three nonzero whitespace forms; zero-byte snapshot + exact comparison accepted | PASS (function integration) | evidence/b2-result.json, b1-b2-build-data.json |
| B3 missing remote with cached managed marker | AC6 | Remove only disposable origin task branch; actual legacy export/restore both refuse; complete primary .beads byte hashes unchanged, no branch recreation; own fault restored | PASS | evidence/b3-result.json; b3-before-primary-store-hashes.json; b3-*.json |
| Linked and isolated managed readers / direct write refusal | AC9 | Actual bd-wt show full object; direct create RC2 in both; primary .beads byte hashes unchanged | PASS scoped | evidence/linked-managed-read.json; isolated-managed-read.json; *-direct-managed-create-denied.json |
| Linked typed queue via registered publisher | AC9 | Queue data prepared from linked worktree, native trusted publisher applies, isolated same-SHA full-object read-back | PASS | evidence/routes-result.json; linked-publication-receipt.json |
| Actual lost transport receipt and identical queue replay | AC4 | Real receive-pack writes task ref then fixture wrapper exits73; Git trace proves failed child; readback confirms publication; same queue retry yields mutations0, unchanged R/ledger/outcomes/queue hash | PASS scoped | evidence/lost-receipt-result.json; lost-receipt-retry-receipt.json; lost-git-trace2.jsonl; lost-receive-pack.trace |
| Two-actor same-field and claim stale-base races | AC3 | Both queues prepared against same R; winner native publishes; loser native apply RC8 retains title/claim conflicts and both queues, winning R unchanged | PASS scoped, sequential interleaving | evidence/races-result.json; race-losing-native-apply-refusal.json |
| Opposing graph edge race | AC3 | Both queues frozen against same R; after first native edge publication, second edge native trusted --dry-run rejects blocking cycle before CLI/publication | PASS scoped for dry-run validation | evidence/race-graph-native-dry-run-refusal.json |
| Simultaneous OS/CAS race, actual graph publication attempt, isolated unavailable-publisher pending handoff, specific stale close, no-advance failed-push restart | AC3/4/9 | Not executed | NOT RUN | evidence/supplement-result.json |

Linked publication `2aecd0779cce2d176bd977afcb0035e738dcb1b7`; lost-receipt publication and identical retry `5a81caeb58e15981b5e75d2f4fdc62c067eae53c`.
Latest winning/peer publication `37a7d061bba28944163dfd4115aadd3c6552f659`. Actual primary issue `wqa-jax.1`, parent `wqa-jax`.
One additional isolated native node `wqa-xw7` was created solely to provide a valid
disconnected graph-race precondition, not to repeat create qualification.
Winner `agent-afc68d65-bbe9-4b1d-a12b-3a72d97120a9`; loser `agent-d2e31940-1e4b-40cb-8d60-ddc3b7710366`; exact intent IDs, queue hashes and five conflict
details are in races-result.json. All four final objects were compared with peer JSON.

The terminal title/claim conflict and raw losing queue remain preserved. There was
no unreviewed resolution, force/LWW, helper edit or extra publisher. Graph proof is
explicitly a native dry-run refusal, not a claim of actual concurrent push execution.
Isolated normal read/direct-refusal was tested; unavailable-writer queue preservation
is a separate NOT RUN surface. Specific stale close and no-advance failed push/restart
are not inferred from the exact stale-title or accepted-write lost-receipt proofs.

PR14 remote HEAD changed to `187d607584388efa31ab7394610bf1afb48a1978` during the last
bounded case. The safe checkpoint was completed on old immutable source only; PM was
asked for affected repeat scope in PR12#6641141167. New source has NOT RUN status.
No whole WI-A/cross-platform/release acceptance claim. WI-C da8b92e remains separately
FAIL/HOLD. No working project DB, merge, release, finalizer or real state migration.

QA fixture note: linked .bd-intents directory was initially absent; the test data
directory was created before its handoff. Earlier passed read/refusal cases were not
rerun, and no publication was repeated to repair harness/evidence.
