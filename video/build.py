# Gera os projetos HyperFrames (um por capítulo) + eventos de som, a partir do words.json.
import json, re, os, sys, unicodedata, shutil
import props as P
from cenas import SHOTS, CHAPTER_TITLES, PHASES, MUTES

FPS = 30
GAP = 1.4        # cartela de capítulo entre capítulos
LEAD = 2 / FPS   # visual chega 2 quadros antes da palavra
TAIL = 0.5

W = json.load(open('words.json'))['words']
NCAP = 9
capdur = []
for c in range(NCAP):
    import subprocess
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'voz/cap{c}.mp3'], capture_output=True, text=True).stdout)
    capdur.append(d)
# offset de cada capítulo no áudio sem pausas (usado pelo align) e no filme final
raw_off = [sum(capdur[:c]) for c in range(NCAP)]
film_off = []
t = 0.0
for c in range(NCAP):
    if c > 0: t += GAP
    film_off.append(t); t += capdur[c]
TOTAL = t + TAIL

def norm(w):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', w.lower()).encode('ascii', 'ignore').decode())

CAPW = {c: [dict(w, n=norm(w['w']), fs=w['s'] - raw_off[c] + film_off[c], fe=w['e'] - raw_off[c] + film_off[c]) for w in W if w['cap'] == c] for c in range(NCAP)}

def find(c, phrase, start=0):
    toks = [norm(x) for x in phrase.split() if norm(x)]
    ws = CAPW[c]
    for i in range(start, len(ws) - len(toks) + 1):
        if all(ws[i + k]['n'] == toks[k] for k in range(len(toks))):
            return i
    raise SystemExit(f'cue não achada no cap {c}: "{phrase}" a partir de {start} ({ws[start]["w"] if start < len(ws) else "fim"})')

def cue_time(c, cue, base_idx, base_t):
    """cue: None -> base_t; número -> base_t + n; '+frase' ou 'frase' -> tempo da palavra."""
    if cue is None: return base_t, base_idx
    if isinstance(cue, (int, float)): return base_t + cue, base_idx
    m = re.match(r'^(.*?)(@([+-]?[0-9.]+))?$', cue)
    phrase, adj = m.group(1), float(m.group(3) or 0)
    nth = 0
    if '#' in phrase:
        phrase, nth = phrase.split('#'); nth = int(nth)
    end = phrase.endswith('$')
    phrase = phrase.rstrip('$').strip()
    i = find(c, phrase, base_idx)
    if nth:
        return CAPW[c][i + nth]['fs'] - LEAD + adj, i
    if end:
        j = i + len([x for x in phrase.split() if norm(x)]) - 1
        return CAPW[c][j]['fe'] + adj, i
    return CAPW[c][i]['fs'] - LEAD + adj, i

items, shots_cam, impacts, sfx, phases, used_imgs = [], [], [], [], [], set()
nid = [0]

def add_item(spec, t0, t1, c, base_idx):
    nid[0] += 1
    it = dict(spec)
    it['id'] = f'i{nid[0]}'
    html_ = it.pop('html')
    if 'at' in it:
        t0, _ = cue_time(c, it.pop('at'), base_idx, t0)
    if 'until' in it:
        t1, _ = cue_time(c, it.pop('until'), base_idx, t0)
    if 'dur' in it:
        t1 = t0 + it.pop('dur')
    it['t0'] = round(t0, 3); it['t1'] = round(t1, 3)
    subs = []
    for s in it.pop('subs', []):
        s = dict(s)
        st, _ = cue_time(c, s.pop('at', None), base_idx, t0)
        s['t'] = round(st - t0, 3)
        n_ = s.pop('sfx', None); v_ = s.pop('vol', 1.0)
        if n_: sfx.append(dict(t=st, n=n_, v=v_))
        subs.append(s)
    it['subs'] = subs
    moves = []
    for m in it.pop('moves', []):
        m = dict(m); mt, _ = cue_time(c, m.pop('at', None), base_idx, t0); m['t'] = round(mt - t0, 3)
        if 'sfx' in m: sfx.append(dict(t=mt, n=m.pop('sfx'), v=m.pop('vol', 1.0)))
        moves.append(m)
    it['moves'] = moves
    if 'sfx' in it:
        s = it.pop('sfx');
        for n in (s if isinstance(s, list) else [s]):
            sfx.append(dict(t=t0 + (it.get('enter', {}).get('d', 0) * 0 if True else 0), n=n, v=it.pop('vol', 1.0) if 'vol' in it else 1.0))
    if 'impact' in it:
        k = it.pop('impact'); impacts.append(dict(t=round(t0 + (0.1 if it.get('enter', {}).get('k') == 'slam' else 0), 3), k=k, v=it.pop('iv', None) or (16 if k == 'shake' else 0.05)))
    for m in re.findall(r'(?:img|blur)/([a-z0-9_]+)\.jpg', html_):
        used_imgs.add(m)
    it['html'] = html_
    items.append(it)
    return it

for c in range(NCAP):
    shots = SHOTS[c]
    cs = film_off[c]
    # cartela de capítulo
    if c > 0 and CHAPTER_TITLES.get(c):
        tt, sub = CHAPTER_TITLES[c]
        t0 = cs - GAP
        add_item(dict(html=P.chapter(tt, sub), x=960, y=520, enter=dict(k='cut'), step=True, jit=True), t0, cs, c, 0)
        shots_cam.append(dict(t0=t0, t1=cs, rate=0.02, s0=1.0))
        sfx.append(dict(t=t0, n='paper', v=1.0)); sfx.append(dict(t=t0 + 0.05, n='thud', v=0.6))
    idx = 0
    prev_t = cs
    resolved = []
    for si, sh in enumerate(shots):
        t0, idx = cue_time(c, sh['cue'], idx, cs) if sh.get('cue') is not None else (cs, idx)
        if si == 0: t0 = cs if c > 0 else 0.0
        resolved.append((t0, idx, sh))
    for si, (t0, idx, sh) in enumerate(resolved):
        t1 = resolved[si + 1][0] if si + 1 < len(resolved) else (film_off[c + 1] - GAP if c + 1 < NCAP else TOTAL)
        if c == NCAP - 1 and si == len(resolved) - 1:
            t1 = CAPW[c][-1]['fe'] + 0.02  # corte seco para preto na última palavra
        cam = dict(t0=round(t0, 3), t1=round(t1, 3), rate=sh.get('rate', 0.012), s0=sh.get('s0', 1.0))
        for k in ('fx', 'fy', 'pan'):
            if k in sh: cam[k] = sh[k]
        shots_cam.append(cam)
        for it in sh['items']:
            add_item(it, t0, t1, c, idx)
        for (cue, name, *v) in sh.get('sfx', []):
            st, _ = cue_time(c, cue, idx, t0); sfx.append(dict(t=st, n=name, v=v[0] if v else 1.0))
        for (cue, k, *v) in sh.get('impacts', []):
            st, _ = cue_time(c, cue, idx, t0); impacts.append(dict(t=round(st, 3), k=k, v=v[0] if v else (16 if k == 'shake' else 0.05)))
    for (cue, ph, *d) in PHASES.get(c, []):
        if cue == 'CARD': st = cs - GAP
        else: st, _ = cue_time(c, cue, 0, cs)
        phases.append(dict(t=round(st, 3), p=ph, d=d[0] if d else 0.27))
if TOTAL > 0:
    phases.append(dict(t=round(CAPW[NCAP - 1][-1]['fe'] + 0.02, 3), p='preto', d=0.0))
phases.sort(key=lambda p: p['t'])
if not phases or phases[0]['t'] > 0: phases.insert(0, dict(t=0, p='auge', d=0))

CSS = open('estilo.css').read()

def page(offset, dur, its, w=1920, h=1080):
    data = dict(offset=round(offset, 3), dur=round(dur, 3), fps=FPS,
                items=[{k: v for k, v in i.items() if k != 'html'} for i in its],
                cam=dict(shots=shots_cam, impacts=impacts, phases=phases))
    body = '\n'.join(f'<div class="it" id="{i["id"]}" style="z-index:{i.get("z", 10)};display:none">{i["html"]}</div>' for i in its)
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width={w}, height={h}">
<script src="gsap.min.js"></script><style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur:.3f}" data-width="{w}" data-height="{h}">
<div id="frame" class="clip" data-start="0" data-duration="{dur:.3f}">
<div id="grade"><div id="cam"><div id="paperbg"></div>
{body}
</div><div id="warm"></div><div id="cold"></div></div>
<div id="vig"></div><div id="grainl"></div><div id="dark"></div>
</div></div>
<script>window.__SCENE={json.dumps(data, ensure_ascii=False)};</script>
<script src="engine.js"></script>
</body></html>'''

def project(dirn, offset, dur, its):
    os.makedirs(dirn, exist_ok=True)
    for f in ['img', 'blur', 'fonts']:
        if not os.path.exists(f'{dirn}/{f}'): os.symlink(os.path.abspath(f'assets/{f}'), f'{dirn}/{f}')
    for f in ['paper.jpg', 'gsap.min.js'] + [f'grain{i}.png' for i in range(4)]:
        shutil.copy(f'assets/{f}', f'{dirn}/{f}')
    shutil.copy('engine.js', f'{dirn}/engine.js')
    open(f'{dirn}/index.html', 'w').write(page(offset, dur, its))
    json.dump({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json", "paths": {"assets": "assets"}}, open(f'{dirn}/hyperframes.json', 'w'))
    json.dump({"id": os.path.basename(dirn), "name": os.path.basename(dirn)}, open(f'{dirn}/meta.json', 'w'))

os.makedirs('build', exist_ok=True)
segs = []
for c in range(NCAP):
    a = film_off[c] - (GAP if c > 0 else 0)
    b = film_off[c + 1] - GAP if c + 1 < NCAP else TOTAL
    its = [i for i in items if i['t1'] > a and i['t0'] < b]
    project(f'build/cap{c}', a, b - a, its)
    segs.append(dict(c=c, a=round(a, 3), b=round(b, 3)))
mutes = []
for (c, cue, d) in MUTES:
    st, _ = cue_time(c, cue, 0, film_off[c]); mutes.append([round(st, 3), round(st + d, 3)])
json.dump(dict(mute=mutes, end=round(CAPW[NCAP - 1][-1]['fe'] + 0.02, 3), total=TOTAL, film_off=film_off, capdur=capdur, segs=segs, sfx=sorted(sfx, key=lambda s: s['t']), phases=phases,
               words=[dict(w=w['w'], s=round(w['fs'], 3), e=round(w['fe'], 3), c=c) for c in range(NCAP) for w in CAPW[c]]),
          open('build/timeline.json', 'w'), ensure_ascii=False)
cred = json.load(open('assets/credits.json'))
json.dump({k: cred[k] for k in sorted(used_imgs) if k in cred}, open('build/credits.json', 'w'), ensure_ascii=False, indent=1)
print(f'total {TOTAL:.1f}s, itens {len(items)}, sfx {len(sfx)}, imagens {len(used_imgs)}')
