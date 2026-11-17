"""Stand · recorte de la estatua de Quito en tamano real (foto de producto).
1) mascara base con IA (rembg isnet-general-use), 2) se rellenan los huecos falsos (logos blancos,
cordones) y se conservan solo los huecos reales entre piernas, 3) trimapa angosta + matting de forma
cerrada (pymatting) para un borde antialiasado limpio, 4) descontaminacion del color del borde.
uso: python cut_quito_real.py <foto.png>"""
import os, sys, numpy as np, cv2
from PIL import Image
from rembg import remove, new_session
from pymatting import estimate_alpha_cf, estimate_foreground_ml
S = os.path.dirname(os.path.abspath(__file__)); OUT = S + '/art/stand'

src = sys.argv[1] if len(sys.argv) > 1 else OUT + '/real/quito_real_original.png'
im = Image.open(src).convert('RGB'); rgb = np.array(im)
a = np.array(remove(im, session=new_session('isnet-general-use')))[..., 3]
H, W = a.shape
m = (a > 128).astype(np.uint8)
# huecos interiores: solo se dejan los reales (fondo visto entre las piernas, > 400 px)
n, l, st, _ = cv2.connectedComponentsWithStats(1 - m, connectivity=4)
for i in range(1, n):
    x, y, w, h, ar = st[i]
    border = x == 0 or y == 0 or x + w >= W or y + h >= H
    if not border and ar < 400: m[l == i] = 1
# huecos que la IA dejo con velo: fondo gris (poco saturado) entre el brazo del mate y el respaldo
sat = rgb.max(2).astype(int) - rgb.min(2)
for (sx, sy), (x0, y0, x1, y1) in [((230, 460), (150, 380, 300, 530))]:
    roi = np.zeros((H, W), np.uint8); roi[y0:y1, x0:x1] = (sat[y0:y1, x0:x1] < 38).astype(np.uint8)
    roi = cv2.morphologyEx(roi, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    _, lr = cv2.connectedComponents(roi, connectivity=4)
    if lr[sy, sx]: m[lr == lr[sy, sx]] = 0
# islas sueltas fuera de la figura
n, l, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
big = 1 + np.argmax(st[1:, 4]); m = (l == big).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
# trimapa: banda de duda de ~5 px a cada lado del contorno
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
fg = cv2.erode(m, k); bg = 1 - cv2.dilate(m, k)
tri = np.full((H, W), 0.5); tri[fg == 1] = 1; tri[bg == 1] = 0
img = rgb.astype(np.float64) / 255
al = estimate_alpha_cf(img, tri)
al = np.clip((al - 0.04) / 0.92, 0, 1)                 # sin velos casi transparentes
al[fg == 1] = 1; al[bg == 1] = 0
F = estimate_foreground_ml(img, al)                    # color del borde sin el gris del taller
out = np.dstack([np.clip(F, 0, 1) * 255, al * 255]).round().astype(np.uint8)
o = Image.fromarray(out, 'RGBA'); o = o.crop(o.getbbox())
o.save(OUT + '/quito_real_recorte.png'); print('ok', o.size)
