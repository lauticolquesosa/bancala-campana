"""Mapas de relieve (alto) de cada pose de Quito para la figura 2.5D del sitio.
Usa el mismo inflado por regiones que el Quito 3D del stand (Presentacion/07_Fuente_Produccion/quito3d.py).
uso: python source/build_depth.py   (desde "Pagina Web", después de build_assets.py)"""
import os, sys, glob, json
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(WEB), 'Presentacion', '07_Fuente_Produccion'))
from quito3d import height_map  # noqa: E402

OUT = os.path.join(WEB, 'img', 'quito', 'depth'); os.makedirs(OUT, exist_ok=True)
meta = {}
for f in sorted(glob.glob(os.path.join(WEB, 'img', 'quito', '*.webp'))):
    key = os.path.splitext(os.path.basename(f))[0]
    im = Image.open(f).convert('RGBA')
    arr = np.asarray(im).astype(np.float32) / 255
    h, _ = height_map(arr[..., :3], arr[..., 3])
    h = h / (h.max() + 1e-6)
    d = Image.fromarray((np.clip(h, 0, 1) * 255).astype(np.uint8), 'L')
    d = d.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    d.save(os.path.join(OUT, key + '.png'), optimize=True)
    meta[key] = [im.width, im.height]
    print(key, im.size)
json.dump(meta, open(os.path.join(WEB, 'data', 'quito.json'), 'w'), indent=0)

# versiones en alta (texturas de la figura 2.5D)
import re, unicodedata
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
SRC = os.path.join(os.path.dirname(WEB), 'Presentacion', '04_Recursos', 'Personaje_Quito', 'Poses_PNG_transparente')
HD = os.path.join(WEB, 'img', 'quito', 'hd'); os.makedirs(HD, exist_ok=True)
for f in sorted(glob.glob(SRC + '/**/*.png', recursive=True)):
    rel = os.path.relpath(f, SRC); sub = os.path.dirname(rel)
    key = slug((sub + '-' if sub else '') + os.path.splitext(os.path.basename(f))[0].replace('Quito_', ''))
    im = Image.open(f).convert('RGBA')
    bb = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox(); im = im.crop(bb)
    if im.width > 1300: im = im.resize((1300, round(im.height * 1300 / im.width)), Image.LANCZOS)
    im.save(os.path.join(HD, key + '.webp'), 'WEBP', quality=86, method=6)
