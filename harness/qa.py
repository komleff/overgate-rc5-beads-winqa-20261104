import os,sys,json,subprocess,hashlib,time
from pathlib import Path
B=Path(__file__).resolve().parent;E=B/'evidence';E.mkdir(exist_ok=True)
BD=Path('D:/CodexArtifacts/overgate-rc4-winqa-20261103/tools/bd.exe')
env=os.environ.copy()
# New child processes use embedded local stores; never inherit database redirects.
redirects=[k for k in env if k.startswith(('BEADS_','BD_'))]
for k in redirects:env.pop(k,None)
env['PYTHONUTF8']='1'
def write(name,data):
    p=E/name
    if isinstance(data,(dict,list)):data=json.dumps(data,ensure_ascii=False,indent=2)
    p.write_text(data,encoding='utf-8',newline='\n');return p
def run(args,cwd=B,label=None,input=None):
    argv=[str(x) for x in args];start=time.time()
    p=subprocess.run(argv,cwd=cwd,env=env,input=input,capture_output=True,text=True,encoding='utf-8',errors='replace')
    r={'command':argv,'cwd':str(cwd),'exit_code':p.returncode,'duration_seconds':round(time.time()-start,3),'stdout':p.stdout,'stderr':p.stderr}
    if label:write(label+'.json',r)
    if p.returncode:
        write('STOP.json',{'label':label,**r});print(json.dumps({'STOP':label,**r},ensure_ascii=True),flush=True);raise SystemExit(p.returncode)
    return p.stdout
def bd(args,root,label):return run([BD,'--sandbox',*args],root,label)
def new(root,prefix,label):
    assert not root.exists(), 'Root must be new: '+str(root)
    root.mkdir(parents=True)
    run(['git','init','-b','main'],root,label+'-git-init')
    (root/'README.md').write_text('Disposable Windows bd1.2.2 CLI qualification. No real project tasks.\n',encoding='utf-8',newline='\n')
    run(['git','add','README.md'],root,label+'-git-add')
    run(['git','commit','-m','test: initialize disposable Beads CLI project'],root,label+'-git-commit')
    assert not run(['git','remote'],root,label+'-no-remotes').strip()
    bd(['init','--prefix',prefix,'--skip-agents','--skip-hooks','--non-interactive','--remote',''],root,label+'-bd-init')
    meta=json.loads((root/'.beads/metadata.json').read_text(encoding='utf-8'))
    assert meta['dolt_mode']=='embedded'
    write(label+'-metadata.json',meta)
    write(label+'-config.yaml',(root/'.beads/config.yaml').read_text(encoding='utf-8'))
    return root
def help_all():
    write('binary.json',{'absolute_path':str(BD),'sha256':hashlib.sha256(BD.read_bytes()).hexdigest(),'version':run([BD,'--version'],label='bd-version').strip(),'removed_database_redirect_names':redirects,'qualification':'Native Windows CLI capability only; no publisher/source/release qualification'})
    for name,args in [('init',['init']),('create',['create']),('update',['update']),('close',['close']),('comments-add',['comments','add']),('comments',['comments']),('dep-add',['dep','add']),('export',['export']),('import',['import']),('show',['show']),('list',['list']),('config',['config']),('config-list',['config','list'])]:
        bd([*args,'--help'],B,'help-'+name)
    print('HELP PASS',flush=True)
def prefix():
    root=new(B/'big-heroes','big-heroes','prefix')
    issue=json.loads(bd(['create','--title','Windows prefix probe','--type','task','--description','Synthetic CLI prequalification only','--json'],root,'prefix-create'))
    iid=issue['id'];show=json.loads(bd(['show',iid,'--json'],root,'prefix-show'))
    configs=bd(['config','list','--json'],root,'prefix-config-list')
    result={'root':str(root),'requested_prefix':'big-heroes','created_id':iid,'metadata':json.loads((root/'.beads/metadata.json').read_text(encoding='utf-8')),'config_yaml':(root/'.beads/config.yaml').read_text(encoding='utf-8'),'config_list':json.loads(configs),'show':show,'result':'PASS' if iid.startswith('big-heroes-') else 'FAIL'}
    write('prefix-result.json',result);print(json.dumps(result,ensure_ascii=True),flush=True)
    if result['result']!='PASS':raise SystemExit(1)
if __name__=='__main__':{'help':help_all,'prefix':prefix}[sys.argv[1]]()
