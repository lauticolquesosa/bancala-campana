from lib import *
from PIL import Image
import hashlib
PX=SITE+'/px'; os.makedirs(PX,exist_ok=True)
PZ=OUT+'/02_Piezas'
def im(path,mx=1500,q=86):
    """cached compressed jpg for PDF; path relative to scratch S or absolute"""
    p=path if os.path.isabs(path) else S+'/'+path
    h=hashlib.md5((p+str(mx)).encode()).hexdigest()[:10]; o=f'{PX}/{h}.jpg'
    if not os.path.exists(o):
        x=Image.open(p)
        if x.mode in ('RGBA','LA','P'):
            x=x.convert('RGBA'); bg=Image.new('RGBA',x.size,(245,241,232,255)); bg.alpha_composite(x); x=bg
        x=x.convert('RGB'); x.thumbnail((mx,mx),Image.LANCZOS); x.save(o,quality=q)
    return 'px/'+os.path.basename(o)
def png(path,mx=1200):
    p=path if os.path.isabs(path) else S+'/'+path
    h=hashlib.md5((p+str(mx)).encode()).hexdigest()[:10]; o=f'{PX}/{h}.png'
    if not os.path.exists(o):
        x=Image.open(p).convert('RGBA'); x.thumbnail((mx,mx),Image.LANCZOS); x.save(o,optimize=True)
    return 'px/'+os.path.basename(o)
def pz(rel,mx=1500): return im(PZ+'/'+rel,mx)

W,H=1920,1080
pages=[]; secs=[]
def page(body,sec='',num=True,strip=True,bg='#fff',dark=False):
    n=len(pages)+1
    st=f'<div class="abs trama-n" style="left:0;top:0;bottom:0;width:58px;background-color:var(--green);background-size:420px auto"></div>' if strip else ''
    fc='#fff' if dark else 'var(--ink)'
    ft=f'<div class="abs kick" style="left:110px;bottom:38px;font-size:15px;color:{fc};opacity:.55">Bancala · Mucho más que un banco</div><div class="abs kick" style="right:70px;bottom:38px;font-size:15px;color:{fc};opacity:.55">{sec}&nbsp;&nbsp;{n:02d}</div>' if num else ''
    pages.append(f'<section class="pg" style="background:{bg}">{st}{body}{ft}</section>')
def label(t,x=110,y=70,c='var(--char)'):
    return f'<div class="abs tag" style="left:{x}px;top:{y}px;font-size:24px;background:{c};padding:.35em .65em .3em;border-radius:6px">{t}</div>'
def h1(t,x=110,y=130,s=92,c='var(--blue)',w=None):
    return f'<div class="abs dsp" style="left:{x}px;top:{y}px;font-size:{s}px;color:{c};{"width:%dpx;"%w if w else ""}line-height:.95">{t}</div>'
def p(t,x,y,w,s=24,c='var(--char)',wt=450,extra=''):
    return f'<div class="abs body" style="left:{x}px;top:{y}px;width:{w}px;font-size:{s}px;color:{c};font-weight:{wt};line-height:1.38;{extra}">{t}</div>'
def why(items,x,y,w,title='Por qué así'):
    li=''.join(f'<div style="display:flex;gap:12px;margin-top:12px"><span style="flex:none;width:10px;height:10px;border-radius:50%;background:var(--green);margin-top:9px"></span><span>{t}</span></div>' for t in items)
    return f'<div class="abs body" style="left:{x}px;top:{y}px;width:{w}px;font-size:20px;line-height:1.36;color:var(--char)"><div class="kick" style="font-size:17px;color:var(--green)">{title}</div>{li}</div>'
def img(src,x,y,w,h,r=14,fit='cover',sh=True,extra=''):
    return f'<img class="abs" src="{src}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:{fit};border-radius:{r}px;{"box-shadow:0 10px 30px rgba(42,40,41,.18);" if sh else ""}{extra}">'
def cap(t,x,y,w,c='var(--char)'):
    return f'<div class="abs kick" style="left:{x}px;top:{y}px;width:{w}px;font-size:14px;color:{c};opacity:.7">{t}</div>'

def build():
    # 01 PORTADA
    page(f'''<div class="abs" style="inset:0;background:var(--navy)"></div><div class="abs trama-b" style="inset:0;opacity:.10;background-size:900px auto"></div>
<img class="abs" src="{im('plates2/quito52_story_full.jpg',1400)}" style="right:0;top:0;width:760px;height:1080px;object-fit:cover">
<div class="abs" style="right:0;top:0;width:760px;height:1080px;background:linear-gradient(90deg,var(--navy),rgba(27,77,139,0) 30%)"></div>
<div class="abs" style="left:120px;top:110px">{logos(46)}</div>
<div class="abs kick" style="left:122px;top:300px;font-size:26px;color:var(--mint)">Campaña de concientización · Presentación de proyecto</div>
<div class="abs dsp bounce" data-k=".5" style="left:116px;top:350px;font-size:178px;line-height:.92">Mucho más<br>que un banco.</div>
<div class="abs body" style="left:122px;top:740px;width:840px;font-size:30px;color:#fff;line-height:1.35">Cuidado de los bancos de los espacios comunes de la Facultad —patios, pasillos y galerías— con Quito, el banquito, como protagonista.</div>
<div class="abs kick" style="left:122px;top:950px;font-size:18px;color:#fff;opacity:.7">Tecnología del Diseño · UCASAL · 2026</div>''',num=False,strip=False)
    # 02 INDICE
    idx=[('01','Diagnóstico','Problema, público e insight'),('02','Estrategia','Concepto, mensaje, tono y referentes'),('03','Personaje','Quito y su integración en la escena'),
         ('04','Sistema visual','Marcas, tipografía, color, tramas y look'),('05','Piezas','Infografía, afiches, redes y stickers'),('06','Arquigrafía','Estación Bancala con mobiliario existente'),('07','Implementación','Articulación, cronograma y medición')]
    ih=''.join(f'<div style="display:flex;gap:28px;align-items:baseline;border-top:3px solid var(--ink);padding:18px 0"><div class="dsp thin" style="font-size:54px;color:var(--mint);width:96px">{a}</div><div style="flex:1"><div class="body" style="font-size:36px;font-weight:800;color:var(--ink)">{b}</div><div class="body" style="font-size:21px;color:var(--char);opacity:.7">{c}</div></div></div>' for a,b,c in idx)
    page(f'''{label('Índice')}{h1('De qué va<br>esta campaña.',y=140,s=96)}
<div class="abs" style="left:900px;top:90px;width:900px">{ih}</div>
<img class="abs" src="{png('quito/q_senalando_feliz.png',700)}" style="left:150px;top:520px;height:440px">''',sec='Índice')
    # 03 PROBLEMA
    page(f'''{label('01 · Diagnóstico')}{h1('Lo que es de todos<br>parece de nadie.',s=84)}
{p('Los bancos de los <b>espacios comunes</b> de la Facultad —patios, pasillos, galerías y sectores de circulación— son el principal punto de encuentro del campus. No hablamos del mobiliario de las aulas: hablamos de los bancos donde se espera, se estudia, se toma mate y se charla.',110,370,760,25)}
{p('Hoy sufren rayones, chicles, basura, usos para los que no fueron pensados (acostarse con zapatillas, pararse encima) y traslados que los dejan lejos de su lugar. Cada daño se traduce en horas de trabajo del equipo de Mantenimiento.',110,560,760,25)}
<div class="abs" style="left:110px;top:760px;width:760px;border-left:8px solid var(--mint);padding-left:26px"><div class="kick" style="font-size:17px;color:var(--green)">Insight</div><div class="body" style="font-size:31px;font-weight:700;color:var(--ink);line-height:1.25;margin-top:6px">“No lo cuido porque no es mío.” Si el banco deja de ser un objeto y pasa a ser <i>alguien</i>, cuidarlo se vuelve natural.</div></div>
{img(im('ph/f41.jpg',900),960,90,400,520)}{img(im('ph/f29.jpg',900),1390,90,400,520)}
{img(im('ph/f10.jpg',900),960,640,400,330)}{img(im('ph/f33.jpg',900),1390,640,400,330)}
{cap('Registro fotográfico del equipo en el campus: escenas reales de uso indebido.',960,985,830)}''',sec='Diagnóstico')
    # 04 PUBLICO Y OBJETIVOS
    cards=[('Público principal','Estudiantes de grado de 18 a 25 años que usan los patios y pasillos todos los días. Nativos de Instagram, responden al humor, a lo cercano y a lo que pueden compartir.'),
           ('Público secundario','Docentes, personal no docente y el equipo de Mantenimiento, que pasa de ser invisible a ser reconocido.'),
           ('Objetivo comunicacional','Que el estudiante reconozca el banco como algo que lo “banca” todos los días y adopte tres conductas: usarlo bien, no dañarlo y avisar cuando está roto.'),
           ('Cómo lo medimos','Votos en encuestas, respuestas en la caja de preguntas, historias del Muro, reportes por QR y relevamiento fotográfico de daños antes y después.')]
    ch=''.join(f'<div style="background:{c};border:4px solid var(--ink);border-radius:22px;padding:28px 30px;box-shadow:7px 9px 0 var(--ink)"><div class="kick" style="font-size:18px;color:var(--ink)">{a}</div><div class="body" style="font-size:23px;line-height:1.35;color:var(--ink);margin-top:10px">{b}</div></div>' for (a,b),c in zip(cards,['var(--mint)','#fff','#fff','var(--mint)']))
    page(f'''{label('01 · Diagnóstico')}{h1('A quién le hablamos<br>y para qué.',s=84)}
<div class="abs" style="left:110px;top:360px;width:1240px;display:grid;grid-template-columns:1fr 1fr;gap:30px">{ch}</div>
<img class="abs" src="{png('quito/q_sentado_feliz.png',700)}" style="left:1420px;top:380px;height:470px">''',sec='Diagnóstico')
    # 05 CONCEPTO / ARQUITECTURA DE MENSAJES
    steps=[('Vínculo','Te banco en todas.','Quito acompaña los momentos reales de la facu: el primer día, los mates, el final aprobado.','var(--mint)','sentado_feliz'),
           ('Límite','Menos en esta.','El humor marca lo que no se hace sin retar: “No soy reposera”, “No soy tu cuaderno”.','#ffd36b','tapandose'),
           ('Acción','Bancala.','El nombre de la campaña es el llamado: bancar al banco que te banca. Reglas simples y un QR para avisar.','#9cc3f2','saludo')]
    sh=''.join(f'''<div style="position:relative;background:{c};border:4px solid var(--ink);border-radius:26px;box-shadow:8px 10px 0 var(--ink);padding:30px;height:520px">
<div class="kick" style="font-size:18px;color:var(--ink)">{i+1:02d} · {a}</div><div class="dsp thin" style="font-size:62px;margin-top:10px;color:#fff">{b}</div>
<div class="body" style="font-size:22px;line-height:1.35;color:var(--ink);margin-top:16px;width:330px">{d}</div>
<img src="{png(f'quito/q_{q}.png',500)}" style="position:absolute;right:18px;bottom:18px;height:220px"></div>''' for i,(a,b,d,c,q) in enumerate(steps))
    page(f'''{label('02 · Estrategia')}{h1('Mucho más que un banco.',s=86)}
{p('<b>Concepto.</b> El banco es mucho más que un mueble: es testigo y sostén de la vida universitaria. Lo personificamos en Quito para que deje de ser “cosa de la facu” y pase a ser un amigo. El juego de palabras <i>banco / bancar</i> ordena todo el sistema de mensajes en tres pasos.',110,250,1100,24)}
<div class="abs" style="left:110px;top:400px;width:1700px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:34px">{sh}</div>''',sec='Estrategia')
    # 06 TONO + REFERENTES
    refs=[('Dumb Ways to Die','McCann Melbourne · Metro Trains, 2012','Un mensaje de seguridad contado con personajes tiernos y humor negro. No sermonea: entretiene, y por eso se comparte. Redujo un 21 % los accidentes.','Tomamos: personaje simpático + humor que evita el reto.'),
          ('Don\'t Mess with Texas','GSD&M · TxDOT, 1986','Campaña contra la basura que habla en el idioma y el orgullo de su público (hombres jóvenes), no en el de la institución. Bajó la basura en rutas un 72 % en tres años.','Tomamos: hablar como habla el público y apelar a la pertenencia.'),
          ('Smokey Bear','Ad Council · USDA, desde 1944','Una mascota con voz propia sostiene un mensaje de cuidado durante décadas, adaptándose a cada medio sin perder identidad.','Tomamos: personaje como vocero estable de todas las piezas.')]
    rh=''.join(f'<div style="border-top:4px solid var(--ink);padding-top:18px"><div class="body" style="font-size:30px;font-weight:800;color:var(--blue)">{a}</div><div class="kick" style="font-size:15px;color:var(--char);opacity:.6;margin-top:4px">{b}</div><div class="body" style="font-size:20px;line-height:1.38;margin-top:12px">{c}</div><div class="body" style="font-size:20px;font-weight:700;color:var(--green);margin-top:12px">{d}</div></div>' for a,b,c,d in refs)
    tono=[('Cercano','Voseo, lenguaje de pasillo, frases cortas.'),('Humorístico','El chiste señala la conducta sin humillar a nadie.'),('Positivo','Siempre se cierra con una acción posible.'),('Claro','Un mensaje por pieza, legible en dos segundos.')]
    th=''.join(f'<div style="background:var(--paper);border-radius:16px;padding:18px 20px"><div class="body" style="font-size:24px;font-weight:800;color:var(--ink)">{a}</div><div class="body" style="font-size:18px;margin-top:4px">{b}</div></div>' for a,b in tono)
    page(f'''{label('02 · Estrategia')}{h1('Tono: el amigo que te<br>la dice con humor.',s=78)}
<div class="abs" style="left:110px;top:330px;width:560px;display:grid;grid-template-columns:1fr 1fr;gap:16px">{th}</div>
{p('Investigamos cómo trabajan las campañas sociales más efectivas: las que mejor funcionan no retan, construyen un vínculo y dan una acción concreta. Estos tres casos guiaron nuestras decisiones.',110,640,560,21)}
<div class="abs kick" style="left:760px;top:330px;font-size:17px;color:var(--green)">Referentes estudiados</div>
<div class="abs" style="left:760px;top:370px;width:1050px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:34px">{rh}</div>''',sec='Estrategia')
    # 07 MANIFIESTO
    page(f'''<div class="abs" style="inset:0;background:var(--navy)"></div><div class="abs trama-b" style="inset:0;opacity:.09"></div>
{label('02 · Manifiesto',c='var(--mint);color:var(--ink)')}
<div class="abs body" style="left:110px;top:170px;width:1100px;font-size:40px;line-height:1.3;color:#fff;font-weight:600">Los bancos de la facu son testigos silenciosos de la vida universitaria. En el mismo banco conviven los nervios del primer día, las risas entre mates, la siesta entre parciales y el orgullo de recibirse.<br><br>Detrás de cada uno hay materiales y horas de trabajo del equipo de Mantenimiento. Cuidar los bancos es cuidar los encuentros que pasan sobre ellos.</div>
<div class="abs dsp bounce" data-k=".5" style="left:106px;top:800px;font-size:110px;color:var(--mint)">Te bancan. Bancalos.</div>
<img class="abs" src="{png('quito/q_saludo.png',800)}" style="left:1300px;top:300px;height:560px">''',sec='Manifiesto',dark=True)
    # 08 PERSONAJE
    poses=['saludo','sentado_feliz','senalando_feliz','limpiando','juntando_basura','policia','paraguas','tapandose','enojado','preocupado_sentado','triste_sentado','llorando']
    ph=''.join(f'<div style="background:var(--paper);border-radius:18px;height:200px;display:flex;align-items:center;justify-content:center"><img src="{png(f"quito/q_{q}.png",400)}" style="max-height:175px;max-width:90%"></div>' for q in poses)
    page(f'''{label('03 · Personaje')}{h1('Quito,<br>el banquito.',s=72)}
{p('<b>Quién es.</b> Un banco de plaza de madera con estética cartoon de los años 30: brazos de manguera, guantes, zapatillas y un morral con el símbolo de reciclaje. Habla como un estudiante más.',110,320,640,22)}
{p('<b>Personalidad.</b> Leal, bonachón y un poco dramático: aguanta todo, pero cuando lo maltratan lo dice con humor. Es testigo, no policía.',110,470,640,22)}
{why(['Usamos el personaje <b>tal cual</b> fue creado: recortamos cada pose original y la reconstruimos con un escalador por IA entrenado en ilustración (Real-ESRGAN) para ganar resolución sin redibujarlo.','Cada emoción tiene una función: feliz para el vínculo, avergonzado o enojado para el límite, limpiando para la acción.','Una sola voz para todas las piezas, como Smokey Bear: el público reconoce la campaña antes de leerla.'],110,590,640)}
<div class="abs" style="left:820px;top:110px;width:990px;display:grid;grid-template-columns:repeat(4,1fr);gap:16px">{ph}</div>
{cap('12 poses y emociones disponibles, recortadas sin alterar el dibujo original.',820,980,990)}''',sec='Personaje')
    # 09 INTEGRACION
    st=[('1','Recorte pegado','Así estaba antes: el personaje flota sobre la foto.'),('2','Sombras','Sombra de contacto y sombra proyectada según el sol de cada foto.'),('3','Luz y color','Lado en sombra, luz de borde, color ambiente y rebote del piso.'),('4','Look común','El mismo grade y el mismo grano para foto y personaje.')]
    sh=''.join(f'<div><img src="{im(f"proc/step{i+1}.jpg",700)}" style="width:100%;height:420px;object-fit:cover;border-radius:14px"><div style="display:flex;gap:12px;margin-top:14px"><div class="dsp thin" style="font-size:44px;color:var(--mint)">{a}</div><div><div class="body" style="font-size:22px;font-weight:800">{b}</div><div class="body" style="font-size:18px;line-height:1.3">{c}</div></div></div></div>' for i,(a,b,c) in enumerate(st))
    page(f'''{label('03 · Corrección: integración del personaje')}{h1('Que Quito esté en la foto,<br>no encima de la foto.',s=72)}
<div class="abs" style="left:110px;top:310px;width:1700px;display:grid;grid-template-columns:repeat(4,1fr);gap:28px">{sh}</div>
{p('Analizamos dirección y dureza de la luz de cada fotografía (sol directo u overcast) y construimos al personaje en capas: así los titulares pueden ir <b>entre</b> la foto y Quito, y el texto deja de ser un elemento aparte.',110,880,1500,22)}''',sec='Personaje')
    # 10 ANTES / DESPUES escena
    page(f'''{label('03 · Antes y después')}{h1('Mismo personaje,<br>otra credibilidad.',s=80)}
{img(im('proc/naive_playa.jpg',900),110,330,480,640)}{img(pz('01_Redes_Instagram/Carrusel_02_Te_banco_en_todas_menos_en_estas/Carrusel02_Slide02_Reposera.png',1000),640,330,512,640)}
{cap('Antes: recorte sin luz ni sombra',110,985,480)}{cap('Después: pieza final de la campaña',640,985,512)}
{why(['La sombra de contacto “apoya” a Quito en el piso; sin ella, cualquier personaje flota.','La escala respeta la perspectiva: Quito mide lo que mide un banco real en ese punto de la imagen.','El pasto tapa apenas la suela y el personaje toma el color del ambiente: el ojo lo lee como parte del lugar.','El globo se ubica siempre sobre la cabeza de Quito, con la cola apuntándolo: se lee quién habla sin buscarlo.'],1240,330,560)}''',sec='Personaje')
    # 11 MARCAS
    page(f'''{label('04 · Corrección: marcas')}{h1('Tres marcas,<br>una firma.',s=86)}
<div class="abs" style="left:110px;top:360px;width:820px;height:250px;background:#fff;border:3px solid #e6e2d8;border-radius:22px;display:flex;align-items:center;justify-content:center">{logos(54,'color')}</div>
<div class="abs" style="left:110px;top:640px;width:820px;height:250px;background:var(--navy);border-radius:22px;display:flex;align-items:center;justify-content:center">{logos(54)}</div>
{why(['<b>Eliminamos el isotipo</b> (el banco abstracto de dos “A”): competía con Quito como símbolo y duplicaba la idea. Ahora el personaje es el ícono.','<b>Bancala</b> va primero: es la campaña y el llamado a la acción. <b>UCASAL Sustentable</b> y <b>UCASAL</b> la avalan, a menor peso, separados por filetes.','Vectorizamos el logotipo Bancala desde el manual y tomamos los logos institucionales de fuentes oficiales (sitio web y calendario de UCASAL Sustentable) para que se vean nítidos en impresión.','Dos versiones: color sobre fondos claros y blanca sobre fotos o fondos de la paleta. La firma siempre va en el mismo lugar de cada formato.'],1010,360,800)}''',sec='Sistema visual')
    # 12 TIPOGRAFIA
    page(f'''{label('04 · Corrección: tipografía')}{h1('Una letra con la<br>personalidad de Quito.',s=62)}
<div class="abs" style="left:110px;top:330px;width:900px;background:var(--paper);border-radius:24px;padding:36px 40px">
<div class="kick" style="font-size:16px;color:var(--green)">Display expresiva · Titan One + tratamiento propio</div>
<div class="dsp bounce" data-k=".6" style="font-size:118px;color:var(--mint);margin-top:14px">Te banco<br>en todas.</div>
<div class="body" style="font-size:19px;margin-top:20px;line-height:1.35">Contorno del mismo color y grosor relativo que el trazo de Quito, sombra desplazada tipo sticker y un leve “rebote” por letra que imita la animación de manguera de los dibujos de los años 30.</div></div>
<div class="abs" style="left:110px;top:800px;width:900px;background:var(--paper);border-radius:24px;padding:28px 40px">
<div class="kick" style="font-size:16px;color:var(--green)">Palo seco de texto · Bricolage Grotesque</div>
<div class="body" style="font-size:40px;font-weight:800;margin-top:6px">Aa Bb Cc 0123 — ¿Me bancás?</div>
<div class="body" style="font-size:19px;margin-top:6px">Reemplaza a Rock Salt en todos los textos: legible en párrafos y en pantalla, con trampas de tinta que le dan calidez.</div></div>
<img class="abs" src="{im(r"C:/Users/Lauti/Documents/Tecnologia del Diseño - Campaña Bancala/05_Material_Original/Referencias_tipograficas/Referencia_tipografica_05.jpeg",900)}" style="left:1090px;top:110px;width:330px;height:520px;object-fit:cover;object-position:50% 20%;border-radius:14px">
{cap('Referencia evaluada (carpeta de referencias)',1090,640,330)}
{why(['La referencia “Nostalgia Sound” funciona: combina personajes de manguera con letras gruesas, redondeadas y contorneadas. Es el mismo lenguaje de Quito.','No la copiamos: elegimos una tipografía libre (Titan One, licencia OFL) y le sumamos el tratamiento propio para que sea de la campaña.','Rock Salt era ilegible en párrafos y competía con las tramas; queda fuera del sistema.','Jerarquía fija: kicker en mayúsculas, titular display, cuerpo palo seco.'],1450,110,370)}''',sec='Sistema visual')
    # 13 COLOR Y TRAMAS
    pal=[('#7ae2a6','Menta','Acentos y titulares sobre oscuro'),('#539f73','Verde','Fondos y franjas'),('#1b4d8b','Azul oscuro','Fondo institucional y firma'),('#2d7cde','Azul','Fondos de redes y títulos sobre claro'),('#ffffff','Blanco','Texto sobre foto')]
    pl=''.join(f'<div><div style="height:150px;border-radius:16px;background:{c};border:{"3px solid #e6e2d8" if c=="#ffffff" else "none"}"></div><div class="body" style="font-size:20px;font-weight:800;margin-top:10px">{n}</div><div class="kick" style="font-size:14px;opacity:.6">{c}</div><div class="body" style="font-size:16px;margin-top:4px">{u}</div></div>' for c,n,u in pal)
    page(f'''{label('04 · Color y tramas')}{h1('La paleta del manual,<br>con una regla clara.',s=80)}
<div class="abs" style="left:110px;top:340px;width:1000px;display:grid;grid-template-columns:repeat(5,1fr);gap:18px">{pl}</div>
{p('<b>Colores de apoyo:</b> el marrón del contorno y el naranja de la madera salen de Quito y solo se usan en elementos que nacen de él (contorno de los titulares, etiquetas). Así la paleta institucional manda y el personaje aporta calidez.',110,650,1000,21)}
<div class="abs trama-b" style="left:1180px;top:110px;width:300px;height:420px;border-radius:18px;background-color:var(--navy);background-size:520px auto"></div>
<div class="abs trama-n" style="left:1510px;top:110px;width:300px;height:420px;border-radius:18px;background-color:var(--green);background-size:520px auto"></div>
{why(['Las tramas representan un banco rayado: usarlas a baja opacidad sobre fondos planos convierte el problema en textura, sin competir con la información.','Las limpiamos: quitamos palabras y dibujos inapropiados para una campaña institucional.','En fotos nunca se superponen tramas: la foto ya es la textura.'],1180,570,630)}''',sec='Sistema visual')
    # 14 LOOK FOTOGRAFICO
    page(f'''{label('04 · Look fotográfico')}{h1('Un solo filtro<br>para toda la campaña.',s=80)}
{img(im('proc/raw52.jpg',900),110,330,420,560)}{img(im('proc/grade52.jpg',900),560,330,420,560)}
{cap('Original del celular',110,905,420)}{cap('Con el look Bancala',560,905,420)}
{why(['Curva fílmica: negros apenas levantados y altas luces suaves, como un negativo de cámara profesional. Recupera los cielos quemados del celular.','Virado: sombras hacia el azul de la paleta y luces cálidas como la madera de Quito. Verdes más oliva y cielos llevados al azul de marca.','Profundidad de campo: calculamos un mapa de profundidad por IA y desenfocamos el fondo como un objetivo luminoso. El fondo se ordena, el sujeto y Quito quedan nítidos y la imagen gana aire.','Halación sutil, viñeta leve y grano fino; cada foto escalada con IA para imprimir en A3.','Se aplica igual en todas las imágenes. La coherencia es lo que hace que 40 piezas parezcan una sola campaña.'],1060,330,750)}''',sec='Sistema visual')
    # 15 INFOGRAFIA
    old=r"C:/Users/Lauti/Documents/Tecnologia del Diseño - Campaña Bancala/05_Material_Original/Infografia_version_anterior.jpeg"
    page(f'''{label('05 · Corrección: infografía')}{h1('Quito al frente,<br>fondo limpio.',s=52)}
<div class="abs" style="left:110px;top:300px;width:400px;height:560px;border-radius:14px;overflow:hidden;box-shadow:0 10px 30px rgba(42,40,41,.18)"><img src="{im(old,900)}" style="width:100%;height:auto;margin-top:-180px"></div>
{cap('Versión anterior',110,875,400)}
{img(pz('02_Impresos/Infografia_A3/Infografia_A3_La_misma_banca_distintas_historias.png',1500),600,80,640,905,r=6)}
{why(['El personaje pasa a ser el soporte de la información: su anatomía (respaldo, asiento, patas, bolso) organiza los cinco “no se banca”.','Fondo papel liso: se eliminó la textura de madera que competía con los textos.','Dos bloques legibles con signos + y −, heredados de la versión anterior, y “tres gestos que bancan” como resumen accionable.','Cierre con humor y acción: QR para avisar a Mantenimiento.','Formato A3 vertical para carteleras de pasillo; también funciona como posteo.'],1300,110,520,'Decisiones')}''',sec='Piezas')
    # 16 AFICHES
    af=sorted(os.listdir(PZ+'/02_Impresos/Afiches_A3_Serie_Te_banco_en_todas'))
    ah=''.join(img(pz('02_Impresos/Afiches_A3_Serie_Te_banco_en_todas/'+f,900),110+i*346,330,320,452,r=6) for i,f in enumerate(af))
    page(f'''{label('05 · Afiches A3')}{h1('Serie “Te banco en todas”.',s=80)}
{p('Cinco afiches para carteleras y galerías, ubicados cerca de los bancos. Cuatro marcan un límite con humor y uno celebra el vínculo.',110,230,1100,23)}
{ah}{why(['Fórmula fija: titular en una franja limpia de azul de marca, foto fundida debajo y Quito reaccionando por delante. Sin textos sobre zonas cargadas de la foto.','Fotos reales del campus con estudiantes reales: el público se ve a sí mismo.','Banda de firma institucional igual en todos: ordena las tres marcas sin invadir la foto.'],110,820,1700,'Por qué así')}''',sec='Piezas')
    # 17 ESTRATEGIA REDES
    feed=[('Posteos/Post_01_Lanzamiento_Hola_soy_Quito.png'),('Carrusel_01_Conoce_a_Quito/Carrusel01_Slide01_Portada.png'),('Posteos/Post_02_Homenaje_Mantenimiento.png'),
          ('Carrusel_02_Te_banco_en_todas_menos_en_estas/Carrusel02_Slide01_Portada.png'),('Posteos/Post_03_Anuncio_Estacion_Bancala.png'),('Carrusel_03_La_misma_banca_distintas_historias/Carrusel03_Slide01_Portada.png'),
          ('Posteos/Post_04_Stickers_Pegalos_en_tu_compu.png'),('Carrusel_02_Te_banco_en_todas_menos_en_estas/Carrusel02_Slide02_Reposera.png'),('Carrusel_01_Conoce_a_Quito/Carrusel01_Slide04_Emociones.png')]
    gh=''.join(f'<img src="{pz("01_Redes_Instagram/"+f,500)}" style="width:100%;aspect-ratio:3/4;object-fit:cover">' for f in feed)
    fases=[('Semana 1','Presentación','Quito llega: posteo de lanzamiento, carrusel “Conocé a Quito”, historia con link.'),('Semana 2','Límites con humor','Carrusel “Menos en estas”, afiches, encuesta y quiz en historias.'),
           ('Semana 3','Participación','Estación Bancala en el patio, cuenta regresiva, caja de preguntas, stickers.'),('Semana 4','Comunidad','Carrusel con historias reales, homenaje a Mantenimiento, resultados.')]
    fh=''.join(f'<div style="display:flex;gap:18px;border-top:3px solid var(--ink);padding:14px 0"><div style="width:140px"><div class="kick" style="font-size:15px;color:var(--green)">{a}</div><div class="body" style="font-size:22px;font-weight:800">{b}</div></div><div class="body" style="flex:1;font-size:19px;line-height:1.3">{c}</div></div>' for a,b,c in fases)
    page(f'''{label('05 · Redes sociales')}{h1('Instagram como<br>sala de estar.',s=80)}
<div class="abs" style="left:110px;top:340px;width:760px">{fh}</div>
{p('Instagram es donde ya está el público. Cada formato cumple un rol: el <b>feed</b> construye el personaje y la serie; los <b>carruseles</b> cuentan; las <b>historias</b> hacen participar; las <b>destacadas</b> dejan todo ordenado.',110,800,760,21)}
<div class="abs" style="left:980px;top:70px;width:420px;height:900px;border-radius:52px;background:var(--char);padding:18px">
<div style="background:#fff;border-radius:38px;height:100%;overflow:hidden">
<div style="display:flex;align-items:center;gap:14px;padding:22px 20px 14px"><div style="width:74px;height:74px;border-radius:50%;background:var(--navy);display:flex;align-items:center;justify-content:center;overflow:hidden"><img src="{png('quito/q_saludo.png',200)}" style="height:66px"></div><div><div class="body" style="font-size:19px;font-weight:800">ucasalsustentable</div><div class="body" style="font-size:14px;opacity:.7">Campaña #Bancala · Mucho más que un banco</div></div></div>
<div style="display:flex;gap:12px;padding:6px 18px 14px">{''.join(f'<div style="text-align:center"><img src="{pz("01_Redes_Instagram/Portadas_Destacadas/"+f,200)}" style="width:58px;height:58px;border-radius:50%;object-fit:cover;border:2px solid #ddd"><div style="font:600 10px Brico">{f.split("_")[2][:-4].replace("Estacion","Estación")}</div></div>' for f in sorted(os.listdir(PZ+"/01_Redes_Instagram/Portadas_Destacadas"))[:5])}</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px">{gh}</div></div></div>
{why(['Formato 4:5 (1080 × 1350): ocupa más pantalla en el feed; todo lo importante queda dentro del recorte 3:4 de la grilla.','Historias 9:16 con márgenes de seguridad arriba y abajo para no chocar con la interfaz.','Alternamos foto y color plano en la grilla: ritmo visual y reconocimiento de serie.'],1460,110,360)}''',sec='Redes')
    # 18-20 CARRUSELES
    def carpage(folder,title,intro,whys):
        fs=sorted(os.listdir(PZ+'/01_Redes_Instagram/'+folder)); n=len(fs); w=(1700-(n-1)*16)/n
        ch=''.join(img(pz('01_Redes_Instagram/'+folder+'/'+f,800),110+i*(w+16),330,w,w*1.25,r=6) for i,f in enumerate(fs))
        page(f'''{label('05 · Carrusel de Instagram')}{h1(title,s=72)}{p(intro,110,230,1500,22)}{ch}{why(whys,110,330+w*1.25+40,1700,'Formato y función')}''',sec='Redes')
    carpage('Carrusel_01_Conoce_a_Quito','01 · Conocé a Quito.','Presenta al personaje como si fuera un compañero nuevo: ficha técnica, lo que vio y su “manual de emociones”. Cierra con la pregunta que activa la campaña: “¿Vos lo bancás?”.',
        ['El carrusel premia el deslizamiento: cada lámina suma un dato y la última pide acción (guardar y compartir), las dos señales que más alcance dan.','Alternamos foto (vínculo con el campus) y fondos planos de la paleta (lectura rápida de información).','El “manual de emociones” anticipa la lógica de las piezas: cada pose de Quito equivale a una conducta.'])
    carpage('Carrusel_02_Te_banco_en_todas_menos_en_estas','02 · Te banco en todas. Menos en estas.','Adapta la serie de afiches al feed. Cada lámina es un chiste con una conducta concreta; la última traduce el humor en cuatro reglas simples.',
        ['Mismo mensaje en dos medios: el afiche impacta en el pasillo y el carrusel lo hace compartible.','Humor de situación con estudiantes reales: se comenta y se etiqueta a amigos.','Cierre con reglas numeradas y QR: el humor nunca queda sin acción.'])
    carpage('Carrusel_03_La_misma_banca_distintas_historias','03 · La misma banca. Distintas historias.','Toma el slogan de la infografía y lo convierte en relato: el primer día, los mates, la siesta, el almuerzo. Quito acompaña cada escena.',
        ['Carrusel emocional para equilibrar la serie de límites: no solo decimos qué no hacer, recordamos por qué vale la pena.','La última lámina pide historias reales: alimenta la caja de preguntas y el Muro de la Estación Bancala (contenido generado por estudiantes).','Las mejores historias recibidas vuelven en un nuevo carrusel: el público se vuelve protagonista.'])
    # 21 HISTORIAS
    sts=sorted(os.listdir(PZ+'/01_Redes_Instagram/Historias_Instagram'))
    fn=[('Link','Lleva al posteo fijado con la campaña.'),('Encuesta','Diagnóstico: cuántos admiten rayar. Se compara con la encuesta física.'),('Quiz','Refuerza el slogan: la respuesta correcta es “mucho más que un banco”.'),
        ('Slider','Mide el vínculo emocional. El cursor es Quito.'),('Preguntas','Junta historias reales para el carrusel 03 y el Muro.'),('Música','Identidad sonora: el mismo tema del reel de Quito (Le Surfuku, CC BY) y una pregunta para armar entre todos la playlist de la campaña.'),('Cuenta regresiva','Lleva tráfico al stand y activa recordatorios.')]
    sh=''.join(f'<div><img src="{pz("01_Redes_Instagram/Historias_Instagram/"+f,700)}" style="width:100%;border-radius:10px;box-shadow:0 8px 22px rgba(42,40,41,.18)"><div class="body" style="font-size:18px;font-weight:800;margin-top:12px;color:var(--blue)">{a}</div><div class="body" style="font-size:15px;line-height:1.3;margin-top:3px">{b}</div></div>' for f,(a,b) in zip(sts,fn))
    page(f'''{label('05 · Historias interactivas')}{h1('Siete historias, siete funciones.',s=72)}
{p('Las historias son el formato de participación: cada sticker nativo de Instagram (encuesta, quiz, slider, preguntas, música, cuenta regresiva, link) tiene un objetivo y un dato que nos devuelve.',110,220,1500,22)}
<div class="abs" style="left:110px;top:300px;width:1700px;display:grid;grid-template-columns:repeat(7,1fr);gap:20px">{sh}</div>''',sec='Redes')
    # 22 POSTEOS + DESTACADAS + STICKERS
    ps=sorted(os.listdir(PZ+'/01_Redes_Instagram/Posteos'))
    pp=''.join(img(pz('01_Redes_Instagram/Posteos/'+f,800),110+i*300,300,280,350,r=6) for i,f in enumerate(ps))
    hs=sorted(os.listdir(PZ+'/01_Redes_Instagram/Portadas_Destacadas'))
    hh=''.join(f'<img class="abs" src="{pz("01_Redes_Instagram/Portadas_Destacadas/"+f,300)}" style="left:{110+i*192}px;top:780px;width:170px;height:170px;border-radius:50%;object-fit:cover">' for i,f in enumerate(hs))
    page(f'''{label('05 · Posteos, destacadas y stickers')}{h1('Piezas que sostienen<br>la conversación.',s=66)}
{pp}{cap('Lanzamiento · Homenaje a Mantenimiento · Anuncio del stand · Stickers',110,665,1180)}
{p('<b>Destacadas</b>: seis portadas con Quito ordenan el perfil por tema.',110,720,1180,20)}{hh}
{img(pz('02_Impresos/Stickers/Stickers_Plancha_A4.png',900),1350,110,460,650,r=6)}
{why(['Stickers troquelados: “Pegalos en tu compu. No en el banco.” Canalizan las ganas de marcar algo hacia un objeto propio y hacen viajar la campaña fuera del campus.'],1350,790,460,'Stickers')}''',sec='Redes')
    # 23 ARQUIGRAFIA PLANO
    page(f'''{label('06 · Corrección: arquigrafía')}{h1('Estación Bancala:<br>un solo stand.',s=80)}
{p('Reunimos todas las piezas de arquigrafía en una propuesta integral, montada sobre el <b>mobiliario que ya existe</b> en el patio: el refugio rojo con asiento de madera, la mesa roja y los bancos del recorrido. No se fabrica ningún mueble nuevo; solo se viste lo existente con vinilos removibles.',110,330,700,23)}
{why(['Un punto de encuentro físico reconocible, en el lugar de mayor circulación.','Cinco piezas que trabajan juntas: atraer (panel), retener (foto con Quito), guiar (piso), participar (mesa) y extender la campaña a todo el campus (placas).','Vinilos removibles y microperforados: no dañan el mueble que la campaña pide cuidar.'],110,620,700)}
{img(pz('03_Arquigrafia_Estacion_Bancala/00_Plano_Estacion_Bancala.png',1500),880,150,930,581,r=10)}''',sec='Arquigrafía')
    # 24 ARQUIGRAFIA MOCKUP REFUGIO
    A='03_Arquigrafia_Estacion_Bancala/'
    page(f'''{label('06 · Arquigrafía · piezas 1, 2, 3 y 5')}{h1('El refugio rojo,<br>vestido de campaña.',s=56)}
{img(pz(A+'01_Panel_Refugio_Rojo/Panel_Refugio_Mockup.jpg',1500),760,70,700,933,r=8)}
{img(pz(A+'01_Panel_Refugio_Rojo/Panel_Refugio_Arte_Final.png',700),1500,70,310,465,r=6)}
{img(pz(A+'05_Placa_Bancos_Existentes/Placa_Banco_Arte_Final.png',800),1500,570,310,108,r=6,sh=False)}
{img(pz(A+'03_Vinilo_de_Piso/Vinilo_Piso_Arte_Final.png',900),1500,700,310,136,r=6,sh=False,extra='background:#c9b9a6')}
{cap('Artes finales: panel, placa y piso',1500,860,310)}
<div class="abs body" style="left:110px;top:330px;width:600px;font-size:20px;line-height:1.36">
<div style="margin-bottom:18px"><b style="color:var(--blue)">1 · Panel del refugio.</b> Vinilo microperforado sobre las chapas existentes; respeta el travesaño del mueble y deja la parte baja como zona de foto.</div>
<div style="margin-bottom:18px"><b style="color:var(--blue)">2 · Corpóreo de Quito.</b> Quito sentado en el asiento real, en foam board con borde blanco: invita a sentarse a su lado y sacarse una foto con #TeBancoEnTodas.</div>
<div style="margin-bottom:18px"><b style="color:var(--blue)">3 · Vinilo de piso.</b> Huellas desde el pasillo, “Sentate, te bancamos” y una flecha al tacho más cercano.</div>
<div><b style="color:var(--blue)">5 · Placas en bancos existentes.</b> “Te banco en todas” con QR para reportar daños: la campaña llega a cada banco del recorrido.</div></div>''',sec='Arquigrafía')
    # 25 MESA
    page(f'''{label('06 · Arquigrafía · pieza 4')}{h1('Mesa roja:<br>Muro de historias.',s=60)}
{img(pz(A+'04_Mesa_Muro_de_Historias/Mesa_Vinilo_Tablero_Mockup.jpg',1500),760,70,600,800,r=8)}
{img(pz(A+'04_Mesa_Muro_de_Historias/Mesa_Vinilo_Tablero_Arte_Final.png',1200),1400,250,420,187,r=6)}
{cap('Arte final del tablero',1400,450,420)}
{p('Sobre el tablero de la mesa roja existente se aplica un vinilo con dos zonas: una superficie tipo pizarra para escribir con tiza o marcador al agua (“Escribí tu historia acá, no en el banco”) y una encuesta física por stickers: “¿Qué le hace peor a un banco?”.',110,330,600,22)}
{why(['Convierte el impulso de rayar en participación: se escribe donde se puede borrar.','La encuesta física repite la de Instagram: comparamos resultados y los publicamos.','Las historias escritas se fotografían y alimentan el carrusel 03.'],110,640,600)}''',sec='Arquigrafía')
    # 26 ARTICULACION
    nodes=[('Pasillo y patio','Afiches, placas QR y vinilo de piso llaman la atención en el recorrido diario.','var(--mint)'),
           ('Estación Bancala','Foto con Quito, encuesta física, Muro de historias y stickers.','#ffd36b'),
           ('Instagram','Carruseles, posteos e historias interactivas amplifican lo que pasa en el patio.','#9cc3f2'),
           ('Vuelta al campus','Resultados, historias reales y homenaje a Mantenimiento vuelven al stand y a los afiches.','#f7c3a0')]
    nh=''.join(f'<div style="position:relative;background:{c};border:4px solid var(--ink);border-radius:24px;box-shadow:7px 9px 0 var(--ink);padding:26px;height:300px"><div class="dsp thin" style="font-size:52px;color:#fff">{i+1}</div><div class="body" style="font-size:26px;font-weight:800;margin-top:6px">{a}</div><div class="body" style="font-size:19px;line-height:1.32;margin-top:8px">{b}</div></div>' for i,(a,b,c) in enumerate(nodes))
    links=[('QR de placas y afiches','→ perfil y posteo fijado'),('Encuesta del tablero','↔ encuesta en historias'),('Muro de historias','↔ caja de preguntas y carrusel 03'),('Foto con el corpóreo','→ repost con #TeBancoEnTodas'),('Cuenta regresiva','→ visitas al stand'),('Stickers','→ la campaña sale del campus')]
    lh=''.join(f'<div style="display:flex;justify-content:space-between;border-top:2px solid rgba(42,40,41,.2);padding:10px 0;font:600 20px Brico"><span>{a}</span><span style="color:var(--blue)">{b}</span></div>' for a,b in links)
    page(f'''{label('07 · Articulación digital y física')}{h1('Del patio al feed,<br>y de vuelta.',s=78)}
<div class="abs" style="left:110px;top:340px;width:1700px;display:grid;grid-template-columns:repeat(4,1fr);gap:34px">{nh}</div>
<div class="abs" style="left:110px;top:700px;width:1000px">{lh}</div>
{why(['Cada pieza física tiene un espejo digital y viceversa: nada queda aislado.','El circuito es cíclico: lo que el público aporta vuelve como contenido.'],1200,700,600,'Lógica del sistema')}''',sec='Implementación')
    # 27 CRONOGRAMA + MEDICION
    rows=[('Lanzamiento','Post 01 · Carrusel 01 · Historia 01 · Destacadas','Afiches 01 y 05 · Infografía en carteleras'),('Concientización','Carrusel 02 · Historias 02, 03 y 04','Afiches 02, 03 y 04 · Placas QR en bancos'),
          ('Participación','Post 03 y 04 · Historias 05, 06 y 07','Estación Bancala: panel, corpóreo, piso, mesa · Stickers'),('Comunidad','Carrusel 03 · Post 02 · Resultados de encuestas','Muro de historias exhibido · Placas permanentes')]
    rh=''.join(f'<tr><td style="padding:18px 16px;font:800 22px Brico;color:var(--blue)">Semana {i+1}<br><span style="font:600 17px Brico;color:var(--char)">{a}</span></td><td style="padding:18px 16px;font:500 19px Brico">{b}</td><td style="padding:18px 16px;font:500 19px Brico">{c}</td></tr>' for i,(a,b,c) in enumerate(rows))
    kp=[('Participación','Votos en encuestas físicas y digitales'),('Vínculo','Respuestas en la caja de preguntas e historias en el Muro'),('Alcance','Guardados y compartidos de los carruseles'),('Conducta','Reportes por QR y relevamiento fotográfico de daños antes y después')]
    kh=''.join(f'<div style="border-top:3px solid var(--ink);padding:12px 0"><div class="body" style="font-size:21px;font-weight:800">{a}</div><div class="body" style="font-size:18px">{b}</div></div>' for a,b in kp)
    page(f'''{label('07 · Implementación')}{h1('Cuatro semanas,<br>un recorrido.',s=78)}
<table class="abs" style="left:110px;top:330px;width:1150px;border-collapse:collapse;background:var(--paper);border-radius:18px;overflow:hidden">
<tr style="background:var(--navy);color:#fff"><th style="padding:14px 16px;text-align:left;font:800 17px Brico;letter-spacing:.05em">ETAPA</th><th style="padding:14px 16px;text-align:left;font:800 17px Brico;letter-spacing:.05em">DIGITAL</th><th style="padding:14px 16px;text-align:left;font:800 17px Brico;letter-spacing:.05em">FÍSICO</th></tr>{rh}</table>
<div class="abs" style="left:1340px;top:330px;width:470px"><div class="kick" style="font-size:17px;color:var(--green);margin-bottom:8px">Indicadores</div>{kh}</div>''',sec='Implementación')
    # 28 CIERRE
    page(f'''<div class="abs" style="inset:0;background:var(--green)"></div><div class="abs trama-n" style="inset:0;opacity:.10"></div>
<div class="abs dsp bounce" data-k=".5" style="left:120px;top:200px;font-size:210px">Bancala.</div>
<div class="abs body" style="left:126px;top:470px;width:800px;font-size:34px;color:#fff;font-weight:600;line-height:1.3">Te banca todos los días.<br>Ahora te toca a vos.</div>
<div class="abs" style="left:126px;top:880px">{logos(52)}</div>
<img class="abs" src="{png('quito/q_saludo.png',900)}" style="left:1080px;top:230px;height:700px">''',num=False,strip=False)

def export(out):
    html=f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>
@page{{size:{W}px {H}px;margin:0}} html,body{{width:{W}px}} .pg{{position:relative;width:{W}px;height:{H}px;overflow:hidden;page-break-after:always;break-after:page}}
</style></head><body>{''.join(pages)}<script src="bounce.js"></script></body></html>'''
    f=SITE+'/presentacion.html'; open(f,'w',encoding='utf8').write(html)
    pg=browser().new_page(viewport={'width':W,'height':H}); pg.goto(Path(f).as_uri()); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(500)
    os.makedirs(os.path.dirname(out),exist_ok=True)
    pg.pdf(path=out,width=f'{W}px',height=f'{H}px',print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'})
    pg.close(); print('pdf',out,len(pages),'pages')

if __name__=='__main__':
    build(); export(OUT+'/01_Presentacion/Bancala_Presentacion_de_Proyecto.pdf')
