import json, os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.normpath(os.path.join(HERE, '..', '..', '07_Fuente_Produccion'))
SITE = OLD + '/site'
JS = open(HERE + '/extract.js', encoding='utf8').read()
_pw = _b = None


def browser():
    global _pw, _b
    if _b is None:
        _pw = sync_playwright().start(); _b = _pw.chromium.launch()
    return _b


def extract(html, root='.pc', w=1080, h=1350):
    pg = browser().new_page(viewport={'width': w, 'height': h})
    pg.goto(Path(SITE + '/' + html).as_uri()); pg.wait_for_load_state('networkidle')
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
    data = pg.evaluate(JS, root)
    pg.close()
    return data


def render_bg(spec, out, scale=2):
    """raster fallback: paint only the background of an element, transparent elsewhere"""
    w, h = spec['w'], spec['h']
    pg = browser().new_page(viewport={'width': max(1, int(round(w))), 'height': max(1, int(round(h)))}, device_scale_factor=scale)
    css = ';'.join(f"{''.join('-' + c.lower() if c.isupper() else c for c in k)}:{v}" for k, v in spec['css'].items())
    f = SITE + '/_ras.html'
    open(f, 'w', encoding='utf8').write(f'<html><body style="margin:0;background:transparent">'
                   f'<style>#x{{width:{w}px;height:{h}px;{css}}}</style><div id="x"></div></body></html>')
    pg.goto(Path(f).as_uri())
    pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(100)
    pg.screenshot(path=out, omit_background=True, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
    pg.close()


if __name__ == '__main__':
    d = extract(sys.argv[1])
    json.dump(d, open(HERE + '/x_' + sys.argv[1] + '.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(json.dumps(d, ensure_ascii=False)[:3000])
