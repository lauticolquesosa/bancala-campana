import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from comp import *
OUT=S+'/plates'; os.makedirs(OUT,exist_ok=True)
SUN=dict(hard=1.0,shadow_op=0.85,contact=0.9,ground_band=0.1,ambient=0.33,grass=0.04,rim=0.3)
SOFT=dict(hard=0.3,shadow_op=0.5,contact=0.95,ground_band=0.12,ambient=0.4,grass=0.04,rim=0.12,shade=0.10,slen=0.45)
SC={
 'hola44':(44,[('saludo',dict(cx=1040,foot=950,height=270,sun=(0.75,0.22),slen=0.8,**SUN))],{'feed':.66,'story':.72}),
 'quito52':(52,[('saludo',dict(cx=740,foot=1090,height=285,sun=(-0.95,0.25),slen=0.9,**SUN))],{'feed':.5,'story':.6}),
 'playa29':(29,[('tapandose',dict(cx=215,foot=1236,height=370,sun=(-0.35,0.22),**SOFT))],{'a3':.5,'feed':.5,'story':.45}),
 'pelu33':(33,[('paraguas',dict(cx=700,foot=1236,height=450,sun=(-0.35,0.22),**SOFT))],{'a3':.5,'feed':.5,'story':.6}),
 'cuaderno41':(41,[('enojado',dict(cx=215,foot=1236,height=350,flip=True,sun=(-0.35,0.22),**SOFT))],{'a3':.5,'feed':.5,'story':.4}),
 'mudanza10':(10,[('llorando',dict(cx=830,foot=1240,height=320,sun=(-0.35,0.22),**SOFT))],{'a3':.5,'feed':.5,'story':.6}),
 'charla23':(23,[('sentado_feliz',dict(cx=560,foot=1010,height=290,sun=(-0.35,0.22),**SOFT))],{'a3':.5,'feed':.5,'story':.55}),
 'mante53':(53,[('limpiando',dict(cx=775,foot=1238,height=360,sun=(-0.85,0.3),slen=0.85,**SUN))],{'feed':.6,'story':.62}),
 'primer53':(53,[('preocupado_sentado',dict(cx=780,foot=1236,height=330,sun=(-0.85,0.3),slen=0.85,**SUN))],{'feed':.6,'story':.62}),
 'siesta26':(26,[('sentado_feliz',dict(cx=300,foot=1235,height=300,sun=(-0.35,0.22),**SOFT))],{'feed':.5,'story':.45}),
 'mesa16':(16,[('sentado_feliz',dict(cx=225,foot=922,height=210,sun=(-0.95,0.18),slen=0.9,**SUN))],{'feed':.45,'story':.4}),
 'almuerzo51':(51,[('juntando_basura',dict(cx=760,foot=1205,height=290,sun=(-0.6,0.3),slen=0.8,**SUN))],{'feed':.6,'story':.65}),
}
FMT={'a3':(2480,3208),'feed':(1080,1350),'story':(1080,1920)}
only=[a for a in sys.argv[1:] if not a.startswith('--')]
fonly=[a[2:] for a in sys.argv[1:] if a.startswith('--')]
for name,(ph,actors,fmts) in SC.items():
    if only and name not in only: continue
    sc=Scene(ph)
    for pose,kw in actors: sc.add(pose,**kw)
    for f,cx in fmts.items():
        if fonly and f not in fonly: continue
        W,H=FMT[f]; sc.export(f'{OUT}/{name}_{f}',W/H,(W,H),cx=cx,cy=0.5,seed=hash(name)%1000,grain=0.85)
    print('ok',name,flush=True)
