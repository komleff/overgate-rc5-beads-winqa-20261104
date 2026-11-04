from qa_common import *
setup=json.loads((E/'setup-result.json').read_text(encoding='utf-8'))
actor=setup['actor'];q=R/'queues';q.mkdir()
fields=dict(title='Windows rc.5 native child — Кириллица',type='bug',priority=2,
 description='Full object preservation\nКириллица и новая строка.',acceptance='Real ID, confirmed claim and independent same-SHA peer object.',
 notes='Initial notes\nВторая строка',labels=['windows-qa','synthetic'],external_ref='https://example.invalid/rc5-windows',
 due_at='2026-12-01T12:00:00Z',metadata={'suite':'wia-0a','nested':{'text':'Кириллица','enabled':True,'count':3,'items':[1,None,'a']}})
intents=[dict(intent_id='win-0a-parent',op='create',handle='tmp:parent',title='Synthetic Windows QA epic',type='epic',priority=2),
 dict(intent_id='win-0a-child',op='create',handle='tmp:child',parent='tmp:parent',**fields),
 dict(intent_id='win-0a-claim',op='claim',ref='tmp:child'),
 dict(intent_id='win-0a-comment',op='comment',ref='tmp:child',text='Native comment\nКомментарий'),
 dict(intent_id='win-0a-edge',op='dep_add',ref='tmp:child',blocked_by='wqa-z5e',dep_type='discovered-from')]
raw=q/'initial.raw.jsonl';prepared=q/'initial.v2.jsonl'
raw.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in intents),encoding='utf-8')
bash('initial-prepare',['scripts/bd-apply-intents.sh','--prepare','--base',setup['seed'],'--actor',actor,'--output',prepared,raw])
receipt=json.loads(bash('initial-apply',['scripts/bd-apply-intents.sh',prepared],timeout=240).stdout)
save('initial-receipt',receipt)
ids={x['intent_id']:x['result']['ref'] for x in receipt['outcomes']}
child=ids['win-0a-child'];parent=ids['win-0a-parent'];published=receipt['published_sha']
check('initial-real-nested-id',child.startswith(parent+'.') and parent.startswith('wqa-'),dict(parent=parent,child=child))
check('initial-claim-confirmed',any(x['id']==child and x['actor']==actor and x['confirmed'] for x in receipt['claims']),receipt)
snapshot=git('initial-published-snapshot',['show',published+':.beads/issues.jsonl']).stdout
rows=[json.loads(x) for x in snapshot.splitlines()];row=next(x for x in rows if x.get('id')==child)
peer=json.loads(bash('initial-isolated-peer-show',['scripts/bd-read.sh','show',child,'--json'],B/'isolated-reader').stdout)
if isinstance(peer,list):peer=peer[0]
check('initial-peer-full-object',peer==row,dict(published=row,peer=peer))
peer_sha=text(git('initial-peer-sha',['rev-parse','origin/beads-backup'],B/'isolated-reader'))
check('initial-peer-same-sha',peer_sha==published,dict(published=published,peer=peer_sha))
for key,wanted in fields.items():
 key={'type':'issue_type','acceptance':'acceptance_criteria'}.get(key,key)
 actual=row.get(key)
 check('initial-field-'+key,set(actual)==set(wanted) if key=='labels' else actual==wanted,dict(expected=wanted,actual=actual))
check('initial-comment-preserved',any('Native comment\nКомментарий' in x.get('text','') for x in row.get('comments',[])),row.get('comments'))
check('initial-typed-edges',any(x.get('type')=='parent-child' and x.get('depends_on_id')==parent for x in row.get('dependencies',[])) and any(x.get('type')=='discovered-from' and x.get('depends_on_id')=='wqa-z5e' for x in row.get('dependencies',[])),row.get('dependencies'))
save('lifecycle-state',dict(id=child,parent=parent,published_sha=published,actor=actor,row=row))
print(json.dumps(dict(result='PASS initial native create/claim/comment/typed edges/peer',id=child,parent=parent,published_sha=published)))
