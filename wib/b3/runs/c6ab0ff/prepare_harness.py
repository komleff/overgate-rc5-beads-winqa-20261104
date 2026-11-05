from pathlib import Path
R=Path(__file__).resolve().parent;old=Path('D:/CodexArtifacts/overgate-rc5-wib-b3-80071dd-winqa-20261105')
for n in ['common.py','preflight.py','installed.py','complex_first.py','pr-contract.txt']:
 data=(old/n).read_text(encoding='utf-8')
 data=data.replace('80071dd6edad740645d8388e3e5f589ad299458e','c6ab0ffb45ec14abf58d0e930d64c220cee73658').replace('96346205f076398cf6e37340e1a3e0d661588442','1122c8fd8426fe7635526dc1ab1f38f570c6aba8').replace('6bacf87521b7d3ee33c944b12ce13cbac8a702158261043b240b2714c4924d0d','6e5e06f4ed5c009b8985e34576985cdccbbf763ce49af3c160e5277059dddada')
 if n=='common.py':data=data.replace("R=Path(__file__)","sys.stdout.reconfigure(encoding='utf-8',errors='backslashreplace');sys.stderr.reconfigure(encoding='utf-8',errors='backslashreplace')\nR=Path(__file__)")
 (R/n).write_text(data,encoding='utf-8',newline='\n')
print('New QA driver prepared; old source/fixtures/archive untouched.')
