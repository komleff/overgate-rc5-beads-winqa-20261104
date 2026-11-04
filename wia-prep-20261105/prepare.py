import os,sys,json,hashlib,subprocess,uuid
from pathlib import Path
B=Path(__file__).resolve().parent;E=B/'evidence';E.mkdir(exist_ok=True)
BD=Path('D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe')
def run(args,cwd=B,label=None):
    p=subprocess.run([str(x) for x in args],cwd=cwd,capture_output=True)
    stdout=p.stdout.decode('utf-8',errors='replace');stderr=p.stderr.decode('utf-8',errors='replace')
    if label:
        (E/(label+'.stdout.bin')).write_bytes(p.stdout);(E/(label+'.stderr.bin')).write_bytes(p.stderr)
        (E/(label+'.json')).write_text(json.dumps({'argv':[str(x) for x in args],'cwd':str(cwd),'exit_code':p.returncode,'stdout':stdout,'stderr':stderr},ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
    if p.returncode:raise RuntimeError(stdout+stderr)
    return stdout.strip()
def info(root):
    assert not run(['git','status','--porcelain'],root)
    index=Path(run(['git','rev-parse','--path-format=absolute','--git-path','index'],root))
    return {'path':str(root),'head':run(['git','rev-parse','HEAD'],root),'branch':run(['git','branch','--show-current'],root),'index_sha256':hashlib.sha256(index.read_bytes()).hexdigest(),'git_dir':run(['git','rev-parse','--absolute-git-dir'],root),'common_dir':run(['git','rev-parse','--path-format=absolute','--git-common-dir'],root),'beads_absent':not(root/'.beads').exists(),'clean':True}
def main():
    origin=B/'origin.git';seed=B/'seed'
    assert not origin.exists() and not seed.exists(),'Do not duplicate workspace preparation'
    run(['git','init','--bare','--initial-branch=qa/preparation',origin],label='origin-init')
    seed.mkdir();run(['git','init','--initial-branch=qa/preparation'],seed,label='seed-init')
    run(['git','config','user.name','Windows QA fixture'],seed);run(['git','config','user.email','windows-qa@example.invalid'],seed)
    (seed/'README.md').write_text('Neutral disposable WI-A Windows QA preparation. No candidate code or Beads state.\n',encoding='utf-8',newline='\n')
    (seed/'.gitattributes').write_text('*.sh text eol=lf\n',encoding='utf-8',newline='\n')
    run(['git','add','.'],seed);run(['git','commit','-m','test: neutral WI-A Windows preparation'],seed,label='seed-commit')
    run(['git','remote','add','origin',origin],seed);run(['git','push','origin','qa/preparation'],seed,label='seed-push')
    actors=[]
    for tag in ['a','b']:
        root=B/('actor-'+tag);run(['git','clone','-c','core.autocrlf=false','--no-hardlinks',origin,root],label='clone-'+tag)
        run(['git','config','user.name','Windows QA actor '+tag],root);run(['git','config','user.email','qa-'+tag+'@example.invalid'],root)
        actors.append({'actor_id':'agent-'+str(uuid.uuid4()),**info(root)})
    linked=B/'linked';run(['git','worktree','add','-b','qa/linked',linked,'qa/preparation'],B/'actor-a',label='linked-worktree-add')
    linked_info=info(linked);assert linked_info['common_dir']==actors[0]['common_dir']
    isolated=B/'isolated-reader';isolated.mkdir()
    route={'mode':'read-and-queue preparation only','origin':str(origin),'publisher_path_candidate':str(B/'actor-a'),'publisher_registered':False,'source_pin':None,'snapshot_sha':None,'pending_queue_path':str(isolated/'queue.raw.jsonl')}
    (isolated/'route.json').write_text(json.dumps(route,indent=2),encoding='utf-8',newline='\n')
    tools={'bd':{'path':str(BD),'version':run([BD,'--version'],label='bd-version'),'sha256':hashlib.sha256(BD.read_bytes()).hexdigest()},'git':run(['git','--version'],label='git-version'),'bash':run(['C:/Program Files/Git/bin/bash.exe','--version'],label='bash-version').splitlines()[0],'python':run([sys.executable,'--version'],label='python-version'),'node':run(['node','--version'],label='node-version')}
    assert tools['bd']['version']=='bd version 1.2.2 (6c124203e)' and tools['bd']['sha256']=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de'
    refs=run(['git','show-ref'],origin,label='origin-baseline-refs')
    assert not run(['git','ls-remote','--heads','origin','main','beads-backup'],B/'actor-a',label='no-main-or-backup').strip()
    result={'status':'NEUTRAL PREP READY; f11a6b5 HOLD; runtime NOT RUN','root':str(B),'origin':str(origin),'origin_refs':refs,'actors':actors,'linked':linked_info,'isolated_reader':route,'tools':tools,'candidate_code_installed':False,'trusted_main_established':False,'publisher_setup_run':False,'beads_or_snapshot_created':False,'working_project_db_used':False}
    (E/'workspace-ready.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n');print(json.dumps(result,ensure_ascii=True))
if __name__=='__main__':main()
