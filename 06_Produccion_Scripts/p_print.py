from lib import *
import shutil
ICON={
 'mochila':'<rect x="18" y="22" width="44" height="50" rx="12"/><path d="M28 22v-6a12 12 0 0 1 24 0v6M18 44h44M34 44v8h12v-8"/>',
 'mate':'<path d="M22 34h36l-4 30a10 10 0 0 1-10 8h-8a10 10 0 0 1-10-8z"/><path d="M48 34 60 8M56 8h8"/><path d="M26 44h28"/>',
 'birrete':'<path d="M8 32 40 18l32 14-32 14z"/><path d="M22 38v14c10 8 26 8 36 0V38M72 32v18"/>',
 'luna':'<path d="M50 14a26 26 0 1 0 16 40A22 22 0 0 1 50 14z"/><path d="M58 18h10l-10 10h10"/>',
 'corazon':'<path d="M40 66S12 48 12 30a14 14 0 0 1 28-6 14 14 0 0 1 28 6c0 18-28 36-28 36z"/>',
}
def icon(n,c='var(--ink)',s=74):
    return f'<svg viewBox="0 0 80 80" width="{s}" height="{s}" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">{ICON[n]}</svg>'

def infografia():
    W,H=1240,1754
    pos=[('mochila','Aprender acompañado siempre vale más.'),('birrete','Cada logro se celebra mejor juntos.'),('mate','Pequeños momentos que también construyen historias.'),
         ('luna','Un lugar para estar cuando alguien lo necesita.'),('corazon','Donde la amistad se hace encuentro.')]
    ph=''.join(f'<div style="width:204px;text-align:center"><div style="width:108px;height:108px;margin:0 auto;border-radius:50%;background:var(--mint);border:5px solid var(--ink);display:flex;align-items:center;justify-content:center">{icon(n)}</div><div class="body b7" style="font-size:20px;line-height:1.16;color:var(--ink);margin-top:12px">{t}</div></div>' for n,t in pos)
    qx,qy,qw,qh=345,742,550,530
    anc={'respaldo':(0.29,0.17),'asiento':(0.22,0.42),'zapa':(0.33,0.86),'bolso':(0.9,0.62),'cara':(0.56,0.26)}
    A={k:(qx+v[0]*qw,qy+v[1]*qh) for k,v in anc.items()}
    calls=[('respaldo','L',750,'Rayarla también la daña.','El respaldo es para tu espalda, no para tu fibrón.'),
           ('asiento','L',930,'No es para cualquier uso.','Se sienta: no se para, no es cama ni reposera.'),
           ('zapa','L',1110,'No me dejes en la nada.','Si lo movés, devolvelo a su lugar.'),
           ('cara','R',750,'Que nadie se sienta menos.','El banco es de todos: no lo vuelvas un lugar de conflicto.'),
           ('bolso','R',1000,'No todo da lo mismo.','La basura y los chicles, al tacho.')]
    lines='';boxes=''
    for k,side,y,t,sub in calls:
        ax,ay=A[k]
        bx=315 if side=='L' else 925
        lines+=f'<path d="M{bx} {y+22} L{(bx+ax)/2 if side=="L" else (bx+ax)/2} {y+22} L{ax} {ay}" fill="none" stroke="#3a1d0c" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round"/><circle cx="{ax}" cy="{ay}" r="11" fill="var(--blue)" stroke="#3a1d0c" stroke-width="4"/><circle cx="{bx}" cy="{y+22}" r="6" fill="#3a1d0c"/>'
        x=70 if side=='L' else 945
        boxes+=f'<div class="abs" style="left:{x}px;top:{y}px;width:230px;text-align:{"right" if side=="L" else "left"}"><div class="body" style="font-weight:800;font-size:25px;line-height:1.08;color:var(--blue)">{t}</div><div class="body" style="font-size:19px;line-height:1.2;color:var(--ink);margin-top:6px">{sub}</div></div>'
    gest=[('Sentate,<br>no te pares.','sentado_feliz'),('La basura,<br>al tacho.','juntando_basura'),('Si lo movés,<br>devolvelo.','senalando_feliz')]
    gh=''.join(f'<div style="flex:1;display:flex;flex-direction:column;align-items:flex-start;gap:12px"><div style="flex:none;width:96px;height:96px;border-radius:50%;background:#fff;border:4px solid var(--ink);display:flex;align-items:center;justify-content:center;overflow:hidden"><img src="{Q}q_{q}.png" style="height:80px"></div><div class="body" style="font-weight:800;font-size:23px;line-height:1.1;color:var(--ink)">{t}</div></div>' for t,q in gest)
    body=f'''<div class="abs" style="inset:0;background:var(--paper)"></div>
<div class="abs" style="right:70px;top:56px">{logos(34,'color')}</div>
<div class="abs dsp bounce" data-k=".5" style="left:66px;top:112px;font-size:104px;color:var(--blue)">La misma banca.</div>
<div class="abs dsp bounce" data-k=".5" style="left:66px;top:214px;font-size:100px;color:var(--mint)">Distintas historias.</div>
<div class="abs" style="left:70px;top:378px;display:flex;align-items:center;gap:14px"><span class="dsp thin" style="font-size:54px;color:var(--mint)">+</span><span class="body" style="font-weight:800;font-size:30px;color:var(--ink)">Lo que te banca</span><span style="width:820px;height:3px;background:var(--ink);opacity:.2"></span></div>
<div class="abs" style="left:70px;right:70px;top:448px;display:flex;justify-content:space-between">{ph}</div>
<div class="abs" style="left:70px;top:676px;display:flex;align-items:center;gap:14px"><span class="dsp thin" style="font-size:54px;color:var(--blue)">−</span><span class="body" style="font-weight:800;font-size:30px;color:var(--ink)">Lo que no se banca: manual de uso de Quito</span></div>
<div class="abs" style="left:{qx+30}px;top:{qy+qh-30}px;width:{qw-60}px;height:60px;border-radius:50%;background:radial-gradient(closest-side,rgba(58,29,12,.22),rgba(58,29,12,0))"></div>
<img class="abs" src="{Q}q_saludo.png" style="left:{qx}px;top:{qy}px;width:{qw}px;height:{qh}px">
<svg class="abs" style="left:0;top:0" width="{W}" height="{H}">{lines}</svg>{boxes}
<div class="abs" style="left:70px;right:70px;top:1306px;height:3px;background:var(--ink);opacity:.15"></div>
<div class="abs" style="left:70px;top:1334px;width:660px">
 <div class="body" style="font-weight:800;font-size:24px;color:var(--green)">Tres gestos que bancan</div>
 <div style="display:flex;gap:18px;margin-top:18px">{gh}</div></div>
<div class="abs" style="left:780px;top:1334px;width:390px;display:flex;gap:20px">
 <div><div class="body" style="font-weight:800;font-size:24px;color:var(--green)">Detrás de cada banco</div>
 <div class="body b7" style="font-size:22px;color:var(--ink);margin-top:12px;line-height:1.2">Lijar, pintar, ajustar y reparar: el trabajo de Mantenimiento.<br><span style="color:var(--blue)">¿Viste uno roto? Escaneá y avisá.</span></div></div>
 <div style="flex:none;width:130px;height:130px;background:#fff;border:4px solid var(--ink);border-radius:14px;padding:8px"><img src="{B}qr_banco.svg" style="width:100%;height:100%"></div></div>
<div class="abs" style="left:0;right:0;top:1604px;height:150px;background:var(--navy)"></div>
<div class="abs dsp" style="left:70px;top:1640px;font-size:54px;color:#fff">Cuidala más que a tu mamá.</div>
<div class="abs body" style="left:72px;top:1706px;font-size:22px;font-weight:700;color:var(--mint)">(Bueno, casi.) #TeBancoEnTodas</div>
<div class="abs" style="right:70px;top:1604px;height:150px;display:flex;align-items:center"><img src="{B}bancala_blanco.svg" style="height:58px"></div>'''
    d=OUT+'/02_Piezas/02_Impresos/Infografia_A3'
    render('info',body,W,H,f'{d}/Infografia_A3_La_misma_banca_distintas_historias.png',scale=2)
    render('info',body,W,H,f'{d}/Infografia_A3_preview_web.jpg',scale=0.87,fmt='jpg')

def stickers_sheet():
    W,H=1240,1754
    items=[('saludo',90,250,420,-5),('enojado',600,230,380,6),('sentado_feliz',140,720,400,4),('tapandose',640,690,380,-4),('llorando',110,1180,380,-6),('limpiando',650,1160,380,5)]
    st=''.join(f'<img class="abs" src="../stickers/st_{p}.png" style="left:{x}px;top:{y}px;height:{h}px;transform:rotate({r}deg)">' for p,x,y,h,r in items)
    txt=[('Te banco<br>en todas.',520,580,'var(--mint)',-8),('Bancala.',470,1090,'var(--blue)',6),('No me<br>rayes.',520,1560,'var(--wood)',-4)]
    tt=''.join(f'<div class="abs" style="left:{x}px;top:{y}px;transform:rotate({r}deg);background:#fff;border-radius:40px;padding:18px 28px;box-shadow:0 0 0 3px #e1ded7"><div class="dsp thin" style="font-size:56px;color:{c}">{t}</div></div>' for t,x,y,c,r in txt)
    body=f'''<div class="abs" style="inset:0;background:#e6e2d8"></div>
<div class="abs dsp" style="left:66px;top:100px;font-size:72px;color:var(--blue)">Pegalos en tu compu.</div>
{st}{tt}<div class="abs" style="left:70px;bottom:50px">{logos(28,'color')}</div>'''
    render('stk',body,W,H,OUT+'/02_Piezas/02_Impresos/Stickers/Stickers_Plancha_A4.png',scale=2)

def arqui_files():
    D=OUT+'/02_Piezas/03_Arquigrafia_Estacion_Bancala'
    os.makedirs(D,exist_ok=True)
    A=S+'/art'
    pairs=[('panel.png','01_Panel_Refugio_Rojo/Panel_Refugio_Arte_Final.png'),('../mock/standP_full.jpg','01_Panel_Refugio_Rojo/Panel_Refugio_Mockup.jpg'),
           ('../stickers/st_sentado_feliz.png','02_Corporeo_Quito/Corporeo_Quito_Arte_Final.png'),
           ('piso.png','03_Vinilo_de_Piso/Vinilo_Piso_Arte_Final.png'),
           ('mesa.png','04_Mesa_Muro_de_Historias/Mesa_Vinilo_Tablero_Arte_Final.png'),('../mock/mesaP_full.jpg','04_Mesa_Muro_de_Historias/Mesa_Vinilo_Tablero_Mockup.jpg'),
           ('placa.png','05_Placa_Bancos_Existentes/Placa_Banco_Arte_Final.png')]
    for a,b in pairs:
        os.makedirs(os.path.dirname(f'{D}/{b}'),exist_ok=True); shutil.copy(f'{A}/{a}',f'{D}/{b}')
    # copia del mockup general en 02 y 03 y 05 (mismo stand)
    for sub,nm in [('02_Corporeo_Quito','Corporeo_Quito_Mockup.jpg'),('03_Vinilo_de_Piso','Vinilo_Piso_Mockup.jpg'),('05_Placa_Bancos_Existentes','Placa_Banco_Mockup.jpg')]:
        shutil.copy(S+'/mock/standP_full.jpg',f'{D}/{sub}/{nm}')
    plano(D+'/00_Plano_Estacion_Bancala.png')

def plano(out):
    W,H=1600,1000
    num=lambda n,x,y,c='var(--blue)':f'<div class="abs" style="left:{x-26}px;top:{y-26}px;width:52px;height:52px;border-radius:50%;background:{c};border:4px solid var(--ink);display:flex;align-items:center;justify-content:center;font:800 26px Brico;color:#fff">{n}</div>'
    benches=''.join(f'<div class="abs" style="left:{x}px;top:{y}px;width:120px;height:40px;border-radius:8px;background:#d89a5a;border:4px solid var(--ink)"></div><div class="abs" style="left:{x+40}px;top:{y+8}px;width:40px;height:24px;border-radius:5px;background:#fff;border:3px solid var(--ink)"></div>' for x,y in [(120,190),(330,190),(1000,190),(1210,190),(1360,560)])
    body=f'''<div class="abs" style="inset:0;background:var(--paper)"></div>
<div class="abs" style="left:0;right:0;top:250px;height:150px;background:#ddd6c8"></div>
<div class="abs kick" style="left:40px;top:312px;font-size:20px;color:var(--ink);opacity:.6">Pasillo de circulación</div>
<div class="abs" style="left:560px;top:430px;width:480px;height:110px;background:#e94c3d;border:5px solid var(--ink);border-radius:6px"></div>
<div class="abs" style="left:575px;top:445px;width:450px;height:24px;background:var(--navy)"></div>
<div class="abs" style="left:575px;top:480px;width:450px;height:46px;background:#c8874b;border:3px solid var(--ink)"></div>
<div class="abs kick" style="left:560px;top:400px;font-size:18px;color:var(--ink)">Refugio rojo existente</div>
<div class="abs" style="left:650px;top:640px;width:300px;height:300px;border-radius:50%;border:5px dashed var(--blue)"></div>
{''.join(f'<div class="abs" style="left:{x}px;top:{y}px;width:22px;height:36px;border-radius:12px;background:var(--mint);border:3px solid var(--ink);transform:rotate({r}deg)"></div>' for x,y,r in [(560,410-0,0)][:0])}
{''.join(f'<div class="abs" style="left:{x}px;top:{y}px;width:24px;height:38px;border-radius:12px;background:var(--mint);border:3px solid var(--ink)"></div>' for x,y in [(790,360),(760,580),(810,600)])}
<div class="abs" style="left:1090px;top:620px;width:280px;height:150px;background:#e94c3d;border:5px solid var(--ink);border-radius:6px"></div>
<div class="abs" style="left:1105px;top:635px;width:250px;height:120px;background:#fff;border:3px solid var(--ink)"></div>
<div class="abs" style="left:1090px;top:580px;width:280px;height:30px;background:#c8874b;border:4px solid var(--ink)"></div>
<div class="abs" style="left:1090px;top:780px;width:280px;height:30px;background:#c8874b;border:4px solid var(--ink)"></div>
<div class="abs kick" style="left:1090px;top:830px;font-size:18px;color:var(--ink)">Mesa roja existente</div>
<div class="abs" style="left:400px;top:600px;width:60px;height:70px;border-radius:10px;background:var(--green);border:4px solid var(--ink)"></div>
<div class="abs kick" style="left:360px;top:680px;font-size:18px;color:var(--ink)">Tacho</div>
{benches}
{num(1,800,420)}{num(2,700,500,'var(--wood)')}{num(3,800,790,'var(--green)')}{num(4,1230,690)}{num(5,180,170,'var(--navy)')}
<div class="abs" style="left:40px;top:40px"><div class="dsp" style="font-size:64px;color:var(--blue);margin-top:6px">Estación Bancala</div></div>
<div class="abs" style="left:40px;top:740px;width:320px">{"".join(f'<div style="display:flex;gap:10px;margin-bottom:8px;font:600 19px Brico;color:var(--ink)"><b style="color:var(--blue)">{n}</b>{t}</div>' for n,t in [(1,'Panel vinílico microperforado en el refugio'),(2,'Corpóreo de Quito sentado: zona de foto'),(3,'Vinilo de piso: huellas + “Sentate, te bancamos”'),(4,'Vinilo de tablero: Muro de historias + encuesta'),(5,'Placas con QR en los bancos del recorrido')])}</div>'''
    render('plano',body,W,H,out,scale=1.5)

if __name__=='__main__':
    import sys
    for w in (sys.argv[1:] or ['infografia','stickers_sheet','arqui_files']): globals()[w](); print('ok',w,flush=True)
