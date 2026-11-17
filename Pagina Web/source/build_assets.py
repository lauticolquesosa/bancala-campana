"""Genera las imágenes del sitio (WebP optimizado) a partir de ../Presentacion y el manifiesto data/piezas.json.
uso: python source/build_assets.py   (desde la carpeta "Pagina Web")"""
import os, re, json, glob, shutil, unicodedata
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.dirname(HERE)
P = os.path.join(os.path.dirname(WEB), 'Presentacion')
IMG = os.path.join(WEB, 'img')


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def save(src, dst, w, q=82, alpha=None):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im = Image.open(src)
    has_a = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    if alpha is False:
        has_a = False
    im = im.convert('RGBA' if has_a else 'RGB')
    if has_a:  # recorta el margen transparente
        bb = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
        if bb:
            im = im.crop(bb)
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=q, method=6)
    return im.size


man = {}

# ---- Quito: poses, stickers y figura 3D ----
poses = []
for f in sorted(glob.glob(P + '/04_Recursos/Personaje_Quito/Poses_PNG_transparente/**/*.png', recursive=True)):
    rel = os.path.relpath(f, P + '/04_Recursos/Personaje_Quito/Poses_PNG_transparente')
    name = os.path.splitext(os.path.basename(f))[0].replace('Quito_', '')
    sub = os.path.dirname(rel)
    key = slug((sub + '-' if sub else '') + name)
    w, h = save(f, f'{IMG}/quito/{key}.webp', 760, 84)
    poses.append(dict(src=f'/img/quito/{key}.webp', name=name.replace('_', ' '), w=w, h=h))
man['poses'] = poses

stk = []
for f in sorted(glob.glob(P + '/04_Recursos/Personaje_Quito/Stickers_troquelados/*.png')):
    name = os.path.splitext(os.path.basename(f))[0].replace('Sticker_Quito_', '')
    w, h = save(f, f'{IMG}/stickers/{slug(name)}.webp', 420, 85)
    stk.append(dict(src=f'/img/stickers/{slug(name)}.webp', name=name.replace('_', ' '), w=w, h=h))
man['stickers'] = stk

# ---- marca ----
os.makedirs(f'{IMG}/brand', exist_ok=True)
for a, b in [('Logo_Bancala_Blanco.svg', 'bancala-blanco.svg'), ('Logo_Bancala_Color.svg', 'bancala-color.svg'),
             ('Logo_Ucasal_Blanco.svg', 'ucasal-blanco.svg'), ('Logo_Ucasal_Color.svg', 'ucasal-color.svg')]:
    shutil.copy(P + '/04_Recursos/Logos/' + a, f'{IMG}/brand/{b}')
save(P + '/04_Recursos/Logos/Logo_Ucasal_Sustentable_Blanco.png', f'{IMG}/brand/ucasal-sustentable-blanco.webp', 600, 90)
save(P + '/04_Recursos/Logos/Logo_Ucasal_Sustentable_Color.png', f'{IMG}/brand/ucasal-sustentable-color.webp', 600, 90)
save(P + '/04_Recursos/Tramas/Trama_blanca_limpia.png', f'{IMG}/brand/trama-blanca.webp', 1100, 80)
save(P + '/04_Recursos/Tramas/Trama_negra_limpia.png', f'{IMG}/brand/trama-negra.webp', 1100, 80)

# ---- fotos del campus (look Bancala) ----
campus = []
for f in sorted(glob.glob(P + '/04_Recursos/Fotos_Campus/Editadas_Look_Bancala/*.jpg')):
    n = re.search(r'(\d+)', os.path.basename(f)).group(1)
    w, h = save(f, f'{IMG}/campus/campus-{n}.webp', 960, 78)
    save(f, f'{IMG}/campus/campus-{n}-sm.webp', 480, 74)
    campus.append(dict(src=f'/img/campus/campus-{n}.webp', sm=f'/img/campus/campus-{n}-sm.webp', w=w, h=h))
man['campus'] = campus
# antes / después del look
save(P + '/04_Recursos/Fotos_Campus/Originales/Campus_12.jpeg', f'{IMG}/campus/antes-12.webp', 960, 78)

# ---- piezas ----
PZ = P + '/02_Piezas'
CATS = [
    ('01_Redes_Instagram/Posteos', 'redes', 'Posteos'),
    ('01_Redes_Instagram/Carrusel_01_Conoce_a_Quito', 'redes', 'Carrusel 01 · Conocé a Quito'),
    ('01_Redes_Instagram/Carrusel_02_Te_banco_en_todas_menos_en_estas', 'redes', 'Carrusel 02 · Te banco en todas. Menos en estas'),
    ('01_Redes_Instagram/Carrusel_03_La_misma_banca_distintas_historias', 'redes', 'Carrusel 03 · La misma banca, distintas historias'),
    ('01_Redes_Instagram/Carrusel_04_Un_dia_en_la_vida_de_Quito', 'redes', 'Carrusel 04 · Un día en la vida de Quito'),
    ('01_Redes_Instagram/Historias_Instagram', 'historias', 'Historias'),
    ('01_Redes_Instagram/Portadas_Destacadas', 'historias', 'Destacadas'),
    ('01_Redes_Instagram/Foto_de_perfil', 'redes', 'Foto de perfil'),
    ('02_Impresos/Afiches_A3_Serie_Te_banco_en_todas', 'impresos', 'Afiches A3'),
    ('02_Impresos/Infografia_A3', 'impresos', 'Infografía A3'),
    ('02_Impresos/Stickers', 'impresos', 'Stickers'),
    ('03_Arquigrafia_Estacion_Bancala/01_Panel_Refugio_Rojo', 'arquigrafia', 'Panel del refugio'),
    ('03_Arquigrafia_Estacion_Bancala/02_Mesa_Muro_de_Historias', 'arquigrafia', 'Mesa · Muro de historias'),
    ('03_Arquigrafia_Estacion_Bancala/03_Placa_Bancos_Existentes', 'arquigrafia', 'Placa de los bancos'),
    ('04_Stand_Bancala', 'stand', 'Stand Bancala'),
]
TITLE_FIX = {'Tamano': 'tamaño', 'tamano': 'tamaño', 'Dia': 'día', 'dia': 'día', 'Conoce': 'Conocé', 'Infografia': 'Infografía',
             'Peluqueria': 'Peluquería', 'peluqueria': 'peluquería', 'moves': 'movés', 'Estacion': 'Estación', 'Presentacion': 'Presentación',
             'compu': 'compu', 'Musica': 'Música', 'regresiva': 'regresiva', 'esc': 'esc.'}


def nice(stem):
    s = stem
    s = re.sub(r'^(Carrusel_04_Un_dia_en_la_vida_de_Quito_|Carrusel0\d_|Stand_Bancala_|Historia_|Destacada_|Post_|Afiche_)', '', s)
    if re.match(r'^Slide\d', s):
        s = re.sub(r'^Slide0?(\d+)_', r'\1 · ', s)
    else:
        s = re.sub(r'^0?(\d+)[ _]', r'\1 · ', s)
    s = s.replace('_', ' ').replace('  ', ' ')
    s = s.replace(' (referencia)', '').replace('Panel Refugio Rojo Panel', 'Panel del refugio ·').replace('Panel Refugio Rojo Mockup', 'Panel del refugio · Mockup')
    s = re.sub(r'(\d\d)-(\d\d)', r'\1:\2', s)
    s = ' '.join(TITLE_FIX.get(w, w) for w in s.split(' '))
    return s.strip()


pieces = []
for folder, cat, group in CATS:
    files = sorted([f for f in glob.glob(f'{PZ}/{folder}/*') if f.lower().endswith(('.png', '.jpg'))])
    for f in files:
        stem = os.path.splitext(os.path.basename(f))[0]
        if 'preview_web' in stem:
            continue
        key = slug(group.split('·')[0] + '-' + stem)[:70]
        im = Image.open(f)
        big = 1800 if cat in ('stand', 'arquigrafia') or im.width > im.height * 1.2 else (1080 if im.width >= 1080 else im.width)
        if cat == 'impresos':
            big = 1400
        if 'Historia_' in stem:
            big = 900
        w, h = save(f, f'{IMG}/piezas/{key}.webp', big, 80, alpha=False)
        save(f, f'{IMG}/piezas/{key}-sm.webp', 520, 74, alpha=False)
        pieces.append(dict(src=f'/img/piezas/{key}.webp', sm=f'/img/piezas/{key}-sm.webp', w=w, h=h, cat=cat, group=group, title=nice(stem)))

# títulos prolijos para el sitio
FIX = {'Panel Refugio Rojo Mockup': 'Panel del refugio · Mockup', 'Panel Refugio Rojo Panel Arte Final': 'Panel del refugio · Arte final',
       'Mesa Vinilo Tablero Arte Final': 'Vinilo del tablero · Arte final', 'Mesa Vinilo Tablero Mockup': 'Vinilo del tablero · Mockup',
       'Placa Banco Arte Final': 'Placa QR · Arte final', 'Placa Banco Mockup': 'Placa QR · Mockup', 'Foto perfil Quito': 'Foto de perfil',
       'Foto perfil Quito cerca': 'Foto de perfil · cerca', 'Infografía A3 La misma banca distintas historias': 'La misma banca, distintas historias',
       'Stickers Plancha A4': 'Plancha de stickers A4', '1 · Lanzamiento Hola soy Quito': '1 · Lanzamiento: Hola, soy Quito',
       '4 · Stickers Pegalos en tu compu': '4 · Stickers: Pegalos en tu compu', '6 · Música Playlist': '6 · Música / Playlist',
       '1 · Presentación Link': '1 · Presentación con link', '4 · Si me movés devolveme': '4 · Si me movés, devolveme'}
for x in pieces:
    x['title'] = FIX.get(x['title'], x['title']).replace('(esc 1-10)', '· esc. 1:10').replace('300x220', '300 × 220').replace('120x100', '120 × 100').replace('85x200', '85 × 200')
man['piezas'] = pieces

os.makedirs(WEB + '/data', exist_ok=True)
json.dump(man, open(WEB + '/data/piezas.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)

# og image: portada del carrusel 01 recortada a 1200x630
og = Image.open(PZ + '/04_Stand_Bancala/Stand_Bancala_10 Mockup en el campus (foto real).png').convert('RGB')
r = 1200 / og.width
og = og.resize((1200, round(og.height * r)), Image.LANCZOS)
t = (og.height - 630) // 2
og.crop((0, t, 1200, t + 630)).save(IMG + '/og.jpg', quality=84)

tot = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(IMG) for f in fs)
print('poses', len(poses), 'stickers', len(stk), 'campus', len(campus), 'piezas', len(pieces), 'MB', round(tot / 1e6, 1))
