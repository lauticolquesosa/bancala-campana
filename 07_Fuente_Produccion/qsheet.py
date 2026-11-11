import sys,glob,os
from PIL import Image,ImageDraw
S=sys.argv[1]; pat=sys.argv[2] if len(sys.argv)>2 else 'q_*.png'
fs=sorted(glob.glob(S+'/quito/'+pat)); cw=400
sh=Image.new('RGB',(cw*4,cw*((len(fs)+3)//4)),(90,170,120)); d=ImageDraw.Draw(sh)
for j,f in enumerate(fs):
    im=Image.open(f); im.thumbnail((cw-10,cw-20)); x=(j%4)*cw; y=(j//4)*cw
    sh.paste(im,(x+5,y+18),im); d.text((x+4,y+2),os.path.basename(f),fill='white')
sh.save(S+'/quito_sheet.png')
