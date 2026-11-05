import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
const [mode,root,globalFile]=process.argv.slice(2);
const {assertPublisherIdentityAndAuth}=await import(pathToFileURL(path.join(root,'scripts/bd-publisher-setup.mjs')));
const {cleanGitEnvironment}=await import(pathToFileURL(path.join(root,'scripts/lib/bd-git-environment.mjs')));
const origin={push:['https://synthetic-auth.example.invalid/test.git']};
if(mode==='missing'){
 let error;try{assertPublisherIdentityAndAuth(root,origin)}catch(e){error=e.message}
 if(!error?.includes('HTTPS authentication unavailable'))throw Error('expected actionable missing-helper STOP: '+error);
 console.log(JSON.stringify({method:'candidate exported auth preflight integration',result:'refused',error,externalNetwork:false}));
}else{
 assertPublisherIdentityAndAuth(root,origin);
 const raw=execFileSync('git',['credential','fill'],{cwd:root,input:'protocol=https\nhost=synthetic-auth.example.invalid\n\n',env:cleanGitEnvironment({...process.env,GIT_CONFIG_GLOBAL:globalFile}),encoding:'utf8'});
 if(!raw.includes('username=windows-qa\npassword=synthetic-test-only'))throw Error('wrong helper selected');
 console.log(JSON.stringify({method:'native git credential fill with synthetic only helper',result:'PASS',ownedHelperSelected:true,globalSpoofSelected:false,authenticatedPush:'NOT RUN'}));
}
