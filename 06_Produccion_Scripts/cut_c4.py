"""Carrusel 04 · recorte de las 8 ilustraciones nuevas de Quito.
Vinieron como JPEG: 6 con tablero de ajedrez *dibujado* (falsa transparencia) y 2 con fondo negro.
Quita el fondo conectado al borde y tambien los huecos interiores (entre patas, bajo el asiento),
conserva las marcas de emocion (vapor, enojo, destellos) y guarda PNG transparentes recortados.
uso: python cut_c4.py <carpeta_con_los_jpeg>"""
import os, sys, glob, numpy as np, cv2
from PIL import Image
S = os.path.dirname(os.path.abspath(__file__)); OUT = S + '/quito'

# archivo (sufijo del nombre de WhatsApp) -> pose del brief
MAP = {'19.29.34.jpeg': 'c4_1_despertando', '19.29.34 (1).jpeg': 'c4_2_animando', '19.29.34 (2).jpeg': 'c4_3_mate',
       '19.29.34 (3).jpeg': 'c4_4_basura', '19.29.34 (4).jpeg': 'c4_5_enojado', '19.29.35.jpeg': 'c4_6_indignado',
       '19.29.35 (1).jpeg': 'c4_7_emocionado', '19.29.35 (2).jpeg': 'c4_8_saludo'}


def cut(rgb):
    a = rgb.astype(np.int16); mx = a.max(2); mn = a.min(2); H, W = mx.shape
    dark_bg = np.median(np.concatenate([mx[0], mx[-1], mx[:, 0], mx[:, -1]])) < 60
    if dark_bg:
        cand = mx < 40
    else:
        cand = ((mx - mn) < 14) & (mx > 200)
    n, lab, st, _ = cv2.connectedComponentsWithStats(cand.astype(np.uint8), connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border))
    for i in range(1, n):  # huecos interiores
        if i in border or st[i, 4] < 350: continue
        m = lab == i
        if dark_bg:
            if st[i, 4] > 2500: bg |= m           # pupilas y detalles chicos se quedan
        else:
            v = mx[m]; hi = (v > 245).mean(); mid = ((v > 212) & (v < 238)).mean()
            if hi > .15 and mid > .15: bg |= m    # patron de tablero, no guantes ni suelas
    fg = ~bg
    n2, l2, st2, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), connectivity=8)
    big = st2[1:, 4].max(); keep = np.zeros(n2, bool)
    keep[1:] = st2[1:, 4] > big * 0.0015
    fg = keep[l2]
    if dark_bg:
        # el contorno negro del dibujo se confunde con el fondo: devolverle un anillo de contorno
        fg = cv2.dilate(fg.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    else:
        # comer 1 px de fringe claro del tablero
        fg = cv2.erode(fg.astype(np.uint8), np.ones((3, 3), np.uint8), 1)
    al = cv2.GaussianBlur(fg.astype(np.float32), (0, 0), 0.7)
    al = np.clip((al - 0.2) / 0.6, 0, 1)
    return (al * 255).astype(np.uint8)


if __name__ == '__main__':
    src = sys.argv[1]
    for f in sorted(glob.glob(src + '/*.jpeg')):
        key = next((k for k in MAP if f.endswith('at ' + k)), None)
        if not key: continue
        rgb = np.array(Image.open(f).convert('RGB'))
        al = cut(rgb)
        im = Image.fromarray(np.dstack([rgb, al])); im = im.crop(im.getbbox())
        im.save(f'{OUT}/q_{MAP[key]}.png'); print(MAP[key], im.size)
