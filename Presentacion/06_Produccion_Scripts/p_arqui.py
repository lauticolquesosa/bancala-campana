from lib import *
import numpy as np, cv2
from PIL import Image
D=OUT+'/02_Piezas/03_Arquigrafia_Estacion_Bancala'
ART=S+'/art'; os.makedirs(ART,exist_ok=True)

def stickers():
    """Quito con borde blanco troquelado (stickers + corporeo)."""
    os.makedirs(S+'/stickers',exist_ok=True)
    for p in ['saludo','enojado','sentado_feliz','tapandose','llorando','limpiando','senalando_feliz','juntando_basura','paraguas','policia']:
        im=Image.open(f'{S}/quito/q_{p}.png').convert('RGBA'); im.thumbnail((900,900),Image.LANCZOS)
        a=np.array(im); al=a[...,3]; pad=int(max(im.size)*0.06)
        A=np.zeros((al.shape[0]+2*pad,al.shape[1]+2*pad),np.uint8); A[pad:-pad,pad:-pad]=al
        r=int(max(im.size)*0.035)
        k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*r+1,2*r+1))
        m=cv2.dilate((A>40).astype(np.uint8),k)
        m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(r*3|1,r*3|1)))
        cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        m=np.zeros_like(m); cv2.drawContours(m,cs,-1,1,-1)
        base=np.zeros((A.shape[0],A.shape[1],4),np.uint8); base[...,:3]=255; base[...,3]=cv2.GaussianBlur(m.astype(np.float32)*255,(0,0),1.0).astype(np.uint8)
        # thin cut line
        edge=cv2.morphologyEx(m,cv2.MORPH_GRADIENT,np.ones((3,3),np.uint8)).astype(bool)
        base[edge,:3]=(225,222,215)
        out=Image.fromarray(base); top=Image.new('RGBA',out.size,(0,0,0,0)); top.paste(im,(pad,pad),im)
        out.alpha_composite(top); out.save(f'{S}/stickers/st_{p}.png')
    print('stickers ok')

def flat_arts():
    # Panel del refugio (proporcion 419x628)
    W,H=838,1256
    render('panel',f'''<div class="abs" style="inset:0;background:var(--navy)"></div><div class="abs trama-b" style="inset:0;opacity:.13;background-size:700px auto"></div>
<div class="abs" style="left:56px;top:46px">{logos(30)}</div>
<div class="abs dsp bounce" data-k=".6" style="left:54px;top:130px;font-size:96px;line-height:.95">Mucho más<br>que un banco.</div>
<div class="abs body b7" style="left:58px;top:355px;width:700px;font-size:30px;color:#fff;text-shadow:0 0 6px var(--navy),0 0 12px var(--navy),0 0 18px var(--navy)">Sentate con Quito, sacate una foto y contá tu historia en el Muro.</div>
<div class="abs" style="left:58px;right:58px;top:560px;height:420px;border:6px dashed rgba(255,255,255,.5);border-radius:30px"></div>
<div class="abs dsp" style="left:58px;top:432px;font-size:44px;color:var(--mint)">#TeBancoEnTodas</div>''',W,H,f'{ART}/panel.png',scale=1.5)
    # Vinilo de piso (circulo + huellas) 1600x700
    steps=''.join(f'<div class="abs" style="left:{x}px;top:{y}px;width:70px;height:120px;border-radius:40px 40px 34px 34px;background:var(--mint);border:6px solid var(--ink);transform:rotate({r}deg)"></div>' for x,y,r in [(90,520,-20),(230,470,-10),(370,500,-14),(510,440,-6)])
    render('piso',f'''<div class="abs" style="inset:0;background:transparent"></div>{steps}
<div class="abs" style="left:640px;top:40px;width:620px;height:620px;border-radius:50%;background:var(--blue);border:10px solid var(--ink)"></div>
<div class="abs dsp" style="left:640px;width:620px;top:200px;text-align:center;font-size:80px;line-height:1">Sentate,<br>te<br>bancamos.</div>
<div class="abs" style="left:1300px;top:250px;padding:20px 30px;border-radius:24px;background:var(--wood);border:8px solid var(--ink);font:800 40px/1.05 Brico;color:var(--ink)">Tacho<br>a 10 pasos →</div>''',1600,700,f'{ART}/piso.png',scale=1,css='body{background:transparent}',transparent=True)
    # Placa para bancos existentes 1200x420
    render('placa',f'''<div class="abs" style="inset:0;background:#fff;border-radius:36px;border:10px solid var(--ink)"></div>
<img class="abs" src="{Q}q_saludo.png" style="left:30px;top:40px;height:340px">
<div class="abs" style="left:380px;top:46px"><div class="body b7" style="font-size:28px;color:var(--green)">Hola, soy un banco de la facu.</div>
<div class="dsp" style="font-size:92px;margin-top:6px;color:var(--blue)">Te banco<br>en todas.</div>
<div class="body b7" style="font-size:28px;color:var(--ink);margin-top:14px">¿Me ves roto? Escaneá y avisá.</div></div>
<div class="abs" style="right:40px;top:90px;width:240px;height:240px;background:#fff;border:6px solid var(--ink);border-radius:20px;padding:12px"><img src="{B}qr_banco.svg" style="width:100%;height:100%"></div>
<div class="abs" style="right:48px;bottom:30px"><img src="{B}bancala_color.svg" style="height:40px"></div>''',1200,420,f'{ART}/placa.png',scale=1,css='body{background:transparent}',transparent=True)
    # Tablero de la mesa "Muro de historias" 1800x800
    opts=[('Rayarlo','var(--blue)'),('Pararse encima','var(--green)'),('Dejarle basura','var(--wood)'),('Arrastrarlo','var(--navy)')]
    oh=''.join(f'''<div style="display:flex;align-items:center;gap:18px;margin-bottom:22px"><div style="width:250px;font:800 34px Brico;color:var(--ink)">{t}</div>
      <div style="flex:1;height:64px;border-radius:14px;background:repeating-linear-gradient(90deg,{c} 0 4px,transparent 4px 64px),#fff;border:5px solid var(--ink)"></div></div>''' for t,c in opts)
    render('mesa',f'''<div class="abs" style="inset:0;background:var(--paper)"></div><div class="abs trama-n" style="inset:0;opacity:.05"></div>
<div class="abs" style="left:40px;top:40px;width:1000px;bottom:40px;border-radius:30px;background:#2f4a3c;border:8px solid var(--ink)"></div>
<div class="abs dsp" style="left:80px;top:72px;font-size:84px;color:var(--mint)">Muro de historias</div>
<div class="abs body b7" style="left:84px;top:172px;width:900px;font-size:28px;color:#fff;opacity:.92">Escribí tu historia acá (no en el banco). Tiza o marcador al agua.</div>
<div class="abs" style="left:84px;right:810px;top:240px;bottom:80px;background:repeating-linear-gradient(0deg,rgba(255,255,255,.18) 0 3px,transparent 3px 70px)"></div>
<div class="abs" style="left:1080px;top:40px;right:40px;bottom:40px;border-radius:30px;background:#fff;border:8px solid var(--ink);padding:40px 40px">
 
 <div class="dsp" style="font-size:58px;color:var(--blue);margin:0 0 8px">¿Qué le hace peor a un banco?</div><div class="body b7" style="font-size:28px;color:var(--green);margin-bottom:26px">Votá pegando un sticker.</div>{oh}
 <div class="body" style="font-size:24px;color:var(--ink);opacity:.8">La misma pregunta está en nuestras historias: comparamos los resultados.</div></div>''',1800,800,f'{ART}/mesa.png',scale=1)
    print('flat ok')

def warp(art,quad,W,H):
    h,w=art.shape[:2]
    M=cv2.getPerspectiveTransform(np.float32([[0,0],[w,0],[w,h],[0,h]]),np.float32(quad))
    return cv2.warpPerspective(art,M,(W,H),flags=cv2.INTER_LANCZOS4)

def mockups():
    import sys; sys.path.insert(0,S)
    from comp import Scene, Scene2
    # standee: Quito with foam edge as a "pose"
    Image.open(f'{S}/stickers/st_sentado_feliz.png').save(f'{S}/quito/q_corporeo.png')
    sc=Scene2(13,focus=(470,960),blur=0.005); k=sc.k; H,W=sc.H,sc.W
    pl=sc.plate
    L=pl.mean(2)
    # panel (upper & lower mesh), keep frame bars
    art=np.array(Image.open(f'{ART}/panel.png').convert('RGB')).astype(np.float32)/255
    q=np.array([[266,239],[684,239],[687,866],[263,866]])*k
    wa=warp(art,q,W,H); m=warp(np.ones(art.shape[:2],np.float32),q,W,H)
    bars=np.zeros((H,W),np.float32)
    for y0,y1 in [(489,503),(760,772)]: bars[int(y0*k):int(y1*k)]=1
    m=m*(1-bars)
    shade=np.clip(L/ (cv2.GaussianBlur(L,(0,0),60)+1e-3),0.5,1.15)
    vin=wa*(0.82+0.18*shade[...,None])*0.95+pl*0.05
    pl=pl*(1-m[...,None])+vin*m[...,None]
    # floor vinyl
    fa=np.array(Image.open(f'{ART}/piso.png').convert('RGBA')).astype(np.float32)/255
    q=np.array([[150,1092],[800,1092],[960,1290],[-40,1290]])*k
    wf=warp(fa,q,W,H); af=wf[...,3:4]
    tex=np.clip(L/(cv2.GaussianBlur(L,(0,0),40)+1e-3),0.6,1.3)[...,None]
    lum=cv2.GaussianBlur(L,(0,0),80)[...,None]/max(L.mean(),1e-3)
    fv=wf[...,:3]*(tex**0.5)*np.clip(lum,0.6,1.1)
    pl=pl*(1-af*0.93)+fv*af*0.93
    # placa on bench box front (frontal)
    pa=np.array(Image.open(f'{ART}/placa.png').convert('RGBA')).astype(np.float32)/255
    q=np.array([[520,935],[745,935],[745,1014],[520,1014]])*k
    wp=warp(pa,q,W,H); ap=wp[...,3:4]
    pl=pl*(1-ap)+wp[...,:3]*ap*np.clip(cv2.GaussianBlur(L,(0,0),30)[...,None]/np.percentile(L,90),0.7,1.0)
    sc.plate=pl
    sc.add('corporeo',cx=345,foot=893,height=330,sun=(0.55,-0.08),slen=0.5,hard=0.8,shadow_op=0.6,contact=0.8,ground_band=0.08,ambient=0.25,rim=0.15,grass=0)
    os.makedirs(S+'/mock',exist_ok=True)
    sc.export(S+'/mock/stand',1080/1350,(1080,1350),cy=0.55,seed=5,grain=0.8)
    import shutil; shutil.copy(S+'/mock/stand_full.jpg',S+'/mock/stand_feed.jpg')
    sc.export(S+'/mock/standS',1080/1920,(1080,1920),cx=0.45,seed=5,grain=0.8); shutil.copy(S+'/mock/standS_full.jpg',S+'/mock/stand_story.jpg')
    sc.export(S+'/mock/standP',2400/3200,(2400,3200),seed=5,grain=0.8)
    # mesa mockup on 52
    sc=Scene2(52,focus=(450,850),blur=0.005); k=sc.k; pl=sc.plate; L=pl.mean(2)
    ma=np.array(Image.open(f'{ART}/mesa.png').convert('RGB')).astype(np.float32)/255
    q=np.array([[433,803],[655,851],[419,877],[250,812]])*k  # TL=back TR=right BR=front BL=left
    wm=warp(ma,q,sc.W,sc.H); mm=warp(np.ones(ma.shape[:2],np.float32),q,sc.W,sc.H)
    lum=np.clip(cv2.GaussianBlur(L,(0,0),20)/np.percentile(L,95),0.75,1.05)[...,None]
    sc.plate=pl*(1-mm[...,None])+wm*lum*mm[...,None]
    sc.add('sentado_feliz',cx=760,foot=1090,height=270,sun=(-0.95,0.25),slen=0.9,hard=1,shadow_op=0.85,contact=0.9,ground_band=0.1,ambient=0.33,grass=0.04,rim=0.3)
    sc.export(S+'/mock/mesa',1080/1350,(1080,1350),seed=6,grain=0.8)
    sc.export(S+'/mock/mesaP',2400/3200,(2400,3200),seed=6,grain=0.8)
    print('mock ok')

if __name__=='__main__':
    import sys
    for w in (sys.argv[1:] or ['stickers','flat_arts','mockups']): globals()[w]()
