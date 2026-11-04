from qa_common import *
import shutil
receipt=json.loads((E/'create-claim-receipt.json').read_text(encoding='utf-8'))
pair=json.loads((E/'create-claim-peer-full-object.json').read_text(encoding='utf-8'))['details']
row=pair['publisher']
raw=[json.loads(x) for x in (R/'queues/create-claim.raw.jsonl').read_text(encoding='utf-8').splitlines()]
create=raw[0]
aliases={'type':'issue_type','acceptance':'acceptance_criteria'}
fields={}
for k,v in create.items():
 if k in ['intent_id','op','handle']:continue
 key=aliases.get(k,k)
 fields[key]=dict(expected=v,actual=row.get(key),result='PASS' if (set(v)==set(row.get(key,[])) if key=='labels' else v==row.get(key)) else 'FAIL')
save('recorded-byte-field-comparison',dict(method='read-only postprocessing of existing captured publication/peer bytes; no candidate rerun',labels_semantics='unordered distinct set',fields=fields,result='PASS' if all(x['result']=='PASS' for x in fields.values()) else 'FAIL'))
save('qa-assertion-classifications',[
 dict(receipt='source-to-local-main.json',kind='QA fixture transport error',reason='shallow Git transfer; fixed by complete ancestry fetch before candidate execution'),
 dict(receipt='publisher-legacy-absent-pre.json',kind='QA overstrict preflight assertion',reason='tracked reference metadata mistaken for existing database; actual store absent'),
 dict(receipt='primary-still-exact-pin.json',kind='QA fixture binding assertion',reason='native bd init makes project-state commit; newer RUN requires candidate-byte equivalence + trusted fixture main; both established before setup'),
 dict(receipt='create-field-labels.json',kind='QA ordered-array comparison error',reason='labels set contents identical; original false FAIL preserved; postprocessing only existing bytes confirms semantic equality')])
refs={}
for name,root in [('primary',PRIMARY),('publisher',PUBLISHER),('linked',LINKED)]:
 refs[name]=dict(path=str(root),head=text(git('checkpoint-'+name+'-head',['rev-parse','HEAD'],root)),
   refs=text(git('checkpoint-'+name+'-refs',['show-ref'],root)),status=text(git('checkpoint-'+name+'-status',['status','--porcelain'],root)),
   index_sha256=sha(git('checkpoint-'+name+'-index',['ls-files','-s','-z'],root).stdout))
refs['bare']=text(git('checkpoint-origin-refs',['ls-remote','origin']))
save('checkpoint-refs',refs)
git('checkpoint-ledger',['show',receipt['published_sha']+':.beads/overgate-ledger.json'],expected=(0,128))
control=PUBLISHER/'.git/overgate-bd-managed'
if not (R/'preserved-managed-control').exists():shutil.copytree(control,R/'preserved-managed-control')
contract=(R/'pr-contract.txt').read_bytes()
fp=json.loads((E/'source-fingerprint.json').read_text())
save('checkpoint-source-contract',dict(source=PIN,target=refs['publisher']['head'],source_fingerprint=fp['sha256'],contract_sha256=sha(contract),contract_bytes=len(contract),
 plan_blob=text(git('checkpoint-plan-blob',['rev-parse',PIN+':docs/plans/2026-11-03-v4.0.0-rc.5-beads.md'])),
 scripts_tree=text(git('checkpoint-scripts-tree',['rev-parse',PIN+':scripts'])),
 combined_fingerprint=sha((fp['sha256']+'\n'+sha(contract)+'\n').encode())))
save('checkpoint-result',dict(result='NOT RUN for WI-A acceptance — PM HOLD',source=PIN,target=refs['publisher']['head'],
 pass_scoped=['binary identity','trusted fixture candidate bytes','setup','verified-absent bootstrap','native create/claim','claims.confirmed','peer full-object same-SHA read-back','recorded field values'],
 not_run=['update/close','linked/isolated managed routes','B1/B2/B3 address negatives','AC3/AC4 race/retry','Linux/macOS/whole-release'],
 issue_id=row['id'],published_sha=receipt['published_sha'],mutations=receipt['mutations'],stop_reason='PM HOLD 6639435396 arrived through active five-minute monitor; no further product operations'))
print(json.dumps(dict(checkpoint='saved',source=PIN,id=row['id'],published_sha=receipt['published_sha'],fields={k:v['result'] for k,v in fields.items()})))
