from qa_common import *
SRC=B/'source-3096e55';contract=(R/'pr-contract.txt').read_bytes()
paths=text(git('fp-changed-paths',['-C',SRC,'diff','--name-only','3f3246c3a3b62377fc02aad05283cae1ef5d4e2d',PIN],B)).splitlines()
blobs={p:text(git('fp-blob-'+str(i),['-C',SRC,'rev-parse',PIN+':'+p],B)) for i,p in enumerate(sorted(paths))}
fingerprint=sha(''.join(p+' '+v+'\n' for p,v in blobs.items()).encode()+contract)
check('expected-content-fingerprint',fingerprint=='1c4215a4ed226aec548dc6f522459dd40901c91c94c871949601e07e88107f7d',fingerprint)
save('source-contract-fingerprint',dict(source=PIN,content_fingerprint=fingerprint,contract_bytes=len(contract),contract_sha256=sha(contract),plan_blob='ceefa86186c62b4c754a59841710128a1ee9bbce',paths=blobs))
result=json.loads((E/'qualification-result.json').read_text(encoding='utf-8'))
save('qa-result',dict(result='PASS scoped AC6/AC9 Windows qualification regression',source=PIN,content_fingerprint=fingerprint,
 actual_native_binary=result['native'],native_platform=result['platform'],DB_or_task_write=False,full_route_smoke='NOT RUN on3096e55; unchanged source/runtime equivalence to accepted0a8685e + native real binary gate check',
 reused_native_checkpoint='0ccd30cf63896db09f41d9e2a8e19c71c0b120bd',reused_native_supplement='08168676eb58fbe44cae1ca56ce3bf752abc30ea'))
report='''# Windows QA — WI-A final allowlist affected regression

Role/model: Windows QA / Codex GPT-6.
Source: `3096e550bfd6f4ff73c987812a2dda2c7d339669`.
Full 37-path+contract fingerprint `{fingerprint}`.
Contract1255 bytes / SHA256 40cfc7c8320c921e7d66c9c74f7769b61598b6841670e05b2c795aa2c7adfc0a;
plan blob ceefa86186c62b4c754a59841710128a1ee9bbce.

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
| Real native Windows binary still qualified | AC6/9 | Actual Windows Node process; default stream SHA256 and actual process.platform, real pinned bd.exe | PASS | evidence/qualification-result.json; native-binary-hash.json; native-bd-version.json |
| Actual changed executable bytes | AC6 | Disposable bd.exe copy with appended bytes; real stream hash; no execution of modified binary | PASS refusal | qualification-result.json; tampered-binary-hash.json |
| Linux digest presented as win32 | AC6 | Exported qualifyBinary function platform/digest matrix with injected reported Linux digest; no live Linux execution claimed | PASS refusal | qualification-result.json |
| Windows actual digest under Linux platform | AC6 | Real stream fingerprint of Windows exe with explicit mismatched platform argument | PASS refusal | qualification-result.json |
| No store/task write | AC6 | .beads bytes unchanged; no Dolt/DB created; no task/registration/publisher calls | PASS | no-store-or-task-write.json |
| Guard/reader/task runtime equivalence | AC6/9 | Exact old/new Git blob IDs for10 guard/reader/contract/Git/journal/transaction/setup/routes; only CLI qualification data/platform list runtime diff | PASS | runtime-equivalence.json; qualifier-affected-diff.json |
| Full native publisher lifecycle on this new SHA | AC1/3–5/9 | Not repeated per bounded PM packet; use frozen accepted0a8685e native evidence and unchanged runtime blobs | NOT RUN here | qa-result.json; prior immutable checkpoint/supplement |

Native bd path: D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe.
Version1.2.2 (6c124203e), real SHA256 b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de.
Actual process.platform win32; Node24.11.0. The changed .exe was never executed or
published; only its path and computed digest are evidence. Cross-platform Linux case
uses the function's documented test fingerprint callback, explicitly a function
decision check, not a Windows execution of a Linux ELF. Actual Linux production
route proof is a separate exact-SHA Ubuntu CI record, not this Windows result.

Accepted native Windows source0a8685e checkpoint: immutable commit
0ccd30cf63896db09f41d9e2a8e19c71c0b120bd; complete remaining supplement
08168676eb58fbe44cae1ca56ce3bf752abc30ea. No stale queue republished, new target SHA/ID
created, source helper changed, or working DB used. Current fixture is qualification
only; target/task SHA is N/A. Native lifecycle/peer old proof latest R was
37a7d061bba28944163dfd4115aadd3c6552f659; it is not relabelled as a3096e55 publication.

PASS scoped for affected Windows gate. Previous explicit NOT RUN surfaces remain
NOT RUN unless separately closed by PM. No whole WI-A/release acceptance, merge,
release or trusted finalizer. WI-C source/fixtures/evidence remain separate.
'''.format(fingerprint=fingerprint)
(R/'REPORT.md').write_text(report,encoding='utf-8')
print('Affected Windows allowlist report PASS '+fingerprint)
