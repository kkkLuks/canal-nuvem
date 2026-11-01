# Recortes de papel em SVG/HTML. Cada função devolve (html, largura_px).
import math, json, html as H

BLUE = '#1d3f8f'; GOLD = '#e5b33a'; RED = '#c8202e'; INK = '#222'; CREAM = '#f3ead6'
ORANGE = '#ff6a13'; GREEN = '#1f8a4c'; YEL = '#ffd23f'

_uid = [0]
def uid(p='u'):
    _uid[0] += 1
    return f'{p}{_uid[0]}'

def cutsvg(vb, body, w, extra=''):
    """SVG com contorno branco de recorte: o mesmo desenho duas vezes (contorno grosso branco embaixo)."""
    return (f'<svg viewBox="{vb}" width="{w}" {extra} xmlns="http://www.w3.org/2000/svg" style="overflow:visible">'
            f'<g class="ol">{body}</g><g>{body}</g></svg>')

def rose(cx, cy, r, fill=BLUE, star='#fff', ring=True):
    pts = []
    for i in range(16):
        a = -math.pi / 2 + i * math.pi / 8
        rr = r * (0.92 if i % 4 == 0 else (0.5 if i % 2 == 0 else 0.26))
        pts.append(f'{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}')
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2"/>' if ring else ''
    return s + f'<polygon points="{" ".join(pts)}" fill="{star}"/>'

def gstar(cx, cy, r, fill=GOLD):
    pts = []
    for i in range(16):
        a = -math.pi / 2 + i * math.pi / 8
        rr = r * (1 if i % 4 == 0 else (0.55 if i % 2 == 0 else 0.3))
        pts.append(f'{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'

LIV = {
    'varig': dict(body='#fbfbf7', stripe=BLUE, tail=BLUE, mark='rose', name='VARIG', namec=BLUE),
    'varig96': dict(body='#fbfbf7', stripe=None, tail='#18346f', mark='star', name='VARIG', namec='#18346f'),
    'blank': dict(body='#e9e6de', stripe='#9a9a9a', tail='#9a9a9a', mark=None, name='', namec=INK),
    'gol': dict(body='#fbfbf7', stripe=None, tail=ORANGE, mark=None, name='', namec=ORANGE),
    'tam': dict(body='#fbfbf7', stripe=RED, tail=RED, mark=None, name='', namec=RED),
    'copa': dict(body='#fbfbf7', stripe=GREEN, tail=YEL, mark='ball', name='VARIG', namec=GREEN),
    'log': dict(body='#fbfbf7', stripe=GOLD, tail='#18346f', mark='star', name='VARIGLOG', namec='#18346f'),
}

def plane(kind='jet', liv='varig', w=520, flip=False):
    L = LIV[liv]; b = []
    fl = ' transform="translate(600,0) scale(-1,1)"' if flip else ''
    names = []
    if kind in ('jet', 'jumbo', 'tri'):
        b.append(f'<path d="M58,84 L22,12 L66,12 L132,84Z" fill="{L["tail"]}" stroke="{INK}" stroke-width="2"/>')
        b.append(f'<path d="M40,100 C40,82 60,80 90,80 L520,80 C556,80 582,92 592,100 C582,110 556,122 520,122 L90,122 C60,122 40,118 40,100Z" fill="{L["body"]}" stroke="{INK}" stroke-width="2"/>')
        if kind == 'jumbo':
            b.append(f'<path d="M400,82 C420,58 500,56 548,84Z" fill="{L["body"]}" stroke="{INK}" stroke-width="2"/>')
        if kind == 'tri':
            b.append(f'<path d="M30,60 L120,60 C130,60 134,66 130,72 L36,76Z" fill="#cfcfcf" stroke="{INK}" stroke-width="2"/>')
        b.append(f'<path d="M36,100 L6,114 L76,108Z" fill="{L["tail"]}" stroke="{INK}" stroke-width="2"/>')
        if L['stripe']:
            b.append(f'<path d="M70,98 L570,98 L580,104 L70,106Z" fill="{L["stripe"]}"/>')
        b.append(''.join(f'<circle cx="{x}" cy="91" r="3.2" fill="#3a4a66"/>' for x in range(120, 520, 16)))
        b.append(f'<path d="M560,88 L578,92 L566,96Z" fill="#3a4a66"/>')
        b.append(f'<path d="M250,108 L196,170 L240,170 L340,108Z" fill="#d8d8d8" stroke="{INK}" stroke-width="2"/>')
        b.append(f'<ellipse cx="232" cy="142" rx="26" ry="10" fill="#bdbdbd" stroke="{INK}" stroke-width="2"/>')
        if kind == 'jumbo':
            b.append(f'<ellipse cx="270" cy="150" rx="22" ry="9" fill="#bdbdbd" stroke="{INK}" stroke-width="2"/>')
        if L['name']:
            names.append(f'<text x="300" y="78" font-family="Anton" font-size="30" letter-spacing="6" fill="{L["namec"]}" text-anchor="middle">{L["name"]}</text>' if kind != 'jumbo' else
                     f'<text x="300" y="76" font-family="Anton" font-size="28" letter-spacing="6" fill="{L["namec"]}" text-anchor="middle">{L["name"]}</text>')
        if L['mark'] == 'rose':
            b.append(rose(58, 46, 17, fill=L['tail'], star='#fff', ring=False))
        elif L['mark'] == 'star':
            b.append(gstar(56, 46, 18))
        elif L['mark'] == 'ball':
            b.append(f'<circle cx="54" cy="46" r="15" fill="#fff" stroke="{INK}" stroke-width="2"/><path d="M54,36 L63,43 L60,54 L48,54 L45,43Z" fill="{INK}"/>')
        vb = '0 0 600 190'
    elif kind == 'sea':  # hidroavião (Dornier Wal)
        b.append(f'<path d="M60,130 C60,112 90,108 130,108 L470,108 C520,108 560,120 575,138 L540,150 L120,150 C80,150 60,145 60,130Z" fill="#c9c1ad" stroke="{INK}" stroke-width="2"/>')
        b.append(f'<path d="M70,112 L40,58 L82,58 L130,112Z" fill="#b8ad93" stroke="{INK}" stroke-width="2"/>')
        b.append(f'<rect x="150" y="40" width="330" height="16" rx="6" fill="#d9d2c0" stroke="{INK}" stroke-width="2"/>')
        b.append(f'<path d="M280,56 L270,108 M360,56 L370,108" stroke="{INK}" stroke-width="4"/>')
        b.append(f'<rect x="270" y="18" width="110" height="24" rx="10" fill="#8f8a7c" stroke="{INK}" stroke-width="2"/>')
        b.append(f'<ellipse cx="262" cy="30" rx="4" ry="30" fill="#555" opacity=".8"/><ellipse cx="388" cy="30" rx="4" ry="30" fill="#555" opacity=".8"/>')
        b.append(''.join(f'<rect x="{x}" y="118" width="12" height="10" fill="#3a4a66"/>' for x in range(200, 460, 26)))
        b.append(f'<path d="M100,150 C200,170 440,170 560,150" fill="none" stroke="#4a78a8" stroke-width="5" opacity=".6"/>')
        vb = '0 0 600 190'
    elif kind in ('prop', 'dc3'):
        big = kind == 'dc3'
        body = L['body'] if big else '#cfcabc'
        b.append(f'<path d="M70,92 L40,30 L82,30 L130,92Z" fill="{L["tail"] if big else "#a59f8c"}" stroke="{INK}" stroke-width="2"/>')
        b.append(f'<path d="M50,104 C50,90 70,86 100,86 L460,86 C500,86 520,96 528,106 C520,116 500,124 460,124 L100,124 C70,124 50,118 50,104Z" fill="{body}" stroke="{INK}" stroke-width="2"/>')
        b.append(f'<path d="M48,104 L16,116 L82,112Z" fill="{L["tail"] if big else "#a59f8c"}" stroke="{INK}" stroke-width="2"/>')
        if big and L['stripe']:
            b.append(f'<path d="M80,102 L510,102 L516,108 L80,110Z" fill="{L["stripe"]}"/>')
        b.append(''.join(f'<rect x="{x}" y="94" width="10" height="8" rx="2" fill="#3a4a66"/>' for x in range(150, 440, 22)))
        b.append(f'<path d="M300,112 L270,150 L360,150 L380,112Z" fill="#d8d8d8" stroke="{INK}" stroke-width="2"/>')
        b.append(f'<rect x="{"300" if big else "500"}" y="{"118" if big else "94"}" width="{"60" if big else "30"}" height="{"18" if big else "24"}" rx="8" fill="#9a9a9a" stroke="{INK}" stroke-width="2"/>')
        b.append(f'<g class="wheel"><circle cx="{"330" if big else "430"}" cy="168" r="14" fill="#333"/><circle cx="{"330" if big else "430"}" cy="168" r="5" fill="#ddd"/></g>')
        b.append(f'<path d="M{"330" if big else "430"},124 L{"330" if big else "430"},156" stroke="{INK}" stroke-width="5"/>')
        b.append(f'<ellipse class="prop" cx="{"366" if big else "534"}" cy="{"127" if big else "106"}" rx="5" ry="40" fill="#555" opacity=".75"/>')
        if big and L['mark'] == 'rose':
            b.append(f'<circle cx="64" cy="58" r="14" fill="#fff"/>' + rose(64, 58, 12, fill=BLUE, ring=False))
        vb = '0 0 600 190'
    body = ''.join(b)
    if flip:
        body = f'<g transform="translate(600,0) scale(-1,1)">{body}</g>'
    return cutsvg(vb, body + ''.join(names), w)

def photo(key, w=900, cap=None, tape=True, bw=False):
    tp = ''
    if tape:
        tp = ('<div class="tape" style="left:-30px;top:-14px;transform:rotate(-28deg)"></div>'
              '<div class="tape" style="right:-30px;top:-14px;transform:rotate(26deg)"></div>')
    cp = f'<div class="pcap">{H.escape(cap)}</div>' if cap else ''
    flt = ' style="filter:grayscale(1) contrast(1.05)"' if bw else ''
    return f'<div class="photo" style="width:{w}px"><div class="pin"><img class="kb" src="img/{key}.jpg"{flt}></div>{cp}{tp}</div>'

def full(key):
    return (f'<div class="full"><img class="fbg" src="blur/{key}.jpg"><div class="ffr"><img class="kb" src="img/{key}.jpg"></div></div>')

def stat(txt, size=150, yellow=False, font='Anton'):
    return f'<div class="stat{" yel" if yellow else ""}" style="font-size:{size}px;font-family:{font}">{H.escape(txt)}</div>'

def label(txt, size=46, rot=0, bg='#fffdf4', color=INK, font='Special Elite'):
    return f'<div class="label" style="font-size:{size}px;background:{bg};color:{color};font-family:\'{font}\'">{H.escape(txt)}</div>'

def stamp(txt, size=120, color=RED, sub=None):
    s = f'<div class="ssub">{H.escape(sub)}</div>' if sub else ''
    return f'<div class="stamp" style="font-size:{size}px;color:{color};border-color:{color}">{H.escape(txt)}{s}</div>'

def headline(title, sub='', paper='JORNAL', date=''):
    return (f'<div class="news"><div class="nmast">{H.escape(paper)}<span>{H.escape(date)}</span></div>'
            f'<div class="nt">{H.escape(title)}</div><div class="ns">{H.escape(sub)}</div>'
            '<div class="ncol"></div><div class="ncol"></div><div class="ncol"></div></div>')

def typew(txt, size=54):
    return f'<div class="label tw-wrap" style="font-size:{size}px"><span class="tw" data-full="{H.escape(txt)}"></span></div>'

def chapter(title, sub=''):
    import random
    rnd = random.Random(title)
    cols = ['#fffdf4', '#f6d36b', '#e9e2cf', '#ffffff', '#c9dbf0', '#f4c7b8']
    fonts = ['Anton', 'Special Elite', 'Oswald', 'Permanent Marker']
    ls = []
    fs = int(min(190, 1650 / max(1, len(title)) * 1.25))
    for i, ch in enumerate(title):
        if ch == ' ':
            ls.append('<span class="cl sp"></span>'); continue
        ls.append(f'<span class="cl" style="font-size:{fs}px;background:{rnd.choice(cols)};font-family:\'{rnd.choice(fonts)}\';transform:rotate({rnd.uniform(-7,7):.1f}deg) translateY({rnd.uniform(-8,8):.0f}px)">{H.escape(ch)}</span>')
    s = f'<div class="csub">{H.escape(sub)}</div>' if sub else ''
    return f'<div class="chap">{"".join(ls)}{s}</div>'

def letters(word, size=200):
    import random
    rnd = random.Random(word)
    out = []
    for i, ch in enumerate(word):
        out.append(f'<span class="l{i}" style="display:inline-block"><span class="cl big" style="font-size:{size}px;background:{["#fffdf4", "#c9dbf0", "#f6d36b", "#ffffff", "#e9e2cf"][i % 5]};transform:rotate({rnd.uniform(-8,8):.1f}deg)">{ch}</span></span>')
    return f'<div class="chap">{"".join(out)}</div>'

def pie(pct, label_txt, w=520, color=RED, people=False):
    a = 2 * math.pi * pct / 100
    x = 250 + 200 * math.sin(a); y = 250 - 200 * math.cos(a)
    large = 1 if pct > 50 else 0
    mid = a / 2
    ox, oy = 26 * math.sin(mid), -26 * math.cos(mid)
    body = f'<circle cx="250" cy="250" r="200" fill="#e9e2cf" stroke="{INK}" stroke-width="3"/>'
    body += f'<g class="slice"><path d="M{250+ox:.1f},{250+oy:.1f} L{250+ox:.1f},{50+oy:.1f} A200,200 0 {large},1 {x+ox:.1f},{y+oy:.1f} Z" fill="{color}" stroke="{INK}" stroke-width="3"/></g>'
    lab = f'<text x="{250+120*math.sin(mid)+ox:.0f}" y="{250-120*math.cos(mid)+oy+16:.0f}" font-family="Anton" font-size="48" fill="#fff" text-anchor="middle" stroke="{INK}" stroke-width="5" paint-order="stroke">{pct}%</text>'
    if people:
        body = f'<circle cx="250" cy="250" r="200" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>'
        ppl = ''
        k = 0
        for r_, n in [(150, 14), (95, 9), (40, 3)]:
            for i in range(n):
                aa = 2 * math.pi * i / n + r_
                px, py = 250 + r_ * math.sin(aa), 250 - r_ * math.cos(aa)
                ppl += f'<g class="pp" style="opacity:1"><circle cx="{px:.0f}" cy="{py-14:.0f}" r="9" fill="#fff"/><path d="M{px-12:.0f},{py+14:.0f} Q{px:.0f},{py-12:.0f} {px+12:.0f},{py+14:.0f}Z" fill="#fff"/></g>'
                k += 1
        body += ppl; lab = ''
    return cutsvg('0 0 500 500', body + lab, w) + (f'<div class="pielab">{H.escape(label_txt)}</div>' if label_txt else '')

def person(color=BLUE, w=70):
    body = f'<circle cx="50" cy="28" r="20" fill="{color}" stroke="{INK}" stroke-width="2"/><path d="M18,140 L22,70 Q50,48 78,70 L82,140Z" fill="{color}" stroke="{INK}" stroke-width="2"/>'
    return cutsvg('0 0 100 150', body, w)

def dominoes(n=14, w=1500):
    sp = 1500 / n
    body = ''
    for i in range(n):
        x = 40 + i * sp
        body += (f'<g class="dm d{i}"><circle cx="{x+30:.0f}" cy="60" r="20" fill="{BLUE}" stroke="{INK}" stroke-width="2"/>'
                 f'<path d="M{x:.0f},190 L{x+4:.0f},100 Q{x+30:.0f},80 {x+56:.0f},100 L{x+60:.0f},190Z" fill="{BLUE}" stroke="{INK}" stroke-width="2"/></g>')
    return cutsvg('0 0 1560 200', body, w)

def globe(w=820, routes=True):
    M = json.load(open('assets/maps.json'))['globe']
    body = f'<path d="{M["sphere"]}" fill="#bcd3e6" stroke="{INK}" stroke-width="3"/>'
    body += f'<path d="{M["grat"]}" fill="none" stroke="#8fb0cc" stroke-width="1"/>'
    body += ''.join(f'<path d="{p}" fill="#efe3c4" stroke="#7a6f58" stroke-width="1"/>' for p in M['paths'])
    if routes:
        for i, (k, d) in enumerate(M['routes'].items()):
            if d:
                body += f'<path class="rt r{i}" d="{d}" fill="none" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>'
        for i, (k, c) in enumerate(M['cities'].items()):
            if c and k in M['routes']:
                body += f'<circle class="cd" cx="{c[0]:.0f}" cy="{c[1]:.0f}" r="6" fill="{RED}" stroke="#fff" stroke-width="2"/>'
        rj = M['cities']['Rio de Janeiro']
        body += f'<circle cx="{rj[0]:.0f}" cy="{rj[1]:.0f}" r="10" fill="{YEL}" stroke="{INK}" stroke-width="3"/>'
    # cópia apagada só com pontos do Brasil (para "sobram poucos pontos")
    return cutsvg('0 0 1000 1000', body, w)

def south_map(w=900, extra='', mvd=False):
    M = json.load(open('assets/maps.json'))['south']
    body = '<rect x="-20" y="-20" width="1040" height="1040" fill="#bcd3e6"/>'
    for p in M['paths']:
        body += f'<path d="{p["d"]}" fill="{"#efe3c4" if p["id"]=="Brazil" else "#e2d8bd"}" stroke="#7a6f58" stroke-width="2"/>'
    C = M['cities']
    # Lagoa dos Patos (aproximação desenhada)
    poa, pel, rg = C['Porto Alegre'], C['Pelotas'], C['Rio Grande']
    lag = f'M{poa[0]+10:.0f},{poa[1]+30:.0f} C{poa[0]+90:.0f},{poa[1]+120:.0f} {rg[0]+60:.0f},{rg[1]-160:.0f} {rg[0]+10:.0f},{rg[1]-10:.0f} C{pel[0]+60:.0f},{pel[1]-40:.0f} {poa[0]+20:.0f},{poa[1]+150:.0f} {poa[0]-10:.0f},{poa[1]+40:.0f}Z'
    body += f'<path class="lagoa" d="{lag}" fill="#9fc0dc" stroke="#5f86a8" stroke-width="2"/>'
    route = f'M{poa[0]:.0f},{poa[1]:.0f} Q{poa[0]+70:.0f},{(poa[1]+rg[1])/2:.0f} {pel[0]:.0f},{pel[1]:.0f} L{rg[0]:.0f},{rg[1]:.0f}'
    body += f'<path class="rtlagoa" d="{route}" fill="none" stroke="{RED}" stroke-width="6" stroke-dasharray="1 0" stroke-linecap="round"/>'
    mv = C['Montevidéu']
    if mvd: body += f'<path class="rtmvd" d="M{poa[0]:.0f},{poa[1]:.0f} Q{(poa[0]+mv[0])/2-120:.0f},{(poa[1]+mv[1])/2:.0f} {mv[0]:.0f},{mv[1]:.0f}" fill="none" stroke="{RED}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1 0"/>'
    for name in ['Porto Alegre', 'Pelotas', 'Rio Grande', 'Montevidéu']:
        x, y = C[name]
        cls = 'cmvd' if name == 'Montevidéu' else 'cpoa'
        if name == 'Montevidéu' and not mvd: continue
        body += f'<g class="{cls}"><circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{RED}" stroke="#fff" stroke-width="3"/><text x="{x+16:.0f}" y="{y+8:.0f}" font-family="Special Elite" font-size="30" fill="{INK}" stroke="#fffdf4" stroke-width="6" paint-order="stroke">{name}</text></g>'
    return cutsvg('0 0 1000 1000', body + extra, w)

def world_map(w=1500, routes=()):
    M = json.load(open('assets/maps.json'))
    W = M['world']; C = M['worldCities']
    body = f'<rect x="0" y="0" width="1600" height="800" fill="#bcd3e6"/>'
    body += ''.join(f'<path d="{p["d"]}" fill="#efe3c4" stroke="#7a6f58" stroke-width="1"/>' for p in W['paths'])
    for i, (a, b_, cls) in enumerate(routes):
        x1, y1 = C[a]; x2, y2 = C[b_]
        mx, my = (x1 + x2) / 2, min(y1, y2) - 120
        body += f'<path class="{cls}" d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" fill="none" stroke="{RED}" stroke-width="5" stroke-linecap="round"/>'
        body += f'<circle class="{cls}d" cx="{x2:.0f}" cy="{y2:.0f}" r="7" fill="{RED}" stroke="#fff" stroke-width="2"/>'
    return cutsvg('0 0 1600 800', body, w)

def brazil_dots(w=700, n=12):
    M = json.load(open('assets/maps.json'))['brazil']
    body = f'<path d="{M["d"]}" fill="#efe3c4" stroke="#7a6f58" stroke-width="3"/>'
    names = ['Rio de Janeiro', 'São Paulo', 'Porto Alegre', 'Salvador', 'Recife', 'Fortaleza', 'Manaus', 'Brasília', 'Belém', 'Curitiba', 'Belo Horizonte', 'Florianópolis']
    for i, k in enumerate(names[:n]):
        x, y = M['cities'][k]
        body += f'<circle class="bd b{i}" cx="{x:.0f}" cy="{y:.0f}" r="12" fill="{RED}" stroke="#fff" stroke-width="3"/>'
    return cutsvg('0 0 1000 1000', body, w)

def card(inner_svg, vb='0 0 400 300', w=400, bg='#fffdf4', cap=None):
    c = f'<div class="pcap" style="font-size:34px">{H.escape(cap)}</div>' if cap else ''
    return f'<div class="card" style="width:{w}px;background:{bg}">{cutsvg(vb, inner_svg, w-40)}{c}</div>'

def suspect(icon, name, w=470):
    return (f'<div class="card susp" style="width:{w}px"><div class="clip"></div>'
            f'<div class="sh">SUSPEITO</div>{icon}<div class="sn">{H.escape(name)}</div></div>')

def gov_icon(w=260):
    b = f'<path d="M20,90 L150,30 L280,90Z" fill="#e9e2cf" stroke="{INK}" stroke-width="3"/>'
    b += ''.join(f'<rect x="{x}" y="96" width="22" height="110" fill="#fffdf4" stroke="{INK}" stroke-width="3"/>' for x in range(40, 270, 46))
    b += f'<rect x="20" y="206" width="260" height="22" fill="#e9e2cf" stroke="{INK}" stroke-width="3"/>'
    return cutsvg('0 0 300 240', b, w)

def pricetag(txt='R$', w=420, lock=True):
    b = f'<path d="M20,60 L80,10 L380,10 L380,210 L80,210 L20,160Z" fill="#f6d36b" stroke="{INK}" stroke-width="3"/><circle cx="70" cy="110" r="14" fill="#fffdf4" stroke="{INK}" stroke-width="3"/>'
    fs = min(96, int((430 if lock else 640) / max(1, len(txt))))
    b += f'<text x="{"200" if lock else "235"}" y="{110 + fs*0.35:.0f}" font-family="Anton" font-size="{fs}" text-anchor="middle" fill="{INK}">{H.escape(txt)}</text>'
    if lock:
        b += f'<g class="lock"><path d="M300,150 L300,120 C300,90 350,90 350,120 L350,150" fill="none" stroke="#555" stroke-width="12"/><rect x="285" y="150" width="80" height="70" rx="8" fill="#6b6b6b" stroke="{INK}" stroke-width="3"/><circle cx="325" cy="182" r="9" fill="#222"/></g>'
    return cutsvg('0 0 400 240', b, w)

def thermo(w=180):
    b = f'<rect x="60" y="20" width="60" height="380" rx="30" fill="#fffdf4" stroke="{INK}" stroke-width="4"/><circle cx="90" cy="420" r="55" fill="{RED}" stroke="{INK}" stroke-width="4"/>'
    b += f'<rect class="merc" x="74" y="60" width="32" height="340" fill="{RED}" style="transform-origin:90px 400px"/>'
    b += f'<text x="90" y="440" font-family="Anton" font-size="56" fill="#fff" text-anchor="middle">US$</text>'
    return cutsvg('0 0 180 490', b, w)

def sandwich(w=520):
    b = (f'<path d="M40,120 Q260,0 480,120Z" fill="#e0a85a" stroke="{INK}" stroke-width="3"/>'
         f'<rect x="40" y="120" width="440" height="26" fill="#6cbf4a" stroke="{INK}" stroke-width="3"/>'
         f'<rect x="50" y="146" width="420" height="40" rx="10" fill="#8a4b2a" stroke="{INK}" stroke-width="3"/>'
         f'<rect x="40" y="186" width="440" height="20" fill="#f2c94c" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M40,206 L480,206 Q470,250 260,250 Q50,250 40,206Z" fill="#e0a85a" stroke="{INK}" stroke-width="3"/>')
    return cutsvg('0 0 520 260', b, w)

def tag(txt, color='#fffdf4', w=260, cls=''):
    b = f'<path d="M10,40 L50,6 L250,6 L250,94 L50,94 L10,60Z" fill="{color}" stroke="{INK}" stroke-width="3"/><circle cx="44" cy="50" r="8" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    b += f'<text x="150" y="66" font-family="Anton" font-size="44" text-anchor="middle" fill="{INK}">{H.escape(txt)}</text>'
    return cutsvg('0 0 260 100', b, w)

def paperstack(n=10, w=520):
    b = ''
    for i in range(n):
        y = 520 - i * 34
        b += f'<g class="ps p{i}"><rect x="{40 + (i*37)%23}" y="{y}" width="420" height="30" fill="#fffdf4" stroke="{INK}" stroke-width="2" transform="rotate({((i*53)%7)-3} 250 {y})"/></g>'
    return cutsvg('0 0 520 580', b, w)

def box(txt='VARIGLOG', w=360):
    b = (f'<path d="M30,90 L200,40 L370,90 L200,140Z" fill="#d9b07a" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M30,90 L200,140 L200,330 L30,280Z" fill="#c69b62" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M370,90 L200,140 L200,330 L370,280Z" fill="#b4884f" stroke="{INK}" stroke-width="3"/>'
         f'<text x="115" y="230" font-family="Anton" font-size="38" fill="#18346f" transform="rotate(16 115 230)" text-anchor="middle">{txt}</text>')
    b += gstar(285, 190, 30)
    return cutsvg('0 0 400 360', b, w)

def hourglass(w=300):
    b = (f'<rect x="20" y="10" width="260" height="26" rx="8" fill="#8a5a2b" stroke="{INK}" stroke-width="3"/>'
         f'<rect x="20" y="464" width="260" height="26" rx="8" fill="#8a5a2b" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M50,36 L250,36 L160,250 L250,464 L50,464 L140,250Z" fill="#e8f1f8" stroke="{INK}" stroke-width="3"/>'
         f'<path class="sandtop" d="M80,80 L220,80 L155,235 L145,235Z" fill="#e5b33a"/>'
         f'<path class="sandbot" d="M70,460 L230,460 L150,330Z" fill="#e5b33a"/>'
         f'<rect x="147" y="235" width="6" height="225" fill="#e5b33a"/>')
    return cutsvg('0 0 300 500', b, w)

def balance(w=1100):
    b = (f'<rect x="530" y="120" width="40" height="420" fill="#8a5a2b" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M430,560 L670,560 L620,520 L480,520Z" fill="#6e4520" stroke="{INK}" stroke-width="3"/>'
         f'<g class="beam"><rect x="120" y="100" width="860" height="26" rx="10" fill="#a0703c" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M160,126 L120,300 M160,126 L200,300 M940,126 L900,300 M940,126 L980,300" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M80,300 L240,300 Q160,350 80,300Z" fill="#c8c8c8" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M860,300 L1020,300 Q940,350 860,300Z" fill="#c8c8c8" stroke="{INK}" stroke-width="3"/></g>'
         f'<circle cx="550" cy="113" r="18" fill="#e5b33a" stroke="{INK}" stroke-width="3"/>')
    return cutsvg('0 0 1100 580', b, w)

def cheque(w=1100, value='R$ 4.000.000.000,00'):
    b = (f'<rect x="10" y="10" width="1080" height="460" rx="14" fill="#e6f0dc" stroke="{INK}" stroke-width="4"/>'
         f'<rect x="30" y="30" width="1040" height="420" rx="10" fill="none" stroke="#7aa36a" stroke-width="3" stroke-dasharray="10 6"/>'
         f'<text x="60" y="100" font-family="Special Elite" font-size="38" fill="{INK}">PAGUE A: MASSA FALIDA DA VARIG</text>'
         f'<text x="60" y="160" font-family="Special Elite" font-size="30" fill="#555">ACORDO UNIÃO · 2024</text>'
         f'<rect x="560" y="200" width="490" height="90" fill="#fff" stroke="{INK}" stroke-width="3"/>'
         f'<text x="805" y="262" font-family="Anton" font-size="52" fill="{INK}" text-anchor="middle">+ R$ 4 BILHÕES</text>'
         f'<path d="M60,400 L460,400" stroke="{INK}" stroke-width="2"/><text x="60" y="436" font-family="Special Elite" font-size="26" fill="#555">CATORZE ANOS DEPOIS DA FALÊNCIA</text>')
    return cutsvg('0 0 1100 480', b, w)

def loyalty(w=820):
    b = (f'<rect x="10" y="10" width="800" height="500" rx="40" fill="#18346f" stroke="{INK}" stroke-width="4"/>'
         f'<path d="M10,330 Q400,250 810,360 L810,470 Q810,510 770,510 L50,510 Q10,510 10,470Z" fill="{ORANGE}"/>'
         f'<text x="70" y="140" font-family="Anton" font-size="96" fill="#fff">SMILES</text>'
         f'<text x="72" y="200" font-family="Special Elite" font-size="34" fill="#fff">programa de milhagem · 1994</text>'
         f'<rect x="70" y="250" width="110" height="80" rx="10" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>'
         f'<text x="70" y="450" font-family="Special Elite" font-size="38" fill="#fff">0000 1994 2007 2013</text>')
    return cutsvg('0 0 820 520', b, w)

def chart(w=1000):
    b = (f'<rect x="0" y="0" width="1000" height="600" fill="#fffdf4" stroke="{INK}" stroke-width="3"/>'
         + ''.join(f'<path d="M80,{y} L960,{y}" stroke="#d6cdb5" stroke-width="2"/>' for y in range(80, 560, 80))
         + f'<path d="M80,40 L80,540 L960,540" fill="none" stroke="{INK}" stroke-width="4"/>'
         f'<path class="ln" d="M80,470 L200,460 L320,455 L440,440 L520,430 L560,250 L620,215 L700,230 L780,180 L860,150 L940,110" fill="none" stroke="{RED}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round"/>'
         f'<text x="100" y="90" font-family="Anton" font-size="56" fill="{INK}">DÓLAR EM REAIS</text>'
         f'<text x="520" y="585" font-family="Special Elite" font-size="34" fill="{INK}" text-anchor="middle">1999</text>'
         f'<text x="120" y="585" font-family="Special Elite" font-size="34" fill="{INK}">1998</text>'
         f'<text x="900" y="585" font-family="Special Elite" font-size="34" fill="{INK}">2002</text>')
    return cutsvg('0 0 1000 600', b, w)

def note(w=300, txt='R$'):
    b = (f'<rect x="5" y="5" width="290" height="140" rx="6" fill="#bfe0c8" stroke="{INK}" stroke-width="3"/>'
         f'<circle cx="150" cy="75" r="42" fill="#9fcaa9" stroke="{INK}" stroke-width="2"/>'
         f'<text x="150" y="92" font-family="Anton" font-size="46" fill="#245a35" text-anchor="middle">{txt}</text>')
    return cutsvg('0 0 300 150', b, w)

def clock(w=420):
    b = (f'<circle cx="200" cy="200" r="185" fill="#fffdf4" stroke="{INK}" stroke-width="6"/>'
         + ''.join(f'<path d="M{200+160*math.sin(i*math.pi/6):.0f},{200-160*math.cos(i*math.pi/6):.0f} L{200+180*math.sin(i*math.pi/6):.0f},{200-180*math.cos(i*math.pi/6):.0f}" stroke="{INK}" stroke-width="6"/>' for i in range(12))
         + f'<g class="hand"><path d="M196,200 L200,50 L204,200Z" fill="{RED}" stroke="{INK}" stroke-width="2"/></g>'
         f'<g class="hand2"><path d="M194,200 L200,110 L206,200Z" fill="{INK}"/></g><circle cx="200" cy="200" r="12" fill="{INK}"/>')
    return cutsvg('0 0 400 400', b, w)

def hotel(w=380):
    b = (f'<path d="M40,120 L200,40 L360,120Z" fill="#d36b4a" stroke="{INK}" stroke-width="3"/>'
         f'<rect x="60" y="120" width="280" height="220" fill="#fffdf4" stroke="{INK}" stroke-width="3"/>'
         + ''.join(f'<rect x="{x}" y="{y}" width="40" height="34" fill="#9fc0dc" stroke="{INK}" stroke-width="2"/>' for x in (90, 180, 270) for y in (150, 210))
         + f'<rect x="170" y="270" width="60" height="70" fill="#8a5a2b" stroke="{INK}" stroke-width="3"/>'
         f'<text x="200" y="104" font-family="Anton" font-size="30" fill="#fff" text-anchor="middle">TROPICAL</text>')
    return cutsvg('0 0 400 360', b, w)

def ruler(years, w=1700):
    n = len(years); b = f'<rect x="0" y="40" width="1700" height="60" fill="#fffdf4" stroke="{INK}" stroke-width="3"/>'
    for i in range(0, 1700, 34):
        b += f'<path d="M{i},40 L{i},{58 if i % 170 else 72}" stroke="{INK}" stroke-width="2"/>'
    for i, y in enumerate(years):
        x = 100 + i * (1500 / max(1, n - 1))
        b += f'<g class="yr y{i}"><circle cx="{x:.0f}" cy="70" r="12" fill="{RED}" stroke="{INK}" stroke-width="2"/><text x="{x:.0f}" y="150" font-family="Anton" font-size="46" text-anchor="middle" fill="{INK}">{y}</text></g>'
    return cutsvg('0 -20 1700 200', b, w)

def ball(w=160):
    b = f'<circle cx="80" cy="80" r="70" fill="#fff" stroke="{INK}" stroke-width="4"/><path d="M80,48 L108,68 L98,100 L62,100 L52,68Z" fill="{INK}"/>'
    return cutsvg('0 0 160 160', b, w)

def star_big(w=420):
    return cutsvg('0 0 400 400', gstar(200, 200, 180), w)

def rose_big(w=420, crumpled=False):
    b = f'<circle cx="200" cy="200" r="190" fill="#fffdf4" stroke="{INK}" stroke-width="3"/>' + rose(200, 200, 160, fill=BLUE)
    if crumpled:
        b += '<path d="M40,120 L180,210 L120,360 M260,40 L230,200 L370,260" stroke="#0004" stroke-width="3" fill="none"/>'
    return cutsvg('0 0 400 400', b, w)

def plane_group(n=4, liv='varig', w=900, kinds=('jet',)):
    cols = min(n, 4); rows = (n + cols - 1) // cols
    out = '<div class="fleet" style="width:%dpx">' % w
    for i in range(n):
        out += f'<div class="fp f{i}">{plane(kinds[i % len(kinds)], liv, w // cols - 20)}</div>'
    return out + '</div>'
