#!/bin/bash
# snapshots no meio de cada cena de cada capítulo -> contact sheets em qa/
cd /home/user/varig
mkdir -p qa
for c in "$@"; do
  T=$(python3 -c "
import json,re
s=open('build/cap$c/index.html').read()
d=json.loads(re.search(r'window.__SCENE=(\{.*?\});</script>',s,re.S).group(1))
off=d['offset'];dur=d['dur']
ts=sorted(set(round(min(dur-0.05,max(0.05,(sh['t0']+min(sh['t1'],sh['t0']+6))/2+0.6-off)),2) for sh in d['cam']['shots'] if sh['t1']>off and sh['t0']<off+dur))
print(','.join(map(str,ts)))")
  (cd build/cap$c && /home/user/hf/node_modules/.bin/hyperframes snapshot --at $T > /tmp/snap$c.log 2>&1)
  d=$(ls -td build/cap$c/.hyperframes/artifacts/snapshots/*/ | head -1)
  python3 - "$d" "$c" <<'PY'
import sys,glob
from PIL import Image,ImageDraw
d,c=sys.argv[1],sys.argv[2]
fs=sorted(glob.glob(d+'frame-*.png'))
W,H=640,360;cols=4;rows=(len(fs)+cols-1)//cols
sh=Image.new('RGB',(W*cols,(H+24)*rows),'black');dr=ImageDraw.Draw(sh)
for i,f in enumerate(fs):
    im=Image.open(f).convert('RGB').resize((W,H));x=(i%cols)*W;y=(i//cols)*(H+24)
    sh.paste(im,(x,y+24));dr.text((x+6,y+4),f.split('-at-')[1],fill='white')
sh.save(f'qa/cap{c}.jpg',quality=78)
PY
done
