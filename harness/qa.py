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
def equal(label,expected,actual):
    if json.dumps(expected,sort_keys=True,ensure_ascii=False)!=json.dumps(actual,sort_keys=True,ensure_ascii=False):
        failure={'label':label,'expected':expected,'actual':actual,'result':'FAIL'}
        write('STOP.json',failure);print(json.dumps(failure,ensure_ascii=True),flush=True);raise SystemExit(1)
def run(args,cwd=B,label=None,input=None):
    argv=[str(x) for x in args];start=time.time()
    p=subprocess.run(argv,cwd=cwd,env=env,input=input,capture_output=True,text=True,encoding='utf-8',errors='replace')
    r={'command':argv,'cwd':str(cwd),'exit_code':p.returncode,'duration_seconds':round(time.time()-start,3),'stdout':p.stdout,'stderr':p.stderr}
    if label:write(label+'.json',r)
    if p.returncode:
        write('STOP.json',{'label':label,**r});print(json.dumps({'STOP':label,**r},ensure_ascii=True),flush=True);raise SystemExit(p.returncode)
    return p.stdout
def bd(args,root,label):return run([BD,'--sandbox',*args],root,label)
def new(root,prefix,label,json_init=False):
    assert not root.exists(), 'Root must be new: '+str(root)
    root.mkdir(parents=True)
    run(['git','init','-b','main'],root,label+'-git-init')
    (root/'README.md').write_text('Disposable Windows bd1.2.2 CLI qualification. No real project tasks.\n',encoding='utf-8',newline='\n')
    run(['git','add','README.md'],root,label+'-git-add')
    run(['git','commit','-m','test: initialize disposable Beads CLI project'],root,label+'-git-commit')
    assert not run(['git','remote'],root,label+'-no-remotes').strip()
    bd(['init','--prefix',prefix,'--skip-agents','--skip-hooks','--non-interactive','--remote','']+(['--json'] if json_init else []),root,label+'-bd-init')
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
def source_seed():
    root=new(B/'qa-source','qa','source',json_init=True)
    parent=json.loads(bd(['--actor','windows-qa','create','--title','Native round-trip parent','--type','epic','--description','Synthetic parent; no real project tasks','--json'],root,'source-create-parent'))
    peer=json.loads(bd(['--actor','windows-qa','create','--title','Native typed-edge peer','--type','task','--description','Synthetic dependency target','--json'],root,'source-create-peer'))
    metadata={'qa':{'platform':'windows','unicode':'проверка','revision':1},'enabled':True,'count':3,'items':['alpha','beta']}
    wanted={'title':'Native round-trip child','description':'Описание synthetic\nSecond line','design':'Дизайн v1\nNo project source','acceptance_criteria':'AC5/AC9 synthetic\nRound-trip fields and edges','notes':'Заметки v1','labels':['qa-native','roundtrip'],'metadata':metadata}
    child=json.loads(bd(['--actor','windows-qa','create','--parent',parent['id'],'--title',wanted['title'],'--type','task','--priority','2','--description',wanted['description'],'--design',wanted['design'],'--acceptance',wanted['acceptance_criteria'],'--notes',wanted['notes'],'--labels',','.join(wanted['labels']),'--metadata',json.dumps(metadata,ensure_ascii=False),'--json'],root,'source-create-child'))
    assert child['id'].startswith(parent['id']+'.'), 'Native --parent did not produce nested ID'
    result={'source_root':str(root),'parent_id':parent['id'],'peer_id':peer['id'],'child_id':child['id'],'wanted_initial_child':wanted,'child_show':json.loads(bd(['show',child['id'],'--json'],root,'source-child-initial-show'))}
    write('source-seed.json',result);print(json.dumps(result,ensure_ascii=True),flush=True)
def source_finish():
    seed=json.loads((E/'source-seed.json').read_text(encoding='utf-8'));root=Path(seed['source_root']);iid=seed['child_id']
    initial=seed['child_show'][0]
    for field,expected in seed['wanted_initial_child'].items():equal('source-initial-'+field,expected,initial.get(field))
    bd(['--actor','windows-qa','update',iid,'--claim','--json'],root,'source-claim')
    claimed=json.loads(bd(['show',iid,'--json'],root,'source-show-claimed'))[0]
    equal('claim-status','in_progress',claimed.get('status'));equal('claim-assignee','windows-qa',claimed.get('assignee'))
    updated={'title':'Native round-trip child updated','description':'Описание updated\nSecond line retained','design':'Дизайн updated\nNative Windows','acceptance_criteria':'AC5/AC9 updated\nCheck all fields','notes':'Заметки updated\nFinal note','metadata':{'qa':{'platform':'windows','unicode':'проверка','revision':2},'enabled':True,'count':3,'items':['alpha','beta'],'updated':True}}
    bd(['--actor','windows-qa','update',iid,'--title',updated['title'],'--description',updated['description'],'--design',updated['design'],'--acceptance',updated['acceptance_criteria'],'--notes',updated['notes'],'--metadata',json.dumps(updated['metadata'],ensure_ascii=False),'--json'],root,'source-update')
    check=json.loads(bd(['show',iid,'--json'],root,'source-show-updated'))[0]
    for field,expected in updated.items():equal('source-updated-'+field,expected,check.get(field))
    comment='Native round-trip comment: комментарий\nSecond comment line'
    bd(['--actor','windows-qa','comments','add',iid,comment,'--json'],root,'source-comment-add')
    bd(['--actor','windows-qa','dep','add',iid,seed['peer_id'],'--type','discovered-from','--json'],root,'source-dep-add')
    bd(['--actor','windows-qa','close',iid,'--reason','Synthetic Windows CLI qualification complete','--json'],root,'source-close')
    shows={}
    for key in ['parent_id','peer_id','child_id']:shows[seed[key]]=json.loads(bd(['show',seed[key],'--json'],root,'source-final-show-'+key))[0]
    child=shows[iid];equal('source-final-status','closed',child.get('status'))
    for field,expected in updated.items():equal('source-final-'+field,expected,child.get(field))
    equal('source-final-labels',seed['wanted_initial_child']['labels'],child.get('labels'))
    edges=sorted((d['id'],d.get('dependency_type')) for d in child.get('dependencies',[]))
    equal('source-typed-edges',sorted([(seed['parent_id'],'parent-child'),(seed['peer_id'],'discovered-from')]),edges)
    comments=json.loads(bd(['comments',iid,'--json'],root,'source-final-comments'))
    equal('source-comment-text',comment,comments[0].get('text'))
    listing=json.loads(bd(['list','--all','--json'],root,'source-final-list'))
    export=E/'native-export.jsonl';bd(['export','--all','--output',export],root,'source-export')
    result={'source_root':str(root),'ids':[seed['parent_id'],seed['peer_id'],iid],'shows':shows,'comments':comments,'list':listing,'export_path':str(export),'export_sha256':hashlib.sha256(export.read_bytes()).hexdigest(),'expected_updated':updated,'expected_comment':comment,'result':'PASS'}
    write('source-complete.json',result);print(json.dumps({'ids':result['ids'],'child':child,'comments':comments,'export_sha256':result['export_sha256'],'result':'PASS'},ensure_ascii=True),flush=True)
def norm(value):
    if isinstance(value,dict):return {k:sorted((norm(x) for x in v),key=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False)) if isinstance(v,list) and k in {'labels','dependencies','dependents'} else norm(v) for k,v in value.items()}
    if isinstance(value,list):return [norm(x) for x in value]
    return value
def target():
    source=json.loads((E/'source-complete.json').read_text(encoding='utf-8'))
    root=new(B/'qa-target','qa','target',json_init=True)
    imported=json.loads(bd(['import',source['export_path'],'--json'],root,'target-import'))
    write('target-import-structured.json',imported)
    result={'source_root':source['source_root'],'target_root':str(root),'ids':source['ids'],'shows':{},'compared_fields':{},'result':'PASS'}
    # Compare each real readback immediately, and stop at the first difference.
    for iid in [source['ids'][2],*source['ids'][:2]]:
        actual=json.loads(bd(['show',iid,'--json'],root,'target-show-'+iid))[0]
        result['shows'][iid]=actual;write('roundtrip-result.json',result)
        expected=source['shows'][iid]
        for field in sorted(set(expected)|set(actual)):
            equal('roundtrip-'+iid+'-'+field,norm({field:expected.get(field)}),norm({field:actual.get(field)}))
        result['compared_fields'][iid]=sorted(expected)
    actual_comments=json.loads(bd(['comments',source['ids'][2],'--json'],root,'target-comments'))
    result['comments']=actual_comments;write('roundtrip-result.json',result)
    equal('roundtrip-comments',source['comments'],actual_comments)
    actual_list=json.loads(bd(['list','--all','--json'],root,'target-list'))
    result['list']=actual_list
    equal('roundtrip-list',{x['id']:norm(x) for x in source['list']},{x['id']:norm(x) for x in actual_list})
    for name in ['qa-source','qa-target']:
        p=B/name;equal(name+'-no-git-remote','',run(['git','remote'],p,name+'-final-remotes').strip())
        result[name+'_git_head']=run(['git','rev-parse','HEAD'],p,name+'-final-head').strip()
    write('roundtrip-result.json',result)
    print(json.dumps({'result':'PASS','ids':result['ids'],'all_show_fields_equal':True,'comments_equal':True,'list_equal':True,'source_root':result['source_root'],'target_root':result['target_root']},ensure_ascii=True),flush=True)
if __name__=='__main__':{'help':help_all,'prefix':prefix,'source-seed':source_seed,'source-finish':source_finish,'target':target}[sys.argv[1]]()
