"""Neutral WI-C Windows fixture preparation; released rc.4.1 bytes only.
No PR16 implementation, recovery payloads, model calls or project state.
"""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, time

B = Path(__file__).resolve().parent
E = B / 'evidence'
E.mkdir(exist_ok=True)
BASE = '3f3246c3a3b62377fc02aad05283cae1ef5d4e2d'
SRC = B / 'released-source'
BASH = r'C:\Program Files\Git\bin\bash.exe'
CLAUDE = r'C:\Users\komle\AppData\Roaming\npm\claude.cmd'
ENV = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
           PATH=r'C:\Program Files\Git\bin;C:\Program Files\Git\usr\bin;' + os.environ['PATH'])
for key in ['GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE', 'CLAUDE_PROJECT_DIR',
            'OVERGATE_COMMIT_GATE_TEST_MAX_SECONDS']:
    ENV.pop(key, None)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def run(label, argv, cwd=B, data=None, expected=0, timeout=90):
    started = time.time()
    p = subprocess.run(list(map(str, argv)), cwd=cwd, env=ENV, input=data,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    (E / (label + '.stdout.bin')).write_bytes(p.stdout)
    (E / (label + '.stderr.bin')).write_bytes(p.stderr)
    receipt = dict(label=label, argv=list(map(str, argv)), cwd=str(cwd), exit_code=p.returncode,
                   expected_exit=expected, seconds=round(time.time()-started, 3),
                   stdout_sha256=sha(p.stdout), stderr_sha256=sha(p.stderr),
                   stdout=p.stdout.decode('utf-8', 'replace'), stderr=p.stderr.decode('utf-8', 'replace'))
    (E / (label + '.json')).write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    assert p.returncode == expected, (label, p.returncode, receipt['stderr'])
    return p.stdout.decode('utf-8').strip()

assert not SRC.exists(), 'Do not overwrite/retry an existing fixture'
run('source-init', ['git', 'init', '--initial-branch=qa/baseline', SRC])
run('source-fetch-released', ['git', '-C', SRC, 'fetch', '--depth=1', 'https://github.com/komleff/overgate.git', BASE])
run('source-checkout', ['git', '-C', SRC, '-c', 'core.autocrlf=false', 'checkout', '--detach', BASE])
assert run('source-head', ['git', '-C', SRC, 'rev-parse', 'HEAD']) == BASE

settings = (SRC / '.claude/settings.json').read_bytes()
entries = [hook for item in json.loads(settings)['hooks']['PreToolUse']
           if item.get('matcher') == 'Bash' for hook in item['hooks']]
assert len(entries) == 1 and entries[0]['timeout'] == 600
entry = entries[0]['command']
assert '\\' not in entry
roots = {}
for label, name in [('ascii','project-ascii'), ('space','project with space'),
                    ('cyrillic','проект-кириллица'), ('parentheses','project(parens)'),
                    ('second','second-dispatcher')]:
    root = B / name
    assert not root.exists(), root
    run(label+'-git-init', ['git','init','--initial-branch=qa/preparation',root])
    for sub in ['hooks','tools']:
        shutil.copytree(SRC / '.claude' / sub, root / '.claude' / sub,
                        ignore=shutil.ignore_patterns('__pycache__','node_modules'))
    (root / '.claude/settings.json').write_bytes(settings)
    (root / 'own-subdir').mkdir()
    (root / 'README.md').write_text('Disposable Windows WI-C baseline hook fixture.\n', encoding='utf-8')
    run(label+'-add', ['git','-C',root,'-c','core.autocrlf=false','add','--','.claude','README.md'])
    run(label+'-commit', ['git','-C',root,'-c','user.name=Windows QA','-c','user.email=qa@example.invalid',
                         '-c','commit.gpgsign=false','commit','-m','fixture: released rc.4.1 hook bytes'])
    roots[label] = dict(path=str(root), head=run(label+'-head',['git','-C',root,'rev-parse','HEAD']),
                       settings_sha256=sha(settings), dispatcher_sha256=sha((root/'.claude/hooks/pre-bash.sh').read_bytes()))

outside = B / 'outside-no-git'
outside.mkdir()
probes = []
for label, info in roots.items():
    root = Path(info['path'])
    for kind,cwd,expected in [('root',root,0),('own-subdir',root/'own-subdir',2)]:
        payload = json.dumps(dict(tool_name='Bash',tool_input=dict(command='git status --short'),cwd=str(cwd)),ensure_ascii=False).encode('utf-8')
        name = label+'-'+kind+'-invocation-only'
        (E/(name+'.payload.json')).write_bytes(payload)
        run(name,[BASH,'-c',entry],cwd,payload,expected,timeout=60)
        probes.append(dict(name=name,cwd=str(cwd),result='PASS scoped invocation',exit_code=expected))
payload = json.dumps(dict(tool_name='Bash',tool_input=dict(command='git status --short'),cwd=str(outside))).encode('utf-8')
(E/'outside-invocation-only.payload.json').write_bytes(payload)
run('outside-invocation-only',[BASH,'-c',entry],outside,payload,2,timeout=30)
probes.append(dict(name='outside-invocation-only',cwd=str(outside),result='PASS scoped invocation',exit_code=2))

tools = dict(git=run('git-version',['git','--version']),
             bash=dict(path=BASH,version=run('bash-version',[BASH,'--version']).splitlines()[0]),
             python=dict(path=sys.executable,version=sys.version.split()[0],
                         from_git_bash=run('bash-python',[BASH,'-c','python -c "import sys; print(sys.executable); print(sys.version.split()[0])"'])),
             claude=dict(path=CLAUDE,version=run('claude-version',['cmd.exe','/d','/c',CLAUDE,'--version'])))
manifest = dict(status='PREP READY; no WI-C acceptance',baseline_source_sha=BASE,
                pr16_implementation_installed=False,working_settings_hooks_changed=False,
                fixture_type='Neutral Git roots populated with exact released hooks/tools/settings bytes; installer acceptance NOT RUN',
                roots=roots,outside=str(outside),entry_count=len(entries),entry_timeout=entries[0]['timeout'],
                probes=probes,tools=tools,
                simple_path_baseline='Read released entry grammar only; no cd recovery payload executed',
                recovery_cases='NOT RUN until exact implementation SHA packet',
                live_claude_model_call='NOT RUN; CLI version only')
(E/'prep-ready.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
