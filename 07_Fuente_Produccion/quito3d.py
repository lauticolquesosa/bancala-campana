"""Quito 3D: convierte la ilustracion 2D en una figura tipo vinilo/resina pintada.
Relieve inflado por regiones (cada zona delimitada por el contorno tinta se abomba sola),
contornos como surcos, luz de estudio (key + fill + rim), especular brillante y oclusion.
Opcional: giro 3/4 sobre el eje vertical (splatting con z-buffer).
uso: quito3d.py pose out.png [giro_grados] [alto_px]"""
import sys, os, numpy as np, cv2
from PIL import Image
S = os.path.dirname(os.path.abspath(__file__))


def poisson(mask, iters=160):
    """inflado tipo membrana: resuelve lap(h) = -1 dentro de mask (h=0 afuera), multiresolucion."""
    H, W = mask.shape
    h = None
    for f in [16, 8, 4, 2, 1]:
        m = (cv2.resize(mask.astype(np.float32), (max(1, W // f), max(1, H // f)), interpolation=cv2.INTER_AREA) > 0.5).astype(np.float32)
        h = np.zeros_like(m) if h is None else cv2.resize(h, (m.shape[1], m.shape[0]), interpolation=cv2.INTER_LINEAR) * 4
        for _ in range(iters if f > 1 else iters // 2):
            nb = (np.roll(h, 1, 0) + np.roll(h, -1, 0) + np.roll(h, 1, 1) + np.roll(h, -1, 1)) * 0.25
            h = (nb + 0.25) * m
    return h


def height_map(rgb, a):
    H, W = a.shape
    L = rgb.mean(2)
    solid = (a > 0.5).astype(np.uint8)
    ink = ((L < 0.30) & (a > 0.5)).astype(np.uint8)
    ink = cv2.morphologyEx(ink, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    # volumen global: domo suave sobre toda la silueta
    pg = poisson(solid)
    g = np.sqrt(pg / (pg.max() + 1e-6))
    # cada zona entre lineas de tinta se abomba un poco (tablas, guantes, zapatillas)
    reg = (solid & (1 - ink)).astype(np.uint8)
    reg = cv2.morphologyEx(reg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    pl = poisson(reg, 120)
    n, lab = cv2.connectedComponents(reg)
    mx = np.zeros(n, np.float32); np.maximum.at(mx, lab.ravel(), pl.ravel())
    size = np.sqrt(mx[lab]); cap = np.sqrt(pl.max()) * 0.35
    loc = np.sqrt(np.clip(pl / (mx[lab] + 1e-6), 0, 1)) * np.minimum(size, cap) / (cap + 1e-6)
    h = 0.72 * g + 0.28 * loc * (reg > 0)
    h = cv2.GaussianBlur(h.astype(np.float32), (0, 0), W / 700)
    ink_s = cv2.GaussianBlur(ink.astype(np.float32), (0, 0), W / 1000)
    h = h - 0.02 * ink_s
    h = h * (a > 0.02)
    return h.astype(np.float32), ink_s


def shade(rgb, a, h, depth, light=(-0.55, -0.65, 0.55)):
    H, W = a.shape
    z = h * depth
    gy, gx = np.gradient(z)
    nx, ny, nz = -gx, -gy, np.ones_like(z)
    n = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2); nx, ny, nz = nx / n, ny / n, nz / n
    def lam(l):
        l = np.array(l, np.float32); l /= np.linalg.norm(l)
        return np.clip(nx * l[0] + ny * l[1] + nz * l[2], 0, 1), l
    key, lk = lam(light)
    fill, _ = lam((0.7, -0.1, 0.7))
    rim, _ = lam((0.85, 0.2, -0.15))
    # especular Blinn-Phong (vista frontal)
    hv = lk + np.array([0, 0, 1], np.float32); hv /= np.linalg.norm(hv)
    spec = np.clip(nx * hv[0] + ny * hv[1] + nz * hv[2], 0, 1)
    spec = 0.22 * spec ** 40 + 0.10 * spec ** 8          # satinado (resina pintada + barniz)
    fres = (1 - nz) ** 3
    # oclusion de cavidades
    blur = cv2.GaussianBlur(h, (0, 0), W / 120)
    ao = np.clip(1 - 2.0 * np.clip(blur - h, 0, 1), 0.45, 1)
    ao2 = np.clip(1 - 1.2 * np.clip(cv2.GaussianBlur(h, (0, 0), W / 40) - h, 0, 1), 0.6, 1)
    key = key ** 0.8                                         # luz envolvente, mas suave
    col = rgb * (0.42 * ao * ao2 + 0.62 * key * ao2 + 0.18 * fill)[..., None]
    col += (np.array([1.0, 0.95, 0.88]) * spec[..., None] * ao[..., None])
    col += np.array([0.80, 0.90, 1.0]) * (rim * fres * 0.28)[..., None]
    return np.clip(col, 0, 1)


def rotate_view(col, a, z, deg, ss=3):
    """gira la figura deg grados sobre el eje vertical: z-buffer por filas."""
    H, W = a.shape
    t = np.radians(deg); c, s = np.cos(t), np.sin(t)
    # superficie frontal + dorsal (espesor simetrico) ; muestreo denso en x
    xs = np.linspace(0, W - 1, W * ss)
    out = np.zeros((H, W, 3), np.float32); oa = np.zeros((H, W), np.float32); zb = np.full((H, W), -1e9, np.float32)
    cx = W / 2
    for side, sgn in ((1, 1.0), (0, -0.85)):
        X = np.broadcast_to(xs, (H, xs.size))
        zi = np.stack([np.interp(xs, np.arange(W), z[r]) for r in range(H)]) * sgn
        ai = np.stack([np.interp(xs, np.arange(W), a[r]) for r in range(H)])
        ci = np.stack([np.stack([np.interp(xs, np.arange(W), col[r, :, k]) for k in range(3)], -1) for r in range(H)])
        if side == 0: ci = ci * 0.55
        xp = (X - cx) * c + zi * s + cx
        dp = -(X - cx) * s + zi * c
        xi = np.clip(np.round(xp).astype(int), 0, W - 1)
        rr = np.broadcast_to(np.arange(H)[:, None], xi.shape)
        m = ai > 0.02
        idx = (rr[m] * W + xi[m]); d = dp[m]
        order = np.argsort(d)  # escribir de atras hacia adelante: el ultimo gana
        idx, d = idx[order], d[order]
        flat_c = out.reshape(-1, 3); flat_a = oa.reshape(-1); flat_z = zb.reshape(-1)
        cc = ci[m][order]; aa = ai[m][order]
        sel = d >= flat_z[idx] - 1e-3
        flat_c[idx[sel]] = cc[sel]; flat_a[idx[sel]] = np.maximum(flat_a[idx[sel]], aa[sel]); flat_z[idx[sel]] = d[sel]
    # rellenar huecos finos
    hole = (oa < 0.02).astype(np.uint8)
    fill = cv2.inpaint((out * 255).astype(np.uint8), cv2.dilate(hole, np.ones((1, 1))) & cv2.morphologyEx(1 - hole, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)), 3, cv2.INPAINT_TELEA)
    closed = cv2.morphologyEx((oa > 0.02).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    out = np.where(hole[..., None] & closed[..., None], fill / 255.0, out)
    oa = np.maximum(oa, closed.astype(np.float32) * (cv2.GaussianBlur(oa, (0, 0), 1.2) > 0.3))
    return out, oa


def render(pose='sentado_feliz', deg=0, height=1600):
    im = Image.open(f'{S}/quito/q_{pose}.png').convert('RGBA')
    im = im.crop(im.getbbox())
    pad = int(im.width * 0.12)
    can = Image.new('RGBA', (im.width + 2 * pad, im.height + pad), (0, 0, 0, 0)); can.paste(im, (pad, pad // 2))
    w = int(can.width * height / can.height); can = can.resize((w, height), Image.LANCZOS)
    x = np.array(can).astype(np.float32) / 255
    rgb, a = x[..., :3], x[..., 3]
    h, ink = height_map(rgb, a)
    depth = w * 0.16
    col = shade(rgb, a, h, depth)
    if deg:
        col, a = rotate_view(col, a, h * depth, deg)
    return col, a


if __name__ == '__main__':
    pose, out = sys.argv[1], sys.argv[2]
    deg = float(sys.argv[3]) if len(sys.argv) > 3 else 0
    hp = int(sys.argv[4]) if len(sys.argv) > 4 else 1600
    col, a = render(pose, deg, hp)
    img = np.dstack([col, a])
    Image.fromarray((np.clip(img, 0, 1) * 255 + .5).astype(np.uint8)).crop(Image.fromarray((a * 255).astype(np.uint8)).getbbox()).save(out)
    print('ok', out)
