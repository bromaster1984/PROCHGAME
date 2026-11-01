"""Build a fresh 140 KiB ProDOS volume, then emit genuine DOS-sector-order .dsk."""
from pathlib import Path
import struct, hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
DO=[0,7,14,6,13,5,12,4,11,3,10,2,9,1,8,15]
PO=[0,8,1,9,2,10,3,11,4,12,5,13,6,14,7,15]
def build():
 disk=bytearray(143360)
 disk[:1024]=(ROOT/'assets/system/boot.bin').read_bytes()
 # Root directory header and four chained blocks.
 for b in range(2,6):struct.pack_into('<HH',disk,b*512,b-1 if b>2 else 0,b+1 if b<5 else 0)
 h=2*512+4;name=b'PROCH1';disk[h]=0xf0|len(name);disk[h+1:h+1+len(name)]=name
 disk[h+0x1c:h+0x20]=bytes([0,0,0xc3,39]);disk[h+0x20]=13
 struct.pack_into('<HH',disk,h+0x23,6,280)
 nextblock=7;entries=[]
 def allocate(data):
  nonlocal nextblock
  n=nextblock;nextblock+=1
  if nextblock>280:raise ValueError('Disk full')
  disk[n*512:n*512+len(data)]=data
  return n
 def add(name,data,kind,aux):
  blocks=[]
  for i in range(0,len(data),512):blocks.append(allocate(data[i:i+512]))
  if len(blocks)>1:
   ix=bytearray(512)
   for i,b in enumerate(blocks):ix[i]=b&255;ix[256+i]=b>>8
   key=allocate(ix);storage=2;count=len(blocks)+1
  else:key=blocks[0];storage=1;count=1
  e=bytearray(39);n=name.encode('ascii');e[0]=(storage<<4)|len(n);e[1:1+len(n)]=n;e[16]=kind
  struct.pack_into('<HH',e,17,key,count);e[21:24]=len(data).to_bytes(3,'little');e[30]=0xe3
  struct.pack_into('<H',e,24,((2026-1900)%100)<<9|10<<5|31)
  struct.pack_into('<H',e,33,((2026-1900)%100)<<9|10<<5|31)
  struct.pack_into('<H',e,31,aux);struct.pack_into('<H',e,37,2)
  entries.append(e)
 add('PRODOS',(ROOT/'assets/system/PRODOS').read_bytes(),0xff,0)
 add('PROCH.SYSTEM',(ROOT/'assets/system/loader.system').read_bytes(),0xff,0x2000)
 # Compiler output is AppleSingle: extract entry 1, preserving load address.
 apple=(OUT/'PROCH').read_bytes();assert apple[:4]==bytes.fromhex('00051600')
 offset,length=struct.unpack_from('>II',apple,30)
 add('PROCH',apple[offset:offset+length],6,0x803)
 for name in ['TYTUL','GABINET','BIURKO','SIEN','FINAL']:add(name,(ROOT/'assets'/name).read_bytes(),6,0x2000)
 for i,e in enumerate(entries):
  slot=i+1;block=2+slot//13;index=slot%13;addr=block*512+4+index*39;disk[addr:addr+39]=e
 struct.pack_into('<H',disk,h+0x21,len(entries))
 for b in range(nextblock,280):disk[6*512+b//8]|=0x80>>(b%8)
 (OUT/'PROCH_EPIZOD_1.po').write_bytes(disk)
 dos=bytearray(143360)
 for t in range(35):
  for p in range(16):dos[(t*16+DO[p])*256:(t*16+DO[p]+1)*256]=disk[(t*16+PO[p])*256:(t*16+PO[p]+1)*256]
 path=OUT/'PROCH_EPIZOD_1.dsk';path.write_bytes(dos)
 (OUT/'SHA256SUMS').write_text(hashlib.sha256(dos).hexdigest()+'  '+path.name+'\n')
 print(f'{path}: 35 tracks, 16 sectors, 256 bytes/sector; {280-nextblock} free blocks')
if __name__=='__main__':build()
