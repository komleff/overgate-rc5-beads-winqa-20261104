# Windows QA EXECUTION — WI-C FAIL, da8b92e

Role/model: Windows QA / Codex GPT-6.
Source: `da8b92e5b83dab0951775f117f0241b84d5a4f76`. Content fingerprint: `5348da2a19b0c8c33980933496b8e55d20b1e124a19c05d254397c64208aa223`.
Plan blob: e56ec8ff7f49e4a85483140ea811dabd42d6de5e.
Contract: 1060 bytes, SHA256 `118a2da8d515cbd809293a8379ecafa7f536b401e419619a521fe76ed36d45a6`.

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
| Six native positive root paths | C1 | ASCII, space, Cyrillic, parentheses, apostrophe and C-drive checkout; native [bash.exe,-c,exact managed entry], full UTF-8 JSON | PASS scoped | evidence/c1-result.json; each *-ls-denied.payload/json |
| Printed command exact-byte hook replay and real execution | C1/P3 | Original printed bytes accepted by same hook, then executed with pwd -P; expected root independently queried by same native Git Bash | PASS scoped, 6/6 | *-printed-command.bin, *-same-byte-hook-replay.json, *-execute-printed.json, *-root-pwd.json |
| Tail/substitution/variable/glob/relative/second cd/foreign checkout/drive-relative negatives | C2/P1/P2/P4 | 12 named commands; spoofed project-dir; 3 complex-path tails; sentinel absent | PASS scoped for executed subset | evidence/c2-*.payload.json and raw stdout/stderr |
| Unquoted DOS same-root absolute cd | C2/C3 | D:/ form from own subdir | PASS scoped | evidence/c2-ascii-dos-same-root.json |
| Unquoted MSYS same-root absolute cd | C2/C3/P3/P4 | /d/ form of the same checkout from own subdir | **FAIL**, actual 2, expected 0 | evidence/c2-ascii-msys-same-root.payload.json, .json and .stderr.bin |
| Remaining cases, installer smoke/upgrade, portability and root guards | C2–C6 | Stopped at first real FAIL | NOT RUN | evidence/stop-scope.json |
| Exact-SHA Windows CI | C6 | PM reported five comparison failures in run 41901054956 | FAIL (external evidence) | PR16#6640622414; not rerun by this worker |

Exact failing payload: `cd /d/CodexArtifacts/overgate-rc5-wic-winqa-20261105/run-da8b92e/cases/project-ascii`.
Cwd: that checkout's `own-subdir/deep`.
Immediately previous successful payload used `D:/CodexArtifacts/.../cases/project-ascii`.
Independent baseline native `pwd -P` returned exactly the rejected `/d/.../project-ascii`.
The hook's stderr prints a recovery command using `D:/.../project-ascii`.
Thus the failure is the actual hook exit code for a same-root alias, not a Python
Path('/d/...').resolve() comparison. No test claim treats the red CI as product PASS.

Binary entry: C:/Program Files/Git/bin/bash.exe, 5.2.37. Git 2.51.2.windows.1;
QA Python C:/Python314/python.exe 3.14.0. Actual hook-selected python3 executable/version
are independently inventoried in evidence/hook-python-resolution.json.
All raw stdout/stderr were captured as binary before display decoding; UTF-8 JSON,
exact printed/executed command bytes and exact full entry argv are retained.
No source fix, retry or additional product cases after FAIL. Sentinel absent: True.

Fixtures are source checkouts with exact managed hook bytes, not completed installer
acceptance. Installer auto/bypass upgrade/custom hook conflict and installed native smoke
are explicitly NOT RUN. No working U2/Toon/OverGate state/hooks/settings/DB touched;
no merge/release/finalizer. WI-A evidence remains separate and intact.
