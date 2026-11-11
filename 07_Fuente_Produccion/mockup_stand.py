"""Mockup del Stand Bancala: render por trazado de rayos (numpy) de una escena de cuadrilateros
con las artes reales como texturas. Sombras suaves (luz de area), oclusion ambiental,
reflejo brillante en piso pulido. uso: mockup_stand.py [ancho] [salida]"""
import os, sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
S = os.path.dirname(os.path.abspath(__file__)); ART = S + '/art/stand'
rng = np.random.default_rng(3)


def tex(path, maxw=2400):
    im = Image.open(path).convert('RGBA')
    if im.width > maxw: im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    a = np.array(im).astype(np.float32) / 255
    a[..., :3] = a[..., :3] ** 2.2                     # a lineal
    return a


def lin(hexs):
    h = hexs.lstrip('#'); return (np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)]) / 255.) ** 2.2


Q = []  # quads: dict(p, u, v, n, tex|col, spec, alpha, shadow, tile)


def quad(p, u, v, col=None, tx=None, spec=0.04, rough=0.3, alpha=False, shadow=True, tile=None, name=''):
    p, u, v = map(lambda z: np.array(z, np.float64), (p, u, v))
    n = np.cross(u, v); n /= np.linalg.norm(n)
    Q.append(dict(p=p, u=u, v=v, n=n, uu=u / np.dot(u, u), vv=v / np.dot(v, v), col=None if col is None else np.array(col),
                  tx=tx, spec=spec, alpha=alpha, shadow=shadow, tile=tile, name=name))


def box(x0, y0, z0, x1, y1, z1, col, front=None, top=None, spec=0.04, name='', ry=0, piv=None):
    """caja alineada (opcional giro ry grados sobre eje Y alrededor de piv)"""
    def R(pt):
        if not ry: return pt
        c, s = np.cos(np.radians(ry)), np.sin(np.radians(ry)); px, pz = piv
        x, y, z = pt; dx, dz = x - px, z - pz
        return [px + dx * c + dz * s, y, pz - dx * s + dz * c]
    def Rv(vv):
        if not ry: return vv
        c, s = np.cos(np.radians(ry)), np.sin(np.radians(ry)); x, y, z = vv
        return [x * c + z * s, y, -x * s + z * c]
    W, H, D = x1 - x0, y1 - y0, z1 - z0
    quad(R([x0, y0, z1]), Rv([W, 0, 0]), Rv([0, H, 0]), col if front is None else None, front, spec, name=name + ' frente')       # frente (z+)
    quad(R([x1, y0, z0]), Rv([-W, 0, 0]), Rv([0, H, 0]), col, None, spec, name=name + ' dorso')
    quad(R([x0, y0, z0]), Rv([0, 0, D]), Rv([0, H, 0]), col, None, spec, name=name + ' izq')
    quad(R([x1, y0, z1]), Rv([0, 0, -D]), Rv([0, H, 0]), col, None, spec, name=name + ' der')
    quad(R([x0, y1, z1]), Rv([W, 0, 0]), Rv([0, 0, -D]), col if top is None else top, None, spec * 2, name=name + ' tapa')
    quad(R([x0, y0, z0]), Rv([W, 0, 0]), Rv([0, 0, D]), col, None, spec, name=name + ' base', shadow=True)


def floor_tex():
    n = 2048
    base = np.full((n, n, 3), 0.60, np.float32)
    noise = cv2.GaussianBlur(rng.normal(0, 1, (n, n)).astype(np.float32), (0, 0), 6) * 0.04
    speck = (rng.random((n, n)) > 0.997).astype(np.float32); speck = cv2.GaussianBlur(speck, (0, 0), 1.2) * 0.6
    base = base * (1 + noise)[..., None] - speck[..., None] * 0.25
    # juntas de baldosa 60 x 60 cm (tile de 2.4 m -> 4 juntas)
    for k in range(4):
        c = int(k * n / 4); base[max(0, c - 2):c + 2, :] *= 0.80; base[:, max(0, c - 2):c + 2] *= 0.80
    t = np.dstack([np.clip(base * np.array([1.0, 0.985, 0.95]), 0, 1) ** 2.2, np.ones((n, n))]).astype(np.float32)
    return t


def piso_tex():
    n = 1400
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((10, 10, n - 10, n - 10), fill=(58, 29, 12, 255)); d.ellipse((34, 34, n - 34, n - 34), fill=(45, 124, 222, 255))
    f = ImageFont.truetype(S + '/fonts/TitanOne-Regular.ttf', 150)
    for i, (t, c) in enumerate([('Sentate,', (255, 255, 255)), ('te', (255, 255, 255)), ('bancamos.', (122, 226, 166))]):
        w = d.textlength(t, font=f); y = 380 + i * 190
        d.text(((n - w) / 2 + 9, y + 11), t, font=f, fill=(58, 29, 12)); d.text(((n - w) / 2, y), t, font=f, fill=c, stroke_width=9, stroke_fill=(58, 29, 12))
    a = np.array(im).astype(np.float32) / 255; a[..., :3] = a[..., :3] ** 2.2
    return a


def build_scene():
    # piso y entorno (hall)
    quad([-8, 0, 9], [16, 0, 0], [0, 0, -12], tx=floor_tex(), spec=0.0, tile=2.4, name='piso')
    wall = lin('#d8d0c4')
    quad([-8, 0, -1.6], [16, 0, 0], [0, 5, 0], col=wall * 0.95, name='pared fondo')
    for x in (-4.6, -0.2, 4.2):  # pilares
        box(x - 0.25, 0, -1.6, x + 0.25, 5, -1.25, wall * 0.98, name='pilar')
    box(-8, 0, -1.6, 8, 0.12, -1.57, lin('#8a8176'), name='zocalo')
    # 1 backwall 3 x 2.2 (lona) + bastidor
    bw = tex(ART + '/backwall.png', 3000)
    box(-1.5, 0.02, -0.08, 1.5, 2.22, 0.0, lin('#d9d9d9'), front=bw, name='backwall')
    for sx in (-1.47, 1.47): box(sx - 0.02, 0, -0.35, sx + 0.02, 0.03, 0.05, lin('#bfc3c7'), spec=0.3, name='pie')
    # banco real del campus (asiento de tablas + estructura roja)
    wood = lin('#b9773a'); red = lin('#c8202a')
    for i in range(4):
        z0 = 0.44 + i * 0.112
        box(-0.95, 0.43, z0, 0.95, 0.46, z0 + 0.095, wood * (0.95 + 0.06 * (i % 2)), spec=0.05, name='tabla')
    for sx in (-0.82, 0.82):
        box(sx - 0.03, 0.0, 0.44, sx + 0.03, 0.43, 0.50, red, spec=0.25, name='pata')
        box(sx - 0.03, 0.0, 0.81, sx + 0.03, 0.43, 0.87, red, spec=0.25, name='pata')
        box(sx - 0.03, 0.38, 0.44, sx + 0.03, 0.43, 0.87, red, spec=0.25, name='travesano')
    # vinilo de piso
    quad([-0.7, 0.002, 2.48], [1.4, 0, 0], [0, 0, -1.4], tx=piso_tex(), spec=0.02, alpha=True, shadow=False, name='vinilo')
    # 2 mostrador 1.2 x 1.0 x 0.5 con frente impreso, tapa blanca laqueada
    mo = tex(ART + '/mostrador.png', 1600)
    box(-1.95, 0.0, 1.20, -0.75, 1.0, 1.70, lin('#f2efe8'), front=mo, top=lin('#f6f4ef'), spec=0.10, name='mostrador')
    box(-1.97, 1.0, 1.18, -0.73, 1.03, 1.72, lin('#f8f6f1'), spec=0.18, name='tapa')
    # figura 3D (billboard con base y sombra horneadas)
    fg = tex(ART + '/figura_recorte.png', 1400)
    fh = 0.62; fw = fh * fg.shape[1] / fg.shape[0]
    quad([-1.20 - fw / 2, 1.03 - 0.075 * fh, 1.47], [fw, 0, 0], [0, fh, 0], tx=fg, alpha=True, shadow=True, spec=0.0, name='figura')
    # display A5 en atril acrilico (inclinado)
    dp = tex(ART + '/display.png', 1000)
    t = np.radians(14)
    quad([-1.86, 1.035, 1.55], [0.148, 0, 0], [0, 0.21 * np.cos(t), -0.21 * np.sin(t)], tx=dp, spec=0.25, name='display')
    # pila de folletos
    fo = tex(ART + '/folleto_exterior.png', 1200)[:, 1485 * 1200 // 2970:]
    box(-0.98, 1.03, 1.42, -0.83, 1.05, 1.63, lin('#f4f1ea'), name='folletos')
    quad([-0.98, 1.0501, 1.63], [0.148, 0, 0], [0, 0, -0.21], tx=fo, spec=0.05, name='folleto tapa')
    # 3 roll-up 0.85 x 2.0, girado hacia el publico
    ru = tex(ART + '/rollup.png', 1200)
    box(1.10, 0.0, 0.95, 1.95, 0.09, 1.17, lin('#c4c8cc'), spec=0.4, name='base rollup', ry=-18, piv=(1.52, 1.06))
    c, s = np.cos(np.radians(-18)), np.sin(np.radians(-18))
    quad([1.52 - 0.425 * c, 0.09, 1.06 + 0.425 * s], [0.85 * c, 0, -0.85 * s], [0, 2.0, 0], tx=ru, spec=0.03, name='rollup')


def intersect(O, D, q, need_alpha=True):
    den = D @ q['n']
    with np.errstate(divide='ignore', invalid='ignore'):
        t = ((q['p'] - O) @ q['n']) / den
    hit = O + D * t[:, None]
    rel = hit - q['p']
    a = rel @ q['uu']; b = rel @ q['vv']
    ok = (t > 1e-4) & (a >= 0) & (a <= 1) & (b >= 0) & (b <= 1) & np.isfinite(t)
    if q['alpha'] and need_alpha and q['tx'] is not None and ok.any():
        al = sample(q, a[ok], b[ok])[:, 3]
        ok2 = ok.copy(); ok2[ok] = al > 0.5; ok = ok2
    return t, a, b, ok


def sample(q, a, b):
    tx = q['tx']; h, w = tx.shape[:2]
    if q['tile']:
        L = np.linalg.norm(q['u']); M = np.linalg.norm(q['v'])
        x = (a * L / q['tile'] % 1) * (w - 1); y = (b * M / q['tile'] % 1) * (h - 1)
    else:
        x = a * (w - 1); y = (1 - b) * (h - 1)
    n = x.size; C = 2048; pad = (-n) % C
    x = np.pad(x.astype(np.float32), (0, pad)).reshape(-1, C); y = np.pad(y.astype(np.float32), (0, pad)).reshape(-1, C)
    out = cv2.remap(tx, x, y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return out.reshape(-1, 4)[:n]


def trace(O, D):
    n = D.shape[0]
    T = np.full(n, np.inf); I = np.full(n, -1); A = np.zeros(n); Bb = np.zeros(n)
    for i, q in enumerate(Q):
        t, a, b, ok = intersect(O if O.ndim == 1 else O, D, q)
        m = ok & (t < T)
        T[m] = t[m]; I[m] = i; A[m] = a[m]; Bb[m] = b[m]
    return T, I, A, Bb


def occluded(P, Ld, maxd):
    vis = np.zeros(P.shape[0], bool)
    for q in Q:
        if not q['shadow']: continue
        t, a, b, ok = intersect(P, Ld, q)
        vis |= ok & (t < maxd)
    return vis


def albedo(I, A, Bb):
    n = I.size; col = np.zeros((n, 3)); spec = np.zeros(n); nrm = np.zeros((n, 3))
    for i, q in enumerate(Q):
        m = I == i
        if not m.any(): continue
        if q['tx'] is not None:
            s = sample(q, A[m], Bb[m])
            base = q['col'] if q['col'] is not None else np.array([0.85, 0.85, 0.85])
            col[m] = s[:, :3] * s[:, 3:4] + base * (1 - s[:, 3:4]) if q['alpha'] and q['name'] == 'vinilo' else s[:, :3]
        else:
            col[m] = q['col']
        spec[m] = q['spec']; nrm[m] = q['n']
    return col, spec, nrm


LIGHT = np.array([-2.8, 4.2, 4.8]); LRAD = 0.9
FILL = np.array([0.35, 0.37, 0.40])


def shade(O, D, T, I, A, Bb, ks=10, ka=6, bounce=False):
    n = I.size
    hit = (O + D * T[:, None]) if O.ndim == 2 else O + D * T[:, None]
    col, spec, nrm = albedo(I, A, Bb)
    flip = (np.einsum('ij,ij->i', nrm, D) > 0)
    nrm[flip] *= -1
    valid = I >= 0
    P = hit + nrm * 1e-3
    # luz de area (sombras suaves)
    vis = np.zeros(n)
    Ld0 = LIGHT - P
    for k in range(ks if not bounce else 2):
        jit = rng.normal(0, LRAD / 2, (n, 3)); Lp = LIGHT + jit
        Ld = Lp - P; dist = np.linalg.norm(Ld, axis=1); Ld /= dist[:, None]
        vis += ~occluded(P[valid] if False else P, Ld, dist)
    vis /= (ks if not bounce else 2)
    L = Ld0 / np.linalg.norm(Ld0, axis=1)[:, None]
    ndl = np.clip(np.einsum('ij,ij->i', nrm, L), 0, 1)
    # oclusion ambiental
    ao = np.ones(n)
    if not bounce:
        occ = np.zeros(n)
        for k in range(ka):
            r = rng.normal(0, 1, (n, 3)); r /= np.linalg.norm(r, axis=1)[:, None]
            r = np.where((np.einsum('ij,ij->i', r, nrm) < 0)[:, None], -r, r)
            r = r + nrm; r /= np.linalg.norm(r, axis=1)[:, None]
            occ += occluded(P, r, 0.9)
        ao = 1 - 0.85 * occ / ka
    sky = 0.55 + 0.45 * np.clip(nrm[:, 1], 0, 1)
    light = col * (FILL[None] * 1.55 * ao[:, None] * sky[:, None] + np.array([1.0, 0.95, 0.87])[None] * 2.0 * (ndl * vis)[:, None])
    # especular
    Hh = L - D; Hh /= np.linalg.norm(Hh, axis=1)[:, None]
    sp = np.clip(np.einsum('ij,ij->i', nrm, Hh), 0, 1) ** 60 * spec * 6 * vis
    light += sp[:, None]
    light[~valid] = np.array([0.6, 0.6, 0.6])
    return light, nrm, hit, valid


def render(W, Hh, out):
    build_scene()
    cam = np.array([0.95, 1.50, 5.7]); look = np.array([-0.15, 1.05, 0.60]); fov = 34
    f = look - cam; f /= np.linalg.norm(f); r = np.cross(f, [0, 1, 0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    th = np.tan(np.radians(fov / 2)); tw = th * W / Hh
    img = np.zeros((Hh, W, 3), np.float32)
    rows = max(1, 240000 // W)
    for y0 in range(0, Hh, rows):
        ys = np.arange(y0, min(Hh, y0 + rows)); xs = np.arange(W)
        X, Y = np.meshgrid(xs, ys)
        px = ((X + 0.5) / W * 2 - 1) * tw; py = (1 - (Y + 0.5) / Hh * 2) * th
        D = f[None] + px.reshape(-1, 1) * r[None] + py.reshape(-1, 1) * u[None]; D /= np.linalg.norm(D, axis=1)[:, None]
        T, I, A, Bb = trace(cam, D)
        c, nrm, hit, valid = shade(cam, D, T, I, A, Bb)
        # reflejo brillante en el piso pulido
        fl = (I == 0)
        if fl.any():
            Df = D[fl].copy(); Df[:, 1] *= -1
            Df += rng.normal(0, 0.035, Df.shape); Df /= np.linalg.norm(Df, axis=1)[:, None]
            Pf = hit[fl] + np.array([0, 1e-3, 0])
            T2, I2, A2, B2 = trace(Pf, Df)
            c2, _, _, v2 = shade(Pf, Df, T2, I2, A2, B2, ks=2, ka=0, bounce=True)
            fres = 0.06 + 0.25 * (1 - np.clip(-D[fl][:, 1] * 1.0, 0, 1)) ** 4
            c[fl] = c[fl] * (1 - fres[:, None] * v2[:, None]) + c2 * (fres * v2)[:, None]
        img[ys] = c.reshape(len(ys), W, 3)
        print(f'{min(Hh, y0 + rows)}/{Hh}', flush=True)
    np.save(out + '.npy', img)
    finish(img, out)


def finish(img, out):
    Hh, W = img.shape[:2]
    # suavizar ruido de muestreo solo en baja frecuencia: bilateral leve
    x = img / (1 + img * 0.25)                      # tonemap suave
    x = np.clip(x * 1.05, 0, 1) ** (1 / 2.2)
    m = x.mean(2, keepdims=True); x = np.clip(m + (x - m) * 1.12, 0, 1)
    x8 = (x * 255).astype(np.uint8)
    x8 = cv2.bilateralFilter(x8, 5, 14, 3)
    x = x8.astype(np.float32) / 255
    # bloom sutil
    hl = np.clip(x - 0.82, 0, 1); x = 1 - (1 - x) * (1 - cv2.GaussianBlur(hl, (0, 0), W / 150) * 0.6)
    yy, xx = np.mgrid[0:Hh, 0:W].astype(np.float32)
    rr = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - Hh / 2) / (Hh / 2)) ** 2)
    x *= (1 - 0.16 * np.clip(rr - 0.55, 0, 1) ** 1.4)[..., None]
    Image.fromarray((np.clip(x, 0, 1) * 255 + .5).astype(np.uint8)).save(out, quality=95)
    print('ok', out)


if __name__ == '__main__':
    W = int(sys.argv[1]) if len(sys.argv) > 1 else 900
    out = sys.argv[2] if len(sys.argv) > 2 else ART + '/mockup_preview.jpg'
    render(W, int(W * 2 / 3), out)
