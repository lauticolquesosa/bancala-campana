import os,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__)); SITE=S+'/site'; OUT=S+'/out'
_pw=None;_b=None
def browser():
    global _pw,_b
    if _b is None: _pw=sync_playwright().start(); _b=_pw.chromium.launch()
    return _b
def page_html(body,w,h,css=''):
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>
    html,body{{width:{w}px;height:{h}px;overflow:hidden}} {css}</style></head><body><div class="pc" style="width:{w}px;height:{h}px">{body}</div>
    <script src="bounce.js"></script></body></html>'''
def render(name,body,w,h,out,scale=1,css='',fmt='png',quality=92,transparent=False):
    f=f'{SITE}/{name}.html'; open(f,'w',encoding='utf8').write(page_html(body,w,h,css))
    pg=browser().new_page(viewport={'width':w,'height':h},device_scale_factor=scale)
    pg.goto(Path(f).as_uri()); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(150)
    os.makedirs(os.path.dirname(out),exist_ok=True)
    if fmt=='jpg': pg.screenshot(path=out,type='jpeg',quality=quality,clip={'x':0,'y':0,'width':w,'height':h})
    else: pg.screenshot(path=out,clip={'x':0,'y':0,'width':w,'height':h},omit_background=transparent)
    pg.close(); return out
P='../plates/'; Q='../quito/'; B='../brand/'
def logos(h,v='blanco',gap=1.0):
    col='#fff' if v=='blanco' else 'var(--navy)'
    bv='bancala_blanco' if v=='blanco' else 'bancala_color'
    uv='ucasal_blanco' if v=='blanco' else 'ucasal_color'
    sv='ucasal_sustentable_blanco' if v=='blanco' else 'ucasal_sustentable_color'
    return (f'<div class="logos" style="color:{col};font-size:{h*gap}px"><img src="{B}{bv}.svg" style="height:{h}px">'
            f'<div class="sep"></div><img src="{B}{sv}.png" style="height:{h*1.12}px">'
            f'<div class="sep"></div><img src="{B}{uv}.svg" style="height:{h*0.62}px"></div>')
