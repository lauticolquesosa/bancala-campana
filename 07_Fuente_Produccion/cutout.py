import sys,numpy as np,cv2
S=sys.argv[1]; sys.path.insert(0,S+'/sr')
from esr import upscale
from PIL import Image
I=r"C:/Users/Lauti/Documents/Tecnologia del Diseño - Campaña Bancala/Contexto/imagenes/"
C=r"C:/Users/Lauti/Documents/Tecnologia del Diseño - Campaña Bancala/Contexto/"
src={
 'policia':I+'WhatsApp Image 2026-11-10 at 20.48.53 (1).jpeg',
 'paraguas':I+'WhatsApp Image 2026-11-10 at 20.48.53 (10).jpeg',
 'preocupado_sentado':I+'WhatsApp Image 2026-11-10 at 20.48.53 (2).jpeg',
 'limpiando':I+'WhatsApp Image 2026-11-10 at 20.48.53 (3).jpeg',
 'sentado_feliz':I+'WhatsApp Image 2026-11-10 at 20.48.53 (4).jpeg',
 'triste_sentado':I+'WhatsApp Image 2026-11-10 at 20.48.53 (5).jpeg',
 'juntando_basura':I+'WhatsApp Image 2026-11-10 at 20.48.53 (6).jpeg',
 'llorando':I+'WhatsApp Image 2026-11-10 at 20.48.53 (7).jpeg',
 'senalando_feliz':I+'WhatsApp Image 2026-11-10 at 20.48.53 (8).jpeg',
 'tapandose':I+'WhatsApp Image 2026-11-10 at 20.48.53 (9).jpeg',
 'enojado':C+'WhatsApp Image 2026-11-09 at 19.26.09 (1).jpeg',
}
def cut(rgb, keep_marks=True):
    H,W=rgb.shape[:2]
    lab=cv2.cvtColor(rgb,cv2.COLOR_RGB2LAB); L=lab[...,0].astype(int)
    dark=(L<105).astype(np.uint8)
    barrier=cv2.dilate(dark,np.ones((3,3),np.uint8))
    free=(1-barrier).astype(np.uint8)
    # flood from border over free pixels
    n,labs=cv2.connectedComponents(free,connectivity=4)
    border=set(np.unique(np.concatenate([labs[0],labs[-1],labs[:,0],labs[:,-1]])))
    border.discard(0)
    bg=np.isin(labs,list(border))
    fg=~bg
    # remove small specks (noise) but keep emotion marks: drop comps < area thr
    n2,l2,st,_=cv2.connectedComponentsWithStats(fg.astype(np.uint8),connectivity=8)
    keep=np.zeros(n2,bool)
    big=st[1:,4].max()
    for i in range(1,n2):
        if st[i,4]>big*0.002: keep[i]=True
    fg=keep[l2]
    # undo the barrier dilation on the outside: erode by 1 where it's bg-ish light pixels
    a=fg.astype(np.float32)
    a=cv2.GaussianBlur(a,(0,0),0.8)
    a=np.clip((a-0.15)/0.7,0,1)
    return (a*255).astype(np.uint8)
for name,f in src.items():
    im=np.array(Image.open(f).convert('RGB'))
    if name=='enojado': im=im[545:1055]
    # crop margins to region of interest roughly (keep all)
    up=upscale(im,S+'/sr/animev3.pth')
    up=np.array(Image.fromarray(up).resize((im.shape[1]*2,im.shape[0]*2),Image.LANCZOS))
    a=cut(up)
    rgba=np.dstack([up,a]); bb=Image.fromarray(a).getbbox()
    out=Image.fromarray(rgba).crop(bb)
    out.save(S+f'/quito/q_{name}.png'); print(name,out.size)
# cover
im=np.array(Image.open(S+'/pdfimg/p01_x44_520x501_a.png').convert('RGBA'))
up=upscale(im[...,:3],S+'/sr/animev3.pth')
a=np.array(Image.fromarray(im[...,3]).resize((up.shape[1],up.shape[0]),Image.LANCZOS)).astype(np.float32)
a=np.clip((a-60)/(255-120)*255,0,255).astype(np.uint8)
out=Image.fromarray(np.dstack([up,a])); out=out.crop(out.getbbox()); out.save(S+'/quito/q_saludo.png'); print('saludo',out.size)
