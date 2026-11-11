"""Pieza 04 · Stand Bancala (stand movil para el hall / eventos).
Genera los HTML fuente (site/stand_*.html) y sus PNG de trabajo en art/stand/.
Escalas (para Illustrator, 1 px = 0,1 mm de mesa de trabajo):
  gran formato a 1:10 -> 1 px = 1 mm real  (backwall, mostrador, roll-up, planta)
  impresos a 1:1      -> 1 px = 0,1 mm real (folleto, afiche, display, fichas)"""
from lib import *
ART = S + '/art/stand'; os.makedirs(ART, exist_ok=True)
A = '../art/stand/'
IG = '@ucasalsustentable'


def flat(bg, trama='b', op=.12, size=900):
    t = f'<div class="abs trama-{trama}" style="inset:0;opacity:{op};background-size:{size}px auto"></div>' if trama else ''
    return f'<div class="abs" style="inset:0;background:{bg}"></div>{t}'


def H(t, x, y, s, c='#fff', k=.55, w=None, align='left'):
    return (f'<div class="abs hl bounce" data-k="{k}" style="left:{x}px;top:{y}px;font-size:{s}px;color:{c};'
            f'text-align:{align};{"width:%dpx;" % w if w else ""}">{t}</div>')


def T(t, x, y, w, s=30, c='#fff', wt=500, lh=1.3, extra=''):
    return f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;font:{wt} {s}px/{lh} Brico;color:{c};{extra}">{t}</div>'


def bub(text, x, y, w, fs, tail=0.25, side='bottom'):
    return f'<div class="bub" style="left:{x}px;top:{y}px;width:{w}px;font-size:{fs}px">{text}<i class="tail" style="left:{w * tail:.0f}px"></i></div>'


def qr(x, y, s, pad=.07, b=None):
    b = b or max(4, s * 0.025)
    return (f'<div class="abs" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:#fff;border:{b:.0f}px solid var(--ink);'
            f'border-radius:{s * .09:.0f}px;padding:{s * pad:.0f}px;box-shadow:{s * .03:.0f}px {s * .04:.0f}px 0 var(--ink)"><img src="{B}qr_instagram.svg" style="width:100%;height:100%;display:block"></div>')


def tag(t, x, y, s, bg='var(--ink)', c='#fff'):
    return f'<div class="abs tag" style="left:{x}px;top:{y}px;font-size:{s}px;background:{bg};color:{c}">{t}</div>'


def step(n, t, d, s, c='var(--blue)', tc='var(--ink)'):
    return (f'<div style="display:flex;gap:{s * .55:.0f}px;align-items:flex-start;margin-bottom:{s * .9:.0f}px">'
            f'<div style="flex:none;width:{s * 1.9:.0f}px;height:{s * 1.9:.0f}px;border-radius:50%;background:{c};border:{s * .12:.0f}px solid var(--ink);'
            f'display:flex;align-items:center;justify-content:center"><span class="hl" style="font-size:{s * 1.15:.0f}px">{n}</span></div>'
            f'<div><div style="font:800 {s}px/1.05 Brico;color:{tc}">{t}</div><div style="font:500 {s * .62:.0f}px/1.3 Brico;color:{tc};opacity:.85;margin-top:{s * .2:.0f}px">{d}</div></div></div>')


def planks(W, H, n, y0=0):
    """frente de tablas de madera (como el respaldo de Quito)"""
    ph = (H - y0) / n; out = ''
    for i in range(n):
        y = y0 + i * ph
        out += (f'<div class="abs" style="left:0;top:{y:.0f}px;width:{W}px;height:{ph:.0f}px;'
                f'background:linear-gradient(180deg,#f2a04a 0,#e8892f 55%,#c96f1f 100%);border-bottom:{ph * .08:.0f}px solid var(--ink)"></div>'
                f'<div class="abs" style="left:0;top:{y + ph * .30:.0f}px;width:{W}px;height:{ph * .05:.0f}px;'
                f'background:repeating-linear-gradient(90deg,rgba(58,29,12,.55) 0 {W * .09:.0f}px,transparent {W * .09:.0f}px {W * .16:.0f}px)"></div>'
                f'<div class="abs" style="left:{W * .07 + (i % 2) * W * .4:.0f}px;top:{y + ph * .62:.0f}px;width:{W * .11:.0f}px;height:{ph * .05:.0f}px;border-radius:9px;background:rgba(58,29,12,.5)"></div>')
    return out


# 1 · BACKWALL 3000 x 2200 mm
def backwall():
    W, Hh = 3000, 2200
    body = f'''{flat('var(--navy)', 'b', .10, 1500)}
<div class="abs" style="left:0;right:0;bottom:0;height:300px;background:var(--green)"></div>
<div class="abs trama-n" style="left:0;right:0;bottom:0;height:300px;opacity:.10;background-size:1500px auto"></div>
<div class="abs" style="left:150px;top:150px">{logos(70)}</div>
{H('Mucho más<br><em>que un banco.</em>', 140, 360, 250, k=.5)}
{T('Sentate un rato con Quito, sacate una foto<br>y contanos tu historia en un banco.', 150, 1010, 1500, 66, wt=600, extra='text-shadow:0 2px 20px rgba(17,40,72,.5)')}
{tag('#TeBancoEnTodas', 150, 1290, 64, 'var(--mint)', 'var(--ink)')}
<div class="abs" style="left:1900px;top:1890px;width:1100px;height:100px;border-radius:50%;background:radial-gradient(closest-side,rgba(20,30,20,.35),rgba(20,30,20,0))"></div>
<img class="abs" src="{Q}q_sentado_feliz.png" style="left:1820px;top:560px;height:1380px">
{bub('¡Sacate una foto conmigo!', 2120, 180, 720, 62, .35)}
<div class="abs" style="left:150px;top:1965px;font:800 64px Brico;color:#fff;letter-spacing:.01em">Seguinos en {IG}</div>
<div class="abs" style="right:150px;top:1950px"><div class="hl" style="font-size:96px;color:#fff">Bancala.</div></div>'''
    render('stand_backwall', body, W, Hh, f'{ART}/backwall.png')


# 2 · MOSTRADOR (frente) 1200 x 1000 mm
def mostrador():
    W, Hh = 1200, 1000
    body = f'''<div class="abs" style="inset:0;background:var(--ink)"></div>
{planks(W, Hh, 5, 120)}
<div class="abs" style="left:0;right:0;top:0;height:120px;background:var(--green);border-bottom:14px solid var(--ink)"></div>
<div class="abs" style="left:0;right:0;top:0;height:120px;display:flex;align-items:center;justify-content:center;font:800 46px Brico;color:#fff;letter-spacing:.08em;text-transform:uppercase">Estación Bancala · Stand</div>
<div class="abs" style="left:310px;top:240px;width:580px;height:580px;border-radius:50%;background:var(--navy);border:18px solid var(--ink);box-shadow:16px 22px 0 var(--ink)"></div>
<div class="abs trama-b" style="left:328px;top:258px;width:544px;height:544px;border-radius:50%;opacity:.12;background-size:700px auto"></div>
<img class="abs" src="{B}bancala_blanco.svg" style="left:470px;top:330px;width:260px">
{H('Pasá,<br><em>sentate.</em>', 330, 500, 120, k=.4, w=540, align='center')}'''
    render('stand_mostrador', body, W, Hh, f'{ART}/mostrador.png')


# 3 · ROLL-UP 850 x 2000 mm
def rollup():
    W, Hh = 850, 2000
    steps = (step(1, 'Escaneá el QR', f'Seguí a {IG}.', 58) +
             step(2, 'Contá tu historia', 'La de ese banco donde te pasó algo. Quito la comparte.', 58, 'var(--green)') +
             step(3, 'Llevate tu sticker', 'Pegalo en la compu, no en el banco.', 58, 'var(--wood)'))
    body = f'''{flat('var(--mint)', 'n', .07, 900)}
<div class="abs" style="left:70px;top:70px">{logos(34, 'color')}</div>
{H('¿Cómo<br><em style="color:var(--blue)">participás?</em>', 66, 170, 118, k=.5)}
<div class="abs" style="left:70px;top:500px;width:720px">{steps}</div>
{qr(70, 1240, 330)}
{T('Escaneá<br>y seguinos', 440, 1300, 340, 46, 'var(--ink)', 800, 1.05)}
{T(IG, 440, 1420, 360, 30, 'var(--ink)', 700)}
<img class="abs" src="{Q}q_senalando_feliz.png" style="left:330px;top:1560px;height:420px;transform:scaleX(-1)">
<div class="abs" style="left:0;right:0;bottom:0;height:110px;background:var(--navy)"></div>
<div class="abs" style="left:70px;bottom:28px"><div class="hl" style="font-size:52px;color:var(--mint)">Bancala.</div></div>'''
    render('stand_rollup', body, W, Hh, f'{ART}/rollup.png')


# 4 · FOLLETO DIPTICO A5 (abierto A4 apaisado 297 x 210 mm)
RULES = [('Sentate, no te pares.', 'Las patas son para el piso, no para el asiento.'), ('La basura, al tacho.', 'Siempre hay uno cerca. Quito lo sabe.'),
         ('Si lo movés, devolvelo.', 'Que ningún banco quede solo en medio de la nada.'), ('¿Está roto? Avisá.', 'Escaneá el QR del banco o avisá a Mantenimiento.')]


def folleto():
    W, Hh, P = 2970, 2100, 1485
    m = 130
    ext = f'''<div class="abs" style="left:0;top:0;width:{P}px;height:{Hh}px;background:var(--paper)"></div>
<div class="abs trama-n" style="left:0;top:0;width:{P}px;height:{Hh}px;opacity:.05"></div>
{T('Bancala es la campaña de UCASAL Sustentable para cuidar los bancos de los patios, pasillos y galerías de la Facultad.', m, 170, P - 2 * m, 52, 'var(--ink)', 600, 1.25)}
{T('Porque un banco es mucho más que un banco: es donde esperás, estudiás, te reís y te recibís.', m, 520, P - 2 * m, 44, 'var(--ink)', 450, 1.3)}
{qr(m, 900, 560)}
{T('Seguí la campaña', m + 640, 960, 640, 56, 'var(--ink)', 800, 1.05)}
{T(IG, m + 640, 1050, 640, 44, 'var(--blue)', 700)}
{T('Subí tu historia en un banco y etiquetanos. Las mejores las comparte Quito.', m + 640, 1150, 620, 36, 'var(--ink)', 500, 1.3)}
<div class="abs" style="left:{m}px;right:{W - P + m}px;top:1700px;height:5px;background:var(--ink);opacity:.2"></div>
<div class="abs" style="left:{m}px;top:1800px">{logos(64, 'color')}</div>
<div class="abs" style="left:{P}px;top:0;width:{P}px;height:{Hh}px;background:var(--navy)"></div>
<div class="abs trama-b" style="left:{P}px;top:0;width:{P}px;height:{Hh}px;opacity:.10;background-size:1300px auto"></div>
<div class="abs" style="left:{P + m}px;top:150px">{logos(52)}</div>
{H('Mucho más<br><em>que un banco.</em>', P + m - 6, 300, 158, k=.5)}
<img class="abs" src="{A}figura_recorte.png" style="left:{P + 330}px;top:860px;width:1000px">
{bub('¡Hola! Soy Quito, el banquito de la facu.', P + m, 760, 520, 46, .7)}'''
    render('stand_folleto_ext', ext, W, Hh, f'{ART}/folleto_exterior.png')
    rh = ''.join(f'<div style="display:flex;gap:44px;align-items:flex-start;margin-bottom:60px"><div class="hl" style="font-size:118px;color:var(--mint);width:96px;flex:none">{i + 1}</div>'
                 f'<div><div style="font:800 64px/1.05 Brico;color:#fff">{a}</div><div style="font:500 44px/1.3 Brico;color:#fff;opacity:.85;margin-top:12px">{b}</div></div></div>' for i, (a, b) in enumerate(RULES))
    no = [('reposera', 'Tapate un poco, che.'), ('peluquería', 'Los pelos van al tacho.'), ('tu cuaderno', 'Eso no es un apunte.'), ('mudanza', 'Si me movés, devolveme.')]
    nh = ''.join(f'<div style="display:flex;align-items:center;gap:26px;margin-bottom:30px"><div style="flex:none;width:70px;height:70px;border-radius:50%;background:var(--wood);border:7px solid var(--ink);display:flex;align-items:center;justify-content:center;font:800 44px Brico;color:var(--ink)">✕</div>'
                 f'<div style="font:800 52px/1.05 Brico;color:var(--ink)">No soy {a}. <span style="font-weight:500;opacity:.8">{b}</span></div></div>' for a, b in no)
    inn = f'''<div class="abs" style="left:0;top:0;width:{P}px;height:{Hh}px;background:var(--paper)"></div>
{H('La misma banca.<br><em style="color:var(--green)">Distintas historias.</em>', m - 4, 140, 118, 'var(--blue)', k=.45)}
{T('En un mismo banco conviven los nervios del primer día, las risas entre mates, la siesta antes del parcial y el día que te recibís. Detrás de cada uno hay horas de trabajo del equipo de Mantenimiento.', m, 470, P - 2 * m, 46, 'var(--ink)', 500, 1.35)}
{T('Te banco en todas,<br>menos en estas:', m, 920, P - 2 * m, 70, 'var(--ink)', 800, 1.05)}
<div class="abs" style="left:{m}px;top:1120px;width:{P - 2 * m}px">{nh}</div>
<img class="abs" src="{Q}q_enojado.png" style="left:{P - 470}px;top:1660px;height:380px">
<div class="abs" style="left:{P}px;top:0;width:{P}px;height:{Hh}px;background:var(--green)"></div>
<div class="abs trama-n" style="left:{P}px;top:0;width:{P}px;height:{Hh}px;opacity:.10;background-size:1300px auto"></div>
{H('Bancarla vale.', P + m, 140, 150)}
{T('Cuatro reglas para que tu banco favorito siga ahí.', P + m, 330, P - 2 * m, 50, '#fff', 600)}
<div class="abs" style="left:{P + m}px;top:500px;width:{P - 2 * m - 300}px">{rh}</div>
<img class="abs" src="{Q}q_limpiando.png" style="left:{W - 520}px;top:1500px;height:520px">'''
    render('stand_folleto_int', inn, W, Hh, f'{ART}/folleto_interior.png')


# 5 · AFICHE A3 convocatoria 297 x 420 mm
def afiche():
    W, Hh = 2970, 4200
    body = f'''<div class="abs" style="inset:0;background:radial-gradient(120% 80% at 50% 58%,#e5f7ec 0,#cdeedb 45%,#9fd9b8 100%)"></div>
<div class="abs trama-n" style="inset:0;opacity:.06;background-size:2200px auto"></div>
<div class="abs" style="left:200px;top:190px">{logos(90, 'color')}</div>
{H('Quito te espera<br><em style="color:var(--blue)">en persona.</em>', 190, 420, 300, k=.5)}
{T('Vení al stand de Bancala: sacate una foto con él, contanos tu historia en un banco y llevate tu sticker.', 200, 1180, 2400, 86, 'var(--ink)', 600, 1.25)}
<img class="abs" src="{A}figura_recorte.png" style="left:385px;top:1560px;width:2200px">
<div class="abs" style="left:0;right:0;bottom:0;height:640px;background:var(--navy)"></div>
<div class="abs trama-b" style="left:0;right:0;bottom:0;height:640px;opacity:.10;background-size:2200px auto"></div>
<div class="abs" style="left:200px;top:3650px;font:800 110px/1 Brico;color:#fff">Hall de la Facultad</div>
<div class="abs" style="left:200px;top:3800px;font:600 78px/1 Brico;color:var(--mint)">Del 00 al 00 de mes · 10 a 18 h</div>
{qr(2280, 3640, 440)}'''
    render('stand_afiche', body, W, Hh, f'{ART}/afiche.png')


# 6 · DISPLAY DE MESA A5 (atril) 148 x 210 mm
def display():
    W, Hh = 1480, 2100
    body = f'''<div class="abs" style="inset:0;background:#fff"></div>
<div class="abs" style="left:0;right:0;top:0;height:520px;background:var(--blue)"></div>
<div class="abs trama-b" style="left:0;right:0;top:0;height:520px;opacity:.12;background-size:1100px auto"></div>
{H('Contale a Quito<br><em>tu historia.</em>', 100, 120, 128, k=.45)}
{qr(390, 640, 700)}
{T('Escaneá, seguí a ' + IG + ' y mandanos tu historia en un banco.', 110, 1430, 1260, 52, 'var(--ink)', 600, 1.25, 'text-align:center')}
<img class="abs" src="{Q}q_saludo.png" style="left:960px;top:1620px;height:420px">
<div class="abs" style="left:110px;top:1890px">{logos(52, 'color')}</div>'''
    render('stand_display', body, W, Hh, f'{ART}/display.png')


# 7 · FICHA FIGURA 3D (A3 apaisado)
def ficha_figura():
    W, Hh = 4200, 2970
    specs = [('Alto total', '55 cm (figura 45 cm + base 10 cm)'), ('Figura', 'Impresión 3D en resina (SLA), lijada, pintada a mano y barniz satinado.'),
             ('Base', 'Disco de MDF laqueado Ø 40 cm, azul Bancala #1B4D8B, logo en vinilo de corte blanco.'),
             ('Ubicación', 'Sobre el mostrador, a 1 m de altura: queda a la altura de la cámara del celular.'),
             ('Fijación', 'Perno roscado oculto en la base; anti-vuelco en el mostrador.')]
    sh = ''.join(f'<div style="display:flex;gap:40px;border-top:5px solid var(--ink);padding:34px 0 30px"><div style="width:380px;flex:none;font:800 50px Brico;color:var(--blue)">{a}</div>'
                 f'<div style="font:500 50px/1.25 Brico;color:var(--ink)">{b}</div></div>' for a, b in specs)
    sw = ''.join(f'<div style="display:flex;align-items:center;gap:22px;margin-right:50px"><div style="width:90px;height:90px;border-radius:50%;background:{c};border:6px solid var(--ink)"></div><div style="font:700 38px/1.15 Brico;color:var(--ink)">{n}<br><span style="font-weight:500;opacity:.7">{h}</span></div></div>'
                 for c, n, h in [('#e8892f', 'Madera', '#E8892F'), ('#3a1d0c', 'Tinta', '#3A1D0C'), ('#fbf1df', 'Guantes', '#FBF1DF'), ('#1b4d8b', 'Base', '#1B4D8B')])
    body = f'''<div class="abs" style="inset:0;background:var(--paper)"></div>
<img class="abs" src="{A}figura_render.png" style="left:0;top:0;width:{Hh}px;height:{Hh}px">
{tag('Pieza 04 · Stand Bancala', 3100, 170, 44, 'var(--green)', '#fff')}
{H('Quito 3D', 3090, 290, 220, 'var(--blue)', k=.5)}
{T('Figura de mostrador: el personaje sale de la pantalla y se sienta con vos. Es el punto de foto del stand.', 3100, 560, 980, 52, 'var(--ink)', 600, 1.25)}
<div class="abs" style="left:3100px;top:900px;width:1000px">{sh}</div>
<div class="abs" style="left:3100px;top:2520px;display:flex;flex-wrap:wrap;width:1050px;row-gap:30px">{sw}</div>'''
    render('stand_figura', body, W, Hh, f'{ART}/ficha_figura.png')


# 8 · PLANTA Y VISTA FRONTAL (1 px = 1 mm real, lamina a 1:10 -> se imprime A3 a 1:? ver rotulo)
def planta():
    W, Hh = 4200, 2970
    k = 0.42  # mm -> px dentro de la lamina (escala grafica)
    ox, oy = 260, 520  # planta
    def r(x, y, w, h, fill, bd='var(--ink)', bw=6, rad=0, txt='', fs=40):
        return (f'<div class="abs" style="left:{ox + x * k:.0f}px;top:{oy + y * k:.0f}px;width:{w * k:.0f}px;height:{h * k:.0f}px;background:{fill};'
                f'border:{bw}px solid {bd};border-radius:{rad}px;display:flex;align-items:center;justify-content:center;text-align:center;font:700 {fs}px/1.1 Brico;color:var(--ink)">{txt}</div>')
    def dim(x1, y1, x2, y2, txt, off=0, vert=False):
        if not vert:
            y = oy + y1 * k + off
            return (f'<div class="abs" style="left:{ox + x1 * k:.0f}px;top:{y:.0f}px;width:{(x2 - x1) * k:.0f}px;height:0;border-top:4px solid var(--blue)"></div>'
                    f'<div class="abs" style="left:{ox + x1 * k - 2:.0f}px;top:{y - 22:.0f}px;width:4px;height:44px;background:var(--blue)"></div><div class="abs" style="left:{ox + x2 * k - 2:.0f}px;top:{y - 22:.0f}px;width:4px;height:44px;background:var(--blue)"></div>'
                    f'<div class="abs" style="left:{ox + x1 * k:.0f}px;top:{y - 66:.0f}px;width:{(x2 - x1) * k:.0f}px;text-align:center;font:800 40px Brico;color:var(--blue)">{txt}</div>')
        x = ox + x1 * k + off
        return (f'<div class="abs" style="left:{x:.0f}px;top:{oy + y1 * k:.0f}px;width:0;height:{(y2 - y1) * k:.0f}px;border-left:4px solid var(--blue)"></div>'
                f'<div class="abs" style="left:{x - 22:.0f}px;top:{oy + y1 * k - 2:.0f}px;width:44px;height:4px;background:var(--blue)"></div><div class="abs" style="left:{x - 22:.0f}px;top:{oy + y2 * k - 2:.0f}px;width:44px;height:4px;background:var(--blue)"></div>'
                f'<div class="abs" style="left:{x - 150:.0f}px;top:{oy + (y1 + y2) / 2 * k - 20:.0f}px;width:120px;text-align:right;font:800 40px Brico;color:var(--blue)">{txt}</div>')
    plan = (f'<div class="abs" style="left:{ox}px;top:{oy}px;width:{4000 * k:.0f}px;height:{3000 * k:.0f}px;border:5px dashed rgba(58,29,12,.35);border-radius:10px"></div>'
            + r(500, 150, 3000, 120, 'var(--navy)', txt='<span style="color:#fff">1 · Backwall 300 × 220</span>')
            + r(1100, 700, 1800, 450, '#e8892f', txt='Banco real del campus', rad=10)
            + f'<div class="abs" style="left:{ox + 1300 * k:.0f}px;top:{oy + 1350 * k:.0f}px;width:{1400 * k:.0f}px;height:{1400 * k:.0f}px;border-radius:50%;background:var(--blue);border:6px solid var(--ink);display:flex;align-items:center;justify-content:center;font:800 40px/1.1 Brico;color:#fff;text-align:center">Vinilo de piso<br>Ø 140</div>'
            + r(150, 1500, 1200, 500, '#f2a04a', txt='2 · Mostrador<br>120 × 50', rad=6).replace('justify-content:center','justify-content:flex-start;padding-left:30px')
            + f'<div class="abs" style="left:{ox + 1000 * k:.0f}px;top:{oy + 1600 * k:.0f}px;width:{400 * k:.0f}px;height:{400 * k:.0f}px;border-radius:50%;background:var(--navy);border:5px solid var(--ink)"></div>'
            + r(3150, 1250, 850, 220, 'var(--mint)', txt='3 · Roll-up', fs=36, rad=6)
            + dim(500, 0, 3500, 0, '300 cm', off=-30) + dim(0, 0, 0, 3000, '300 cm', off=-30, vert=True)
            + dim(150, 2000, 1350, 2000, '120 cm', off=70) + dim(0, 1500, 0, 2000, '50', off=60, vert=True))
    # vista frontal
    fx, fy, fk = 2350, 760, 0.44
    def fr(x, y, w, h, fill, txt='', c='#fff', bw=6):
        return (f'<div class="abs" style="left:{fx + x * fk:.0f}px;top:{fy + (2300 - y - h) * fk:.0f}px;width:{w * fk:.0f}px;height:{h * fk:.0f}px;background:{fill};'
                f'border:{bw}px solid var(--ink);display:flex;align-items:center;justify-content:center;text-align:center;font:700 36px/1.1 Brico;color:{c}">{txt}</div>')
    front = (fr(100, 0, 3000, 2200, 'var(--navy)', 'Backwall 300 × 220') + fr(800, 0, 1500, 450, '#e8892f', 'Banco 45', 'var(--ink)')
             + fr(-150, 0, 1200, 1000, '#f2a04a', 'Mostrador 100', 'var(--ink)') + fr(200, 1000, 400, 100, 'var(--navy)', '', bw=4)
             + f'<img class="abs" src="{A}figura_recorte.png" style="left:{fx + 110 * fk:.0f}px;top:{fy + (2300 - 1560) * fk:.0f}px;width:{600 * fk:.0f}px">'
             + fr(2950, 0, 850, 2000, 'var(--mint)', 'Roll-up<br>85 × 200', 'var(--ink)')
             + f'<div class="abs" style="left:{fx - 150 * fk - 40:.0f}px;top:{fy + 2300 * fk:.0f}px;width:{4100 * fk:.0f}px;height:6px;background:var(--ink)"></div>')
    body = f'''<div class="abs" style="inset:0;background:var(--paper)"></div>
{tag('Pieza 04 · Stand Bancala', 260, 150, 44, 'var(--green)', '#fff')}
{H('Planta y vista frontal', 250, 240, 150, 'var(--blue)', k=.4)}
<div class="abs" style="left:260px;top:2000px;font:800 52px Brico;color:var(--ink)">Planta · módulo 3 × 3 m</div>
<div class="abs" style="left:2280px;top:2000px;font:800 52px Brico;color:var(--ink)">Vista frontal</div>
{plan}{front}
<div class="abs" style="left:260px;top:2180px;width:3680px;font:500 40px/1.4 Brico;color:var(--ink)">
<b>1 · Backwall</b> lona tensada sobre bastidor de aluminio desarmable. <b>2 · Mostrador</b> MDF 18 mm con frente impreso en vinilo laminado mate y tapa laqueada; adentro, estante para folletos y stickers. <b>3 · Roll-up</b> 85 × 200 cm con base de aluminio. <b>Banco real</b>: un banco del campus restaurado por Mantenimiento, para sentarse en la foto. <b>Vinilo de piso</b> antideslizante Ø 140 cm “Sentate, te bancamos”. Medidas en cm.</div>'''
    render('stand_planta', body, W, Hh, f'{ART}/planta.png')


# 9 · LAMINA MOCKUP (A3 apaisado)
def lamina_mockup():
    W, Hh = 4200, 2970
    body = f'''<div class="abs" style="inset:0;background:var(--char)"></div>
<img class="abs" src="{A}mockup_stand.jpg" style="left:0;top:0;width:{W}px;height:2800px;object-fit:cover">
<div class="abs" style="left:0;right:0;top:2800px;height:170px;background:var(--navy)"></div>
<div class="abs" style="left:150px;top:2800px;height:170px;display:flex;align-items:center;gap:40px">
<span class="hl" style="font-size:84px;color:#fff">Estación Bancala · Stand</span>
<span style="font:600 46px Brico;color:#fff;opacity:.85">Módulo 3 × 3 m · backwall, mostrador con Quito 3D, roll-up, banco real y vinilo de piso</span></div>
<div class="abs" style="right:150px;top:2800px;height:170px;display:flex;align-items:center">{logos(56)}</div>'''
    render('stand_mockup', body, W, Hh, f'{ART}/lamina_mockup.png')


if __name__ == '__main__':
    only = sys.argv[1:]
    for f in [backwall, mostrador, rollup, folleto, afiche, display, ficha_figura, planta, lamina_mockup]:
        if only and f.__name__ not in only: continue
        f(); print('ok', f.__name__, flush=True)
