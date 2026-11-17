import json
from lib import *
P2='../plates2/'
FMTS={'feed':dict(W=1080,H=1350,top=150,ph=1200,sc=1,m=64,hs=112,bs=30),
      'story':dict(W=1080,H=1920,top=480,ph=1440,sc=1,m=64,hs=128,bs=36),
      'poster':dict(W=1240,H=1754,top=154,ph=1450,sc=.5,m=84,hs=140,bs=34)}
def info(plate,fmt): return json.load(open(f'{S}/plates2/{plate}_{fmt}.json'))
def bubble(plate,fmt,text,w=None,fs=None,dx=0,gap=None):
    F=FMTS[fmt]; i=info(plate,fmt); sc=F['sc']
    fs=fs or F['bs']; w=w or int(fs*11.5)
    hx=i['headx']*sc+dx; top=i['top']*sc+F['top']
    gap=gap if gap is not None else fs*0.95
    x=max(F['m'],min(F['W']-F['m']-w,hx-w/2))
    tx=max(fs*1.1,min(w-fs*1.6,hx-x))-fs*0.5
    bottom=F['H']-(top-gap)
    return f'<div class="bub" style="left:{x:.0f}px;bottom:{bottom:.0f}px;width:{w}px;font-size:{fs}px">{text}<i class="tail" style="left:{tx:.0f}px"></i></div>'
def photo_piece(fmt,plate,head,lede=None,bub=None,extra='',footer=True,hs=None,header_extra=''):
    F=FMTS[fmt]; W,H,top,ph,m=F['W'],F['H'],F['top'],F['ph'],F['m']; hs=hs or F['hs']
    ht=70 if fmt=='feed' else (250 if fmt=='story' else 84)
    led=f'<div class="lede" style="margin-top:{hs*0.22:.0f}px;font-size:{F["bs"]-2}px;max-width:{W-2*m-40}px">{lede}</div>' if lede else ''
    logos_top=f'<div class="abs" style="left:{m}px;top:150px">{logos(28)}</div>' if fmt=='story' else ''
    foot=''
    if footer and fmt=='feed':
        foot=f'<div class="abs" style="left:0;right:0;bottom:0;height:240px;background:linear-gradient(0deg,rgba(17,40,72,.62),rgba(17,40,72,0))"></div><div class="abs" style="left:{m}px;bottom:46px">{logos(30)}</div>'
    if fmt=='poster':
        foot=f'''<div class="abs" style="left:0;right:0;top:1604px;height:150px;background:var(--navy)"></div>
<div class="abs" style="left:{m}px;top:1604px;height:150px;display:flex;align-items:center">{logos(42)}</div>
<div class="abs" style="right:{m}px;top:1604px;height:150px;display:flex;flex-direction:column;justify-content:center;align-items:flex-end">
<div class="hl" style="font-size:32px;color:var(--mint)">Mucho más que un banco.</div><div class="lede" style="font-size:21px;margin-top:6px;opacity:.85;font-weight:700">#TeBancoEnTodas</div></div>'''
    return f'''<div class="abs" style="inset:0;background:var(--navy)"></div>
<img class="abs fade" src="{P2}{plate}_{fmt}_bg.jpg" style="left:0;top:{top}px;width:{W}px;height:{ph}px">
{logos_top}
<div class="abs" style="left:{m}px;top:{ht}px;right:{m}px"><div class="hl bounce" data-k=".55" style="font-size:{hs}px">{head}</div>{led}{header_extra}</div>
<img class="abs" src="{P2}{plate}_{fmt}_fg.png" style="left:0;top:{top}px;width:{W}px;height:{ph}px">
{foot}{bub or ''}{extra}'''
