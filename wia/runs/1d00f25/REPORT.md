# Windows QA checkpoint — WI-A on HOLD

Role/model: Windows QA / Codex GPT-6 (exact preset unavailable).
Source: `1d00f257202dbced5894b841e97f1945dad7a158`.
Fixture trusted main: `020e7ad5fbc1c4d078e8f0ea349bd908df6ffa64`.
Published task snapshot: `b4e8a10366dc205dbae2aef32a0a8487a35588f3`.
Real issue ID: `wqa-z5e`; claim actor `agent-a2081464-1158-48ce-b6c4-42f3324f9918`.

Overall: **NOT RUN for WI-A acceptance — PM HOLD 6639435396**.
Residual AC4 blocker is independently reported by Reviewer in PR14#6639476168;
Windows did not reproduce or close it.

| Case | AC | Method | Result | Evidence |
|---|---|---|---|---|
| Native CLI identity | AC5/AC9 precondition | Native version and SHA256 | PASS scoped | evidence/cli-hash.json, cli-version.json |
| Candidate bytes and trusted fixture main | AC6 precondition | Canonical Git bytes/fingerprint, source/target SHA separation | PASS scoped | evidence/source-fingerprint.json, fixture-target-candidate-byte-equivalence.json |
| Publisher setup and verified-absent bootstrap | AC6/AC9 precondition | Native setup prepare/install, ZERO read-state, bootstrap | PASS scoped | evidence/setup-result.json, setup-prepare.json, setup-install.json, publisher-bootstrap.json |
| Typed create → claim → publication | AC1/AC9 subset | Native qualified bd, real non-tmp ID, claims.confirmed | PASS scoped | evidence/create-claim-receipt.json, queues/create-claim.raw.jsonl, queues/create-claim.v2.jsonl |
| Independent peer full-object read-back | AC5/AC9 subset | Primary clone bd-read.sh show --json, exact object and published ref equality | PASS scoped | evidence/create-claim-peer-full-object.json, create-claim-peer-same-sha.json |
| Supplied fields preserved | AC5 subset | Existing captured bytes only; labels as unordered set, metadata arrays ordered | PASS scoped | evidence/recorded-byte-field-comparison.json |
| Update/close, linked queue, isolated reader | AC1/AC9 | Planned native cases | NOT RUN | PM HOLD before these cases |
| B1/B2/B3 addressed negatives | AC4/AC5/AC6 | Planned guard/reader/malformed-empty/legacy downgrade negatives | NOT RUN | PM HOLD before these cases |
| Race/retry, stale operations, conflicts | AC3/AC4 | Planned disposable cases | NOT RUN | PM HOLD before these cases |
| Linux/macOS/whole-release | AC9/release | Outside Windows checkpoint | NOT RUN | Not a cross-platform or release verdict |

Native binary: `D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe`,
`bd version 1.2.2 (6c124203e)`, SHA256
`b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de`.
Git 2.51.2.windows.1, Git Bash 5.2.37, Python 3.14.0, Node 24.11.0.

Source/contract binding: evidence/checkpoint-source-contract.json.
Contract 1255 bytes, SHA256 `40cfc7c8320c921e7d66c9c74f7769b61598b6841670e05b2c795aa2c7adfc0a`;
plan blob `ceefa86186c62b4c754a59841710128a1ee9bbce`;
scripts tree `853c8480eb4f38b91e73cef92a1a5e58606a5775`.
Combined scoped fingerprint `75d6da66af2e6cc7f425e97cf80784bca3dcc3dc0da0a207721e28a94c8922a0`.
Fingerprint algorithm: SHA256 of scoped source inventory SHA256 + LF + contract SHA256 + LF;
the complete path/hash inventory is saved.

All operations ran only in the dedicated disposable WI-A fixture. Native bd init
created one fixture project-state Git commit, which was fast-forwarded to local
bare main. Candidate helper/docs bytes remained exact. Publisher had no actual
legacy store or pending queue at bootstrap. Initial reference metadata is tracked
source, not an existing database. Fixture primary has a newly created embedded
synthetic DB; no working U2/Toon/OverGate DB was used. The registered publisher
is actor-b; its bare origin has no GitHub remote. Source stayed unchanged.

## QA harness limitations and corrections

Original receipts remain intact; no product publication was retried.

- Initial shallow Git transfer was refused by local bare origin before candidate
  execution. Complete ancestry fetch resolved this fixture transport error.
- An overly strict QA assertion mistook tracked metadata.json for an existing
  database. Actual publisher database/redirect/endpoint files were absent.
- Another QA assertion initially required source commit == synthetic target main.
  Native bd init creates a project-state commit; current RUN explicitly binds
  exact helper bytes and trusted fixture HEAD == origin/main. Both were verified.
- A QA comparison treated labels as ordered. Actual labels contained the same
  two distinct strings. Saved publication/peer bytes were compared with set
  semantics; no candidate rerun. Original false FAIL remains in create-field-labels.json.
- First postprocessing opened UTF-8 JSON through Windows locale defaults, producing
  false Unicode comparisons. That diagnostic is retained separately. Explicit
  UTF-8 decoding of the same saved raw data confirms all supplied fields. This
  correction ran no product operations.

Raw stdout/stderr are binary files, with hashes in command receipts. Git refs,
queues, published snapshot bytes and managed journal/control checkpoint are saved.
Update/close, additional publications and all negatives stopped before execution.
No merge, release, finalizer or real migration was performed.
