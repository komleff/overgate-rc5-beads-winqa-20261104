from native_common import *
import sys
fp=json.loads((E/'source-fingerprint.json').read_text(encoding='utf-8'));contract=(R/'pr-contract.txt').read_bytes()
blobs={p:decode(run('fp-blob-'+str(i),['git','-C',SRC,'rev-parse',PIN+':'+p]).stdout).strip() for i,p in enumerate(sorted(fp['files']))}
fingerprint=sha(''.join(p+' '+v+'\n' for p,v in blobs.items()).encode()+contract)
check('expected-source-fingerprint',fingerprint=='536044bb778a67a193afeee6aa5a196bcb1ba5bfcef883a0da6e7e6fa96207cd',fingerprint)
save('source-contract-fingerprint',dict(source=PIN,content_fingerprint=fingerprint,contract_bytes=len(contract),contract_sha256=sha(contract),plan_blob='e56ec8ff7f49e4a85483140ea811dabd42d6de5e',blobs=blobs))
installed=json.loads((E/'installer-result.json').read_text(encoding='utf-8'))
run('inventory-git',['git','--version']);run('inventory-bash',[BASH,'--version']);save('inventory-python',dict(executable=sys.executable,version=sys.version))
save('qa-result',dict(result='PASS scoped native Windows C1-C5/installed smoke; C6 CI/finalizer separate',source=PIN,content_fingerprint=fingerprint,
 passed=['exact old apostrophe root read','six-root hint replay and actual execution','C2 injection/identity/no sentinel','own canonical recovery under spoofed Git env; foreign denied','DOS/MSYS aliases C and D','missing dispatcher','outside-Git legacy simple recovery and honest guidance','native root guards/test gate','auto/bypass rc4.1 installer upgrade with installed native smoke','custom managed hook conflict before target write','C5 existing portability/mutation tests'],
 not_run=['full local verify-reference by independent Windows QA','live Claude model session','trusted finalizer/release'],external_ci='see ci-jobs-snapshot.json'))
report='''# Windows QA EXECUTION — WI-C 89128db, scoped PASS

Role/model: Windows QA / Codex GPT-6. Source `{source}`.
Full 18-path+contract fingerprint `{fingerprint}`.
Plan blob e56ec8ff7f49e4a85483140ea811dabd42d6de5e;
contract 1060 bytes / SHA256 118a2da8d515cbd809293a8379ecafa7f536b401e419619a521fe76ed36d45a6.

| Test case | AC | Method | Result | Evidence |
|---|---|---|---|---|
| Exact old apostrophe root failure | C3/P3 | New exact launcher in preserved failed root; unchanged candidate settings; native hook git log RC0 and actual git log execution succeeds | PASS | evidence/exact-root-result.json; exact-apostrophe-root-read.json; original-failed-launcher.bin |
| Six-root recovery and executed cwd | C1 | Native full JSON/exact entry; ASCII, space, Cyrillic, parentheses, apostrophe and C drive; printed bytes accepted, executed pwd matches independent pwd | PASS 6/6 | evidence/c1-result.json; *-printed-command.bin, *-execute-printed.json |
| Injection/foreign/relative/drive variants | C2 | Tail ;/&&/newline, substitution/backtick, variable/glob, second cd, other dispatcher, relative/drive-relative, different real drive; no sentinel | PASS | evidence/c2-c4-result.json; c2-*.payload.json/.json/.bin |
| Spoofed Git env canonical own/foreign | C1/C2/P4 | Own printed canonical recovery RC0 despite foreign GIT_DIR/GIT_WORK_TREE; foreign canonical target RC2 | PASS | ci-spoofed-git-own-canonical.json; ci-spoofed-git-foreign-canonical-denied.json |
| Missing dispatcher; outside Git | C2/C4 | Missing dispatcher target refused; outside-Git simple unquoted absolute cd retained, complex quoted refused with root-session guidance | PASS | c2-missing-dispatcher.json; c3-outside-legacy-simple-cd.json; c4-*.json |
| Root guards and test budget handoff | C3 | Root main mutation/readiness denied; existing 3 native RootScenarios incl red/green project verifier gate | PASS scoped | c3-root-*.json; c3-existing-native-root-scenarios.json |
| Installer rc4.1 auto/bypass upgrade | C3/C6 installed subset | Full baseline payload3f3246c -> candidate89128db; frozen synthetic test approval; exact settings/runtime bytes and mode preserved, no-Beads closure, project README preserved | PASS 2/2 | evidence/installer-result.json; installer-plans/*.json |
| Installed runtime in combined complex roots | C1/C3 | Native root read/readiness denial and nested recovery printed/replayed/executed in both upgraded targets | PASS | installer-*-installed-*.json |
| Modified managed runtime hook | C3 | Current plan reports custom-hook conflict; apply RC1 before any target/backup change | PASS | installer-custom-hook-plan-refusal.json; installer-custom-target-unchanged.json |
| Generic active names / mutation | C5 | Existing targeted two-test producer/consumer + negative mutation suite on native Python | PASS | c5-result.json; c5-existing-portability-and-mutation.json |
| Full local independent reference/live Claude/finalizer | C6 / separate surfaces | Not executed by Windows QA; Developer/CI separately evidenced | NOT RUN here | qa-result.json; ci-jobs-snapshot.json |

Installer source is exact current89128db; baseline reads frozen released rc.4.1 payload
3f3246c3a3b62377fc02aad05283cae1ef5d4e2d. Synthetic fixture approval is only test input,
not a real-project PLAN_READY/permission. No real target was installed or upgraded.
Auto and bypass combined complex target roots, exact source SHA/install-state,
settings/launcher hashes and executed pwd are in installer-result.json.
Both targets contain apostrophe, spaces, Cyrillic and parentheses.

Original da8b92e/82603f8 FAIL reports remain immutable. Only the expressly requested
saved failed fixture received current launcher for exact affected repro; old launcher
bytes preserved. All six new source checkouts and two installed targets are separate.
DOS-quoted noncanonical spelling was not promoted to an extra product requirement;
spoofed-Git recovery uses actual printed canonical bytes per amended PM contract.

Git Bash C:/Program Files/Git/bin/bash.exe 5.2.37; Git 2.51.2.windows.1;
native QA/hook Python C:/Python314/python.exe 3.14.0. Raw binary stdout/stderr,
full argv/payload JSON, printed/executed bytes, plans and approvals are retained.
Checkouts/installed projects stay local, not published as embedded Git repositories.
No source fix or helper workaround, no working settings/hooks/DB, no merge/release/finalizer.
This is scoped native Windows QA, not whole-release acceptance. Exact-HEAD CI statuses
are captured separately; full source verifier was not repeated by Windows QA.
'''.format(source=PIN,fingerprint=fingerprint)
(R/'REPORT.md').write_text(report,encoding='utf-8')
print(json.dumps(dict(result='PASS scoped',source=PIN,content_fingerprint=fingerprint,installer_upgrades=len(installed['upgrades']))))
