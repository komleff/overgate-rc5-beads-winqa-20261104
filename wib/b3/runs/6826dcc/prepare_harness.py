from pathlib import Path
R=Path(__file__).resolve().parent;old=Path('D:/CodexArtifacts/overgate-rc5-wib-b3-c6ab0ff-winqa-20261105')
for n in ['common.py','preflight.py','installed.py','complex_first.py','pr-contract.txt']:
 data=(old/n).read_text(encoding='utf-8').replace('c6ab0ffb45ec14abf58d0e930d64c220cee73658','6826dccad5691cb41c3d749e25de5a41d13a299c').replace('1122c8fd8426fe7635526dc1ab1f38f570c6aba8','54b843d2ff2e6455f7df04148dcb1d960cd05375').replace('6e5e06f4ed5c009b8985e34576985cdccbbf763ce49af3c160e5277059dddada','6348aa8058cdb1af68c2a0c63a7fc00e9d94795903b778b7ec8924016e82f36f')
 if n=='common.py':data=data.replace("ENV.update(BD_BIN", "ENV.pop('PYTHONUTF8',None);ENV.pop('PYTHONIOENCODING',None)\nENV.update(BD_BIN")
 (R/n).write_text(data,encoding='utf-8',newline='\n')
print('Fresh source-bound QA harness prepared; native child UTF8 env overrides removed.')
