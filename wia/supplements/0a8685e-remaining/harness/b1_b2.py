from qa_common import *
import re
data=R/'b1-b2-data.json'
run('b1-b2-build-data',['node',B/'b1_b2_data.mjs',E/'lifecycle-complete.json',data])
cases=json.loads(data.read_text(encoding='utf-8'))
for case in cases['cases']:
 name='b1-'+case['name']
 refusal=git(name+'-actual-prepush',['push','origin',case['candidate']+':refs/heads/beads-backup'],expected=(1,))
 check(name+'-guard-cause',bool(re.search(r'snapshot|outcome|postcondition|preserv',decode(refusal.stderr),re.I)),decode(refusal.stderr))
 peer=B/'isolated-reader';ref='refs/qa/'+case['name']
 git(name+'-fetch-data',['fetch',PUBLISHER,'refs/heads/qa/'+case['name']+':'+ref],peer)
 refusal=bash(name+'-peer-reader',['scripts/bd-read.sh','list','--json'],peer,expected=(2,),env=dict(ENV,BD_READ_REF=ref))
 check(name+'-peer-no-state',not refusal.stdout and bool(re.search(r'snapshot|outcome|postcondition|preserv',decode(refusal.stderr),re.I)),decode(refusal.stderr))
 check(name+'-origin-unchanged',text(git(name+'-origin',['ls-remote','--heads','origin','beads-backup'])).split()[0]==case['base'],case['base'])
save('b1-result',dict(result='PASS',source=PIN,cases=cases['cases'],guard='actual registered pre-push',peer='isolated bd-read.sh on custom data ref',origin_unchanged=True))
save('b2-result',cases['B2'])
print('B1 guard+reader task-loss/rewrite PASS; B2 canonical-empty/malformed parser PASS')
