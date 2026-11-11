import json, os, sys, hashlib, time, urllib.parse
import numpy as np
from PIL import Image
from extract import extract, render_bg, OLD, HERE

PROJ = r'C:/Users/Lauti/Documents/Tecnologia del Diseño - Campaña Bancala'
PZ = PROJ + '/02_Piezas'
LINKS = HERE + '/links'; os.makedirs(LINKS, exist_ok=True)
PREV = HERE + '/preview'; os.makedirs(PREV, exist_ok=True)
A3 = 841.89 / 1240; A4 = 595.28 / 1240

IG = PZ + '/01_Redes_Instagram'
IMP = PZ + '/02_Impresos'
ARQ = PZ + '/03_Arquigrafia_Estacion_Bancala'


def names(folder):
    return [os.path.splitext(f)[0] for f in sorted(os.listdir(folder)) if f.lower().endswith('.png')]


def pretty(stem):
    # 'Carrusel01_Slide02_Ficha' -> 'Slide 02 · Ficha'
    s = stem.replace('_', ' ')
    for pre in ['Carrusel01 ', 'Carrusel02 ', 'Carrusel03 ']: s = s.replace(pre, '')
    return s


DOCS = {
    'car1': dict(out=IG + '/Carrusel_01_Conoce_a_Quito/Carrusel_01_Conoce_a_Quito.ai', S=1,
                 pages=[(f'c1_{i}.html', 1080, 1350) for i in range(1, 6)], titles=names(IG + '/Carrusel_01_Conoce_a_Quito')),
    'car2': dict(out=IG + '/Carrusel_02_Te_banco_en_todas_menos_en_estas/Carrusel_02_Te_banco_en_todas_menos_en_estas.ai', S=1,
                 pages=[(f'c2_{i}.html', 1080, 1350) for i in range(1, 7)], titles=names(IG + '/Carrusel_02_Te_banco_en_todas_menos_en_estas')),
    'car3': dict(out=IG + '/Carrusel_03_La_misma_banca_distintas_historias/Carrusel_03_La_misma_banca_distintas_historias.ai', S=1,
                 pages=[(f'c3_{i}.html', 1080, 1350) for i in range(1, 7)], titles=names(IG + '/Carrusel_03_La_misma_banca_distintas_historias')),
    'hist': dict(out=IG + '/Historias_Instagram/Historias_Instagram.ai', S=1,
                 pages=[(f's{i}.html', 1080, 1920) for i in range(1, 8)], titles=names(IG + '/Historias_Instagram')),
    'dest': dict(out=IG + '/Portadas_Destacadas/Portadas_Destacadas.ai', S=1,
                 pages=[(f'h{i}.html', 1080, 1080) for i in range(6)], titles=names(IG + '/Portadas_Destacadas')),
    'post': dict(out=IG + '/Posteos/Posteos.ai', S=1,
                 pages=[(f'post{i}.html', 1080, 1350) for i in range(1, 5)], titles=names(IG + '/Posteos')),
    'afiches': dict(out=IMP + '/Afiches_A3_Serie_Te_banco_en_todas/Afiches_A3_Serie_Te_banco_en_todas.ai', S=A3,
                    pages=[(n + '.html', 1240, 1754) for n in names(IMP + '/Afiches_A3_Serie_Te_banco_en_todas')], titles=names(IMP + '/Afiches_A3_Serie_Te_banco_en_todas')),
    'info': dict(out=IMP + '/Infografia_A3/Infografia_A3_La_misma_banca_distintas_historias.ai', S=A3,
                 pages=[('info.html', 1240, 1754)], titles=['Infografia A3']),
    'stk': dict(out=IMP + '/Stickers/Stickers_Plancha_A4.ai', S=A4, pages=[('stk.html', 1240, 1754)], titles=['Plancha A4'], troquel=True),
    'plano': dict(out=ARQ + '/00_Plano_Estacion_Bancala.ai', S=1, pages=[('plano.html', 1600, 1000)], titles=['Plano Estacion Bancala']),
    'panel': dict(out=ARQ + '/01_Panel_Refugio_Rojo/Panel_Refugio_Rojo.ai', S=1, pages=[('panel.html', 838, 1256)], titles=['Panel Arte Final'],
                  mock=ARQ + '/01_Panel_Refugio_Rojo/Panel_Refugio_Mockup.jpg'),
    'corp': dict(out=ARQ + '/02_Corporeo_Quito/Corporeo_Quito.ai', S=1, pages=[], titles=[], corporeo=True,
                 mock=ARQ + '/02_Corporeo_Quito/Corporeo_Quito_Mockup.jpg'),
    'piso': dict(out=ARQ + '/03_Vinilo_de_Piso/Vinilo_de_Piso.ai', S=1, pages=[('piso.html', 1600, 700)], titles=['Vinilo Piso Arte Final'],
                 mock=ARQ + '/03_Vinilo_de_Piso/Vinilo_Piso_Mockup.jpg'),
    'mesa': dict(out=ARQ + '/04_Mesa_Muro_de_Historias/Mesa_Muro_de_Historias.ai', S=1, pages=[('mesa.html', 1800, 800)], titles=['Tablero Arte Final'],
                 mock=ARQ + '/04_Mesa_Muro_de_Historias/Mesa_Vinilo_Tablero_Mockup.jpg'),
    'placa': dict(out=ARQ + '/05_Placa_Bancos_Existentes/Placa_Bancos_Existentes.ai', S=1, pages=[('placa.html', 1200, 420)], titles=['Placa Arte Final'],
                  mock=ARQ + '/05_Placa_Bancos_Existentes/Placa_Banco_Mockup.jpg'),
}


def local(src):
    p = urllib.parse.unquote(src.replace('file:///', ''))
    return p


def mask_alpha(g, h):
    """vertical alpha profile (css mask linear-gradient) over h px; angle 180 = top->bottom"""
    st = g['stops']; ys = np.linspace(0, 100, h)
    a = np.interp(ys, [s['p'] for s in st], [s['c'][3] for s in st])
    if g['angle'] == 0: a = a[::-1]
    return a


from fontTools.ttLib import TTFont
FD = 'C:/Users/Lauti/AppData/Local/Microsoft/Windows/Fonts/'
CMAP = {'Titan': set(TTFont(FD + 'TitanOne-Regular.ttf').getBestCmap()), 'Brico': set(TTFont(FD + 'BricolageGrotesque-Bold.ttf').getBestCmap())}


def glyph_fallback(t):
    # split runs where the brand font lacks a glyph (Chrome silently used a system font there)
    for ln in t['lines']:
        out = []
        for r in ln['runs']:
            cm = CMAP[r['st']['f']]; cur = None
            for ch in r['t']:
                sym = ord(ch) not in cm and ch != ' '
                if cur is None or cur['_s'] != sym:
                    cur = dict(r, t='', _s=sym); cur['st'] = dict(r['st'], f='Sym') if sym else r['st']; out.append(cur)
                cur['t'] += ch
        for o in out: o.pop('_s', None)
        ln['runs'] = out


def blank_lines(t):
    L = t['lines']
    gaps = [L[i]['bl'] - L[i - 1]['bl'] for i in range(1, len(L))]
    lead = t.get('lh') or (min(gaps) if gaps else None)
    if not lead: return
    t['lead'] = lead
    out = [L[0]]
    for i in range(1, len(L)):
        n = round((L[i]['bl'] - L[i - 1]['bl']) / lead) - 1
        for j in range(max(0, n)):
            out.append(dict(bl=L[i - 1]['bl'] + lead * (j + 1), x0=L[i]['x0'], x1=L[i]['x0'], runs=[], br=-1000 - i * 10 - j))
        out.append(L[i])
    t['lines'] = out


def prep(items, base):
    for it in items:
        k = it['k']
        if k == 't': glyph_fallback(it); blank_lines(it)
        if k == 'g': prep(it['ch'], base); continue
        if k == 'img':
            src = local(it['src']); it['file'] = src
            if it.get('mask'):
                im = Image.open(src).convert('RGBA'); w, h = im.size
                # mask is defined over the element box; place == box for these plates
                a = mask_alpha(it['mask'], h)
                al = np.array(im)[..., 3].astype(np.float32) * a[:, None]
                arr = np.array(im); arr[..., 3] = al.astype(np.uint8)
                out = f"{LINKS}/{os.path.splitext(os.path.basename(src))[0]}_fundido.png"
                Image.fromarray(arr).save(out, optimize=False, compress_level=6)
                it['file'] = out; it['name'] = 'Foto de fondo (con fundido)'
            else:
                it['name'] = nice_img(src)
        elif k == 'ras':
            out = f"{LINKS}/{base}_{it['id']}.png"
            render_bg(RAS[it['id']], out, scale=2)
            it['file'] = out; it['place'] = dict(x=it['x'], y=it['y'], w=it['w'], h=it['h']); it['clip'] = None
        elif k == 'svg':
            out = f"{LINKS}/{base}_{hashlib.md5(it['svg'].encode()).hexdigest()[:8]}.svg"
            open(out, 'w', encoding='utf8').write(it['svg'])
            it['file'] = out; it['place'] = dict(x=it['x'], y=it['y'], w=it['w'], h=it['h']); it['clip'] = None


def nice_img(src):
    b = os.path.basename(src)
    m = {'bancala_blanco.svg': 'Logo Bancala blanco', 'bancala_color.svg': 'Logo Bancala color', 'ucasal_blanco.svg': 'Logo UCASAL blanco',
         'ucasal_color.svg': 'Logo UCASAL color', 'ucasal_sustentable_blanco.png': 'Logo UCASAL Sustentable blanco',
         'ucasal_sustentable_color.png': 'Logo UCASAL Sustentable color', 'qr_banco.svg': 'Código QR'}
    if b in m: return m[b]
    if b.startswith('q_'): return 'Quito ' + b[2:-4].replace('_', ' ')
    if b.startswith('st_'): return 'Sticker Quito ' + b[3:-4].replace('_', ' ')
    if b.endswith('_fg.png'): return 'Recorte primer plano (personas + Quito)'
    if '_bg' in b: return 'Foto de fondo'
    return 'Imagen ' + b


RAS = {}


def troquel_items(png, x, y, h, rot=0, s_px=None):
    """die-cut contour of a sticker PNG -> polygon in page px (handles rotation about centre)"""
    import cv2
    im = Image.open(png).convert('RGBA'); a = np.array(im)[..., 3]
    cs, _ = cv2.findContours((a > 8).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)
    c = cv2.approxPolyDP(c, 1.2, True)[:, 0, :].astype(float)
    sc = h / im.size[1]; w = im.size[0] * sc
    pts = c * sc + [x, y]
    if rot:
        cx, cy = x + w / 2, y + h / 2; t = np.radians(rot)
        R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
        pts = (pts - [cx, cy]) @ R.T + [cx, cy]
    return pts.round(2).tolist()


def build_doc(key, png=True, keep=False):
    D = DOCS[key]; pages = []
    base = key
    for i, (html, w, h) in enumerate(D['pages']):
        d = extract(html, w=w, h=h)
        for r in d['raster']: RAS[r['id']] = r
        pg = d['pages'][0]
        # make raster ids unique per page
        def ren(items):
            for it in items:
                if it['k'] == 'g': ren(it['ch'])
                if it['k'] == 'ras': it['id'] = it['id']
        prep(pg['items'], f'{base}{i}')
        pages.append(dict(name=pretty(D['titles'][i]), w=pg['w'], h=pg['h'], items=pg['items'], src=html))
        RAS.clear()
    if D.get('corporeo'):
        st = OLD + '/stickers/st_sentado_feliz.png'; im = Image.open(st); W, H = im.size
        pages.append(dict(name='Corpóreo Arte Final', w=W, h=H, items=[
            dict(k='img', file=st, name='Quito sentado feliz (con borde blanco)', place=dict(x=0, y=0, w=W, h=H), clip=None),
            dict(k='poly', pts=troquel_items(st, 0, 0, H), name='Troquel (línea de corte)')]))
    if D.get('troquel'):
        # sticker positions as in p_print.stickers_sheet
        items = [('saludo', 90, 250, 420, -5), ('enojado', 600, 230, 380, 6), ('sentado_feliz', 140, 720, 400, 4), ('tapandose', 640, 690, 380, -4), ('llorando', 110, 1180, 380, -6), ('limpiando', 650, 1160, 380, 5)]
        pages[0]['troquel'] = [dict(k='poly', pts=troquel_items(OLD + f'/stickers/st_{p}.png', x, y, h, r), name=f'Troquel {p.replace("_", " ")}') for p, x, y, h, r in items]
    if D.get('mock'):
        im = Image.open(D['mock']); W, H = im.size; f = 1600 / max(W, H)
        pages.append(dict(name='Mockup (referencia)', w=W * f, h=H * f, items=[
            dict(k='img', file=D['mock'], name='Mockup fotográfico', place=dict(x=0, y=0, w=W * f, h=H * f), clip=None)]))
    doc = dict(name=key, out=D['out'], S=D['S'], pages=pages, png=PREV if png else None, base=key, keepOpen=keep, pngScale=100 / D['S'] if D['S'] < 1 else 100)
    js = HERE + f'/run_{key}.jsx'
    open(js, 'w', encoding='utf-8-sig').write('var DOC=' + json.dumps(doc, ensure_ascii=False) + ';\n' + open(HERE + '/builder.jsx', encoding='utf8').read())
    return js


def run(js):
    import win32com.client
    ai = win32com.client.Dispatch('Illustrator.Application')
    t = time.time(); r = ai.DoJavaScriptFile(js)
    print(os.path.basename(js), '%.0fs' % (time.time() - t), '\n', r, flush=True)


if __name__ == '__main__':
    for k in sys.argv[1:]:
        js = build_doc(k); run(js)
