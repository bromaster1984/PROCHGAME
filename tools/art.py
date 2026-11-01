"""Original procedural pixel illustrations; native 280x192 Apple II HGR.
All pixels are designed for this adaptation, no modern rendered game substitute.
"""
from pathlib import Path
from PIL import Image, ImageDraw
from pixel_font import hgr_bytes, draw_text
import random
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'; OUT.mkdir(exist_ok=True)
rng=random.Random(1898)
glyphs=hgr_bytes()
(ROOT/'src/font.h').write_text('static const unsigned char font[512]={'+','.join(map(str,glyphs))+'};\n')

def base():
 im=Image.new('L',(280,192));d=ImageDraw.Draw(im)
 # Wallpaper: restrained period pattern, wainscoting and floor perspective.
 d.rectangle((0,16,279,123),fill=10)
 for x in range(0,280,8):d.line((x,17,x,96),fill=45)
 for x in range(4,280,16):
  for y in range(24,91,16):d.polygon([(x,y-2),(x+2,y),(x,y+3),(x-2,y)],fill=95)
 d.rectangle((0,96,279,123),fill=22);d.line((0,96,279,96),fill=180)
 for x in range(0,280,23):d.rectangle((x+2,100,x+20,119),outline=75)
 for y in (120,123,126):d.line((0,y,279,y),fill=65)
 return im,d

def label(im,s,y,scale=1):
 draw_text(im,s,(280-len(s)*7*scale)//2,y,scale)

def save(im,name):
 # Stable Bayer stipple preserves thin pen lines and atmosphere.
 bayer=((0,8,2,10),(12,4,14,6),(3,11,1,9),(15,7,13,5))
 bw=Image.new('1',im.size)
 for y in range(192):
  for x in range(280):bw.putpixel((x,y),255 if im.getpixel((x,y))>bayer[y%4][x%4]*16+7 else 0)
 data=bytearray(8192)
 for y in range(192):
  a=((y&7)<<10)+((y&56)<<4)+(y>>6)*40
  for x in range(280):
   if bw.getpixel((x,y)):data[a+x//7]|=1<<(x%7)
 (OUT/name).write_bytes(data)
 # PNG is an exact monochrome decoding of the native memory bitmap.
 bw.convert('RGB').resize((840,576),Image.Resampling.NEAREST).save(OUT/(name.lower()+'.png'))

im,d=base()
# Window overlooking rainy Warsaw; leaded frame and a passing horse tram.
d.rectangle((166,23,230,91),fill=145,outline=245)
for x,w,h in [(169,15,25),(182,19,36),(202,12,27),(216,11,40)]:
 d.rectangle((x,83-h,x+w,86),fill=57);d.polygon([(x-2,83-h),(x+w//2,76-h),(x+w+2,83-h)],fill=35)
 for yy in range(85-h,82,7):
  for xx in range(x+3,x+w-1,5):d.rectangle((xx,yy,xx+1,yy+2),fill=170)
for _ in range(58):
 x=rng.randrange(169,227);y=rng.randrange(26,87);d.line((x,y,x-1,y+4),fill=220)
for x in (166,196,199,230):d.line((x,23,x,91),fill=245,width=2)
for y in (23,49,91):d.line((166,y,230,y),fill=245,width=2)
d.polygon([(156,20),(170,20),(162,98),(150,98)],fill=40)
for x in range(155,166,3):d.line((x,24,x-5,94),fill=120)
# Grandfather clock / doorway right.
d.rectangle((239,24,274,124),fill=18,outline=160);d.rectangle((243,29,270,116),outline=75)
d.ellipse((247,71,251,75),fill=230)
d.rectangle((126,22,149,100),fill=20,outline=155);d.arc((125,16,150,41),180,360,fill=210)
d.ellipse((130,26,145,42),fill=215);d.line((137,28,137,35,142,38),fill=0)
d.rectangle((132,48,143,90),outline=95);d.line((137,51,137,81),fill=180);d.ellipse((133,80,142,89),outline=190)
# Karol in a leather armchair, cigar, waistcoat, spectacles.
d.rounded_rectangle((9,64,61,112),radius=9,fill=30,outline=145)
d.rectangle((13,88,20,121),fill=80);d.rectangle((54,88,61,121),fill=80)
d.polygon([(24,67),(43,65),(52,91),(43,110),(26,110),(18,90)],fill=52,outline=145)
d.polygon([(28,65),(36,83),(42,65)],fill=210);d.line((35,71,36,90),fill=15,width=2)
d.ellipse((25,42,45,67),fill=170,outline=230);d.pieslice((24,40,46,61),180,345,fill=28)
d.line((26,52,33,51,35,53,41,51),fill=10);d.line((30,60,40,60),fill=30,width=2)
d.line((41,84,60,78),fill=180,width=3);d.line((58,78,69,75),fill=220)
for x,y in [(69,70),(73,65),(70,59)]:d.arc((x,y,x+12,y+10),80,290,fill=120)
d.line((27,108,23,122),fill=40,width=7);d.line((43,108,48,123),fill=40,width=7)
# Your satchel on the floor, envelope.
d.polygon([(72,90),(106,90),(113,120),(68,120)],fill=45,outline=185)
d.rectangle((78,86,98,92),outline=170);d.line((70,98,110,98),fill=180);d.rectangle((88,97,94,103),fill=180)
# Massive secretary / sloping writing desk.
d.polygon([(123,85),(191,85),(208,112),(115,112)],fill=110,outline=235)
for _ in range(22):
 x=rng.randrange(123,189);y=rng.randrange(88,110);d.line((x,y,x+8,y),fill=60)
d.rectangle((119,112,204,118),fill=30,outline=190);d.line((125,118,123,127),fill=170,width=3);d.line((198,118,200,127),fill=170,width=3)
d.polygon([(143,89),(168,90),(177,103),(148,105)],fill=225,outline=30)
for y in (93,96,99):d.line((150,y,168,y),fill=45)
d.ellipse((185,95,192,102),fill=15,outline=240)
# Glass of brandy on side table.
d.ellipse((60,69,91,77),fill=85,outline=180);d.line((76,77,76,87),fill=170)
d.ellipse((72,57,81,66),outline=220);d.line((77,65,77,71),fill=230);d.line((73,71,81,71),fill=220)
save(im,'GABINET')
# Desk close-up, retaining exact hotspot geometry.
im,d=base();d.rectangle((0,20,279,127),fill=60)
for _ in range(190):
 x=rng.randrange(280);y=rng.randrange(23,127);d.line((x,y,min(x+rng.randrange(3,25),279),y),fill=rng.choice([25,35,90,110]))
d.rectangle((39,32,235,123),fill=22,outline=180);d.rectangle((44,37,230,119),outline=90)
d.polygon([(49,45),(104,43),(116,111),(56,116)],fill=210,outline=250)
for yy in range(58,104,6):d.line((59,yy,101,yy-2),fill=65)
d.ellipse((84,94,103,109),outline=100);d.line((87,100,99,102),fill=80)
d.polygon([(126,56),(165,52),(179,116),(132,119)],fill=130,outline=205)
# Pencil in the right middle hotspot, diagonal over paper.
d.line((137,97,164,63),fill=240,width=3);d.line((138,97,164,64),fill=20)
d.polygon([(134,102),(137,95),(140,98)],fill=230)
d.ellipse((204,87,231,113),fill=10,outline=200);d.rectangle((208,84,227,100),fill=40,outline=170);d.ellipse((207,81,228,88),fill=5,outline=245)
d.line((223,83,251,39),fill=200);d.polygon([(240,55),(239,31),(260,22),(251,44)],fill=150)
d.rectangle((0,53,34,79),fill=0,outline=230);d.line((8,66,27,66),fill=255);d.line((8,66,15,60),fill=255);d.line((8,66,15,72),fill=255)
save(im,'BIURKO')
# Vestibule: marble, door to the street, Marian.
im,d=base()
for x in range(0,280,28):d.line((x,121,140+(x-140)*0.7,91),fill=160)
for yy in (102,111,123):d.line((0,yy,279,yy),fill=100)
d.rectangle((86,20,177,123),fill=13,outline=230)
d.rectangle((94,27,168,119),outline=135)
for xx in (101,136):
 for yy in (34,70):d.rectangle((xx,yy,xx+26,yy+30),outline=115)
d.ellipse((157,82,161,86),fill=250)
d.polygon([(5,20),(39,20),(54,123),(0,123)],fill=45,outline=170)
for x in range(5,40,5):d.line((x,22,x+9,121),fill=95)
d.rectangle((8,55,37,80),fill=0,outline=230);d.line((15,67,30,67),fill=255);d.line((15,67,21,61),fill=255);d.line((15,67,21,73),fill=255)
# Broad, kindly butler in white shirt and waistcoat.
d.polygon([(205,57),(238,57),(252,93),(239,106),(205,106),(193,91)],fill=100,outline=230)
d.polygon([(211,58),(221,75),(233,58),(229,99),(214,99)],fill=180)
d.polygon([(216,58),(224,58),(221,65)],fill=8)
d.ellipse((209,31,236,60),fill=175,outline=240);d.pieslice((208,29,237,47),180,355,fill=35)
d.line((213,43,219,44),fill=20);d.line((225,44,231,43),fill=20);d.line((218,53,228,53),fill=40)
for yy in (76,83,90):d.ellipse((220,yy,222,yy+2),fill=10)
d.line((209,104,205,124),fill=50,width=9);d.line((233,104,239,124),fill=50,width=9)
d.ellipse((193,91,201,101),fill=170);d.ellipse((241,91,249,101),fill=170)
save(im,'SIEN')
# Title card: original architectural engraving and typographic credits.
im=Image.new('L',(280,192));d=ImageDraw.Draw(im)
for x,w,h in [(5,42,53),(50,38,64),(93,46,47),(144,34,71),(182,43,58),(231,43,50)]:
 d.rectangle((x,117-h,x+w,122),fill=35,outline=110)
 d.polygon([(x-3,117-h),(x+w//2,105-h),(x+w+3,117-h)],fill=55,outline=130)
 for yy in range(124-h,117,9):
  for xx in range(x+6,x+w-4,9):d.rectangle((xx,yy,xx+3,yy+4),fill=155)
for _ in range(150):
 x=rng.randrange(280);y=rng.randrange(5,124);d.line((x,y,x-1,y+4),fill=75)
d.rectangle((20,22,261,68),fill=0,outline=145)
label(im,'PROCH',29,4);label(im,'LIST Z PETERSBURGA',72)
label(im,'WARSZAWA / MARZEC 1898',127)
label(im,'NA PODSTAWIE POWIESCI "PROCH"',145)
label(im,'SZYMON BROMA',156)
label(im,'EPIZOD 1 / DYSKIETKA 1 / APPLE IIC',170)
label(im,'KLIKNIJ MYSZA LUB NACISNIJ ENTER',182)
save(im,'TYTUL')
# Epilogue: red ring box rendered as a luminous engraving.
im=Image.new('L',(280,192));d=ImageDraw.Draw(im)
d.polygon([(89,75),(132,61),(188,75),(145,94)],fill=85,outline=230)
d.polygon([(89,75),(145,94),(145,117),(89,97)],fill=45,outline=180)
d.polygon([(145,94),(188,75),(188,97),(145,117)],fill=25,outline=160)
d.polygon([(89,75),(83,39),(128,25),(132,61)],fill=55,outline=220)
d.ellipse((119,57,146,79),outline=245,width=2)
d.polygon([(126,57),(133,50),(140,57),(133,63)],fill=255)
label(im,'MIKOLAJ GOWOREK',4);label(im,'PRZYCHODZI PROSIC O REKE KONSTANCJI.',119)
save(im,'FINAL')
print('Generated 5 native HGR images and 7x8 font.')
