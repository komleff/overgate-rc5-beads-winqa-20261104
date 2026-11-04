from native_common import *
import sys
p=run('c5-existing-portability-and-mutation',[sys.executable,SRC/'scripts/tests/portability-names.test.py'],SRC,timeout=120)
save('c5-result',dict(result='PASS',source=PIN,method='existing two portability producer/consumer and mutation tests on native Windows Python',stdout=decode(p.stdout),stderr=decode(p.stderr)))
print('C5 existing targeted portability/mutation suite PASS')
