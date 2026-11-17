// =========================================================
// QUITO 3D — la ilustración original de Quito, tal cual, convertida en figura con volumen.
// Cada pose es un relieve (mapa de alto por regiones, el mismo método del Quito 3D del stand):
// frente y dorso inflados como un vinilo, luz suave que no altera los colores del dibujo.
// Se inclina hacia el cursor, rebota, salta, se gira arrastrándolo y cambia de pose con un "pop".
// =========================================================
import * as THREE from 'three';

const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const lerp = (a, b, t) => a + (b - a) * t;
const damp = (a, b, k, dt) => lerp(a, b, 1 - Math.exp(-k * dt));
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);

const FIG_H = 3.1;                     // alto de la figura (unidades)
const DEFAULT = 'carrusel-04-saludo';  // el Quito de la pantalla de carga

// emoción → pose dibujada
const BY_EXPR = {
  feliz: 'carrusel-04-saludo', guino: 'carrusel-04-saludo', euforico: 'carrusel-04-animando',
  enojado: 'carrusel-04-indignado', triste: 'llorando', avergonzado: 'tapandose', sorprendido: 'carrusel-04-emocionado',
};
function resolve(expr, pose, keys) {
  if (keys.has(expr)) return [expr, false];
  if (keys.has(pose)) return [pose, false];
  switch (pose) {
    case 'wave': return [expr === 'euforico' ? 'carrusel-04-animando' : 'carrusel-04-saludo', false];
    case 'thumbs': return ['saludo', false];
    case 'point': return [expr === 'enojado' ? 'carrusel-04-enojado' : 'senalando-feliz', false];
    case 'pointR': return [expr === 'enojado' ? 'carrusel-04-enojado' : 'senalando-feliz', true];
    case 'cheer': return ['carrusel-04-animando', false];
    case 'hips': return ['carrusel-04-indignado', false];
    case 'shy': return ['tapandose', false];
    default: return [BY_EXPR[expr] || DEFAULT, false];
  }
}

const vert = /* glsl */`
  uniform sampler2D uDepth; uniform float uAmt, uFlip, uBack; uniform vec2 uTexel, uSize;
  varying vec2 vUv; varying vec3 vN; varying float vD;
  float D(vec2 p){ return texture2D(uDepth, p).r; }
  void main(){
    vec2 st = uv;
    if (uFlip > .5) st.x = 1. - st.x;
    if (uBack > .5) st.x = 1. - st.x;
    float d = D(st);
    float dx = (D(st + vec2(uTexel.x, 0.)) - D(st - vec2(uTexel.x, 0.))) / (2. * uTexel.x);
    float dy = (D(st + vec2(0., uTexel.y)) - D(st - vec2(0., uTexel.y))) / (2. * uTexel.y);
    float sx = ((uFlip > .5) != (uBack > .5)) ? -1. : 1.;
    vec3 n = normalize(vec3(-dx * sx * uAmt / uSize.x, -dy * uAmt / uSize.y, 1.));
    vN = normalize(normalMatrix * n);
    vUv = st; vD = d;
    vec3 p = position; p.z += d * uAmt;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.);
  }
`;
const frag = /* glsl */`
  precision highp float;
  uniform sampler2D uMap; uniform float uBack, uHover;
  varying vec2 vUv; varying vec3 vN; varying float vD;
  void main(){
    vec4 t = texture2D(uMap, vUv);
    if (t.a < .45) discard;
    vec3 n = normalize(vN);
    vec3 L = normalize(vec3(-.45, .55, .75));
    float key = max(dot(n, L), 0.);
    float rim = pow(1. - max(n.z, 0.), 2.5);
    vec3 H = normalize(L + vec3(0., 0., 1.));
    float spec = pow(max(dot(n, H), 0.), 36.) * .14;
    vec3 col = t.rgb * (.76 + .32 * key) + spec + vec3(.75, .88, 1.) * rim * .2;
    col *= .92 + .08 * smoothstep(0., .25, vD);
    if (uBack > .5) col = mix(t.rgb * .42, vec3(.32, .16, .06), .35) * (.8 + .3 * key) + rim * .12;
    col += uHover * .035;
    gl_FragColor = vec4(col, 1.);
    #include <colorspace_fragment>
  }
`;

export async function initQuito(canvas, { onProgress } = {}) {
  onProgress?.(.1);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const maxAniso = renderer.capabilities.getMaxAnisotropy();
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(26, 1, .1, 100);
  const CAM_Z = 14; camera.position.set(0, .9, CAM_Z); camera.lookAt(0, 0, 0);

  const meta = await (await fetch('/data/quito.json')).json();
  const keys = new Set(Object.keys(meta));
  const loader = new THREE.TextureLoader();
  const cache = new Map();
  function load(key) {
    if (cache.has(key)) return cache.get(key);
    const p = Promise.all([
      loader.loadAsync(`/img/quito/hd/${key}.webp`).then((t) => { t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = maxAniso; return t; }),
      loader.loadAsync(`/img/quito/depth/${key}.png`).then((t) => { t.colorSpace = THREE.NoColorSpace; t.minFilter = THREE.LinearFilter; t.generateMipmaps = false; return t; }),
    ]).then(([map, depth]) => ({ key, map, depth, aspect: meta[key][0] / meta[key][1], texel: [1 / depth.image.width, 1 / depth.image.height] }));
    cache.set(key, p); return p;
  }

  // jerarquía
  const rig = new THREE.Group(); scene.add(rig);                                   // ubicación por scroll
  const quito = new THREE.Group(); quito.position.y = -1.55; rig.add(quito);
  const body = new THREE.Group(); quito.add(body);                                 // rebote + squash (pivote en los pies)
  const fig = new THREE.Group(); body.add(fig);                                    // giro

  const geo = new THREE.PlaneGeometry(1, 1, 220, 220); geo.translate(0, .5, 0);
  const mkMat = (isBack) => new THREE.ShaderMaterial({
    vertexShader: vert, fragmentShader: frag,
    uniforms: { uMap: { value: null }, uDepth: { value: null }, uAmt: { value: .55 }, uFlip: { value: 0 }, uBack: { value: isBack ? 1 : 0 },
      uTexel: { value: new THREE.Vector2(.003, .003) }, uSize: { value: new THREE.Vector2(3, 3) }, uHover: { value: 0 } },
  });
  const front = new THREE.Mesh(geo, mkMat(false)); fig.add(front);
  const back = new THREE.Mesh(geo, mkMat(true)); back.rotation.y = Math.PI; fig.add(back);
  front.visible = back.visible = false;

  // sombra de contacto
  const shCan = document.createElement('canvas'); shCan.width = shCan.height = 128;
  { const g = shCan.getContext('2d'); const gr = g.createRadialGradient(64, 64, 4, 64, 64, 62); gr.addColorStop(0, 'rgba(20,20,50,.5)'); gr.addColorStop(.6, 'rgba(20,20,50,.2)'); gr.addColorStop(1, 'rgba(20,20,50,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); }
  const shadow = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 1.5), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(shCan), transparent: true, depthWrite: false }));
  shadow.rotation.x = -Math.PI / 2; shadow.position.y = .01; quito.add(shadow);

  const hit = new THREE.Mesh(new THREE.BoxGeometry(2.7, 3.1, 1), new THREE.MeshBasicMaterial({ visible: false })); hit.position.y = 1.55; body.add(hit);

  let current = null, flip = false;
  function apply(tex, fl) {
    current = tex; flip = fl;
    const w = FIG_H * tex.aspect;
    for (const m of [front, back]) {
      const u = m.material.uniforms;
      u.uMap.value = tex.map; u.uDepth.value = tex.depth; u.uFlip.value = fl ? 1 : 0;
      u.uTexel.value.set(tex.texel[0] * 1.5, tex.texel[1] * 1.5); u.uSize.value.set(w, FIG_H);
      u.uAmt.value = .5 + .1 * Math.min(1, w / FIG_H);
      m.scale.set(w, FIG_H, 1); m.visible = true;
    }
    hit.scale.set(w / 2.7, 1, 1);
    shadow.scale.x = Math.max(.7, w / 3.2);
  }

  onProgress?.(.4);
  apply(await load(DEFAULT), false);
  // precarga liviana: solo las poses que más aparecen, cuando el navegador está libre (en celulares, a demanda)
  if (innerWidth > 860) {
    const idle = window.requestIdleCallback || ((f) => setTimeout(f, 3000));
    idle(() => ['carrusel-04-enojado', 'senalando-feliz', 'saludo', 'carrusel-04-animando'].forEach((k, i) => setTimeout(() => keys.has(k) && load(k), i * 400)));
  }
  onProgress?.(.8);

  // ---------- estado ----------
  const st = {
    x: 0, y: 0, s: .72, ry: 0, tx: 0, ty: 0, ts: .72, tRy: 0,
    expr: 'feliz', pose: 'idle', baseExpr: 'feliz', basePose: 'idle', lockExpr: false, lockPose: false,
    want: DEFAULT, wantFlip: false, pop: 0, pendingTex: null, pendingFlip: false,
    look: { x: 0, y: 0 }, pointer: { x: 0, y: 0, active: false },
    jump: 0, jumpV: 0, squash: 0, spin: 0, spinV: 0, drag: false,
    walk: 0, prevX: 0, intro: 1, introDone: true, hover: 0, hoverT: false, t: 0, visible: true,
  };

  async function updateLook() {
    const [k, fl] = resolve(st.expr, st.pose, keys);
    if (k === st.want && fl === st.wantFlip) return;
    st.want = k; st.wantFlip = fl;
    const tex = await load(k);
    if (st.want !== k || st.wantFlip !== fl) return; // cambió mientras cargaba
    if (current === tex && flip === fl) return;
    st.pop = 1; st.pendingTex = tex; st.pendingFlip = fl; // se achica, cambia y rebota
  }

  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  function hitTest(cx, cy) {
    const r = canvas.getBoundingClientRect();
    ndc.set(((cx - r.left) / r.width) * 2 - 1, -((cy - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera); return st.visible && ray.intersectObject(hit).length > 0;
  }

  let W = 1, H = 1, halfH = 1, halfW = 1;
  function resize() {
    W = canvas.clientWidth || innerWidth; H = canvas.clientHeight || innerHeight;
    renderer.setSize(W, H, false); camera.aspect = W / H; camera.updateProjectionMatrix();
    halfH = CAM_Z * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)); halfW = halfH * camera.aspect;
  }
  resize(); addEventListener('resize', resize);

  const clock = new THREE.Clock();
  function update() {
    const dt = Math.max(1e-3, Math.min(clock.getDelta(), 1 / 20)); st.t += dt; const t = st.t;
    st.x = damp(st.x, st.tx, 4.5, dt); st.y = damp(st.y, st.ty, 4.5, dt); st.s = damp(st.s, st.ts, 4.5, dt); st.ry = damp(st.ry, st.tRy, 4, dt);
    const mob = W < 760;
    const unit = Math.min(2 * halfH, 2 * halfW * (mob ? 1.15 : .9)) / 3.3;
    rig.position.set(st.x * halfW, st.y * halfH, 0);
    rig.scale.setScalar(Math.max(st.s, .0001) * unit);
    st.visible = st.s > .02 && st.y > -1.5 && st.y < 1.5 && Math.abs(st.x) < 1.6;
    const vx = (st.x - st.prevX) / dt; st.prevX = st.x;
    st.walk = damp(st.walk, clamp(Math.abs(vx) * 1.4 + Math.abs(st.ty - st.y) * 1.2, 0, 1), 6, dt);

    // intro: cae desde arriba y aterriza
    if (!st.introDone) st.intro = Math.min(1, st.intro + dt);
    const drop = st.intro < .6 ? (1 - (st.intro / .6) ** 2) * 7 : 0;
    if (st.intro >= .6 && !st._landed) { st._landed = true; st.squash = .25; }

    // inclinación hacia el cursor
    const lx = st.pointer.active ? clamp((st.pointer.x - st.x) * 1.2, -1, 1) : Math.sin(t * .45) * .35;
    const ly = st.pointer.active ? clamp((st.pointer.y - st.y) * 1.2, -1, 1) : Math.sin(t * .33) * .2;
    st.look.x = damp(st.look.x, lx, 5, dt); st.look.y = damp(st.look.y, ly, 5, dt);

    // giro por arrastre con inercia y vuelta al frente
    if (!st.drag) { st.spinV *= Math.exp(-2.4 * dt); st.spin += st.spinV * dt; if (Math.abs(st.spinV) < .6) st.spin = damp(st.spin, Math.round(st.spin / (Math.PI * 2)) * Math.PI * 2, 3, dt); }

    // salto
    st.jumpV -= 24 * dt; st.jump = Math.max(0, st.jump + st.jumpV * dt);
    if (st.jump === 0 && st.jumpV < 0) { if (st.jumpV < -3) st.squash = .2; st.jumpV = 0; }
    st.squash = damp(st.squash, 0, 8, dt);
    const air = st.jump > .01 || drop > 0;

    // pop de cambio de pose
    if (st.pop > 0) {
      st.pop = Math.max(0, st.pop - dt * 4.5);
      if (st.pendingTex && st.pop < .55) { apply(st.pendingTex, st.pendingFlip); st.pendingTex = null; st.squash = Math.max(st.squash, .16); }
    }
    const popK = st.pop > .55 ? Math.sin((1 - st.pop) / .45 * Math.PI / 2) : 0;

    // rebote "de manguera"
    const beat = Math.abs(Math.sin(t * Math.PI * 1.4));
    const bounce = air ? 0 : beat * .05 * (1 + st.walk);
    body.position.y = st.jump + drop + bounce;
    const sq = st.squash + (air ? -.05 : 0) + (1 - beat) * .012 + popK * .18;
    body.scale.set((1 + sq * .8) * (1 + st.hover * .03), (1 - sq) * (1 + st.hover * .03), 1);

    fig.rotation.y = st.ry + st.spin + st.look.x * .42 + Math.sin(t * Math.PI * .7) * .03;
    fig.rotation.x = -st.look.y * .1;
    body.rotation.z = Math.sin(t * Math.PI * .7) * .025 - st.look.x * .03 + st.walk * Math.sin(t * 9) * .06;

    const sk = 1 / (1 + (st.jump + drop) * .6);
    shadow.scale.y = sk; shadow.material.opacity = sk * (st.intro < .5 ? st.intro * 2 : 1);

    st.hover = damp(st.hover, st.hoverT ? 1 : 0, 8, dt);
    front.material.uniforms.uHover.value = st.hover;
  }

  let running = true, rendered = false;
  renderer.setAnimationLoop(() => {
    if (!running) return;
    update();
    if (st.visible) { renderer.render(scene, camera); rendered = true; }
    else if (rendered) { renderer.clear(); rendered = false; }
  });

  const api = {
    renderer, scene, camera,
    set(p) {
      if (p.x !== undefined) st.tx = p.x; if (p.y !== undefined) st.ty = p.y; if (p.s !== undefined) st.ts = p.s; if (p.ry !== undefined) st.tRy = p.ry * .6;
      if (p.pose) { st.basePose = p.pose; if (!st.lockPose) st.pose = p.pose; }
      if (p.expr) { st.baseExpr = p.expr; if (!st.lockExpr) st.expr = p.expr; }
      updateLook();
    },
    snap() { st.x = st.tx; st.y = st.ty; st.s = st.ts; st.ry = st.tRy; st.prevX = st.x; },
    setExpression(name, lockMs = 0) {
      st.expr = name; updateLook();
      if (lockMs) { st.lockExpr = true; clearTimeout(st._lt); st._lt = setTimeout(() => { st.lockExpr = false; st.expr = st.baseExpr; updateLook(); }, lockMs); }
    },
    setPose(name, ms = 0) {
      st.pose = name; updateLook();
      if (ms) { st.lockPose = true; clearTimeout(st._pt); st._pt = setTimeout(() => { st.lockPose = false; st.pose = st.basePose; updateLook(); }, ms); }
    },
    jump(power = 7.5) { if (st.jump < .05) { st.jumpV = power; st.squash = .14; } },
    pointer(x, y) { st.pointer.x = x; st.pointer.y = y; st.pointer.active = true; },
    pointerLeave() { st.pointer.active = false; },
    hitTest, get state() { return st; },
    hover(on) { st.hoverT = on; },
    spinBy(v) { st.spinV += v; },
    dragStart() { st.drag = true; }, dragMove(dx) { st.spin += dx * .012; st.spinV = dx * .6; }, dragEnd() { st.drag = false; },
    reveal() { st.intro = 0; st.introDone = false; st._landed = false; setTimeout(() => { st.introDone = true; st.intro = 1; }, 1100); },
    headScreen(out = { x: 0, y: 0 }) {
      const p = V(0, FIG_H * .96, 0); fig.localToWorld(p); p.project(camera);
      out.x = (p.x * .5 + .5) * W; out.y = (-p.y * .5 + .5) * H; out.visible = st.visible; out.scale = st.s; return out;
    },
    pause() { running = false; }, resume() { if (!running) { running = true; clock.getDelta(); } },
  };
  onProgress?.(1);
  return api;
}
