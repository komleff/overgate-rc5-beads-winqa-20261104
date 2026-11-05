from pathlib import Path
import subprocess,sys,locale,json
root=Path(sys.argv[1]).resolve()
args=['git','-C',str(root),'rev-parse','--show-toplevel']
raw=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
native=subprocess.run(args,capture_output=True,text=True,check=True).stdout.strip()
utf8=raw.decode('utf-8').strip()
result=dict(method='read-only native isolated Python/Git encoding diagnostic; no candidate source imported or executed',argv=args,python=sys.executable,utf8_mode=sys.flags.utf8_mode,locale_encoding=locale.getencoding(),preferred_encoding=locale.getpreferredencoding(False),actual_root=str(root),raw_stdout_hex=raw.hex(),decoded_utf8=utf8,decoded_default_text=native,utf8_path_equals_root=Path(utf8).resolve()==root,default_text_path_equals_root=Path(native).resolve()==root)
print(json.dumps(result,ensure_ascii=True,sort_keys=True))
