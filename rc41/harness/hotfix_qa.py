"""Disposable native Windows QA harness. No candidate is selected by this module."""
import os,sys,json,hashlib,subprocess,time,re,traceback
from pathlib import Path
B=Path(__file__).resolve().parent;E=B/'evidence'
BD=Path('D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe')
BASH='C:/Program Files/Git/bin/bash.exe'
FILES=('scripts/bd-bootstrap.sh','scripts/bd-sync-common.sh','scripts/bd-sync-export.sh','scripts/bd-sync-restore.sh','scripts/lib/bd-env.sh','.claude/tools/run-python.sh','.agents/distribution-manifest.json')
BASE=os.environ.copy()
for key in list(BASE):
    if key.startswith(('BEADS_','BD_')) or key in {'GIT_INDEX_FILE','GIT_WORK_TREE','GIT_DIR'}:BASE.pop(key,None)
BASE['PATH']=str(BD.parent)+';C:/Program Files/Git/bin;C:/Program Files/Git/usr/bin;'+BASE['PATH']
BASE['PYTHONUTF8']='1'
def save(name,value):
    p=E/(name+'.json');p.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n');return p
def run(args,cwd=B,label=None,extra=None,expected_zero=True,input=None):
    env=dict(BASE,**(extra or {}));started=time.time()
    p=subprocess.run([str(x) for x in args],cwd=cwd,env=env,input=input.encode('utf-8') if isinstance(input,str) else input,capture_output=True)
    rawout,rawerr=p.stdout,p.stderr
    if label:
        (E/(label+'.stdout.bin')).write_bytes(rawout)
        (E/(label+'.stderr.bin')).write_bytes(rawerr)
    def decode(data):
        for encoding in ['utf-8','cp1251']:
            try:return data.decode(encoding),encoding
            except UnicodeDecodeError:pass
        return data.decode('utf-8',errors='replace'),'utf-8 replacement; original bytes retained'
    p.stdout,out_encoding=decode(rawout);p.stderr,err_encoding=decode(rawerr)
    record={'argv':[str(x) for x in args],'cwd':str(cwd),'environment_overrides':extra or {},'exit_code':p.returncode,'duration_seconds':round(time.time()-started,3),'stdout':p.stdout,'stderr':p.stderr,'stdout_encoding':out_encoding,'stderr_encoding':err_encoding,'stdout_raw_sha256':hashlib.sha256(rawout).hexdigest(),'stderr_raw_sha256':hashlib.sha256(rawerr).hexdigest()}
    if label:save(label,record)
    if expected_zero and p.returncode:raise RuntimeError(json.dumps(record,ensure_ascii=True))
    return p
def git(root,*args,**kw):return run(['git',*args],root,**kw).stdout.strip()
def bd(root,*args,label=None):return run([BD,'--sandbox',*args],root,label=label).stdout
def source_payload(source,sha,target):
    for name in FILES:
        data=subprocess.run(['git','show',sha+':'+name],cwd=source,capture_output=True,check=True).stdout
        p=target/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
def snapshot(root):
    index=root/'.git/index'
    paths=['README.md','sentinel.txt','.beads/metadata.json','.beads/config.yaml']
    files={name:hashlib.sha256((root/name).read_bytes()).hexdigest() if(root/name).is_file() else None for name in paths}
    return {'head':git(root,'rev-parse','HEAD'),'index_sha256':hashlib.sha256(index.read_bytes()).hexdigest(),'files':files,'origin_refs':git(root,'ls-remote','--heads','origin'),'local_db_exists':(root/'.beads/embeddeddolt').exists() or(root/'.beads/dolt').exists()}
def setup_helpers(root,source,sha,label):
    assert not(root/'.beads').exists()
    source_payload(source,sha,root)
    git(root,'add',*FILES);git(root,'commit','-m','test: frozen helper payload '+label,label=label+'-helpers-commit')
def staged_case(root,source,sha,label,alternate=False):
    setup_helpers(root,source,sha,label)
    extra={}
    if alternate:
        alt=E/(label+'-alternate-index.bin');alt.write_bytes((root/'.git/index').read_bytes());extra['GIT_INDEX_FILE']=str(alt)
    (root/'sentinel.txt').write_bytes(b'Foreign staged project sentinel\n')
    git(root,'add','sentinel.txt')
    before=snapshot(root);save(label+'-before',before)
    alt_before=hashlib.sha256(alt.read_bytes()).hexdigest() if alternate else None
    p=run([BASH,'scripts/bd-bootstrap.sh'],root,label=label+'-bootstrap',extra=extra,expected_zero=False)
    after=snapshot(root);save(label+'-after',after)
    checks={'controlled_stop':p.returncode!=0 and 'STOP:' in p.stderr,'snapshot_unchanged':before==after,'no_local_beads':not(root/'.beads').exists()}
    if alternate:checks['alternate_index_unchanged']=hashlib.sha256(alt.read_bytes()).hexdigest()==alt_before
    r={'case':label,'H':'H1','source_sha':sha,'method':'Actual native Git Bash bootstrap with canonical staged sentinel'+(' and clean GIT_INDEX_FILE override' if alternate else ''),'checks':checks,'result':'PASS' if all(checks.values()) else 'FAIL'}
    save(label+'-result',r);return r

# The coordinator supplies a new PM-approved packet and exact clean source only
# after HOLD is explicitly lifted. Importing this module performs no fixture work.
SHA='825c0b9d9e2ad7fe61182836649008a47a34c0c4'
SOURCE=B/'source-825c0b9'
def fresh_group(name):
    group=B/'cases'/name;group.mkdir(exist_ok=True)
    origin=group/'origin.git';primary=group/'big-heroes'
    assert not origin.exists() and not primary.exists()
    run(['git','init','--bare','--initial-branch=qa/project',origin],label=name+'-origin-init')
    run(['git','clone','-c','core.autocrlf=false',origin,primary],label=name+'-primary-clone')
    git(primary,'config','user.name','Windows QA fixture');git(primary,'config','user.email','windows-qa@example.invalid')
    (primary/'README.md').write_text('Disposable RC4.1 native Windows helper fixture\n',encoding='utf-8',newline='\n')
    (primary/'.gitattributes').write_text('*.sh text eol=lf\n',encoding='utf-8',newline='\n')
    source_payload(SOURCE,SHA,primary)
    git(primary,'add','.');git(primary,'commit','-m','test: frozen RC4.1 helper fixture',label=name+'-payload-commit')
    git(primary,'push','origin','qa/project',label=name+'-payload-push')
    return group,origin,primary
def fail_result(label,H,checks,**data):
    r={'case':label,'H':H,'source_sha':SHA,'checks':checks,**data,'result':'PASS' if all(checks.values()) else 'FAIL'}
    save(label+'-result',r);print(json.dumps(r,ensure_ascii=True),flush=True)
    return r
def empty_case():
    label='H2-empty';group,origin,primary=fresh_group('empty')
    sentinel=b'Untracked project data must stay outside bd init commit\n';(primary/'sentinel.txt').write_bytes(sentinel)
    save(label+'-primary-before',snapshot(primary))
    p=run([BASH,'scripts/bd-bootstrap.sh'],primary,label=label+'-primary-bootstrap',expected_zero=False)
    save(label+'-primary-after',snapshot(primary))
    if p.returncode:return fail_result(label,'H2',{'fresh_bootstrap_exit0':False},stage='primary bootstrap')
    changed=git(primary,'show','--format=','--name-only','HEAD').splitlines()
    prefix=json.loads(bd(primary,'config','get','issue_prefix','--json',label=label+'-effective-prefix'))['value']
    config=(primary/'.beads/config.yaml').read_bytes();metadata=(primary/'.beads/metadata.json').read_bytes()
    checks={'fresh_bootstrap_exit0':True,'beads_only_init_commit':bool(changed) and all(x.startswith('.beads/') or x=='.gitignore' for x in changed),'untracked_sentinel_preserved':(primary/'sentinel.txt').read_bytes()==sentinel and 'sentinel.txt' not in changed,'actual_hyphen_prefix':prefix=='big-heroes','active_pin_written':('issue-prefix: '+json.dumps(prefix)).encode() in config,'pin_requires_project_commit':'.beads/config.yaml' in git(primary,'diff','--name-only')}
    if not all(checks.values()):return fail_result(label,'H2',checks,stage='fresh primary assertions',committed_files=changed)
    git(primary,'add','.beads/config.yaml');git(primary,'commit','-m','project: commit active issue prefix pin',label=label+'-project-pin-commit');git(primary,'push','origin','qa/project',label=label+'-project-pin-push')
    R=git(primary,'ls-remote','origin','refs/heads/beads-backup').split()[0]
    frozen=git(primary,'show',R+':.beads/issues.jsonl');checks['snapshot_empty_before_any_issue']=not frozen
    if not all(checks.values()):return fail_result(label,'H2',checks,stage='freeze empty snapshot')
    clone=group/'peer-empty';run(['git','clone','-c','core.autocrlf=false',origin,clone],label=label+'-peer-clone')
    git(clone,'config','user.name','Windows QA fixture');git(clone,'config','user.email','windows-qa@example.invalid')
    before=snapshot(clone);save(label+'-clone-before',before)
    checks['clone_metadata_pin_tracked']=git(clone,'ls-files','.beads/metadata.json','.beads/config.yaml').splitlines()==['.beads/config.yaml','.beads/metadata.json']
    checks['clone_db_absent_before_restore']=not before['local_db_exists']
    if not all(checks.values()):return fail_result(label,'H2',checks,stage='clone preconditions')
    p=run([BASH,'scripts/bd-bootstrap.sh'],clone,label=label+'-clone-bootstrap',extra={'BD_BOOTSTRAP_EXPECTED_R':R},expected_zero=False)
    after=snapshot(clone);save(label+'-clone-after',after)
    checks['clone_bootstrap_exit0']=p.returncode==0
    checks['clone_db_created']=after['local_db_exists']
    checks['clone_head_index_metadata_config_origin_preserved']={k:v for k,v in before.items() if k!='local_db_exists'}=={k:v for k,v in after.items() if k!='local_db_exists'}
    if p.returncode or not all(checks.values()):return fail_result(label,'H2',checks,stage='empty clone restore',frozen_R=R,primary=str(primary),clone=str(clone))
    export=E/(label+'-restored.jsonl');bd(clone,'export','--all','--output',export,label=label+'-clone-export')
    checks['restored_export_empty']=export.read_bytes()==b''
    checks['lastSeen_frozen_R']=git(clone,'config','--local','--get','beads-sync.lastSeen')==R
    checks['remote_R_unchanged']=git(clone,'ls-remote','origin','refs/heads/beads-backup').split()[0]==R
    checks['no_dolt_remote']=json.loads(bd(clone,'dolt','remote','list','--json',label=label+'-clone-dolt-remotes'))==[]
    checks['exact_effective_prefix']=json.loads(bd(clone,'config','get','issue_prefix','--json',label=label+'-clone-prefix'))['value']==prefix
    checks['metadata_project_id_preserved']=json.loads((clone/'.beads/metadata.json').read_bytes())['project_id']==json.loads(metadata)['project_id']
    return fail_result(label,'H2',checks,frozen_R=R,primary=str(primary),clone=str(clone),committed_files=changed,primary_init_commit=git(primary,'rev-parse','HEAD^'),project_pin_commit=git(primary,'rev-parse','HEAD'))
def main():
    assert git(SOURCE,'rev-parse','HEAD')==SHA and not git(SOURCE,'status','--porcelain')
    assert hashlib.sha256(BD.read_bytes()).hexdigest()=='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de'
    try:
        result={'empty':empty_case}[sys.argv[1]]()
    except Exception as e:
        result={'H':sys.argv[1],'source_sha':SHA,'result':'FAIL','reason':str(e),'traceback':traceback.format_exc()}
        save('STOP',result);print(json.dumps(result,ensure_ascii=True),flush=True);raise SystemExit(1)
    if result['result']!='PASS':save('STOP',result);raise SystemExit(1)
if __name__=='__main__':main()
