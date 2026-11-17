// =========================================================
// QUITO 3D — el banquito, modelado y animado en Three.js
// Estética cartoon años 30: sombreado toon en 3 tonos + contorno tinta (casco invertido),
// brazos y piernas "de manguera" que se recalculan cada cuadro.
// =========================================================
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

const COL = {
  wood: '#ec8a2c', woodL: '#f7a748', woodD: '#c8641a', ink: '#3a1d0c', engrave: '#b5560f',
  hose: '#8a4719', glove: '#f8edd6', shoe: '#9a5626', cream: '#f5e3c1', white: '#fffaf0',
  bag: '#ecc78f', bagD: '#d9a865', pupil: '#1d0e06',
};
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const lerp = (a, b, t) => a + (b - a) * t;
const damp = (a, b, k, dt) => lerp(a, b, 1 - Math.exp(-k * dt));

// ---------- materiales ----------
function toonRamp() {
  const t = new THREE.DataTexture(new Uint8Array([105, 175, 255]), 3, 1, THREE.RedFormat);
  t.minFilter = t.magFilter = THREE.NearestFilter; t.needsUpdate = true; return t;
}
const RAMP = toonRamp();
const toon = (color, extra = {}) => new THREE.MeshToonMaterial({ color, gradientMap: RAMP, ...extra });
const OUTLINE = new THREE.ShaderMaterial({
  uniforms: { color: { value: new THREE.Color(COL.ink) }, thickness: { value: 0.03 } },
  vertexShader: 'uniform float thickness; void main(){ vec3 p = position + normal * thickness; gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0); }',
  fragmentShader: 'uniform vec3 color; void main(){ gl_FragColor = vec4(color, 1.0); }',
  side: THREE.BackSide,
});
const OUTLINE_THIN = OUTLINE.clone(); OUTLINE_THIN.uniforms = { color: { value: new THREE.Color(COL.ink) }, thickness: { value: 0.018 } };

function outlined(geo, mat, thin = false) {
  const m = new THREE.Mesh(geo, mat);
  const o = new THREE.Mesh(geo, thin ? OUTLINE_THIN : OUTLINE);
  o.name = 'outline'; m.add(o); m.userData.outline = o;
  return m;
}

// ---------- texturas pintadas ----------
function woodTexture(seed, w = 1024, h = 192) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d');
  let s = seed; const r = () => ((s = (s * 16807) % 2147483647) / 2147483647);
  g.fillStyle = COL.wood; g.fillRect(0, 0, w, h);
  const grd = g.createLinearGradient(0, 0, 0, h); grd.addColorStop(0, 'rgba(255,214,140,.55)'); grd.addColorStop(.35, 'rgba(255,200,120,0)'); grd.addColorStop(1, 'rgba(150,60,10,.22)');
  g.fillStyle = grd; g.fillRect(0, 0, w, h);
  g.lineCap = 'round';
  for (let i = 0; i < 9; i++) {
    const y0 = 18 + r() * (h - 36), amp = 3 + r() * 7, f = .004 + r() * .01, ph = r() * 6;
    g.strokeStyle = `rgba(150,62,10,${.18 + r() * .25})`; g.lineWidth = 2 + r() * 3.5;
    g.beginPath();
    for (let x = -10; x <= w + 10; x += 12) { const y = y0 + Math.sin(x * f + ph) * amp; x < 0 ? g.moveTo(x, y) : g.lineTo(x, y); }
    g.stroke();
  }
  for (let k = 0; k < 2; k++) { // nudos
    const x = 120 + r() * (w - 240), y = 40 + r() * (h - 80);
    g.strokeStyle = 'rgba(140,55,10,.35)'; g.lineWidth = 3;
    for (let j = 0; j < 3; j++) { g.beginPath(); g.ellipse(x, y, 16 + j * 12, 6 + j * 5, 0, 0, Math.PI * 2); g.stroke(); }
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}

// ---------- cara: grabados, boca, rubor (se redibuja al cambiar de emoción) ----------
const FW = 2.0, FH = 1.52, PX = 512; // unidades de la cara y px por unidad
function faceCanvas() {
  const c = document.createElement('canvas'); c.width = FW * PX; c.height = Math.round(FH * PX); return c;
}
function drawFace(c, expr) {
  const g = c.getContext('2d'); g.clearRect(0, 0, c.width, c.height);
  const X = (x) => (x + FW / 2) * PX, Y = (y) => (FH - y) * PX;
  g.lineCap = 'round'; g.lineJoin = 'round';
  // grabados en la madera
  g.strokeStyle = COL.engrave; g.lineWidth = 11; g.globalAlpha = .95;
  // corazón
  g.save(); g.translate(X(-.78), Y(1.0)); g.scale(1.35, 1.35); g.beginPath();
  g.moveTo(0, 26); g.bezierCurveTo(-46, -4, -30, -40, 0, -18); g.bezierCurveTo(30, -40, 46, -4, 0, 26); g.stroke(); g.restore();
  // caritas
  const smiley = (x, y) => { g.save(); g.translate(X(x), Y(y)); g.scale(1.4, 1.4); g.beginPath(); g.arc(-14, -8, 3.5, 0, 7); g.arc(14, -8, 3.5, 0, 7); g.fillStyle = COL.engrave; g.fill();
    g.beginPath(); g.arc(0, 2, 20, .25, Math.PI - .25); g.stroke(); g.restore(); };
  smiley(-.8, .42); smiley(.82, .5);
  // hoja
  g.save(); g.translate(X(.74), Y(1.36)); g.rotate(-.5); g.scale(1.3, 1.3); g.beginPath();
  g.moveTo(-40, 0); g.quadraticCurveTo(0, -30, 40, 0); g.quadraticCurveTo(0, 30, -40, 0); g.moveTo(-48, 0); g.lineTo(36, 0);
  for (const k of [-18, 0, 18]) { g.moveTo(k, 0); g.lineTo(k + 12, -14); g.moveTo(k, 0); g.lineTo(k + 12, 14); }
  g.stroke(); g.restore();
  g.globalAlpha = 1;

  // rubor
  const blush = expr === 'enojado' ? 'rgba(226,64,40,.55)' : 'rgba(244,110,90,.42)';
  if (expr !== 'triste') for (const sx of [-1, 1]) {
    g.save(); g.translate(X(sx * .64), Y(.66));
    if (expr === 'avergonzado' || expr === 'enojado') { g.fillStyle = blush; g.beginPath(); g.ellipse(0, 6, 62, 30, 0, 0, 7); g.fill(); }
    g.strokeStyle = COL.ink; g.lineWidth = 7; g.globalAlpha = .85;
    for (const k of [-22, 0, 22]) { g.beginPath(); g.moveTo(k - 7, 12); g.lineTo(k + 7, -12); g.stroke(); }
    g.restore();
  }
  g.globalAlpha = 1;

  // boca
  const mx = X(0), my = Y(.44);
  g.save(); g.translate(mx, my); g.scale(1.3, 1.3);
  g.strokeStyle = COL.ink; g.lineWidth = 13; g.fillStyle = '#7a210f';
  const tongue = (cx, cy, rx, ry) => { g.save(); g.clip(); g.fillStyle = '#f2785a'; g.beginPath(); g.ellipse(cx, cy, rx, ry, 0, 0, 7); g.fill(); g.restore(); };
  if (expr === 'feliz' || expr === 'guino' || expr === 'euforico') {
    const w = expr === 'euforico' ? 175 : 150, d = expr === 'euforico' ? 175 : 140;
    g.beginPath(); g.moveTo(-w, -34); g.quadraticCurveTo(0, -8, w, -34); g.bezierCurveTo(w - 8, d * .75, -w + 8, d * .75, -w, -34); g.closePath();
    g.fill(); tongue(10, d * .55, w * .5, d * .32); g.stroke();
    // comisuras
    g.beginPath(); g.moveTo(-w - 18, -52); g.quadraticCurveTo(-w - 4, -36, -w + 2, -24); g.moveTo(w + 18, -52); g.quadraticCurveTo(w + 4, -36, w - 2, -24); g.stroke();
  } else if (expr === 'enojado') {
    g.beginPath(); g.moveTo(-120, 30); g.quadraticCurveTo(0, -40, 120, 30); g.quadraticCurveTo(0, 90, -120, 30); g.closePath(); g.fill();
    g.save(); g.clip(); g.fillStyle = '#fffaf0'; g.fillRect(-140, -50, 280, 52); g.restore(); g.stroke();
  } else if (expr === 'triste') {
    g.beginPath(); g.moveTo(-90, 46); g.quadraticCurveTo(0, -36, 90, 46); g.stroke();
    g.lineWidth = 9; g.beginPath(); g.moveTo(-100, 40); g.lineTo(-86, 56); g.moveTo(100, 40); g.lineTo(86, 56); g.stroke();
  } else if (expr === 'avergonzado') {
    g.beginPath(); g.moveTo(-70, 10);
    for (let i = 0; i <= 8; i++) g.lineTo(-70 + i * 17.5, 10 + (i % 2 ? -12 : 10));
    g.stroke();
  } else if (expr === 'sorprendido') {
    g.beginPath(); g.ellipse(0, 20, 54, 70, 0, 0, 7); g.fill(); tongue(0, 74, 34, 26); g.stroke();
  }
  g.restore();

  // extras
  if (expr === 'triste') { // lágrima
    g.save(); g.translate(X(-.42), Y(.5)); g.fillStyle = '#7fd0ff'; g.strokeStyle = COL.ink; g.lineWidth = 7;
    g.beginPath(); g.moveTo(0, -40); g.bezierCurveTo(28, 0, 26, 30, 0, 32); g.bezierCurveTo(-26, 30, -28, 0, 0, -40); g.fill(); g.stroke(); g.restore();
  }
  if (expr === 'avergonzado') { // gota de sudor
    g.save(); g.translate(X(.9), Y(1.22)); g.rotate(.3); g.fillStyle = '#9fe0ff'; g.strokeStyle = COL.ink; g.lineWidth = 7;
    g.beginPath(); g.moveTo(0, -46); g.bezierCurveTo(32, 0, 30, 34, 0, 36); g.bezierCurveTo(-30, 34, -32, 0, 0, -46); g.fill(); g.stroke(); g.restore();
  }
  if (expr === 'enojado') { // venita
    g.save(); g.translate(X(-.82), Y(1.34)); g.strokeStyle = '#e2402a'; g.lineWidth = 11;
    for (const a of [0, 1, 2, 3]) { g.save(); g.rotate(a * Math.PI / 2); g.beginPath(); g.moveTo(10, -26); g.quadraticCurveTo(12, -10, 26, -10); g.stroke(); g.restore(); }
    g.restore();
  }
}

// ---------- expresiones ----------
// browA: inclinación de cejas (+ = enojado, punta interna abajo), browY: altura, eye: apertura, pupil: tamaño, look: mirada forzada
const EXPR = {
  feliz: { browA: -.08, browY: .04, eye: 1, pupil: 1 },
  euforico: { browA: -.15, browY: .1, eye: 1.05, pupil: .95 },
  guino: { browA: -.1, browY: .05, eye: 1, pupil: 1, wink: 1 },
  enojado: { browA: .5, browY: -.1, eye: .74, pupil: .82 },
  triste: { browA: -.42, browY: .02, eye: .92, pupil: 1.1, look: [0, -.75] },
  avergonzado: { browA: -.3, browY: -.02, eye: .9, pupil: .95, look: [.85, -.35] },
  sorprendido: { browA: -.05, browY: .17, eye: 1.1, pupil: .86 },
};
export const EXPRESSIONS = Object.keys(EXPR);

// ---------- poses de manos (espacio del cuerpo; x<0 = izquierda de pantalla) ----------
const POSES = {
  idle: { L: [-1.2, 1.52, .25], R: [1.2, 1.52, .25], hL: 'open', hR: 'open' },
  wave: { L: [-1.62, 2.85, .35], R: [1.2, 1.62, .3], hL: 'open', hR: 'open', waveL: 1 },
  thumbs: { L: [-1.05, 2.05, .95], R: [1.2, 1.62, .3], hL: 'thumb', hR: 'open' },
  point: { L: [-2.05, 2.15, .55], R: [1.18, 1.3, .25], hL: 'point', hR: 'fist' },
  pointR: { L: [-1.2, 1.62, .3], R: [2.05, 2.15, .55], hL: 'open', hR: 'point' },
  cheer: { L: [-1.55, 3.05, .25], R: [1.55, 3.05, .25], hL: 'open', hR: 'open' },
  hips: { L: [-1.32, 1.28, .05], R: [1.32, 1.28, .05], hL: 'fist', hR: 'fist' },
  shy: { L: [-.42, 1.85, .82], R: [.42, 1.85, .82], hL: 'open', hR: 'open' },
};
export const POSE_NAMES = Object.keys(POSES);
const HAND_CURL = { open: [0, 0, 0, 0], fist: [1, 1, 1, .6], point: [0, 1, 1, .7], thumb: [1, 1, 1, -.4] };

// =========================================================
export async function initQuito(canvas, { onProgress } = {}) {
  onProgress?.(.1);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(26, 1, .1, 100);
  const CAM_Z = 14; camera.position.set(0, 1.6, CAM_Z); camera.lookAt(0, 0, 0);

  scene.add(new THREE.HemisphereLight(0xfff1dc, 0x6f86b8, 1.05));
  const key = new THREE.DirectionalLight(0xfff4e2, 2.5); key.position.set(-4, 6, 7); scene.add(key);
  const rim = new THREE.DirectionalLight(0xbfe9ff, 1.25); rim.position.set(5, 3, -6); scene.add(rim);

  // jerarquía
  const rig = new THREE.Group(); scene.add(rig);           // ubicación por scroll
  const quito = new THREE.Group(); quito.position.y = -1.55; rig.add(quito); // giro y personaje
  const torso = new THREE.Group(); quito.add(torso);        // rebote
  const head = new THREE.Group(); head.position.set(0, 1.22, -.32); torso.add(head); // respaldo = cabeza

  const matWood = (seed) => toon(0xffffff, { map: woodTexture(seed) });
  const matWoodPlain = toon(COL.wood), matWoodL = toon(COL.woodL), matWoodD = toon(COL.woodD);

  // --- respaldo: 4 tablas ---
  const slatY = [.2, .575, .95, 1.335], slatH = [.34, .34, .34, .38];
  slatY.forEach((y, i) => {
    const m = outlined(new RoundedBoxGeometry(i === 3 ? 2.1 : 2.0, slatH[i], .17, 4, .07), [matWoodPlain, matWoodPlain, matWoodL, matWoodD, matWood(11 + i * 7), matWoodPlain]);
    m.position.set(0, y, 0); m.rotation.z = (i % 2 ? .012 : -.01); head.add(m);
  });
  for (const sx of [-1, 1]) { // parantes traseros
    const p = outlined(new RoundedBoxGeometry(.17, 1.55, .15, 3, .05), matWoodD); p.position.set(sx * .8, .62, -.15); head.add(p);
  }
  // cara pintada
  const fc = faceCanvas(); const faceTex = new THREE.CanvasTexture(fc); faceTex.colorSpace = THREE.SRGBColorSpace; faceTex.anisotropy = 8;
  const face = new THREE.Mesh(new THREE.PlaneGeometry(FW, FH), new THREE.MeshBasicMaterial({ map: faceTex, transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2 }));
  face.position.set(0, FH / 2, .087); head.add(face);

  // ojos
  const eyeGeo = new THREE.SphereGeometry(1, 40, 28); eyeGeo.scale(.27, .36, .11);
  const pupilGeo = new THREE.SphereGeometry(1, 28, 20); pupilGeo.scale(.12, .175, .05);
  const eyes = [-1, 1].map((sx) => {
    const g = new THREE.Group(); g.position.set(sx * .36, .99, .1); head.add(g);
    const white = outlined(eyeGeo, new THREE.MeshBasicMaterial({ color: COL.white })); g.add(white);
    const pupil = new THREE.Mesh(pupilGeo, new THREE.MeshBasicMaterial({ color: COL.pupil })); g.add(pupil);
    const hl = new THREE.Mesh(new THREE.SphereGeometry(.036, 12, 10), new THREE.MeshBasicMaterial({ color: 0xffffff })); hl.position.set(.045, .07, .04); pupil.add(hl);
    const hl2 = new THREE.Mesh(new THREE.SphereGeometry(.018, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffffff })); hl2.position.set(-.03, -.05, .04); pupil.add(hl2);
    return { g, white, pupil, sx, open: 1, pscale: 1 };
  });
  // cejas
  const browCurve = new THREE.QuadraticBezierCurve3(V(-.2, -.02, 0), V(0, .12, 0), V(.2, -.02, 0));
  const browGeo = new THREE.TubeGeometry(browCurve, 20, .052, 10, false);
  const brows = [-1, 1].map((sx) => {
    const g = new THREE.Group(); g.position.set(sx * .37, 1.62, .03); head.add(g);
    const m = new THREE.Mesh(browGeo, new THREE.MeshBasicMaterial({ color: COL.ink })); g.add(m);
    for (const e of [-1, 1]) { const cap = new THREE.Mesh(new THREE.SphereGeometry(.052, 10, 8), m.material); cap.position.set(e * .2, -.02, 0); g.add(cap); }
    return { g, sx };
  });

  // --- asiento ---
  [.4, .14, -.12].forEach((z, i) => {
    const m = outlined(new RoundedBoxGeometry(2.2, .13, .25, 3, .05), [matWoodPlain, matWoodPlain, matWoodL, matWoodD, matWood(51 + i), matWoodPlain]);
    m.position.set(0, 1.12, z); torso.add(m);
  });
  for (const sx of [-1, 1]) {
    const rail = outlined(new RoundedBoxGeometry(.14, .14, .8, 3, .05), matWoodD); rail.position.set(sx * .98, .99, .12); torso.add(rail);
    for (const z of [.44, -.22]) { const leg = outlined(new RoundedBoxGeometry(.14, .42, .14, 3, .05), matWoodPlain); leg.position.set(sx * .98, .8, z); torso.add(leg); }
    // apoyabrazos curvo
    const arc = new THREE.CatmullRomCurve3([V(sx * 1.06, 1.1, -.32), V(sx * 1.1, 1.42, -.22), V(sx * 1.12, 1.5, .1), V(sx * 1.1, 1.4, .42), V(sx * 1.06, 1.1, .52)]);
    const ar = outlined(new THREE.TubeGeometry(arc, 40, .075, 10, false), matWoodL); torso.add(ar);
  }

  // --- extremidades de manguera ---
  const matHose = toon(COL.hose);
  const limbs = {};
  for (const k of ['armL', 'armR', 'legL', 'legR']) {
    const m = outlined(new THREE.BufferGeometry(), matHose); quito.add(m); limbs[k] = m;
  }
  const strap = outlined(new THREE.BufferGeometry(), toon(COL.bagD), true); quito.add(strap);
  const shoulderCaps = [-1, 1].map(() => { const s = outlined(new THREE.SphereGeometry(.085, 14, 10), matHose); quito.add(s); return s; });

  // guantes
  const matGlove = toon(COL.glove);
  function makeGlove(side) { // side: -1 izquierda de pantalla, 1 derecha
    const g = new THREE.Group(); quito.add(g);
    const cuff = outlined(new THREE.CylinderGeometry(.12, .1, .1, 18), matGlove); cuff.position.y = .03; g.add(cuff);
    const palm = outlined(new THREE.SphereGeometry(1, 20, 16).scale(.155, .16, .085), matGlove); palm.position.y = .2; g.add(palm);
    const fingers = [];
    [-.075, 0, .075].forEach((x, i) => {
      const piv = new THREE.Group(); piv.position.set(x * -side, .31, 0); g.add(piv);
      const f = outlined(new THREE.CapsuleGeometry(.045, .12, 6, 10), matGlove, true); f.position.y = .08; piv.add(f);
      piv.rotation.z = (i - 1) * .14 * side; fingers.push(piv);
    });
    const tp = new THREE.Group(); tp.position.set(.12 * -side, .17, .02); g.add(tp);
    const th = outlined(new THREE.CapsuleGeometry(.045, .1, 6, 10), matGlove, true); th.position.y = .07; tp.add(th);
    tp.rotation.z = -1.0 * -side;
    return { g, fingers, thumb: tp, side, curl: [0, 0, 0, 0] };
  }
  const gloves = { L: makeGlove(-1), R: makeGlove(1) };

  // zapatillas
  function makeShoe() {
    const g = new THREE.Group(); quito.add(g);
    const sock = outlined(new THREE.CylinderGeometry(.1, .11, .1, 16), toon(COL.cream)); sock.position.y = .27; g.add(sock);
    const up = outlined(new THREE.SphereGeometry(1, 24, 18).scale(.23, .18, .33), toon(COL.shoe)); up.position.set(0, .17, .0); g.add(up);
    const toe = outlined(new THREE.SphereGeometry(1, 24, 18).scale(.22, .15, .19), toon(COL.cream)); toe.position.set(0, .13, .24); g.add(toe);
    const sole = outlined(new RoundedBoxGeometry(.5, .1, .76, 4, .045), toon(COL.cream)); sole.position.set(0, .05, .06); g.add(sole);
    for (const z of [-.05, .04]) { const l = new THREE.Mesh(new THREE.CapsuleGeometry(.018, .14, 4, 8), new THREE.MeshBasicMaterial({ color: COL.white })); l.rotation.z = Math.PI / 2; l.position.set(0, .33, z); l.rotation.x = .5; g.add(l); }
    return g;
  }
  const shoes = { L: makeShoe(), R: makeShoe() };

  // morral
  const bag = new THREE.Group(); quito.add(bag);
  const bagBody = outlined(new RoundedBoxGeometry(.52, .46, .2, 4, .07), toon(COL.bag)); bagBody.position.y = -.26; bag.add(bagBody);
  const flap = outlined(new RoundedBoxGeometry(.54, .22, .22, 4, .07), toon(COL.bagD)); flap.position.set(0, -.12, .01); bag.add(flap);
  { // reciclaje
    const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
    g.strokeStyle = '#a8742f'; g.lineWidth = 16; g.lineCap = 'round'; g.lineJoin = 'round'; g.translate(128, 136);
    for (let i = 0; i < 3; i++) { g.save(); g.rotate(i * Math.PI * 2 / 3); g.beginPath(); g.moveTo(-50, 40); g.lineTo(-6, -40); g.stroke();
      g.beginPath(); g.moveTo(-26, -40); g.lineTo(-4, -46); g.lineTo(2, -24); g.stroke(); g.restore(); }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.3, .3), new THREE.MeshBasicMaterial({ map: t, transparent: true })); p.position.set(0, -.33, .102); bag.add(p);
  }

  // sombra de contacto
  const shCan = document.createElement('canvas'); shCan.width = shCan.height = 128;
  { const g = shCan.getContext('2d'); const gr = g.createRadialGradient(64, 64, 4, 64, 64, 62); gr.addColorStop(0, 'rgba(20,20,50,.55)'); gr.addColorStop(.6, 'rgba(20,20,50,.22)'); gr.addColorStop(1, 'rgba(20,20,50,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); }
  const shadow = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 1.6), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(shCan), transparent: true, depthWrite: false }));
  shadow.rotation.x = -Math.PI / 2; shadow.position.y = .005; quito.add(shadow);

  // zona de clic
  const hit = new THREE.Mesh(new THREE.BoxGeometry(2.6, 3.4, 1.4), new THREE.MeshBasicMaterial({ visible: false })); hit.position.set(0, 1.6, 0); quito.add(hit);

  onProgress?.(.7);

  // =========================================================
  // estado
  const st = {
    // placement (NDC) — controlado desde afuera, suavizado acá
    x: 0, y: 0, s: .72, ry: 0, tx: 0, ty: 0, ts: .72, tRy: 0,
    expr: 'feliz', exprShown: '', pose: 'idle', basePose: 'idle', baseExpr: 'feliz',
    look: V(), lookT: V(), pointer: { x: 0, y: 0, active: false },
    jump: 0, jumpV: 0, squash: 0, spin: 0, spinV: 0, drag: null,
    walk: 0, phase: 0, intro: 0, introDone: false, hover: 0,
    hands: { L: V(-1.2, 1.62, .3), R: V(1.2, 1.62, .3) },
    bagAng: 0, bagV: 0, blinkT: 2, blink: 0, t: 0, prevX: 0,
    reacting: 0, visible: true,
  };
  drawFace(fc, 'feliz'); faceTex.needsUpdate = true;

  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  function hitTest(cx, cy) {
    const r = canvas.getBoundingClientRect();
    ndc.set(((cx - r.left) / r.width) * 2 - 1, -((cy - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera); return st.visible && ray.intersectObject(hit).length > 0;
  }

  // ---------- tamaño ----------
  let W = 1, H = 1, halfH = 1, halfW = 1;
  function resize() {
    W = canvas.clientWidth || innerWidth; H = canvas.clientHeight || innerHeight;
    renderer.setSize(W, H, false); camera.aspect = W / H; camera.updateProjectionMatrix();
    halfH = CAM_Z * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)); halfW = halfH * camera.aspect;
  }
  resize(); addEventListener('resize', resize);

  // ---------- helpers de geometría ----------
  const tmp = V(), tmp2 = V();
  const toQ = (obj, x, y, z, out = V()) => { out.set(x, y, z); obj.localToWorld(out); return quito.worldToLocal(out); };
  function hose(mesh, pts, r) {
    const curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal');
    const geo = new THREE.TubeGeometry(curve, 28, r, 9, false);
    mesh.geometry.dispose(); mesh.geometry = geo; mesh.userData.outline.geometry = geo;
    return curve;
  }
  const qa = new THREE.Quaternion(), mtx = new THREE.Matrix4();
  function orient(obj, dir, faceZ = V(0, 0, 1)) {
    const y = dir.clone().normalize();
    const z = faceZ.clone().sub(y.clone().multiplyScalar(faceZ.dot(y))).normalize();
    const x = new THREE.Vector3().crossVectors(y, z).normalize();
    mtx.makeBasis(x, y, z); obj.quaternion.setFromRotationMatrix(mtx);
  }

  function setExpression(name) { if (EXPR[name]) st.expr = name; }

  // ---------- animación ----------
  const clock = new THREE.Clock();
  function update() {
    const dt = Math.max(1e-3, Math.min(clock.getDelta(), 1 / 20)); st.t += dt; const t = st.t;
    // ubicación suave
    st.x = damp(st.x, st.tx, 4.5, dt); st.y = damp(st.y, st.ty, 4.5, dt); st.s = damp(st.s, st.ts, 4.5, dt); st.ry = damp(st.ry, st.tRy, 4, dt);
    const mob = W < 760;
    const unit = (Math.min(2 * halfH, 2 * halfW * (mob ? 1.15 : .9))) / 3.3;
    rig.position.set(st.x * halfW, st.y * halfH, 0);
    rig.scale.setScalar(Math.max(st.s, .0001) * unit);
    st.visible = st.s > .02 && st.y > -1.5 && st.y < 1.5 && Math.abs(st.x) < 1.6;
    // velocidad horizontal → camina
    const vx = (st.x - st.prevX) / dt; st.prevX = st.x;
    st.walk = damp(st.walk, clamp(Math.abs(vx) * 1.6 + Math.abs(st.ty - st.y) * 1.5, 0, 1), 6, dt);

    // intro: cae desde arriba
    if (!st.introDone) { st.intro = Math.min(1, st.intro + dt / 1.1); }
    const ip = st.intro;
    const dropY = ip < .55 ? (1 - (ip / .55) ** 2) * 6 : 0;

    // mirada
    const sx = st.x, sy = st.y + .1;
    const lx = st.pointer.active ? clamp((st.pointer.x - sx) * 1.3, -1, 1) : Math.sin(t * .5) * .3;
    const ly = st.pointer.active ? clamp((st.pointer.y - sy) * 1.3, -1, 1) : Math.sin(t * .37) * .15;
    const E = EXPR[st.expr];
    st.lookT.set(E.look ? E.look[0] : lx, E.look ? E.look[1] : ly, 0);
    st.look.x = damp(st.look.x, st.lookT.x, 9, dt); st.look.y = damp(st.look.y, st.lookT.y, 9, dt);

    // giro por arrastre con inercia
    if (!st.drag) { st.spinV *= Math.exp(-2.2 * dt); st.spin += st.spinV * dt; st.spin = damp(st.spin, Math.round(st.spin / (Math.PI * 2)) * Math.PI * 2, Math.abs(st.spinV) < .5 ? 2.5 : 0, dt); }
    quito.rotation.y = st.ry + st.spin + st.look.x * .22;
    quito.rotation.x = -st.look.y * .06;

    // salto (reacción al clic)
    st.jumpV -= 22 * dt; st.jump = Math.max(0, st.jump + st.jumpV * dt); if (st.jump === 0 && st.jumpV < 0) { if (st.jumpV < -3) st.squash = .22; st.jumpV = 0; }
    st.squash = damp(st.squash, 0, 7, dt);
    const airborne = st.jump > .01;

    // rebote de manguera (a 1.6 tiempos por segundo)
    const beat = Math.abs(Math.sin(t * Math.PI * 1.55));
    const bounce = (airborne ? 0 : beat * .07) * (1 - st.walk * .4);
    const lift = st.jump + dropY + bounce;
    torso.position.y = lift - st.squash * .4;
    const sq = 1 - st.squash + (airborne ? .06 : 0) - (1 - beat) * .015;
    torso.scale.set(1 + (1 - sq) * .7, sq, 1 + (1 - sq) * .7);
    torso.rotation.z = Math.sin(t * Math.PI * .78) * .03 + (st.walk * Math.sin(st.phase) * .05);
    head.rotation.y = st.look.x * .32;
    head.rotation.x = -.1 - st.look.y * .14 + (st.expr === 'triste' ? .1 : 0);
    head.rotation.z = Math.sin(t * Math.PI * .78 + 1) * .035 + (st.expr === 'avergonzado' ? -.08 : 0);

    // cara: redibujar si cambió la emoción
    if (st.exprShown !== st.expr) { drawFace(fc, st.expr); faceTex.needsUpdate = true; st.exprShown = st.expr; }
    // parpadeo
    st.blinkT -= dt; if (st.blinkT <= 0) { st.blink = 1; st.blinkT = 1.8 + Math.random() * 3.2; if (Math.random() < .2) st.blinkT = .25; }
    st.blink = Math.max(0, st.blink - dt * 7);
    const blinkK = st.blink > 0 ? 1 - Math.sin(st.blink * Math.PI) * .92 : 1;
    eyes.forEach((e) => {
      const wink = E.wink && e.sx > 0 ? .1 : 1;
      e.open = damp(e.open, E.eye * (1 + st.hover * .06) * wink, 14, dt);
      e.pscale = damp(e.pscale, E.pupil * (1 + st.hover * .12), 10, dt);
      e.g.scale.set(1, e.open * blinkK, 1);
      const px = st.look.x * .12, py = st.look.y * .14;
      const zz = Math.sqrt(Math.max(.05, 1 - (px / .27) ** 2 - (py / .36) ** 2));
      e.pupil.position.set(px, py, .11 * zz - .035);
      e.pupil.scale.setScalar(e.pscale);
      e.pupil.visible = wink > .5;
    });
    brows.forEach((b) => {
      b.g.rotation.z = damp(b.g.rotation.z, -b.sx * E.browA, 10, dt);
      b.g.position.y = damp(b.g.position.y, 1.62 + E.browY + st.hover * .05 + (st.jumpV > 2 ? .06 : 0), 10, dt);
    });

    // ---- piernas ----
    st.phase += dt * (6 + st.walk * 4) * (st.walk > .05 ? 1 : 0);
    torso.updateMatrix(); head.updateMatrix(); quito.updateMatrixWorld(true);
    for (const [k, sxx] of [['L', -1], ['R', 1]]) {
      const ph = st.phase + (sxx > 0 ? Math.PI : 0);
      const w = st.walk;
      const foot = V(sxx * .44, 0, .32 + Math.sin(ph) * .42 * w);
      foot.y = Math.max(0, Math.cos(ph)) * .26 * w + (airborne ? st.jump * .85 + dropY : dropY);
      if (airborne) foot.z += .12;
      const hip = toQ(torso, sxx * .33, 1.0, .18);
      const ankle = foot.clone().add(V(0, .3, -.06));
      const mid = hip.clone().lerp(ankle, .5); mid.z += .22 + w * .1 - (hip.y - ankle.y - .8) * .4; mid.x += sxx * .06;
      hose(limbs['leg' + k], [hip.clone().add(V(0, .12, 0)), hip, mid, ankle], .088);
      const sh = shoes[k]; sh.position.copy(foot); sh.rotation.set((airborne ? .35 : 0) + Math.sin(ph) * .3 * w, sxx * .12, 0);
    }
    // sombra
    const shadowK = 1 / (1 + lift * .7);
    shadow.scale.set(shadowK, shadowK, 1); shadow.material.opacity = shadowK * (st.intro < .4 ? st.intro / .4 : 1);

    // ---- brazos ----
    const P = POSES[st.pose] || POSES.idle;
    for (const [k, sxx] of [['L', -1], ['R', 1]]) {
      const tgt = V(...P[k]);
      if (airborne || st.reacting > 0) tgt.set(sxx * 1.55, 3.0, .25); // brazos arriba al saltar
      else if (P['wave' + k]) { tgt.x += Math.sin(t * 9) * .2; tgt.y += Math.cos(t * 9) * .05; }
      else if (st.pose === 'idle') { tgt.y += Math.sin(t * Math.PI * 1.55 + (sxx > 0 ? 1 : 0)) * .03; }
      tgt.y += torso.position.y;
      st.hands[k].x = damp(st.hands[k].x, tgt.x, 9, dt); st.hands[k].y = damp(st.hands[k].y, tgt.y, 9, dt); st.hands[k].z = damp(st.hands[k].z, tgt.z, 9, dt);
      const hand = st.hands[k];
      const sh = toQ(head, sxx * 1.0, .62, -.02);
      shoulderCaps[sxx < 0 ? 0 : 1].position.copy(sh);
      const mid = sh.clone().lerp(hand, .5); mid.x += sxx * .32; mid.y -= .12 + Math.max(0, sh.y - hand.y) * .0; mid.z += .1;
      const curve = hose(limbs['arm' + k], [sh.clone().add(V(-sxx * .1, 0, 0)), sh, mid, hand], .068);
      const gl = gloves[k]; gl.g.position.copy(hand);
      const dir = curve.getTangent(1);
      if (P['wave' + k] && !airborne) dir.set(Math.sin(t * 9) * .35 + sxx * .15, 1, 0);
      orient(gl.g, dir, V(0, 0, 1));
      const curl = HAND_CURL[(airborne ? 'open' : P['h' + k])] || HAND_CURL.open;
      gl.fingers.forEach((f, i) => { const c = curl[i] ?? 0; f.rotation.x = damp(f.rotation.x, -c * 1.9, 12, dt); });
      gl.thumb.rotation.x = damp(gl.thumb.rotation.x, -(curl[3] > 0 ? curl[3] : 0) * 1.4, 12, dt);
      gl.thumb.rotation.z = damp(gl.thumb.rotation.z, curl[3] < 0 ? 0 : -1.0 * -gl.side, 12, dt);
    }

    // ---- morral (péndulo) ----
    const anchor = toQ(torso, 1.32, 1.42, .12);
    bag.position.copy(anchor);
    const acc = -(torso.position.y - (st._ly ?? torso.position.y)) / dt * .4 + st.walk * Math.sin(st.phase) * 2; st._ly = torso.position.y;
    st.bagV += (-st.bagAng * 30 - st.bagV * 4 + acc) * dt; st.bagAng += st.bagV * dt; st.bagAng = clamp(st.bagAng, -.6, .6);
    bag.rotation.set(st.bagAng * .4, -.35, st.bagAng);
    const top = toQ(head, .78, 1.3, -.05);
    const bagTop = bag.localToWorld(V(.12, -.08, 0)); quito.worldToLocal(bagTop);
    hose(strap, [top.clone().add(V(-.15, .05, -.1)), top, top.clone().lerp(bagTop, .5).add(V(.18, 0, .05)), bagTop], .035);

    st.reacting = Math.max(0, st.reacting - dt);
    st.hover = damp(st.hover, st.hoverT ? 1 : 0, 8, dt);
  }

  let running = true, rendered = false;
  renderer.setAnimationLoop(() => {
    if (!running) return;
    update();
    if (st.visible) { renderer.render(scene, camera); rendered = true; }
    else if (rendered) { renderer.clear(); rendered = false; }
  });

  // ---------- interacción ----------
  const api = {
    renderer, scene, camera,
    set(p) { // posición en NDC, escala relativa a la altura de pantalla, giro
      if (p.x !== undefined) st.tx = p.x; if (p.y !== undefined) st.ty = p.y; if (p.s !== undefined) st.ts = p.s; if (p.ry !== undefined) st.tRy = p.ry;
      if (p.pose && st.reacting <= 0) st.pose = p.pose; if (p.pose) st.basePose = p.pose;
      if (p.expr && !st.lockExpr) st.expr = p.expr; if (p.expr) st.baseExpr = p.expr;
    },
    snap() { st.x = st.tx; st.y = st.ty; st.s = st.ts; st.ry = st.tRy; st.prevX = st.x; },
    setExpression(name, lockMs = 0) {
      setExpression(name);
      if (lockMs) { st.lockExpr = true; clearTimeout(st._lt); st._lt = setTimeout(() => { st.lockExpr = false; st.expr = st.baseExpr; }, lockMs); }
    },
    setPose(name, ms = 0) { st.pose = name; if (ms) { clearTimeout(st._pt); st._pt = setTimeout(() => { st.pose = st.basePose; }, ms); } },
    jump(power = 7.5) { if (st.jump < .05) { st.jumpV = power; st.squash = .12; } },
    pointer(x, y) { st.pointer.x = x; st.pointer.y = y; st.pointer.active = true; },
    pointerLeave() { st.pointer.active = false; },
    hitTest, get state() { return st; },
    hover(on) { st.hoverT = on; },
    spinBy(v) { st.spinV += v; },
    dragStart() { st.drag = true; }, dragMove(dx) { st.spin += dx * .012; st.spinV = dx * .6; }, dragEnd() { st.drag = null; },
    reveal() { st.intro = 0; st.introDone = false; setTimeout(() => { st.introDone = true; st.intro = 1; }, 1200); setTimeout(() => api.setPose('wave', 2200), 650); },
    // posición de pantalla (px) de la parte de arriba de la cabeza, para el globo de diálogo
    headScreen(out = { x: 0, y: 0 }) {
      const p = V(0, 1.95, 0); head.localToWorld(p); p.project(camera);
      out.x = (p.x * .5 + .5) * W; out.y = (-p.y * .5 + .5) * H; out.visible = st.visible; out.scale = st.s; return out;
    },
    pause() { running = false; }, resume() { if (!running) { running = true; clock.getDelta(); } },
  };
  onProgress?.(1);
  return api;
}
