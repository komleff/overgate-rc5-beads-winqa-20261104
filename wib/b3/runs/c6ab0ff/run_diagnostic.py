from common import *
root=C/"Проект's (QA) space"/'primary'
before=files(root)
q=run('read-only-encoding-diagnostic',[sys.executable,'-I','-B',R/'read_only_encoding_probe.py',root],root)
assert files(root)==before
save('encoding-diagnostic-root-unchanged',dict(all_target_bytes_equal=True,candidate_replayed=False))
print(q.stdout.decode('utf-8'))
