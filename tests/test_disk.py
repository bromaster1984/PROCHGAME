"""Check disk ordering, ProDOS directory/bitmap, actual file bytes and boot data."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from disk import ROOT,DO,PO
po=(ROOT/'dist/PROCH_EPIZOD_1.po').read_bytes()
do=(ROOT/'dist/PROCH_EPIZOD_1.dsk').read_bytes()
assert len(po)==len(do)==143360
assert po[:1024]==(ROOT/'assets/system/boot.bin').read_bytes()
for t in range(35):
 for p in range(16):assert do[(t*16+DO[p])*256:(t*16+DO[p]+1)*256]==po[(t*16+PO[p])*256:(t*16+PO[p]+1)*256]
header=po[1028:1067]
assert header[31:33]==bytes([39,13])
assert int.from_bytes(header[33:35],'little')==8
assert int.from_bytes(header[35:37],'little')==6
used=set(range(7));files={}
for i in range(1,9):
 e=po[1028+i*39:1028+(i+1)*39];name=e[1:1+(e[0]&15)].decode()
 key=int.from_bytes(e[17:19],'little');size=int.from_bytes(e[21:24],'little')
 if e[0]>>4==1:blocks=[key]
 else:
  assert key not in used;used.add(key)
  ix=po[key*512:(key+1)*512]
  blocks=[ix[i]+256*ix[256+i] for i in range((size+511)//512)]
 for b in blocks:assert b not in used;used.add(b)
 files[name]=b''.join(po[b*512:(b+1)*512] for b in blocks)[:size]
for b in range(280):assert bool(po[3072+b//8]&(0x80>>(b%8)))==(b not in used)
for name in ['TYTUL','GABINET','BIURKO','SIEN','FINAL']:assert files[name]==(ROOT/'assets'/name).read_bytes()
assert files['PRODOS']==(ROOT/'assets/system/PRODOS').read_bytes()
assert files['PROCH.SYSTEM']==(ROOT/'assets/system/loader.system').read_bytes()
assert len(files['PROCH'])>8192
print('PASS: 560 sector mappings, boot blocks, 8 files, allocation bitmap, HGR asset bytes')
