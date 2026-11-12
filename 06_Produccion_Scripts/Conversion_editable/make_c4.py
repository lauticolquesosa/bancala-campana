"""Genera Carrusel_04_Un_dia_en_la_vida_de_Quito.ai (una mesa de trabajo por slide) con el conversor de make.py."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
src = open(HERE + '/make.py', encoding='utf8').read()
src = src.replace("PROJ = r'C:/Users/Lauti/Documents/Tecnologia del Diseño - Campaña Bancala'", f'PROJ = r"{ROOT}"')
src = src.replace("FD = 'C:/Users/Lauti/AppData/Local/Microsoft/Windows/Fonts/'", "FD = os.environ['LOCALAPPDATA'].replace('\\\\', '/') + '/Microsoft/Windows/Fonts/'")
src = src.replace("TTFont(FD + 'TitanOne-Regular.ttf')", "TTFont(FD + 'TitanOne-Regular_Display.ttf')")
src = src.split("if __name__ == '__main__':")[0]
exec(compile(src, 'make.py', 'exec'))
D = IG + '/Carrusel_04_Un_dia_en_la_vida_de_Quito'
T = ['01 Portada', '02 08-00 Primer ingresante', '03 10-30 Hora del mate', '04 13-00 Almuerzo al sol',
     '05 15-00 Hora libre', '06 17-00 Siesta improvisada', '07 19-00 Llega Mantenimiento', '08 20-00 Cierre']
DOCS['car4'] = dict(out=D + '/Carrusel_04_Un_dia_en_la_vida_de_Quito.ai', S=1,
                    pages=[(f'c4_{i}.html', 1080, 1350) for i in range(1, 9)], titles=T)
pretty = lambda s: s
if __name__ == '__main__':
    run(build_doc('car4', png='--png' in sys.argv))
