# Plano de cenas do piloto Varig: cada cena começa numa palavra da narração (cue).
import props as P

def it(html, x=960, y=540, enter='pop', d=0.45, exit=None, ed=0.3, **kw):
    o = dict(html=html, x=x, y=y, enter=dict(k=enter, d=d), **kw)
    if exit: o['exit'] = dict(k=exit, d=ed)
    return o

def stat(txt, x=960, y=540, size=150, yellow=False, at=None, **kw):
    kw.setdefault('sfx', 'swoosh')
    o = it(P.stat(txt, size, yellow), x, y, 'pop', 0.35, z=40, **kw)
    if at is not None: o['at'] = at
    return o

def label(txt, x=960, y=540, size=46, at=None, enter='drop', **kw):
    kw.setdefault('sfx', 'paper')
    o = it(P.label(txt, round(size * 1.15)), x, y, enter, 0.5, z=30, **kw)
    if at is not None: o['at'] = at
    return o

def typed(txt, x=960, y=540, size=54, at=None, **kw):
    o = it(P.typew(txt, round(size * 1.15)), x, y, 'cut', 0, sfx='typewriter', z=30, type='typew', cps=24, step=False, **kw)
    if at is not None: o['at'] = at
    return o

def stamp(txt, x=960, y=540, size=130, at=None, sub=None, color=P.RED, rot=-8, shake=True, **kw):
    kw.setdefault('sfx', 'stamp')
    o = it(P.stamp(txt, size, color, sub), x, y, 'slam', 0.1, z=50, rot=rot, **kw)
    if shake: o['impact'] = 'shake'
    if at is not None: o['at'] = at
    return o

def photo(key, x=960, y=540, w=900, rot=0, enter='slideR', at=None, cap=None, bw=False, kb=(1.0, 1.08), **kw):
    kw.setdefault('sfx', 'paper')
    o = it(P.photo(key, w, cap, bw=bw), x, y, enter, 0.55, rot=rot, kb=list(kb), z=kw.pop('z', 20), **kw)
    if at is not None: o['at'] = at
    return o

def full(key, at=None, **kw):
    o = it(P.full(key), 960, 540, 'cut', 0, kb=[1.0, 1.1], z=5, jit=False, **kw)
    if at is not None: o['at'] = at
    return o

def plane(kind='jet', liv='varig', x=960, y=540, w=700, enter='slideL', at=None, flip=False, **kw):
    o = it(P.plane(kind, liv, w, flip), x, y, enter, 0.6, z=kw.pop('z', 25), **kw)
    if at is not None: o['at'] = at
    return o

def mv(at=None, d=0.8, e='out', **kw):
    o = dict(d=d, e=e, **kw)
    if at is not None: o['at'] = at
    return o

def sub(sel, k, at=None, d=0.4, **kw):
    o = dict(sel=sel, k=k, d=d, **kw)
    if at is not None: o['at'] = at
    return o

def stagger(sels, k, at, step=0.12, d=0.35, **kw):
    out = []
    for i, s in enumerate(sels):
        if isinstance(at, str):
            base, _, adj = at.partition('@')
            a = f'{base}@{float(adj or 0) + i*step:.2f}'
        else:
            a = (at or 0) + i * step
        out.append(sub(s, k, at=a, d=d, **kw))
    return out

ROUTES = [f'.r{i}' for i in range(22)]
FLEET8 = [f'.f{i}' for i in range(8)]

CHAPTER_TITLES = {1: ('1927', 'a origem'), 2: ('RUBEN BERTA', 'o homem que fez a Varig crescer'), 3: ('A ESCALADA', '1955 a 1991'),
                  4: ('A PERGUNTA', ''), 5: ('PREÇO CONGELADO', 'o primeiro golpe'), 6: ('O MUNDO MUDA', 'anos 90'),
                  7: ('A QUEDA', '2005 a 2010'), 8: ('O QUE SOBROU', '')}

MUTES = [(7, 'demitidos', 1.3)]

PHASES = {0: [('Só que em 2006', 'virada', 0.27), ('Então como a maior', 'auge', 0.27)],
          5: [('CARD', 'virada', 0.27)],
          7: [('CARD', 'queda', 0.27)]}

S = {}
# ---------------- 1. GANCHO ----------------
S[0] = [
    dict(cue=None, rate=0.01, sfx=[(0, 'turbine', 0.9)], items=[
        plane('jet', 'varig', x=150, y=600, w=1000, enter='cut', moves=[mv(0, d=6.6, e='lin', x=2500, y=420, r=-4)]),
        label('anos 70 · 80 · 90', x=1500, y=220, size=50, at=1.4, enter='drop'),
        photo('b747_1', x=960, y=520, w=1150, rot=-2, enter='drop', at='embarcar na Varig', z=30, impact='kick'),
    ]),
    dict(cue='Ela voava para mais', rate=0.008, items=[
        it(P.globe(860), x=620, y=560, enter='spin', d=0.6, sfx='whoosh', subs=stagger(ROUTES, 'draw', 'Ela voava@0.4', step=0.09, d=0.5)
           + [sub('.cd', 'appear', at='Ela voava@0.5', d=0.3)], moves=[mv(0, d=12, e='lin', r=8)]),
        stat('102 DESTINOS', x=1400, y=430, size=150, yellow=True, at='cem destinos'),
        label('todos os continentes habitados', x=1400, y=640, at='continentes'),
    ]),
    dict(cue='Nenhuma outra companhia', rate=0.016, items=[
        full('b747_0'),
        label('nenhuma outra brasileira chegou lá', x=960, y=930, size=48, at='chegou'),
    ]),
    dict(cue='Só que em 2006', rate=0.012, sfx=[(0, 'boom', 0.8)], items=[
        it(P.headline('Varig faz o último voo internacional', 'Companhia deixa de voar para fora do país', 'O DIÁRIO', 'agosto de 2006'), x=960, y=520, enter='flip', d=0.6, rot=-3, sfx='typewriter'),
        stat('2006', x=1560, y=170, size=130, yellow=True, at='2006'),
        stamp('FALÊNCIA', x=980, y=560, size=170, at='falência', sub='2010'),
    ]),
    dict(cue='Então como a maior', rate=0.01, items=[
        plane('jet', 'varig', x=960, y=600, w=900, enter='cut', moves=[mv('some do céu', d=1.0, e='in', x=1700, y=60, s=0.05, r=-14)], sfx='whoosh'),
        stat('?', x=960, y=480, size=320, at='céu'),
    ]),
    dict(cue='A resposta não é', rate=0.01, items=[
        it(P.headline('Varig x União', 'O processo que atravessou décadas', 'ARQUIVO', ''), x=720, y=500, enter='drop', d=0.5, rot=2, sfx='paper'),
        stat('2024', x=1560, y=330, size=170, yellow=True, at='2024'),
        label('14 anos depois da falência', x=1340, y=860, at='catorze'),
    ]),
]
# ---------------- 2. ORIGEM ----------------
S[1] = [
    dict(cue=None, rate=0.01, items=[
        it(P.south_map(860), x=600, y=560, enter='pop', d=0.5, sfx='paper', subs=[sub('.cpoa', 'show', at='Porto Alegre', d=0.3)]),
        label('Porto Alegre · maio de 1927', x=1400, y=230, at='Porto Alegre'),
        photo('portoalegre_0', x=1400, y=640, w=620, rot=3, at='maio'),
    ]),
    dict(cue='Um alemão chamado', items=[
        typed('Otto Ernst Meyer', x=960, y=330, size=80, at='Otto'),
        label('Viação Aérea Rio-Grandense', x=960, y=640, size=72, at='funda a'),
    ]),
    dict(cue='Que é exatamente', rate=0.008, items=[
        it(P.letters('VARIG', 220), x=960, y=520, enter='cut', subs=[sub('.l0', 'drop', at='V A R I G', d=0.45, sfx='paper'),
                                                                    sub('.l1', 'drop', at='V A R I G#1', d=0.45, sfx='paper'),
                                                                    sub('.l2', 'drop', at='V A R I G#2', d=0.45, sfx='paper'),
                                                                    sub('.l3', 'drop', at='V A R I G#3', d=0.45, sfx='paper'),
                                                                    sub('.l4', 'drop', at='V A R I G#4', d=0.45, sfx='paper')]),
    ]),
    dict(cue='O primeiro avião nem pousava', items=[
        plane('sea', 'blank', x=720, y=620, w=1000, enter='slideL'),
        photo('dornier_0', x=1480, y=330, w=600, rot=4, at='hidroavião', bw=True, cap='Dornier Wal, o modelo do Atlântico'),
        label('ATLÂNTICO', x=700, y=330, size=64, at='Atlântico'),
        stat('9 PASSAGEIROS', x=1350, y=860, size=130, yellow=True, at='nove passageiros'),
    ]),
    dict(cue='A rota ligava', rate=0.02, fx=820, fy=620, items=[
        it(P.south_map(1050), x=900, y=560, enter='cut', subs=[sub('.cpoa', 'appear', at=0, d=0.2), sub('.rtlagoa', 'draw', at='Porto Alegre', d=2.4)]),
        label('Linha da Lagoa', x=1480, y=820, size=60, at='Linha da Lagoa'),
    ]),
    dict(cue='Inclusive, uma parte', items=[
        it(P.pie(21, 'Condor Syndikat'), x=660, y=540, enter='pop', sfx='paper', subs=[sub('.slice', 'grow', at='vinte e um', d=0.5, v=[0.2, 1.0])]),
        stat('21%', x=1380, y=420, size=200, yellow=True, at='vinte e um'),
        label('mais tarde, parte da Lufthansa', x=1380, y=680, at='Lufthansa'),
    ]),
    dict(cue='E durante os primeiros anos', rate=0.01, items=[
        it(P.south_map(820), x=960, y=560, enter='cut', subs=[sub('.cpoa', 'appear', at=0, d=0.2), sub('.rtlagoa', 'draw', at=0, d=0.1)]),
        plane('sea', 'blank', x=760, y=380, w=300, enter='pop', moves=[mv(0.3, d=5, e='inout', x=1100, y=740)]),
        label('uma empresa pequena', x=1500, y=220, at='pequena'),
    ]),
    dict(cue='O primeiro avião com rodas', items=[
        plane('sea', 'blank', x=800, y=560, w=800, enter='cut', moves=[mv(0, d=1.0, e='in', x=-700)]),
        plane('prop', 'blank', x=1000, y=600, w=900, enter='slideR', at='rodas', sfx='prop', moves=[mv('Junkers', d=0.4, y=585), mv('Junkers@0.4', d=0.4, y=600)]),
        stat('1932', x=1500, y=230, size=150, yellow=True, at='1932'),
        photo('junkers_0', x=430, y=260, w=520, rot=-4, at='Junkers', bw=True, enter='slideL', cap='Junkers'),
    ]),
    dict(cue='Ou seja, a maior companhia', items=[
        label('PEQUENA', x=520, y=420, size=70, at='pequena'),
        label('REGIONAL', x=980, y=600, size=70, at='regional', rot=3),
        label('SOTAQUE ALEMÃO', x=1420, y=420, size=70, at='sotaque', rot=-3),
    ]),
    dict(cue='E se alguém dissesse', rate=0.008, items=[
        it(P.world_map(1560, routes=[('Porto Alegre', 'Nova York', 'wa'), ('Porto Alegre', 'Tóquio', 'wb'), ('Porto Alegre', 'Joanesburgo', 'wc')]), x=960, y=520, enter='pop', sfx='paper',
           subs=[sub('.wa', 'draw', at='Nova York', d=0.6), sub('.wad', 'show', at='Nova York@0.5', d=0.2),
                 sub('.wb', 'draw', at='Tóquio', d=0.6), sub('.wbd', 'show', at='Tóquio@0.5', d=0.2),
                 sub('.wc', 'draw', at='Joanesburgo', d=0.6), sub('.wcd', 'show', at='Joanesburgo@0.5', d=0.2)]),
        label('ninguém ia acreditar', x=960, y=930, size=56, at='ninguém'),
    ]),
]
# ---------------- 3. RUBEN BERTA ----------------
S[2] = [
    dict(cue=None, items=[
        label('o fundador?', x=700, y=420, size=70),
        stamp('NÃO', x=760, y=470, size=110, at='não foi', shake=False),
        it(P.card(P.person.__call__(P.BLUE, 200).replace('<svg', '<svg'), w=360), x=1350, y=520, enter='slideR', at='funcionário', sfx='paper') if False else
        it(P.person(P.BLUE, 260), x=1350, y=540, enter='slideR', d=0.5, at='funcionário', sfx='paper'),
        label('RUBEN BERTA', x=1350, y=860, size=64, at='Ruben Berta'),
    ]),
    dict(cue='Ele assume a empresa', items=[
        it(P.person(P.BLUE, 220), x=420, y=560, enter='cut'),
        stat('1942 A 1966', x=1100, y=440, size=170, yellow=True, at='1942'),
        label('24 anos no comando', x=1100, y=700, size=56, at='vinte e quatro'),
        label('no meio da Segunda Guerra', x=1100, y=180, size=44, at='Segunda Guerra', enter='slideU'),
    ]),
    dict(cue='E no mesmo ano em que', rate=0.012, fx=700, fy=700, items=[
        it(P.south_map(940, mvd=True), x=760, y=560, enter='pop', sfx='paper', subs=[sub('.cpoa', 'appear', at=0, d=0.2), sub('.rtmvd', 'draw', at='Porto Alegre para', d=1.4, sfx='swoosh'), sub('.cmvd', 'show', at='Montevidéu', d=0.3)]),
        label('1º voo internacional', x=1480, y=300, size=56, at='primeiro voo'),
    ]),
    dict(cue='Quando a guerra acaba', items=[
        photo('dc3_0', x=620, y=420, w=900, rot=-3, enter='slideL', cap='Douglas DC-3'),
        plane('dc3', 'varig', x=1300, y=700, w=900, enter='drop', at='Douglas', impact='kick', sfx='thud'),
        stat('1946', x=1520, y=220, size=150, yellow=True, at='1946'),
    ]),
    dict(cue='Só que o mais importante', items=[
        label('comprar avião', x=960, y=480, size=80),
        stamp('NÃO', x=1020, y=520, size=150, at='não foi', shake=False),
    ]),
    dict(cue='Ele tinha uma ideia', items=[
        typed('uma ideia diferente de empresa', x=960, y=520, size=70, at='ideia'),
    ]),
    dict(cue='Em 1945 ele cria', items=[
        stat('1945', x=480, y=220, size=140, yellow=True, at='1945'),
        label('FUNDAÇÃO RUBEN BERTA', x=1300, y=220, size=56, at='Fundação'),
        it(P.pie(0, 'controle dos funcionários', people=True), x=960, y=620, enter='pop', at='controle', sfx='pop'),
    ]),
    dict(cue='Na prática, quem mandava', items=[
        label('quem mandava', x=560, y=300, size=64, at='mandava'),
        label('= quem trabalhava', x=1340, y=300, size=64, at='trabalhava'),
        it(P.dominoes(12, 1400), x=960, y=720, enter='slideU', at='trabalhava', sfx='paper'),
    ]),
    dict(cue='Na época isso parecia', items=[
        it(P.pie(0, '', people=True), x=960, y=540, enter='cut'),
        stamp('GENIAL', x=960, y=540, size=160, at='genial', color=P.GREEN, shake=False),
    ]),
    dict(cue='Guarda essa parte', rate=0.02, items=[
        it(P.pie(0, '', people=True), x=760, y=540, enter='cut', moves=[mv(0, d=0.5, s=0.8, r=-6)]),
        label('GUARDA ESSA PARTE', x=1380, y=540, size=60, at='Guarda', rot=4),
    ]),
]
# ---------------- 4. ESCALADA ----------------
YEARS = ['1955', '1959', '1960', '1961', '1965', '1974', '1975', '1976', '1981', '1985', '1987', '1991']
YCUE = ['Em 1955', 'Em 1959', 'Em 1960', 'Em 1961', 'Em 1965', 'Em 1974', 'Em 1975', 'Em 1976', 'em 1981', 'de 1985', 'Em 1987', 'em 1991']
S[3] = [
    dict(cue=None, rate=0.012, items=[
        it(P.ruler(YEARS, 1760), x=960, y=990, enter='slideU', d=0.5, z=60, until='Copa do Mundo$@0.4', sfx='paper',
           subs=[sub(f'.y{i}', 'show', at=YCUE[i] + '#1', d=0.3, sfx='stamp', vol=0.5) for i in range(12)]),
        plane('jet', 'varig', x=-300, y=760, w=700, enter='cut', moves=[mv(0, d=4.0, e='inout', x=2300, y=120, r=-14)], sfx='turbine'),
        stat('NÃO PARA DE CRESCER', x=960, y=420, size=110, at='não para'),
    ]),
    dict(cue='Em 1955 ela já', items=[
        photo('constellation_0', x=640, y=430, w=820, rot=-3, enter='slideL', bw=True, cap='Lockheed Constellation'),
        stat('1955', x=1460, y=250, size=150, yellow=True, at='1955'),
        label('Porto Alegre → Nova York', x=1400, y=560, size=52, at='Nova York'),
    ]),
    dict(cue='Em 1959 chegam', items=[
        plane('jet', 'varig', x=900, y=560, w=1100, enter='slideR'),
        label('os primeiros jatos', x=960, y=250, size=60, at='jatos'),
    ]),
    dict(cue='E no mesmo ano ela abre', items=[
        plane('jet', 'varig', x=620, y=620, w=760, enter='cut'),
        it(P.hotel(420), x=1400, y=540, enter='pop', at='hotéis', sfx='fold'),
        label('Hotéis Tropical', x=1400, y=860, size=50, at='Tropical'),
        label('queria estar em tudo', x=620, y=250, size=56, at='estar em tudo'),
    ]),
    dict(cue='Em 1960 vêm', items=[
        photo('b707_0', x=960, y=480, w=1250, rot=1, enter='slideR', cap='Boeing 707 da Varig'),
        stat('BOEING 707', x=1500, y=170, size=110, yellow=True, at='707'),
    ]),
    dict(cue='Em 1961 ela compra', items=[
        label('compra a Real Aerovias', x=960, y=170, size=56, at='Real'),
        it(P.plane_group(8, 'varig', 1500, kinds=('jet', 'dc3')), x=960, y=560, enter='cut', subs=[sub('.f0', 'show', at='Real', d=0.3), sub('.f1', 'show', at='Real@0.15', d=0.3), sub('.f2', 'show', at='Real@0.3', d=0.3), sub('.f3', 'show', at='Real@0.45', d=0.3)]
           + stagger(['.f4', '.f5', '.f6', '.f7'], 'show', 'dobra', step=0.08, d=0.25, sfx='pop')),
        stat('FROTA x2', x=1500, y=860, size=130, yellow=True, at='dobra'),
    ]),
    dict(cue='E é aí que aparece', rate=0.018, items=[
        photo('variggeral_3', x=1350, y=470, w=900, rot=3, enter='slideR', cap='a rosa dos ventos na cauda'),
        it(P.rose_big(460), x=560, y=520, enter='spin', d=0.7, at='rosa dos ventos', sfx='whoosh', impact='kick'),
    ]),
    dict(cue='Pensa que nessa época', items=[
        photo('galeao_0', x=860, y=480, w=1100, rot=-2, enter='slideL', bw=True),
        label('coisa de gente rica', x=1450, y=860, size=56, at='gente rica'),
    ]),
    dict(cue='Em 1965 vem', items=[
        stat('1965', x=960, y=420, size=200, yellow=True, at='1965'),
        label('o passo mais polêmico', x=960, y=660, size=64, at='polêmico'),
    ]),
    dict(cue='A Panair do Brasil', rate=0.008, items=[
        it(P.world_map(1560, routes=[('Rio de Janeiro', 'Lisboa', 'ea'), ('Rio de Janeiro', 'Paris', 'eb'), ('Rio de Janeiro', 'Londres', 'ec'), ('Rio de Janeiro', 'Frankfurt', 'ed'), ('Rio de Janeiro', 'Roma', 'ee')]), x=960, y=540, enter='pop', sfx='paper',
           subs=stagger(['.ea', '.eb', '.ec', '.ed', '.ee'], 'draw', 'rotas para a Europa', step=0.15, d=0.6) + stagger(['.ead', '.ebd', '.ecd', '.edd', '.eed'], 'show', 'rotas para a Europa@0.5', step=0.15, d=0.2)),
        stamp('PANAIR DO BRASIL', x=700, y=230, size=80, color=P.BLUE, rot=-4, shake=False, exit='slideD', ed=0.35, until='vão parar'),
        stamp('FECHADA', x=760, y=330, size=120, at='fechada', until='vão parar', exit='slideD', ed=0.35),
        label('→ VARIG', x=1300, y=860, size=70, at='justamente na Varig'),
    ]),
    dict(cue='Muita gente até hoje', items=[
        typed('favorecida?', x=960, y=500, size=110, at='favorecida'),
    ]),
    dict(cue='E de fato', rate=0.012, items=[
        it(P.globe(820), x=700, y=540, enter='spin', d=0.5, sfx='whoosh', subs=stagger(ROUTES, 'draw', 'E de fato@0.2', step=0.05, d=0.4) + [sub('.cd', 'appear', at=0.3, d=0.3)]),
        label('a porta do Brasil para o mundo', x=1400, y=860, size=48, at='porta'),
    ]),
    dict(cue='Em 1974 chegam', items=[
        photo('dc10_0', x=820, y=460, w=1150, rot=-2, enter='slideL', cap='McDonnell Douglas DC-10'),
        label('3º motor na cauda', x=1450, y=860, size=56, at='terceiro motor'),
    ]),
    dict(cue='Em 1975 ela compra', items=[
        stamp('CRUZEIRO · 1975', x=600, y=300, size=80, color=P.BLUE, rot=-6, at='Cruzeiro', shake=False),
        stamp('RIO SUL · 1976', x=1300, y=460, size=80, color=P.BLUE, rot=5, at='Rio Sul', shake=False),
        stamp('747 · 1981', x=760, y=680, size=90, color=P.BLUE, rot=-3, at='1981', shake=False),
        plane('jumbo', 'varig', x=1400, y=760, w=760, enter='slideR', at='jumbo'),
    ]),
    dict(cue='E em janeiro de 1985', rate=0.016, impacts=[('747 da Varig', 'kick', 0.08)], items=[
        full('b747_1'),
        stat('GUARULHOS, 1985', x=960, y=860, size=130, yellow=True, at='Guarulhos'),
    ]),
    dict(cue='Pensa no tamanho', items=[
        photo('guarulhos_1', x=960, y=480, w=1100, rot=2, enter='drop'),
        label('o maior aeroporto do país', x=960, y=900, size=56, at='maior aeroporto'),
    ]),
    dict(cue='E ela não para', items=[
        photo('b767_0', x=560, y=400, w=820, rot=-3, enter='slideL', at='767', cap='Boeing 767', sfx='turbine'),
        photo('b747_0', x=1360, y=640, w=820, rot=3, enter='slideR', at='747-400', cap='Boeing 747-400'),
    ]),
    dict(cue='A mesa da Varig', rate=0.006, items=[
        it(P.plane_group(8, 'varig', 1600, kinds=('jet', 'jumbo', 'tri', 'dc3')), x=960, y=480, enter='cut', subs=stagger(FLEET8, 'show', 0, step=0.1, d=0.3)),
    ]),
    dict(cue='Nessa época, a Varig era mais', items=[
        it(P.rose_big(520), x=700, y=520, enter='pop', sfx='paper'),
        label('quase um símbolo nacional', x=1360, y=520, size=56, at='símbolo'),
    ]),
    dict(cue='Tinha até avião pintado', sfx=[('Copa', 'crowd', 0.8)], items=[
        plane('jet', 'copa', x=640, y=440, w=820, enter='drop', at='pintado'),
        plane('jet', 'copa', x=1300, y=720, w=820, enter='drop', at='Copa', flip=True),
        it(P.ball(170), x=1580, y=280, enter='drop', at='Copa', sfx='pop'),
    ]),
]
# ---------------- 5. PERGUNTA ----------------
SUS = [P.suspect(P.gov_icon(260), 'O GOVERNO'), P.suspect(P.plane('jet', 'blank', 290), 'A CONCORRÊNCIA'), P.suspect(P.rose_big(220), 'A PRÓPRIA VARIG')]
S[4] = [
    dict(cue=None, rate=0.005, items=[
        it(P.rose_big(500), x=960, y=480, enter='cut'),
        typed('deveria ser impossível de quebrar', x=960, y=880, size=56, at='deveria'),
    ]),
    dict(cue='Então o que deu errado', rate=0.004, items=[
        stat('O QUE DEU ERRADO?', x=960, y=520, size=150),
    ]),
    dict(cue='Tem três suspeitos', items=[
        stat('3 SUSPEITOS', x=960, y=200, size=120, at='três'),
        it(SUS[0], x=450, y=620, enter='drop', at='O governo', sfx='clip', rot=-3),
        it(SUS[1], x=960, y=640, enter='drop', at='a concorrência', sfx='clip', rot=2),
        it(SUS[2], x=1470, y=620, enter='drop', at='a própria Varig', sfx='clip', rot=-2),
    ]),
    dict(cue='E o mais curioso', rate=0.006, items=[
        it(SUS[0], x=450, y=560, enter='cut', rot=-3), it(SUS[1], x=960, y=580, enter='cut', rot=2), it(SUS[2], x=1470, y=560, enter='cut', rot=-2),
        stamp('CULPA', x=450, y=640, size=70, at='culpa', rot=-10, shake=False),
        stamp('CULPA', x=960, y=660, size=70, at='culpa@0.25', rot=6, shake=False),
        stamp('CULPA', x=1470, y=640, size=70, at='culpa@0.5', rot=-4, shake=True),
    ]),
]
# ---------------- 6. PREÇO CONGELADO ----------------
S[5] = [
    dict(cue=None, items=[
        typed('o primeiro golpe', x=960, y=300, size=70),
        it(P.gov_icon(520), x=960, y=640, enter='drop', at='governo', sfx='thud'),
    ]),
    dict(cue='Em 1985 o Brasil', items=[
        stat('OUT/1985 A JAN/1992', x=960, y=170, size=100, yellow=True, at='1985'),
        label('inflação absurda', x=500, y=420, size=56, at='inflação'),
        it(P.pricetag('PASSAGEM', 600, lock=True), x=1000, y=620, enter='pop', at='preços', sfx='register', subs=[sub('.lock', 'drop', at='passagens', d=0.5, v=300, sfx='clip')]),
    ]),
    dict(cue='Só que o combustível', items=[
        it(P.pricetag('PASSAGEM', 420, lock=True), x=520, y=420, enter='cut'),
        it(P.thermo(220), x=1350, y=560, enter='pop', sfx='paper', subs=[sub('.merc', 'growy', at=0, d=0.1, v=[0.25, 0.25]), sub('.merc', 'growy', at='subindo', d=1.8, v=[0.25, 1.0])]),
        it(P.tag('COMBUSTÍVEL', '#f6d36b', 320), x=820, y=760, enter='drop', at='combustível', sfx='paper'),
        it(P.tag('PEÇAS', '#f6d36b', 260), x=520, y=820, enter='drop', at='peças', sfx='paper'),
        label('cotados em dólar', x=1350, y=180, size=56, at='dólar'),
    ]),
    dict(cue='Imagina ter uma lanchonete', rate=0.008, items=[
        it(P.sandwich(620), x=760, y=560, enter='pop', sfx='paper'),
        it(P.pricetag('R$ 5', 380, lock=True), x=760, y=250, enter='drop', at='mesmo preço', sfx='register'),
        it(P.tag('PÃO ↑', '#fffdf4', 240), x=1400, y=820, enter='pop', at='pão', sfx='pop', moves=[mv('pão@0.3', d=3.5, e='inout', y=420)]),
        it(P.tag('CARNE ↑', '#fffdf4', 260), x=1600, y=860, enter='pop', at='carne', sfx='pop', moves=[mv('carne@0.3', d=3.2, e='inout', y=300)]),
        it(P.tag('GÁS ↑', '#fffdf4', 240), x=1300, y=900, enter='pop', at='gás', sfx='pop', moves=[mv('gás@0.3', d=3.0, e='inout', y=200)]),
    ]),
    dict(cue='Você vende mais', items=[
        stat('VENDE MAIS', x=960, y=360, size=130, at='vende'),
        stat('PERDE MAIS', x=960, y=620, size=150, yellow=True, at='perde'),
        it(P.note(300), x=600, y=820, enter='cut', at='perde', moves=[mv('perde', d=1.2, e='in', x=-300, y=1200, r=-40)], sfx='coins'),
        it(P.note(300), x=1300, y=840, enter='cut', at='perde@0.2', moves=[mv('perde@0.2', d=1.2, e='in', x=2200, y=1250, r=50)]),
    ]),
    dict(cue='Foi isso que aconteceu', items=[
        stat('+ DE 6 ANOS', x=960, y=480, size=200, yellow=True, at='seis'),
    ]),
    dict(cue='E a Varig entrou na Justiça', items=[
        it(P.headline('Varig x União', 'Ação pede indenização pelo congelamento de tarifas', 'TRIBUNAL', ''), x=760, y=520, enter='flip', d=0.6, rot=-2, sfx='typewriter'),
        it(P.clock(380), x=1530, y=560, enter='pop', at='demorar', sfx='tick', subs=[sub('.hand', 'rot', at='demorar', d=2.5, v=[0, 1440], e='lin', origin='50% 100%'), sub('.hand2', 'rot', at='demorar', d=2.5, v=[0, 120], e='lin', origin='50% 100%')]),
        label('décadas', x=1530, y=860, size=56, at='décadas'),
    ]),
]
# ---------------- 7. O MUNDO MUDA ----------------
S[6] = [
    dict(cue=None, items=[
        it(P.clock(420), x=700, y=540, enter='pop', sfx='tick', subs=[sub('.hand', 'rot', at=0, d=2.0, v=[0, 1080], e='lin', origin='50% 100%')]),
        stat('ANOS 90', x=1350, y=480, size=170, yellow=True, at='90'),
    ]),
    dict(cue='O mercado aéreo brasileiro', items=[
        plane('jet', 'varig', x=960, y=540, w=760, enter='cut'),
        plane('jet', 'blank', x=360, y=280, w=520, enter='slideL', at='concorrentes', sfx='whoosh'),
        plane('jet', 'blank', x=1560, y=820, w=520, enter='slideR', at='concorrentes@0.2', flip=True),
        label('disputa de preço', x=960, y=180, size=52, at='disputar'),
    ]),
    dict(cue='Primeiro a TAM', items=[
        photo('tam_0', x=560, y=420, w=760, rot=-3, enter='slideL', at='TAM', cap='TAM'),
        photo('gol_0', x=1360, y=560, w=820, rot=3, enter='slideR', at='Gol', cap='Gol'),
        stat('2001', x=1500, y=170, size=120, yellow=True, at='2001'),
        label('passagem barata, avião cheio', x=760, y=880, size=50, at='barata'),
    ]),
    dict(cue='E é aqui que aquela fundação', items=[
        it(P.pie(0, 'Fundação Ruben Berta', people=True), x=960, y=480, enter='pop', sfx='paper', moves=[mv('pesar', d=0.8, e='bounce', y=600, r=8)]),
        label('começa a pesar', x=1480, y=860, size=56, at='pesar', sfx='creak'),
    ]),
    dict(cue='Uma decisão que a concorrente', items=[
        it(P.paperstack(12, 560), x=760, y=560, enter='cut', subs=[sub(f'.p{i}', 'drop', at=f'Uma decisão@{0.25*i:.2f}', d=0.3, v=200, sfx='stamp' if i % 3 == 0 else None) for i in range(12)]),
        stamp('AGUARDANDO APROVAÇÃO', x=760, y=560, size=60, at='aprovada', rot=-6, shake=False),
        plane('jet', 'gol', x=-300, y=200, w=420, enter='cut', at='poucos dias', moves=[mv('poucos dias', d=2.0, e='lin', x=2300, y=160)], sfx='whoosh', z=8),
        plane('jet', 'tam', x=-300, y=330, w=380, enter='cut', at='meses', moves=[mv('meses', d=2.0, e='lin', x=2300, y=300)], sfx='whoosh', z=8),
    ]),
    dict(cue='Na minha opinião', rate=0.006, items=[
        it(P.rose_big(460), x=700, y=520, enter='cut'),
        typed('a parte mais triste da história', x=1300, y=300, size=50, at='mais triste'),
        stamp('LENTA DEMAIS', x=1300, y=640, size=90, at='lenta', shake=False),
    ]),
    dict(cue='Em 1994 ela já tinha', items=[
        stat('1994', x=520, y=260, size=150, yellow=True, at='1994'),
        stamp('MORATÓRIA', x=960, y=520, size=150, at='moratória'),
        label('não ia conseguir pagar as dívidas em dia', x=960, y=860, size=46, at='não ia conseguir'),
    ]),
    dict(cue='Inclusive, foi nesse período', items=[
        it(P.box('VARIGLOG', 420), x=960, y=560, enter='drop', at='cargas', sfx='box', moves=[mv('Esse nome', d=0.8, x=1640, y=820, s=0.6)]),
        stat('1993', x=1500, y=250, size=130, yellow=True, at='1993'),
        label('a empresa de cargas', x=520, y=250, size=52, at='cargas'),
    ]),
    dict(cue='E mesmo com a moratória', items=[
        plane('jumbo', 'varig', x=900, y=560, w=1100, enter='slideL', sfx='turbine'),
        it(P.box('VARIGLOG', 420), x=1640, y=820, enter='cut', scale=0.6),
    ]),
    dict(cue='Em 1996 troca', items=[
        it(P.star_big(460), x=620, y=520, enter='spin', d=0.7, at='estrela', sfx='whoosh'),
        photo('varigtail_0', x=1340, y=520, w=860, rot=3, enter='slideR', at='marca', cap='a marca nova, com a estrela'),
        stat('1996', x=620, y=170, size=120, yellow=True, at='1996'),
    ]),
    dict(cue='Em 1997 entra', items=[
        label('STAR ALLIANCE · 1997', x=960, y=200, size=64, at='Star Alliance'),
        label('Lufthansa · United', x=960, y=330, size=48, at='Lufthansa'),
        it(P.pie(21, 'Condor Syndikat · 1927'), x=700, y=650, enter='pop', at='herdeira', sfx='paper', scale=0.8),
        stat('70 ANOS DEPOIS', x=1350, y=660, size=110, yellow=True, at='Setenta'),
    ]),
    dict(cue='E em 1998 faz', items=[
        it(P.plane_group(8, 'varig96', 1600, kinds=('jet', 'jumbo')), x=960, y=460, enter='cut', subs=stagger(FLEET8, 'show', 'encomenda', step=0.08, d=0.25, sfx='pop')),
        stat('39 AVIÕES', x=960, y=900, size=150, yellow=True, at='trinta e nove'),
    ]),
    dict(cue='Só que no ano seguinte', items=[
        it(P.chart(1100), x=900, y=520, enter='pop', sfx='paper', subs=[sub('.ln', 'draw', at='despenca', d=2.2, e='inout', sfx='swoosh')]),
        it(P.note(260), x=1600, y=300, enter='cut', at='sente isso', moves=[mv('sente isso', d=1.0, e='in', x=2300, y=-200, r=40)], sfx='coins'),
        it(P.note(260), x=1650, y=600, enter='cut', at='sente isso@0.15', moves=[mv('sente isso@0.15', d=1.0, e='in', x=2400, y=1300, r=-30)]),
        it(P.note(260), x=1500, y=850, enter='cut', at='sente isso@0.3', moves=[mv('sente isso@0.3', d=1.0, e='in', x=-300, y=1300, r=60)]),
    ]),
    dict(cue='Depois de 2001', items=[
        stat('2001', x=960, y=380, size=170, yellow=True, at='2001'),
        typed('a conta não fechava mais', x=960, y=680, size=64, at='conta'),
    ]),
    dict(cue='Em 2004 ainda', items=[
        it(P.rose_big(320), x=400, y=520, enter='cut', moves=[mv('fusão', d=0.8, x=780), mv('não andou', d=0.4, e='out', x=400)]),
        plane('jet', 'blank', x=1550, y=520, w=520, enter='cut', flip=True, moves=[mv('fusão', d=0.8, x=1180), mv('não andou', d=0.4, e='out', x=1550)]),
        stat('FUSÃO?', x=960, y=220, size=130, at='fusão'),
        stamp('NÃO ANDOU', x=960, y=820, size=90, at='não andou', shake=False),
    ]),
    dict(cue='E enquanto isso, a Gol', sfx=[('mesmo modelo', 'creak', 1.0)], items=[
        it(P.balance(1300), x=960, y=640, enter='pop', sfx='paper', subs=[sub('.beam', 'rot', at='mais barata', d=4.0, v=[0, -9], e='inout', origin='50% 6%')]),
        label('VARIG: aviões de vários tamanhos + dívida', x=700, y=150, size=34, at='E enquanto'),
        label('GOL: aviões iguais, passagem barata', x=1250, y=260, size=34, at='Gol crescia'),
    ]),
]
# ---------------- 8. QUEDA ----------------
S[7] = [
    dict(cue=None, sfx=[(0, 'typewriter', 0.8)], items=[
        it(P.headline('Varig pede recuperação judicial', 'Dívida chega a R$ 5,7 bilhões', 'O DIÁRIO', 'junho de 2005'), x=900, y=480, enter='flip', d=0.6, rot=-2),
        stat('R$ 5,7 BILHÕES', x=1300, y=900, size=130, yellow=True, at='cinco vírgula sete'),
    ]),
    dict(cue='Ela era uma das primeiras', items=[
        typed('a lei nova de recuperação judicial', x=960, y=440, size=60, at='lei nova'),
        label('em vigor desde junho de 2005', x=960, y=640, size=48, at='vigor'),
    ]),
    dict(cue='A ideia era ganhar tempo', items=[
        it(P.hourglass(330), x=700, y=540, enter='pop', sfx='paper', subs=[sub('svg', 'rot', at=0.1, d=0.6, v=[180, 360])]),
        stat('180 DIAS', x=1350, y=520, size=170, yellow=True, at='cento e oitenta'),
    ]),
    dict(cue='Só que o tempo não ajudou', items=[
        it(P.hourglass(330), x=700, y=540, enter='cut', subs=[sub('.sandtop', 'grow', at=0, d=1.4, v=[1, 0.05], e='in'), sub('.sandbot', 'grow', at=0, d=1.4, v=[0.4, 1.2])]),
        typed('o tempo não ajudou', x=1350, y=540, size=60, at='tempo'),
    ]),
    dict(cue='Para fazer dinheiro', items=[
        it(P.rose_big(380), x=960, y=520, enter='cut'),
        it(P.tag('CARGAS', '#f6d36b', 300), x=620, y=300, enter='pop', at='cargas', sfx='paper', moves=[mv('vão embora', d=0.8, e='in', x=-400, r=-30)]),
        it(P.tag('MANUTENÇÃO', '#f6d36b', 360), x=1340, y=760, enter='pop', at='manutenção', sfx='paper', moves=[mv('vão embora@0.2', d=0.8, e='in', x=2400, r=30)]),
        label('fim de 2005', x=960, y=900, size=48, at='fim de 2005'),
    ]),
    dict(cue='E em julho de 2006', items=[
        plane('jet', 'varig', x=960, y=560, w=900, enter='cut'),
        stamp('LEILOADA', x=960, y=560, size=150, at='leiloada'),
        stat('JULHO DE 2006', x=960, y=200, size=110, yellow=True, at='julho'),
    ]),
    dict(cue='Quem compra é a VarigLog', rate=0.008, items=[
        plane('jet', 'varig', x=900, y=520, w=760, enter='cut', moves=[mv('própria mãe', d=0.7, e='in', x=1500, y=760, s=0.05, r=20)]),
        it(P.box('VARIGLOG', 360), x=1500, y=780, enter='pop', at='VarigLog', sfx='box', subs=[sub('svg', 'grow', at='voltava', d=1.2, v=[1, 1.9])]),
        label('a filha comprou a mãe', x=640, y=200, size=56, at='própria mãe', sfx='box'),
    ]),
    dict(cue='No dia 28 de julho', sfx=[('demitidos', 'papers', 1.0)], items=[
        it(P.dominoes(14, 1600), x=960, y=620, enter='cut', subs=[sub(f'.d{i}', 'fall', at=f'demitidos@{i*0.09:.2f}', d=0.35, v=80, origin='100% 100%') for i in range(14)]),
        stat('+5.000 DEMITIDOS EM 1 DIA', x=960, y=220, size=110, yellow=True, at='cinco mil'),
    ]),
    dict(cue='Cinco dias depois', items=[
        it(P.globe(820), x=700, y=540, enter='cut', subs=stagger(ROUTES, 'draw', 0, step=0.0, d=0.01) + [sub('.cd', 'appear', at=0, d=0.1)]
           + stagger(ROUTES, 'undraw', 'último voo', step=0.08, d=0.4) + [sub('.cd', 'hide', at='último voo@1.5', d=0.4)]),
        stat('3 DE AGOSTO DE 2006', x=1360, y=300, size=90, yellow=True, at='3 de agosto'),
        label('último voo internacional', x=1360, y=480, size=48, at='último voo'),
    ]),
    dict(cue='Aquela empresa que voava', items=[
        it(P.brazil_dots(760, 12), x=700, y=540, enter='pop', sfx='paper', subs=stagger([f'.b{i}' for i in range(12)], 'show', 'doze', step=0.06, d=0.2)),
        stat('12 CIDADES', x=1380, y=540, size=150, yellow=True, at='doze'),
    ]),
    dict(cue='Em abril de 2007', items=[
        photo('gol_1', x=760, y=480, w=980, rot=-2, enter='slideL', at='Gol', cap='Gol'),
        stat('US$ 320 MILHÕES', x=1250, y=880, size=130, yellow=True, at='trezentos e vinte'),
        stat('2007', x=1580, y=200, size=110, yellow=True, at='2007'),
    ]),
    dict(cue='E a velha Varig', items=[
        it(P.rose_big(360), x=600, y=520, enter='cut'),
        label('FLEX', x=1300, y=380, size=90, at='Flex'),
        label('voos fretados até 2009', x=1300, y=600, size=50, at='fretados'),
    ]),
    dict(cue='Em agosto de 2010', rate=0.008, items=[
        it(P.rose_big(560, crumpled=True), x=960, y=520, enter='cut'),
        stamp('FALÊNCIA', x=960, y=540, size=200, at='falência', sub='AGOSTO DE 2010'),
    ]),
]
# ---------------- 9. O QUE SOBROU ----------------
S[8] = [
    dict(cue=None, rate=0.004, items=[
        it(P.rose_big(460, crumpled=True), x=960, y=520, enter='cut', rot=-6),
        typed('o processo das passagens congeladas', x=960, y=900, size=50, at='processo'),
    ]),
    dict(cue='Ele não morreu', items=[
        it(P.headline('Varig x União', 'Ação pelo congelamento de tarifas continua', 'TRIBUNAL', ''), x=960, y=520, enter='flip', d=0.6, rot=2, sfx='typewriter'),
    ]),
    dict(cue='Em 2014 o Supremo', items=[
        stat('2014', x=520, y=300, size=150, yellow=True, at='2014'),
        stamp('INDENIZAR', x=1100, y=520, size=150, at='indenizar', color=P.BLUE),
        label('decisão do STF', x=520, y=600, size=52, at='Supremo'),
    ]),
    dict(cue='E em 2024 o governo', rate=0.008, items=[
        it(P.cheque(1300), x=960, y=480, enter='slideR', at='acordo', sfx='paper'),
        stat('+ R$ 4 BILHÕES · 2024', x=960, y=900, size=110, yellow=True, at='quatro bilhões'),
    ]),
    dict(cue='Dinheiro que vai para pagar', items=[
        it(P.dominoes(12, 1400), x=960, y=640, enter='slideU', sfx='paper'),
        label('catorze anos depois', x=960, y=250, size=60, at='catorze'),
    ]),
    dict(cue='Só a parte do FGTS', items=[
        it(P.dominoes(14, 1600), x=960, y=640, enter='cut'),
        stat('17 MIL EX-FUNCIONÁRIOS', x=960, y=250, size=120, yellow=True, at='dezessete mil'),
    ]),
    dict(cue='Os mesmos funcionários', items=[
        it(P.pie(0, 'os donos da empresa', people=True), x=960, y=520, enter='pop', sfx='paper'),
        stat('1945', x=1500, y=220, size=130, yellow=True, at='1945'),
    ]),
    dict(cue='Ou seja, a Varig ganhou', rate=0.006, items=[
        it(P.cheque(1100), x=960, y=480, enter='cut'),
        stamp('GANHOU', x=960, y=480, size=130, at='ganhou', color=P.GREEN, shake=False),
        label('sem nenhum avião', x=960, y=880, size=60, at='nenhum avião'),
    ]),
    dict(cue='E tem uma última coisa', rate=0.006, items=[
        it(P.rose_big(360, crumpled=True), x=960, y=520, enter='cut'),
        typed('continua viva até hoje', x=960, y=880, size=60, at='continua viva'),
    ]),
    dict(cue='Em 1994, no mesmo ano', items=[
        stat('1994', x=960, y=360, size=170, yellow=True, at='1994'),
        label('um programa de milhagem', x=960, y=640, size=64, at='programa de milhagem'),
    ]),
    dict(cue='Esse programa foi junto', rate=0.01, items=[
        it(P.card(P.plane('jet', 'varig', 300), w=360, cap='?'), x=960, y=540, enter='slideR', d=0.6, sfx='swoosh', until='Smiles', exit='fade', ed=0.1),
        it(P.loyalty(860), x=960, y=540, enter='flip', d=0.5, at='Smiles', sfx='swoosh', impact='kick'),
    ]),
    dict(cue='Então toda vez', rate=0.008, items=[
        it(P.loyalty(700), x=620, y=520, enter='cut', rot=-4),
        photo('gol_0', x=1380, y=520, w=760, rot=3, enter='slideR', at='voando'),
        label('a única parte que nunca parou', x=960, y=900, size=52, at='única parte'),
    ]),
]
SHOTS = S
