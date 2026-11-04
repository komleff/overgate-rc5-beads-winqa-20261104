import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import {ManagedGit} from './actor-b/scripts/lib/bd-managed-git.mjs';
import {parseSnapshot,assertExactSnapshot} from './actor-b/scripts/lib/bd-snapshot.mjs';
const repo=new ManagedGit({cwd:process.cwd()}),state=repo.readPublished();
const rows=state.snapshot.trimEnd().split('\n').map(JSON.parse);
const id=JSON.parse(fs.readFileSync(process.argv[2],'utf8')).id;
const cases=[];
for(const [name,data] of [['task-loss',rows.filter(x=>x.id!==id)],['same-count-rewrite',rows.map(x=>x.id===id?{...x,title:'Unauthorized same-count rewrite'}:x)]]){
 const snapshot=data.map(JSON.stringify).join('\n')+'\n';
 const candidate=repo.commitCandidate({base:state.R,snapshot,ledger:state.ledger});
 execFileSync('git',['update-ref','refs/heads/qa/'+name,candidate]);
 cases.push({name,candidate,base:state.R,id});
}
const malformed=[];
for(const raw of [' \n\t\n','\n',' ']){
 let rejected=false,message='';try{parseSnapshot(raw);}catch(e){rejected=true;message=e.message}
 if(!rejected)throw new Error('B2 malformed nonempty snapshot accepted: '+JSON.stringify(raw));
 malformed.push({raw,rejected,message});
}
if(parseSnapshot('').length!==0)throw new Error('B2 canonical empty rejected');
assertExactSnapshot('','');
const result={source:'0a8685ed072fece134418a1d18ed11d8a53759a3',cases,B2:{result:'PASS',canonical_zero_bytes:true,malformed}};
fs.writeFileSync(process.argv[3],JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
