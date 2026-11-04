import sys,json,subprocess,shutil,hashlib
from pathlib import Path
from qa import B,E
R=B/'evidence-repo';REPO='komleff/overgate-rc5-beads-winqa-20261104'
def git(args,cwd=R,input=None):
    p=subprocess.run([str(x) for x in args],cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace',input=input)
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
    return p.stdout.strip()
def publish(stage):
    if not R.exists():
        body=json.dumps({'name':REPO.split('/')[1],'description':'Synthetic isolated native Windows bd1.2.2 capability evidence for OverGate rc.5','private':False,'auto_init':True})
        p=subprocess.run(['gh','api','user/repos','--method','POST','--input','-'],input=body,cwd=B,capture_output=True,text=True,encoding='utf-8')
        (E/'publication-repo-create.txt').write_text(p.stdout+'\n'+p.stderr,encoding='utf-8',newline='\n')
        if p.returncode:
            # A failed POST can still create a repository; read before another write.
            q=subprocess.run(['gh','api','repos/'+REPO],cwd=B,capture_output=True,text=True,encoding='utf-8')
            if q.returncode:raise RuntimeError(p.stdout+p.stderr)
        git(['git','clone','https://github.com/'+REPO+'.git',R],B)
        git(['git','switch','-c','qa/evidence'])
    assert not git(['git','status','--porcelain'])
    (R/'receipts').mkdir(exist_ok=True);(R/'harness').mkdir(exist_ok=True)
    for p in E.iterdir():
        if p.is_file() and p.suffix in {'.json','.jsonl','.yaml','.md','.txt'}:shutil.copyfile(p,R/'receipts'/p.name)
    for p in B.glob('*.py'):shutil.copyfile(p,R/'harness'/p.name)
    index={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['receipts','harness'] for p in (R/folder).rglob('*') if p.is_file()}
    (R/'SHA256SUMS.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
    git(['git','add','receipts','harness','SHA256SUMS.json'])
    git(['git','diff','--cached','--check','--','harness'])
    git(['git','commit','-m','docs: '+stage+' Windows Beads native qualification'])
    git(['git','push','-u','origin','qa/evidence'])
    sha=git(['git','rev-parse','HEAD'])
    (E/(stage+'-evidence-sha.txt')).write_text(sha,encoding='utf-8')
    print(json.dumps({'repo':REPO,'stage':stage,'evidence_commit':sha,'indexed_files':len(index)}),flush=True)
if __name__=='__main__':publish(sys.argv[1])
