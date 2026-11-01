"""nicho.py — busca de outliers para o canal dark (finanças e histórias de negócios).

Mesmo motor do luks-outlier-nuvem (views ÷ mediana dos vídeos vizinhos do mesmo canal), sem os filtros de games.
Só biblioteca padrão do Python. A chave fica na variável de ambiente YT_API_KEY (só YouTube Data API), nunca no repo.

  python3 nicho.py discover            roda as buscas de data/buscas.txt (100 unidades cada) e cadastra os canais
  python3 nicho.py scan                atualiza os vídeos dos canais cadastrados (~3 unidades por canal)
  python3 nicho.py rank [--formato longo|short] [--dias 30] [--top 40]   gera out/rank.txt e out/rank.json
  python3 nicho.py diario              discover (rodízio) + scan + rank, o que a rotina da nuvem roda

Opções: --idioma pt (filtra títulos/canais), --min-views 10000, --min-ratio 2.5, --buscas 6 (por dia, em rodízio).
Banco: work/nicho.sqlite. Saída: out/. Cota diária: NICHO_QUOTA (padrão 9000 de 10000).
"""
import json, os, re, sqlite3, statistics, sys, threading, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK, OUT, DATA = HERE / 'work', HERE / 'out', HERE / 'data'
NOW = datetime.now(timezone.utc)
QUOTA = int(os.environ.get('NICHO_QUOTA', 9000))
args = sys.argv[1:]
def opt(n, d=None): return args[args.index('--' + n) + 1] if '--' + n in args else d
def iso(d): return d.strftime('%Y-%m-%dT%H:%M:%SZ')
def parse(s): return datetime.strptime(s[:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
def med(xs): return statistics.median(xs) if xs else None

# títulos que não são história/explicação: lives, cortes, notícias do dia, análise de ação, cripto pump
RUIDO = re.compile(r'\blive\b|ao vivo|\bcorte\b|cortes|podcast|#\d+ ?ep|epis[oó]dio|react|reag|giveaway|sorteio|'
                   r'cota[cç][aã]o|fechamento do mercado|ibovespa hoje|d[oó]lar hoje|day ?trade|sinal|pump|airdrop|'
                   r'comprar agora|carteira recomendada|dividendos? de (janeiro|fevereiro|mar[cç]o|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)', re.I)

# ------------------------------------------------------------------ banco
WORK.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
db = sqlite3.connect(os.environ.get('NICHO_DB', WORK / 'nicho.sqlite'), check_same_thread=False); db.row_factory = sqlite3.Row
LOCK = threading.Lock()   # o scan chama a API em 8 threads; banco e contador de cota passam por aqui
db.executescript('''
create table if not exists channels(id text primary key, title text, handle text, subs integer, lang text, country text,
  source text, added_utc text, scan_utc text, status text default 'active');
create table if not exists videos(id text primary key, channel_id text, title text, published text, duration integer,
  views integer, likes integer, comments integer, lang text, is_short integer, scanned_utc text);
create table if not exists snaps(id text, utc text, views integer, primary key(id, utc));
create table if not exists quota(day text primary key, units integer);
create table if not exists topics(video_id text primary key, status text, reason text, utc text);
''')
def quota_day(): return (NOW - timedelta(hours=7)).strftime('%Y-%m-%d')   # o dia da cota vira à meia-noite do Pacífico
units = 0
def used(): r = db.execute('select units from quota where day=?', (quota_day(),)).fetchone(); return (r['units'] if r else 0) + units
def commit_units():
    global units
    db.execute('insert into quota(day, units) values(?,?) on conflict(day) do update set units=units+excluded.units', (quota_day(), units)); db.commit(); units = 0

# ------------------------------------------------------------------ API
def api(route, cost=1, **kw):
    global units
    key = os.environ.get('YT_API_KEY') or sys.exit('YT_API_KEY ausente no ambiente')
    with LOCK:
        if used() + cost > QUOTA: raise RuntimeError(f'cota do dia esgotada ({used()}/{QUOTA})')
        units += cost
    q = urllib.parse.urlencode({k: v for k, v in kw.items() if v not in (None, '')} | {'key': key})
    for tent in range(3):
        try:
            with urllib.request.urlopen(f'https://www.googleapis.com/youtube/v3/{route}?{q}', timeout=90) as r: return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', 'replace')[:300]
            if e.code in (500, 503) and tent < 2: continue
            raise RuntimeError(f'{e.code} {route}: {body}') from None   # a mensagem do Google não traz a chave
        except (urllib.error.URLError, TimeoutError):
            if tent == 2: raise

def dur(s):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s or '')
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (86400, 3600, 60, 1))) if m else 0

# ------------------------------------------------------------------ canais
def add_channels(ids, source):
    have = {r['id'] for r in db.execute('select id from channels')}; new = [i for i in dict.fromkeys(ids) if i not in have]
    for i in range(0, len(new), 50):
        for c in api('channels', part='snippet,statistics', id=','.join(new[i:i + 50])).get('items', []):
            sn, st = c['snippet'], c.get('statistics', {})
            db.execute('insert or ignore into channels(id, title, handle, subs, lang, country, source, added_utc) values(?,?,?,?,?,?,?,?)',
                       (c['id'], sn.get('title'), sn.get('customUrl'), int(st.get('subscriberCount') or 0), sn.get('defaultLanguage'), sn.get('country'), source, iso(NOW)))
    db.commit(); return new

def discover(q, formato, dias=60, idioma='pt'):
    r = api('search', cost=100, part='snippet', q=q, type='video', order='viewCount', maxResults=50, relevanceLanguage=idioma,
            videoDuration='short' if formato == 'short' else 'medium', publishedAfter=iso(NOW - timedelta(days=dias)))
    found = [x['snippet']['channelId'] for x in r.get('items', [])]
    new = add_channels(found, 'busca:' + q); return f'{q} [{formato}]: {len(set(found))} canais, {len(new)} novos'

def fetch(cid, cutoff, pages=2):
    """últimos vídeos do canal: playlist de longos (UULF) e de Shorts (UUSH)"""
    ids = {}
    for pl, short in (('UULF' + cid[2:], 0), ('UUSH' + cid[2:], 1)):
        page = None
        for _ in range(pages):
            try: r = api('playlistItems', part='contentDetails', playlistId=pl, maxResults=50, pageToken=page)
            except RuntimeError as e:
                if '404' in str(e) or 'playlistNotFound' in str(e): break
                raise
            its = r.get('items', []); ids.update({x['contentDetails']['videoId']: short for x in its}); page = r.get('nextPageToken')
            if not page or not its or (its[-1]['contentDetails'].get('videoPublishedAt') or '9') < cutoff: break
    vids, lst = [], list(ids)
    for i in range(0, len(lst), 50):
        for v in api('videos', part='snippet,statistics,contentDetails', id=','.join(lst[i:i + 50])).get('items', []):
            sn, st = v['snippet'], v.get('statistics', {})
            if sn.get('liveBroadcastContent') not in (None, 'none'): continue
            vids.append(dict(id=v['id'], channel_id=cid, title=sn.get('title'), published=sn.get('publishedAt'), duration=dur(v['contentDetails'].get('duration')),
                             views=int(st.get('viewCount') or 0), likes=int(st.get('likeCount') or 0), comments=int(st.get('commentCount') or 0),
                             lang=sn.get('defaultAudioLanguage') or sn.get('defaultLanguage'), is_short=ids[v['id']]))
    return cid, vids

def scan(dias=130, max_age_h=20):
    stale = iso(NOW - timedelta(hours=max_age_h)); cutoff = iso(NOW - timedelta(days=dias))
    rows = db.execute("select id from channels where status != 'muted' and (scan_utc is null or scan_utc < ?) order by subs desc", (stale,)).fetchall()
    n = v = 0; errs = []; t = iso(NOW)
    with ThreadPoolExecutor(8) as ex:
        for f in [ex.submit(fetch, r['id'], cutoff) for r in rows]:
            try: cid, vids = f.result()
            except Exception as e: errs.append(str(e)[:120]); continue
            for x in vids:
                db.execute('''insert into videos(id, channel_id, title, published, duration, views, likes, comments, lang, is_short, scanned_utc)
                    values(:id,:channel_id,:title,:published,:duration,:views,:likes,:comments,:lang,:is_short,:t)
                    on conflict(id) do update set title=excluded.title, views=excluded.views, likes=excluded.likes, comments=excluded.comments, scanned_utc=excluded.scanned_utc''', x | {'t': t})
                db.execute('insert or replace into snaps(id, utc, views) values(?,?,?)', (x['id'], t, x['views']))
            db.execute('update channels set scan_utc=? where id=?', (t, cid)); n += 1; v += len(vids)
    db.commit(); commit_units()
    return f'{n} canais, {v} vídeos' + (f' | {len(errs)} erros: ' + '; '.join(errs[:3]) if errs else '')

# ------------------------------------------------------------------ ranking
def ranked(formato='longo', dias=30, idioma=None, min_ratio=2.5, min_views=10000, only_new=True):
    short = 1 if formato == 'short' else 0; lo = iso(NOW - timedelta(days=dias)); janela = 14 if short else 30
    judged = {r['video_id'] for r in db.execute('select video_id from topics')}; out = []
    for c in db.execute("select * from channels where status != 'muted'").fetchall():
        vs = db.execute('select * from videos where channel_id=? and is_short=? and (is_short=1 or duration >= 240) order by published', (c['id'], short)).fetchall()
        if len(vs) < (7 if short else 5): continue
        ts = [parse(v['published']).timestamp() for v in vs]
        for i, v in enumerate(vs):
            if v['published'] < lo or v['views'] < min_views or RUIDO.search(v['title'] or ''): continue
            if only_new and v['id'] in judged: continue
            if idioma and (v['lang'] or c['lang'] or idioma)[:2] != idioma: continue
            others = sorted((abs(ts[j] - ts[i]), vs[j]['views']) for j in range(len(vs)) if j != i)
            n14 = [x for _, x in others[:14]]; perto = [x for d, x in others if d <= janela * 86400]
            r14 = v['views'] / max(med(n14), 1); rj = v['views'] / max(med(perto), 1) if len(perto) >= 4 else None
            rs = [r for r in (r14, rj) if r]
            if r14 < min_ratio or min(rs) < min_ratio * 0.6: continue
            age = (NOW.timestamp() - ts[i]) / 86400
            prev = db.execute('select utc, views from snaps where id=? and utc <= ? and utc >= ? order by utc desc limit 1',
                              (v['id'], iso(NOW - timedelta(hours=12)), iso(NOW - timedelta(hours=72)))).fetchone()
            g24 = round(max(v['views'] - prev['views'], 0) * 24 / max((NOW - parse(prev['utc'])).total_seconds() / 3600, 1)) if prev else None
            out.append(dict(id=v['id'], title=v['title'], channel=c['title'], subs=c['subs'], views=v['views'], age=round(age, 1), dur=v['duration'],
                            r14=round(r14, 2), rj=round(rj, 2) if rj else None, score=round(statistics.geometric_mean(rs), 2), base=round(med(n14)),
                            g24=g24, young=age < 3, url=('https://youtube.com/shorts/' if short else 'https://youtu.be/') + v['id']))
    return sorted(out, key=lambda r: -r['score'])

def show(rows, top):
    lines = []
    for r in rows[:top]:
        sub = f" ↑+{r['g24']}/dia" if r.get('g24') else ''
        lines.append(f"{r['score']:6.2f} | r14 {r['r14']:5.1f} | {r['views']:>9,} views | {r['age']:5.1f}d{' NOVO<3d' if r['young'] else ''}{sub} | "
                     f"{r['channel'][:28]} | {r['title'][:90]} | {r['url']}")
    return '\n'.join(lines) or 'nenhum candidato'

# ------------------------------------------------------------------ comandos
def buscas():
    p = DATA / 'buscas.txt'
    return [l.strip() for l in p.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')] if p.exists() else []

def rodar_buscas(n=None):
    qs = buscas(); idioma = opt('idioma', 'pt')
    if n is not None and qs:
        day = NOW.toordinal(); qs = [qs[(day * n + i) % len(qs)] for i in range(min(n, len(qs)))]
    res = []
    for q in qs:
        formato, _, termo = q.partition('|') if '|' in q else ('longo', '', q)
        try: res.append(discover(termo.strip(), formato.strip(), idioma=idioma))
        except RuntimeError as e: res.append(f'{q}: parou: {str(e)[:200]}'); break
    commit_units(); return '\n'.join(res)

def rank_out():
    txt = []; allrows = {}
    for formato in ([opt('formato')] if opt('formato') else ['longo', 'short']):
        rows = ranked(formato, int(opt('dias', 30)), opt('idioma'), float(opt('min-ratio', 2.5)), int(opt('min-views', 10000)))
        allrows[formato] = rows[:int(opt('top', 40))]; txt.append(f'## {formato} ({len(rows)} candidatos)\n' + show(rows, int(opt('top', 40))))
    (OUT / 'rank.txt').write_text('\n\n'.join(txt) + '\n', encoding='utf-8')
    (OUT / 'rank.json').write_text(json.dumps(allrows, ensure_ascii=False, indent=1), encoding='utf-8')
    return '\n\n'.join(txt)

if __name__ == '__main__':
    cmd = args[0] if args else 'diario'
    if cmd == 'discover': print(rodar_buscas())
    elif cmd == 'scan': print(scan())
    elif cmd == 'rank': print(rank_out())
    elif cmd == 'diario':
        log = [rodar_buscas(int(opt('buscas', 6))), scan(), rank_out()]
        (OUT / 'meta.json').write_text(json.dumps(dict(utc=iso(NOW), units_hoje=used(), canais=db.execute('select count(*) from channels').fetchone()[0],
                                                       videos=db.execute('select count(*) from videos').fetchone()[0]), indent=1), encoding='utf-8')
        print('\n'.join(log))
    else: sys.exit(__doc__)
