"""Figura 3D de Quito sobre base cilindrica: foto de producto de estudio + recorte transparente.
salidas: art/stand/figura_render.png (con fondo), art/stand/figura_recorte.png (transparente)"""
import os, sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
from quito3d import render
OUT = S + '/art/stand'; os.makedirs(OUT, exist_ok=True)

N = 3000
NAVY = np.array([27, 77, 139]) / 255; MINT = np.array([122, 226, 166]) / 255
INK = np.array([58, 29, 12]) / 255


def sstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t)


def logo_png(h=260):
    """logo Bancala blanco rasterizado (via Chromium, respeta el svg)."""
    p = OUT + '/_logo.png'
    if not os.path.exists(p):
        from playwright.sync_api import sync_playwright
        svg = open(S + '/brand/bancala_blanco.svg', encoding='utf8').read()
        with sync_playwright() as pw:
            b = pw.chromium.launch(); pg = b.new_page(device_scale_factor=4)
            pg.set_content(f'<html><body style="margin:0;background:transparent"><div id="x" style="display:inline-block;height:{h}px">{svg}</div><style>svg{{height:{h}px;width:auto;display:block}}</style></body></html>')
            pg.locator('#x').screenshot(path=p, omit_background=True); b.close()
    return np.array(Image.open(p).convert('RGBA')).astype(np.float32) / 255


def pedestal(img, alpha_total, cx, cyT, rx, ry, hgt, col, logo):
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (xx - cx) / rx
    inside_x = np.abs(u) < 1
    arc = ry * np.sqrt(np.clip(1 - u ** 2, 0, 1))
    ytop = cyT + arc; ybot = cyT + hgt + arc
    # ---- lateral
    cov = sstep(-1, 1, (1 - np.abs(u)) * rx) * sstep(-1, 1, ybot - yy) * sstep(-1, 1, yy - (cyT - arc))
    th = np.arcsin(np.clip(u, -1, 1))
    nx, nz = np.sin(th), np.cos(th)
    L = np.array([-0.55, -0.25, 0.80]); L /= np.linalg.norm(L)
    dif = np.clip(nx * L[0] + nz * L[2], 0, 1)
    hv = L + np.array([0, 0, 1.0]); hv /= np.linalg.norm(hv)
    spec = np.clip(nx * hv[0] + nz * hv[2], 0, 1) ** 30 * 0.35
    vgrad = 1 - 0.18 * np.clip((yy - ytop) / hgt, 0, 1)        # mas oscuro abajo (rebote del piso)
    side = col * (0.28 + 0.78 * dif)[..., None] * vgrad[..., None] + spec[..., None]
    # logo envuelto en el cilindro
    lh, lw = logo.shape[:2]
    sc = hgt * 0.50 / lh                                         # alto del logo = 50 % de la banda
    tx = rx * th / sc + lw / 2                                   # longitud de arco -> envuelve el cilindro
    ty = ((yy - ytop) - hgt / 2) / sc + lh / 2
    m = (ty >= 0) & (ty < lh - 1) & (tx >= 0) & (tx < lw - 1)
    la = np.zeros((H, W), np.float32)
    la[m] = cv2.remap(logo[..., 3], tx.astype(np.float32), ty.astype(np.float32), cv2.INTER_LINEAR)[m]
    la *= np.clip(np.cos(th) * 1.4, 0, 1)
    side = side * (1 - la[..., None]) + np.array([0.97, 0.97, 0.95]) * (0.55 + 0.5 * dif)[..., None] * la[..., None]
    side_cov = cov * (yy > cyT - ry)
    img[:] = img * (1 - side_cov[..., None]) + side * side_cov[..., None]
    # ---- tapa superior
    e = ((xx - cx) / rx) ** 2 + ((yy - cyT) / ry) ** 2
    topc = sstep(-0.004, 0.004, 1 - e)
    tg = 1.06 - 0.10 * (xx - cx) / rx - 0.06 * (yy - cyT) / ry
    top = col * 1.05 * tg[..., None]
    # bisel claro en el borde
    rim = sstep(0.90, 0.985, e) * (1 - sstep(0.985, 1.0, e))
    top = top + rim[..., None] * 0.18
    img[:] = img * (1 - topc[..., None]) + top * topc[..., None]
    alpha_total[:] = np.maximum(alpha_total, np.maximum(side_cov, topc))
    return topc


def main():
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
    # fondo de estudio: barrido crema con halo menta detras de la figura
    t = yy / N
    bg = np.array([0.965, 0.945, 0.905])[None, None] * (1 - 0.10 * t)[..., None]
    halo = np.exp(-(((xx - N / 2) / (N * 0.42)) ** 2 + ((yy - N * 0.42) / (N * 0.40)) ** 2))
    bg = bg * (1 - 0.35 * halo[..., None]) + (MINT * 0.95 + 0.05) * 0.35 * halo[..., None]
    floor = sstep(N * 0.70, N * 0.86, yy)
    bg = bg * (1 - 0.08 * floor[..., None])
    img = bg.astype(np.float32).copy()
    acc = np.zeros((N, N), np.float32)                          # alfa del recorte (base + figura + sombra)

    cx, cyT, rx, ry, hgt = N / 2, N * 0.705, N * 0.33, N * 0.105, N * 0.075
    # sombra de la base en el piso
    sh = np.zeros((N, N), np.float32)
    cv2.ellipse(sh, (int(cx + rx * 0.10), int(cyT + hgt + ry * 0.55)), (int(rx * 1.12), int(ry * 1.25)), 0, 0, 360, 1, -1)
    sh = cv2.GaussianBlur(sh, (0, 0), N * 0.022) * 0.55
    sh2 = np.zeros((N, N), np.float32)
    cv2.ellipse(sh2, (int(cx), int(cyT + hgt + ry * 0.2)), (int(rx * 1.0), int(ry * 1.0)), 0, 0, 360, 1, -1)
    sh2 = cv2.GaussianBlur(sh2, (0, 0), N * 0.006) * 0.55
    shadow = np.clip(sh + sh2, 0, 0.85)
    img *= (1 - shadow[..., None] * np.array([0.62, 0.60, 0.55]))
    acc = np.maximum(acc, shadow)

    logo = logo_png()
    topc = pedestal(img, acc, cx, cyT, rx, ry, hgt, NAVY * 1.05, logo)

    # figura
    col, a = render('sentado_feliz', 0, 1900)
    ys, xs = np.where(a > 0.05); col = col[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    fh, fw = a.shape
    # las patas traseras del banco (76 % del alto) apoyan atras en la tapa; las zapatillas adelante
    fx = int(cx - fw / 2 + fw * 0.03); fy = int(cyT - ry * 0.50 - fh * 0.76)
    A = np.zeros((N, N), np.float32); C = np.zeros((N, N, 3), np.float32)
    A[fy:fy + fh, fx:fx + fw] = a; C[fy:fy + fh, fx:fx + fw] = col
    # sombras de contacto: punto mas bajo de cada columna de la mitad inferior de la figura
    cs = np.zeros((N, N), np.float32)
    low = np.where(A[::-1].argmax(0) > 0, N - 1 - A[::-1].argmax(0), -1)
    for x in range(N):
        y = low[x]
        if y > fy + fh * 0.6 and A[y, x] > 0.3: cs[min(N - 1, y + 4), x] = 1
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(N * 0.03), int(N * 0.012)))
    cs = cv2.GaussianBlur(cv2.dilate(cs, k), (0, 0), N * 0.006)
    amb = np.zeros((N, N), np.float32)
    cv2.ellipse(amb, (int(cx + fw * 0.05), int(cyT - ry * 0.05)), (int(fw * 0.40), int(ry * 0.55)), 0, 0, 360, 1, -1)
    amb = cv2.GaussianBlur(amb, (0, 0), N * 0.025)
    cs = np.clip(cs * 1.0 + amb * 0.55, 0, 0.9) * topc
    img *= (1 - cs[..., None] * np.array([0.72, 0.72, 0.66]))
    # oclusion bajo las patas
    occ = cv2.GaussianBlur(A, (0, 0), N * 0.004) * topc * (1 - A)
    img *= (1 - 0.45 * occ[..., None])
    img = img * (1 - A[..., None]) + C * A[..., None]
    acc = np.maximum(acc, A)

    # acabado: vineta suave
    r = np.sqrt(((xx - N / 2) / (N / 2)) ** 2 + ((yy - N / 2) / (N / 2)) ** 2)
    final = img * (1 - 0.10 * np.clip(r - 0.6, 0, 1))[..., None]
    Image.fromarray((np.clip(final, 0, 1) * 255 + .5).astype(np.uint8)).save(OUT + '/figura_render.png')
    # recorte: figura + base + sombras (sobre transparente, premultiplicado por fondo neutro)
    cut = np.dstack([np.clip(img / np.maximum(1e-3, 1), 0, 1), acc])
    # en zonas de sombra pura, color negro tintado con alfa = sombra
    solid = np.maximum(A, np.maximum(topc, (acc > 0.99).astype(np.float32)))
    rgb = np.where(solid[..., None] > 0.5, img, np.array([0.18, 0.14, 0.10]))
    cut = np.dstack([rgb, acc])
    bb = Image.fromarray((acc * 255).astype(np.uint8)).getbbox()
    Image.fromarray((np.clip(cut, 0, 1) * 255 + .5).astype(np.uint8)).crop(bb).save(OUT + '/figura_recorte.png')
    print('ok', OUT)


if __name__ == '__main__':
    main()
