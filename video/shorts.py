# Monta os 3 Shorts (1080x1920) a partir do vídeo longo renderizado e da mixagem.
import json, re, unicodedata, subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont

T = json.load(open('build/timeline.json'))
W = T['words']
def norm(w): return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', w.lower()).encode('ascii', 'ignore').decode())
for w in W: w['n'] = norm(w['w'])

def span(c, a, b):
    ws = [w for w in W if w['c'] == c]
    def idx(ph, start=0):
        t = [norm(x) for x in ph.split() if norm(x)]
        for i in range(start, len(ws) - len(t) + 1):
            if all(ws[i + k]['n'] == t[k] for k in range(len(t))): return i, i + len(t) - 1
        raise SystemExit(f'não achei {ph}')
    i, _ = idx(a); _, j = idx(b, i)
    return ws[i]['s'] - 0.25, ws[j]['e'] + 0.45

SHORTS = [
    dict(slug='short1-lanchonete-do-governo', title=['O GOVERNO QUEBROU', 'A VARIG SEM QUERER?'],
         parts=[(5, 'O primeiro golpe', 'décadas para terminar'), (8, 'Em 2014 o Supremo', 'massa falida')]),
    dict(slug='short2-quem-mandava-na-varig', title=['QUEM MANDAVA', 'NA VARIG?'],
         parts=[(2, 'Só que o mais importante', 'final da história'), (6, 'E é aqui que aquela fundação', 'quando o jogo mudou')]),
    dict(slug='short3-o-que-sobrou-da-varig', title=['A ÚNICA PARTE DA VARIG', 'QUE AINDA FUNCIONA'],
         parts=[(0, 'Durante décadas', 'decretou a falência'), (8, 'E tem uma última coisa', 'parou de funcionar')]),
]

def title_png(lines, path):
    im = Image.new('RGBA', (1080, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype('assets/fonts/anton-latin-400-normal.ttf', 104)
    y = 90
    for k, ln in enumerate(lines):
        while d.textlength(ln, font=f) > 1000: f = ImageFont.truetype('assets/fonts/anton-latin-400-normal.ttf', f.size - 4)
    for k, ln in enumerate(lines):
        w = d.textlength(ln, font=f)
        d.text(((1080 - w) / 2, y), ln, font=f, fill=(255, 210, 63) if k == len(lines) - 1 else (255, 255, 255), stroke_width=10, stroke_fill=(17, 17, 17))
        y += f.size + 30
    im.save(path)

os.makedirs('shorts', exist_ok=True)
src = sys.argv[1] if len(sys.argv) > 1 else 'final/varig-longo.mp4'
for s in SHORTS:
    rng = [span(*p) for p in s['parts']]
    title_png(s['title'], f'shorts/{s["slug"]}-titulo.png')
    fc = []; n = len(rng)
    for i, (a, b) in enumerate(rng):
        fc.append(f'[{i}:v]setpts=PTS-STARTPTS,fps=30[v{i}]')
        fc.append(f'[{i}:a]asetpts=PTS-STARTPTS,afade=t=in:d=0.08,afade=t=out:st={b-a-0.12:.3f}:d=0.12[a{i}]')
    fc.append(''.join(f'[v{i}][a{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=1[cv][ca]')
    # 9:16: fundo borrado + quadro central recortado (mantém o miolo do 16:9)
    fc.append('[cv]split[c1][c2]')
    fc.append('[c1]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.08[bg]')
    fc.append('[c2]scale=1460:-2,crop=1080:ih[fg]')
    fc.append('[bg][fg]overlay=0:(H-h)/2+90[vv]')
    fc.append(f'[vv][{n}:v]overlay=0:150[vt]')
    fc.append('[ca]loudnorm=I=-14:TP=-1.5:LRA=11[aa]')
    out = f'shorts/{s["slug"]}.mp4'
    ins = []
    for a, b in rng: ins += ['-ss', f'{a:.3f}', '-t', f'{b-a:.3f}', '-i', src]
    cmd = ['ffmpeg', '-y', '-v', 'error'] + ins + ['-i', f'shorts/{s["slug"]}-titulo.png', '-filter_complex', ';'.join(fc),
           '-map', '[vt]', '-map', '[aa]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout)
    print(out, f'{dur:.1f}s', [f'{a:.1f}-{b:.1f}' for a, b in rng])
