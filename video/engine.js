// Motor de cena do canal: tudo é função do tempo (determinístico), dirigido pelo timeline do HyperFrames.
(function () {
  const D = window.__SCENE;            // {offset, dur, items, cam:{shots,impacts,phases}, fps}
  const OFF = D.offset || 0;
  const STEP = 1 / 8;                  // stop motion a 8 FPS
  const clamp = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
  const lerp = (a, b, k) => a + (b - a) * k;
  const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
  const EASE = {
    lin: (x) => x,
    out: (x) => 1 - Math.pow(1 - x, 3),
    out5: (x) => 1 - Math.pow(1 - x, 5),
    in: (x) => x * x * x,
    inout: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
    back: (x) => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
    bounce: (x) => { const n1 = 7.5625, d1 = 2.75; if (x < 1 / d1) return n1 * x * x; if (x < 2 / d1) return n1 * (x -= 1.5 / d1) * x + 0.75; if (x < 2.5 / d1) return n1 * (x -= 2.25 / d1) * x + 0.9375; return n1 * (x -= 2.625 / d1) * x + 0.984375; },
  };
  const qt = (t) => Math.floor(t / STEP + 1e-6) * STEP;

  // pré-processa
  const els = {};
  const items = D.items;
  for (const it of items) {
    it.el = document.getElementById(it.id);
    it.subs = (it.subs || []).sort((a, b) => a.t - b.t);
    it.subEls = [];
    const groups = {};
    for (const s of it.subs) {
      const list = s.sel === ':self' ? [it.el] : Array.from(it.el.querySelectorAll(s.sel));
      s.list = list;
      for (const e of list) {
        if (s.k === 'draw' && e.getTotalLength) { e.__len = e.getTotalLength(); e.style.strokeDasharray = e.__len + ' ' + e.__len; }
        if (s.origin) e.style.transformOrigin = s.origin;
        if (!e.__subs) { e.__subs = []; it.subEls.push(e); }
        e.__subs.push(s);
      }
    }
    it.seed = hash(it.id.length * 13.7 + (it.t0 || 0));
  }

  function enterState(it, lt) {
    const en = it.enter || { k: 'cut', d: 0 };
    const d = en.d || 0.5;
    const p = d ? clamp(lt / d) : 1;
    const st = { dx: 0, dy: 0, s: 1, r: 0, o: 1, ry: 0 };
    if (p >= 1 && en.k !== 'slam') return st;
    switch (en.k) {
      case 'slideL': st.dx = -lerp(1500, 0, EASE.out(p)); break;
      case 'slideR': st.dx = lerp(1500, 0, EASE.out(p)); break;
      case 'slideU': st.dy = -lerp(1000, 0, EASE.out(p)); break;
      case 'slideD': st.dy = lerp(1000, 0, EASE.out(p)); break;
      case 'drop': st.dy = -lerp(700, 0, EASE.bounce(p)); st.r = lerp(-8, 0, p); break;
      case 'pop': st.s = Math.max(0.0001, EASE.back(p)); break;
      case 'fade': st.o = p; break;
      case 'flip': st.ry = lerp(90, 0, EASE.out(p)); st.s = lerp(0.6, 1, EASE.out(p)); break;
      case 'spin': st.r = lerp(-200, 0, EASE.out(p)); st.s = Math.max(0.0001, EASE.out(p)); break;
      case 'slam': { const f = clamp(lt / 0.1); st.s = lerp(2.6, 1, EASE.in(f)); st.o = f > 0 ? 1 : 0; break; }
      case 'type': st.o = 1; break;
      default: break;
    }
    return st;
  }
  function exitState(it, t) {
    const ex = it.exit; if (!ex) return null;
    const d = ex.d || 0.3; const p = clamp((t - (it.t1 - d)) / d); if (p <= 0) return null;
    const st = { dx: 0, dy: 0, s: 1, o: 1, r: 0 };
    switch (ex.k) {
      case 'slideL': st.dx = -1600 * EASE.in(p); break;
      case 'slideR': st.dx = 1600 * EASE.in(p); break;
      case 'slideD': st.dy = 1100 * EASE.in(p); break;
      case 'slideU': st.dy = -1100 * EASE.in(p); break;
      case 'fade': st.o = 1 - p; break;
      case 'shrink': st.s = 1 - EASE.in(p) * 0.999; break;
    }
    return st;
  }
  function movesState(it, lt) {
    // moves: [{t (local), d, x,y,r,s, e}] valores absolutos alvo
    let x = it.x, y = it.y, r = it.rot || 0, s = it.scale || 1, o = 1;
    for (const m of it.moves || []) {
      const p = m.d ? clamp((lt - m.t) / m.d) : lt >= m.t ? 1 : 0;
      if (p <= 0) continue;
      const e = (EASE[m.e || 'out'])(p);
      if (m.x !== undefined) x = lerp(x, m.x, e);
      if (m.y !== undefined) y = lerp(y, m.y, e);
      if (m.r !== undefined) r = lerp(r, m.r, e);
      if (m.s !== undefined) s = lerp(s, m.s, e);
      if (m.o !== undefined) o = lerp(o, m.o, e);
    }
    return { x, y, r, s, o };
  }
  function applySubs(e, lt, it) {
    const st = {};
    for (const s of e.__subs) {
      const t0 = s.t; const d = s.d || 0.4; const raw = (lt - t0) / d; const p = clamp(raw);
      const started = lt >= t0;
      const set = (k, v0, v1, ease) => { if (!started) { if (!(k in st)) st[k] = v0; } else st[k] = lerp(v0, v1, (EASE[ease || s.e || 'out'])(p)); };
      switch (s.k) {
        case 'show': set('o', 0, 1, 'lin'); set('sc', 0.0001, 1, 'back'); break;
        case 'appear': set('o', 0, 1, 'lin'); break;
        case 'hide': set('o', 1, 0, 'lin'); break;
        case 'drop': set('o', 0, 1, 'lin'); set('ty', -(s.v || 400), 0, 'bounce'); break;
        case 'fall': set('ro', 0, s.v || 90, 'in'); break;
        case 'grow': set('sc', s.v[0], s.v[1]); break;
        case 'growy': set('sy', s.v[0], s.v[1]); break;
        case 'rot': set('ro', s.v[0], s.v[1]); break;
        case 'move': set('tx', s.v[0], s.v[2]); set('ty', s.v[1], s.v[3]); break;
        case 'draw': set('dash', 1, 0, s.e || 'inout'); break;
        case 'undraw': set('dash', 0, 1, 'in'); break;
        case 'fadeTo': set('o', s.v[0], s.v[1], 'lin'); break;
      }
    }
    let tr = '';
    if ('tx' in st || 'ty' in st) tr += `translate(${(st.tx || 0).toFixed(1)}px,${(st.ty || 0).toFixed(1)}px) `;
    if ('ro' in st) tr += `rotate(${st.ro.toFixed(2)}deg) `;
    if ('sc' in st) tr += `scale(${Math.max(0.0001, st.sc).toFixed(4)})`;
    if ('sy' in st) tr += ` scaleY(${Math.max(0.0001, st.sy).toFixed(4)})`;
    if (tr) e.style.transform = tr;
    if ('o' in st) e.style.opacity = st.o.toFixed(3);
    if ('dash' in st && e.__len) e.style.strokeDashoffset = (st.dash * e.__len).toFixed(1);
  }

  // câmera
  const cam = document.getElementById('cam');
  const grade = document.getElementById('grade');
  const warm = document.getElementById('warm');
  const cold = document.getElementById('cold');
  const dark = document.getElementById('dark');
  const grain = document.getElementById('grainl');
  const paper = document.getElementById('paperbg');
  const C = D.cam;
  const PH = { auge: { sat: 1.12, bri: 1.0, sep: 0.08, warm: 0.22, cold: 0, dark: 0 }, virada: { sat: 0.78, bri: 0.97, sep: 0.0, warm: 0, cold: 0.28, dark: 0.05 }, queda: { sat: 0.35, bri: 0.92, sep: 0.05, warm: 0, cold: 0.12, dark: 0.1 }, preto: { sat: 0, bri: 0, sep: 0, warm: 0, cold: 0, dark: 1 } };
  function phaseAt(t) {
    let cur = PH[C.phases[0].p], prev = cur, p = 1;
    for (let i = 0; i < C.phases.length; i++) {
      const ph = C.phases[i];
      if (t >= ph.t) { prev = i ? PH[C.phases[i - 1].p] : PH[ph.p]; cur = PH[ph.p]; p = clamp((t - ph.t) / (ph.d || 0.27)); }
    }
    const o = {}; for (const k in cur) o[k] = lerp(prev[k], cur[k], p); return o;
  }
  function camAt(t) {
    let sh = null; for (const s of C.shots) if (t >= s.t0 && t < s.t1) sh = s;
    let sc = 1, fx = 960, fy = 540, tx = 0, ty = 0;
    if (sh) {
      const lt = t - sh.t0;
      sc = (sh.s0 || 1.0) + (sh.rate === undefined ? 0.012 : sh.rate) * lt;
      fx = sh.fx || 960; fy = sh.fy || 540;
      if (sh.pan) { tx = lerp(0, sh.pan[0], EASE.inout(clamp(lt / (sh.t1 - sh.t0)))); ty = lerp(0, sh.pan[1], EASE.inout(clamp(lt / (sh.t1 - sh.t0)))); }
    }
    for (const im of C.impacts) {
      const lt = t - im.t; if (lt < 0 || lt > 0.5) continue;
      const f = Math.floor(lt * 30);
      if (im.k === 'kick' && f < 10) sc *= 1 + (im.v || 0.05) * Math.pow(1 - f / 10, 2);
      if (im.k === 'shake' && f < 7) { const a = (im.v || 14) * (1 - f / 7); tx += (f % 2 ? 1 : -1) * a; ty += (f % 2 ? -0.6 : 0.6) * a; }
    }
    return { sc, fx, fy, tx, ty };
  }

  function render(T) {
    const t = T + OFF;
    // câmera
    const c = camAt(t);
    cam.style.transformOrigin = `${c.fx}px ${c.fy}px`;
    cam.style.transform = `translate(${c.tx.toFixed(1)}px,${c.ty.toFixed(1)}px) scale(${c.sc.toFixed(4)})`;
    const ph = phaseAt(t);
    grade.style.filter = `saturate(${ph.sat.toFixed(3)}) brightness(${ph.bri.toFixed(3)}) sepia(${ph.sep.toFixed(3)})`;
    warm.style.opacity = ph.warm.toFixed(3); cold.style.opacity = ph.cold.toFixed(3); dark.style.opacity = ph.dark.toFixed(3);
    const g8 = Math.floor(t * 8);
    grain.style.backgroundPosition = `${Math.floor(hash(g8) * 512)}px ${Math.floor(hash(g8 + 9) * 512)}px`;
    paper.style.transform = `translate(${((hash(g8 * 3) - 0.5) * 3).toFixed(1)}px,${((hash(g8 * 5) - 0.5) * 3).toFixed(1)}px)`;
    // itens
    for (const it of items) {
      const vis = t >= it.t0 && t < it.t1;
      if (!vis) { if (it.el.style.display !== 'none') it.el.style.display = 'none'; continue; }
      it.el.style.display = '';
      const raw = t - it.t0;
      const lt = it.step === false ? raw : qt(raw);
      const en = it.enter && it.enter.k === 'slam' ? enterState(it, raw) : enterState(it, lt);
      const mv = movesState(it, lt);
      const ex = exitState(it, it.step === false ? t : it.t0 + lt);
      let x = mv.x + en.dx, y = mv.y + en.dy, r = mv.r + en.r, s = mv.s * en.s, o = en.o * mv.o;
      if (ex) { x += ex.dx; y += ex.dy; s *= ex.s; o *= ex.o; r += ex.r; }
      if (it.jit !== false) { const k = Math.floor(t * 8) + it.seed * 1000; x += (hash(k) - 0.5) * 2.4; y += (hash(k + 1) - 0.5) * 2.4; r += (hash(k + 2) - 0.5) * 0.5; }
      let tr = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) translate(-50%,-50%)`;
      if (en.ry) tr += ` perspective(1400px) rotateY(${en.ry.toFixed(1)}deg)`;
      tr += ` rotate(${r.toFixed(2)}deg) scale(${Math.max(0.0001, s).toFixed(4)})`;
      it.el.style.transform = tr;
      it.el.style.opacity = o.toFixed(3);
      if (it.kb) { const img = it.el.querySelector('.kb'); if (img) { const p = clamp(raw / Math.max(1, it.t1 - it.t0)); img.style.transform = `scale(${lerp(it.kb[0], it.kb[1], p).toFixed(4)}) translate(${lerp(0, it.kb[2] || 0, p).toFixed(1)}px,${lerp(0, it.kb[3] || 0, p).toFixed(1)}px)`; } }
      if (it.type && it.type.startsWith('typew')) {
        const tx = it.el.querySelector('.tw'); const full = tx.getAttribute('data-full'); const n = Math.min(full.length, Math.floor(raw * (it.cps || 22)));
        tx.textContent = full.slice(0, n);
      }
      for (const e of it.subEls) applySubs(e, lt, it);
    }
  }

  const tl = gsap.timeline({ paused: true });
  const P = { v: 0 };
  tl.to(P, { v: 1, duration: D.dur, ease: 'none', onUpdate: () => render(tl.time()) }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines['main'] = tl;
  render(0);
})();
