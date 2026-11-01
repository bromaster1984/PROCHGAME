/* Run with a built apple2js at EMULATOR_URL, linked proch.dsk, and Playwright. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {chromium}=require(process.env.PLAYWRIGHT_PATH||'/opt/codex/cua_node/lib/node_modules/playwright');
const base=process.env.EMULATOR_URL||'http://127.0.0.1:8123';
const khz=Number(process.env.TEST_KHZ||8000);
const out=require('node:path').resolve(__dirname,'../dist');
(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
 const page=await browser.newPage({viewport:{width:1200,height:1000}});
 page.on('pageerror',e=>console.error('PAGE:',e.message));
 await page.goto(base+'/apple2jse.html?gl_canvas=false');
 await page.waitForFunction(()=>window.Apple2&&Apple2.apple2.getIO().getSlot(6));
 await page.evaluate(async(khz)=>{const a=Apple2.apple2,d=a.getIO().getSlot(6);d.worker=null;await d.setBinary(1,'PROCH','dsk',await(await fetch('proch.dsk')).arrayBuffer());a.getVideoModes().mono(true);a.getIO().updateKHz(khz);a.reset();a.run();},khz);
 const state=()=>page.evaluate(()=>Array.from({length:8},(_,i)=>Apple2.apple2.getCPU().read(0x300+i)));
 const wait=async(index,value)=>{await page.waitForFunction(([i,v])=>Apple2.apple2.getCPU().read(0x300+i)===v,[index,value],{timeout:60000});};
 await page.waitForFunction(()=>Apple2.apple2.getCPU().read(0x30f)===0xa7&&Apple2.apple2.getCPU().read(0x310)===0x59,null,{timeout:60000});
 await wait(7,1);assert.equal((await state())[6],1,'AppleMouse found');
 await page.locator('#screen').screenshot({path:out+'/ekran-tytulowy.png'});
 const idle=()=>page.waitForFunction(()=>Apple2.apple2.getCPU().read(0x308)===0,null,{timeout:60000});
 const count=i=>page.evaluate(i=>Apple2.apple2.getCPU().read(0x300+i),i);
 const consumed=(i,n)=>page.waitForFunction(([i,n])=>Apple2.apple2.getCPU().read(0x300+i)!==n,[i,n],{timeout:60000});
 const click=async(x,y)=>{await idle();const n=await count(9);const r=await page.locator('#screen').boundingBox();await page.mouse.move(r.x+x/280*r.width,r.y+y/192*r.height);await page.mouse.down();await page.waitForTimeout(200);await page.mouse.up();await consumed(9,n);await idle();await page.waitForTimeout(80);};
 const key=async(c)=>{await idle();const n=await count(10);await page.evaluate(c=>Apple2.apple2.getIO().keyDown(c.charCodeAt(0)),c);await page.waitForTimeout(150);await page.evaluate(()=>Apple2.apple2.getIO().keyUp());await consumed(10,n);await idle();};
 const verb=async(n)=>click(n*70+25,132);
 await click(140,90);await wait(7,0);await wait(0,0);
 await page.locator('#screen').screenshot({path:out+'/gabinet-test.png'});
 // Leaving without documents must not finish the game.
 await click(254,68);await wait(0,2);await verb(3);await click(220,70);assert.equal((await state())[3],0);
 await click(20,66);await wait(0,0);
 await verb(3);await click(30,60);await wait(1,65);
 await verb(1);await click(90,102);await wait(2,1);
 await click(156,96);await wait(0,1);
 await verb(0);await click(80,70);await wait(1,67);
 await click(65,147);await click(80,70);await wait(1,71);
 await verb(1);await click(145,85);await wait(2,2);
 await click(65,147);await click(80,70);await wait(2,6);
 await click(20,66);await wait(0,0);
 // In inventory OLOWEK is first, KOPIA is second after paper is consumed.
 await click(113,147);await click(211,50);await wait(1,95);
 await click(156,96);await wait(0,1);await verb(1);await click(80,70);await wait(2,14);
 // Save, deliberately reset state using the public R command, then restore.
 await key('S');await page.waitForTimeout(2500);
 await key('R');await wait(1,0);
 await key('L');await wait(2,14);await wait(0,1);
 await click(20,66);await wait(0,0);await click(254,68);await wait(0,2);
 await verb(3);await click(220,70);await wait(3,1);
 await page.locator('#screen').screenshot({path:out+'/zakonczenie-test.png'});
 console.log('PASS: cold disk boot, native AppleMouse, no premature ending, full mouse-only puzzle, disk save/reset/load, finale');
 fs.writeFileSync(out+'/emulator-results.json',JSON.stringify({emulator:'apple2js enhanced IIe + AppleMouse slot 4',cpuMHz:khz/1000,tested_at:new Date().toISOString(),disk_sha256:require('node:crypto').createHash('sha256').update(fs.readFileSync(out+'/PROCH_EPIZOD_1.dsk')).digest('hex'),checks:['disk boot','mouse detection','premature exit blocked','complete point and click path','save/reset/load','ending'],state:await state()},null,2));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
