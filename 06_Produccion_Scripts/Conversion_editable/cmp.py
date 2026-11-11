import sys,os
from PIL import Image
from make import DOCS,HERE
import glob
def cmp(key,idx=None,h=700):
    D=DOCS[key]; folder=os.path.dirname(D['out'])
    ORIG={'info':['Infografia_A3_La_misma_banca_distintas_historias'],'stk':['Stickers_Plancha_A4'],'plano':['00_Plano_Estacion_Bancala'],
          'panel':['Panel_Refugio_Arte_Final'],'corp':['Corporeo_Quito_Arte_Final'],'piso':['Vinilo_Piso_Arte_Final'],'mesa':['Mesa_Vinilo_Tablero_Arte_Final'],'placa':['Placa_Banco_Arte_Final']}
    origs=[os.path.join(folder,t+'.png') for t in ORIG.get(key,D['titles'])]
    out=[]
    for i,o in enumerate(origs):
        if idx is not None and i not in idx: continue
        p=f'{HERE}/preview/{key}_{i+1}.png'
        if not os.path.exists(o) or not os.path.exists(p): continue
        a=Image.open(o).convert('RGB'); b=Image.open(p).convert('RGB')
        a=a.resize((int(a.width*h/a.height),h)); b=b.resize((int(b.width*h/b.height),h))
        c=Image.new('RGB',(a.width+b.width+10,h),'red'); c.paste(a,(0,0)); c.paste(b,(a.width+10,0))
        f=f'{HERE}/preview/cmp_{key}_{i+1}.png'; c.save(f); out.append(f)
    print('\n'.join(out))
if __name__=='__main__':
    cmp(sys.argv[1],[int(x)-1 for x in sys.argv[2:]] or None)
