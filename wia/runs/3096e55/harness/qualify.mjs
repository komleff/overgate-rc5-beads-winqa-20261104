import fs from 'node:fs';
import {qualifyBinary} from './source-3096e55/scripts/lib/bd-managed-cli.mjs';
const [native,tampered,out]=process.argv.slice(2);
const win='b1f3609fea1d9f0f19b2ed49098b3628acfa6ca115aa28b01a1ee178c3a214de';
const linux='54fc0e0581ce4c5487a5b242f0a4f34af1ef09cf056e164a1af63a6ec7aa1e0e';
if(process.platform!=='win32')throw new Error('native Windows required');
const actual=qualifyBinary(native);
if(actual!==win)throw new Error('actual native Windows hash qualification mismatch');
const cases=[{case:'actual qualified native Windows binary',result:'PASS',digest:actual,platform:process.platform,method:'default real stream fingerprint and actual platform'}];
function denied(name,file,options,method){
 let refused=false,error='';try{qualifyBinary(file,options)}catch(e){refused=true;error=e.message}
 if(!refused||!error.includes('fingerprint not qualified'))throw new Error(name+' was not rejected by fingerprint/platform gate: '+error);
 cases.push({case:name,result:'PASS refusal',error,method});
}
denied('actual tampered executable bytes',tampered,undefined,'real stream SHA256, no execution of tampered file');
denied('Linux digest presented under win32',native,{platform:'win32',fingerprint:()=>linux},'exported function platform/digest matrix with injected reported Linux digest; not a live Linux execution');
denied('real Windows digest under Linux platform',native,{platform:'linux'},'default real stream fingerprint, explicit mismatched platform argument');
const result={result:'PASS scoped',source:'3096e550bfd6f4ff73c987812a2dda2c7d339669',native,platform:process.platform,cases,db_or_task_calls:0};
fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
