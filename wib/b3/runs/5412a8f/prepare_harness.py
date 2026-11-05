from pathlib import Path
R=Path(__file__).resolve().parent;old=Path('D:/CodexArtifacts/overgate-rc5-wib-b3-6826dcc-winqa-20261105')
for n in ['common.py','preflight.py','installed.py','complex_first.py','pr-contract.txt']:
 data=(old/n).read_text(encoding='utf-8').replace('6826dccad5691cb41c3d749e25de5a41d13a299c','5412a8f25fe94f2e6c313357e556717469514f14').replace('54b843d2ff2e6455f7df04148dcb1d960cd05375','d4741fe7744ea1da0bd86fba2b1b6bbbe0dff2d4').replace('6348aa8058cdb1af68c2a0c63a7fc00e9d94795903b778b7ec8924016e82f36f','e0987f00495fbda3047784afc29c67ec66dae10d568cef2458408754a04d05d2')
 if n=='preflight.py':data=data.replace('len(paths)==25','len(paths)==29')
 (R/n).write_text(data,encoding='utf-8',newline='\n')
print('Fresh source-bound harness prepared; old archives and failed stores untouched.')
