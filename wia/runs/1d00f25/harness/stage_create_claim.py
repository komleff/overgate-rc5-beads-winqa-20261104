from qa_common import *
setup=json.loads((E/'setup-result.json').read_text())
actor=setup['actor']
q=R/'queues'
q.mkdir()
raw=q/'create-claim.raw.jsonl'
prepared=q/'create-claim.v2.jsonl'
fields=dict(title='Windows managed QA — synthetic task',type='bug',priority=2,
 description='Synthetic disposable data only.\nКириллица: сохранение полей.',acceptance='Published ID and claim match peer snapshot.',
 notes='Initial notes\nВторая строка',labels=['windows-qa','synthetic'],external_ref='https://example.invalid/windows-qa',
 due_at='2026-12-01T12:00:00Z',metadata={'suite':'wia','nested':{'text':'Кириллица','enabled':True,'count':3,'items':[1,None,'a']}})
intents=[dict(intent_id='win-create-001',op='create',handle='tmp:task',**fields),dict(intent_id='win-claim-001',op='claim',ref='tmp:task')]
raw.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in intents),encoding='utf-8')
bash('create-claim-prepare',['scripts/bd-apply-intents.sh','--prepare','--base','0'*40,'--actor',actor,'--output',prepared,raw])
receipt=json.loads(bash('create-claim-apply',['scripts/bd-apply-intents.sh',prepared],timeout=240).stdout)
save('create-claim-receipt',receipt)
ids=[x['result']['ref'] for x in receipt['outcomes'] if x['intent_id']=='win-create-001']
check('create-claim-real-id',len(ids)==1 and ids[0].startswith('wqa-') and not ids[0].startswith('tmp:'),receipt)
id=ids[0]
check('create-claim-confirmed',receipt['status']=='published' and any(x['id']==id and x['confirmed'] and x['actor']==actor for x in receipt['claims']),receipt)
published=receipt['published_sha']
peer=json.loads(bash('create-claim-peer-show',['scripts/bd-read.sh','show',id,'--json'],PRIMARY).stdout)
snapshot=git('create-claim-published-snapshot',['show',published+':.beads/issues.jsonl']).stdout
rows=[json.loads(x) for x in snapshot.splitlines()]
row=next(x for x in rows if x.get('id')==id)
if isinstance(peer,list): peer=peer[0]
check('create-claim-peer-full-object',peer==row,dict(publisher=row,peer=peer))
peer_sha=text(git('create-claim-peer-sha',['rev-parse','origin/beads-backup'],PRIMARY))
check('create-claim-peer-same-sha',peer_sha==published,dict(published_sha=published,peer_sha=peer_sha))
for key,wanted in {'title':fields['title'],'description':fields['description'],'acceptance_criteria':fields['acceptance'],'notes':fields['notes'],'labels':fields['labels'],'metadata':fields['metadata'],'status':'in_progress','assignee':actor}.items():
 check('create-field-'+key,row.get(key)==wanted,dict(expected=wanted,actual=row.get(key)))
save('lifecycle-state',dict(id=id,published_sha=published,actor=actor,row=row))
print(json.dumps(dict(result='PASS create/claim/peer',id=id,published_sha=published)))
