from tpl import *
import sys,shutil
FW,FH=1080,1350; SW,SH=1080,1920
R=OUT+'/02_Piezas/01_Redes_Instagram'
IMP=OUT+'/02_Piezas/02_Impresos'

def foot(v='blanco',m=64,b=46,h=30):
    return f'<div class="abs" style="left:{m}px;bottom:{b}px">{logos(h,v)}</div>'
def flat(bg,trama='b',op=.12):
    t=f'<div class="abs trama-{trama}" style="inset:0;opacity:{op}"></div>' if trama else ''
    return f'<div class="abs" style="inset:0;background:{bg}"></div>{t}'
def quito(pose,x,y,h,flip=False,shadow=True):
    sh=f'<div class="abs" style="left:{x}px;top:{y+h*0.9}px;width:{h*1.05}px;height:{h*0.13}px;border-radius:50%;background:radial-gradient(closest-side,rgba(42,40,41,.30),rgba(42,40,41,0))"></div>' if shadow else ''
    return f'{sh}<img class="abs" src="{Q}q_{pose}.png" style="left:{x}px;top:{y}px;height:{h}px;{"transform:scaleX(-1)" if flip else ""}">'
def H(t,x,y,s,c='#fff',k=.55,w=None):
    return f'<div class="abs hl bounce" data-k="{k}" style="left:{x}px;top:{y}px;font-size:{s}px;color:{c};{"width:%dpx;"%w if w else ""}">{t}</div>'
def T(t,x,y,w,s=30,c='#fff',wt=500):
    return f'<div class="abs lede" style="left:{x}px;top:{y}px;width:{w}px;font-size:{s}px;color:{c};font-weight:{wt}">{t}</div>'

# ---------------- AFICHES ----------------
AF=[('Afiche_01_No_soy_reposera','playa29','No soy<br><em>reposera.</em>','¡Tapate un poco, che!',360),
    ('Afiche_02_No_soy_peluqueria','pelu33','No soy<br><em>peluquería.</em>','¡Los pelos van al tacho, no a mí!',400),
    ('Afiche_03_No_soy_tu_cuaderno','cuaderno41','No soy<br><em>tu cuaderno.</em>','¡Eso no es un apunte!',360),
    ('Afiche_04_Si_me_moves_devolveme','mudanza10','Si me movés,<br><em>devolveme.</em>','¿Me llevan… y me traen?',360),
    ('Afiche_05_Te_banco_en_todas','charla23','Te banco<br><em>en todas.</em>','Acá se arreglan los grandes temas del mundo.',420)]
def afiches():
    d=IMP+'/Afiches_A3_Serie_Te_banco_en_todas'
    if os.path.exists(d): shutil.rmtree(d)
    for name,pl,h,b,bw in AF:
        render(name,photo_piece('poster',pl,h,bub=bubble(pl,'poster',b,w=bw)),1240,1754,f'{d}/{name}.png',scale=2)
        print(name,flush=True)

# ---------------- POSTEOS ----------------
def posts():
    d=R+'/Posteos'
    if os.path.exists(d): shutil.rmtree(d)
    render('post1',photo_piece('feed','hola44','Hola,<br><em>soy Quito.</em>',lede='El banquito de los patios de la facu.',
        bub=bubble('hola44','feed','Vengo a pedirte una mano… bueno, una pata.',w=380)),FW,FH,f'{d}/Post_01_Lanzamiento_Hola_soy_Quito.png')
    render('post2',photo_piece('feed','mante53','Los que nos<br><em>bancan a nosotros.</em>',hs=84,lede='Gracias, equipo de Mantenimiento.',
        bub=bubble('mante53','feed','¡Este equipo me deja como nuevo!',w=340)),FW,FH,f'{d}/Post_02_Homenaje_Mantenimiento.png')
    tags=''.join(f'<span class="tag" style="font-size:22px;background:{c};color:{tc}">{t}</span>' for t,c,tc in [('Foto con Quito','var(--mint)','var(--ink)'),('Encuesta en vivo','var(--blue)','#fff'),('Muro de historias','var(--green)','#fff'),('Stickers gratis','var(--wood)','var(--ink)')])
    render('post3',f'''{flat('var(--paper)','n',.05)}
{H('Pasá por la<br>Estación Bancala.',60,70,96,'var(--blue)')}
{T('Martes y jueves, de 10 a 14 h, en el refugio rojo del patio.',64,300,900,30,'var(--ink)',600)}
<div class="abs" style="left:64px;top:390px;width:540px;height:720px;border-radius:30px;overflow:hidden;border:6px solid var(--ink);box-shadow:10px 12px 0 var(--ink);transform:rotate(-2deg)"><img src="../mock/standP_full.jpg" style="width:100%;height:100%;object-fit:cover"></div>
{T('Vestimos el refugio y la mesa que ya están en el patio. Nada nuevo: todo bancado.',660,420,360,29,'var(--ink)',600)}
<div class="abs" style="left:660px;top:640px;width:360px;display:flex;flex-direction:column;align-items:flex-start;gap:14px">{tags}</div>
{foot('color')}''',FW,FH,f'{d}/Post_03_Anuncio_Estacion_Bancala.png')
    items=[('saludo',90,400,300,-6),('enojado',600,360,250,5),('sentado_feliz',380,640,280,-3),('tapandose',80,860,270,4),('llorando',700,700,280,-5)]
    st=''.join(f'<img class="abs" src="../stickers/st_{p}.png" style="left:{x}px;top:{y}px;height:{h}px;transform:rotate({r}deg);filter:drop-shadow(6px 10px 0 rgba(42,40,41,.18))">' for p,x,y,h,r in items)
    render('post4',f'''{flat('var(--blue)','b',.12)}
{H('Pegalos en tu compu.<br><em>No en el banco.</em>',60,70,84)}
{T('Gratis en la Estación Bancala.',64,270,900,30,'#fff',600)}{st}{foot()}''',FW,FH,f'{d}/Post_04_Stickers_Pegalos_en_tu_compu.png')

# ---------------- CARRUSELES ----------------
def car1():
    d=R+'/Carrusel_01_Conoce_a_Quito'
    if os.path.exists(d): shutil.rmtree(d)
    render('c1_1',photo_piece('feed','quito52','Conocé<br><em>a Quito.</em>',hs=130,
        bub=bubble('quito52','feed','¡Hola! ¿Tenés un minuto? Bueno, sentate.',w=330)),FW,FH,f'{d}/Carrusel01_Slide01_Portada.png')
    rows=[('Nombre','Quito, el banquito.'),('Vive en','Patios, pasillos y galerías de la facu.'),('Edad','Más que tu plan de estudios.'),
          ('Le gusta','Los mates, las charlas largas y que lo usen.'),('No se banca','Los fibrones, los chicles y que lo arrastren.'),('Superpoder','Bancarte en todas.')]
    rh=''.join(f'<div style="display:flex;border-top:3px solid var(--ink);padding:16px 0 14px"><div style="width:200px;font:800 25px Brico;color:var(--blue)">{a}</div><div style="flex:1;font:600 30px/1.15 Brico;color:var(--ink)">{b}</div></div>' for a,b in rows)
    render('c1_2',f'''{flat('var(--paper)','n',.05)}{H('¿Quién es?',60,70,110,'var(--blue)')}
<div class="abs" style="left:64px;top:250px;width:600px">{rh}<div style="border-top:3px solid var(--ink)"></div></div>
{quito('sentado_feliz',640,740,470)}''',FW,FH,f'{d}/Carrusel01_Slide02_Ficha.png')
    words=['primeros días','finales aprobados','rondas de mates','chismes','amores','desamores','siestas de diez minutos','“después lo leo”']
    wl=' <span style="color:var(--mint)">·</span> '.join(words)
    render('c1_3',f'''{flat('var(--navy)','b',.09)}{H('Vio de todo.',60,70,120)}
{T(wl,64,250,900,46,'#fff',700)}
{T('En un mismo banco conviven la ansiedad del primer día, el orgullo de recibirse y la calma de una pausa.',64,720,450,29)}
{quito('senalando_feliz',560,760,470)}''',FW,FH,f'{d}/Carrusel01_Slide03_Testigo.png')
    tiles=[('sentado_feliz','Feliz','cuando lo usás para lo que es.','var(--mint)'),('enojado','Enojado','cuando lo rayás.','#ffd36b'),
           ('llorando','Triste','cuando lo dejás lleno de basura.','#9cc3f2'),('tapandose','Avergonzado','cuando lo usás de cama, reposera o peluquería.','#f7c3a0')]
    th=''.join(f'''<div style="position:relative;background:{c};border:4px solid var(--ink);border-radius:28px;box-shadow:7px 9px 0 var(--ink);height:450px;overflow:hidden">
      <img src="{Q}q_{p}.png" style="position:absolute;left:50%;top:24px;height:250px;transform:translateX(-50%)">
      <div style="position:absolute;left:24px;right:20px;top:296px"><div class="hl" style="font-size:44px">{t}</div>
      <div style="font:600 25px/1.12 Brico;color:var(--ink);margin-top:10px">{x}</div></div></div>''' for p,t,x,c in tiles)
    render('c1_4',f'''{flat('var(--paper)','n',.05)}{H('Su humor<br>depende de vos.',60,70,96,'var(--blue)')}
<div class="abs" style="left:64px;right:64px;top:330px;display:grid;grid-template-columns:1fr 1fr;gap:28px">{th}</div>''',FW,FH,f'{d}/Carrusel01_Slide04_Emociones.png')
    render('c1_5',f'''{flat('var(--green)','n',.09)}
{H('Él te banca<br>en todas.',60,80,124)}{H('¿Vos lo<br>bancás?',60,360,124,'var(--mint)')}
{T('Guardá este post y mandáselo a quien todavía usa los bancos de pizarrón.',64,680,430,30,'#fff',600)}
{quito('saludo',520,640,540)}{foot(h=34)}''',FW,FH,f'{d}/Carrusel01_Slide05_Cierre.png')

def car2():
    d=R+'/Carrusel_02_Te_banco_en_todas_menos_en_estas'
    if os.path.exists(d): shutil.rmtree(d)
    render('c2_1',f'''{flat('var(--blue)','b',.13)}
{H('Te banco<br>en todas.',60,80,150)}{H('Menos<br>en estas.',60,390,150,'var(--mint)')}
{quito('tapandose',470,680,570)}{foot()}''',FW,FH,f'{d}/Carrusel02_Slide01_Portada.png')
    S_=[('playa29','No soy<br><em>reposera.</em>','¡Tapate un poco, che!',320,'Reposera'),
        ('pelu33','No soy<br><em>peluquería.</em>','¡Los pelos van al tacho, no a mí!',360,'Peluqueria'),
        ('cuaderno41','No soy<br><em>tu cuaderno.</em>','¡Eso no es un apunte!',320,'Cuaderno'),
        ('mudanza10','Si me movés,<br><em>devolveme.</em>','¿Me llevan… y me traen?',330,'Devolveme')]
    for i,(pl,h,b,bw,n) in enumerate(S_):
        render(f'c2_{i+2}',photo_piece('feed',pl,h,hs=118,bub=bubble(pl,'feed',b,w=bw)),FW,FH,f'{d}/Carrusel02_Slide{i+2:02d}_{n}.png')
    rules=[('Sentate, no te pares.','Las patas son para el piso, no para el asiento.'),('La basura, al tacho.','Siempre hay uno cerca. Quito lo sabe.'),
           ('Si lo movés, devolvelo.','Que ningún banco quede solo en medio de la nada.'),('¿Está roto? Avisá.','Escaneá el QR del banco o avisá a Mantenimiento.')]
    rh=''.join(f'<div style="display:flex;gap:22px;align-items:flex-start;margin-bottom:32px"><div class="hl" style="font-size:58px;color:var(--mint);width:56px">{i+1}</div><div><div style="font:800 38px/1.05 Brico;color:#fff">{a}</div><div style="font:500 26px/1.3 Brico;color:#fff;opacity:.85;margin-top:6px">{b}</div></div></div>' for i,(a,b) in enumerate(rules))
    render('c2_6',f'''{flat('var(--navy)','b',.09)}{H('Bancala.',60,70,150,'var(--mint)')}
<div class="abs" style="left:64px;top:290px;width:620px">{rh}</div>
{quito('limpiando',640,760,430)}{foot()}''',FW,FH,f'{d}/Carrusel02_Slide06_Reglas.png')

def car3():
    d=R+'/Carrusel_03_La_misma_banca_distintas_historias'
    if os.path.exists(d): shutil.rmtree(d)
    render('c3_1',photo_piece('feed','historias25','La misma banca.<br><em>Distintas historias.</em>',hs=88,
        bub=bubble('historias25','feed','Mismo banco, cada uno en su historia.',w=320)),FW,FH,f'{d}/Carrusel03_Slide01_Portada.png')
    S_=[('primer53','El primer día.','Llegaste temprano, no encontrabas el aula y te sentaste acá a respirar.','¿Vos también sos nuevo?',300,'Primer_dia'),
        ('mesa16','La ronda<br><em>de mates.</em>',None,'¡El que ceba se queda!',300,'Mates'),
        ('siesta26','La siesta de<br><em>diez minutos.</em>',None,'Shhh… está repasando.',300,'Siesta'),
        ('almuerzo51','El almuerzo<br><em>de todos.</em>',None,'¡Yo junto, vos tirás!',290,'Almuerzo')]
    for i,(pl,h,led,b,bw,n) in enumerate(S_):
        render(f'c3_{i+2}',photo_piece('feed',pl,h,hs=110,lede=led,bub=bubble(pl,'feed',b,w=bw)),FW,FH,f'{d}/Carrusel03_Slide{i+2:02d}_{n}.png')
    render('c3_6',f'''{flat('var(--mint)','n',.09)}{H('¿Cuál es tu<br>historia en<br>un banco?',60,70,118)}
{T('Contala en la caja de preguntas de nuestras historias o escribila en el Muro de la Estación Bancala.<br><br>Las mejores vuelven en el próximo carrusel.',64,500,520,31,'var(--ink)',600)}
{quito('senalando_feliz',560,720,470,flip=True)}{foot('color')}''',FW,FH,f'{d}/Carrusel03_Slide06_Participa.png')

# ---------------- HISTORIAS ----------------
def card(inner,x,y,w,rot=0):
    return f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;background:#fff;border-radius:34px;box-shadow:0 14px 40px rgba(0,0,0,.28);transform:rotate({rot}deg);overflow:hidden">{inner}</div>'
def stories():
    d=R+'/Historias_Instagram'
    if os.path.exists(d): shutil.rmtree(d)
    render('s1',photo_piece('story','hola44','¡Buenas!<br><em>Soy Quito.</em>',
        bub=bubble('hola44','story','Vengo a pedirte una mano… bueno, una pata.',w=420),
        header_extra=f'<div style="display:inline-flex;margin-top:30px;background:#fff;border-radius:22px;padding:20px 28px;font:800 28px Brico;color:var(--blue);transform:rotate(-2deg);box-shadow:0 10px 30px rgba(0,0,0,.25)">🔗 CONOCÉ LA CAMPAÑA</div>'),SW,SH,f'{d}/Historia_01_Presentacion_Link.png')
    poll=f'''<div style="padding:34px 34px 30px"><div style="font:800 40px/1.1 Brico;color:var(--ink);text-align:center;margin-bottom:24px">¿Alguna vez rayaste un banco?</div>
<div style="display:flex;border:3px solid #e6e6e6;border-radius:22px;overflow:hidden">
<div style="flex:1;padding:26px 0;text-align:center;font:800 32px Brico;color:var(--blue);border-right:3px solid #e6e6e6">SÍ, CONFIESO</div>
<div style="flex:1;padding:26px 0;text-align:center;font:800 32px Brico;color:var(--green)">JAMÁS (MENTIRA)</div></div></div>'''
    render('s2',photo_piece('story','cuaderno41','Confesionario<br><em>de bancos.</em>',hs=116,extra=card(poll,90,600,900,-2)),SW,SH,f'{d}/Historia_02_Encuesta.png')
    opts=[('A','Un banco',''),('B','Un amigo',''),('C','Mucho más que un banco','✓')]
    oq=''.join(f'<div style="display:flex;align-items:center;gap:18px;border:3px solid {"var(--green)" if c else "#e6e6e6"};background:{"#eafbf1" if c else "#fff"};border-radius:20px;padding:18px 22px;margin-top:14px;font:700 32px Brico;color:var(--ink)"><span style="width:46px;height:46px;border-radius:50%;background:{"var(--green)" if c else "#eee"};color:{"#fff" if c else "var(--ink)"};display:flex;align-items:center;justify-content:center;font:800 24px Brico">{a}</span>{t}<span style="margin-left:auto;color:var(--green);font-size:38px">{c}</span></div>' for a,t,c in opts)
    quiz=f'<div style="background:var(--blue);padding:26px 30px;font:800 38px Brico;color:#fff;text-align:center">¿Qué es Quito?</div><div style="padding:10px 28px 30px">{oq}</div>'
    render('s3',photo_piece('story','quito52','Pregunta<br><em>de final.</em>',extra=card(quiz,110,580,860,2)),SW,SH,f'{d}/Historia_03_Quiz.png')
    slider=f'''<div style="padding:36px 40px 44px"><div style="font:800 40px/1.1 Brico;color:var(--ink);text-align:center">¿Cuánto bancás a tu banco favorito?</div>
<div style="position:relative;height:60px;margin-top:40px"><div style="position:absolute;left:0;right:0;top:24px;height:14px;border-radius:8px;background:linear-gradient(90deg,var(--mint),var(--blue))"></div>
<img src="{Q}q_sentado_feliz.png" style="position:absolute;left:62%;top:-38px;height:120px"></div></div>'''
    render('s4',photo_piece('story','charla23','¿Cuánto<br><em>lo bancás?</em>',extra=card(slider,110,580,860,-2)),SW,SH,f'{d}/Historia_04_Slider.png')
    qbox=f'''<div style="background:linear-gradient(135deg,var(--green),var(--navy));padding:30px 34px;text-align:center"><div style="font:800 38px/1.12 Brico;color:#fff">Contale a Quito tu mejor historia en un banco</div></div>
<div style="padding:30px;font:500 32px Brico;color:#9a9a9a;text-align:center">Escribí acá…</div>'''
    render('s5',photo_piece('story','primer53','Tu historia<br><em>acá.</em>',extra=card(qbox,110,580,860,1.5)),SW,SH,f'{d}/Historia_05_Caja_de_preguntas.png')
    music=f'''<div style="display:flex;gap:22px;align-items:center;padding:24px"><div style="width:130px;height:130px;border-radius:18px;background:var(--navy);display:flex;align-items:center;justify-content:center;overflow:hidden"><img src="{Q}q_saludo.png" style="height:118px"></div>
<div><div style="font:800 34px Brico;color:var(--ink)">Le Surfuku</div><div style="font:500 28px Brico;color:#777">Léo Lago · CC BY</div>
<div style="display:flex;gap:6px;margin-top:14px;align-items:flex-end;height:34px">{''.join(f'<span style="width:9px;height:{h}px;border-radius:4px;background:var(--blue)"></span>' for h in [12,26,18,32,22,14,28,20,30,16,24,12,26,18])}</div></div></div>'''
    render('s6',photo_piece('story','siesta26','Para escuchar<br><em>sentado.</em>',hs=118,lede='El tema de Quito. ¿Qué canción le pondrías a tu banco? Respondé y armamos juntos la playlist Bancala.',
        extra=card(music,110,640,860,-2)),SW,SH,f'{d}/Historia_06_Musica_Playlist.png')
    cd=f'''<div style="padding:32px 34px;text-align:center;background:linear-gradient(135deg,var(--blue),var(--navy))"><div style="font:800 26px Brico;letter-spacing:.08em;color:var(--mint)">CUENTA REGRESIVA</div>
<div style="font:800 46px Brico;color:#fff;margin-top:6px">Estación Bancala</div>
<div style="display:flex;justify-content:center;gap:14px;margin-top:20px">{''.join(f'<div style="background:rgba(255,255,255,.16);border-radius:14px;padding:12px 18px;color:#fff"><div style="font:800 52px Brico">{v}</div><div style="font:600 18px Brico;letter-spacing:.08em">{u}</div></div>' for v,u in [('02','DÍAS'),('14','HS'),('30','MIN')])}</div>
<div style="font:600 24px Brico;color:#fff;margin-top:18px;opacity:.9">🔔 Recordármelo</div></div>'''
    render('s7',f'''{flat('var(--navy)','b',.10)}
<div class="abs" style="left:64px;top:150px">{logos(28)}</div>
{H('Nos vemos<br><em>en el patio.</em>',60,250,124)}
<div class="abs" style="left:150px;top:560px;width:780px;height:1040px;border-radius:34px;overflow:hidden;border:6px solid var(--ink);box-shadow:10px 12px 0 var(--ink);transform:rotate(2deg)"><img src="../mock/standP_full.jpg" style="width:100%;height:100%;object-fit:cover"></div>
{card(cd,150,1420,780,-2)}''',SW,SH,f'{d}/Historia_07_Cuenta_regresiva_Stand.png')

if __name__=='__main__':
    for w in (sys.argv[1:] or ['afiches','posts','car1','car2','car3','stories']): globals()[w](); print('ok',w,flush=True)
