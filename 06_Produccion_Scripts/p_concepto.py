from lib import *
from p_pres import im, png, pz
W,H=794,1123
pages=[]
def page(body,n=True,bg='#fff'):
    k=len(pages)+1
    ft=f'<div class="abs kick" style="left:56px;bottom:28px;font-size:9px;opacity:.55">Bancala · Concepto y fundamentación</div><div class="abs kick" style="right:56px;bottom:28px;font-size:9px;opacity:.55">{k:02d}</div>' if n else ''
    pages.append(f'<section class="pg" style="background:{bg}">{body}{ft}</section>')
def head(sec,t,s=46,c='var(--blue)'):
    return f'<div class="abs tag" style="left:56px;top:52px;font-size:11px;background:var(--char)">{sec}</div><div class="abs dsp" style="left:54px;top:84px;font-size:{s}px;line-height:.95;color:{c}">{t}</div>'
def txt(t,x,y,w,s=11.5,wt=450,c='var(--char)'):
    return f'<div class="abs body" style="left:{x}px;top:{y}px;width:{w}px;font-size:{s}px;font-weight:{wt};line-height:1.45;color:{c}">{t}</div>'
def block(t,b,x,y,w,c='var(--paper)'):
    return f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;background:{c};border-radius:12px;padding:14px 16px"><div class="kick" style="font-size:9.5px;color:var(--green)">{t}</div><div class="body" style="font-size:11.5px;line-height:1.42;margin-top:5px">{b}</div></div>'

def build():
    page(f'''<div class="abs" style="inset:0;background:var(--navy)"></div><div class="abs trama-b" style="inset:0;opacity:.10;background-size:600px auto"></div>
<div class="abs" style="left:56px;top:60px">{logos(22)}</div>
<div class="abs kick" style="left:58px;top:250px;font-size:13px;color:var(--mint)">Documento 03 · Síntesis estratégica</div>
<div class="abs dsp" style="left:54px;top:280px;font-size:76px;line-height:.92">Concepto y<br>fundamentación.</div>
<div class="abs body" style="left:58px;top:470px;width:420px;font-size:15px;line-height:1.45;color:#fff">La lógica completa de la campaña Bancala en pocas páginas: qué problema resuelve, a quién le habla, qué dice, cómo lo dice y cómo conecta el patio con Instagram.</div>
<img class="abs" src="{png('quito/q_saludo.png',800)}" style="left:330px;top:640px;height:400px">''',n=False)
    # plan on a page
    g=[('Problema','Los bancos de patios, pasillos y galerías de la Facultad se rayan, se ensucian, se usan para lo que no son y se trasladan sin devolverlos.'),
       ('Insight','“No lo cuido porque no es mío.” Lo que es de todos parece de nadie.'),
       ('Idea','Darle cara al banco. Quito, el banquito, deja de ser un mueble y pasa a ser un amigo que te banca.'),
       ('Mensaje principal','Mucho más que un banco. Te banco en todas. Bancala.'),
       ('Público','Estudiantes de 18 a 25 años que usan a diario los espacios comunes; en segundo plano, docentes, personal y Mantenimiento.'),
       ('Objetivo','Que usen bien los bancos, no los dañen y avisen cuando están rotos.'),
       ('Tono','Cercano, con humor y siempre positivo: el amigo que te la dice sin retarte.'),
       ('Medios','Instagram (feed, carruseles, historias, destacadas), afiches A3, infografía, stickers y la Estación Bancala en el patio.')]
    gh=''.join(f'<div style="border-top:2.5px solid var(--ink);padding:10px 0 8px"><div class="kick" style="font-size:10px;color:var(--green)">{a}</div><div class="body" style="font-size:{14 if a in ("Insight","Idea","Mensaje principal") else 12}px;font-weight:{700 if a in ("Insight","Idea","Mensaje principal") else 450};line-height:1.38;margin-top:3px">{b}</div></div>' for a,b in g)
    page(f'''{head('Plan en una página','La campaña,<br>de un vistazo.')}
<div class="abs" style="left:56px;top:210px;width:682px;display:grid;grid-template-columns:1fr 1fr;gap:4px 34px">{gh}</div>
<img class="abs" src="{im('plates2/historias25_feed_full.jpg',900)}" style="left:56px;top:820px;width:682px;height:230px;object-fit:cover;border-radius:12px">''')
    # problema y publico
    page(f'''{head('01 · Problema y público','Un mueble<br>que nadie siente propio.')}
{txt('El foco son los bancos de los <b>espacios públicos y de circulación</b> de la Facultad —patios, pasillos, galerías y sectores comunes—, no el mobiliario de las aulas. Son el principal punto de encuentro del campus y, a la vez, el mobiliario más expuesto: rayones, chicles, basura, zapatillas sobre el asiento, usos de reposera o peluquería y traslados que los dejan lejos de su lugar.',56,230,420,12.5)}
{txt('Cada daño tiene un costo invisible: materiales y horas de trabajo del equipo de Mantenimiento. El problema no es de información (todos saben que no hay que rayar) sino de <b>vínculo</b>: lo que es de todos se percibe como de nadie.',56,400,420,12.5)}
{block('Público principal','Estudiantes de grado, 18 a 25 años. Pasan horas entre clases en los espacios comunes, viven en Instagram, responden al humor y comparten lo que los representa.',56,540,420,'var(--mint)')}
{block('Público secundario','Docentes, personal y el equipo de Mantenimiento, que la campaña reconoce públicamente.',56,660,420)}
{img_(im('ph/f41.jpg',700),500,230,238,260)}{img_(im('ph/f10.jpg',700),500,505,238,260)}
<div class="abs" style="left:56px;top:830px;width:682px;border-left:6px solid var(--mint);padding-left:18px"><div class="kick" style="font-size:10px;color:var(--green)">Insight</div><div class="body" style="font-size:19px;font-weight:700;line-height:1.3;margin-top:4px">Si el banco deja de ser un objeto y pasa a ser alguien, cuidarlo se vuelve natural. Nadie le rayaría la cara a un amigo.</div></div>''')
    # objetivo y mensaje
    arch=[('1 · Vínculo','Te banco en todas.','Quito acompaña los momentos reales: primer día, mates, finales, siestas, charlas.'),('2 · Límite','Menos en esta.','El humor marca la conducta concreta sin señalar a nadie: “No soy reposera”.'),('3 · Acción','Bancala.','Bancar al que te banca: usarlo bien, no dañarlo, avisar si está roto.')]
    ah=''.join(f'<div style="background:{c};border:2.5px solid var(--ink);border-radius:14px;box-shadow:4px 5px 0 var(--ink);padding:14px"><div class="kick" style="font-size:10px">{a}</div><div class="dsp thin" style="font-size:24px;margin-top:6px">{b}</div><div class="body" style="font-size:11px;line-height:1.4;margin-top:8px">{d}</div></div>' for (a,b,d),c in zip(arch,['var(--mint)','#ffd36b','#9cc3f2']))
    page(f'''{head('02 · Objetivo y mensaje','Mucho más<br>que un banco.')}
{block('Objetivo comunicacional','Que el estudiante reconozca el banco como algo que lo “banca” todos los días y adopte tres conductas: usarlo para lo que es, no dañarlo y avisar cuando está roto.',56,230,682,'var(--paper)')}
{txt('<b>Mensaje principal.</b> “Mucho más que un banco” es el paraguas: el banco es testigo y sostén de la vida universitaria. El juego de palabras <i>banco / bancar</i> —apoyar, aguantar, estar para alguien— organiza el resto de los mensajes en tres pasos que cualquier pieza puede recorrer:',56,340,682,12.5)}
<div class="abs" style="left:56px;top:440px;width:682px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px">{ah}</div>
{txt('<b>Por qué funciona.</b> Una campaña de concientización falla cuando reta: el público se defiende. Al ponerle voz al banco, el reclamo deja de venir de la institución y pasa a venir de un personaje querible. El humor baja la guardia; la acción concreta evita que el mensaje quede en simpatía.',56,660,682,12.5)}
<div class="abs" style="left:56px;top:800px;width:682px;display:flex;gap:12px;flex-wrap:wrap">{''.join(f'<span class="tag" style="font-size:12px;background:{c};color:{tc}">{t}</span>' for t,c,tc in [('#TeBancoEnTodas','var(--blue)','#fff'),('Bancala.','var(--mint)','var(--ink)'),('La misma banca. Distintas historias.','var(--green)','#fff'),('Cuidala más que a tu mamá (bueno, casi).','var(--wood)','var(--ink)')])}</div>''')
    # tono y personaje
    dos=[('Sí','“No soy tu cuaderno.”','“Prohibido escribir en el mobiliario.”'),('Sí','“Si me movés, devolveme.”','“No mover los bancos de su lugar.”'),('Sí','“Los que nos bancan a nosotros.”','“Agradecemos al área de Mantenimiento.”')]
    dh=''.join(f'<tr><td style="padding:8px 10px;font:700 12.5px Brico;color:var(--green)">{b}</td><td style="padding:8px 10px;font:500 12px Brico;color:#9a8f86;text-decoration:line-through">{c}</td></tr>' for a,b,c in dos)
    page(f'''{head('03 · Tono y personaje','Quito, el amigo<br>que te la dice.')}
{txt('<b>Tono.</b> Cercano (voseo y lenguaje de pasillo), humorístico (el chiste señala la conducta, nunca humilla a una persona), positivo (siempre cierra con algo que se puede hacer) y claro (un mensaje por pieza, legible en dos segundos).',56,230,420,12.5)}
{txt('<b>Personalidad de Quito.</b> Leal, bonachón y un poco dramático. Es testigo, no policía: acompaña, celebra, se avergüenza o se enoja, pero nunca sermonea. Sus emociones son la gramática de la campaña: feliz = vínculo; avergonzado o enojado = límite; limpiando = acción.',56,360,420,12.5)}
<img class="abs" src="{png('quito/q_tapandose.png',600)}" style="left:510px;top:220px;height:230px">
<div class="abs kick" style="left:56px;top:540px;font-size:10px;color:var(--green)">Así habla la campaña · así no</div>
<table class="abs" style="left:56px;top:560px;width:682px;border-collapse:collapse;background:var(--paper);border-radius:10px">{dh}</table>
{txt('<b>Uso del personaje.</b> Se usa tal cual fue diseñado: doce poses originales recortadas y escaladas sin redibujar. En fotografía se integra con sombra de contacto, sombra proyectada según el sol, luz y color del ambiente y el mismo grano que la foto, para que forme parte de la escena.',56,720,682,12.5)}''')
    # estrategia creativa
    fases=[('Semana 1 · Presentación','Quito llega a la facu: lanzamiento, carrusel “Conocé a Quito”, historia con link, destacadas, afiches de vínculo e infografía.'),
           ('Semana 2 · Límites con humor','Serie “Te banco en todas. Menos en estas.” en afiches y carrusel; encuesta y quiz en historias; placas con QR en los bancos.'),
           ('Semana 3 · Participación','Estación Bancala en el patio: panel, corpóreo para la foto, vinilo de piso, Muro de historias y encuesta física; stickers; cuenta regresiva.'),
           ('Semana 4 · Comunidad','Carrusel con historias reales del Muro, homenaje a Mantenimiento y publicación de resultados.')]
    fh=''.join(f'<div style="border-top:2.5px solid var(--ink);padding:10px 0"><div class="body" style="font-size:13px;font-weight:800;color:var(--blue)">{a}</div><div class="body" style="font-size:11.5px;line-height:1.4;margin-top:3px">{b}</div></div>' for a,b in fases)
    refs=[('Dumb Ways to Die · McCann Melbourne','Personajes tiernos y humor en vez de miedo: el mensaje se comparte porque entretiene.'),('Don\'t Mess with Texas · GSD&M','Hablar el idioma y el orgullo del público, no el de la institución.'),('Smokey Bear · Ad Council','Un personaje como vocero estable de todas las piezas y medios.')]
    rh=''.join(f'<div style="background:var(--paper);border-radius:10px;padding:10px 12px;margin-bottom:8px"><div class="body" style="font-size:12px;font-weight:800">{a}</div><div class="body" style="font-size:11px;line-height:1.38">{b}</div></div>' for a,b in refs)
    page(f'''{head('04 · Estrategia creativa','Del vínculo<br>a la acción.')}
{txt('La estrategia combina <b>personaje + humor + participación</b>. Primero se presenta a Quito para generar afecto; después se usa ese afecto para marcar límites con humor; por último se abre la participación para que el estudiante pase de espectador a protagonista.',56,230,682,12.5)}
<div class="abs" style="left:56px;top:330px;width:400px">{fh}</div>
<div class="abs" style="left:486px;top:340px;width:252px"><div class="kick" style="font-size:10px;color:var(--green);margin-bottom:8px">Referentes que guiaron las decisiones</div>{rh}</div>
{txt('<b>Criterio de formatos.</b> Cada formato tiene una función: el afiche impacta en el recorrido; el carrusel cuenta y se guarda; la historia pide una respuesta; el stand convierte la campaña en experiencia; el sticker la saca del campus.',56,800,682,12.5)}''')
    # sistema visual
    rules=[('Marcas','Firma fija: Bancala (campaña) + UCASAL Sustentable + UCASAL, separadas por filetes. Se eliminó el isotipo: el ícono es Quito.'),
           ('Tipografía','Display: Titan One con tratamiento propio (contorno del color del trazo de Quito, sombra tipo sticker, leve rebote por letra). Texto: Bricolage Grotesque, palo seco legible. Rock Salt queda fuera.'),
           ('Color','Paleta del manual: menta #7ae2a6, verde #539f73, azul oscuro #1b4d8b, azul #2d7cde y blanco. Marrón y naranja de Quito solo como apoyo.'),
           ('Tramas','Garabatos de banco rayado, limpios de contenido inapropiado, a baja opacidad sobre fondos planos. Nunca sobre fotos.'),
           ('Fotografía','Fotos reales del campus con un único look: curva fílmica, sombras hacia el azul, luces cálidas, profundidad de campo, halación y grano fino. Escaladas con IA para A3.'),
           ('Composición','Titular sobre una franja limpia de azul de marca que se funde con la foto; fondo desenfocado por profundidad; Quito por delante y su globo siempre sobre su cabeza; firma siempre en el mismo lugar. Sin rótulos ni numeraciones en las piezas.')]
    rr=''.join(f'<div style="border-top:2.5px solid var(--ink);padding:9px 0"><div class="kick" style="font-size:10px;color:var(--green)">{a}</div><div class="body" style="font-size:11.5px;line-height:1.4;margin-top:3px">{b}</div></div>' for a,b in rules)
    pal=''.join(f'<div style="flex:1;height:44px;background:{c};border-radius:8px;{"border:1.5px solid #ddd" if c=="#ffffff" else ""}"></div>' for c in ['#7ae2a6','#539f73','#1b4d8b','#2d7cde','#ffffff'])
    page(f'''{head('05 · Sistema visual','Un sistema,<br>muchas piezas.')}
<div class="abs" style="left:56px;top:220px;width:400px">{rr}</div>
<div class="abs" style="left:486px;top:226px;width:252px;background:var(--paper);border-radius:12px;padding:16px"><div class="dsp bounce" data-k=".6" style="font-size:40px;color:var(--mint)">Te banco<br>en todas.</div><div class="body" style="font-size:16px;font-weight:800;margin-top:10px">Bricolage Grotesque</div><div class="body" style="font-size:11px">Aa Bb Cc 0123 ¿Me bancás?</div><div style="display:flex;gap:5px;margin-top:14px">{pal}</div></div>
<img class="abs" src="{im(PZ_('02_Impresos/Afiches_A3_Serie_Te_banco_en_todas/Afiche_01_No_soy_reposera.png'),700)}" style="left:486px;top:470px;width:120px;border-radius:5px">
<img class="abs" src="{im(PZ_('01_Redes_Instagram/Carrusel_01_Conoce_a_Quito/Carrusel01_Slide04_Emociones.png'),700)}" style="left:616px;top:470px;width:122px;border-radius:5px">
<img class="abs" src="{im(PZ_('02_Impresos/Infografia_A3/Infografia_A3_La_misma_banca_distintas_historias.png'),700)}" style="left:486px;top:650px;width:120px;border-radius:5px">
<img class="abs" src="{im(PZ_('01_Redes_Instagram/Historias_Instagram/Historia_03_Quiz.png'),700)}" style="left:616px;top:640px;width:100px;border-radius:5px">''')
    # articulacion
    flow=[('Pasillo y patio','Afiches, infografía, placas QR en cada banco y vinilo de piso interrumpen el recorrido diario.','var(--mint)'),
          ('Estación Bancala','Montada sobre el refugio rojo, la mesa roja y los bancos existentes: foto con el corpóreo, encuesta física, Muro de historias, stickers.','#ffd36b'),
          ('Instagram','Feed, carruseles e historias interactivas amplifican lo que pasa en el patio y lo vuelven compartible.','#9cc3f2'),
          ('Vuelta al campus','Resultados, historias reales y el homenaje a Mantenimiento regresan al stand y a las carteleras.','#f7c3a0')]
    fl=''.join(f'<div style="background:{c};border:2.5px solid var(--ink);border-radius:12px;box-shadow:4px 5px 0 var(--ink);padding:12px 14px;margin-bottom:{14 if i<3 else 0}px;display:flex;gap:14px"><div class="dsp thin" style="font-size:28px;color:#fff">{i+1}</div><div><div class="body" style="font-size:13.5px;font-weight:800">{a}</div><div class="body" style="font-size:11.5px;line-height:1.38">{b}</div></div></div>' for i,(a,b,c) in enumerate(flow))
    links=[('QR de placas y afiches','perfil y posteo fijado'),('Encuesta del tablero','encuesta en historias'),('Muro de historias','caja de preguntas y carrusel 03'),('Foto con el corpóreo','repost con #TeBancoEnTodas'),('Cuenta regresiva','visitas al stand'),('Stickers','la campaña sale del campus')]
    lh=''.join(f'<div style="display:flex;justify-content:space-between;border-top:1.5px solid rgba(42,40,41,.2);padding:6px 0;font:600 11.5px Brico"><span>{a}</span><span style="color:var(--blue)">↔ {b}</span></div>' for a,b in links)
    kp=[('Participación','votos en encuestas físicas y digitales'),('Vínculo','respuestas en la caja de preguntas e historias del Muro'),('Alcance','guardados y compartidos de carruseles'),('Conducta','reportes por QR y relevamiento fotográfico de daños antes y después')]
    kh=''.join(f'<div class="body" style="font-size:11.5px;line-height:1.4;margin-bottom:5px"><b>{a}:</b> {b}.</div>' for a,b in kp)
    page(f'''{head('06 · Articulación','Del patio al feed,<br>y de vuelta.')}
<div class="abs" style="left:56px;top:220px;width:400px">{fl}</div>
<div class="abs" style="left:486px;top:226px;width:252px"><div class="kick" style="font-size:10px;color:var(--green);margin-bottom:6px">Cada pieza física tiene un espejo digital</div>{lh}
<div class="kick" style="font-size:10px;color:var(--green);margin:22px 0 6px">Cómo medimos</div>{kh}</div>
{txt('La campaña es un circuito: el recorrido físico capta la atención, el stand la convierte en experiencia, Instagram la amplifica y lo que el público aporta vuelve como contenido. Así ninguna pieza queda aislada y el mensaje se repite en cada punto de contacto con la misma voz y la misma imagen.',56,800,682,12.5)}''')
    # inventario
    inv=[('Redes · Instagram','4 posteos · 3 carruseles (17 láminas) · 7 historias interactivas · 6 portadas de destacadas'),('Impresos','Infografía A3 · serie de 5 afiches A3 · plancha de stickers A4'),
         ('Arquigrafía · Estación Bancala','Plano de implantación · panel del refugio · corpóreo de Quito · vinilo de piso · vinilo de tablero (Muro + encuesta) · placas QR para bancos existentes'),('Sistema','Logos vectorizados · 12 poses de Quito · tipografías · tramas limpias · look fotográfico')]
    ih=''.join(f'<div style="border-top:2.5px solid #fff;padding:10px 0"><div class="kick" style="font-size:10px;color:var(--mint)">{a}</div><div class="body" style="font-size:12.5px;line-height:1.4;color:#fff;margin-top:3px">{b}</div></div>' for a,b in inv)
    page(f'''<div class="abs" style="inset:0;background:var(--green)"></div><div class="abs trama-n" style="inset:0;opacity:.09;background-size:600px auto"></div>
<div class="abs tag" style="left:56px;top:52px;font-size:11px;background:var(--char)">07 · Entregables</div>
<div class="abs dsp" style="left:54px;top:84px;font-size:46px;line-height:.95">Lo que incluye<br>la campaña.</div>
<div class="abs" style="left:56px;top:230px;width:420px">{ih}</div>
<img class="abs" src="{png('quito/q_limpiando.png',600)}" style="left:500px;top:300px;height:300px">
<div class="abs dsp" style="left:54px;top:900px;font-size:64px">Bancala.</div>
<div class="abs" style="left:56px;top:1000px">{logos(20)}</div>''',n=False)

def img_(src,x,y,w,h): return f'<img class="abs" src="{src}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:cover;border-radius:10px">'
def PZ_(rel): return OUT+'/02_Piezas/'+rel

def export(out):
    html=f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>
@page{{size:A4;margin:0}} html,body{{width:{W}px}} .pg{{position:relative;width:{W}px;height:{H}px;overflow:hidden;page-break-after:always;break-after:page}}
</style></head><body>{''.join(pages)}<script src="bounce.js"></script></body></html>'''
    f=SITE+'/concepto.html'; open(f,'w',encoding='utf8').write(html)
    pg=browser().new_page(viewport={'width':W,'height':H}); pg.goto(Path(f).as_uri()); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(500)
    os.makedirs(os.path.dirname(out),exist_ok=True)
    pg.pdf(path=out,format='A4',print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'},prefer_css_page_size=True)
    pg.close(); print('pdf',len(pages))
if __name__=='__main__':
    build(); export(OUT+'/03_Concepto_y_Fundamentacion/Bancala_Concepto_y_Fundamentacion.pdf')
