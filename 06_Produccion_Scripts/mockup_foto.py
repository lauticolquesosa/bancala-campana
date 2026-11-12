"""Mockup del Stand Bancala montado sobre una foto real del campus (UCASAL, mediodia).
La camara se calibro con la foto: puntos de fuga del camino y de la fachada -> focal (HFOV 91 grados),
giro y cabeceo; altura 1,70 m (verificada con la puerta 2,04 m, el totem 1,98 m y la baliza 0,72 m).
El stand se apoya sobre el cesped, sobre una tarima, con el frente hacia el camino (alineado a la grilla
de la foto). Sol de mediodia alto desde la izquierda (sombras de troncos y mesas). Render por trazado de
rayos (reutiliza mockup_stand.py) con supermuestreo; el cesped funciona como 'atrapasombras' sobre la foto.
uso: mockup_foto.py [escala] [salida]   (escala 2 = 2950 x 1660)"""
import os, sys, numpy as np, cv2
from PIL import Image
import mockup_stand as ms
from mockup_stand import tex, lin, quad, box, Q
S = ms.S; ART = ms.ART; FOTO = ART + '/foto/facultad_original.jpg'
rng = np.random.default_rng(7)

# ---------------- camara calibrada (pixeles de la foto original 1475 x 830) ----------------
W0, H0 = 1475, 830; CX, CY = W0 / 2, H0 / 2
V1 = np.array([1268.2, 370.5])      # fuga del camino
V2 = np.array([-260.0, 405.0])      # fuga de la fachada / juntas del camino
F = np.sqrt(-((V1 - [CX, CY]) @ (V2 - [CX, CY])))
Kinv = lambda x, y: np.stack([(x - CX) / F, (y - CY) / F, np.ones_like(x)], -1)
dz = Kinv(*V1); dz /= np.linalg.norm(dz)
dx = -Kinv(*V2); dx -= dz * (dx @ dz); dx /= np.linalg.norm(dx)
up = np.cross(dz, dx); up = -up if up[1] > 0 else up; up /= np.linalg.norm(up)
RW = np.stack([dx, up, dz], 1)      # cam = RW @ mundo   (mundo: X der, Y arriba, Z hacia el fondo)
CAMH = 1.70
# stand: backwall en X = XC (mundo), centrado en Z = ZC, frente hacia +X (hacia el camino)
XC, ZC = -7.0, 3.5
M = np.array([[0, 0, 1.], [0, 1, 0], [1, 0, 0]])        # mundo -> local del stand (x = Z, y = Y, z = X)
CAM = np.array([0 - ZC, CAMH, 0 - XC])             # camara en coords locales
DECK = 0.10                                             # alto de la tarima

# ---------------- sol de mediodia ----------------
EL = np.radians(72)
sw = np.array([-0.92, -0.40]); sw /= np.linalg.norm(sw)  # hacia el sol, en (X, Z) mundo
SUN = np.array([sw[1] * np.cos(EL), np.sin(EL), sw[0] * np.cos(EL)]); SUN /= np.linalg.norm(SUN)
ES, ESKY = 0.90, 0.40
SUNC = np.array([1.0, 0.97, 0.91]); SKYC = np.array([0.93, 0.98, 1.08]); GRASSC = np.array([0.50, 0.62, 0.28])


def deck_tex():
    """tarima de WPC: tablas de 14 cm a lo largo del backwall, juntas de 6 mm, veta suave."""
    n = 2048; L = 4.6                       # la textura cubre 4,6 m de ancho
    y = np.arange(n)[:, None] / n * 3.2; x = np.arange(n)[None, :] / n * L
    board = np.floor(y / 0.146).astype(int)
    tone = 0.92 + 0.10 * ((board * 7919) % 13) / 13
    grain = cv2.GaussianBlur(rng.normal(0, 1, (n, n)).astype(np.float32), (0, 0), sigmaX=24, sigmaY=1.2) * 0.25
    base = np.array([0.56, 0.50, 0.43])[None, None] * (tone + grain)[..., None]
    gap = ((y % 0.146) < 0.007)[..., None]
    end = (((x + (board % 3) * 0.9) % 2.4) < 0.006)[..., None]
    c = np.where(gap | end, base * 0.30, base)
    return np.dstack([np.clip(c, 0, 1) ** 2.2, np.ones((n, n))]).astype(np.float32)


def build():
    Q.clear(); y0 = DECK
    # tarima 4,5 x 3,1 m, 10 cm de alto, con faldon
    dk = deck_tex(); wpc = lin('#8c8073')
    quad([-2.20, y0, 2.62], [4.6, 0, 0], [0, 0, -3.2], tx=dk, spec=0.03, name='tarima tapa')
    for p, u in [([-2.20, 0, 2.62], [4.6, 0, 0]), ([2.40, 0, 2.62], [0, 0, -3.2]), ([2.40, 0, -0.58], [-4.6, 0, 0]), ([-2.20, 0, -0.58], [0, 0, 3.2])]:
        quad(p, u, [0, y0, 0], col=wpc * 0.82, spec=0.02, name='tarima lado')
    # 1 backwall 3 x 2,2 sobre la tarima + pies con lastre
    bw = tex(ART + '/backwall.png', 3000)
    box(-1.5, y0 + 0.02, -0.08, 1.5, y0 + 2.22, 0.0, lin('#d9d9d9'), front=bw, name='backwall')
    for sx in (-1.47, 1.47):
        box(sx - 0.02, y0, -0.45, sx + 0.02, y0 + 0.03, 0.05, lin('#bfc3c7'), spec=0.3, name='pie')
        box(sx - 0.09, y0, -0.44, sx + 0.09, y0 + 0.025, -0.16, lin('#8d9094'), spec=0.2, name='lastre')
    # banco real del campus, a la izquierda de la estatua
    wood = lin('#b9773a'); red = lin('#c8202a'); BX0, BX1 = -1.30, 0.12
    for i in range(4):
        z0 = 0.44 + i * 0.112
        box(BX0, y0 + 0.43, z0, BX1, y0 + 0.46, z0 + 0.095, wood * (0.95 + 0.06 * (i % 2)), spec=0.05, name='tabla')
    for sx in (BX0 + 0.13, BX1 - 0.13):
        box(sx - 0.03, y0, 0.44, sx + 0.03, y0 + 0.43, 0.50, red, spec=0.25, name='pata')
        box(sx - 0.03, y0, 0.81, sx + 0.03, y0 + 0.43, 0.87, red, spec=0.25, name='pata')
        box(sx - 0.03, y0 + 0.38, 0.44, sx + 0.03, y0 + 0.43, 0.87, red, spec=0.25, name='travesano')
    # vinilo sobre la tarima
    vin = tex_vinilo()
    quad([-0.7, y0 + 0.002, 2.48], [1.4, 0, 0], [0, 0, -1.4], col=lin('#8c8073'), tx=vin, spec=0.02, alpha=True, shadow=False, name='vinilo')
    # 2 mostrador
    mo = tex(ART + '/mostrador.png', 1600)
    box(-1.95, y0, 1.20, -0.75, y0 + 1.0, 1.70, lin('#f2efe8'), front=mo, top=lin('#f6f4ef'), spec=0.10, name='mostrador')
    box(-1.97, y0 + 1.0, 1.18, -0.73, y0 + 1.03, 1.72, lin('#f8f6f1'), spec=0.18, name='tapa')
    dp = tex(ART + '/display.png', 1000); t = np.radians(14)
    quad([-1.50, y0 + 1.035, 1.50], [0.148, 0, 0], [0, 0.21 * np.cos(t), -0.21 * np.sin(t)], tx=dp, spec=0.25, name='display')
    fo = tex(ART + '/folleto_exterior.png', 1200)[:, 1485 * 1200 // 2970:]
    box(-0.98, y0 + 1.03, 1.42, -0.83, y0 + 1.05, 1.63, lin('#f4f1ea'), name='folletos')
    quad([-0.98, y0 + 1.0501, 1.63], [0.148, 0, 0], [0, 0, -0.21], tx=fo, spec=0.05, name='folleto tapa')
    # 3 roll-up
    ru = tex(ART + '/rollup.png', 1200); RX, RZ, RA = 1.90, 1.20, -24
    box(RX - 0.425, y0, RZ - 0.11, RX + 0.425, y0 + 0.09, RZ + 0.11, lin('#c4c8cc'), spec=0.4, name='base rollup', ry=RA, piv=(RX, RZ))
    c, s = np.cos(np.radians(RA)), np.sin(np.radians(RA))
    quad([RX - 0.425 * c, y0 + 0.09, RZ + 0.425 * s], [0.85 * c, 0, -0.85 * s], [0, 2.0, 0], tx=ru, spec=0.03, name='rollup')
    # 4 Quito 3D en tamano real (billboard orientado a la camara, base O 90)
    qr_ = tex(ART + '/quito_real_recorte.png', 1400)
    qw = 1.10; qh = qw * qr_.shape[0] / qr_.shape[1]
    SX, SZ = 0.78, 0.42; zf = SZ + 0.45
    d = CAM - np.array([SX, 0, zf]); d[1] = 0; d /= np.linalg.norm(d)
    ux = np.array([d[2], 0, -d[0]])
    quad(np.array([SX, y0, zf]) - ux * qw / 2, ux * qw, [0, qh, 0], tx=qr_, alpha=True, shadow=True, spec=0.0, name='estatua')
    global STAT
    STAT = dict(c=np.array([SX, y0, SZ]), back=-d)


def tex_vinilo():
    return ms.piso_tex()


def rays(xs, ys, scale):
    """pixeles de la imagen escalada -> rayos en coordenadas locales del stand"""
    x1 = (xs + 0.5) / scale - 0.5; y1 = (ys + 0.5) / scale - 0.5
    dc = Kinv(x1, y1); dw = dc @ RW                       # RW.T @ dc
    dl = dw[:, [2, 1, 0]]
    return dl / np.linalg.norm(dl, axis=1)[:, None]


def sky_irr(nrm):
    ny = nrm[:, 1:2]
    return ESKY * (0.55 + 0.45 * ny) * SKYC + 0.10 * np.clip(0.5 - 0.5 * ny, 0, 1) * GRASSC


def sun_vis(P, n=3):
    v = np.zeros(P.shape[0])
    for k in range(n):
        Ld = SUN + rng.normal(0, 0.006, (P.shape[0], 3)); Ld /= np.linalg.norm(Ld, axis=1)[:, None]
        v += ~ms.occluded(P, Ld, 50.0)
    return v / n


def ao(P, nrm, k=5, dist=0.8):
    occ = np.zeros(P.shape[0])
    for i in range(k):
        r = rng.normal(0, 1, (P.shape[0], 3)); r /= np.linalg.norm(r, axis=1)[:, None]
        r = np.where((np.einsum('ij,ij->i', r, nrm) < 0)[:, None], -r, r); r = r + nrm; r /= np.linalg.norm(r, axis=1)[:, None]
        occ += ms.occluded(P, r, dist)
    return 1 - occ / k


def shade_obj(D, T, I, A, Bb):
    n = I.size
    hit = CAM + D * T[:, None]
    col, spec, nrm = ms.albedo(I, A, Bb)
    flip = np.einsum('ij,ij->i', nrm, D) > 0; nrm[flip] *= -1
    names = np.array([q['name'] for q in Q])[I]
    stat = names == 'estatua'
    P = hit + nrm * 1e-3
    # la estatua es un billboard: sombras y oclusion se consultan desde su volumen real (40 cm mas atras)
    P[stat] = hit[stat] + STAT['back'] * 0.40 + np.array([0, 0, 0])
    vis = sun_vis(P)
    a = ao(P, np.where(stat[:, None], np.array([0, 1., 0]), nrm))
    ndl = np.clip(nrm @ SUN, 0, 1)
    out = col * (ES * SUNC * (ndl * vis)[:, None] + sky_irr(nrm) * a[:, None])
    # lona y roll-up a contraluz: un poco del sol atraviesa la tela
    thru = np.isin(names, ['backwall frente', 'rollup']) & (nrm @ SUN < 0)
    out[thru] += col[thru] * (ES * 0.10 * np.clip(-(nrm[thru] @ SUN), 0, 1))[:, None] * SUNC
    # estatua: foto de estudio relumbrada con el sol (luz alta de la izquierda)
    if stat.any():
        hy = (hit[stat, 1] - DECK) / 1.45
        out[stat] = col[stat] * (0.40 * a[stat, None] * SKYC + ES * 0.80 * vis[stat, None] * (0.75 + 0.35 * np.clip(hy, 0, 1))[:, None] * SUNC)
    Hh = SUN - D; Hh /= np.linalg.norm(Hh, axis=1)[:, None]
    out += (np.clip(np.einsum('ij,ij->i', nrm, Hh), 0, 1) ** 80 * spec * 8 * vis)[:, None]
    return out, names, hit


def render(scale=2, out=None):
    build()
    Wd, Hd = int(W0 * scale), int(H0 * scale); ss = 2; sc = scale * ss
    # zona a trazar: caja envolvente del stand proyectada (+ margen para sombras)
    pts = np.array([[x, y, z] for x in (-2.3, 2.5) for y in (0, 2.5) for z in (-0.7, 2.7)])
    pw = (pts[:, [2, 1, 0]] + [XC, -CAMH, ZC]) @ RW.T
    px = CX + F * pw[:, 0] / pw[:, 2]; py = CY + F * pw[:, 1] / pw[:, 2]
    bx0, bx1 = int(max(0, (px.min() - 25) * sc)), int(min(W0 * sc, (px.max() + 25) * sc))
    by0, by1 = int(max(0, (py.min() - 25) * sc)), int(min(H0 * sc, (py.max() + 25) * sc))
    bx0 -= bx0 % ss; by0 -= by0 % ss; bx1 -= bx1 % ss; by1 -= by1 % ss
    w, h = bx1 - bx0, by1 - by0
    print('zona', bx0, by0, w, h, flush=True)
    colA = np.zeros((h, w, 3), np.float32); alA = np.zeros((h, w), np.float32); shA = np.ones((h, w, 3), np.float32)
    rows = max(1, 160000 // w)
    for r0 in range(0, h, rows):
        ys, xs = np.mgrid[r0:min(h, r0 + rows), 0:w]
        ys = ys + by0; xs = xs + bx0
        D = rays(xs.ravel().astype(float), ys.ravel().astype(float), sc)
        T, I, A, Bb = ms.trace(CAM, D)
        obj = I >= 0
        c = np.zeros((D.shape[0], 3)); al = obj.astype(np.float32); sh = np.ones((D.shape[0], 3))
        if obj.any():
            o, names, hit = shade_obj(D[obj], T[obj], I[obj], A[obj], Bb[obj])
            c[obj] = o
            # pasto sobre el borde inferior de la tarima
            side = names == 'tarima lado'
            if side.any():
                hy = hit[side, 1]
                blade = (np.sin(xs.ravel()[obj][side] * 1.9) * 0.5 + np.sin(xs.ravel()[obj][side] * 0.73 + 1.3) * 0.5 + rng.random(side.sum()) * 0.6)
                cover = hy < 0.018 + 0.03 * np.clip(blade, 0, 1)
                tmp = al[obj]; tmp[np.where(side)[0][cover]] = 0; al[obj] = tmp
        # cesped: atrapasombras (sol + cielo)
        g = ~obj & (D[:, 1] < 0)
        if g.any():
            t = -CAM[1] / D[g, 1]; P = CAM + D[g] * t[:, None] + np.array([0, 1e-3, 0])
            near = (P[:, 0] > -3.5) & (P[:, 0] < 4.0) & (P[:, 2] > -1.5) & (P[:, 2] < 4.0)
            if near.any():
                Pn = P[near]; nv = np.tile([0, 1., 0], (Pn.shape[0], 1))
                v = sun_vis(Pn, 3); a = ao(Pn, nv, 6, 0.9)
                full = ES * SUN[1] + ESKY
                m = (ES * SUN[1] * v + ESKY * a) / full
                tint = 1 + (1 - v)[:, None] * (SKYC - 1) * 1.4
                tmp = sh[g]; tmp[near] = m[:, None] * tint; sh[g] = tmp
        rr = slice(r0, min(h, r0 + rows))
        colA[rr] = c.reshape(-1, w, 3); alA[rr] = al.reshape(-1, w); shA[rr] = sh.reshape(-1, w, 3)
        print(f'{min(h, r0 + rows)}/{h}', flush=True)
    # supermuestreo 2x2 -> resolucion final
    def down(x):
        return cv2.resize(x, (x.shape[1] // ss, x.shape[0] // ss), interpolation=cv2.INTER_AREA)
    pre = down(colA * alA[..., None]); al = down(alA); sh = down(shA)
    np.savez_compressed(ART + '/foto/_render.npz', pre=pre, al=al, sh=sh, box=np.array([bx0 // ss, by0 // ss, Wd, Hd]))
    composite(scale, out)


def composite(scale=2, out=None):
    z = np.load(ART + '/foto/_render.npz'); pre, al, sh = z['pre'], z['al'], z['sh']; bx, by, Wd, Hd = z['box']
    ph = Image.open(FOTO).convert('RGB').resize((Wd, Hd), Image.LANCZOS)
    ph = np.array(ph).astype(np.float32) / 255
    bl = cv2.GaussianBlur(ph, (0, 0), 1.2); ph = np.clip(ph + (ph - bl) * 0.35, 0, 1)   # nitidez leve del reescalado
    lin_ = ph ** 2.2
    h, w = al.shape
    reg = lin_[by:by + h, bx:bx + w]
    reg = reg * sh
    # el render se ablanda y lleva grano para igualar la foto
    pre = cv2.GaussianBlur(pre, (0, 0), 0.55); al_ = cv2.GaussianBlur(al, (0, 0), 0.55)
    obj = np.clip(pre / np.maximum(al_, 1e-4)[..., None], 0, None)
    obj_s = (obj / (1 + 0.08 * obj)) ** (1 / 2.2)
    m = obj_s.mean(2, keepdims=True); obj_s = np.clip(m + (obj_s - m) * 1.08, 0, 1)      # saturacion como la foto
    grain = rng.normal(0, 0.012, obj_s.shape[:2]).astype(np.float32)[..., None]
    obj_s = np.clip(obj_s + grain * al_[..., None], 0, 1)
    reg_s = reg ** (1 / 2.2)
    comp = obj_s * al_[..., None] + reg_s * (1 - al_[..., None])
    res = ph.copy(); res[by:by + h, bx:bx + w] = np.clip(comp, 0, 1)
    out = out or ART + '/mockup_foto.jpg'
    Image.fromarray((res * 255 + .5).astype(np.uint8)).save(out, quality=95); print('ok', out)


if __name__ == '__main__':
    sc = float(sys.argv[1]) if len(sys.argv) > 1 else 1
    if len(sys.argv) > 2 and sys.argv[2] == 'comp':
        composite(sc)
    else:
        render(sc, sys.argv[2] if len(sys.argv) > 2 else None)
