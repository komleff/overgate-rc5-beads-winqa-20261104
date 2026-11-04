## WINDOWS QA → PM / QA EXECUTION — RC4.1 H2 empty FAIL

Role/model: Windows QA / Codex GPT-6 (exact preset unavailable). Source `825c0b9d9e2ad7fe61182836649008a47a34c0c4`, clean detached clone; PM RUN6633997887 + start6634028533. Tested-content fingerprint `0cc9cd7c9c8375d352e49d489f6929428efd275e4e05cdb934bd5bab9197c545` ([exact blobs/contract method](source-fingerprint.json)). Binary `D:\CodexArtifacts\overgate-rc4-winqa-20261103\tools\bd.exe`, `bd1.2.2 (6c124203e)`, SHA256 `b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de`. Git2.51.2.windows.1, native Git Bash5.2.37, Python3.14.0. Codex0.154.0 availability only, H6 not executed.

**H2 empty FAIL. Run stopped at its first real failure; no retry or source repair.**

| H | PASS/FAIL/NOT RUN | Actual method / observation | Exact evidence |
|---|---|---|---|
| H2 fresh primary substeps | PASS scoped substeps | Actual Git Bash bootstrap exit0; Beads-only init commit; untracked sentinel preserved; effective prefixbig-heroes; active pin created, then project commit/push | [primary call](H2-empty-primary-bootstrap.json), [case checks](H2-empty-result.json), project-pin commit/push receipts |
| H2 empty second clone | FAIL | Tracked metadata+pin, no local DB, frozen empty snapshot. Actual bootstrap exit1 in bd-sync-restore child; DB created before STOP | [failing argv/stdout/stderr](H2-empty-clone-bootstrap.json), [full result](H2-empty-result.json) |
| H2 preservation facts | PASS scoped observations | HEAD/index/README/metadata/config/origin refs unchanged; DB absent→present | [before](H2-empty-clone-before.json), [after](H2-empty-clone-after.json) |
| H3 populated | NOT RUN | First-FAIL stop rule | RUN6633997887 |
| H1 staged / alternate index | NOT RUN | First-FAIL stop rule | Prepared baseline only, no candidate case invoked |
| H4 tracked prefix / forged receipt / corrupt snapshot | NOT RUN | First-FAIL stop rule | No candidate negative case invoked |
| H5 installed links/version | NOT RUN | First-FAIL stop rule | No installer fixture invoked |
| H6 / overall rc.4.1 acceptance / merge/release/finalize | NOT RUN | Outside this Windows packet | No readiness claim |

Primary: `D:\CodexArtifacts\overgate-rc41-winqa-20261104\cases\empty\big-heroes`. Clone: `D:\CodexArtifacts\overgate-rc41-winqa-20261104\cases\empty\peer-empty`. Frozen `beads-backup R=9ab3001ce8979a8d73868d47c47f4d8f721abe19`. Clone HEAD `b02a1172f9dbd2246a2aa4b7d1ea459445bd49c3`, exact index SHA256 `1196c88837156f7dec3a6c8ba37055c5c264881227e31faf8d69482beff8d503` unchanged. Metadata SHA256 `4758f7e9962888b820d7f06220624b3ddb25a71a0e3bc8079c1a7c7d16428bfc` and config SHA256 `ea94dc4f0da51dcf87072043a0d561ff14adc0706518a44418bc092ec664f511` unchanged. No real project DB or GitHub production ref used; origin is a new local bare repository.

The failed call is exactly native `bash scripts/bd-bootstrap.sh` from the clone root, with `BD_BOOTSTRAP_EXPECTED_R=9ab3001ce8979a8d73868d47c47f4d8f721abe19`. It exits1 after approximately3s; nested failure names `C:\Program Files\Git\usr\bin\bash.exe scripts/bd-sync-restore.sh` and `origin/beads-backup`. The pinned restore source has the matching missing-snapshot diagnostic at line51. Read-only Git inspection confirms the clone's remote-tracking ref equalsR and `.beads/issues.jsonl` exists as zero-byte blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`: [diagnostic](H2-readonly-diagnostic.json). Underlying cause is not asserted by QA.

Capture limit: the harness decoded native stderr as UTF8 with replacement; Cyrillic characters in the nested diagnostic are garbled in the recorded text. ASCII argv, exit code and state observations are intact. Original undecoded stderr bytes were not retained for this completed invocation; no rerun was made to improve the log. The receipt is exact captured text, not a claim of byte-exact original stderr. Future native capture needs raw-byte preservation; this does not turn the observed nonzero runtime result into PASS.

User-requested PM_ERR/DOC_PR self-check: target remains a working OverGate install/clone for the new project. My earlier passive notification setup did not perform active PM follow-up; I also spent excess time packaging evidence. The present H2 failure directly violates the requested clone acceptance. Minimal next action is Developer triage/fix via PM, then only affected Windows recheck on a new explicit pin. No expanded product guarantee, reviewer swarm, policy rewrite or source fix by QA.

Both source and all disposable roots/bare origin are retained. No cleanup, reset, force, alternate invocation, helper replay or additional candidate run followed the refusal. Remaining cases stay NOT RUN. [Prepared environment/baselines](workspace-ready.json).
