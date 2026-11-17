"""Versión intermedia (-md, 900 px) de cada pieza para srcset y agrega 'md' a data/piezas.json.
uso: python source/build_md.py  (desde "Pagina Web", después de build_assets.py)"""
import os, json
from PIL import Image
WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = json.load(open(os.path.join(WEB, 'data', 'piezas.json'), encoding='utf8'))
for p in m['piezas']:
    src = os.path.join(WEB, p['src'].lstrip('/'))
    md = p['src'].replace('.webp', '-md.webp')
    im = Image.open(src)
    if im.width > 1000:
        im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS).save(os.path.join(WEB, md.lstrip('/')), 'WEBP', quality=78, method=6)
        p['md'] = md
    else:
        p['md'] = p['src']
json.dump(m, open(os.path.join(WEB, 'data', 'piezas.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print(sum(1 for p in m['piezas'] if p['md'] != p['src']), 'md generadas')
