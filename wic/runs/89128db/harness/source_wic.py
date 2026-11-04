from native_common import *
assert not SRC.exists()
run('source-init',['git','init','--initial-branch=qa/source',SRC])
run('source-fetch',['git','-C',SRC,'fetch','--no-tags','https://github.com/komleff/overgate.git',PIN])
run('source-checkout',['git','-C',SRC,'-c','core.autocrlf=false','checkout','--detach',PIN])
files=decode(run('source-changed-paths',['git','-C',SRC,'diff','--name-only','3f3246c3a3b62377fc02aad05283cae1ef5d4e2d',PIN]).stdout).splitlines()
inventory={p:sha(run('source-blob-'+str(i),['git','-C',SRC,'show',PIN+':'+p]).stdout) for i,p in enumerate(files)}
save('source-fingerprint',dict(source=PIN,files=inventory,sha256=sha(json.dumps(inventory,sort_keys=True,separators=(',',':')).encode())))
print('SOURCE READY '+PIN)
