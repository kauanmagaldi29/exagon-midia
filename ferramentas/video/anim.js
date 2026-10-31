// deterministic timeline: window.renderAt(t)
const OFF = 0.3;
const TM = window.TIMING;
const S = i => TM.segs[i].wt[0] + OFF;
const WT = (i, j) => TM.segs[i].wt[Math.min(j, TM.segs[i].wt.length - 1)] + OFF;
const DURATION = TM.audio_end + OFF + 2.3;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const prog = (t, a, b) => clamp((t - a) / (b - a));
const eio = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const eout = x => 1 - Math.pow(1 - x, 3);
const eback = x => { const c1 = 1.6, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const $ = id => document.getElementById(id);

// ---- captions
function parseSeg(s) {
  let hl = false;
  return s.split(' ').map(tok => {
    let html = '', buf = '';
    const flush = () => { if (buf) { html += hl ? `<span class="hl">${buf}</span>` : buf; buf = ''; } };
    for (const ch of tok) { if (ch === '*') { flush(); hl = !hl; } else buf += ch; }
    flush(); return html;
  });
}
const capEl = $('cap');
const segEls = window.SEGS.map(s => {
  const d = document.createElement('div'); d.className = 'seg';
  d.innerHTML = parseSeg(s).map(h => `<span class="w">${h}</span>`).join(' ');
  capEl.appendChild(d); return { d, ws: [...d.querySelectorAll('.w')] };
});
let activeSeg = -2;
function captions(t, hidden, dark) {
  let k = -1;
  for (let i = 0; i < segEls.length; i++) if (t >= S(i) - 0.02) k = i;
  if (hidden) k = -1;
  if (k !== activeSeg) { segEls.forEach((e, i) => e.d.style.display = i === k ? 'block' : 'none'); activeSeg = k; }
  capEl.classList.toggle('on-dark', dark);
  $('capbg').style.opacity = dark || hidden ? 0 : 1;
  if (k < 0) return;
  const wt = TM.segs[k].wt;
  segEls[k].ws.forEach((el, j) => {
    const p = eout(prog(t, wt[j] + OFF - 0.04, wt[j] + OFF + 0.16));
    el.style.opacity = p.toFixed(3); el.style.transform = `translateY(${((1 - p) * 14).toFixed(1)}px)`;
  });
}

// ---- element animation
function show(id, t, a, b, o = {}) {
  const el = typeof id === 'string' ? $(id) : id;
  const inD = o.inD ?? 0.45, outD = o.outD ?? 0.3;
  if (t < a || t > b + outD) { el.style.visibility = 'hidden'; el.style.opacity = 0; return 0; }
  el.style.visibility = 'visible';
  const i = clamp((t - a) / inD), out = 1 - clamp((t - b) / outD);
  const kind = o.kind || 'pop';
  let tr = '';
  if (kind === 'pop') { const s0 = o.s0 ?? 0.55; tr = `scale(${((s0 + (1 - s0) * eback(i)) * (0.9 + 0.1 * out)).toFixed(4)})`; }
  if (kind === 'up') tr = `translateY(${((1 - eout(i)) * (o.dy ?? 90) - (1 - out) * 40).toFixed(1)}px)`;
  if (kind === 'down') tr = `translateY(${(-(1 - eout(i)) * (o.dy ?? 120)).toFixed(1)}px) scale(${(0.94 + 0.06 * out).toFixed(3)})`;
  if (kind === 'right') tr = `translateX(${((1 - eout(i)) * (o.dx ?? 260)).toFixed(1)}px)`;
  const bob = o.bob ? Math.sin((t - a) * 1.7 + (o.ph || 0)) * o.bob : 0;
  el.style.transform = `translate(-50%,-50%) translateY(${bob.toFixed(1)}px) ${tr}`;
  el.style.opacity = (Math.min(1, i * 1.7) * out).toFixed(3);
  return i;
}
const fmt = n => Math.round(n).toLocaleString('pt-BR');

// ---- scene windows
const SC = {
  A: [0, S(1) - 0.3], B: [S(1) - 0.15, S(3) - 0.3], C: [S(3) - 0.15, S(5) - 0.3], D: [S(5) - 0.15, S(7) - 0.3],
  E: [S(7) - 0.15, S(9) - 0.3], F: [S(9) - 0.15, S(11) - 0.5], H: [S(12) + 0.1, S(13) - 0.3], I: [S(13) - 0.15, S(15) - 0.3],
  J: [S(15) - 0.15, S(17) - 0.3], K: [S(17) - 0.15, S(19) - 0.3], L: [S(19) - 0.15, S(23) - 0.5],
};

// ---- sfx cue list (read by the sound builder)
const SFX = []; const sfx = (t, k, v = 1) => SFX.push({ t: +t.toFixed(3), k, v });
sfx(0.12, 'pop', 0.9); [0, 1, 2, 3].forEach(k => sfx(0.5 + k * 0.12, 'pop', 0.45));
sfx(WT(0, 4) - 0.1, 'swish', 0.6);
sfx(S(1) + 0.1, 'whoosh', 0.6); sfx(S(1) + 0.15, 'pop', 0.7); sfx(WT(1, 3) + 0.25, 'thump', 0.6);
sfx(S(2), 'pop', 0.8); [0, 1, 2].forEach(k => sfx(WT(2, 2) - 0.05 + k * 0.25, 'tick', 0.8)); sfx(WT(2, 4), 'drop', 0.7);
sfx(S(3), 'whoosh', 0.6); sfx(S(3) + 0.05, 'pop', 0.7); sfx(WT(3, 5), 'err', 0.8);
sfx(S(4), 'swish', 0.6); for (let k = 0; k < 10; k++) sfx(S(4) + k * 0.12, 'tick', 0.3);
sfx(S(5) - 0.1, 'whoosh', 0.6); sfx(S(5), 'pop', 0.7);
[WT(5, 2), S(6), WT(6, 3)].forEach(t => { sfx(t, 'swish', 0.6); sfx(t + 0.25, 'coin', 0.5); });
sfx(S(7), 'whoosh', 0.6); sfx(S(7) + 0.1, 'ding', 0.8); sfx(WT(7, 4), 'pop', 0.7); sfx(WT(8, 1), 'thump', 0.8);
sfx(S(9), 'whoosh', 0.6); sfx(S(9) + 0.05, 'pop', 0.7); sfx(S(10), 'swish', 0.5);
[WT(10, 2), WT(10, 3), WT(10, 5)].forEach(t => sfx(t, 'coin', 0.45));
sfx(S(11) - 0.3, 'whoosh', 1.0); sfx(WT(11, 4), 'thump', 1.0);
sfx(S(12) - 0.2, 'whoosh', 0.9); sfx(S(12) + 0.15, 'shimmer', 0.9);
sfx(S(13) - 0.1, 'whoosh', 0.6); sfx(S(13), 'pop', 0.7); sfx(WT(13, 1), 'pop', 0.6); sfx(S(14), 'pop', 0.6); sfx(S(14) + 0.1, 'ding', 0.8); sfx(WT(14, 3), 'pop', 0.8);
sfx(S(15) - 0.1, 'whoosh', 0.6); sfx(S(15), 'pop', 0.7); [WT(15, 0) + 0.1, WT(15, 3), WT(15, 4)].forEach(t => sfx(t, 'beep', 0.6)); sfx(WT(16, 1), 'drop', 0.6);
sfx(S(17) - 0.1, 'whoosh', 0.6); sfx(S(17), 'pop', 0.6); sfx(WT(17, 0) + 0.6, 'msg', 0.8); sfx(WT(17, 2), 'pop', 0.6); sfx(WT(17, 4), 'thump', 0.7); sfx(S(18) + 0.1, 'pop', 0.7);
sfx(S(19) - 0.1, 'whoosh', 0.6); sfx(S(19), 'pop', 0.7);
[[S(20) - 0.1, WT(20, 1) + 0.1], [S(21) - 0.1, WT(21, 1)], [S(22) - 0.1, WT(22, 5)]].forEach(([a, c]) => { sfx(a, 'pop', 0.5); sfx(c, 'check', 0.9); });
sfx(S(23) - 0.35, 'whoosh', 1.0); sfx(WT(23, 1), 'thump', 1.0);
for (let k = 0; k < 5; k++) sfx(S(24) + 0.12 + k * 0.17, 'key', 0.8);
sfx(S(24) + 1.15, 'send', 0.9); sfx(S(24) + 1.3, 'shimmer', 0.6);

// ---- render
function render(t) {
  // camera-ish drift
  $('stage').style.transform = `scale(${(1.012 + 0.012 * Math.sin(t * 0.33)).toFixed(4)}) translateY(${(Math.sin(t * 0.27) * 6).toFixed(1)}px)`;
  $('dots').style.transform = `translate(${(-(t * 7) % 44).toFixed(1)}px, ${(-(t * 4) % 44).toFixed(1)}px)`;

  // A · hook
  {
    const [a, b] = SC.A;
    show('aIcon', t, 0.1, b, { bob: 6 });
    ['aSat1', 'aSat2', 'aSat3', 'aSat4'].forEach((id, k) => show(id, t, 0.45 + k * 0.12, b, { bob: 5, ph: k }));
    const c0 = WT(0, 4) - 0.15;
    show('aChart', t, c0, b, { kind: 'up' });
    $('aLine').style.strokeDashoffset = (800 * (1 - eio(prog(t, c0 + 0.1, c0 + 1.1)))).toFixed(1);
  }
  // B · fechaduras
  {
    const [a, b] = SC.B;
    show('bKey', t, S(1) - 0.05, b, { bob: 5 });
    const x = clamp((t - (WT(1, 3) + 0.2)) / 0.3); $('bKeyX').style.transform = `scale(${t < WT(1, 3) + 0.2 ? 0 : eback(x).toFixed(3)})`;
    show('bLock', t, S(2) - 0.05, b, { bob: 5, ph: 1 });
    $('bLed').style.opacity = (0.35 + 0.65 * (Math.sin(t * 9) > 0 ? 1 : 0)).toFixed(2);
    ['bG1', 'bG2', 'bG3'].forEach((id, k) => show(id, t, WT(2, 2) - 0.05 + k * 0.25, b, { kind: 'up' }));
    show('bWarn', t, WT(2, 4) - 0.05, b, { kind: 'down' });
  }
  // C · sistema + site
  {
    const [a, b] = SC.C;
    show('cWin', t, S(3) - 0.08, b);
    $('cSpin').style.transform = `rotate(${(t * 300) % 360}deg)`;
    const e = clamp((t - WT(3, 5)) / 0.35); $('cErr').style.opacity = e.toFixed(3); $('cErr').style.transform = `translateY(${((1 - eout(e)) * 30).toFixed(1)}px)`;
    show('cFun', t, S(4) - 0.05, b, { kind: 'up' });
    $('cVis').textContent = fmt(384 * eio(prog(t, S(4), S(4) + 1.3)));
  }
  // D · taxas
  {
    const [a, b] = SC.D;
    show('dTot', t, S(5) - 0.05, b);
    $('dTotV').textContent = '−R$ ' + fmt(1870 * eio(prog(t, WT(5, 2), WT(6, 3) + 0.9)));
    [WT(5, 2), S(6), WT(6, 3)].forEach((t0, k) => show('dR' + (k + 1), t, t0 - 0.05, b, { kind: 'right' }));
  }
  // E · última hora
  {
    const [a, b] = SC.E;
    show('eNote', t, S(7) - 0.08, b, { kind: 'down' });
    show('eClock', t, WT(7, 4) - 0.1, b);
    const m = 41 + Math.floor(6 * prog(t, WT(7, 4), S(9) - 0.6)); $('eClockV').textContent = '23:' + String(m).padStart(2, '0');
    show('eYou', t, WT(8, 1) - 0.05, b);
  }
  // F · contratar
  {
    const [a, b] = SC.F;
    show('fHire', t, S(9) - 0.08, b, { bob: 4 });
    show('fRec', t, S(10) - 0.1, b, { kind: 'up' });
    [WT(10, 2), WT(10, 3), WT(10, 5)].forEach((t0, k) => { const p = clamp((t - t0 + 0.05) / 0.3); const el = $('fL' + (k + 1)); el.style.opacity = p.toFixed(3); el.style.transform = `translateX(${((1 - eout(p)) * 40).toFixed(1)}px)`; });
  }
  // G · wipe "Tá na hora de mudar."
  let wipeCover = 0;
  {
    const a = S(11) - 0.3, b = S(12) - 0.2;
    const xin = eio(prog(t, a, a + 0.42)), xout = eio(prog(t, b, b + 0.42));
    const x = t < b ? 100 * (1 - xin) : -100 * xout;
    $('wipe').style.transform = `translateX(${x.toFixed(2)}%)`;
    wipeCover = t > a + 0.2 && t < b + 0.2 ? 1 : 0;
    const p1 = clamp((t - S(11)) / 0.35), p2 = clamp((t - (WT(11, 4) - 0.05)) / 0.4);
    $('gT1').style.opacity = p1.toFixed(3); $('gT1').style.transform = `translateY(${((1 - eout(p1)) * 40).toFixed(1)}px)`;
    $('gT2').style.opacity = Math.min(1, p2 * 1.8).toFixed(3); $('gT2').style.transform = `scale(${(0.6 + 0.4 * eback(p2)).toFixed(4)})`;
  }
  // H · brand
  show('hBrand', t, SC.H[0], SC.H[1]);
  // I · reserva direta
  {
    const [a, b] = SC.I;
    show('iPhone', t, S(13) - 0.05, b, { bob: 5 });
    const sw = clamp((t - (S(14) + 0.05)) / 0.3); $('iScrA').style.opacity = (1 - sw).toFixed(3); $('iScrB').style.opacity = sw.toFixed(3);
    show('iC1', t, WT(13, 1) - 0.05, b, { kind: 'right' });
    show('iC2', t, S(14) - 0.05, b, { kind: 'right' });
    show('iC3', t, WT(14, 3) - 0.05, b, { kind: 'pop' });
  }
  // J · senha nova
  {
    const [a, b] = SC.J;
    show('jLock', t, S(15) - 0.05, b, { bob: 5 });
    const g = [WT(15, 0) + 0.1, WT(15, 3), WT(15, 4)];
    ['jG1', 'jG2', 'jG3'].forEach((id, k) => show(id, t, g[k] - 0.05, b, { kind: 'right', dx: -220 }));
    const ex = WT(16, 1);
    let code = '4827'; if (t >= g[1]) code = '1593'; if (t >= g[2]) code = '7064'; if (t >= ex) code = '----';
    $('jLockScr').textContent = code;
    $('jLed').style.background = t >= ex ? '#555' : '#3DDC84';
    const st = clamp((t - ex) / 0.35);
    $('jG1n').style.textDecoration = st > 0.5 ? 'line-through' : 'none';
    $('jG1c').style.opacity = (1 - 0.45 * st).toFixed(3);
    show('jExp', t, ex - 0.05, b, { kind: 'up' });
  }
  // K · 24h
  {
    const [a, b] = SC.K;
    show('kChat', t, S(17) - 0.05, b, { kind: 'down' });
    const an = clamp((t - (WT(17, 0) + 0.6)) / 0.3); $('kAns').style.opacity = an.toFixed(3); $('kAns').style.transform = `translateY(${((1 - eout(an)) * 20).toFixed(1)}px)`;
    show('kTotem', t, WT(17, 2) - 0.05, b, { bob: 5 });
    show('k24', t, WT(17, 4) - 0.1, b, { bob: 6, ph: 2 });
    show('kSleep', t, S(18) + 0.05, b, { kind: 'up' });
  }
  // L · checklist
  {
    const [a, b] = SC.L;
    show('lTitle', t, S(19) - 0.05, b);
    [[S(20) - 0.1, WT(20, 1) + 0.1], [S(21) - 0.1, WT(21, 1)], [S(22) - 0.1, WT(22, 5)]].forEach(([a0, c], k) => {
      const el = $('lR' + (k + 1)); show(el, t, a0, b, { kind: 'up' });
      const box = el.querySelector('.box'), ck = box.querySelector('svg');
      const p = clamp((t - c) / 0.3);
      box.style.background = p > 0 ? '#1F4D3A' : 'transparent'; box.style.borderColor = p > 0 ? '#1F4D3A' : '#D9D2C7';
      ck.style.opacity = p.toFixed(3); ck.style.transform = `scale(${(0.4 + 0.6 * eback(p)).toFixed(3)})`;
    });
  }
  // M · CTA
  let ctaDark = 0;
  {
    const a = S(23) - 0.35, x = eio(prog(t, a, a + 0.42));
    $('wipe2').style.transform = `translateX(${(100 * (1 - x)).toFixed(2)}%)`;
    ctaDark = t > a + 0.25 ? 1 : 0;
    const k = clamp((t - (S(23) - 0.05)) / 0.35), q = clamp((t - (WT(23, 1) - 0.08)) / 0.42);
    $('mK').style.opacity = k.toFixed(3); $('mK').style.transform = `translateY(${((1 - eout(k)) * 30).toFixed(1)}px)`;
    $('mQ').style.opacity = Math.min(1, q * 1.8).toFixed(3); $('mQ').style.transform = `scale(${(0.6 + 0.4 * eback(q)).toFixed(4)})`;
    const bx = clamp((t - (S(24) - 0.1)) / 0.4); $('mBox').style.opacity = bx.toFixed(3); $('mBox').style.transform = `translateY(${((1 - eout(bx)) * 50).toFixed(1)}px)`;
    const n = Math.max(0, Math.min(5, Math.floor((t - (S(24) + 0.12)) / 0.17) + 1)); $('mTyped').textContent = 'QUERO'.slice(0, t < S(24) + 0.12 ? 0 : n);
    $('mCaret').style.opacity = Math.sin(t * 12) > 0 ? 1 : 0;
    const sent = t > S(24) + 1.15; $('mSend').style.background = sent ? '#FF4F1F' : '#E6E0D6';
    $('mSend').style.transform = `scale(${sent ? (1 + 0.15 * Math.max(0, Math.sin(Math.min(1, (t - S(24) - 1.15) / 0.3) * Math.PI))).toFixed(3) : 1})`;
    const lg = clamp((t - (S(24) + 0.3)) / 0.5); $('mLogo').style.opacity = lg.toFixed(3);
  }
  captions(t, wipeCover === 1, ctaDark === 1);
}

async function boot() {
  await Promise.all([400, 500, 600, 700, 800].map(w => document.fonts.load(`${w} 40px Outfit`)));
  await document.fonts.ready;
  window.DURATION = DURATION; window.SFX = SFX;
  window.renderAt = t => { render(t); return true; };
  render(0.01);
  window.READY = true;
}
boot();
