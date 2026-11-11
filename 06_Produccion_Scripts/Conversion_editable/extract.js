(rootSel) => {
  const roots = [...document.querySelectorAll(rootSel)];
  // ---------- font ascent (as Chrome lays it out) ----------
  const ASC = {};
  function ascent(fam) {
    if (ASC[fam] != null) return ASC[fam];
    const s = document.createElement('div');
    s.style.cssText = `position:absolute;left:0;top:0;font-family:${fam};font-size:100px;line-height:normal;white-space:nowrap`;
    s.innerHTML = '<span>H</span><i style="display:inline-block;width:0;height:0;vertical-align:baseline"></i>';
    document.body.appendChild(s);
    const r = document.createRange(); r.selectNodeContents(s.firstChild.firstChild);
    const top = r.getClientRects()[0].top, b = s.lastChild.getBoundingClientRect().bottom;
    s.remove(); return (ASC[fam] = (b - top) / 100);
  }
  // ---------- record & neutralise transforms ----------
  const XF = new Map();
  const all = roots.flatMap(r => [r, ...r.querySelectorAll('*')]);
  for (const el of all) {
    const cs = getComputedStyle(el);
    if (cs.transform && cs.transform !== 'none') {
      const m = new DOMMatrix(cs.transform);
      const o = cs.transformOrigin.split(' ').map(parseFloat);
      XF.set(el, { a: m.a, b: m.b, c: m.c, d: m.d, e: m.e, f: m.f, ox: o[0], oy: o[1] });
    }
  }
  for (const el of XF.keys()) el.style.setProperty('transform', 'none', 'important');
  document.body.offsetHeight;

  const col = s => {
    if (!s || s === 'transparent') return null;
    const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(parseFloat);
    const a = p.length > 3 ? p[3] : 1; if (a === 0) return null;
    return [Math.round(p[0]), Math.round(p[1]), Math.round(p[2]), +a.toFixed(3)];
  };
  // split top-level commas
  const splitTop = s => { const out = []; let d = 0, cur = ''; for (const ch of s) { if (ch === '(') d++; if (ch === ')') d--; if (ch === ',' && d === 0) { out.push(cur.trim()); cur = ''; } else cur += ch; } if (cur.trim()) out.push(cur.trim()); return out; };
  function parseShadows(s) {
    if (!s || s === 'none') return [];
    return splitTop(s).map(t => {
      const c = t.match(/rgba?\([^)]+\)/); const rest = t.replace(c ? c[0] : '', '').trim().split(/\s+/).map(parseFloat);
      return { c: col(c ? c[0] : 'rgb(0,0,0)'), x: rest[0] || 0, y: rest[1] || 0, blur: rest[2] || 0, spread: rest[3] || 0, inset: /inset/.test(t) };
    });
  }
  function parseGrad(s) {
    // linear-gradient / radial-gradient (single, non-repeating)
    const m = s.match(/^(linear|radial)-gradient\((.*)\)$/); if (!m) return null;
    const parts = splitTop(m[2]); let angle = 180, shape = null;
    if (m[1] === 'linear') {
      if (/deg$/.test(parts[0])) angle = parseFloat(parts.shift());
      else if (/^to /.test(parts[0])) { const t = parts.shift(); angle = { 'to top': 0, 'to right': 90, 'to bottom': 180, 'to left': 270 }[t] ?? 180; }
    } else { if (!/^rgb/.test(parts[0])) shape = parts.shift(); }
    const stops = parts.map(p => { const c = p.match(/rgba?\([^)]+\)/); const pos = p.replace(c[0], '').trim(); return { c: col(c[0]) || [col(c[0].replace(/,[^,]*\)$/, ',1)'))?.[0] ?? 0, 0, 0, 0], p: pos ? parseFloat(pos) : null }; });
    // transparent stops come back as rgba(r,g,b,0) -> col() returns null; recover rgb
    parts.forEach((p, i) => { const mm = p.match(/rgba?\(([^)]+)\)/); const v = mm[1].split(/[ ,\/]+/).filter(Boolean).map(parseFloat); stops[i].c = [v[0], v[1], v[2], v.length > 3 ? v[3] : 1]; });
    stops.forEach((st, i) => { if (st.p == null) st.p = i === 0 ? 0 : (i === stops.length - 1 ? 100 : null); });
    for (let i = 0; i < stops.length; i++) if (stops[i].p == null) { let j = i; while (stops[j].p == null) j++; const a = stops[i - 1].p, b = stops[j].p; for (let k = i; k < j; k++) stops[k].p = a + (b - a) * (k - i + 1) / (j - i + 1); }
    return { type: m[1], angle, shape, stops };
  }
  const rad = (cs, w, h) => {
    const g = k => { const v = cs[k].split(' '); const rx = v[0].endsWith('%') ? parseFloat(v[0]) / 100 * w : parseFloat(v[0]); const ry = v[1] ? (v[1].endsWith('%') ? parseFloat(v[1]) / 100 * h : parseFloat(v[1])) : (v[0].endsWith('%') ? parseFloat(v[0]) / 100 * h : rx); return [rx || 0, ry || 0]; };
    let r = [g('borderTopLeftRadius'), g('borderTopRightRadius'), g('borderBottomRightRadius'), g('borderBottomLeftRadius')];
    // CSS clamping
    let f = 1; const sum = (a, b) => a + b;
    f = Math.min(f, w / Math.max(1e-6, r[0][0] + r[1][0]), w / Math.max(1e-6, r[3][0] + r[2][0]), h / Math.max(1e-6, r[0][1] + r[3][1]), h / Math.max(1e-6, r[1][1] + r[2][1]));
    if (f < 1) r = r.map(([x, y]) => [x * f, y * f]);
    return r.some(([x, y]) => x > 0.01 || y > 0.01) ? r.map(([x, y]) => [+x.toFixed(2), +y.toFixed(2)]) : null;
  };
  const visibleBg = cs => col(cs.backgroundColor) || (cs.backgroundImage && cs.backgroundImage !== 'none');
  const hasBorder = cs => ['Top', 'Right', 'Bottom', 'Left'].some(s => parseFloat(cs['border' + s + 'Width']) > 0 && cs['border' + s + 'Style'] !== 'none');
  const isInline = n => {
    if (n.nodeType !== 1) return false;
    if (['IMG', 'SVG', 'svg', 'BR', 'TABLE'].includes(n.tagName)) return n.tagName === 'BR';
    const cs = getComputedStyle(n);
    if (!(cs.display === 'inline' || cs.display === 'inline-block')) return false;
    if (cs.position === 'absolute') return false;
    if (visibleBg(cs) || hasBorder(cs)) return false;
    return [...n.children].every(isInline);
  };
  let RO = { x: 0, y: 0 };
  const R = el => { const r = el.getBoundingClientRect(); return { x: r.left - RO.x, y: r.top - RO.y, w: r.width, h: r.height }; };
  const fam = f => /titan/i.test(f) ? 'Titan' : 'Brico';
  const raster = []; // elements needing a raster fallback for their background
  let rid = 0;

  function styleOf(e) {
    const cs = getComputedStyle(e);
    const sw = parseFloat(cs.webkitTextStrokeWidth) || 0;
    const ts = parseShadows(cs.textShadow);
    return {
      f: fam(cs.fontFamily), w: Math.round(parseFloat(cs.fontWeight)), st: parseFloat(cs.fontStretch) || 100,
      s: parseFloat(cs.fontSize), c: col(cs.color), ls: parseFloat(cs.letterSpacing) || 0, up: cs.textTransform === 'uppercase',
      sw: sw ? +sw.toFixed(2) : 0, sc: sw ? col(cs.webkitTextStrokeColor) : null, ts: ts.length ? ts : null,
    };
  }
  function textItem(el) {
    const chars = [];
    const walkT = (n) => {
      for (const c of n.childNodes) {
        if (c.nodeType === 3) {
          const p = c.parentElement; const st = styleOf(p); const xf = XF.get(p);
          for (let i = 0; i < c.length; i++) {
            const ch = c.data[i];
            const rg = document.createRange(); rg.setStart(c, i); rg.setEnd(c, i + 1);
            const rs = rg.getClientRects(); if (!rs.length) continue; const rc = rs[0];
            if (/\s/.test(ch) && rc.width < 0.01) continue;
            const o = { ch: /\s/.test(ch) ? ' ' : (st.up ? ch.toUpperCase() : ch), x: rc.left - RO.x, r: rc.right - RO.x, bl: rc.top - RO.y + ascent(st.f === 'Titan' ? 'Titan' : 'Brico') * st.s, st };
            if (xf && p.classList.contains('l')) { o.rot = Math.atan2(xf.b, xf.a) * 180 / Math.PI; o.ty = xf.f; }
            chars.push(o);
          }
        } else if (c.nodeType === 1) {
          if (c.tagName === 'BR') { chars.push({ br: 1 }); continue; }
          if (isInline(c)) walkT(c);
        }
      }
    };
    walkT(el);
    if (!chars.some(c => c.ch && c.ch.trim())) return null;
    const lines = []; let cur = null, brs = 0, prev = null;
    for (const c of chars) {
      if (c.br) { brs++; cur = null; prev = null; continue; }
      if (cur && prev && (Math.abs(c.bl - cur.bl) > 2 && c.x < prev.r - 1)) cur = null;
      if (!cur) { cur = { bl: c.bl, ch: [], br: brs }; lines.push(cur); }
      cur.ch.push(c); prev = c;
    }
    const L = [];
    for (const ln of lines) {
      while (ln.ch.length && ln.ch[0].ch === ' ') ln.ch.shift();
      while (ln.ch.length && ln.ch[ln.ch.length - 1].ch === ' ') ln.ch.pop();
      if (!ln.ch.length) continue;
      // baseline = most common among chars (bounce letters are unshifted now)
      const bl = ln.ch.map(c => c.bl).sort((a, b) => a - b)[Math.floor(ln.ch.length / 2)];
      const runs = []; let rr = null;
      for (const c of ln.ch) {
        const key = JSON.stringify(c.st) + '|' + (c.rot ?? '') + '|' + (c.ty ?? '');
        if (c.rot != null || !rr || rr.key !== key) { rr = { key, t: '', st: c.st, rot: c.rot, ty: c.ty }; runs.push(rr); }
        rr.t += c.ch;
      }
      runs.forEach(r => delete r.key);
      L.push({ bl: +bl.toFixed(2), x0: +ln.ch[0].x.toFixed(2), x1: +ln.ch[ln.ch.length - 1].r.toFixed(2), runs, br: ln.br });
    }
    // "hard" line count = breaks by <br>; wrapped if more lines than that
    const nbr = new Set(L.map(l => l.br)).size;
    const cs = getComputedStyle(el); const r = R(el);
    const pl = parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth), pr = parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth);
    const pt = parseFloat(cs.paddingTop) + parseFloat(cs.borderTopWidth);
    let lh = parseFloat(cs.lineHeight); if (isNaN(lh)) lh = null;
    return { k: 't', lines: L, wrapped: L.length > nbr, align: cs.textAlign, box: { x: r.x + pl, y: r.y + pt, w: r.w - pl - pr }, lh, cls: el.className || '' };
  }

  function boxItems(el, cs, r, out, only) {
    const rr = rad(cs, r.w, r.h);
    // box-shadow (outer) drawn first
    for (const sh of (only === false ? [] : parseShadows(cs.boxShadow).reverse())) {
      if (sh.inset || !sh.c) continue;
      if (sh.spread && !sh.x && !sh.y && !sh.blur) { // ring (e.g. 0 0 0 3px)
        out.push({ k: 'r', x: r.x - sh.spread, y: r.y - sh.spread, w: r.w + 2 * sh.spread, h: r.h + 2 * sh.spread, rad: rr ? rr.map(([a, b]) => [a + sh.spread, b + sh.spread]) : null, fill: sh.c, name: 'Contorno' });
        continue;
      }
      out.push({ k: 'r', x: r.x + sh.x - sh.spread, y: r.y + sh.y - sh.spread, w: r.w + 2 * sh.spread, h: r.h + 2 * sh.spread, rad: rr, fill: sh.c, blur: sh.blur, name: sh.blur ? 'Sombra suave' : 'Sombra' });
    }
    if (only === true) return;
    const bg = col(cs.backgroundColor);
    const bi = cs.backgroundImage && cs.backgroundImage !== 'none' ? cs.backgroundImage : null;
    const bw = ['Top', 'Right', 'Bottom', 'Left'].map(s => cs['border' + s + 'Style'] !== 'none' ? parseFloat(cs['border' + s + 'Width']) || 0 : 0);
    const bc = ['Top', 'Right', 'Bottom', 'Left'].map(s => col(cs['border' + s + 'Color']));
    const uniform = bw.every(v => v === bw[0]) && bw[0] > 0 && bc.every(c => c && bc[0] && c.join() === bc[0].join());
    const name = nameOf(el);
    let grad = null;
    if (bi && !/url\(|repeating/.test(bi) && splitTop(bi).length === 1) grad = parseGrad(bi);
    if (bg || grad || uniform) {
      out.push({ k: 'r', x: r.x, y: r.y, w: r.w, h: r.h, rad: rr, fill: bg, grad, stroke: uniform ? { w: bw[0], c: bc[0], dash: cs.borderTopStyle === 'dashed' } : null, name });
    }
    if (bi && !grad) { // raster fallback for patterns / repeating gradients
      const id = 'bg' + (rid++); raster.push({ id, css: { backgroundImage: bi, backgroundSize: cs.backgroundSize, backgroundPosition: cs.backgroundPosition, backgroundRepeat: cs.backgroundRepeat, backgroundColor: 'transparent', borderRadius: cs.borderRadius }, w: r.w, h: r.h, base: document.baseURI });
      out.push({ k: 'ras', id, x: r.x, y: r.y, w: r.w, h: r.h, rad: rr, name: /trama/.test(el.className) ? 'Trama' : name + ' (textura)' });
    }
    if (!uniform) bw.forEach((w, i) => {
      if (!w || !bc[i]) return;
      const b = [{ x: r.x, y: r.y, w: r.w, h: w }, { x: r.x + r.w - w, y: r.y, w, h: r.h }, { x: r.x, y: r.y + r.h - w, w: r.w, h: w }, { x: r.x, y: r.y, w, h: r.h }][i];
      out.push({ k: 'r', ...b, fill: bc[i], name: 'Línea' });
    });
  }
  function nameOf(el) {
    const c = (el.className && el.className.baseVal === undefined ? el.className : '') || '';
    if (/\bbub\b|bubble/.test(c)) return 'Globo de diálogo';
    if (/tail/.test(c)) return 'Cola del globo';
    if (/\bsep\b/.test(c)) return 'Separador';
    if (/\btag\b/.test(c)) return 'Etiqueta';
    if (/trama/.test(c)) return 'Trama';
    const st = el.getAttribute('style') || '';
    if (/inset:0/.test(st)) return 'Fondo';
    return 'Forma';
  }
  function imgItem(el, cs, r) {
    const src = el.currentSrc || el.src;
    const nw = el.naturalWidth, nh = el.naturalHeight;
    let fit = cs.objectFit, pr = { x: r.x, y: r.y, w: r.w, h: r.h };
    const bl = parseFloat(cs.borderLeftWidth) || 0, bt = parseFloat(cs.borderTopWidth) || 0, br_ = parseFloat(cs.borderRightWidth) || 0, bb = parseFloat(cs.borderBottomWidth) || 0;
    const pl = parseFloat(cs.paddingLeft) || 0, pt = parseFloat(cs.paddingTop) || 0, prr = parseFloat(cs.paddingRight) || 0, pb = parseFloat(cs.paddingBottom) || 0;
    const cb = { x: r.x + bl + pl, y: r.y + bt + pt, w: r.w - bl - pl - br_ - prr, h: r.h - bt - pt - bb - pb };
    pr = { ...cb };
    if (nw && nh && (fit === 'cover' || fit === 'contain')) {
      const s = fit === 'cover' ? Math.max(cb.w / nw, cb.h / nh) : Math.min(cb.w / nw, cb.h / nh);
      const op = cs.objectPosition.split(' ').map(v => parseFloat(v) / 100);
      pr = { w: nw * s, h: nh * s }; pr.x = cb.x + (cb.w - pr.w) * (isNaN(op[0]) ? .5 : op[0]); pr.y = cb.y + (cb.h - pr.h) * (isNaN(op[1]) ? .5 : op[1]);
    }
    const rr = rad(cs, r.w, r.h);
    const clip = (fit === 'cover' && (pr.w > cb.w + 0.5 || pr.h > cb.h + 0.5)) || !!rr;
    const mask = cs.webkitMaskImage && cs.webkitMaskImage !== 'none' ? parseGrad(cs.webkitMaskImage) : null;
    return { k: 'img', src, nw, nh, place: pr, clip: clip ? { ...cb, rad: rr } : null, mask, box: cb, name: decodeURIComponent(src.split('/').pop()) };
  }
  function svgItem(el, r) {
    const c = el.cloneNode(true);
    const fix = (o, n) => { const cs = getComputedStyle(n); for (const a of ['fill', 'stroke']) { const v = o.getAttribute(a); if (v && /var\(/.test(v)) o.setAttribute(a, cs[a]); } [...o.children].forEach((k, i) => fix(k, n.children[i])); };
    fix(c, el); c.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    // invisible frame so Illustrator keeps the svg canvas (removed after import)
    const vb = (el.getAttribute('viewBox') || `0 0 ${el.getAttribute('width') || r.w} ${el.getAttribute('height') || r.h}`).split(/[ ,]+/).map(parseFloat);
    if (!el.getAttribute('viewBox')) c.setAttribute('viewBox', vb.join(' '));
    const fr = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    fr.setAttribute('id', 'FRAME'); fr.setAttribute('x', vb[0]); fr.setAttribute('y', vb[1]); fr.setAttribute('width', vb[2]); fr.setAttribute('height', vb[3]);
    fr.setAttribute('fill', 'none'); fr.setAttribute('stroke', 'none'); c.insertBefore(fr, c.firstChild);
    c.setAttribute('width', r.w); c.setAttribute('height', r.h);
    return { k: 'svg', svg: c.outerHTML, x: r.x, y: r.y, w: r.w, h: r.h, name: 'Ícono' };
  }

  function walk(el, out) {
    if (['SCRIPT', 'STYLE', 'BR'].includes(el.tagName)) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const op = parseFloat(cs.opacity); if (op === 0) return;
    const xf = XF.get(el);
    let target = out;
    const filt = cs.filter && cs.filter !== 'none' ? cs.filter : null;
    const clipEl = el !== RO.el && el.tagName !== 'IMG' && (cs.overflow === 'hidden' || cs.overflowX === 'hidden') && [...el.querySelectorAll('*')].some(k => { const a = k.getBoundingClientRect(), b = el.getBoundingClientRect(); return a.left < b.left - 1 || a.top < b.top - 1 || a.right > b.right + 1 || a.bottom > b.bottom + 1; });
    if ((xf && !el.classList.contains('l')) || op < 0.999 || filt) {
      const r = R(el);
      const g = { k: 'g', op, ch: [], name: nameOf(el) === 'Forma' ? (el.tagName === 'IMG' ? 'Imagen' : 'Grupo') : nameOf(el) };
      if (xf && !el.classList.contains('l')) { const flip = xf.a * xf.d - xf.b * xf.c < 0;
        g.xf = { flip, ang: (flip ? Math.atan2(-xf.b, -xf.a) : Math.atan2(xf.b, xf.a)) * 180 / Math.PI, sc: Math.hypot(xf.a, xf.b), ox: r.x + xf.ox, oy: r.y + xf.oy, tx: xf.e, ty: xf.f }; }
      if (filt) { const m = filt.match(/drop-shadow\((rgba?\([^)]+\))\s+([-\d.]+)px\s+([-\d.]+)px\s+([-\d.]+)px\)/); if (m) g.ds = { c: col(m[1]), x: +m[2], y: +m[3], blur: +m[4] }; }
      out.push(g); target = g.ch;
    }
    const r = R(el);
    if (clipEl) {
      // shadows stay outside the clipping group
      const sh = []; boxItems(el, cs, r, sh, true); sh.forEach(x => target.push(x));
      const g = { k: 'g', op: 1, ch: [], name: nameOf(el) === 'Forma' ? 'Tarjeta' : nameOf(el), clip: { x: r.x, y: r.y, w: r.w, h: r.h, rad: rad(cs, r.w, r.h) } };
      target.push(g); target = g.ch;
      boxItems(el, cs, r, target, false);
      const t = textItem(el); if (t) target.push(t);
      for (const c of el.children) if (!isInline(c)) walk(c, target);
      return;
    }
    if (el.tagName === 'IMG') { boxItems(el, cs, r, target); target.push(imgItem(el, cs, r)); return; }
    if (el.tagName.toLowerCase() === 'svg') { target.push(svgItem(el, r)); return; }
    if (el !== RO.el) boxItems(el, cs, r, target);
    const t = textItem(el); if (t) target.push(t);
    for (const c of el.children) if (!isInline(c)) walk(c, target);
  }
  const res = [];
  for (const root of roots) {
    const rr = root.getBoundingClientRect(); RO = { x: rr.left, y: rr.top, el: root };
    const cs = getComputedStyle(root); const items = [];
    const bg = col(cs.backgroundColor);
    if (bg) items.push({ k: 'r', x: 0, y: 0, w: rr.width, h: rr.height, fill: bg, name: 'Fondo' });
    walk(root, items);
    res.push({ w: rr.width, h: rr.height, items });
  }
  return { pages: res, raster, asc: ASC };
}
