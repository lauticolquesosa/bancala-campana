// Bancala · constructor HTML -> Illustrator (ES3)
// expects global DOC = {name, out, S, pages:[{name,w,h,items}], png:'dir or null'}
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
app.coordinateSystem = CoordinateSystem.DOCUMENTCOORDINATESYSTEM;
var S = DOC.S, LOG = [];
var GAP = 120;
var FONTS = {};
function font(f, w, st) {
  var n;
  if (f == 'Titan') n = 'TitanOne';
  else if (f == 'Sym') n = 'SegoeUISymbol';
  else {
    var ws = 'ExtraBold';
    if (w <= 750) ws = 'Bold';
    if (w <= 650) ws = 'SemiBold';
    if (w <= 550) ws = 'Medium';
    if (w <= 450) ws = 'Regular';
    n = (st < 95 ? 'BricolageGrotesqueCondensed-' : 'BricolageGrotesque-') + ws;
  }
  if (!FONTS[n]) FONTS[n] = app.textFonts.getByName(n);
  return FONTS[n];
}
var doc, ABX = [], SW = {};
var PALETTE = [['Navy', [27, 77, 139]], ['Azul', [45, 124, 222]], ['Verde', [83, 159, 115]], ['Menta', [122, 226, 166]], ['Tinta', [58, 29, 12]],
  ['Madera', [232, 137, 47]], ['Crema', [251, 241, 223]], ['Papel', [245, 241, 232]], ['Carbón', [42, 40, 41]], ['Blanco', [255, 255, 255]]];
function rgbc(c) { var k = new RGBColor(); k.red = c[0]; k.green = c[1]; k.blue = c[2]; return k; }
function color(c) {
  var key = c[0] + ',' + c[1] + ',' + c[2];
  if (SW[key]) { var sc = new SpotColor(); sc.spot = SW[key]; sc.tint = 100; return sc; }
  return rgbc(c);
}
function X(p, x) { return ABX[p] + x * S; }
function Y(y) { return -y * S; }

function makeDoc() {
  var W = 0, H = 0, i;
  doc = app.documents.add(DocumentColorSpace.RGB, DOC.pages[0].w * S, DOC.pages[0].h * S);
  var tot = 0;
  for (i = 0; i < DOC.pages.length; i++) tot += DOC.pages[i].w * S + GAP;
  // fila muy ancha: centrarla en el lienzo (limite ~ +-8191 pt desde el centro)
  var x = tot > 7000 ? -Math.round(tot / 2) : 0;
  for (i = 0; i < DOC.pages.length; i++) { ABX.push(x); x += DOC.pages[i].w * S + GAP; }
  doc.artboards[0].artboardRect = [ABX[0], 0, ABX[0] + DOC.pages[0].w * S, -DOC.pages[0].h * S];
  doc.artboards[0].name = DOC.pages[0].name;
  for (i = 1; i < DOC.pages.length; i++) {
    var ab = doc.artboards.add([ABX[i], 0, ABX[i] + DOC.pages[i].w * S, -DOC.pages[i].h * S]); ab.name = DOC.pages[i].name;
  }
  try { doc.rasterEffectSettings.resolution = 300; } catch (e) { }
  // swatches: global process colours for the brand palette
  var grp; try { grp = doc.swatchGroups.add(); grp.name = 'Bancala'; } catch (e) { grp = null; }
  for (i = 0; i < PALETTE.length; i++) {
    var sp = null;
    for (var tr = 0; tr < 5 && !sp; tr++) {
      try { sp = doc.spots.add(); sp.color = rgbc(PALETTE[i][1]); sp.colorType = ColorModel.PROCESS; sp.name = 'Bancala ' + PALETTE[i][0]; }
      catch (e) { LOG.push('swatch retry ' + PALETTE[i][0] + ': ' + e); try { if (sp) sp.remove(); } catch (e2) { } sp = null; app.redraw(); $.sleep(300); }
    }
    if (!sp) continue;
    SW[PALETTE[i][1].join(',')] = sp;
    if (grp) { try { var sw = doc.swatches.getByName(sp.name); grp.addSwatch(sw); } catch (e) { } }
  }
}

// ---------- shapes ----------
var K = 0.5522847, GN = 0;
function pathRR(parent, p, x, y, w, h, rad) {
  var pa = parent.pathItems.add();
  if (!rad) {
    pa.setEntirePath([[X(p, x), Y(y)], [X(p, x + w), Y(y)], [X(p, x + w), Y(y + h)], [X(p, x), Y(y + h)]]); pa.closed = true; return pa;
  }
  // corners: tl,tr,br,bl each [rx,ry]
  var tl = rad[0], tr = rad[1], br = rad[2], bl = rad[3];
  var pts = []; // [anchor, left(in), right(out)] in px, clockwise from top-left top edge
  function P(ax, ay, lx, ly, rx, ry) { pts.push([[X(p, ax), Y(ay)], [X(p, lx), Y(ly)], [X(p, rx), Y(ry)]]); }
  // top edge start (after tl corner)
  P(x + tl[0], y, x + tl[0] - tl[0] * K, y, x + tl[0], y);
  P(x + w - tr[0], y, x + w - tr[0], y, x + w - tr[0] + tr[0] * K, y);
  P(x + w, y + tr[1], x + w, y + tr[1] - tr[1] * K, x + w, y + tr[1]);
  P(x + w, y + h - br[1], x + w, y + h - br[1], x + w, y + h - br[1] + br[1] * K);
  P(x + w - br[0], y + h, x + w - br[0] + br[0] * K, y + h, x + w - br[0], y + h);
  P(x + bl[0], y + h, x + bl[0], y + h, x + bl[0] - bl[0] * K, y + h);
  P(x, y + h - bl[1], x, y + h - bl[1] + bl[1] * K, x, y + h - bl[1]);
  P(x, y + tl[1], x, y + tl[1], x, y + tl[1] - tl[1] * K);
  for (var i = 0; i < pts.length; i++) {
    var q = pa.pathPoints.add(); q.anchor = pts[i][0]; q.leftDirection = pts[i][1]; q.rightDirection = pts[i][2]; q.pointType = PointType.SMOOTH;
  }
  pa.closed = true;
  // remove duplicate zero-length points (when radius==0 on a side)
  for (var j = pa.pathPoints.length - 1; j > 0; j--) {
    var A = pa.pathPoints[j].anchor, B = pa.pathPoints[j - 1].anchor;
    if (Math.abs(A[0] - B[0]) < 0.001 && Math.abs(A[1] - B[1]) < 0.001) { pa.pathPoints[j - 1].rightDirection = pa.pathPoints[j].rightDirection; pa.pathPoints[j].remove(); }
  }
  return pa;
}
function gradFill(pa, g, nm) {
  var gr = doc.gradients.add(); GN++; gr.name = (nm || 'Degradé') + ' ' + GN;
  gr.type = g.type == 'radial' ? GradientType.RADIAL : GradientType.LINEAR;
  var st = g.stops;
  while (gr.gradientStops.length < st.length) gr.gradientStops.add();
  for (var i = 0; i < st.length; i++) {
    var s = gr.gradientStops[i]; s.rampPoint = Math.max(0, Math.min(100, st[i].p)); s.midPoint = 50; s.color = color(st[i].c); s.opacity = st[i].c[3] * 100;
  }
  var gc = new GradientColor(); gc.gradient = gr; pa.fillColor = gc;
  if (g.type == 'linear') {
    var ang = 90 - g.angle; // css 0deg = upwards
    if (Math.abs(ang) > 0.01) pa.rotate(ang, false, false, true, false, Transformation.CENTER);
  }
}
function rect(parent, p, it) {
  var x = it.x, y = it.y, w = it.w, h = it.h, rad = it.rad, sw = 0;
  if (it.stroke) { sw = it.stroke.w; x += sw / 2; y += sw / 2; w -= sw; h -= sw; if (rad) { var r2 = []; for (var i = 0; i < 4; i++) r2.push([Math.max(0, rad[i][0] - sw / 2), Math.max(0, rad[i][1] - sw / 2)]); rad = r2; } }
  var radial = it.grad && it.grad.type == 'radial';
  var pa = pathRR(parent, p, x, y, w, h, rad);
  pa.name = it.name || 'Forma';
  if (it.grad && !radial) { gradFill(pa, it.grad, it.name); }
  else if (radial) {
    // build as circle, then squash so the radial gradient follows the ellipse
    pa.remove(); var d = Math.max(w, h);
    pa = parent.pathItems.ellipse(Y(y + h / 2 - d / 2), X(p, x + w / 2 - d / 2), d * S, d * S); pa.name = 'Sombra (degradé radial)';
    gradFill(pa, it.grad, 'Sombra radial');
    pa.resize(w / d * 100, h / d * 100, true, true, true, true, 100, Transformation.CENTER);
  }
  else if (it.fill) { pa.fillColor = color(it.fill); if (it.fill[3] < 1) pa.opacity = it.fill[3] * 100; }
  else pa.filled = false;
  if (it.stroke && it.stroke.c) {
    pa.stroked = true; pa.strokeColor = color(it.stroke.c); pa.strokeWidth = sw * S;
    if (it.stroke.c[3] < 1 && !it.fill) pa.opacity = it.stroke.c[3] * 100;
    if (it.stroke.dash) { pa.strokeDashes = [sw * 2.2 * S, sw * 1.6 * S]; pa.strokeCap = StrokeCap.BUTTENDCAP; }
  } else pa.stroked = false;
  if (it.blur) fxBlur(pa, it.blur * S);
  return pa;
}
function fxBlur(item, b) {
  try { item.applyEffect('<LiveEffect name="Adobe PSL Gaussian Blur"><Dict data="R blur ' + (b / 2) + '"/></LiveEffect>'); } catch (e) { LOG.push('blur ' + e); }
}
function fxShadow(item, x, y, blur, op) {
  try {
    item.applyEffect('<LiveEffect name="Adobe Drop Shadow"><Dict data="R horz ' + x + ' R vert ' + y + ' R blur ' + blur + ' R opac ' + op + ' I mode 0 R dark 0 I csrc 0 B pspc 0 B usePSLBlur 1"/></LiveEffect>');
  } catch (e) { LOG.push('shadow ' + e); }
}

// ---------- images ----------
function place(parent, p, it) {
  var f = new File(it.file);
  if (!f.exists) { LOG.push('missing ' + it.file); return null; }
  var pl = it.place, item;
  if (/\.svg$/i.test(it.file)) {
    item = parent.groupItems.createFromFile(f);
    item.width = pl.w * S; item.height = pl.h * S; item.position = [X(p, pl.x), Y(pl.y)];
    item.name = it.name;
    for (var fi = item.pageItems.length - 1; fi >= 0; fi--) { if (item.pageItems[fi].name == 'FRAME') { item.pageItems[fi].remove(); break; } }
    if (item.pageItems.length == 1 && item.pageItems[0].typename == 'GroupItem') { var inner = item.pageItems[0]; inner.name = it.name; inner.move(item, ElementPlacement.PLACEBEFORE); item.remove(); item = inner; }
  } else {
    var pi2 = parent.placedItems.add(); pi2.file = f;
    pi2.width = pl.w * S; pi2.height = pl.h * S; pi2.position = [X(p, pl.x), Y(pl.y)];
    pi2.embed(); item = parent.pageItems[0]; item.name = it.name;
  }
  if (it.clip) {
    var g = parent.groupItems.add(); g.name = it.name + ' (marco)';
    item.move(g, ElementPlacement.PLACEATEND);
    var c = pathRR(g, p, it.clip.x, it.clip.y, it.clip.w, it.clip.h, it.clip.rad);
    c.move(g, ElementPlacement.PLACEATBEGINNING); c.clipping = true; g.clipped = true;
    item = g;
  }
  return item;
}

// ---------- text ----------
var AASC = {};
function areaAscent(st) { // distance frame-top -> first baseline for 1pt type, measured in Illustrator itself
  var f = font(st.f, st.w, st.st), key = f.name;
  if (AASC[key] != null) return AASC[key];
  var r = doc.pathItems.rectangle(5000, 0, 2000, 400), t = doc.textFrames.areaText(r);
  t.contents = 'H'; t.textRange.characterAttributes.textFont = f; t.textRange.characterAttributes.size = 100;
  var o = t.duplicate().createOutline(); var b = o.geometricBounds; // [l,t,r,b]
  AASC[key] = (5000 - b[3]) / 100; o.remove(); t.remove();
  return AASC[key];
}
function applyStyle(rng, st) {
  var ca = rng.characterAttributes;
  ca.textFont = font(st.f, st.w, st.st); ca.size = st.s * S;
  ca.fillColor = color(st.c);
  ca.tracking = Math.round(st.ls / st.s * 1000);
  ca.horizontalScale = 100; ca.verticalScale = 100; ca.autoLeading = false;
  if (st.sw) { ca.strokeColor = color(st.sc); ca.strokeWeight = st.sw / 2 * S; }
  else ca.strokeColor = new NoColor();
}
function text(parent, p, it) {
  var L = it.lines; if (!L.length) return null;
  var lead = it.lead || it.lh || 0, st0 = firstStyle(L);
  if (!lead) lead = st0.s * 1.2;
  var str = [], i, j;
  for (i = 0; i < L.length; i++) { var s = ''; for (j = 0; j < L[i].runs.length; j++) s += L[i].runs[j].t; str.push(s); }
  var just = Justification.LEFT;
  if (it.align == 'center') just = Justification.CENTER;
  if (it.align == 'right' || it.align == 'end') just = Justification.RIGHT;
  var tf, area = it.wrapped;
  if (area) {
    var bx = { x: it.box.x, w: it.box.w }, ext = 3;
    if (just == Justification.LEFT) { var mx = 1e9; for (var q = 0; q < L.length; q++) if (L[q].runs.length) mx = Math.min(mx, L[q].x0); if (mx > bx.x && mx < bx.x + bx.w) { bx.w -= mx - bx.x; bx.x = mx; } }
    var rp = parent.pathItems.rectangle(Y(L[0].bl - areaAscent(st0) * st0.s), X(p, bx.x) - (just == Justification.CENTER ? ext / 2 * S : (just == Justification.RIGHT ? ext * S : 0)), (bx.w + ext) * S, (L[L.length - 1].bl - L[0].bl + st0.s * 2) * S);
    tf = parent.textFrames.areaText(rp);
    tf.contents = joinLines(str, L, ' ');
  } else {
    var ax = L[0].x0;
    if (just == Justification.CENTER) ax = (L[0].x0 + L[0].x1) / 2;
    if (just == Justification.RIGHT) ax = L[0].x1;
    tf = parent.textFrames.pointText([X(p, ax), Y(L[0].bl)]);
    tf.contents = str.join('\r');
  }
  tf.textRange.paragraphAttributes.justification = just;
  try { tf.textRange.paragraphAttributes.hyphenation = false; } catch (e) { }
  // styles by run
  var all = tf.textRange; applyStyle(all, st0); all.characterAttributes.leading = lead * S;
  var pos = 0, chars = tf.textRange.characters;
  var hasStroke = false, ts = null;
  for (i = 0; i < L.length; i++) {
    for (j = 0; j < L[i].runs.length; j++) {
      var r = L[i].runs[j], n = r.t.length;
      if (r.st.sw) hasStroke = true;
      if (r.st.ts && !ts) ts = r.st.ts[0];
      var differs = JSON_eq(r.st, st0) ? false : true;
      if (differs || r.rot != null) {
        for (var k = 0; k < n; k++) {
          var ch = chars[pos + k];
          if (differs) { applyStyle(ch, r.st); ch.characterAttributes.leading = lead * S; }
          if (r.rot != null) { ch.characterAttributes.rotation = -r.rot; ch.characterAttributes.baselineShift = -r.ty * S; }
        }
      }
      pos += n;
    }
    pos += 1; // separator (\r or space)
  }
  if (area) {
    tf.textRange.paragraphAttributes.justification = just;
    // verify wrapping: search a frame width that reproduces the browser's exact line breaks
    var w0 = tf.textPath.width, ok = false, D = [0, -0.01, 0.01, -0.02, 0.02, -0.03, 0.03, -0.045, 0.045, -0.06, 0.06, -0.08, 0.08, 0.1];
    for (var di = 0; di < D.length && !ok; di++) {
      tf.textPath.width = w0 * (1 + D[di]);
      if (tf.lines.length != L.length) continue;
      ok = true;
      for (var li = 0; li < L.length; li++) { if (tf.lines[li].contents.replace(/\s+$/, '') != str[li]) { ok = false; break; } }
    }
    if (!ok) { // keep it as point text with the browser's line breaks
      LOG.push('wrap fallback: ' + str[0].substr(0, 30));
      tf.remove(); it.wrapped = false; return text(parent, p, it);
    }
    // grow the frame a bit at the bottom so nothing overflows
    tf.textPath.height = tf.textPath.height + st0.s * S;
  }
  // order matters: drop shadow first, then stroke offset (outside stroke)
  if (ts) { fxShadow(tf, ts.x * S, ts.y * S, ts.blur * S * 0.5, ts.c[3]); }
  if (hasStroke) { try { tf.applyEffect('<LiveEffect name="Adobe Stroke Offset"><Dict data="B StrokeOffsetInside 0"/></LiveEffect>'); } catch (e) { LOG.push('so ' + e); } }
  var a0 = st0.c[3]; if (a0 < 1) tf.opacity = a0 * 100;
  return tf;
}
function firstStyle(L) { for (var i = 0; i < L.length; i++) if (L[i].runs.length) return L[i].runs[0].st; }
function joinLines(str, L, soft) {
  var s = str[0];
  for (var i = 1; i < str.length; i++) s += (L[i].br != L[i - 1].br ? String.fromCharCode(13) : soft) + str[i];
  return s;
}
function JSON_eq(a, b) {
  return a.f == b.f && a.w == b.w && a.st == b.st && a.s == b.s && a.ls == b.ls && a.sw == b.sw && a.c.join() == b.c.join() && ((a.sc || []).join() == (b.sc || []).join());
}

function poly(parent, p, it) {
  var pa = parent.pathItems.add(), pts = [];
  for (var i = 0; i < it.pts.length; i++) pts.push([X(p, it.pts[i][0]), Y(it.pts[i][1])]);
  pa.setEntirePath(pts); pa.closed = true; pa.filled = false; pa.stroked = true;
  var c = new RGBColor(); c.red = 236; c.green = 0; c.blue = 140; pa.strokeColor = c; pa.strokeWidth = 0.5; pa.name = it.name;
  return pa;
}
// ---------- tree ----------
function build(parent, p, items) {
  for (var i = 0; i < items.length; i++) {
    var it = items[i], o = null;
    try {
      if (it.k == 'r') o = rect(parent, p, it);
      else if (it.k == 'img' || it.k == 'ras' || it.k == 'svg') o = place(parent, p, it);
      else if (it.k == 't') o = text(parent, p, it);
      else if (it.k == 'g') o = group(parent, p, it);
      else if (it.k == 'poly') o = poly(parent, p, it);
    } catch (e) { LOG.push('item ' + it.k + ' ' + (it.name || '') + ': ' + e + ' line ' + e.line); }
    if (o) o.move(parent, ElementPlacement.PLACEATBEGINNING);
  }
}
function group(parent, p, it) {
  var g = parent.groupItems.add(); g.name = it.name || 'Grupo';
  build(g, p, it.ch);
  if (g.pageItems.length == 0) { g.remove(); return null; }
  if (it.clip) {
    var cp = pathRR(g, p, it.clip.x, it.clip.y, it.clip.w, it.clip.h, it.clip.rad);
    cp.move(g, ElementPlacement.PLACEATBEGINNING); cp.name = 'Recorte'; cp.clipping = true; g.clipped = true;
  }
  if (it.xf && (it.xf.flip || Math.abs(it.xf.ang) > 0.01 || Math.abs(it.xf.tx) > 0.01 || Math.abs(it.xf.ty) > 0.01)) {
    // rotate about (ox,oy) then translate: use a marker to resolve the pivot
    var m = g.pathItems.rectangle(Y(it.xf.oy), X(p, it.xf.ox), 0.01, 0.01); m.filled = false; m.stroked = false;
    var before = [X(p, it.xf.ox), Y(it.xf.oy)];
    if (it.xf.flip) g.resize(-100, 100, true, true, true, true, 100, Transformation.CENTER);
    if (Math.abs(it.xf.ang) > 0.01) g.rotate(-it.xf.ang, true, true, true, true, Transformation.CENTER);
    var after = m.position;
    g.translate(before[0] - after[0] + it.xf.tx * S, before[1] - after[1] - it.xf.ty * S);
    m.remove();
  }
  if (it.op < 0.999) g.opacity = it.op * 100;
  if (it.ds) fxShadow(g, it.ds.x * S, it.ds.y * S, it.ds.blur * S * 0.5, it.ds.c[3]);
  if (g.pageItems.length == 1 && !it.xf && it.op >= 0.999 && !it.ds && !it.clip) { var only = g.pageItems[0]; only.move(parent, ElementPlacement.PLACEATBEGINNING); g.remove(); return only; }
  return g;
}

try {
makeDoc();
var baseLayer = doc.layers[0];
for (var pi = DOC.pages.length - 1; pi >= 0; pi--) {
  var pg = DOC.pages[pi];
  var lay = pi == DOC.pages.length - 1 ? baseLayer : doc.layers.add();
  lay.name = pg.name;
  build(lay, pi, pg.items);
  if (pg.troquel) { var tl = doc.layers.add(); tl.name = 'Troquel (línea de corte · no imprimir)'; build(tl, pi, pg.troquel); tl.printable = false; }
}
// build() moves each new item to the top, so later DOM items end on top (same paint order as the browser)
var so = new IllustratorSaveOptions(); so.pdfCompatible = true; so.embedICCProfile = true; so.compressed = true;
doc.saveAs(new File(DOC.out), so);
if (DOC.png) {
  for (var a = 0; a < doc.artboards.length; a++) {
    doc.artboards.setActiveArtboardIndex(a);
    var o = new ExportOptionsPNG24(); o.artBoardClipping = true; o.antiAliasing = true; o.transparency = false;
    o.horizontalScale = o.verticalScale = DOC.pngScale || 100;
    doc.exportFile(new File(DOC.png + '/' + DOC.base + '_' + (a + 1) + '.png'), ExportType.PNG24, o);
  }
}
if (!DOC.keepOpen) doc.close(SaveOptions.DONOTSAVECHANGES);
} catch (e) { try { doc.close(SaveOptions.DONOTSAVECHANGES); } catch (e2) { } LOG.push('FATAL ' + e + ' line ' + e.line); }
LOG.join('\n') || 'ok';
