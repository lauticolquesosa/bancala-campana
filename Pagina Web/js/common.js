// =========================================================
// BANCALA — piezas compartidas: scroll suave, menú, header, cursor, letras con rebote
// =========================================================
export const gsap = window.gsap, ScrollTrigger = window.ScrollTrigger;
gsap.registerPlugin(ScrollTrigger);
export const $ = (s, c = document) => c.querySelector(s);
export const $$ = (s, c = document) => [...c.querySelectorAll(s)];
export const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
export const isTouch = matchMedia('(hover: none)').matches;
export const isMobile = () => innerWidth < 860;

// ---------- smooth scroll ----------
export const lenis = new window.Lenis({ duration: 1.15, smoothWheel: !reduced });
window.__lenis = lenis;
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((t) => lenis.raf(t * 1000));
gsap.ticker.lagSmoothing(0);

export function bindAnchors(onNav) {
  $$('a[href^="#"]').forEach((a) => a.addEventListener('click', (e) => {
    const id = a.getAttribute('href'); const el = id === '#top' ? 0 : $(id);
    if (el === null) return;
    e.preventDefault(); closeMenu(); lenis.scrollTo(el, { duration: 1.6, offset: 0 }); onNav?.(id);
  }));
}

// ---------- menú ----------
const menu = $('#menu'), menuBtn = $('#menuBtn'), header = $('#header');
export function closeMenu() {
  if (!menu) return;
  menu.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); menu.setAttribute('aria-hidden', 'true'); header.classList.remove('menu-open'); lenis.start();
}
menuBtn?.addEventListener('click', () => {
  const open = !menu.classList.contains('open');
  if (!open) return closeMenu();
  menu.classList.add('open'); menuBtn.setAttribute('aria-expanded', 'true'); menu.setAttribute('aria-hidden', 'false'); header.classList.add('menu-open'); header.classList.remove('on-light', 'hidden');
  lenis.stop();
  gsap.fromTo('.menu__list a', { yPercent: 110 }, { yPercent: 0, stagger: .05, duration: .9, ease: 'expo.out', delay: .25 });
  gsap.fromTo('.menu__quito', { y: 120, rotate: 10, opacity: 0 }, { y: 0, rotate: 0, opacity: 1, duration: 1.1, ease: 'elastic.out(1,.6)', delay: .35 });
});
addEventListener('keydown', (e) => e.key === 'Escape' && closeMenu());

// ---------- header: color según la sección + se esconde al bajar ----------
export function setupHeader(lightSel) {
  let lastY = scrollY;
  const update = () => {
    if (menu?.classList.contains('open')) return;
    const probe = 40; let light = false;
    for (const s of $$(lightSel)) { const r = s.getBoundingClientRect(); if (r.top <= probe && r.bottom >= probe) { light = s.dataset.light !== 'off'; break; } }
    header.classList.toggle('on-light', light);
    const y = scrollY;
    header.classList.toggle('hidden', y > 300 && y > lastY + 2);
    if (y < lastY - 2 || y < 300) header.classList.remove('hidden');
    lastY = y;
  };
  lenis.on('scroll', update); addEventListener('scroll', update, { passive: true }); update();
  return update;
}

// ---------- cursor + magnéticos ----------
export const cursor = { el: $('#cursor'), label: $('#cursorLabel') };
export function setCursor(mode, text = '') {
  if (!cursor.el) return;
  cursor.el.classList.toggle('big', mode === 'big');
  cursor.el.classList.toggle('label', mode === 'label');
  if (cursor.label) cursor.label.textContent = text;
}
export function setupCursor() {
  if (isTouch || !cursor.el) return;
  const pos = { x: innerWidth / 2, y: innerHeight / 2 }, cur = { ...pos };
  addEventListener('pointermove', (e) => { pos.x = e.clientX; pos.y = e.clientY; cursor.el.style.opacity = 1; });
  document.addEventListener('pointerleave', () => (cursor.el.style.opacity = 0));
  gsap.ticker.add(() => { cur.x += (pos.x - cur.x) * .22; cur.y += (pos.y - cur.y) * .22; cursor.el.style.transform = `translate(${cur.x}px,${cur.y}px) translate(-50%,-50%)`; });
  document.addEventListener('pointerover', (e) => {
    const t = e.target.closest('a, button, [data-cursor]');
    if (!t) return;
    const lbl = t.dataset.cursor;
    setCursor(lbl ? 'label' : 'big', lbl || '');
  });
  document.addEventListener('pointerout', (e) => { const t = e.target.closest('a, button, [data-cursor]'); if (t && !t.contains(e.relatedTarget)) setCursor(''); });
  $$('.magnetic').forEach((el) => {
    el.addEventListener('pointermove', (e) => {
      const r = el.getBoundingClientRect();
      gsap.to(el, { x: (e.clientX - r.left - r.width / 2) * .25, y: (e.clientY - r.top - r.height / 2) * .3, duration: .4, ease: 'power3.out' });
    });
    el.addEventListener('pointerleave', () => gsap.to(el, { x: 0, y: 0, duration: .8, ease: 'elastic.out(1,.4)' }));
  });
}

// ---------- letras con rebote (tratamiento display de la campaña) ----------
export function splitBounce(root) {
  let n = 0;
  const walk = (node) => {
    [...node.childNodes].forEach((c) => {
      if (c.nodeType === 3) {
        const frag = document.createDocumentFragment();
        c.textContent.split(/(\s+)/).forEach((word) => {
          if (!word) return;
          if (/^\s+$/.test(word)) { frag.appendChild(document.createTextNode(' ')); return; }
          const w = document.createElement('span'); w.style.whiteSpace = 'nowrap'; w.style.display = 'inline-block';
          [...word].forEach((ch) => {
            const s = document.createElement('span'); s.className = 'ch'; s.textContent = ch;
            const k = n++; s.style.transform = `translateY(${(k % 3 - 1) * .02}em) rotate(${(k % 2 ? 1 : -1) * (1.5 + (k % 3))}deg)`;
            w.appendChild(s);
          });
          frag.appendChild(w);
        });
        c.replaceWith(frag);
      } else if (c.nodeType === 1 && c.tagName !== 'BR') walk(c);
    });
  };
  walk(root);
  return $$('.ch', root);
}
export function setupBounce() {
  $$('[data-bounce]').forEach((el) => {
    const chars = splitBounce(el);
    el.addEventListener('pointerenter', () => {
      gsap.fromTo(chars, { y: 0 }, { y: '-0.14em', duration: .18, ease: 'power2.out', stagger: .025, yoyo: true, repeat: 1, overwrite: 'auto' });
    });
    if (el.closest('.hero') || el.closest('[data-no-reveal]')) return;
    gsap.from(chars, { yPercent: 70, opacity: 0, rotate: () => gsap.utils.random(-25, 25), duration: .9, ease: 'back.out(2.2)', stagger: .018,
      scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
  });
}

export function revealOnScroll(sel, opts = {}) {
  $$(sel).forEach((el) => gsap.from(el, { y: 50, opacity: 0, duration: 1.1, ease: 'expo.out', ...opts, scrollTrigger: { trigger: el, start: 'top 90%', once: true } }));
}

export async function loadData() {
  try { return await (await fetch('/data/piezas.json')).json(); } catch { return { poses: [], piezas: [], campus: [], stickers: [] }; }
}
