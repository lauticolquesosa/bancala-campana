"""Genera 02_Piezas/04_Stand_Bancala/Stand_Bancala.ai (una mesa de trabajo por pieza + mockup)
reutilizando el conversor HTML -> Illustrator de make.py (texto vivo, vectores, muestras globales).
Escala: 1 px del HTML = 0,1 mm de mesa de trabajo. Gran formato dibujado a 1:10."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
src = open(HERE + '/make.py', encoding='utf8').read()
src = src.replace("PROJ = r'C:/Users/Lauti/Documents/Tecnologia del Diseño - Campaña Bancala'", f'PROJ = r"{ROOT}"')
src = src.replace("FD = 'C:/Users/Lauti/AppData/Local/Microsoft/Windows/Fonts/'", "FD = os.environ['LOCALAPPDATA'].replace('\\\\', '/') + '/Microsoft/Windows/Fonts/'")
src = src.replace("TTFont(FD + 'TitanOne-Regular.ttf')", "TTFont(FD + 'TitanOne-Regular_Display.ttf')")
src = src.split("if __name__ == '__main__':")[0]
exec(compile(src, 'make.py', 'exec'))

OUT = ROOT + '/02_Piezas/04_Stand_Bancala'; os.makedirs(OUT, exist_ok=True)
PAGES = [  # (html, w, h, nombre de la mesa de trabajo)
    ('stand_mockup.html', 4200, 2970, '00 Mockup del stand'),
    ('stand_backwall.html', 3000, 2200, '01 Backwall 300x220 cm (esc 1-10)'),
    ('stand_mostrador.html', 1200, 1000, '02 Mostrador frente 120x100 cm (esc 1-10)'),
    ('stand_rollup.html', 850, 2000, '03 Roll-up 85x200 cm (esc 1-10)'),
    ('stand_figura.html', 4200, 2970, '04 Quito 3D figura de mostrador'),
    ('stand_folleto_ext.html', 2970, 2100, '05 Folleto A5 exterior'),
    ('stand_folleto_int.html', 2970, 2100, '06 Folleto A5 interior'),
    ('stand_afiche.html', 2970, 4200, '07 Afiche A3 convocatoria'),
    ('stand_display.html', 1480, 2100, '08 Display de mesa A5 con QR'),
    ('stand_planta.html', 4200, 2970, '09 Planta y vista frontal'),
]
DOCS['stand'] = dict(out=OUT + '/Stand_Bancala.ai', S=72 / 254, pages=[(h, w, hh) for h, w, hh, _ in PAGES], titles=[n for *_, n in PAGES])
pretty = lambda s: s  # nombres tal cual

if __name__ == '__main__':
    js = build_doc('stand', png=False); run(js)
