import json,base64
from pathlib import Path
from hotfix_qa import B,E,run,snapshot,save
root=B/'cases/empty/peer-empty';R='9ab3001ce8979a8d73868d47c47f4d8f721abe19'
before=snapshot(root);save('readonly-comparison-before',before)
commands=[('env','printf \'MSYSTEM=%s\\nPATH=%s\\n\' "${MSYSTEM-}" "$PATH"'),('pwd','pwd'),('git-path','command -v git'),('remote-tip','git rev-parse refs/remotes/origin/beads-backup'),('show-ref','git show origin/beads-backup:.beads/issues.jsonl'),('show-sha','git show '+R+':.beads/issues.jsonl'),('autocrlf','git config --get core.autocrlf')]
results=[]
for name,exe in [('bin','C:/Program Files/Git/bin/bash.exe'),('usr-bin','C:/Program Files/Git/usr/bin/bash.exe')]:
    context={'bash':exe,'environment_method':'Same native initial environment as the outer QA harness; no candidate script sourced','commands':[]}
    for label,command in commands:
        log='readonly-'+name+'-'+label
        p=run([exe,'-c',command],root,label=log,expected_zero=False)
        out=(E/(log+'.stdout.bin')).read_bytes();err=(E/(log+'.stderr.bin')).read_bytes()
        context['commands'].append({'name':label,'command':command,'returncode':p.returncode,'stdout':p.stdout,'stdout_length':len(out),'stderr':p.stderr,'stderr_raw_base64':base64.b64encode(err).decode(),'raw_stdout_file':log+'.stdout.bin','raw_stderr_file':log+'.stderr.bin'})
    results.append(context)
after=snapshot(root);save('readonly-comparison-after',after)
report={'source_sha':'825c0b9d9e2ad7fe61182836649008a47a34c0c4','pm_authorization':[6634342369,6634357455],'root':str(root),'frozen_R':R,'read_only_commands_only':True,'candidate_bootstrap_restore_bd_invoked':False,'before':before,'after':after,'state_unchanged':before==after,'contexts':results}
save('readonly-comparison-result',report)
assert report['state_unchanged']
print(json.dumps(report,ensure_ascii=True))
