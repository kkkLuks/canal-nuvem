# Som do vídeo: efeitos sintetizados, trilha sintetizada por fase e mixagem com a narração.
# Tudo gerado aqui (sem arquivos de terceiros), então não há licença a creditar.
import json, sys, subprocess, numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(1927)

def t_(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.005, r=0.2, shape=4.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / max(r, 1e-4) * 1.0)
    return e
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def noise(d): return rng.standard_normal(int(d * SR))
def norm(x, peak=0.9):
    m = np.max(np.abs(x)) or 1
    return x / m * peak

def s_paper():
    d = 0.32; n = noise(d); a = np.abs(lp(noise(d), 60)); a = a / a.max()
    x = bp(n, 1500, 7000) * a * env(len(n), 0.01, 0.12)
    return norm(x, 0.5)
def s_fold():
    x = np.concatenate([s_paper() * 0.8, s_paper()[: int(0.2 * SR)]]); return x
def s_thud():
    t = t_(0.35); x = np.sin(2 * np.pi * (70 + 40 * np.exp(-t * 30)) * t) * np.exp(-t * 14)
    x += lp(noise(0.35), 400) * np.exp(-t * 40) * 0.4
    return norm(x, 0.8)
def s_stamp():
    t = t_(0.4); x = np.sin(2 * np.pi * (95 + 60 * np.exp(-t * 40)) * t) * np.exp(-t * 18)
    x += bp(noise(0.4), 300, 3000) * np.exp(-t * 60) * 0.9
    x += bp(noise(0.4), 2000, 6000) * np.exp(-t * 120) * 0.3
    return norm(x, 0.95)
def s_swoosh():
    d = 0.4; t = t_(d); n = noise(d)
    lo = bp(n, 400, 1500); hi = bp(n, 1500, 6000)
    e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    x = (lo * (1 - t / d) + hi * (t / d)) * e
    return norm(x, 0.45)
def s_whoosh():
    d = 0.9; t = t_(d); n = lp(noise(d), 1800)
    e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 3
    return norm(n * e, 0.55)
def s_typewriter():
    out = np.zeros(int(1.0 * SR))
    for k in range(9):
        p = int((0.02 + k * 0.105 + rng.uniform(-0.02, 0.02)) * SR)
        c = bp(noise(0.03), 1800, 7000) * env(int(0.03 * SR), 0.001, 0.008)
        c += np.sin(2 * np.pi * 180 * t_(0.03)) * env(int(0.03 * SR), 0.001, 0.01) * 0.6
        out[p:p + len(c)] += c
    return norm(out, 0.55)
def s_register():
    t = t_(0.9); x = (np.sin(2 * np.pi * 2093 * t) + 0.6 * np.sin(2 * np.pi * 2637 * t) + 0.3 * np.sin(2 * np.pi * 4186 * t)) * np.exp(-t * 4)
    k = s_thud()[: len(t)]; x[: len(k)] += k * 0.6
    return norm(x, 0.55)
def s_coins():
    out = np.zeros(int(0.9 * SR))
    for k in range(7):
        p = int(rng.uniform(0, 0.6) * SR); f = rng.uniform(3000, 6500); t = t_(0.25)
        c = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.51 * t)) * np.exp(-t * 18)
        out[p:p + len(c)] += c
    return norm(out, 0.45)
def s_clip():
    t = t_(0.08); x = bp(noise(0.08), 2500, 9000) * np.exp(-t * 90) + np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 60) * 0.4
    return norm(x, 0.6)
def s_box():
    t = t_(0.4); x = np.sin(2 * np.pi * 140 * t) * np.exp(-t * 16) + lp(noise(0.4), 900) * np.exp(-t * 25) * 0.7
    return norm(x, 0.8)
def s_pop():
    t = t_(0.09); f = 700 * np.exp(-t * 18) + 250
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35), 0.4)
def s_tick():
    out = np.zeros(int(2.4 * SR))
    for k in range(8):
        p = int(k * 0.3 * SR); c = s_clip()[: int(0.05 * SR)] * (0.9 if k % 2 else 0.6); out[p:p + len(c)] += c
    return out * 0.7
def s_creak():
    d = 1.3; t = t_(d); f = 110 + 25 * np.sin(2 * np.pi * 1.3 * t) + 10 * np.sin(2 * np.pi * 7 * t)
    ph = np.cumsum(f) / SR; x = ((ph % 1) * 2 - 1)
    x = bp(x, 200, 1800) * np.sin(np.pi * t / d) ** 2
    return norm(x, 0.35)
def s_crowd():
    d = 2.8; t = t_(d); x = bp(noise(d), 300, 2500)
    x *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.8 * t + 1) ** 2
    return norm(x * np.sin(np.pi * t / d), 0.3)
def s_turbine():
    d = 4.5; t = t_(d); n = lp(noise(d), 2200)
    e = np.exp(-((t - d * 0.45) / (d * 0.28)) ** 2)
    f = 2600 - 900 * (t / d); whine = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.12
    return norm((n + whine) * e, 0.5)
def s_prop():
    d = 2.6; t = t_(d); pulse = (0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 22 * t)))
    x = lp(noise(d), 900) * pulse + np.sin(2 * np.pi * 66 * t) * 0.3
    return norm(x * np.sin(np.pi * t / d), 0.45)
def s_papers():
    out = np.zeros(int(1.8 * SR))
    for k in range(14):
        p = int((k * 0.09 + 0.05) * SR); c = s_paper(); out[p:p + len(c)] += c * 0.7
    return norm(out, 0.6)
def s_boom():
    t = t_(1.6); x = np.sin(2 * np.pi * (48 + 30 * np.exp(-t * 6)) * t) * np.exp(-t * 2.5) + lp(noise(1.6), 200) * np.exp(-t * 4) * 0.5
    return norm(x, 0.8)

SFX = {k[2:]: f for k, f in globals().items() if k.startswith('s_')}
VOL = dict(paper=0.5, fold=0.5, thud=0.6, stamp=0.75, swoosh=0.35, whoosh=0.45, typewriter=0.4, register=0.5, coins=0.45, clip=0.5,
           box=0.6, pop=0.35, tick=0.35, creak=0.5, crowd=0.35, turbine=0.5, prop=0.45, papers=0.55, boom=0.7)

# ---------- trilha ----------
def midi(n): return 440 * 2 ** ((n - 69) / 12)
def pad(freqs, d):
    t = t_(d); x = np.zeros_like(t)
    for f in freqs:
        for det in (-0.12, 0.0, 0.12):
            ph = 2 * np.pi * f * (1 + det / 100) * t + rng.uniform(0, 6.28)
            x += np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.1 * np.sin(3 * ph)
    a = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6)
    return lp(x * a, 2200) / (len(freqs) * 3)
def pluck(f, d=0.6):
    N = int(SR / f); buf = rng.uniform(-1, 1, N); out = np.zeros(int(d * SR))
    for i in range(len(out)):
        out[i] = buf[i % N]; buf[i % N] = 0.5 * (buf[i % N] + buf[(i + 1) % N]) * 0.996
    return out
PL = {}
def pluck_c(n, d=0.6):
    if (n, d) not in PL: PL[(n, d)] = pluck(midi(n), d)
    return PL[(n, d)]
def piano(n, d=2.5):
    f = midi(n); t = t_(d)
    x = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (1.2 + k * 0.8)) for k, a in [(1, 1), (2, 0.4), (3, 0.2), (4, 0.08)])
    return x * np.minimum(1, t / 0.005)

def music(kind, d):
    out = np.zeros(int(d * SR) + SR)
    if kind == 'auge':
        bpm = 100; beat = 60 / bpm; bar = 4 * beat
        prog = [[48, 52, 55, 60], [45, 52, 57, 60], [41, 53, 57, 60], [43, 55, 59, 62]]
        t = 0.0; i = 0
        while t < d:
            ch = prog[i % 4]; p = pad([midi(n) for n in ch[1:]], bar + 0.6); s = int(t * SR); out[s:s + len(p)] += p[: len(out) - s] * 0.5
            b = piano(ch[0] - 12, bar) * 0.35; out[s:s + len(b)] += b[: len(out) - s]
            for k in range(8):
                n = ch[[0, 2, 1, 3, 2, 1, 3, 2][k]] + 12; pl = pluck_c(n, 0.5) * 0.22; ps = int((t + k * beat / 2) * SR)
                out[ps:ps + len(pl)] += pl[: max(0, len(out) - ps)]
            for k in range(8):
                hs = int((t + k * beat / 2 + beat / 4) * SR); hh = hp(noise(0.05), 7000) * env(int(0.05 * SR), 0.001, 0.01) * 0.05
                out[hs:hs + len(hh)] += hh[: max(0, len(out) - hs)]
            t += bar; i += 1
    elif kind == 'virada':
        bpm = 88; beat = 60 / bpm; bar = 4 * beat
        prog = [[38, 50, 53, 57], [34, 50, 53, 58], [31, 50, 55, 58], [33, 49, 52, 57]]
        t = 0.0; i = 0
        while t < d:
            ch = prog[i % 4]; s = int(t * SR)
            p = pad([midi(n) for n in ch[1:]], bar + 0.6) * 0.45; out[s:s + len(p)] += p[: len(out) - s]
            for k in range(8):
                bs = int((t + k * beat / 2) * SR); b = np.sin(2 * np.pi * midi(ch[0]) * t_(0.22)) * env(int(0.22 * SR), 0.005, 0.08) * 0.35
                out[bs:bs + len(b)] += b[: max(0, len(out) - bs)]
                tk = bp(noise(0.03), 4000, 9000) * env(int(0.03 * SR), 0.001, 0.006) * 0.06; out[bs:bs + len(tk)] += tk[: max(0, len(out) - bs)]
            t += bar; i += 1
    elif kind == 'queda':
        bpm = 66; beat = 60 / bpm; bar = 4 * beat
        prog = [[45, 57, 60, 64], [41, 57, 60, 65], [36, 55, 60, 64], [40, 56, 59, 64]]
        mel = [76, 74, 72, 71, 72, 69, 67, 68]
        t = 0.0; i = 0
        while t < d:
            ch = prog[i % 4]; s = int(t * SR)
            p = pad([midi(n) for n in ch[1:]], bar + 0.6) * 0.35; out[s:s + len(p)] += p[: len(out) - s]
            b = piano(ch[0], bar) * 0.4; out[s:s + len(b)] += b[: len(out) - s]
            for k, n in enumerate([mel[(2 * i) % 8], mel[(2 * i + 1) % 8]]):
                ps = int((t + k * 2 * beat) * SR); pn = piano(n, 2 * beat + 1) * 0.22; out[ps:ps + len(pn)] += pn[: max(0, len(out) - ps)]
            t += bar; i += 1
    out = out[: int(d * SR)]
    return out / (np.max(np.abs(out)) or 1) * 0.8

def place(buf, x, at, g=1.0):
    s = int(at * SR)
    if s < 0: x = x[-s:]; s = 0
    e = min(len(buf), s + len(x)); buf[s:e] += x[: e - s] * g

def main(tlpath, out_wav, voice_dir='voz'):
    T = json.load(open(tlpath))
    total = T['total']; N = int(total * SR) + SR
    voice = np.zeros(N); fx = np.zeros(N); mus = np.zeros(N)
    for c, off in enumerate(T['film_off']):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{voice_dir}/cap{c}.mp3', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
        place(voice, np.frombuffer(raw, np.float32).astype(np.float64), off)
    cache = {}
    for s in T['sfx']:
        n = s['n']
        if n not in SFX: print('sfx desconhecido', n); continue
        if n not in cache or n in ('paper', 'coins', 'typewriter'): cache[n] = SFX[n]()
        place(fx, cache[n], s['t'], VOL.get(n, 0.5) * s.get('v', 1.0))
    # trilha por fase (capítulos): auge 0–4, virada 5–6, queda 7–8
    fo = T['film_off']; GAP = 1.4
    segs = [('auge', 0, fo[5] - GAP), ('virada', fo[5] - GAP, fo[7] - GAP), ('queda', fo[7] - GAP, T['total'])]
    XF = 1.2
    for kind, a, b in segs:
        m = music(kind, b - a + XF)
        f = np.ones(len(m)); nx = int(XF * SR)
        if a > 0: f[:nx] = np.linspace(0, 1, nx)
        f[-nx:] = np.linspace(1, 0, nx)
        place(mus, m * f, max(0, a - XF / 2))
    # silêncio da trilha (demissões) e corte final
    for w in T['words']:
        pass
    for s in T.get('mute', []):
        a, b = int(s[0] * SR), int(s[1] * SR); ramp = int(0.15 * SR)
        mus[a:b] = 0; mus[a - ramp:a] *= np.linspace(1, 0, ramp); mus[b:b + ramp] *= np.linspace(0, 1, ramp)
    endv = int(T['end'] * SR); mus[endv:] = 0; fx[endv + int(0.3 * SR):] = 0
    # ducking: trilha abaixa sob a voz
    ve = np.abs(voice); k = int(0.25 * SR); ve = np.convolve(ve, np.ones(k) / k, 'same'); ve = ve / (ve.max() or 1)
    duck = 1 - 0.55 * np.clip(ve * 6, 0, 1)
    duck = np.convolve(duck, np.ones(int(0.3 * SR)) / int(0.3 * SR), 'same')
    mix = voice * 1.0 + fx * 0.55 + mus * 0.16 * duck
    mix = mix / max(1.0, np.max(np.abs(mix)) / 0.95)
    import wave
    pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
    with wave.open(out_wav, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print('ok', out_wav, len(mix) / SR)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
