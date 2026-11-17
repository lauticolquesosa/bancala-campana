import glob,os,sys
from PIL import Image, ImageDraw, ImageFont
S=sys.argv[1]
base=r"C:/Users/Lauti/Documents/Tecnologia del Diseño - Campaña Bancala/Contexto/imagenes"
fs=sorted(glob.glob(base+'/*.jpeg'))+sorted(glob.glob(S+'/zip/*.jpeg'))
with open(S+'/zip/index.txt','w',encoding='utf8') as o:
    for i,f in enumerate(fs):
        im=Image.open(f); o.write(f"{i}\t{f}\t{im.size}\n")
cw,ch=300,400
font=ImageFont.load_default()
for k in range(0,len(fs),12):
    sheet=Image.new('RGB',(cw*4,ch*3),'white'); d=ImageDraw.Draw(sheet)
    for j,f in enumerate(fs[k:k+12]):
        im=Image.open(f).convert('RGB'); im.thumbnail((cw,ch)); x=(j%4)*cw; y=(j//4)*ch
        sheet.paste(im,(x,y)); d.rectangle([x,y,x+40,y+20],fill='yellow'); d.text((x+4,y+4),str(k+j),fill='black',font=font)
    sheet.save(S+'/zip/sheet%d.png'%(k//12))
print(len(fs))
