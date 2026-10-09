// Kullanım: node render.cjs <html> <out.mp4> | node render.cjs <html> <out.png> --still <sn>
const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const {spawn}=require('child_process');const path=require('path');
(async()=>{
 const [,,html,out,flag,tv]=process.argv;const FPS=30;
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox']});
 const pg=await b.newPage({viewport:{width:1080,height:1920}});
 await pg.goto('file://'+path.resolve(html));await pg.waitForFunction('window.READY===true');
 if(flag==='--still'){await pg.evaluate(t=>render(t),+tv);await pg.screenshot({path:out});await b.close();return}
 const dur=await pg.evaluate('window.DURATION');const n=Math.round(dur*FPS);
 const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-f','lavfi','-i','anullsrc=r=44100:cl=stereo','-shortest','-c:v','libx264','-pix_fmt','yuv420p','-crf','17','-preset','medium','-c:a','aac','-b:a','96k','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
 for(let i=0;i<n;i++){await pg.evaluate(t=>render(t),i/FPS);const buf=await pg.screenshot({type:'jpeg',quality:94});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r))}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('ok',out,dur+'s');
})();
