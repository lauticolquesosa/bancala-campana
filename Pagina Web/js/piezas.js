// =========================================================
// BANCALA — archivo de piezas: filtros, grilla, visor y Quito compañero
// =========================================================
import { gsap, ScrollTrigger, $, $$, lenis, isTouch, setupHeader, setupCursor, setupBounce, loadData } from './common.js';

setupHeader('.filters, .arc');
setupCursor();
setupBounce();

const CATS = [
  { id: 'todas', label: 'Todas' },
  { id: 'redes', label: 'Redes', title: 'Instagram <em>como sala de estar.</em>', desc: 'Posteos de lanzamiento, cuatro carruseles y la foto de perfil. Formato 4:5 para ocupar más pantalla en el feed.' },
  { id: 'historias', label: 'Historias', title: 'Historias <em>que piden respuesta.</em>', desc: 'Siete historias interactivas (encuesta, quiz, slider, caja de preguntas, playlist, cuenta regresiva) y seis destacadas.' },
  { id: 'impresos', label: 'Impresos', title: 'Afiches, infografía <em>y stickers.</em>', desc: 'Serie de cinco afiches A3, infografía para carteleras y plancha de stickers A4.' },
  { id: 'arquigrafia', label: 'Arquigrafía', title: 'Estación <em>Bancala.</em>', desc: 'El refugio rojo, la mesa del Muro de historias y las placas QR de los bancos existentes. Artes finales y mockups.' },
  { id: 'stand', label: 'Stand', title: 'Stand <em>Bancala.</em>', desc: 'Backwall, mostrador, roll-up, Quito 3D en tamaño real, folleto, afiche, display con QR y planta.' },
  { id: 'quito', label: 'Quito', title: 'Las poses <em>de Quito.</em>', desc: 'Cada emoción es una conducta: feliz para el vínculo, enojado o avergonzado para el límite, limpiando para la acción.' },
  { id: 'campus', label: 'Fotos del campus', title: 'El campus <em>con el look Bancala.</em>', desc: 'Fotos reales con un único look: curva fílmica, sombras al azul, luces cálidas, profundidad y grano fino.' },
];

let ITEMS = [], view = [], filter = 'todas';

async function init() {
  const data = await loadData();
  const pieces = data.piezas.map((p) => ({ ...p, full: p.src, kind: 'pieza' }));
  const poses = data.poses.map((p) => ({ src: p.src, sm: p.src, full: p.src, w: p.w, h: p.h, cat: 'quito', group: 'Poses de Quito', title: p.name, kind: 'pose' }));
  const stk = data.stickers.map((p) => ({ src: p.src, sm: p.src, full: p.src, w: p.w, h: p.h, cat: 'quito', group: 'Stickers troquelados', title: p.name, kind: 'pose' }));
  const campus = data.campus.map((p, i) => ({ src: p.src, sm: p.sm, full: p.src, w: p.w, h: p.h, cat: 'campus', group: 'Fotos del campus', title: 'Campus ' + String(i + 1).padStart(2, '0'), kind: 'foto' }));
  ITEMS = [...pieces, ...poses, ...stk, ...campus];

  count('#statPiezas', pieces.length); count('#statFotos', campus.length); count('#statPoses', poses.length);

  const counts = Object.fromEntries(CATS.map((c) => [c.id, c.id === 'todas' ? ITEMS.length : ITEMS.filter((i) => i.cat === c.id).length]));
  $('#filters').innerHTML = CATS.map((c) => `<button class="chipf" role="tab" data-f="${c.id}">${c.label}<small>${counts[c.id]}</small></button>`).join('');
  $$('.chipf').forEach((b) => b.addEventListener('click', () => { setFilter(b.dataset.f); history.replaceState(null, '', b.dataset.f === 'todas' ? '/piezas' : '#' + b.dataset.f); lenis.scrollTo('#filters', { offset: 0, duration: 1 }); }));
  const h = location.hash.slice(1);
  setFilter(CATS.some((c) => c.id === h) ? h : 'todas', true);
  gsap.from('.arc-hero .ch', { yPercent: 110, rotate: () => gsap.utils.random(-25, 25), opacity: 0, duration: 1, ease: 'back.out(1.8)', stagger: .03, delay: .1 });
  gsap.from('.arc-hero__quito', { y: 200, rotate: 15, duration: 1.4, ease: 'elastic.out(1,.6)', delay: .3 });
  initBuddy();
}

function count(sel, n) { const o = { v: 0 }; gsap.to(o, { v: n, duration: 2, ease: 'power3.out', delay: .4, onUpdate: () => ($(sel).textContent = Math.round(o.v)) }); }

function setFilter(f, first = false) {
  filter = f;
  $$('.chipf').forEach((b) => b.classList.toggle('on', b.dataset.f === f));
  const arc = $('#archive');
  const groups = (f === 'todas' ? CATS.slice(1) : CATS.filter((c) => c.id === f));
  view = [];
  arc.innerHTML = groups.map((c) => {
    const list = ITEMS.filter((i) => i.cat === c.id);
    const tiles = list.map((it) => { const idx = view.push(it) - 1; return tile(it, idx); }).join('');
    return `<div class="arc__group" id="g-${c.id}"><h2 class="dsp">${c.title}</h2><p>${c.desc}</p><div class="arc__grid">${tiles}</div></div>`;
  }).join('');
  $$('.tile', arc).forEach((t) => t.addEventListener('click', () => openLB(+t.dataset.i)));
  const tiles = $$('.tile', arc);
  ScrollTrigger.batch(tiles, { start: 'top 95%', once: true, onEnter: (els) => gsap.fromTo(els, { y: 60, opacity: 0, rotate: () => gsap.utils.random(-3, 3) }, { y: 0, opacity: 1, rotate: 0, stagger: .05, duration: .9, ease: 'expo.out', overwrite: true }) });
  gsap.set(tiles, { opacity: 0 });
  if (!first) ScrollTrigger.refresh();
  let to; $$('img', arc).forEach((im) => im.addEventListener('load', () => { clearTimeout(to); to = setTimeout(() => ScrollTrigger.refresh(), 200); }, { once: true }));
}

function tile(it, i) {
  const n = it.title.match(/^(\d+) · /);
  const title = it.title.replace(/^\d+ · /, '');
  return `<figure class="tile${it.kind === 'pose' ? ' tile--pose' : ''}" data-i="${i}" data-cursor="Ver"><img src="${it.sm}" alt="${it.group}: ${title}" width="${it.w}" height="${it.h}" loading="lazy" decoding="async"><figcaption>${title}<span>${n ? it.group.split('·')[0].trim() + ' · ' + n[1].padStart(2, '0') : it.group.split('·')[0].trim()}</span></figcaption></figure>`;
}

// ---------- visor ----------
const lb = $('#lb'), lbImg = $('#lbImg');
let cur = 0;
function showLB(i, dir = 0) {
  cur = (i + view.length) % view.length; const it = view[cur];
  lbImg.src = it.full; lbImg.alt = it.title; $('#lbTitle').textContent = it.title.replace(/^\d+ · /, ''); $('#lbGroup').textContent = it.group;
  $('#lbCount').textContent = `${String(cur + 1).padStart(2, '0')} / ${String(view.length).padStart(2, '0')}`; $('#lbOpen').href = it.full;
  gsap.fromTo('.lb__fig', { x: dir * 80, opacity: 0, rotate: dir * 3 }, { x: 0, opacity: 1, rotate: 0, duration: .6, ease: 'expo.out' });
  [view[cur + 1], view[cur - 1]].forEach((n) => { if (n) { const im = new Image(); im.src = n.full; } });
}
function openLB(i) { lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false'); lenis.stop(); showLB(i); gsap.fromTo('.lb__fig', { scale: .85 }, { scale: 1, duration: .7, ease: 'expo.out' }); }
function closeLB() { lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true'); lenis.start(); }
$('#lbClose').addEventListener('click', closeLB); $('#lbBg').addEventListener('click', closeLB);
$('#lbPrev').addEventListener('click', () => showLB(cur - 1, -1)); $('#lbNext').addEventListener('click', () => showLB(cur + 1, 1));
addEventListener('keydown', (e) => { if (!lb.classList.contains('open')) return; if (e.key === 'Escape') closeLB(); if (e.key === 'ArrowLeft') showLB(cur - 1, -1); if (e.key === 'ArrowRight') showLB(cur + 1, 1); });
let sx = null;
lbImg.addEventListener('pointerdown', (e) => (sx = e.clientX));
lbImg.addEventListener('pointerup', (e) => { if (sx === null) return; const dx = e.clientX - sx; if (Math.abs(dx) > 40) showLB(cur + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1); sx = null; });

// ---------- Quito compañero (3D chiquito en la esquina) ----------
async function initBuddy() {
  const canvas = $('#buddyCanvas'), bub = $('#buddyBubble');
  let Q;
  try { const m = await import('./quito3d.js'); Q = await m.initQuito(canvas); } catch (e) { $('#buddy').remove(); return; }
  Q.set({ x: 0, y: -.02, s: .92, ry: -.35, expr: 'feliz', pose: 'idle' }); Q.snap(); Q.reveal();
  const lines = [['¿Buscás algo? Tocame.', 'feliz', 'wave'], ['¡Mirá los afiches!', 'guino', 'pointR'], ['Esa foto me gusta.', 'euforico', 'cheer'], ['¿Me bancás?', 'guino', 'thumbs'], ['No soy tu cuaderno.', 'enojado', 'hips']];
  let k = 0;
  const say = (t) => { bub.textContent = t; gsap.killTweensOf(bub); gsap.timeline().to(bub, { opacity: 1, scale: 1, duration: .5, ease: 'back.out(2.4)' }).to(bub, { opacity: 0, scale: .6, duration: .3, delay: 2.4 }); };
  setTimeout(() => say(lines[0][0]), 1600);
  addEventListener('pointermove', (e) => {
    const r = canvas.getBoundingClientRect();
    Q.pointer(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  }, { passive: true });
  canvas.addEventListener('click', () => { const [t, ex, po] = lines[++k % lines.length]; Q.jump(7); Q.setExpression(ex, 2600); Q.setPose(po, 2600); say(t); });
  canvas.dataset.cursor = '¡Hola!';
  // al abrir el visor, se pausa
  new MutationObserver(() => (lb.classList.contains('open') ? Q.pause() : Q.resume())).observe(lb, { attributes: true, attributeFilter: ['class'] });
  void isTouch;
}

init();
