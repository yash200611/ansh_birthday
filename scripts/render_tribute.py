import sys, math, subprocess, wave, json
from pathlib import Path
sys.path.insert(0,str(Path('build/vendor').resolve()))
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import imageio_ffmpeg
W,H,FPS=1080,1920,30
OUT=Path('output');OUT.mkdir(exist_ok=True)
BLUE=(78,214,255);GOLD=(241,192,105);RED=(201,45,54);WHITE=(242,242,237)
fontdir='/System/Library/Fonts/Supplemental/'
def font(n,bold=False):return ImageFont.truetype(fontdir+('Arial Narrow Bold.ttf' if bold else 'Arial.ttf'),n)
fonts={n:font(n,b) for n,b in []}
def text(im,s,y,size=42,col=WHITE,bold=False,x=None):
 d=ImageDraw.Draw(im);f=font(size,bold);box=d.textbbox((0,0),s,font=f);x=(W-(box[2]-box[0]))/2 if x is None else x;d.text((x,y),s,font=f,fill=col)
def track(im,s,y,size=24,col=BLUE,spacing=5):
 d=ImageDraw.Draw(im);f=font(size);width=sum(d.textlength(c,font=f)+spacing for c in s)-spacing;x=(W-width)/2
 for c in s:d.text((x,y),c,font=f,fill=col);x+=d.textlength(c,font=f)+spacing
photos=[Image.open(f'public/photos/{i:02}.jpg').convert('RGB') for i in range(15)]
cards=[]
for p in photos:
 c=Image.new('RGB',(628,850),(7,14,22));f=ImageOps.contain(p,(600,800),Image.Resampling.LANCZOS);c.paste(f,((628-f.width)//2,(850-f.height)//2));cards.append(c)
y,x=np.mgrid[0:H,0:W];r=np.sqrt(((x-W/2)/W)**2+((y-H*.43)/H)**2)
base=np.zeros((H,W,3),dtype=np.uint8)
for i,v in enumerate([8,20,32]):base[:,:,i]=np.clip(v*(1-r*.8)+3,0,255)
BASE=Image.fromarray(base)
rng=np.random.default_rng(3000);stars=rng.random((95,4))
def reactor(im,cx,cy,rad,t,col=BLUE,power=1):
 d=ImageDraw.Draw(im)
 for rr,ww in [(rad,2),(rad*.91,5),(rad*.75,2),(rad*.49,2)]:
  d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),outline=tuple(int(c*power) for c in col),width=ww)
 for j in range(12):
  a=j*30+t*17;d.arc((cx-rad*.84,cy-rad*.84,cx+rad*.84,cy+rad*.84),a,a+17,fill=col,width=max(3,int(rad*.06)))
 pts=[(cx+rad*.44*math.cos(a),cy+rad*.44*math.sin(a)) for a in [-math.pi/2,math.pi/6,math.pi*5/6]]
 d.polygon(pts,fill=col);rr=rad*.23;d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill=WHITE)
def helmet(im,cx,cy,s,col=GOLD):
 d=ImageDraw.Draw(im)
 def pts(v):return [(cx+a*s,cy+b*s) for a,b in v]
 d.polygon(pts([(-.65,-.75),(-.35,-1),(.35,-1),(.65,-.75),(.73,.15),(.42,.84),(.2,1),(-.2,1),(-.42,.84),(-.73,.15)]),fill=(54,18,24),outline=col,width=4)
 d.line(pts([(-.53,-.65),(-.37,-.86),(.37,-.86),(.53,-.65),(.46,-.06),(.25,.2),(.3,.64),(.15,.83),(-.15,.83),(-.3,.64),(-.25,.2),(-.46,-.06),(-.53,-.65)]),fill=col,width=5)
 for sign in [-1,1]:d.polygon(pts([(sign*.12,-.08),(sign*.51,-.18),(sign*.46,.0),(sign*.15,.07)]),fill=BLUE)
 d.line(pts([(-.25,.57),(.25,.57)]),fill=col,width=5)
def bg(t,warm=0):
 im=BASE.copy();d=ImageDraw.Draw(im);col=tuple(int(BLUE[i]*(1-warm)+GOLD[i]*warm) for i in range(3))
 for xx in range(0,W,90):d.line((xx,0,xx,H),fill=(10,26,36),width=1)
 for yy in range(0,H,90):d.line((0,yy,W,yy),fill=(10,26,36),width=1)
 for a,b,c,e in stars:
  xx=int(a*W);yy=int((b*H-t*(12+e*23))%H);br=.25+.5*abs(math.sin(t*.6+c*6));cc=tuple(int(z*br) for z in col);d.ellipse((xx,yy,xx+2+c*3,yy+2+c*3),fill=cc)
 for xx,sgn in [(50,1),(1030,-1)]:
  d.line((xx,190,xx,1610),fill=(26,70,84),width=1)
  d.line((xx,190,xx+sgn*65,190),fill=col,width=3);d.line((xx,1610,xx+sgn*65,1610),fill=col,width=3)
 track(im,'STARK INDUSTRIES   /   SPECIAL PROJECTS',110,19,col)
 d.line((90,160,990,160),fill=(33,71,83),width=1)
 track(im,'BIRTHDAY PROTOCOL   •   ANSH',1680,23,col)
 text(im,f'ARCHIVE 3000  /  {int(t):02d}:00',1740,21,col)
 d.line((140,1810,940,1810),fill=(31,56,67),width=3);d.line((140,1810,140+800*t/45,1810),fill=col,width=4)
 return im
scenes=[(5,12,'THE BOLLYWOOD','BUFF','Main character energy.','Every single day.',[6,7,8,0,12],GOLD),(12,19,'THE MARVEL','GEEK',"Earth’s Mightiest Fan.",'',[9,13,12,4,0],BLUE),(19,26,'THE BEST','DANCER','The dance floor? His kingdom.','',[6,3,10,7,8],RED),(26,33,'MY GOAT.','','UNMATCHED. UNDEFEATED.','IRREPLACEABLE.',[0,14,8,11,12],GOLD)]
def carousel(im,ids,u,col,speed=.38):
 center=(u*speed)%len(ids);poses=[]
 for k in range(-2,3):
  idx=(math.floor(center)+k)%len(ids);p=k-(center%1);poses.append((abs(p),p,idx))
 for _,p,idx in sorted(poses,reverse=True):
  scale=max(.40,1-abs(p)*.24);hh=int(850*scale);ww=int(628*scale*max(.63,1-abs(p)*.13));px=int(540+p*390-ww/2);py=int(690+(1-scale)*240)
  card=cards[ids[idx]].resize((ww,hh),Image.Resampling.BICUBIC)
  # Perspective tilts animate original photos without face synthesis.
  tilt=int(p*20);quad=(0,max(0,tilt),0,hh-min(0,tilt),ww,hh+min(0,tilt),ww,max(0,-tilt))
  card=card.transform((ww,hh),Image.Transform.QUAD,quad,Image.Resampling.BICUBIC)
  border=ImageOps.expand(card,border=3,fill=col)
  im.paste(border,(px-3,py-3)); reflection=ImageOps.flip(card).crop((0,0,ww,min(95,hh))).filter(ImageFilter.GaussianBlur(2)); reflection=Image.blend(Image.new('RGB',reflection.size,(8,17,25)),reflection,.13); im.paste(reflection,(px,py+hh+20));d=ImageDraw.Draw(im);d.line((px,py+hh+12,px+ww,py+hh+12),fill=col,width=2)
  if abs(p)<.5:text(im,f'MEMORY FILE / {ids[idx]+1:03d}',py+hh+23,18,col,x=max(80,px+12))
 return im

def frame(t):
 if t<5:
  im=bg(t);d=ImageDraw.Draw(im);p=min(1,t/.7);reactor(im,540,750,185,t,power=p)
  track(im,'J.A.R.V.I.S. ONLINE',325,38,BLUE)
  if t>1:text(im,'IDENTITY VERIFIED.',1130,35,BLUE,True)
  if t>1.8:text(im,'INITIATING BIRTHDAY',1210,44,WHITE,True);text(im,'PROTOCOL...',1270,44,GOLD,True)
  if t>2.7:helmet(im,540,1510,110)
  text(im,'A SURPRISE BUILT FOR A LEGEND',480,24,GOLD)
  if t<.5:im=Image.blend(Image.new('RGB',(W,H)),im,t/.5)
 elif t<33:
  a,b,h1,h2,s1,s2,ids,col=next(v for v in scenes if v[0]<=t<v[1]);u=t-a;im=bg(t, .8 if col==GOLD else 0)
  reactor(im,540,1030,430,t,col)
  track(im,f'0{scenes.index((a,b,h1,h2,s1,s2,ids,col))+1}   /   LEGEND PROFILE',230,21,col)
  text(im,h1,310,136 if not h2 else (91 if len(h1)<15 else 78),col,True)
  if h2:text(im,h2,405,114,WHITE,True)
  text(im,s1,555,34,WHITE);text(im,s2,601,30,col)
  carousel(im,ids,u,col,.48 if a==19 else .36)
  # Fine energy streaks at the beat, outside photo faces.
  d=ImageDraw.Draw(im)
  for j in range(5):
   yy=1550+j*13;xx=int((t*320+j*110)%1200)-100;d.line((xx,yy,xx+130,yy),fill=col,width=2)
 elif t<40:
  u=t-33;im=bg(t,1)
  ids=[1,5,3,11];ii=min(3,int(u/1.75));p=photos[ids[ii]]
  ww,hh=900,1040;photo=ImageOps.contain(p,(ww,hh),Image.Resampling.LANCZOS)
  panel=Image.new('RGB',(ww,hh),(8,17,25));panel.paste(photo,((ww-photo.width)//2,(hh-photo.height)//2)); transition=(u%1.75)/.38
  if ii>0 and transition<1:
   prev=ImageOps.contain(photos[ids[ii-1]],(ww,hh),Image.Resampling.LANCZOS); old=Image.new('RGB',(ww,hh),(8,17,25));old.paste(prev,((ww-prev.width)//2,(hh-prev.height)//2));panel=Image.blend(old,panel,transition)
  im.paste(panel,(90,610));d=ImageDraw.Draw(im);d.rectangle((83,603,997,1657),outline=GOLD,width=2)
  text(im,'MORE THAN MY BROTHER.',285,61,GOLD,True)
  if u>.7:text(im,'MY BESTEST FRIEND.',385,68,WHITE,True)
  if u>2.3:text(im,'MY FOREVER TEAMMATE.',485,48,GOLD,True)
 else:
  u=t-40;im=bg(t,1);reactor(im,540,1010,420,t,GOLD)
  # Ansh identity confirmed by the user against this restaurant portrait.
  p=photos[0];photo=ImageOps.contain(p,(630,760),Image.Resampling.LANCZOS);im.paste(photo,((W-photo.width)//2,670+(760-photo.height)//2))
  text(im,'HAPPY BIRTHDAY,',310,89,GOLD,True);text(im,'LEGEND!',405,136,WHITE,True)
  if u>.65:text(im,'LOVE YOU 3000.',1470,88,GOLD,True)
  if u>4.7:im=Image.blend(im,Image.new('RGB',(W,H)),min(1,(u-4.7)/.267))
 # Black-dip cuts make titles easy to read and establish scene boundaries.
 for boundary in [5,12,19,26,33,40]:
  dist=abs(t-boundary)
  if dist<.12:im=Image.blend(Image.new('RGB',(W,H)),im,.25+.75*dist/.12)
 return im

def audio():
 sr=48000;n=45*sr;tt=np.arange(n)/sr;L=np.zeros(n);R=np.zeros(n)
 rng=np.random.default_rng(42)
 def add(start,dur,freq,vol,kind='pad',pan=0):
  off=int(start*sr);length=min(int(dur*sr),n-off)
  if length<=0:return
  t=np.arange(length)/sr
  if kind=='pad':env=np.minimum(1,t/.4)*np.minimum(1,(dur-t)/.9);s=(np.sin(2*np.pi*freq*t)+.28*np.sin(2*np.pi*freq*2.003*t))*env
  elif kind=='bell':s=(np.sin(2*np.pi*freq*t)+.2*np.sin(2*np.pi*freq*3*t))*np.exp(-t*3.5)*np.minimum(1,t/.006)
  elif kind=='kick':s=np.sin(2*np.pi*(45*t+40*.035*(1-np.exp(-t/.035))))*np.exp(-t*13)
  else:s=rng.normal(0,1,length)*np.exp(-t*35)*np.minimum(1,t/.002)
  L[off:off+length]+=s*vol*(1-pan*.35);R[off:off+length]+=s*vol*(1+pan*.35)
 # Original score: E minor / C / G / D. No borrowed recording or melody.
 chords=[[164.81,196,246.94],[130.81,164.81,196],[146.83,196,246.94],[146.83,185,220]]
 for j,start in enumerate(np.arange(5,45,3.5)):
  for f in chords[j%4]:add(start,4.3,f,.032 if start<33 else .047)
  add(start,3.6,chords[j%4][0]/2,.065)
 for k,start in enumerate(np.arange(5,43.8,.4375)):
  energetic=19<=start<33;f=chords[int((start-5)/3.5)%4][k%3]*2
  add(start,1.4,f,.055 if start>=33 else .038,'bell',math.sin(k)*.7)
  if start<33:
   if k%2==0:add(start,.4,0,.19 if energetic else .12,'kick')
   add(start+.21875,.12,0,.022 if energetic else .011,'noise',(-1)**k)
   if energetic and k%2:add(start,.16,0,.05,'noise')
 for start in [0.2,.65,1.1,1.8,2.5,3.2,4.1]:add(start,.35,850+start*120,.035,'bell')
 for start in [5,12,19,26,33,40]:
  add(start,2,55,.16,'pad');add(start,.6,0,.11,'kick')
 fade=np.minimum(1,tt/.25)*np.minimum(1,(45-tt)/1.2);arr=np.stack([L*fade,R*fade],axis=1);arr=np.tanh(arr*1.8)*.83
 with wave.open('build/score.wav','wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((arr*32767).astype('<i2').tobytes())

if __name__=='__main__':
 if '--stills' in sys.argv:
  for t in [3,7,14,21,28,36,41.5]:frame(t).save(f'build/preview-{t}.jpg',quality=92)
 else:
  audio();exe=imageio_ffmpeg.get_ffmpeg_exe()
  cmd=[exe,'-y','-f','rawvideo','-vcodec','rawvideo','-s','1080x1920','-pix_fmt','rgb24','-r','30','-i','-','-i','build/score.wav','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-t','45','-movflags','+faststart',str(OUT/'Ansh_Birthday_Protocol.mp4')]
  with open('build/render.log','w') as log:
   proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
   for f in range(1350):
    proc.stdin.write(frame(f/30).tobytes())
    if f%150==0:print(f'{f}/1350 frames',flush=True)
   proc.stdin.close();rc=proc.wait()
   if rc:raise RuntimeError(f'Encoder failed: {rc}')
  print('RENDER COMPLETE',flush=True)
