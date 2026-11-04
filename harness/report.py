import json,hashlib
from qa import B,E,BD,write,run
def read(n):return json.loads((E/n).read_text(encoding='utf-8'))
p=read('prefix-result.json');r=read('roundtrip-result.json');s=read('source-complete.json');b=read('binary.json')
assert p['result']==r['result']=='PASS' and not(E/'STOP.json').exists()
assert hashlib.sha256(BD.read_bytes()).hexdigest()==b['sha256']
versions={'git':run(['git','--version'],label='final-git-version').strip(),'python':run([__import__('sys').executable,'--version'],label='final-python-version').strip()}
fields={iid:len(names) for iid,names in r['compared_fields'].items()}
environment={'binary':b,'versions':versions,'source_git_sha':r['qa-source_git_head'],'target_git_sha':r['qa-target_git_head'],'source_store':r['source_root'],'target_store':r['target_root'],'prefix_root':p['root'],'show_field_counts':fields,'commands_failed':False,'source_pr14_tested':False,'publisher_tested':False,'result':'PASS: selected native CLI operations and round-trip'}
write('final-summary.json',environment)
report=f'''## WINDOWS QA → PM / FINAL — rc.5 Beads native CLI prequalification

**Result: PASS for this single disposable Windows native CLI capability/round-trip.** Publisher code and rc.5 acceptance **NOT RUN**. This report is not bound to any changing PR14 source HEAD.

Role/model: Windows QA / Codex GPT-6 (exact preset unavailable), 2026-11-04 Asia/Novosibirsk. Source: actual native Windows `bd1.2.2 (6c124203e)` binary `{b['absolute_path']}`, SHA256 `{b['sha256']}` rechecked after execution. {versions['git']}; {versions['python']}. Contract: [packet6629030464](https://github.com/komleff/overgate/pull/12#issuecomment-6629030464), [urgent prefix scope6629428649](https://github.com/komleff/overgate/pull/12#issuecomment-6629428649), [single-run acknowledgement6630607183](https://github.com/komleff/overgate/pull/12#issuecomment-6630607183).

Only new roots under `D:/CodexArtifacts/overgate-rc5-beads-winqa-20261104`: `big-heroes`, `qa-source`, `qa-target`; each native embedded Dolt, each Git repo **without remotes**. A separate evidence-publication checkout has the QA GitHub remote. Source Git SHA `{r['qa-source_git_head']}`, target Git SHA `{r['qa-target_git_head']}` identify these disposable Git roots, not a publisher candidate or the mutable Dolt working sets. No working U2/OverGate stores, old rc.4 target, PR14 source, release, macOS qualification script or parallel QA workers used.

| Field / operation | Actual CLI result | Round-trip PASS/FAIL/NOT RUN | Raw evidence |
|---|---|---|---|
| Absolute binary, version, hash | Exact scoped1.2.2; final binary hash unchanged | PASS | [binary](binary.json), [final summary](final-summary.json) |
| Help/JSON capabilities | init/create/update/close/comments add/dep add/export/import/show/list actual help captured; issue operations returned parseable JSON | PASS for executed issue operations | help-*.json, operation receipts below |
| Hyphen prefix | `dolt_database=big_heroes`; `config list issue_prefix=big-heroes`; actual ID `big-heroes-aad` | PASS | [prefix result](prefix-result.json), [config raw](prefix-config-list.json), [show raw](prefix-show.json) |
| Two isolated initializations with prefixqa | init --json exit0; embedded, DB nameqa; stdout is **text, not JSON** | PASS for init; no structured init stdout claim | [source init](source-bd-init.json), [target init](target-bd-init.json) |
| Create/nested issue ID | Epic `qa-yzw`, peer `qa-3qo`, child `qa-yzw.1`; parent relation preserved | PASS | [initial child](source-child-initial-show.json), [imported child](target-show-qa-yzw.1.json) |
| Atomic claim | update --claim gives assignee windows-qa/status in_progress | PASS | [claim raw](source-claim.json), [claimed readback](source-show-claimed.json) |
| Update and close | Updated title and content; closed with explicit close_reason | PASS | [update](source-update.json), [close](source-close.json), [final source](source-complete.json) |
| description/design/acceptance_criteria/notes | Multiline Cyrillic+ASCII values match chosen input before export and actual target readback | PASS | [source expected + actual](source-complete.json), [round-trip comparison](roundtrip-result.json) |
| labels | qa-native,roundtrip preserved | PASS | [initial raw](source-create-child.json), [target child](target-show-qa-yzw.1.json) |
| Structured metadata | Nested object, unicode, numeric values, boolean true and array; update revision2 preserved with JSON types | PASS | [source update](source-show-updated.json), [target child](target-show-qa-yzw.1.json) |
| Status/priority/type/assignee/owner/created_by/timestamps/close_reason | All actual source show fields compared to target, no mismatch | PASS | [complete field inventory](roundtrip-result.json) |
| Comment | UUID, issue_id, author, text/newline/Cyrillic, persisted created_at all equal before/after | PASS | [source comments](source-final-comments.json), [target comments](target-comments.json) |
| Typed dependencies | child→parent parent-child and child→peer discovered-from preserved | PASS | [dep add](source-dep-add.json), [source child](source-final-show-child_id.json), [target child](target-show-qa-yzw.1.json) |
| Export all | export --all --output writes3 native JSONL records | PASS | [export call](source-export.json), [native JSONL](native-export.jsonl) |
| Import JSON | import file --json gives created3/skipped0 and exact IDs | PASS | [import raw](target-import.json), [import structured](target-import-structured.json) |
| show/list readback | All3 IDs; all show fields; full list including closed issue; comment and edges equal | PASS | [round-trip result](roundtrip-result.json), [source list](source-final-list.json), [target list](target-list.json) |
| Real publisher/PR14 code/rc.5 acceptance | Not part of native CLI prequalification | NOT RUN | PM will issue final-HEAD acceptance separately |

Important CLI capability detail: `bd init --json` accepts the flag but prints ordinary initialization text. Do not parse its stdout as JSON; `.beads/metadata.json` and config/readback provide structured facts. `create`, `update --claim`, `update`, `close`, `comments add/list`, `dep add`, `show`, `list`, and `import --json` produced actual parseable JSON here; export output is JSONL. No requested command/field was rejected and no persisted round-trip value changed.

Prefix conclusion confirmed by actual outputs: metadata database name `big_heroes` is not issue prefix `big-heroes`. Generated `.beads/config.yaml` contains only commented `# issue-prefix: ""`; `bd config list --json` returns persisted DB key `issue_prefix`. [Exact config file](prefix-config.yaml). Source/target roots use actual prefixqa, each stored independently despite both database names beingqa.

Method: compare initial/updated requested input values to source readback, then compare every actual source `show --json` field for all3 issues to the imported `show` output; also compare full `list --all --json` keyed by issue ID and exact persisted comment objects. Field counts: {json.dumps(fields,sort_keys=True)}. Only order of semantically unordered labels/dependencies/dependents is normalized; JSON scalar types, strings/newlines, timestamps, nested IDs, comment UUID and edge types are unchanged. Native export SHA256 `{s['export_sha256']}`. Source artifacts/stores/export retained; no cleanup, retry or workaround of a failed command was needed.

This is preliminary CLI evidence for AC5/AC9, not writer/publisher readiness or release permission. Follow-up remains PM-controlled in PR14; reports/instructions stay on PR12.
'''
write('final-report.md',report)
print(json.dumps({'result':'PASS: native prequalification only','field_counts':fields,'report':str(E/'final-report.md')}))
