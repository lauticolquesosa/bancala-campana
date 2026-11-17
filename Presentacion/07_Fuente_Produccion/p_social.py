from lib import *
import sys
FW,FH=1080,1350; SW,SH=1080,1920
R=OUT+'/02_Piezas/01_Redes_Instagram'

def foot_small(color='#fff',v='blanco'):
    return f'<div class="abs" style="left:64px;bottom:52px">{logos(30,v)}</div>'
def pager(i,n,color='#fff'):
    dots=''.join(f'<span style="display:inline-block;width:{26 if k==i else 10}px;height:10px;border-radius:6px;margin-left:7px;background:{color};opacity:{1 if k==i else .45}"></span>' for k in range(1,n+1))
    return f'<div class="abs" style="right:64px;bottom:62px">{dots}</div>'
def swipe(color='#fff'):
    return f'<div class="abs swipe" style="right:64px;top:64px;font-size:26px;color:{color}">Deslizá →</div>'
def photo_slide(pl,kick,head,size=118,bub=None,body=None,top=64,headtop=112,extra='',scrim=620,fmt='feed',w=FW,h=FH):
    b=''
    if bub:
        t,bx,by,bw,tail=bub[:5]; fs=bub[5] if len(bub)>5 else 30
        b=f'<div class="bubble {tail}" style="left:{bx}px;top:{by}px;width:{bw}px;font-size:{fs}px">{t}</div>'
    bd=f'<div class="abs body" style="left:64px;top:{headtop+size*2.05}px;width:560px;font-size:30px;color:#fff;text-shadow:0 1px 12px rgba(0,0,0,.35)">{body}</div>' if body else ''
    return f'''<img class="fill" src="{P}{pl}_{fmt}_bg.jpg">
<div class="scrimT" style="height:{scrim}px"></div>
<div class="abs kick" style="left:64px;top:{top}px;font-size:24px;color:var(--mint)">{kick}</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:{headtop}px;font-size:{size}px;line-height:.98">{head}</div>
{bd}
<img class="fill" src="{P}{pl}_{fmt}_fg.png">{b}{extra}'''
def quito(pose,x,y,h,shadow=True,flip=False):
    sh=f'<div class="abs" style="left:{x-h*0.05}px;top:{y+h*0.93}px;width:{h*1.1}px;height:{h*0.12}px;border-radius:50%;background:radial-gradient(closest-side,rgba(42,40,41,.35),rgba(42,40,41,0))"></div>' if shadow else ''
    return f'{sh}<img class="abs" src="{Q}q_{pose}.png" style="left:{x}px;top:{y}px;height:{h}px;{"transform:scaleX(-1)" if flip else ""}">'
def flat(bg,trama='b',op=.13):
    t=f'<div class="abs trama-{trama}" style="inset:0;opacity:{op}"></div>' if trama else ''
    return f'<div class="abs" style="inset:0;background:{bg}"></div>{t}'

# ---------------- POSTS ----------------
def posts():
    d=R+'/Posteos'
    render('post1',photo_slide('hola44','Nuevo en la facu','Hola,<br>soy Quito.',size=130,
        bub=('¡Vengo a pedirte una mano… bueno, una pata!',470,760,400,'tr',30),
        body='El banquito de los patios de la facu. Te banca en el primer día, en los mates y en el final que aprobaste raspando.')
        +foot_small(),FW,FH,f'{d}/Post_01_Lanzamiento_Hola_soy_Quito.png')
    render('post2',photo_slide('mante53','Gracias, Mantenimiento','Los que nos<br>bancan a<br>nosotros.',size=104,scrim=760,
        bub=('¡Este equipo me deja como nuevo!',520,800,330,'tr',28),
        body=None,extra='''<div class="abs body" style="left:64px;top:470px;width:520px;font-size:27px;color:#fff;text-shadow:0 1px 12px rgba(0,0,0,.4)">
        Detrás de cada banco sano hay horas de trabajo: lijar, pintar, ajustar y reparar. Cuidar los bancos también es cuidar ese trabajo.</div>''')
        +foot_small(),FW,FH,f'{d}/Post_02_Homenaje_Mantenimiento.png')
    render('post3',stand_post(),FW,FH,f'{d}/Post_03_Anuncio_Estacion_Bancala.png')
    render('post4',stickers_post(),FW,FH,f'{d}/Post_04_Stickers_Pegalos_en_tu_compu.png')

def stand_post():
    tags=''.join(f'<span class="tag" style="font-size:22px;background:{c};color:{tc}">{t}</span>' for t,c,tc in [('Foto con Quito','var(--mint)','var(--ink)'),('Encuesta en vivo','var(--blue)','#fff'),('Muro de historias','var(--green)','#fff'),('Stickers gratis','var(--wood)','var(--ink)')])
    return f'''{flat('var(--paper)','n',.05)}
<div class="abs kick" style="left:64px;top:64px;font-size:24px;color:var(--green)">Martes y jueves · 10 a 14 h · Refugio rojo del patio</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:108px;font-size:92px;color:var(--blue)">Pasá por la<br>Estación Bancala.</div>
<div class="abs" style="left:64px;top:330px;width:560px;height:746px;border-radius:30px;overflow:hidden;border:6px solid var(--ink);box-shadow:10px 12px 0 var(--ink);transform:rotate(-2deg)"><img src="../mock/standP_full.jpg" style="width:100%;height:100%;object-fit:cover"></div>
<div class="abs body b7" style="left:672px;top:360px;width:350px;font-size:30px;color:var(--ink);line-height:1.2">Usamos el refugio rojo y los bancos que ya están en el patio: nada nuevo, todo bancado.</div>
<div class="abs" style="left:672px;top:560px;width:350px;display:flex;flex-direction:column;align-items:flex-start;gap:14px">{tags}</div>
<div class="abs" style="left:64px;bottom:52px">{logos(30,'color')}</div>'''

def stickers_post():
    poses=[('saludo',90,420,300,-6),('enojado',600,360,250,5),('sentado_feliz',380,640,280,-3),('tapandose',80,860,270,4),('llorando',700,700,280,-5)]
    st=''.join(f'<img class="abs" src="../stickers/st_{p}.png" style="left:{x}px;top:{y}px;height:{h}px;transform:rotate({r}deg);filter:drop-shadow(6px 10px 0 rgba(42,40,41,.18))">' for p,x,y,h,r in poses)
    return f'''{flat('var(--blue)','b',.12)}
<div class="abs kick" style="left:64px;top:64px;font-size:24px;color:var(--mint)">Gratis en la Estación Bancala</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:112px;font-size:84px">Pegalos en tu compu.<br><span style="color:var(--mint)">No en el banco.</span></div>
{st}{foot_small()}'''

# ---------------- CARRUSEL 01: CONOCE A QUITO ----------------
def car1():
    d=R+'/Carrusel_01_Conoce_a_Quito'; n=5
    render('c1_1',photo_slide('quito52','Ficha del banquito más bancador','Conocé<br>a Quito.',size=140,
        bub=('¡Hola! ¿Tenés un minuto? Bueno, sentate.',420,610,360,'tr',28))+swipe()+pager(1,n)+f'<div class="abs" style="left:64px;bottom:52px">{logos(30)}</div>',FW,FH,f'{d}/Carrusel01_Slide01_Portada.png')
    rows=[('Nombre','Quito, el banquito.'),('Vive en','Patios, pasillos y galerías de la facu.'),('Edad','Más que tu plan de estudios.'),
          ('Le gusta','Los mates, las charlas largas y que lo usen.'),('No se banca','Los fibrones, los chicles y que lo arrastren.'),('Superpoder','Bancarte en todas.')]
    rh=''.join(f'<div style="display:flex;border-top:3px solid var(--ink);padding:16px 0 14px"><div class="kick" style="width:210px;font-size:22px;color:var(--navy);padding-top:6px">{a}</div><div class="body b7" style="flex:1;font-size:31px;color:var(--ink);line-height:1.15">{b}</div></div>' for a,b in rows)
    render('c1_2',f'''{flat('var(--paper)','n',.06)}
<div class="abs kick" style="left:64px;top:64px;font-size:24px;color:var(--green)">Ficha técnica</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:108px;font-size:96px;color:var(--blue)">¿Quién es?</div>
<div class="abs" style="left:64px;top:280px;width:600px">{rh}<div style="border-top:3px solid var(--ink)"></div></div>
{quito('sentado_feliz',640,700,470)}{pager(2,n,'var(--ink)')}''',FW,FH,f'{d}/Carrusel01_Slide02_Ficha.png')
    words=['primeros días','finales aprobados','rondas de mates','chismes','amores','desamores','siestas de diez minutos','“después lo leo”']
    wl=' <span style="color:var(--mint)">·</span> '.join(words)
    render('c1_3',f'''{flat('var(--navy)','b',.10)}
<div class="abs kick" style="left:64px;top:64px;font-size:24px;color:var(--mint)">Testigo silencioso</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:108px;font-size:104px">Vio de todo.</div>
<div class="abs body b7" style="left:64px;top:270px;width:900px;font-size:46px;line-height:1.22;color:#fff">{wl}</div>
<div class="abs body" style="left:64px;top:760px;width:470px;font-size:28px;color:#fff;opacity:.9">En un mismo banco conviven la ansiedad del primer día, el orgullo de recibirse y la calma de una pausa.</div>
{quito('senalando_feliz',560,760,470)}{pager(3,n)}''',FW,FH,f'{d}/Carrusel01_Slide03_Testigo.png')
    tiles=[('sentado_feliz','Feliz','cuando lo usás para lo que es.','var(--mint)'),('enojado','Enojado','cuando lo rayás.','#ffd36b'),
           ('llorando','Triste','cuando lo dejás lleno de basura.','#9cc3f2'),('tapandose','Avergonzado','cuando lo usás de cama, reposera o peluquería.','#f7c3a0')]
    th=''.join(f'''<div style="position:relative;background:{c};border:4px solid var(--ink);border-radius:28px;box-shadow:7px 9px 0 var(--ink);height:440px;overflow:hidden">
      <img src="{Q}q_{p}.png" style="position:absolute;left:50%;top:22px;height:250px;transform:translateX(-50%)">
      <div style="position:absolute;left:24px;right:20px;top:290px"><div class="dsp thin" style="font-size:44px">{t}</div>
      <div class="body b7" style="font-size:25px;color:var(--ink);margin-top:10px;line-height:1.12">{x}</div></div></div>''' for p,t,x,c in tiles)
    render('c1_4',f'''{flat('var(--paper)','n',.05)}
<div class="abs kick" style="left:64px;top:64px;font-size:24px;color:var(--green)">Manual de emociones</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:108px;font-size:92px;color:var(--blue)">Su humor<br>depende de vos.</div>
<div class="abs" style="left:64px;right:64px;top:330px;display:grid;grid-template-columns:1fr 1fr;gap:26px 26px">{th}</div>{pager(4,n,'var(--ink)')}''',FW,FH+0,f'{d}/Carrusel01_Slide04_Emociones.png')
    render('c1_5',f'''{flat('var(--green)','n',.10)}
<div class="abs kick" style="left:64px;top:64px;font-size:24px;color:#fff">Ahora te toca a vos</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:110px;font-size:128px">Él te banca<br>en todas.</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:390px;font-size:128px;color:var(--mint)">¿Vos lo<br>bancás?</div>
<div class="abs body b7" style="left:64px;top:690px;width:440px;font-size:30px;color:#fff">Guardá este post y mandáselo a quien todavía usa los bancos de pizarrón.</div>
{quito('saludo',520,640,560)}
<div class="abs" style="left:64px;bottom:52px">{logos(34)}</div>{pager(5,n)}''',FW,FH,f'{d}/Carrusel01_Slide05_Cierre.png')

# ---------------- CARRUSEL 02: MENOS EN ESTAS ----------------
def car2():
    d=R+'/Carrusel_02_Te_banco_en_todas_menos_en_estas'; n=6
    render('c2_1',f'''{flat('var(--blue)','b',.14)}
<div class="abs kick" style="left:64px;top:64px;font-size:24px;color:#fff">Campaña Bancala · Serie 01</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:118px;font-size:150px">Te banco<br>en todas.</div>
<div class="abs dsp bounce" data-k=".9" style="left:60px;top:420px;font-size:150px;color:var(--mint)">Menos<br>en estas.</div>
{quito('tapandose',470,690,560)}{swipe()}{pager(1,n)}<div class="abs" style="left:64px;bottom:52px">{logos(30)}</div>''',FW,FH,f'{d}/Carrusel02_Slide01_Portada.png')
    S=[('playa29','Menos en esta · 01','No soy<br>reposera.',('¡Tapate un poco, che!',120,700,320,'tl')),
       ('pelu33','Menos en esta · 02','No soy<br>peluquería.',('¡Los pelos van al tacho, no a mí!',380,600,380,'tr')),
       ('cuaderno41','Menos en esta · 03','No soy<br>tu cuaderno.',('¡Eso no es un apunte!',140,740,320,'tl')),
       ('mudanza10','Menos en esta · 04','Si me movés,<br>devolveme.',('¿Me llevan… y me traen?',560,700,360,'tr'))]
    for i,(pl,k,h,b) in enumerate(S):
        render(f'c2_{i+2}',photo_slide(pl,k,h,size=124,bub=b)+pager(i+2,n)+f'<div class="abs" style="left:64px;bottom:52px"><img src="{B}bancala_blanco.svg" style="height:30px"></div>',
               FW,FH,f'{d}/Carrusel02_Slide{i+2:02d}_{["Reposera","Peluqueria","Cuaderno","Devolveme"][i]}.png')
    rules=[('Sentate, no te pares.','Las patas son para el piso, no para el asiento.'),('La basura, al tacho.','Siempre hay uno cerca. Quito lo sabe.'),
           ('Si lo movés, devolvelo.','Que ningún banco quede solo en medio de la nada.'),('¿Está roto? Avisá.','Escaneá el QR del banco o avisá a Mantenimiento.')]
    rh=''.join(f'<div style="display:flex;gap:22px;align-items:flex-start;margin-bottom:30px"><div class="dsp thin" style="font-size:58px;color:var(--mint);width:60px">{i+1}</div><div><div class="body" style="font-weight:800;font-size:38px;color:#fff;line-height:1.05">{a}</div><div class="body" style="font-size:26px;color:#fff;opacity:.85;margin-top:6px">{b}</div></div></div>' for i,(a,b) in enumerate(rules))
    render('c2_6',f'''{flat('var(--navy)','b',.10)}
<div class="abs kick" style="left:64px;top:64px;font-size:24px;color:var(--mint)">Cuatro reglas simples</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:110px;font-size:150px;color:var(--mint)">Bancala.</div>
<div class="abs" style="left:64px;top:330px;width:620px">{rh}</div>
{quito('limpiando',640,760,430)}{pager(6,n)}<div class="abs" style="left:64px;bottom:52px">{logos(30)}</div>''',FW,FH,f'{d}/Carrusel02_Slide06_Reglas.png')

# ---------------- CARRUSEL 03: DISTINTAS HISTORIAS ----------------
def car3():
    d=R+'/Carrusel_03_La_misma_banca_distintas_historias'; n=6
    render('c3_1',photo_slide('charla23','Mucho más que un banco','La misma banca.<br><span style="color:var(--mint)">Distintas historias.</span>',size=82,
        bub=('Acá se arreglan los grandes temas del mundo.',150,560,380,'tr',27))+swipe()+pager(1,n)+f'<div class="abs" style="left:64px;bottom:52px">{logos(30)}</div>',FW,FH,f'{d}/Carrusel03_Slide01_Portada.png')
    S=[('primer53','Historia 01','El primer día.','Llegaste temprano, no encontrabas el aula y te sentaste acá a respirar. Quito también estaba nervioso.',('¿Vos también sos nuevo?',560,690,300,'tr')),
       ('mesa16','Historia 02','La ronda<br>de mates.','Termo, bizcochitos y una charla que se estira hasta la próxima clase.',('¡El que ceba se queda!',130,480,300,'tl')),
       ('siesta26','Historia 03','La siesta de<br>diez minutos.','Entre parcial y parcial, cerrar los ojos también es estudiar. (Las zapatillas, fuera del banco.)',('Shhh… está repasando.',140,770,300,'tl')),
       ('almuerzo51','Historia 04','El almuerzo<br>de todos.','Se comparte la mesa, se comparte la sobremesa… y la basura se va al tacho.',('¡Yo junto, vos tirás!',560,700,300,'tr'))]
    for i,(pl,k,h,body,b) in enumerate(S):
        two='<br>' in h; sz=110
        render(f'c3_{i+2}',photo_slide(pl,k,h,size=sz,bub=b,scrim=700,extra=f'<div class="abs body" style="left:64px;top:{112+sz*(2.1 if two else 1.1)}px;width:600px;font-size:29px;color:#fff;text-shadow:0 1px 14px rgba(0,0,0,.45)">{body}</div>')
               +pager(i+2,n)+f'<div class="abs" style="left:64px;bottom:52px"><img src="{B}bancala_blanco.svg" style="height:30px"></div>',
               FW,FH,f'{d}/Carrusel03_Slide{i+2:02d}_{["Primer_dia","Mates","Siesta","Almuerzo"][i]}.png')
    render('c3_6',f'''{flat('var(--mint)','n',.10)}
<div class="abs kick" style="left:64px;top:64px;font-size:24px;color:var(--ink)">Te toca contar</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:110px;font-size:118px">¿Cuál es tu<br>historia en<br>un banco?</div>
<div class="abs body b7" style="left:64px;top:560px;width:520px;font-size:31px;color:var(--ink)">Contala en la caja de preguntas de nuestras historias o escribila en el Muro de la Estación Bancala.<br><br>Las mejores vuelven en el próximo carrusel.</div>
{quito('senalando_feliz',560,700,470,flip=True)}{pager(6,n,'var(--ink)')}<div class="abs" style="left:64px;bottom:52px">{logos(30,'color')}</div>''',FW,FH,f'{d}/Carrusel03_Slide06_Participa.png')

# ---------------- HISTORIAS ----------------
def st_base(pl,kick,head,size=120,headtop=270,extra='',scrim=900):
    return f'''<img class="fill" src="{P}{pl}_story_bg.jpg"><div class="scrimT" style="height:{scrim}px"></div>
<div class="abs" style="left:64px;top:150px">{logos(28)}</div>
<div class="abs kick" style="left:64px;top:228px;font-size:26px;color:var(--mint)">{kick}</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:{headtop}px;font-size:{size}px;line-height:.98">{head}</div>
<img class="fill" src="{P}{pl}_story_fg.png">{extra}'''
def card(inner,x,y,w,rot=0):
    return f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;background:#fff;border-radius:34px;box-shadow:0 14px 40px rgba(0,0,0,.28);transform:rotate({rot}deg);overflow:hidden">{inner}</div>'
def stories():
    d=R+'/Historias_Instagram'
    render('s1',st_base('hola44','Nuevo en la facu','¡Buenas!<br>Soy Quito.',size=140,extra=f'''
<div class="bubble tr" style="left:300px;top:1040px;width:470px;font-size:36px">Vengo a pedirte una mano… bueno, una pata.</div>
{card('<div style="padding:22px 30px;font:800 30px Brico;color:var(--blue);display:flex;gap:14px;align-items:center">🔗 <span>CONOCÉ LA CAMPAÑA</span></div>',64,640,480,-3)}'''),SW,SH,f'{d}/Historia_01_Presentacion_Link.png')
    poll=f'''<div style="padding:34px 34px 30px"><div style="font:800 40px/1.1 Brico;color:var(--ink);text-align:center;margin-bottom:24px">¿Alguna vez rayaste un banco?</div>
<div style="display:flex;border:3px solid #e6e6e6;border-radius:22px;overflow:hidden">
<div style="flex:1;padding:26px 0;text-align:center;font:800 34px Brico;color:var(--blue);border-right:3px solid #e6e6e6">SÍ, CONFIESO</div>
<div style="flex:1;padding:26px 0;text-align:center;font:800 34px Brico;color:var(--green)">JAMÁS (MENTIRA)</div></div></div>'''
    render('s2',st_base('cuaderno41','Encuesta · Sé honesto','Confesionario<br>de bancos.',size=118,extra=card(poll,90,660,900,-2)),SW,SH,f'{d}/Historia_02_Encuesta.png')
    opts=[('A','Un banco',''),('B','Un amigo',''),('C','Mucho más que un banco','✓')]
    oq=''.join(f'<div style="display:flex;align-items:center;gap:18px;border:3px solid {"var(--green)" if c else "#e6e6e6"};background:{"#eafbf1" if c else "#fff"};border-radius:20px;padding:18px 22px;margin-top:14px;font:700 32px Brico;color:var(--ink)"><span style="width:46px;height:46px;border-radius:50%;background:{"var(--green)" if c else "#eee"};color:{"#fff" if c else "var(--ink)"};display:flex;align-items:center;justify-content:center;font:800 24px Brico">{a}</span>{t}<span style="margin-left:auto;color:var(--green);font-size:38px">{c}</span></div>' for a,t,c in opts)
    quiz=f'<div style="background:var(--blue);padding:26px 30px;font:800 38px Brico;color:#fff;text-align:center">¿Qué es Quito?</div><div style="padding:10px 28px 30px">{oq}</div>'
    render('s3',st_base('quito52','Quiz · Tocá la correcta','Pregunta<br>de final.',size=130,extra=card(quiz,110,640,860,2)),SW,SH,f'{d}/Historia_03_Quiz.png')
    slider=f'''<div style="padding:36px 40px 44px"><div style="font:800 40px/1.1 Brico;color:var(--ink);text-align:center">¿Cuánto bancás a tu banco favorito?</div>
<div style="position:relative;height:60px;margin-top:40px"><div style="position:absolute;left:0;right:0;top:24px;height:14px;border-radius:8px;background:linear-gradient(90deg,var(--mint),var(--blue))"></div>
<img src="{Q}q_sentado_feliz.png" style="position:absolute;left:62%;top:-38px;height:120px"></div></div>'''
    render('s4',st_base('charla23','Deslizá a Quito','¿Cuánto<br>lo bancás?',size=130,extra=card(slider,110,650,860,-2)),SW,SH,f'{d}/Historia_04_Slider.png')
    qbox=f'''<div style="background:linear-gradient(135deg,var(--green),var(--navy));padding:30px 34px;text-align:center"><div style="font:800 38px/1.12 Brico;color:#fff">Contale a Quito tu mejor historia en un banco</div></div>
<div style="padding:30px;font:500 32px Brico;color:#9a9a9a;text-align:center">Escribí acá…</div>'''
    render('s5',st_base('primer53','Caja de preguntas','Tu historia<br>acá.',size=140,extra=card(qbox,110,660,860,1.5)),SW,SH,f'{d}/Historia_05_Caja_de_preguntas.png')
    music=f'''<div style="display:flex;gap:22px;align-items:center;padding:24px"><div style="width:130px;height:130px;border-radius:18px;background:var(--navy);display:flex;align-items:center;justify-content:center;overflow:hidden"><img src="{Q}q_saludo.png" style="height:118px"></div>
<div><div style="font:800 34px Brico;color:var(--ink)">Le Surfuku</div><div style="font:500 28px Brico;color:#777">Léo Lago · CC BY</div>
<div style="display:flex;gap:6px;margin-top:14px;align-items:flex-end;height:34px">{''.join(f'<span style="width:9px;height:{h}px;border-radius:4px;background:var(--blue)"></span>' for h in [12,26,18,32,22,14,28,20,30,16,24,12,26,18])}</div></div></div>'''
    render('s6',st_base('siesta26','Banda sonora oficial','Para escuchar<br>sentado.',size=118,extra=card(music,110,680,860,-2)+
        '<div class="abs body b7" style="left:64px;top:900px;width:760px;font-size:32px;color:#fff;text-shadow:0 2px 14px rgba(0,0,0,.5)">La playlist “Bancala” ya está en Spotify: temas para el mate, la siesta y la previa del parcial.</div>'),SW,SH,f'{d}/Historia_06_Musica_Playlist.png')
    cd=f'''<div style="padding:32px 34px;text-align:center;background:linear-gradient(135deg,var(--blue),var(--navy))"><div style="font:800 26px Brico;letter-spacing:.08em;color:var(--mint)">CUENTA REGRESIVA</div>
<div style="font:800 46px Brico;color:#fff;margin-top:6px">Estación Bancala</div>
<div style="display:flex;justify-content:center;gap:14px;margin-top:20px">{''.join(f'<div style="background:rgba(255,255,255,.16);border-radius:14px;padding:12px 18px;color:#fff"><div style="font:800 52px Brico">{v}</div><div style="font:600 18px Brico;letter-spacing:.08em">{u}</div></div>' for v,u in [('02','DÍAS'),('14','HS'),('30','MIN')])}</div>
<div style="font:600 24px Brico;color:#fff;margin-top:18px;opacity:.9">🔔 Recordármelo</div></div>'''
    render('s7',f'''{flat('var(--navy)','b',.12)}
<div class="abs" style="left:64px;top:150px">{logos(28)}</div>
<div class="abs kick" style="left:64px;top:228px;font-size:26px;color:var(--mint)">Martes · Refugio rojo del patio</div>
<div class="abs dsp bounce" data-k=".6" style="left:60px;top:270px;font-size:124px">Nos vemos<br>en el patio.</div>
<div class="abs" style="left:150px;top:560px;width:780px;height:1040px;border-radius:34px;overflow:hidden;border:6px solid var(--ink);box-shadow:10px 12px 0 var(--ink);transform:rotate(2deg)"><img src="../mock/standP_full.jpg" style="width:100%;height:100%;object-fit:cover"></div>
{card(cd,150,1380,780,-2)}''',SW,SH,f'{d}/Historia_07_Cuenta_regresiva_Stand.png')

def highlights():
    d=R+'/Portadas_Destacadas'
    H=[('Quito','saludo','var(--navy)'),('Encuestas','enojado','var(--blue)'),('Historias','sentado_feliz','var(--green)'),('Estacion','senalando_feliz','var(--mint)'),('Playlist','paraguas','var(--navy)'),('Reglas','limpiando','var(--blue)')]
    for i,(t,p,c) in enumerate(H):
        render(f'h{i}',f'''{flat(c,'b',.12)}<div class="abs" style="left:140px;top:140px;width:800px;height:800px;border-radius:50%;background:#fff;border:10px solid var(--ink)"></div>
<img class="abs" src="{Q}q_{p}.png" style="left:50%;top:220px;height:560px;transform:translateX(-50%)">
<div class="abs dsp" style="left:0;right:0;top:860px;text-align:center;font-size:96px">{t.replace("Estacion","Estación")}</div>''',1080,1080,f'{d}/Destacada_{i+1:02d}_{t}.png')

if __name__=='__main__':
    which=sys.argv[1:] or ['posts','car1','car2','car3','stories','highlights']
    for w in which: globals()[w](); print('ok',w,flush=True)
