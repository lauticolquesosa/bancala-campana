import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from comp import *
OUT=S+'/plates2'; os.makedirs(OUT,exist_ok=True)
SUN=dict(hard=1.0,shadow_op=0.85,contact=0.9,ground_band=0.1,ambient=0.33,grass=0.04,rim=0.3)
SOFT=dict(hard=0.3,shadow_op=0.5,contact=0.95,ground_band=0.12,ambient=0.4,grass=0.04,rim=0.12,shade=0.10,slen=0.45)
FMT={'poster':(2480,2900),'feed':(1080,1200),'story':(1080,1440)}
# name: (photo, focus, actors, {fmt:(cx,cy,zoom)})
SC={
 'hola44':(44,(1040,930),[('saludo',dict(cx=1030,foot=905,height=250,sun=(0.75,0.22),slen=0.8,**SUN))],{'feed':(.62,.95,1),'story':(.66,.6,1)}),
 'quito52':(52,(600,1000),[('saludo',dict(cx=740,foot=1090,height=285,sun=(-0.95,0.25),slen=0.9,**SUN))],{'feed':(.5,.95,1),'story':(.55,.75,1)}),
 'playa29':(29,(520,900),[('tapandose',dict(cx=215,foot=1236,height=370,sun=(-0.35,0.22),**SOFT))],{'poster':(.5,.95,1),'feed':(.5,.95,1)}),
 'pelu33':(33,(470,880),[('paraguas',dict(cx=700,foot=1236,height=450,sun=(-0.35,0.22),**SOFT))],{'poster':(.5,.95,1),'feed':(.5,.95,1)}),
 'cuaderno41':(41,(600,900),[('enojado',dict(cx=215,foot=1236,height=350,flip=True,sun=(-0.35,0.22),**SOFT))],{'poster':(.5,.95,1),'feed':(.5,.95,1),'story':(.45,.6,1)}),
 'mudanza10':(10,(450,950),[('llorando',dict(cx=830,foot=1240,height=320,sun=(-0.35,0.22),**SOFT))],{'poster':(.5,.95,1),'feed':(.5,.95,1)}),
 'charla23':(23,(560,800),[('sentado_feliz',dict(cx=560,foot=1010,height=290,sun=(-0.35,0.22),**SOFT))],{'poster':(.5,.95,1),'story':(.55,.6,1)}),
 'historias25':(25,(560,900),[('senalando_feliz',dict(cx=790,foot=1050,height=265,sun=(-0.35,0.22),**SOFT))],{'feed':(.5,.95,1)}),
 'mante53':(53,(720,1150),[('limpiando',dict(cx=775,foot=1238,height=360,sun=(-0.85,0.3),slen=0.85,**SUN))],{'feed':(.6,.95,1)}),
 'primer53':(53,(720,1150),[('preocupado_sentado',dict(cx=780,foot=1236,height=330,sun=(-0.85,0.3),slen=0.85,**SUN))],{'feed':(.6,.95,1),'story':(.62,.6,1)}),
 'siesta26':(26,(620,900),[('sentado_feliz',dict(cx=300,foot=1235,height=300,sun=(-0.35,0.22),**SOFT))],{'feed':(.5,.95,1),'story':(.45,.6,1)}),
 'mesa16':(16,(330,950),[('sentado_feliz',dict(cx=225,foot=922,height=210,sun=(-0.95,0.18),slen=0.9,**SUN))],{'feed':(.45,.95,1)}),
 'almuerzo51':(51,(600,1000),[('juntando_basura',dict(cx=760,foot=1205,height=290,sun=(-0.6,0.3),slen=0.8,**SUN))],{'feed':(.6,.95,1)}),
}
BLUR={'hola44':0.0022,'quito52':0.0035,'mesa16':0.0035,'almuerzo51':0.0045}
if __name__=='__main__':
    only=sys.argv[1:]
    for name,(ph,foc,actors,fmts) in SC.items():
        if only and name not in only: continue
        sc=Scene2(ph,focus=foc,blur=BLUR.get(name,0.0065))
        for pose,kw in actors: sc.add(pose,**kw)
        for f,(cx,cy,z) in fmts.items():
            W,H=FMT[f]; sc.export2(f'{OUT}/{name}_{f}',W/H,(W,H),cx=cx,cy=cy,zoom=z,seed=hash(name)%1000,grain=0.8)
        print('ok',name,flush=True)
