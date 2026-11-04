# WINDOWS QA → PM / WI-B early B1/B2 `65f21ed`

Role/model: Windows QA / Codex GPT-6. UTC: 2026-11-04T22:34:02.521183+00:00.
Commit: `65f21ed72b6cbc85cd7b5ed41502e3a84a464739`; base `3096e550bfd6f4ff73c987812a2dda2c7d339669`.
Content-Fingerprint: `f51ba29323722d0732c4aa93213b70fad906129541c7c96b83f6c3c750a9c9ff` (5 paths + exact 1024-byte CONTRACT).
Plan blob: `5dedca627bf31916b871d85e88c4906551aaf576`; CONTRACT SHA256 `32b9d90893e2a686506b3210403857c43e4b422b091d4fce0cbe11426834c795`.
Source: PR12 [bounded RUN 6643640897](https://github.com/komleff/overgate/pull/12#issuecomment-6643640897), PR17 B1/B2/I1/I3.

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
| fresh-managed-closure-no-init | B1 | Native plan/apply + all Beads source/target SHA256; installed checker; no .beads/registration/queue; origin byte unchanged | PASS | [receipt](evidence/fresh-result.json) |
| no-beads | B1 | Actual native plan/apply/checker; none; complete Beads closure absent; prior false upgrade has no --no-beads override | PASS | [receipt](evidence/no-beads-result.json) |
| old-beads-false | B1 | Actual native plan/apply/checker; none; complete Beads closure absent; prior false upgrade has no --no-beads override | PASS | [receipt](evidence/old-beads-false-result.json) |
| local-native-legacy | B2 | Actual plan records blocked inventory; approved apply RC1; full target/Git/backup/remote hashes unchanged | PASS | [receipt](evidence/local-native-legacy-apply-readonly.json) |
| pending-only | B2 | Actual plan records blocked inventory; approved apply RC1; full target/Git/backup/remote hashes unchanged | PASS | [receipt](evidence/pending-only-apply-readonly.json) |
| unknown-receipt | B2 | Actual plan records blocked inventory; approved apply RC1; full target/Git/backup/remote hashes unchanged | PASS | [receipt](evidence/unknown-receipt-apply-readonly.json) |
| remote-present | B2 | Actual plan records blocked inventory; approved apply RC1; full target/Git/backup/remote hashes unchanged | PASS | [receipt](evidence/remote-present-apply-readonly.json) |
| remote-unavailable | B2 | Actual plan records blocked inventory; approved apply RC1; full target/Git/backup/remote hashes unchanged | PASS | [receipt](evidence/remote-unavailable-apply-readonly.json) |
| local-plan-apply-drift | B2 | Exact approved plan then new pending; actual apply RC1 drift before target/backup write | PASS | [receipt](evidence/local-drift-apply-readonly.json) |
| remote-R-advance | B2 | Synthetic known local remote advance; actual approved apply refuses exact frozen-R drift, preserves injected remote | PASS | [receipt](evidence/remote-advance-result.json) |
| symlink | B2 | Native Windows symlink creation unavailable; no emulation | NOT RUN | [receipt](evidence/symlink-capability.json) |
| missing-managed-import | B1/I3 | Exact-source exported validator with one manifest import dependency omitted in memory; actual checker refuses projected temp closure; source/installed target untouched | PASS | [receipt](evidence/closure-negative-result.json) |
| permissions-negative | B2 | No reliable denied-access fixture established under current Windows account; no mock substituted | NOT RUN | [receipt](evidence/results.json) |
| activation-switch-fence-publication | B3/B4 | Explicitly excluded by early B1/B2 packet | NOT RUN | [receipt](evidence/results.json) |

All native subprocess outputs were captured as raw `.stdout.bin` / `.stderr.bin` before decoding. Each JSON receipt records exact argv/cwd/exit, hashes and displayed output. Plans and approvals are frozen in `plans/`; approvals are **synthetic disposable-test inputs only**, not real project/operator approvals. Before/after snapshots include every target file, Git metadata, backup directories, remote file/object/ref hashes, and symlink identity where supported. Plan/apply refusals preserved the exact captured target/backup/remote bytes.

The fresh and no-Beads targets are new independent disposable clones of the prepared local bare origin. The old `beads:false` case copies the actual released rc.4.1 `3f3246c` baseline payload/state into a new disposable clone, then upgrades with no no-Beads override. Original frozen preparation stores remain intact; the real native legacy store was inventoried read-only, not opened by bd. `bd --version` only, known scoped binary1.2.2 SHA256 `b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de`; Git2.51.2.windows.1, Git Bash5.2.37, Python3.14.0, Node24.11.0. Full raw version receipts are included.

The remote advance is an explicit local fixture injection: a new same-tree Git commit advances only the disposable `beads-backup` ref between plan/apply. It is not a managed task publication or activation. The missing-import negative calls the exact source validator against an in-memory manifest omission and records the actual projected checker refusal; source SHA stays pinned. No synthetic alternate source commit is claimed qualified.

Target SHA is the synthetic fixture code HEAD recorded in `fresh-result.json`; task publication SHA/actual new task ID are **N/A**. There was no task lifecycle run. B3 activation/trusted-main writes, B4 migration/protocol switch/old-writer fence/publication/rollback-after-publication, live Claude/Codex sessions, full local verifier/CI qualification and whole WI-B/release verdict are **NOT RUN here**. No working U2/Toon/OverGate checkout/DB/hooks/settings, merge/release or finalize were used.
