import sys,subprocess
from pathlib import Path
sys.path.insert(0,str(Path('build/vendor').resolve()))
import imageio_ffmpeg
exe=imageio_ffmpeg.get_ffmpeg_exe()
cmd=[exe,'-y','-i','output/Ansh_Birthday_Protocol.mp4','-i','source/The Avengers - Alan Silvestri.mp3','-i','build/score.wav','-filter_complex',"[1:a]atrim=78:123,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.3,afade=t=out:st=44.5:d=0.5,volume=0.85[music];[2:a]atrim=0:4.8,asetpts=PTS-STARTPTS,afade=t=out:st=4:d=0.8,volume=0.55[fx];[music][fx]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",'-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','256k','-t','45','-movflags','+faststart','app/public/media/Ansh_Birthday_Protocol.mp4']
subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=open('build/audio-mix.log','w'))
print('Avengers soundtrack mixed into final video.')
