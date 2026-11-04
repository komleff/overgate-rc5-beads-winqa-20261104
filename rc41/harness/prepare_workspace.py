import os,sys,subprocess,json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;E=B/'evidence';E.mkdir(exist_ok=True)
BD=Path('D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe')
def run(args,cwd=B,label=None):
    p=subprocess.run([str(x) for x in args],cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if label:(E/(label+'.json')).write_text(json.dumps({'argv':[str(x) for x in args],'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr},ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
    if p.returncode:raise RuntimeError(str(args)+'\n'+p.stdout+p.stderr)
    return p.stdout.strip()
def main():
    prep=B/'prepared';assert not prep.exists(),'Prepared workspace already exists; do not duplicate'
    prep.mkdir();origin=prep/'origin.git';seed=prep/'seed'
    run(['git','init','--bare','--initial-branch=qa/windows',origin],label='prep-origin-init')
    seed.mkdir();run(['git','init','--initial-branch=qa/windows'],seed,label='prep-seed-init')
    run(['git','config','user.name','Windows QA fixture'],seed);run(['git','config','user.email','windows-qa@example.invalid'],seed)
    (seed/'README.md').write_text('RC4.1 disposable Windows QA baseline. No Beads database or candidate installed.\n',encoding='utf-8',newline='\n')
    (seed/'.gitattributes').write_text('*.sh text eol=lf\n',encoding='utf-8',newline='\n')
    run(['git','add','README.md','.gitattributes'],seed);run(['git','commit','-m','test: baseline isolated Windows QA workspace'],seed,label='prep-seed-commit')
    run(['git','remote','add','origin',origin],seed);run(['git','push','origin','qa/windows'],seed,label='prep-seed-push')
    clones=[]
    for name in ['primary','peer']:
        root=prep/name;run(['git','clone','-c','core.autocrlf=false','--no-hardlinks',origin,root],label='prep-clone-'+name)
        run(['git','config','user.name','Windows QA fixture'],root);run(['git','config','user.email','windows-qa@example.invalid'],root)
        head=run(['git','rev-parse','HEAD'],root);assert not run(['git','status','--porcelain'],root)
        index=(root/'.git/index').read_bytes();(E/(name+'-baseline-index.bin')).write_bytes(index)
        assert not(root/'.beads').exists()
        clones.append({'path':str(root),'head':head,'index_sha256':hashlib.sha256(index).hexdigest(),'clean':True,'beads_absent':True,'origin':run(['git','remote','get-url','origin'],root)})
    for name in ['empty','populated']:(B/'cases'/name).mkdir(parents=True)
    tools={'bd':{'path':str(BD),'sha256':hashlib.sha256(BD.read_bytes()).hexdigest(),'version':run([BD,'--version'],label='prep-bd-version')},'git':run(['git','--version'],label='prep-git-version'),'bash':run(['C:/Program Files/Git/bin/bash.exe','--version'],label='prep-bash-version').splitlines()[0],'python':run([sys.executable,'--version'],label='prep-python-version'),'codex':run(['powershell.exe','-NoProfile','-Command','codex --version'],label='prep-codex-version')}
    assert tools['bd']['version']=='bd version 1.2.2 (6c124203e)'
    refs=run(['git','show-ref'],origin,label='prep-origin-refs')
    r={'status':'READY FOR NEW PIN; candidate runtime NOT RUN','pm_packet':6633775710,'hold_source':'e4a737dc79e079a49b69c97fd0274d88eb40f700','workspace':str(B),'bare_origin':str(origin),'baseline_origin_refs':refs,'clones':clones,'future_case_paths':{'empty':str(B/'cases/empty'),'populated':str(B/'cases/populated')},'tools':tools,'candidate_bootstrap_or_restore_run':False,'beads_snapshot_created':False,'working_databases_used':False}
    (E/'workspace-ready.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
    print(json.dumps(r,ensure_ascii=True))
if __name__=='__main__':main()
