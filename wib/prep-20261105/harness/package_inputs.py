from pathlib import Path
import json,hashlib,shutil,subprocess,zipfile
B=Path(__file__).resolve().parent;E=B/'evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
shutil.copyfile(B/'legacy-pending/.bd-intents/qa-pending.raw.jsonl',E/'retained-pending.raw.jsonl')
shutil.copyfile(B/'unknown-receipt/.git/bd-receipts/qa-unknown-receipt.json',E/'unknown-receipt.fixture.json')
source=B/'frozen-legacy-stores';archive=E/'frozen-legacy-stores.zip'
files=[p for p in source.rglob('*') if p.is_file()]
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,p.relative_to(source).as_posix())
with zipfile.ZipFile(archive) as z:
 assert all(z.read(p.relative_to(source).as_posix())==p.read_bytes() for p in files)
bundle=E/'legacy-baseline.bundle'
result=subprocess.run(['git','--git-dir='+str(B/'legacy-origin.git'),'bundle','create',str(bundle),'refs/heads/qa/preparation','refs/heads/beads-backup'],capture_output=True)
assert result.returncode==0,result.stderr
check=subprocess.run(['git','bundle','verify',str(bundle)],cwd=B/'legacy-pending',capture_output=True)
assert check.returncode==0,check.stderr
(E/'legacy-bundle-verify.stdout.bin').write_bytes(check.stdout);(E/'legacy-bundle-verify.stderr.bin').write_bytes(check.stderr)
summary=dict(frozen_files=len(files),frozen_zip_sha256=sha(archive),frozen_zip_bytes=archive.stat().st_size,zip_full_bytes_equal=True,
 legacy_bundle_sha256=sha(bundle),legacy_bundle_bytes=bundle.stat().st_size,git_bundle_verified=True,
 pending_sha256=sha(E/'retained-pending.raw.jsonl'),unknown_receipt_sha256=sha(E/'unknown-receipt.fixture.json'),candidate_executed=False)
(E/'preservation-input-pack.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary))
