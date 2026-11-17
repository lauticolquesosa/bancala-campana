// =========================================================
// BANCALA — home: Quito 3D, scroll y secciones interactivas
// =========================================================
import { gsap, ScrollTrigger, $, $$, lenis, reduced, isTouch, isMobile, bindAnchors, setupHeader, setupCursor, setCursor, setupBounce, loadData } from './common.js';

lenis.stop();
bindAnchors();
const updateHeader = setupHeader('.why, .poses, .look, .flow, .info, .stickers, .station');
setupCursor();

const DATA = loadData();
let Q = null; // api de Quito 3D

// =========================================================
// LOADER + BOOT
// =========================================================
const pctEl = $('#loaderPct');
const prog = { v: 0, target: 0 };
const progTick = () => { prog.v += (prog.target - prog.v) * .1; pctEl.textContent = Math.round(prog.v); };
gsap.ticker.add(progTick);

function webglOK() { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch { return false; } }

async function boot() {
  prog.target = 12;
  setupBounce();
  const fonts = document.fonts?.ready ?? Promise.resolve();
  let qP = Promise.resolve(null);
  if (webglOK()) {
    qP = import('./quito3d.js')
      .then((m) => m.initQuito($('#quitoCanvas'), { onProgress: (p) => (prog.target = 20 + p * 60) }))
      .catch((e) => { console.warn('[bancala] Quito 3D no disponible', e); document.documentElement.classList.add('no-webgl'); return null; });
  } else document.documentElement.classList.add('no-webgl');
  // la página no espera al 3D más de 1,5 s: si tarda, Quito cae apenas está listo
  qP.then((q) => { Q = q; if (introStarted) startQuito(); });
  const minTime = new Promise((r) => setTimeout(r, 600));
  const qWait = Promise.race([qP, new Promise((r) => setTimeout(r, 1500))]);
  await Promise.all([qWait, fonts, minTime, DATA]);
  prog.target = 100;
  await new Promise((r) => setTimeout(r, 250));
  intro();
}

let introStarted = false, quitoStarted = false;
function startQuito() {
  if (!Q || quitoStarted || !introStarted) return;
  quitoStarted = true;
  setupQuitoInput(); computeAnchors(); placeQuito(true); Q.reveal();
  setTimeout(() => say('¡Hola! Soy Quito, el banquito.', 3200), 900);
}

function intro() {
  const heroChars = $$('.hero .ch');
  const tl = gsap.timeline();
  tl.to('.loader__center', { y: -40, opacity: 0, duration: .5, ease: 'power2.in' })
    .to('.loader__bottom', { opacity: 0, duration: .3 }, '<')
    .to('.loader__slats i', { xPercent: (i) => (i % 2 ? 101 : -101), duration: 1, ease: 'expo.inOut', stagger: .06 }, '-=.15')
    .add(() => {
      document.body.classList.remove('is-loading'); lenis.start(); gsap.ticker.remove(progTick);
      if (location.hash && $(location.hash)) { lenis.scrollTo($(location.hash), { immediate: true }); computeAnchors(); }
      introStarted = true; startQuito();
    }, '-=.75')
    .from(heroChars, { yPercent: 120, rotate: () => gsap.utils.random(-30, 30), opacity: 0, duration: 1.1, ease: 'back.out(1.8)', stagger: .025 }, '-=.6')
    .from('.header > *', { y: -40, opacity: 0, stagger: .08, duration: 1, ease: 'expo.out' }, '-=.9')
    .from('.reveal-up', { y: 40, opacity: 0, stagger: .08, duration: 1.1, ease: 'expo.out' }, '-=.8')
    .set('#loader', { display: 'none' });
  setupScroll();
}

// =========================================================
// QUITO: ubicación por scroll (anclas data-q), mirada, clic, arrastre, globo
// =========================================================
let anchors = [];
function parseQ(str) { const [x, y, s, ry, expr, pose] = str.trim().split(/\s+/); return { x: +x, y: +y, s: +s, ry: +ry, expr, pose }; }
function computeAnchors() {
  const H = innerHeight, mob = isMobile();
  anchors = $$('[data-q]').filter((el) => !el.dataset.only || el.dataset.only === (mob ? 'mobile' : 'desktop')).map((el) => {
    const r = el.getBoundingClientRect(), top = r.top + scrollY, bottom = top + r.height;
    const start = top - H * .25, end = Math.max(start, bottom - H * .75);
    return { start, end, q: parseQ(mob && el.dataset.qm ? el.dataset.qm : el.dataset.q), el };
  }).sort((a, b) => a.start - b.start);
}
const smooth = (t) => t * t * (3 - 2 * t);
let lastPlacedExpr = '', lastIdx = -1, lastSayAt = 0;
function placeQuito(snap = false) {
  if (!Q || !anchors.length) return;
  const y = scrollY;
  let q, idx = 0;
  if (y <= anchors[0].end) q = anchors[0].q;
  else {
    q = anchors[anchors.length - 1].q;
    for (let i = 0; i < anchors.length; i++) {
      const a = anchors[i], b = anchors[i + 1];
      if (y >= a.start && y <= a.end) { q = a.q; idx = i; break; }
      if (b && y > a.end && y < b.start) {
        const t = smooth((y - a.end) / (b.start - a.end)); idx = t < .5 ? i : i + 1;
        q = { x: a.q.x + (b.q.x - a.q.x) * t, y: a.q.y + (b.q.y - a.q.y) * t, s: a.q.s + (b.q.s - a.q.s) * t, ry: a.q.ry + (b.q.ry - a.q.ry) * t,
          expr: t < .5 ? a.q.expr : b.q.expr, pose: t < .5 ? a.q.pose : b.q.pose };
        // a mitad de camino salta (como si cambiara de lugar)
        break;
      }
    }
  }
  const moodLocked = q.expr === 'feliz' && currentAnchorEl() === $('#quito') && moodExpr;
  Q.set({ ...q, expr: moodLocked ? moodExpr : q.expr, pose: moodLocked ? moodPose : q.pose });
  if (snap) Q.snap();
  if (y > anchors[anchors.length - 1].end) idx = anchors.length - 1;
  if (idx !== lastIdx) { lastIdx = idx; if (performance.now() - lastSayAt > 1200) bubbleUntil = 0; }
  if (q.expr !== lastPlacedExpr && lastPlacedExpr && !snap) { /* cambio de sección */ }
  lastPlacedExpr = q.expr;
}
function currentAnchorEl() {
  const y = scrollY; for (const a of anchors) if (y >= a.start - innerHeight * .3 && y <= a.end + innerHeight * .3) return a.el; return null;
}

// globo de diálogo
const bubble = $('#bubble'), bubbleText = $('#bubbleText');
// el globo se pide con say(); se muestra solo mientras la cabeza de Quito está en pantalla
let bubbleUntil = 0, bubbleShown = false;
function say(text, ms = 2600) {
  if (!Q) return;
  const was = bubbleShown && bubbleText.textContent !== text;
  bubbleText.textContent = text; bubbleUntil = performance.now() + ms + 600; lastSayAt = performance.now();
  if (was) gsap.fromTo(bubble, { scale: .88 }, { scale: 1, duration: .4, ease: 'back.out(3)', overwrite: 'auto' });
}
const hs = { x: 0, y: 0 };
gsap.ticker.add(() => {
  if (!Q) return;
  const now = performance.now();
  if (now > bubbleUntil && !bubbleShown) return;
  Q.headScreen(hs);
  const onScreen = hs.visible && hs.y > 110 && hs.y < innerHeight - 40 && hs.x > 0 && hs.x < innerWidth && Q.state.s > .2 && Math.abs(Q.state.y - Q.state.ty) < .15;
  const want = now < bubbleUntil && onScreen;
  if (want !== bubbleShown) {
    bubbleShown = want;
    gsap.to(bubble, want ? { opacity: 1, scale: 1, duration: .55, ease: 'back.out(2.4)', overwrite: true } : { opacity: 0, scale: .6, duration: .25, overwrite: true });
  }
  if (onScreen) {
    const bw = bubble.offsetWidth;
    const x = Math.min(innerWidth - bw * .72 - 10, Math.max(bw * .3 + 10, hs.x + 20));
    bubble.style.left = x + 'px'; bubble.style.top = (hs.y - 8) + 'px';
  }
});

const PHRASES = [
  ['¡Hola! Soy Quito, el banquito.', 'feliz', 'wave'],
  ['¿Me bancás? Yo te banco en todas.', 'guino', 'thumbs'],
  ['¡Ey! No soy tu cuaderno.', 'enojado', 'hips'],
  ['No soy reposera… ¡tapate un poco, che!', 'avergonzado', 'shy'],
  ['¡Jaja, me hacés cosquillas!', 'euforico', 'cheer'],
  ['¡El que ceba se queda!', 'carrusel-04-mate', 'idle'],
  ['Si me movés, devolveme.', 'preocupado-sentado', 'idle'],
  ['Cuidame más que a tu mamá (bueno, casi).', 'sentado-feliz', 'idle'],
  ['Lo que dejás en el banco, lo junta alguien.', 'juntando-basura', 'idle'],
  ['¿Está roto? Avisá a Mantenimiento.', 'limpiando', 'idle'],
  ['¡Me despertaste! Estaba en la siesta…', 'carrusel-04-despertando', 'idle'],
  ['¡Si llueve, te cubro!', 'paraguas', 'idle'],
];
let phraseI = 0;
function react() {
  if (!Q) return;
  const [txt, expr, pose] = PHRASES[phraseI++ % PHRASES.length];
  Q.jump(7 + Math.random() * 2);
  Q.setExpression(expr, 2800); Q.setPose(pose, 2800);
  say(txt, 2800);
}

function setupQuitoInput() {
  if (!Q) return;
  const canvasEl = $('#quitoCanvas');
  let down = null, hovering = false;
  addEventListener('pointermove', (e) => {
    Q.pointer((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1);
    if (down) {
      const dx = e.clientX - down.x;
      if (!down.drag && Math.abs(dx) > 6) { down.drag = true; Q.dragStart(); }
      if (down.drag) { Q.dragMove(e.clientX - down.lx); down.lx = e.clientX; }
      return;
    }
    if (isTouch) return;
    const over = !e.target.closest('a, button, input, .meet__content, .poster, .rules__list') && Q.hitTest(e.clientX, e.clientY);
    if (over !== hovering) { hovering = over; Q.hover(over); setCursor(over ? 'label' : '', over ? '¡Tocame!' : ''); document.body.style.cursor = over ? 'pointer' : ''; }
  }, { passive: true });
  document.addEventListener('pointerleave', () => Q.pointerLeave());
  addEventListener('pointerdown', (e) => {
    if (e.button !== 0 || e.target.closest('a, button, input, .slider, .board, .compare, .coverflow')) return;
    if (!Q.hitTest(e.clientX, e.clientY)) return;
    down = { x: e.clientX, lx: e.clientX, drag: false, t: performance.now() };
    if (!isTouch) e.preventDefault();
  });
  addEventListener('pointerup', () => {
    if (!down) return;
    if (down.drag) { Q.dragEnd(); if (Math.random() < .5) say('¡Uy, me mareo!', 1600); } else react();
    down = null;
  });
  addEventListener('pointercancel', () => { if (down?.drag) Q.dragEnd(); down = null; });
  // si el puntero no se mueve (táctil), mirar al centro
  if (isTouch) Q.pointerLeave();
  void canvasEl;
}

// =========================================================
// SCROLL Y SECCIONES
// =========================================================
let moodExpr = null, moodPose = null;

async function setupScroll() {
  const data = await DATA;

  computeAnchors(); placeQuito(true);
  lenis.on('scroll', () => placeQuito());
  ScrollTrigger.addEventListener('refresh', () => { computeAnchors(); placeQuito(); updateHeader(); });
  addEventListener('resize', () => { computeAnchors(); placeQuito(); });

  // ---- hero: filas que se abren + Quito se aleja ----
  const heroTl = gsap.timeline({ scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  heroTl.to('.hero__row--a', { xPercent: -18, ease: 'none' }, 0).to('.hero__row--b', { xPercent: 14, ease: 'none' }, 0)
    .to('.hero__side, .hero__tag, .hero__scroll', { opacity: 0, y: -40, ease: 'none', duration: .4 }, 0)
    .to('.hero__glow', { scale: 1.6, opacity: 0, ease: 'none' }, 0);

  // ---- por qué cuidarlos: aparición simple ----
  gsap.from('.why__copy > *', { y: 30, opacity: 0, stagger: .08, duration: .9, ease: 'power3.out', scrollTrigger: { trigger: '.why', start: 'top 70%', once: true } });
  gsap.from('.why__media', { y: 40, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: '.why', start: 'top 65%', once: true } });

  // ---- conocé a Quito ----
  gsap.from('.meet__halo, .meet__ring', { scale: .6, opacity: 0, duration: 1.4, ease: 'expo.out', scrollTrigger: { trigger: '.meet', start: 'top 60%', once: true } });
  gsap.from('.meet__content > *:not(h2)', { y: 30, opacity: 0, stagger: .08, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.meet', start: 'top 55%', once: true } });
  gsap.from('.ficha > div', { y: 16, opacity: 0, stagger: .05, duration: .8, ease: 'expo.out', scrollTrigger: { trigger: '.ficha', start: 'top 85%', once: true } });
  ScrollTrigger.create({ trigger: '.meet', start: 'top 30%', once: true, onEnter: () => say('Mi humor depende de vos. ¡Probá los botones!', 3200) });
  $$('#moods .mood').forEach((b) => b.addEventListener('click', () => {
    $$('#moods .mood').forEach((x) => x.classList.toggle('is-on', x === b));
    moodExpr = b.dataset.expr; moodPose = b.dataset.pose;
    if (Q) { Q.setExpression(moodExpr); Q.setPose(moodPose, 2600); Q.jump(5); placeQuito(); say(b.dataset.say, 3000); }
  }));

  // ---- poses: carrusel infinito arrastrable ----
  buildPoses(data.poses);

  // ---- menos en estas: scroll horizontal ----
  const mm = gsap.matchMedia();
  mm.add('(min-width: 861px)', () => {
    const track = $('#limitsTrack');
    const dist = () => track.scrollWidth - innerWidth;
    const tw = gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: { trigger: '.limits', start: 'top top', end: () => '+=' + dist(), pin: '.limits__pin', scrub: .6, invalidateOnRefresh: true,
      onUpdate: (s) => { $('#limitsBar').style.transform = `scaleX(${s.progress})`; } } });
    $$('.poster').forEach((p) => {
      gsap.fromTo(p, { rotate: 6, y: 60 }, { rotate: -3, y: 0, ease: 'none', scrollTrigger: { trigger: p, containerAnimation: tw, start: 'left right', end: 'right left', scrub: true } });
      ScrollTrigger.create({ trigger: p, containerAnimation: tw, start: 'left 62%', end: 'right 38%', onEnter: () => say(p.dataset.say, 2200), onEnterBack: () => say(p.dataset.say, 2200) });
    });
    return () => {};
  });
  mm.add('(max-width: 860px)', () => {
    $$('.poster').forEach((p) => gsap.from(p, { y: 60, rotate: 4, opacity: 0, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: p, start: 'top 92%', once: true } }));
  });

  // ---- un día en la vida ----
  setupDay();

  // ---- la misma banca: galería en profundidad ----
  setupDepth(data);

  // ---- antes / después ----
  setupCompare();

  // ---- estrategia ----
  gsap.from('.step', { y: 100, opacity: 0, rotate: (i) => (i - 1) * 4, stagger: .12, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: '.steps__grid', start: 'top 85%', once: true } });
  gsap.to('#weeksLine', { scaleX: 1, ease: 'none', scrollTrigger: { trigger: '.weeks', start: 'top 85%', end: 'bottom 60%', scrub: true } });
  gsap.from('.week', { y: 40, opacity: 0, stagger: .12, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.weeks', start: 'top 85%', once: true } });
  gsap.from('.ref', { y: 30, opacity: 0, stagger: .1, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.refs', start: 'top 90%', once: true } });

  // ---- estación ----
  const stl = gsap.timeline({ scrollTrigger: { trigger: '.station', start: 'top top', end: 'bottom bottom', scrub: .8,
    onUpdate: (s) => { $('.station').dataset.light = s.progress > .25 ? 'off' : 'on'; } } });
  stl.fromTo('#stationMedia', { clipPath: 'inset(30% 32% 30% 32% round 24px)' }, { clipPath: 'inset(0% 0% 0% 0% round 0px)', ease: 'power2.inOut', duration: 1 }, 0)
    .fromTo('#stationMedia img', { scale: 1.35 }, { scale: 1, ease: 'none', duration: 1.5 }, 0)
    .fromTo('.station__line > span', { yPercent: 115, rotate: 8 }, { yPercent: 0, rotate: 0, stagger: .12, duration: .5, ease: 'back.out(2)' }, .55)
    .fromTo('.station__sub', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .3 }, .8)
    .fromTo('.station__chips li', { opacity: 0, y: 30, scale: .6 }, { opacity: 1, y: 0, scale: 1, stagger: .06, duration: .3, ease: 'back.out(2)' }, .85);

  setupCoverflow(data);
  setupSocial(data);
  setupLoupe();

  // ---- reglas: cada regla cambia a Quito ----
  $$('.rules__list li').forEach((li) => {
    li.addEventListener('pointerenter', () => { if (!Q) return; Q.setExpression(li.dataset.expr, 2400); Q.jump(4); say(li.dataset.say, 2400); });
  });
  gsap.from('.rules__list li', { x: -60, opacity: 0, stagger: .1, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.rules__list', start: 'top 85%', once: true } });
  ScrollTrigger.create({ trigger: '.rules', start: 'top 40%', once: true, onEnter: () => say('Cuatro reglas y listo. ¡Fácil!', 2800) });

  setupStickers(data.stickers);

  // ---- footer ----
  ScrollTrigger.create({ trigger: '.footer', start: 'top 40%', onEnter: () => { say('¡Gracias por bancarme! Nos vemos en el patio.', 3600); Q?.jump(8); } });
  gsap.from('.footer__firm > *', { y: 30, opacity: 0, stagger: .08, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.footer__firm', start: 'top 95%', once: true } });

  // las galerías que se mueven (horizontal, en profundidad, apiladas) piden sus imágenes un poco antes de llegar,
  // así no aparecen tarde: el lazy-load nativo no ve lo que queda fuera de pantalla por transformaciones
  ['.limits', '.day', '.depth', '.coverflow', '.social'].forEach((sel) => ScrollTrigger.create({ trigger: sel, start: 'top 250%', once: true,
    onEnter: () => $$(sel + ' img[loading="lazy"]').forEach((im) => { im.loading = 'eager'; im.decode?.().catch(() => {}); }) }));

  // refrescar cuando cargan imágenes lazy
  let to; $$('img[loading="lazy"]').forEach((im) => im.addEventListener('load', () => { clearTimeout(to); to = setTimeout(() => ScrollTrigger.refresh(), 250); }, { once: true }));
  ScrollTrigger.refresh();
}

// ---------------------------------------------------------
function buildPoses(poses) {
  const track = $('#posesTrack'), slider = $('#posesSlider');
  const list = poses.filter((p) => !p.src.includes('stand-'));
  const html = list.map((p) => `<div class="pcard"><img src="${p.src}" alt="Quito ${p.name}" width="${p.w}" height="${p.h}" loading="lazy" draggable="false"><span>${p.name}</span></div>`).join('');
  track.innerHTML = html + html;
  let x = 0, v = -.6, half = 0, drag = null, inView = false;
  const measure = () => { half = track.scrollWidth / 2; };
  measure(); addEventListener('resize', measure);
  $$('img', track).forEach((im) => im.addEventListener('load', measure, { once: true }));
  ScrollTrigger.create({ trigger: slider, start: 'top bottom', end: 'bottom top', onToggle: (s) => (inView = s.isActive), onUpdate: (s) => { if (!drag) v = -.6 - Math.min(8, Math.abs(s.getVelocity()) / 300) * Math.sign(s.getVelocity() || 1); } });
  const cards = () => $$('.pcard', track);
  gsap.ticker.add(() => {
    if (!inView) return;
    if (!drag) { x += v; v += (-.6 - v) * .04; }
    if (half) { x = ((x % half) - half) % half; }
    track.style.transform = `translate3d(${x}px,0,0)`;
    const skew = Math.max(-12, Math.min(12, (drag ? drag.vx : v + .6) * 1.4));
    cards().forEach((c) => (c.style.transform = `skewX(${skew * -.6}deg) rotate(${skew * .25}deg)`));
  });
  slider.addEventListener('pointerdown', (e) => { drag = { lx: e.clientX, vx: 0 }; slider.classList.add('dragging'); slider.setPointerCapture(e.pointerId); });
  slider.addEventListener('pointermove', (e) => { if (!drag) return; const dx = e.clientX - drag.lx; drag.lx = e.clientX; drag.vx = dx; x += dx; });
  const up = () => { if (!drag) return; v = drag.vx; drag = null; slider.classList.remove('dragging'); };
  slider.addEventListener('pointerup', up); slider.addEventListener('pointercancel', up);
  slider.dataset.cursor = 'Arrastrá';
  gsap.from('.poses__head > *', { y: 40, opacity: 0, stagger: .1, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.poses', start: 'top 70%', once: true } });
}

// ---------------------------------------------------------
function setupDay() {
  const slides = $$('.dslide'), N = slides.length;
  const dots = $('#dayDots'); dots.innerHTML = slides.map(() => '<i></i>').join('');
  const ticks = $('.clock__ticks'); ticks.innerHTML = Array.from({ length: 12 }, (_, i) => { const a = i / 12 * Math.PI * 2; const r1 = i % 3 ? 78 : 70; return `<line x1="${100 + Math.sin(a) * r1}" y1="${100 - Math.cos(a) * r1}" x2="${100 + Math.sin(a) * 84}" y2="${100 - Math.cos(a) * 84}"/>`; }).join('');
  const times = slides.map((s) => { const [h, m] = s.dataset.time.split(':').map(Number); return h * 60 + m; });
  const SKY = [[8, '#8fd3ff', '#ffe7b0'], [10.5, '#5fb6ff', '#d6f0ff'], [13, '#3f9cf5', '#bfe6ff'], [15, '#3a8ae6', '#9fd6ff'], [17, '#f59a55', '#ffd59a'], [19, '#6b4c9e', '#ff8e6a'], [20, '#14295a', '#33508f']];
  const mix = (a, b, t) => { const pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16); const c = [16, 8, 0].map((s) => Math.round(((pa >> s) & 255) * (1 - t) + ((pb >> s) & 255) * t)); return `rgb(${c.join(',')})`; };
  const sky = $('#daySky'), hH = $('#clockH'), hM = $('#clockM'), tEl = $('#dayTime'), cap = $('#dayCaption');
  let shown = -1;
  const render = (p) => {
    const f = p * (N - 1);
    slides.forEach((s, i) => {
      const d = i - f;
      let tr, op = 1;
      if (d < 0) { const k = Math.min(1, -d); tr = `translate3d(${-k * 120}%, ${-k * 12}%, 0) rotate(${-k * 22}deg)`; op = 1 - Math.max(0, -d - .6) * 2.5; }
      else { tr = `translate3d(${d * 3}%, ${-d * 3.5}%, ${-d * 70}px) rotate(${(i % 2 ? 1 : -1) * Math.min(d, 3) * 3}deg)`; op = d > 3.2 ? 0 : 1; }
      s.style.transform = tr; s.style.opacity = Math.max(0, op); s.style.zIndex = String(100 - i);
    });
    const i0 = Math.min(N - 2, Math.floor(f)), t = f - i0;
    const mins = times[i0] + (times[i0 + 1] - times[i0]) * t;
    const h = mins / 60;
    hH.setAttribute('transform', `rotate(${(h % 12) * 30} 100 100)`); hM.setAttribute('transform', `rotate(${(mins % 60) * 6} 100 100)`);
    let k = 0; while (k < SKY.length - 2 && h > SKY[k + 1][0]) k++;
    const st = Math.min(1, Math.max(0, (h - SKY[k][0]) / (SKY[k + 1][0] - SKY[k][0])));
    sky.style.background = `linear-gradient(180deg, ${mix(SKY[k][1], SKY[k + 1][1], st)}, ${mix(SKY[k][2], SKY[k + 1][2], st)})`;
    const idx = Math.round(f);
    if (idx !== shown) {
      shown = idx; tEl.textContent = slides[idx].dataset.time; cap.textContent = slides[idx].dataset.cap;
      gsap.fromTo([tEl, cap], { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: .5, ease: 'expo.out', stagger: .05 });
      $$('i', dots).forEach((d, j) => d.classList.toggle('on', j === idx));
    }
  };
  render(0);
  ScrollTrigger.create({ trigger: '.day', start: 'top top', end: 'bottom bottom', scrub: true, onUpdate: (s) => render(s.progress) });
  gsap.from('.day__copy > *', { y: 40, opacity: 0, stagger: .1, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.day', start: 'top 60%', once: true } });
}

// ---------------------------------------------------------
function setupDepth(data) {
  const stage = $('#depthStage');
  const c3 = data.piezas.filter((p) => p.group.startsWith('Carrusel 03')).map((p) => ({ ...p, cap: p.title.replace(/^\d+ · /, '') }));
  const pick = [3, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 40, 43, 45].map((n) => data.campus[n - 1]).filter(Boolean).map((c) => ({ ...c, cap: 'Campus UCASAL' }));
  const items = [];
  for (let i = 0; i < Math.max(c3.length, pick.length); i++) { if (pick[i]) items.push(pick[i]); if (c3[i]) items.push(c3[i]); if (pick[i + 7] && i < 4) items.push(pick[i + 7]); }
  let s = 11; const rnd = () => ((s = (s * 16807) % 2147483647) / 2147483647);
  const cards = items.slice(0, 20).map((it, i) => {
    const ang = i * 2.4 + rnd() * .6, rad = 22 + rnd() * 14;
    const fig = document.createElement('figure'); fig.className = 'dcard';
    fig.dataset.x = (Math.cos(ang) * rad * 1.25).toFixed(1); fig.dataset.y = (Math.sin(ang) * rad * .8).toFixed(1); fig.dataset.z = String(-i * 170);
    fig.dataset.w = String(11 + rnd() * 6);
    fig.innerHTML = `<img src="${it.sm || it.src}" alt="${it.cap}" width="${it.w}" height="${it.h}" loading="lazy" decoding="async"><figcaption>${it.cap}</figcaption>`;
    stage.appendChild(fig); return fig;
  });
  const depthMax = cards.length * 170 + 300;
  const place = (p) => {
    const camZ = p * depthMax, vw = innerWidth / 100, vh = innerHeight / 100, mob = innerWidth < 760;
    cards.forEach((c) => {
      const x = +c.dataset.x * vw * (mob ? .75 : 1), y = +c.dataset.y * vh, z = +c.dataset.z + camZ;
      c.style.width = (+c.dataset.w * (mob ? 1.9 : 1)) + 'vw';
      let o = 1; if (z < -1700) o = 0; else if (z < -1000) o = (z + 1700) / 700; if (z > 300) o = Math.max(0, 1 - (z - 300) / 300);
      c.style.opacity = o.toFixed(3); c.style.visibility = o <= 0 ? 'hidden' : 'visible';
      c.style.transform = `translate3d(calc(-50% + ${x}px), calc(-50% + ${y}px), ${z}px)`;
    });
    $('#depthBar').style.transform = `scaleX(${p})`;
  };
  place(0);
  ScrollTrigger.create({ trigger: '.depth', start: 'top top', end: 'bottom bottom', scrub: true, onUpdate: (st) => place(st.progress), onRefresh: (st) => place(st.progress) });
  if (!isTouch) $('.depth__pin').addEventListener('pointermove', (e) => {
    const nx = e.clientX / innerWidth - .5, ny = e.clientY / innerHeight - .5;
    gsap.to(stage, { rotationY: nx * 7, rotationX: -ny * 5, duration: 1.2, ease: 'power3.out' });
  });
  gsap.from('.depth__copy > *', { y: 40, opacity: 0, stagger: .12, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.depth', start: 'top 30%', once: true } });
}

// ---------------------------------------------------------
function setupCompare() {
  const box = $('#compare'), before = $('#compareBefore'), handle = $('#compareHandle');
  const st = { p: 50 };
  const set = (p) => { st.p = Math.max(2, Math.min(98, p)); before.style.clipPath = `inset(0 ${100 - st.p}% 0 0)`; handle.style.left = st.p + '%'; };
  set(50);
  let dragging = false;
  const fromEvent = (e) => { const r = box.getBoundingClientRect(); return (e.clientX - r.left) / r.width * 100; };
  box.addEventListener('pointerdown', (e) => { dragging = true; box.setPointerCapture(e.pointerId); gsap.killTweensOf(st); set(fromEvent(e)); });
  box.addEventListener('pointermove', (e) => { if (dragging || !isTouch) { gsap.killTweensOf(st); set(fromEvent(e)); } });
  box.addEventListener('pointerup', () => (dragging = false));
  box.dataset.cursor = 'Deslizá';
  gsap.timeline({ scrollTrigger: { trigger: box, start: 'top 70%', once: true } })
    .to(st, { p: 85, duration: 1, ease: 'power2.inOut', onUpdate: () => set(st.p) })
    .to(st, { p: 20, duration: 1.3, ease: 'power2.inOut', onUpdate: () => set(st.p) })
    .to(st, { p: 50, duration: .9, ease: 'power2.inOut', onUpdate: () => set(st.p) });
  gsap.from('.look__list li', { y: 30, opacity: 0, stagger: .08, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.look__list', start: 'top 85%', once: true } });
}

// ---------------------------------------------------------
function setupCoverflow(data) {
  const items = [
    ...data.piezas.filter((p) => p.cat === 'stand'),
    ...data.piezas.filter((p) => p.cat === 'arquigrafia'),
  ];
  const order = [10, 0, 4, 1, 3, 2, 7, 8, 5, 6, 9].map((i) => items[i]).filter(Boolean).concat(items.slice(11));
  const stage = $('#cfStage'), cap = $('#cfCap');
  const els = order.map((p) => { const d = document.createElement('div'); d.className = 'cf-item'; d.innerHTML = `<img src="${p.md}" srcset="${p.sm} 520w, ${p.md} 900w, ${p.src} ${p.w}w" sizes="(max-width: 860px) 82vw, 58vw" alt="${p.title}" width="${p.w}" height="${p.h}" loading="lazy" decoding="async" draggable="false">`; stage.appendChild(d); return d; });
  let cur = 0; const pos = { v: 0 };
  const layout = () => {
    const mob = innerWidth < 860;
    els.forEach((el, i) => {
      const k = i - pos.v, a = Math.abs(k);
      el.style.transform = `translate(-50%,-50%) translateX(${k * (mob ? 62 : 48)}%) translateZ(${-a * 280}px) rotateY(${Math.max(-1, Math.min(1, k)) * -32}deg) scale(${1 - Math.min(a, 3) * .04})`;
      el.style.opacity = a > 3.2 ? 0 : 1 - Math.max(0, a - 2.2) * .8;
      el.style.zIndex = String(100 - Math.round(a * 10));
      el.style.filter = a > .5 ? `brightness(${1 - Math.min(a, 3) * .12})` : 'none';
    });
  };
  const go = (i) => {
    cur = (i + els.length) % els.length;
    gsap.to(pos, { v: cur, duration: .9, ease: 'expo.out', onUpdate: layout });
    const p = order[cur];
    cap.innerHTML = `<small>${p.cat === 'stand' ? 'Stand Bancala' : 'Arquigrafía · ' + p.group}</small>${p.title.replace(/^\d+ · /, '')}`;
  };
  layout(); go(0);
  $('#cfPrev').addEventListener('click', () => go(cur - 1));
  $('#cfNext').addEventListener('click', () => go(cur + 1));
  $('#coverflow').addEventListener('keydown', (e) => { if (e.key === 'ArrowLeft') go(cur - 1); if (e.key === 'ArrowRight') go(cur + 1); });
  els.forEach((el, i) => el.addEventListener('click', () => i !== cur && go(i)));
  let sx = null;
  stage.addEventListener('pointerdown', (e) => (sx = e.clientX));
  stage.addEventListener('pointerup', (e) => { if (sx === null) return; const dx = e.clientX - sx; if (Math.abs(dx) > 40) go(cur + (dx < 0 ? 1 : -1)); sx = null; });
  stage.dataset.cursor = 'Arrastrá';
  addEventListener('resize', layout);
  gsap.from('.flow__head > *', { y: 40, opacity: 0, stagger: .1, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.flow', start: 'top 70%', once: true } });
}

// ---------------------------------------------------------
function setupSocial(data) {
  const stories = data.piezas.filter((p) => p.group === 'Historias');
  const hls = data.piezas.filter((p) => p.group === 'Destacadas');
  const box = $('#phoneStories'), bars = $('#phoneBars');
  box.innerHTML = stories.map((s, i) => `<img src="${s.sm}" srcset="${s.sm} 520w, ${s.src} ${s.w}w" sizes="340px" alt="Historia de Instagram: ${s.title.replace(/^\d+ · /, '')}" width="${s.w}" height="${s.h}" loading="lazy" decoding="async"${i ? '' : ' class="on"'}>`).join('');
  bars.innerHTML = stories.map(() => '<i><b></b></i>').join('');
  const imgs = $$('img', box), fills = $$('b', bars);
  let cur = 0, tw = null, active = false;
  const show = (i) => {
    cur = (i + stories.length) % stories.length;
    imgs.forEach((im, j) => im.classList.toggle('on', j === cur));
    fills.forEach((f, j) => gsap.set(f, { scaleX: j < cur ? 1 : 0 }));
    tw?.kill(); tw = gsap.fromTo(fills[cur], { scaleX: 0 }, { scaleX: 1, duration: 5, ease: 'none', paused: !active, onComplete: () => show(cur + 1) });
    $$('.hl').forEach((h, j) => h.classList.toggle('on', j === Math.min(cur, hls.length - 1)));
  };
  $('#storyPrev').addEventListener('click', () => show(cur - 1));
  $('#storyNext').addEventListener('click', () => show(cur + 1));
  const hlMap = [0, 1, 4, 6, 5, 3];
  $('#highlights').innerHTML = hls.map((h, i) => `<button class="hl" data-i="${hlMap[i] ?? i}"><span class="hl__ring"><img src="${h.sm}" alt="" width="92" height="92" loading="lazy"></span>${h.title.replace(/^\d+ · /, '')}</button>`).join('');
  $$('.hl').forEach((b) => b.addEventListener('click', () => show(+b.dataset.i)));
  show(0);
  ScrollTrigger.create({ trigger: '#phone', start: 'top 85%', end: 'bottom 10%', onToggle: (s) => { active = s.isActive; active ? tw?.play() : tw?.pause(); } });

  // abanico de posteos
  const fanItems = [...data.piezas.filter((p) => p.group === 'Posteos'), ...data.piezas.filter((p) => /^Carrusel 0[1-4]/.test(p.group) && /^1 · /.test(p.title))];
  const fan = $('#fan');
  fan.innerHTML = fanItems.map((p) => `<a class="fan__card" href="/piezas#redes" data-cursor="Ver"><img src="${p.sm}" alt="${p.group}: ${p.title}" width="${p.w}" height="${p.h}" loading="lazy"></a>`).join('');
  const cards = $$('.fan__card', fan), mid = (cards.length - 1) / 2;
  const st = { p: 0 };
  const lay = () => cards.forEach((c, i) => {
    const k = i - mid, mob = innerWidth < 860;
    c.style.transform = `translateX(${k * (mob ? 22 : 42) * st.p}%) rotate(${k * (mob ? 9 : 8) * st.p}deg) translateY(${Math.abs(k) * 4 * st.p}%)`;
    c.style.zIndex = String(50 - Math.round(Math.abs(k) * 2));
  });
  lay();
  gsap.to(st, { p: 1, ease: 'power2.out', onUpdate: lay, scrollTrigger: { trigger: fan, start: 'top 90%', end: 'center 55%', scrub: .8 } });
  gsap.from('.phone', { y: 120, rotate: -8, opacity: 0, duration: 1.3, ease: 'expo.out', scrollTrigger: { trigger: '.social__grid', start: 'top 80%', once: true } });
  gsap.from('.hl', { scale: 0, stagger: .06, duration: .8, ease: 'back.out(2.4)', scrollTrigger: { trigger: '#highlights', start: 'top 90%', once: true } });
}

// ---------------------------------------------------------
function setupLoupe() {
  const wrap = $('#loupeWrap'), img = $('#infoImg'), loupe = $('#loupe');
  if (isTouch) { loupe.remove(); return; }
  const Z = 2.6;
  wrap.addEventListener('pointerenter', () => { loupe.style.backgroundImage = `url(${img.getAttribute('src')})`; });
  wrap.addEventListener('pointermove', (e) => {
    const r = wrap.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
    loupe.style.left = (x - 110) + 'px'; loupe.style.top = (y - 110) + 'px';
    loupe.style.backgroundSize = `${r.width * Z}px ${r.height * Z}px`;
    loupe.style.backgroundPosition = `${-(x * Z - 110)}px ${-(y * Z - 110)}px`;
  });
  gsap.from('.loupe-wrap', { y: 100, rotate: 8, opacity: 0, duration: 1.3, ease: 'expo.out', scrollTrigger: { trigger: '.info', start: 'top 70%', once: true } });
}

// ---------------------------------------------------------
function setupStickers(list) {
  const board = $('#board');
  const stickers = list.map((s, i) => {
    const el = document.createElement('div'); el.className = 'sticker';
    el.innerHTML = `<img src="${s.src}" alt="Sticker de Quito ${s.name}" width="${s.w}" height="${s.h}" draggable="false" loading="lazy">`;
    board.appendChild(el);
    return { el, img: el.firstElementChild, x: 0, y: 0, r: 0, vx: 0, vy: 0, vr: 0, i };
  });
  let W = 0, H = 0, z = 10;
  const layout = () => {
    W = board.clientWidth; H = board.clientHeight;
    stickers.forEach((s, i) => {
      const cols = innerWidth < 860 ? 3 : 4, cw = W / cols, rows = Math.ceil(stickers.length / cols), rh = H / rows;
      s.x = (i % cols) * cw + cw * .5 + (Math.sin(i * 7.3) * cw * .2); s.y = Math.floor(i / cols) * rh + rh * .5 + Math.cos(i * 3.1) * rh * .15; s.r = Math.sin(i * 5.7) * 14;
    });
  };
  const draw = () => stickers.forEach((s) => { const w = s.el.offsetWidth || 140; s.el.style.transform = `translate(${s.x - w / 2}px, ${s.y - w / 2}px) rotate(${s.r}deg)`; });
  layout(); draw(); addEventListener('resize', () => { layout(); draw(); });
  let drag = null, running = false;
  const tick = () => {
    let moving = false;
    stickers.forEach((s) => {
      if (drag && drag.s === s) return;
      if (Math.abs(s.vx) + Math.abs(s.vy) + Math.abs(s.vr) < .05) return;
      moving = true; s.x += s.vx; s.y += s.vy; s.r += s.vr; s.vx *= .92; s.vy *= .92; s.vr *= .9;
      if (s.x < 40 || s.x > W - 40) { s.vx *= -.6; s.x = Math.max(40, Math.min(W - 40, s.x)); }
      if (s.y < 40 || s.y > H - 40) { s.vy *= -.6; s.y = Math.max(40, Math.min(H - 40, s.y)); }
    });
    draw();
    if (!moving && !drag) { gsap.ticker.remove(tick); running = false; }
  };
  const kick = () => { if (!running) { running = true; gsap.ticker.add(tick); } };
  stickers.forEach((s) => {
    s.el.addEventListener('pointerdown', (e) => {
      e.preventDefault(); s.el.setPointerCapture(e.pointerId); s.el.classList.add('dragging'); s.el.style.zIndex = ++z;
      const r = board.getBoundingClientRect();
      drag = { s, ox: e.clientX - r.left - s.x, oy: e.clientY - r.top - s.y, lx: e.clientX, ly: e.clientY }; s.vx = s.vy = 0; kick();
      gsap.to(s.img, { scale: 1.12, duration: .3, ease: 'back.out(3)' });
    });
    s.el.addEventListener('pointermove', (e) => {
      if (!drag || drag.s !== s) return;
      const r = board.getBoundingClientRect();
      s.x = Math.max(30, Math.min(W - 30, e.clientX - r.left - drag.ox)); s.y = Math.max(30, Math.min(H - 30, e.clientY - r.top - drag.oy));
      s.vx = e.clientX - drag.lx; s.vy = e.clientY - drag.ly; s.r += s.vx * .3; drag.lx = e.clientX; drag.ly = e.clientY;
    });
    const end = () => { if (!drag || drag.s !== s) return; s.vr = s.vx * .3; drag = null; s.el.classList.remove('dragging'); gsap.to(s.img, { scale: 1, duration: .4, ease: 'back.out(3)' }); kick(); };
    s.el.addEventListener('pointerup', end); s.el.addEventListener('pointercancel', end);
  });
  board.dataset.cursor = 'Agarrá';
  gsap.from(stickers.map((s) => s.img), { opacity: 0, scale: 2.2, rotate: () => gsap.utils.random(-60, 60), stagger: .07, duration: .7, ease: 'back.out(1.6)',
    scrollTrigger: { trigger: board, start: 'top 75%', once: true } });
}

boot();
