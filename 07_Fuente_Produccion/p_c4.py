"""Carrusel 04 · "Un día en la vida de Quito" (8 slides 1080 x 1350).
Foto real del campus + Quito recortado (cut_c4.py) + burbuja de comic + chip de hora + linea de tiempo.
Genera site/c4_N.html, los PNG finales en 02_Piezas y una lamina de control.
uso: python p_c4.py [n ...]"""
import math, json
from lib import *
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

W, H = 1080, 1350
ROOT = os.path.normpath(S + '/..')
DEST = ROOT + '/02_Piezas/01_Redes_Instagram/Carrusel_04_Un_dia_en_la_vida_de_Quito'
LOOK = ROOT + '/04_Recursos/Fotos_Campus/Editadas_Look_Bancala'
ART = S + '/art/c4'; A = '../art/c4/'
os.makedirs(ART, exist_ok=True); os.makedirs(DEST, exist_ok=True)

AZUL, VERDE, MADERA, AMARILLO = '#183F79', '#51B058', '#985A30', '#F2B417'
M = 72           # margen de texto (>= 64 del brief, dentro de la zona segura 3:4)
TL_Y = 1270      # linea de tiempo: 80 px sobre el borde inferior
N = 8

CSS = f'''
@font-face{{font-family:Hand;src:url(../fonts/PatrickHandSC-Regular.ttf)}}
@font-face{{font-family:Mono;src:url(../fonts/SpaceMono-Bold.ttf);font-weight:700}}
.t4{{position:absolute;font-family:Titan;color:#fff;line-height:.95;letter-spacing:.005em;
  -webkit-text-stroke:.06em var(--ink);paint-order:stroke fill;
  text-shadow:.045em .06em 0 var(--ink),0 6px 26px rgba(8,18,40,.55)}}
.t4 em{{font-style:normal;color:{VERDE}}}
.baj{{position:absolute;font-family:Brico;font-weight:600;color:#fff;line-height:1.22;letter-spacing:-.005em;
  text-shadow:0 2px 3px rgba(8,18,40,.55),0 2px 22px rgba(8,18,40,.6)}}
.chip{{position:absolute;display:flex;align-items:center;gap:12px;background:{AMARILLO};color:#111;
  font-family:Mono;font-weight:700;font-size:34px;line-height:1;padding:11px 22px 11px 16px;border-radius:999px;
  box-shadow:0 5px 0 rgba(58,29,12,.9),0 10px 26px rgba(0,0,0,.25)}}
.chip i{{display:block;width:30px;height:30px;border-radius:50%;border:4px solid #111;position:relative}}
.chip i:before,.chip i:after{{content:"";position:absolute;left:11px;bottom:11px;width:4px;background:#111;border-radius:2px;transform-origin:50% 100%}}
.chip i:before{{height:10px}}.chip i:after{{height:8px;transform:rotate(90deg)}}
.btxt{{position:absolute;display:flex;align-items:center;justify-content:center;text-align:center;
  font-family:Hand;color:#111;line-height:1.02;letter-spacing:.01em}}
'''


# ---------------------------------------------------------------- fotos
def prep_photo(n, grade=None):
    """foto del campus (960x1280) -> 1080x1440 con remuestreo Lanczos + enfoque, grado opcional"""
    im = Image.open(f'{LOOK}/Campus_{n:02d}_look.jpg').convert('RGB').resize((1080, 1440), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    a = np.asarray(im).astype(np.float32) / 255
    if grade == 'manana':      # luz de manana: un poco mas fresca y luminosa
        a = a * np.array([0.98, 1.0, 1.04]); a = 1 - (1 - a) * 0.96
    elif grade == 'tarde':     # 17 hs: calida suave
        a = a * np.array([1.05, 1.0, 0.92])
    elif grade in ('dorado', 'atardecer'):   # 19/20 hs: dorado, sombras calidas, cielo apagado
        k = 1.0 if grade == 'dorado' else 1.25
        a = a * np.array([1 + .09 * k, 1 + .01 * k, 1 - .13 * k])
        lum = a.mean(2, keepdims=True)
        a = a * (0.94 - 0.04 * k) + np.array([0.06, 0.025, -0.01]) * k * (1 - lum)
    a = np.clip(a, 0, 1)
    out = f'{ART}/foto_{n:02d}.jpg'
    Image.fromarray((a * 255 + .5).astype(np.uint8)).save(out, quality=95)
    return f'{A}foto_{n:02d}.jpg'


# ---------------------------------------------------------------- piezas
def logos_top():
    return f'<div class="abs" style="left:64px;top:64px">{logos(46)}</div>'


def scrim(op=.58, to=50, extra=0):
    c = '24,63,121'  # azul UCASAL
    return (f'<div class="abs" style="left:0;right:0;top:0;height:{to}%;background:linear-gradient(180deg,'
            f'rgba({c},{op}) 0%,rgba({c},{op * .78}) 38%,rgba({c},{op * .3}) 72%,rgba({c},0) 100%)"></div>'
            + (f'<div class="abs" style="left:0;right:0;bottom:0;height:{extra}px;background:linear-gradient(0deg,'
               f'rgba(10,22,45,.72),rgba(10,22,45,.45) 55%,rgba(10,22,45,0))"></div>' if extra else ''))


def chip(t, y=150):
    return f'<div class="chip" style="left:{M}px;top:{y}px"><i></i>{t}</div>'


def title(html, y, size, w=900):
    return f'<div class="t4" style="left:{M - 4}px;top:{y}px;width:{w}px;font-size:{size}px">{html}</div>'


def bajada(html, y, size=36, w=640):
    return f'<div class="baj" style="left:{M}px;top:{y}px;width:{w}px;font-size:{size}px">{html}</div>'


def timeline(i):
    x0, x1 = M, W - M; L = x1 - x0
    px = x0 + L * (i - 1) / (N - 1)
    stops = ''.join(f'<div class="abs" style="left:{x0 + L * k / (N - 1) - 6:.1f}px;top:{TL_Y - 4}px;width:12px;height:12px;'
                    f'border-radius:50%;background:#fff;opacity:{.95 if k < i else .6}"></div>' for k in range(N))
    return (f'<div class="abs" style="left:{x0}px;top:{TL_Y}px;width:{L}px;height:4px;border-radius:2px;background:rgba(255,255,255,.6);'
            f'box-shadow:0 1px 6px rgba(0,0,0,.25)"></div>'
            f'<div class="abs" style="left:{x0}px;top:{TL_Y}px;width:{px - x0:.1f}px;height:4px;border-radius:2px;background:#fff"></div>'
            f'{stops}<div class="abs" style="left:{px - 17:.1f}px;top:{TL_Y - 15}px;width:34px;height:34px;border-radius:50%;'
            f'background:{VERDE};border:5px solid #fff;box-shadow:0 0 0 6px rgba(81,176,88,.35),0 3px 10px rgba(0,0,0,.35)"></div>')


def quito(pose, x, y, h, flip=False, ground=True, cast=(-0.9, .22), sh_w=.62, sh_x=.5, sh_y=.975):
    """Quito (PNG recortado) con sombra de contacto; ground=True agrega sombra proyectada al piso."""
    f = f'{S}/quito/q_{pose}.png'; iw, ih = Image.open(f).size; w = h * iw / ih
    tr = 'transform:scaleX(-1);' if flip else ''
    out = ''
    if ground:   # sombra proyectada (silueta aplastada y difusa)
        out += (f'<img class="abs" src="{Q}q_{pose}.png" style="left:{x}px;top:{y}px;height:{h}px;transform-origin:50% 97%;'
                f'transform:{"scaleX(-1) " if flip else ""}scaleY({cast[1]}) skewX({cast[0] * 40 * (-1 if flip else 1)}deg);'
                f'filter:brightness(0) blur(7px);opacity:.28"></img>')
    cw = w * sh_w; cx = x + w * (sh_x if not flip else 1 - sh_x)
    out += (f'<div class="abs" style="left:{cx - cw / 2:.0f}px;top:{y + h * sh_y - h * .04:.0f}px;width:{cw:.0f}px;height:{h * .08:.0f}px;'
            f'border-radius:50%;background:radial-gradient(closest-side,rgba(25,16,8,.55),rgba(25,16,8,.25) 55%,rgba(25,16,8,0))"></div>')
    out += (f'<img class="abs" src="{Q}q_{pose}.png" style="left:{x}px;top:{y}px;height:{h}px;{tr}'
            f'filter:drop-shadow(0 4px 6px rgba(0,0,0,.18))">')
    return out, w


def bubble(text, bx, by, bw, bh, tip, fs=38, kind='round', base=None):
    """globo ovalado tipo comic. tip = punta de la colita (apunta a la boca). kind='rayo' -> colita en zigzag."""
    cx, cy = bx + bw / 2, by + bh / 2; rx, ry = bw / 2, bh / 2
    tx, ty = tip
    ang = math.atan2((ty - cy) / ry, (tx - cx) / rx) if base is None else base
    # base de la colita sobre el borde de la elipse
    def on(a): return cx + rx * math.cos(a) * .9, cy + ry * math.sin(a) * .9
    da = .26 if kind == 'round' else .2
    b1, b2 = on(ang - da), on(ang + da)
    if kind == 'round':
        mx, my = (b1[0] + b2[0]) / 2, (b1[1] + b2[1]) / 2
        # curvas suaves (colita redonda clasica, levemente curvada)
        nx, ny = ty - my, -(tx - mx); L = math.hypot(nx, ny) or 1; nx, ny = nx / L, ny / L
        bend = 18
        c1 = ((b1[0] + tx) / 2 + nx * bend, (b1[1] + ty) / 2 + ny * bend)
        c2 = ((b2[0] + tx) / 2 + nx * bend * .4, (b2[1] + ty) / 2 + ny * bend * .4)
        tail = f'M{b1[0]:.1f},{b1[1]:.1f} Q{c1[0]:.1f},{c1[1]:.1f} {tx:.1f},{ty:.1f} Q{c2[0]:.1f},{c2[1]:.1f} {b2[0]:.1f},{b2[1]:.1f} Z'
    else:  # rayo: zigzag que se afina hacia la punta
        mx, my = (b1[0] + b2[0]) / 2, (b1[1] + b2[1]) / 2
        dx, dy = tx - mx, ty - my; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; px_, py_ = -uy, ux
        hw = math.hypot(b2[0] - b1[0], b2[1] - b1[1]) / 2
        pts_l, pts_r = [b1], [b2]
        for k, (t, off) in enumerate([(.36, .55), (.33, -.1), (.68, .2), (.64, -.45)]):
            w_ = hw * (1 - t) * 1.1
            bx_, by_ = mx + dx * t + px_ * off * hw * 1.4, my + dy * t + py_ * off * hw * 1.4
            if k % 2 == 0: pts_l.append((bx_ - px_ * w_ * .2, by_ - py_ * w_ * .2)); pts_r.append((bx_ + px_ * w_, by_ + py_ * w_))
            else: pts_l.append((bx_ - px_ * w_, by_ - py_ * w_)); pts_r.append((bx_ + px_ * w_ * .2, by_ + py_ * w_ * .2))
        poly = pts_l + [(tx, ty)] + pts_r[::-1]
        tail = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in poly) + ' Z'
    ell = f'M{cx - rx:.1f},{cy:.1f} a{rx:.1f},{ry:.1f} 0 1,0 {2 * rx:.1f},0 a{rx:.1f},{ry:.1f} 0 1,0 {-2 * rx:.1f},0 Z'
    svg = (f'<svg class="abs" style="left:0;top:0;overflow:visible;filter:drop-shadow(0 8px 14px rgba(0,0,0,.28))" width="{W}" height="{H}">'
           f'<g stroke="#111" stroke-width="11" stroke-linejoin="round" fill="#111"><path d="{ell}"/><path d="{tail}"/></g>'
           f'<g fill="#fff"><path d="{ell}"/><path d="{tail}"/></g></svg>')
    pad = .2
    txt = (f'<div class="btxt" style="left:{bx + bw * pad / 2:.0f}px;top:{by + bh * .1:.0f}px;width:{bw * (1 - pad):.0f}px;'
           f'height:{bh * .8:.0f}px;font-size:{fs}px">{text}</div>')
    return svg + txt


def swipe_hint(y=1196):
    return (f'<div class="abs" style="right:{M}px;top:{y}px;display:flex;align-items:center;gap:10px;font:700 32px Brico;color:#fff;'
            f'letter-spacing:.02em;text-shadow:0 2px 12px rgba(0,0,0,.55)">Deslizá<svg width="44" height="22" viewBox="0 0 44 22">'
            f'<path d="M2 11h36M28 2l11 9-11 9" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')


def photo(src, pos='50% 50%'):
    return f'<img class="fill" src="{src}" style="object-position:{pos}">'


# ---------------------------------------------------------------- slides
SLIDES = {}


def slide(i, name):
    def deco(f): SLIDES[i] = (name, f); return f
    return deco


@slide(1, 'Portada')
def s1():
    bg = photo(prep_photo(42, 'manana'), '50% 40%')
    q, _ = quito('c4_1_despertando', 488, 640, 560, cast=(-1.0, .2))
    return (bg + scrim(.6, 52) +
            # brillo de sol de manana
            '<div class="abs" style="left:-200px;top:-260px;width:900px;height:900px;border-radius:50%;'
            'background:radial-gradient(closest-side,rgba(255,236,190,.28),rgba(255,236,190,0));mix-blend-mode:screen"></div>'
            + logos_top()
            + title('UN DÍA<br>EN LA VIDA<br><em>DE QUITO</em>', 150, 116)
            + bajada('Lo que vive un banco del campus,<br>de 8 a 20 hs.', 500, 38)
            + timeline(1) + q + swipe_hint())


@slide(2, '0800_Primer_ingresante')
def s2():
    bg = photo(prep_photo(11), '50% 0%')
    q, w = quito('c4_2_animando', 420, 486, 400, flip=True, ground=False, sh_y=.96, sh_w=.75)
    return (bg + scrim(.58, 50) + logos_top() + chip('08:00')
            + title('Llega el primer<br>ingresante, <em>re nervioso.</em>', 226, 72, w=960)
            + timeline(2) + q
            + bubble('Tranqui, que te<br>va a ir bien.', 640, 760, 390, 200, (690, 650), fs=52))


@slide(3, '1030_Hora_del_mate')
def s3():
    bg = photo(prep_photo(21), '50% 50%')
    q, w = quito('c4_3_mate', 300, 850, 410, ground=False, sh_y=.965, sh_w=.8)
    return (bg + scrim(.6, 48) + logos_top() + chip('10:30')
            + title('Hora del <em>mate.</em>', 226, 92)
            + timeline(3) + q
            + bubble('¿Me pasan<br>uno, che?', 680, 650, 340, 200, (575, 955), fs=54))


@slide(4, '1300_Almuerzo_al_sol')
def s4():
    bg = photo(prep_photo(41), '50% 50%')
    q, w = quito('c4_4_basura', 500, 820, 440, cast=(-.8, .2), sh_x=.47, sh_w=.8)
    return (bg + scrim(.58, 50) + logos_top() + chip('13:00')
            + title('Almuerzo <em>al sol.</em>', 226, 92)
            + bajada('Lo que dejás en el banco,<br>lo junta alguien.', 336, 36)
            + timeline(4) + q
            + bubble('Rico el sánguche…<br>¿y los papelitos?', 330, 560, 520, 210, (690, 880), fs=50))


@slide(5, '1500_Hora_libre')
def s5():
    bg = photo(prep_photo(27), '50% 50%')
    q, w = quito('c4_5_enojado', 640, 830, 430, cast=(-.7, .18), sh_w=.7, sh_x=.55)
    return (bg + scrim(.6, 50) + logos_top() + chip('15:00')
            + title('Hora libre y alguien<br><em>se aburre…</em>', 226, 82)
            + timeline(5) + q
            + bubble('¡Ey! No soy<br>tu cuaderno.', 72, 990, 420, 210, (650, 960), fs=54, kind='rayo'))


@slide(6, '1700_Siesta_improvisada')
def s6():
    bg = photo(prep_photo(15, 'tarde'), '50% 50%')
    q, w = quito('c4_6_indignado', 610, 372, 380, cast=(-.9, .2), sh_w=.7)
    return (bg + scrim(.58, 50) + logos_top() + chip('17:00')
            + title('<em>Siesta</em> improvisada.', 226, 84, w=960)
            + timeline(6) + q
            + bubble('Soy banco, no cama.<br>Las zapatillas, al piso.', 64, 382, 560, 220, (700, 520), fs=46))


@slide(7, '1900_Llega_Mantenimiento')
def s7():
    bg = photo(prep_photo(2, 'dorado'), '50% 50%')
    q, w = quito('c4_7_emocionado', 380, 700, 370, ground=False, sh_y=.955, sh_w=.85)
    return (bg + scrim(.62, 52)
            + '<div class="abs" style="inset:0;background:radial-gradient(120% 90% at 85% 15%,rgba(255,170,80,.30),rgba(255,140,60,0) 60%);mix-blend-mode:screen"></div>'
            + logos_top() + chip('19:00')
            + title('Llega<br><em>Mantenimiento.</em>', 226, 90)
            + bajada('Lija lo rayado, ajusta tornillos<br>y junta lo que quedó.', 420, 36)
            + timeline(7) + q
            + bubble('Ellos sí que<br>me bancan.', 630, 545, 370, 205, (560, 800), fs=54))


@slide(8, '2000_Cierre')
def s8():
    bg = photo(prep_photo(40, 'atardecer'), '50% 50%')
    q, w = quito('c4_8_saludo', 610, 520, 430, ground=False, sh_y=.62, sh_w=.9)
    big = (f'<div class="abs" style="left:0;right:0;top:972px;display:flex;flex-direction:column;align-items:center">'
           f'<img src="{B}bancala_blanco.svg" style="height:66px;filter:drop-shadow(0 3px 10px rgba(0,0,0,.4))">'
           f'<div class="t4" style="position:relative;margin-top:22px;font-size:66px;text-align:center;line-height:1">BANCARLA VALE.<br><em>AHORA TE TOCA A VOS.</em></div>'
           f'<div style="margin-top:14px;font:500 19px Brico;color:rgba(255,255,255,.82);letter-spacing:.02em">'
           f'Campaña desarrollada por [Agencia] · DCV IV · UCASAL 2026</div></div>')
    return (bg + scrim(.6, 50, extra=560)
            + '<div class="abs" style="inset:0;background:radial-gradient(90% 70% at 90% 30%,rgba(255,160,70,.32),rgba(255,140,60,0) 65%);mix-blend-mode:screen"></div>'
            + logos_top() + chip('20:00')
            + title('Mañana arranca<br>todo <em>de nuevo.</em>', 226, 84)
            + bajada('Yo te banco en todas.<br>Bancame vos también.', 410, 36)
            + q + big + timeline(8))


def build(only=()):
    outs = []
    for i, (name, f) in sorted(SLIDES.items()):
        if only and i not in only: continue
        out = f'{DEST}/carrusel04_slide{i:02d}.png'
        render(f'c4_{i}', f(), W, H, out, css=CSS); outs.append(out); print('ok', i, name, flush=True)
    return outs


if __name__ == '__main__':
    only = tuple(int(a) for a in sys.argv[1:])
    build(only)
