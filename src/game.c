/* PROCH: List z Petersburga. Native Apple IIc / enhanced IIe. */
#include <conio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdint.h>
#include "font.h"
#define PEEK(a) (*(volatile unsigned char*)(a))
#define STATE ((unsigned char*)0x0300)
extern unsigned char native_init(void);
extern void native_poll(void);
extern void native_move(void);
extern unsigned int mouse_x,mouse_y;
extern unsigned char mouse_button;
static unsigned char room=0,verb=0,selected=0,flags=0,inventory=0,done=0;
static unsigned char mouseok=0,oldbutton=0,title=1,overlay=0;
static int mx=140,my=80,cx=140,cy=80;
static unsigned char curdrawn=0,hover=255;
static const char* objects[]={"", "KAROL KORECKI", "TECZKA IZYDORA", "SEKRETARZYK", "DRZWI DO PRZEDSIONKA", "OKNO", "LIST Z PETERSBURGA", "OLOWEK", "KALAMARZ", "POWROT DO GABINETU", "MARIAN", "DRZWI WYJSCIOWE"};
static char message[121]="";
static const char* names[]={"", "PAPIER", "OLOWEK", "KOPIA", "LIST"};
static const char* rooms[]={"GABINET KORECKIEGO", "SEKRETARZYK", "PRZEDSIONEK"};
static const char* verbs[]={"OBEJRZYJ", "WEZ", "UZYJ", "ROZMOWA"};
/* flag bits: permission, read, placed paper, copied, dry, returned, spoken Marian */
static unsigned int rowaddr(unsigned char y) {
 return 0x2000+((y&7)<<10)+((y&56)<<4)+(y>>6)*40;
}
static void glyph(unsigned char x,unsigned char y,unsigned char c,unsigned char inv) {
 unsigned char i,b; unsigned char* p;
 if(c<32||c>95)c='?';
 for(i=0;i<8;++i){p=(unsigned char*)(rowaddr(y+i)+x);b=font[(c-32)*8+i];*p=inv?(b^127):b;}
}
static void text(unsigned char col,unsigned char y,const char* s,unsigned char inv) {
 while(*s && col<40){glyph(col++,y,*s++,inv);}
}
static void band(unsigned char y,unsigned char n) {
 unsigned char j;for(j=0;j<n;++j)memset((void*)rowaddr(y+j),0,40);
}
static void say(const char* s){
 unsigned char n=0;char last=0;
 while(*s&&n<120){if(*s!=' '||last!=' '){message[n++]=*s;last=*s;}++s;}
 message[n]=0;
}
static void cursorflip(void) {
 unsigned char i; unsigned int a; int x,y;
 for(i=0;i<9;++i){x=cx+(i<5?i-2:0); y=cy+(i<5?0:i-6);if(x>=0&&x<280&&y>=0&&y<192){a=rowaddr((unsigned char)y)+x/7;*(unsigned char*)a^=1<<(x%7);}}
 curdrawn=!curdrawn;
}
static void hud(void) {
 unsigned char i,n,col,pos=0,end,len; char line[41];
 band(128,64);
 /* Four verbs, selected inverse; inventory is a row of clickable names. */
 for(i=0;i<4;++i) text(i*10,128,verbs[i],verb==i);
 text(0,144,"TORBA:",0);col=7;
 for(i=1;i<=4;++i)if(inventory&(1<<(i-1))){text(col,144,names[i],selected==i);col+=8;}
 n=(unsigned char)strlen(message);
 for(i=0;i<3&&pos<n;++i){
  while(message[pos]==' ')++pos;
  end=pos+40;if(end>n)end=n;
  if(end<n&&message[end]!=' '){len=end;while(len>pos&&message[len]!=' ')--len;if(len>pos)end=len;}
  len=end-pos;memcpy(line,message+pos,len);line[len]=0;text(0,160+i*8,line,0);pos=end;
 }
 text(0,184,"? POMOC   S ZAPIS   L ODCZYT   R OD NOWA",0);
 /* Small test/debug state, intentionally outside ProDOS globals. */
 STATE[0]=room;STATE[1]=flags;STATE[2]=inventory;STATE[3]=done;STATE[4]=selected;STATE[5]=verb;STATE[6]=mouseok;STATE[7]=title;
}
static unsigned char loadpic(const char* name) {
 int fd,n; fd=open(name,O_RDONLY);if(fd<0)return 0;
 n=read(fd,(void*)0x2000,8192);close(fd);return n==8192;
}
static void draw(void) {
 const char* files[]={"GABINET","BIURKO","SIEN"};
 if(curdrawn)cursorflip();hover=255;
 if(!loadpic(files[room])){memset((void*)0x2000,0,8192);say("BLAD ODCZYTU OBRAZU. SPRAWDZ DYSKIETKE.");}
 text(1,0,"PROCH / LIST Z PETERSBURGA",0);text(1,8,rooms[room],0);
 hud();
}
static void inventoryclick(int x) {
 unsigned char i,col=7;
 for(i=1;i<=4;++i)if(inventory&(1<<(i-1))){if(x>=col*7&&x<(col+8)*7){selected=i;verb=2;say("WYBRANO PRZEDMIOT. KLIKNIJ CEL UZYCIA.");return;}col+=8;}
 selected=0;say("TORBA IZYDORA. WYBIERZ PRZEDMIOT.");
}
static unsigned char target(int x,int y) {
 if(room==0){if(x<65)return 1;if(x<121&&y>66)return 2;if(x<204&&y>73)return 3;if(x>230)return 4;if(x>164&&y<84)return 5;}
 if(room==1){if(x<40)return 9;if(x<119&&y>42&&y<110)return 6;if(x<183&&y>51&&y<117)return 7;if(x>190&&y>77)return 8;}
 if(room==2){if(x<65)return 9;if(x>183)return 10;if(x>90&&x<183)return 11;}
 return 0;
}
static void help(void){
 if(curdrawn)cursorflip();band(24,104);
 text(1,24,"JESTES IZYDOREM JELINKIEM.",0);
 text(1,40,"SKOPIUJ LIST I SCHOWAJ ORYGINAL.",0);
 text(1,56,"KLIKNIJ CZASOWNIK, POTEM OBIEKT.",0);
 text(1,72,"PRZEDMIOT Z TORBY WYBIERA UZYJ.",0);
 text(1,88,"STRZALKI + ENTER ZASTEPUJA MYSZ.",0);
 text(1,104,"KLIKNIJ, ABY WROCIC DO SCENY.",0);overlay=1;
}
static void hint(void){
 if(!(flags&1))say("POROZMAWIAJ Z KAROLEM O LISTACH I PRASIE.");
 else if(!(inventory&1)&&!(flags&4))say("W TWOJEJ TECZCE JEST CZYSTY PAPIER.");
 else if(!(flags&2))say("OBEJRZYJ LIST NA SEKRETARZYKU.");
 else if(!(flags&4))say("WYBIERZ PAPIER Z TORBY I UZYJ NA LISCIE.");
 else if(!(flags&8))say("WEZ OLOWEK. UZYJ GO NA LISCIE Z PAPIEREM.");
 else if(!(flags&16))say("OBEJRZYJ GAZETE. SPRAWDZ KOPIE NA OKNIE.");
 else if(!(flags&32))say("TERAZ WEZ ORYGINALNY LIST Z SEKRETARZYKA.");
 else say("POROZMAWIAJ Z MARIANEM W PRZEDSIONKU.");
}
static void interact(unsigned char t) {
 if(!t){say("DESZCZ I TYKANIE ZEGARA. POMYSL SPOKOJNIE.");return;}
 if(t==9){room=0;say("WRACASZ DO GABINETU.");draw();return;}
 if(t==3){if(!(flags&1)){say("KAROL: NIE GRZEB MI W PAPIERACH. ZAPYTAJ.");return;}room=1;say("LIST MUSI WROCIC NIENARUSZONY DO KONSULATU.");draw();return;}
 if(t==4){room=2;say("MARIAN CZEKA PRZY DRZWIACH WYJSCIOWYCH.");draw();return;}
 if(t==1){
  if(verb==3){flags|=1;say("KAROL: SKORO MUSISZ, SKOPIUJ LIST PRZY  SEKRETARZYKU. TYLKO UWAZAJ NA ORYGINAL.");}
  else if(verb==2&&selected==3){if(flags&16)say("KAROL: WIEC NIE WOLNO NAM JUZ NIC PISAC? SCHOWAJ ORYGINAL I IDZ DO KONSULATU.");else say("KAROL: CZY TA KOPIA JEST W OGOLE CZYTELNA?");}
  else say("KAROL KORECKI. KONIAK I INTERESY CENI   BARDZIEJ NIZ WOLNOSC SLOWA.");return;
 }
 if(t==2){
  if(verb==1){if((inventory&1)||(flags&4))say("W TECZCE NIE MA JUZ CZYSTYCH KARTEK.");else{inventory|=1;say("Z TECZKI WYJMUJESZ CZYSTA KARTKE PAPIERU.");}}
  else say("TWOJA TECZKA. W SRODKU CZYSTY PAPIER.   ORYGINAL LISTU MUSI WROCIC DO SRODKA.");return;
 }
 if(t==5){if(verb==2&&selected==3){flags|=16;say("POD SWIATLO SPRAWDZASZ KOPIE. WSZYSTKIE ZAKAZY PRZEPISANE. ORYGINAL JEST CALY.");}else say("WARSZAWA, MARZEC 1898. ZA SZYBA DESZCZ I OSTATNI TRAMWAJ KONNY.");return;}
 if(t==6){
  if(flags&32){say("ORYGINALNY LIST JEST BEZPIECZNY W TORBIE.");return;}
  if(verb==0){flags|=2;say("LIST: ZAKAZ PISANIA O POLAKACH, SZKOLACH I MICKIEWICZU. TRZEBA SKOPIOWAC ZAKAZY.");}
  else if(verb==1){if(!(flags&16))say("NIE ZABIORE LISTU, POKI NIE SPRAWDZE   WIERNEJ KOPII POD SWIATLO.");else{flags|=32;inventory|=8;say("CHOWASZ ORYGINAL W TECZCE. NIC NIE     ZOSTALO USZKODZONE. CZAS DO KONSULATU.");}}
  else if(verb==2&&selected==1){if(!(flags&2))say("NAJPIERW PRZECZYTAJ LIST. MUSISZ WIEDZIEC CO PRZEPISAC.");else{flags|=4;inventory&=254;selected=0;say("KLADZIESZ CZYSTY PAPIER OBOK LISTU.    TERAZ POTRZEBNY BEDZIE OLOWEK.");}}
  else if(verb==2&&selected==2){if(!(flags&4))say("NIE PISZ PO ORYGINALE! NAJPIERW POLOZ  CZYSTY PAPIER OBOK LISTU.");else if(flags&8)say("KOPIA JUZ JEST W TORBIE.");else{flags|=8;inventory|=4;say("PRZEPISUJESZ ZAKAZY. KOPIA TRAFIA DO   TORBY. SPRAWDZ JA JESZCZE POD SWIATLO.");}}
  else say("ORYGINAL MA WROCIC W STANIE NIENARUSZONYM.");return;
 }
 if(t==7){if(verb==1){inventory|=2;say("BIERZESZ OLOWEK. GRAFIT NIE WYMAGA TUSZU.");}else say("OLOWEK I PRZYBORY PISARSKIE KAROLA.    LEPIEJ NIE RYZYKOWAC PLAMY Z ATRAMENTU.");return;}
 if(t==8){say("KALAMARZ. JEDNA PLAMA MOGLABY ZNISZCZYC POUFNY DOKUMENT. OLOWEK JEST LEPSZY.");return;}
 if(t==10){
  if(verb==3){flags|=64;if((flags&48)==48){done=1;loadpic("FINAL");band(128,64);text(1,128,"KONIEC EPIZODU 1",0);text(1,144,"NA PODSTAWIE POWIESCI PROCH",0);text(1,152,"AUTOR: SZYMON BROMA",0);text(1,168,"MIKOLAJ PRZYBYWA PROSIC O REKE...",0);text(1,184,"CIAG DALSZY: PLANOWANA DYSKIETKA 2",0);STATE[3]=1;}
   else say("MARIAN: PAN JEST ZAMYSLONY. CZY LIST   JEST SKOPIOWANY I SCHOWANY DO TECZKI?");}
  else say("MARIAN, KAMERDYNER. SUROWA TWARZ,      LAGODNE OCZY. CZUWA NAD DOMEM KORECKICH.");return;
 }
 if(t==11){if(verb==2&&selected==3){if(flags&16)say("KOPIA JEST JUZ SPRAWDZONA. ZABIERZ    ORYGINAL I POROZMAWIAJ Z MARIANEM.");else say("TU JEST ZA CIEMNO. SPRAWDZ KOPIE PRZY  OKNIE W GABINECIE.");}else say("ZA TYMI DRZWIAMI JEST MIASTO I KONSULAT. NIE ODEJDE BEZ BEZPIECZNEGO ORYGINALU.");}
}
static void click(void){
 unsigned char t;
 if(title){title=0;STATE[7]=0;room=0;say("IZYDOR: LIST JEST TYLKO POZYCZONY.    MUSZE GO SKOPIOWAC I ODDAC FRANCUZOM.");draw();return;}
 if(done)return;
 if(overlay){overlay=0;draw();return;}
 if(my>=184){help();return;}
 if(my>=160){hint();hud();return;}
 if(my>=144&&my<152){inventoryclick(mx);hud();return;}
 if(my>=128&&my<140){verb=(unsigned char)(mx/70);selected=0;hud();return;}
 t=target(mx,my);interact(t);if(!done)hud();
}
static void savegame(void){
 unsigned char data[12];int fd;unsigned char i,sum=0;
 data[0]='P';data[1]='R';data[2]=1;data[3]=room;data[4]=flags;data[5]=inventory;
 data[6]=verb;data[7]=selected;data[8]=done;data[9]=0;data[10]=0;
 for(i=0;i<11;++i)sum+=data[i];data[11]=sum;
 fd=open("POSTEP",O_WRONLY|O_CREAT|O_TRUNC,0666);
 if(fd<0){say("NIE MOZNA ZAPISAC. ODBLOKUJ DYSKIETKE.");return;}
 if(write(fd,data,12)==12)say("ZAPISANO POSTEP NA TEJ DYSKIETCE.");else say("BLAD ZAPISU POSTEPU.");close(fd);
}
static void loadgame(void){
 unsigned char data[12],i,sum=0;int fd,n;fd=open("POSTEP",O_RDONLY);
 if(fd<0){say("NIE MA JESZCZE ZAPISU NA TEJ DYSKIETCE.");return;}memset(data,0,12);n=read(fd,data,12);close(fd);
 for(i=0;i<11;++i)sum+=data[i];
 if(n!=12||data[0]!='P'||data[1]!='R'||data[2]!=1||data[3]>2||data[6]>3||data[7]>4||data[11]!=sum){say("NIEPRAWIDLOWY PLIK ZAPISU.");return;}
 room=data[3];flags=data[4];inventory=data[5];verb=data[6];selected=data[7];done=0;title=0;overlay=0;
 say("WCZYTANO POSTEP.");draw();
}
void main(void){
 unsigned char key,b,t;
 clrscr();memset(STATE,0,11);
 mouseok=native_init();
 if(mouseok){mouse_x=140;mouse_y=80;native_move();}
 /* Main RAM HGR page one, 40 columns, full-screen graphics. */
 PEEK(0xC00C)=0;PEEK(0xC000)=0;PEEK(0xC052)=0;PEEK(0xC054)=0;PEEK(0xC057)=0;PEEK(0xC050)=0;
 if(!loadpic("TYTUL")){memset((void*)0x2000,0,8192);text(2,40,"PROCH",0);text(2,64,"NA PODSTAWIE POWIESCI SZYMONA BROMY",0);}
 STATE[6]=mouseok;STATE[7]=title;STATE[15]=0xa7;STATE[16]=0x59;
 while(1){
  if(curdrawn)cursorflip();
  if(mouseok){native_poll();mx=mouse_x;my=mouse_y;b=mouse_button;}
  else b=0;
  if(!title&&!done&&!overlay){t=my>=24&&my<128?target(mx,my):0;if(t!=hover){band(16,8);text(1,16,objects[t],0);hover=t;}}
  if(b&&!oldbutton){STATE[8]=1;click();STATE[8]=0;++STATE[9];}oldbutton=b;
  if(kbhit()){
   STATE[8]=1;key=cgetc();
   if(key==CH_CURS_LEFT)mx-=7;else if(key==CH_CURS_RIGHT)mx+=7;
   else if(key==CH_CURS_UP)my-=5;else if(key==CH_CURS_DOWN)my+=5;
   else if(key==13||key==' ')click();
   else if(key=='?'||key=='h'||key=='H')help();
   else if(key=='s'||key=='S'){if(!title&&!done){savegame();hud();}}
   else if(key=='l'||key=='L'){loadgame();hud();}
   else if(key=='r'||key=='R'){room=verb=selected=flags=inventory=done=title=overlay=0;say("NOWA GRA. POROZMAWIAJ Z KAROLEM.");draw();}
   else if(key>='1'&&key<='4'){verb=key-'1';selected=0;hud();}
   if(mx<2)mx=2;if(mx>277)mx=277;if(my<2)my=2;if(my>189)my=189;
   if(mouseok){mouse_x=mx;mouse_y=my;native_move();}
   STATE[8]=0;++STATE[10];
  }
  cx=mx;cy=my;cursorflip();
 }
}
