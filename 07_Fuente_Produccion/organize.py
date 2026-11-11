import os,shutil,glob,sys
sys.path.insert(0,'.')
from PIL import Image
import numpy as np
from look import grade
S=os.getcwd()
P=r"C:/Users/Lauti/Documents/Tecnologia del Diseño - Campaña Bancala"
C=P+'/Contexto'
def mk(d): os.makedirs(d,exist_ok=True); return d
# 1-3 entregables
for d in ['01_Presentacion','02_Piezas','03_Concepto_y_Fundamentacion']:
    if os.path.exists(P+'/'+d): shutil.rmtree(P+'/'+d)
    shutil.copytree(S+'/out/'+d,P+'/'+d)
R=mk(P+'/04_Recursos')
L=mk(R+'/Logos')
for f in ['bancala_color.svg','bancala_blanco.svg','bancala_negro.svg','ucasal_color.svg','ucasal_blanco.svg','ucasal_sustentable_color.png','ucasal_sustentable_blanco.png']:
    a,b=os.path.splitext(f); shutil.copy(S+'/brand/'+f,L+'/Logo_'+a.title().replace('_','_')+b)
Q=mk(R+'/Personaje_Quito/Poses_PNG_transparente'); ST=mk(R+'/Personaje_Quito/Stickers_troquelados')
for f in glob.glob(S+'/quito/q_*.png'):
    n=os.path.basename(f)[2:-4]
    if n=='corporeo': continue
    shutil.copy(f,Q+'/Quito_'+n+'.png')
for f in glob.glob(S+'/stickers/st_*.png'): shutil.copy(f,ST+'/Sticker_Quito_'+os.path.basename(f)[3:])
T=mk(R+'/Tipografias')
shutil.copy(S+'/fonts/TitanOne-Regular.ttf',T+'/TitanOne-Regular_Display.ttf'); shutil.copy(S+'/fonts/Bricolage.ttf',T+'/BricolageGrotesque-Variable_Texto.ttf')
open(T+'/LEEME.txt','w',encoding='utf8').write('Titan One (display, licencia OFL) y Bricolage Grotesque (texto, licencia OFL), ambas de Google Fonts.\nTratamiento del display: contorno #3a1d0c al 8,5 % del cuerpo + sombra desplazada (5,5 % / 7 %) + leve rotación alternada por letra.\n')
TR=mk(R+'/Tramas'); shutil.copy(S+'/brand/trama_blanca.png',TR+'/Trama_blanca_limpia.png'); shutil.copy(S+'/brand/trama_negra.png',TR+'/Trama_negra_limpia.png')
# fotos
FO=mk(R+'/Fotos_Campus/Originales'); FE=mk(R+'/Fotos_Campus/Editadas_Look_Bancala')
idx=[l.split('\t') for l in open(S+'/zip/index.txt',encoding='utf8')]
QMAP={0:'policia',1:'paraguas',2:'preocupado_sentado',3:'limpiando',4:'sentado_feliz',5:'triste_sentado',6:'juntando_basura',7:'llorando',8:'senalando_feliz',9:'tapandose'}
QO=mk(R+'/Personaje_Quito/Originales')
k=0
for i,f,_ in idx:
    i=int(i)
    if i in QMAP: shutil.move(f,QO+f'/Quito_{QMAP[i]}_original.jpeg'); continue
    if i==11: shutil.move(f,L+'/Referencia_UCASAL_Sustentable_captura.jpeg'); continue
    if i==12: shutil.move(f,mk(P+'/05_Material_Original/Referencias_tipograficas')+'/Referencia_tipografica_05.jpeg'); continue
    k+=1; name=f'Campus_{k:02d}'
    if os.path.exists(f) and 'scratchpad' not in f: shutil.move(f,FO+f'/{name}.jpeg')
    else: shutil.copy(f,FO+f'/{name}.jpeg')
    src=S+f'/phx/f{i:02d}.jpg' if os.path.exists(S+f'/phx/f{i:02d}.jpg') else S+f'/ph/f{i:02d}.jpg'
    im=np.array(Image.open(src).convert('RGB'))
    Image.fromarray(grade(im,seed=i,grain_amt=0.8)).save(FE+f'/{name}_look.jpg',quality=92)
    print(name,flush=True)
# material original
MO=mk(P+'/05_Material_Original')
shutil.move(C+'/Presentación de Proyecto Trabajo Sustentable Madera Collage Blanco y Marrón.pdf',MO+'/Presentacion_version_anterior.pdf')
shutil.move(C+'/contexto.md',MO+'/Contexto_campana.md')
shutil.move(C+'/WhatsApp Image 2026-11-09 at 19.26.09.jpeg',MO+'/Infografia_version_anterior.jpeg')
shutil.move(C+'/WhatsApp Image 2026-11-09 at 19.26.09 (1).jpeg',QO+'/Quito_enojado_original.jpeg')
shutil.move(C+'/WhatsApp Image 2026-11-09 at 19.26.09 (2).jpeg',MO+'/Pieza_version_anterior_mesa_roja.jpeg')
RT=mk(MO+'/Referencias_tipograficas')
for j,f in enumerate(sorted(glob.glob(C+'/referencias/combinaciones tipograficas/*.jpeg'))):
    shutil.move(f,RT+f'/Referencia_tipografica_{j+1:02d}.jpeg')
