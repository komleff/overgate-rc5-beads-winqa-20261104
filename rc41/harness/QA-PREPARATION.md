# RC4.1 Windows QA preparation — no candidate run

Role: Windows QA / Codex GPT-6. Coordination: OverGate PR12; implementation: PR15.

Latest authority at preparation: PM HOLD6633466737. Both c557fa2 and e4a737d were NOT RUN on Windows by this agent. Candidate execution requires a new explicit exact-SHA packet. This document is preparation only, no install/bootstrap/restore commands have been run.

All future fixtures: new disposable directories beneath this artifact root, separate local Git repos and local bare origins; one sequential worker. Working U2/Toon/OverGate databases, prior rc.4 targets, global tool configuration and source checkout stay untouched. Recheck scoped native bd1.2.2 absolute executable path/SHA256, Git/Python/Bash versions and current station memory before launch. Source clone is new, detached at approved SHA, clean; compare PR HEAD immediately before starting. Stop and ask PM if HEAD differs or another HOLD supersedes the packet.

| Case | Source AC | Actual method and required observation | Status |
|---|---|---|---|
| Canonical staged sentinel | H1 | Snapshot HEAD, index bytes, sentinel bytes and bare-origin refs; run bootstrap once; controlled STOP before bd init/commit; all snapshots unchanged and no local DB | NOT RUN |
| Alternate clean index plus canonical staged sentinel | H1 | Separate new fixture; canonical index contains staged sentinel; GIT_INDEX_FILE points at a clean alternate index; same STOP and no mutation; preserve both index byte snapshots | NOT RUN |
| Clean fresh installation/bootstrap | H2 | First actual bootstrap; automatic init commit contains only Beads paths/.gitignore; untracked sentinel retained; obtain effective prefix via bd config list --json; active project pin equals that value | NOT RUN |
| Empty two-clone recovery | H2/H3 | New primary has valid empty published snapshot; commit project-owned config pin; new clone has tracked metadata/config but no ignored DB; restore empty store under pin, preserving metadata/project_id/config/index/HEAD/R and lastSeen, no Dolt remote | NOT RUN |
| Nonempty two-clone recovery | H2/H3 | Separate primary has two synthetic issues with chosen supported fields and typed dependency; canonical export freezes R; project pin committed; new clone restores exact IDs/full fields/edge and preserves all clone invariants | NOT RUN |
| Missing active tracked pin | H3/H4 | New source fixture commits config without active pin; clone with snapshot stops before local init; caller data is not substituted for trusted pin | NOT RUN |
| Forged caller receipt | H3/H4 | Use exact documented/rejected legacy input route once known from approved source; forged receipt cannot authorize missing/conflicting tracked pin; no init/publication | NOT RUN |
| Wrong prefix | H4 | New clone has committed conflicting tracked prefix; frozen valid snapshot namespace differs; controlled STOP before local init/publication | NOT RUN |
| Corrupt/missing snapshot or local pending | H4 | One or two negatives from final PM packet, each separate fixture; preserve raw input, R/HEAD/index/metadata/config and filesystem before/after; no repair/retry | NOT RUN |
| Installed docs/version closure | H5 | Fresh installed target checker/link checks; HOW_TO_USE QUICKSTART target resolves under source-defined ownership; manifest/helper/rule agree on bd1.2.2 | NOT RUN |

Record for every invocation: exact argv/stdin, cwd, selected nonsecret environment overrides, start/end, exit code, raw stdout/stderr. Preserve immutable binary hash and source Git SHA/tree/blob fingerprints. Do not call macOS-only qualification code. Do not call H6 (separate Mac QA), full source verification/CI, finalization, merge or release unless separately assigned.

For restore cases compare pre/post local HEAD, exact index bytes, tracked metadata/config bytes, original project_id, frozen beads-backup R, lastSeen and Dolt remote list. Compare native source readback against restored IDs, full supported issue fields and exact edge types; unordered collection ordering is not a data mismatch. Empty and nonempty snapshots are separate cases, never infer one from the other.

On first real unsupported command/field, product refusal or data/invariant mismatch: stop that single authorized run, preserve raw evidence, mark remaining cases NOT RUN, post precise failure to PR12 for Developer via PM; do not modify source or retry through another path. Preserve infrastructure errors separately and do not fabricate product verdicts.

Final report: H | PASS/FAIL/NOT RUN | actual method | immutable evidence; exact source SHA/binary path/hash; tested-content fingerprint; versions; explicit not-tested boundary. Publish in PR12 with role/model and immutable links in a separate QA evidence repository. This is scoped Windows evidence, not overall rc.4.1 acceptance.
