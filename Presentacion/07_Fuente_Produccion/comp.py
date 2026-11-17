"""Integracion de Quito en fotos: sombras, luz, color y grano compartidos."""
import os,numpy as np,cv2
from PIL import Image
S=os.path.dirname(os.path.abspath(__file__))
from look import grade
def load_photo(i,hi=True):
    p=f'{S}/phx/f{i:02d}.jpg' if hi and os.path.exists(f'{S}/phx/f{i:02d}.jpg') else f'{S}/ph/f{i:02d}.jpg'
    im=np.array(Image.open(p).convert('RGB')).astype(np.float32)/255
    k=im.shape[1]/960 if im.shape[1]<im.shape[0] else im.shape[1]/1280
    return im,k
def sprite(name,height,flip=False,rot=0):
    im=Image.open(f'{S}/quito/q_{name}.png').convert('RGBA')
    if flip: im=im.transpose(Image.FLIP_LEFT_RIGHT)
    if rot: im=im.rotate(rot,resample=Image.BICUBIC,expand=True)
    im=im.crop(im.getbbox())
    w=int(im.width*height/im.height); im=im.resize((w,int(height)),Image.LANCZOS)
    a=np.array(im).astype(np.float32)/255
    return a[...,:3],a[...,3]
def _shift(a,dx,dy):
    M=np.float32([[1,0,dx],[0,1,dy]]); return cv2.warpAffine(a,M,(a.shape[1],a.shape[0]))
def place(plate,name,cx,foot,height,k=1.0,flip=False,rot=0,
          sun=(-0.9,0.1),slen=0.8,hard=1.0,shadow_op=0.85,contact=0.75,
          shade=0.16,rim=0.35,ambient=0.22,soft=0.6,occ=None,ground_band=0.06,cast=True,lift=True,desat=0.92,bounce=0.18,grass=0.0):
    """plate float HxWx3. coords in 960-px photo units * k. sun=(sx,sy) shadow direction per unit height."""
    cx,foot,height=cx*k,foot*k,height*k
    rgb,a=sprite(name,height,flip,rot)
    h,w=a.shape; x0=int(cx-w/2); y0=int(foot-h)
    H,W=plate.shape[:2]
    # full-canvas alpha
    A=np.zeros((H,W),np.float32)
    xs,ys=max(0,x0),max(0,y0); xe,ye=min(W,x0+w),min(H,y0+h)
    A[ys:ye,xs:xe]=a[ys-y0:ye-y0,xs-x0:xe-x0]
    C=np.zeros((H,W,3),np.float32); C[ys:ye,xs:xe]=rgb[ys-y0:ye-y0,xs-x0:xe-x0]
    # ---- shadows on plate
    if cast and shadow_op>0:
        sx,sy=sun[0]*slen,sun[1]*slen
        M=np.float32([[1,-sx,sx*foot],[0,-sy+1-1,0]])
        # y' = foot + (foot-y)*sy ; x' = x + (foot-y)*sx
        M=np.float32([[1,-sx,sx*foot],[0,-sy,foot+sy*foot]])
        sh=cv2.warpAffine(A,M,(W,H))
        b1=cv2.GaussianBlur(sh,(0,0),max(1,height*0.004+ (1-hard)*height*0.03))
        b2=cv2.GaussianBlur(sh,(0,0),max(2,height*0.025+(1-hard)*height*0.06))
        yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
        d=np.sqrt((xx-cx)**2+(yy-foot)**2)/height
        t=np.clip(d/0.9,0,1)[...,]
        shd=(b1*(1-t)+b2*t)*shadow_op*(1-0.25*t)
        shd*= (yy>foot-height*0.12)  # only on ground-ish area
    else: shd=np.zeros((H,W),np.float32)
    # contact / ambient occlusion: bottom band of alpha
    band=A.copy(); band[:int(max(0,foot-height*ground_band))]=0
    band=cv2.GaussianBlur(band,(0,0),height*0.012)
    cont=cv2.GaussianBlur(cv2.dilate(band,np.ones((3,int(height*0.05)|1),np.uint8)),(0,0),height*0.02)
    shd=np.clip(shd+cont*contact,0,0.92)
    tint=np.array([0.30,0.34,0.45]) if hard>0.5 else np.array([0.42,0.45,0.50])
    plate=plate*(1-shd[...,None]*(1-tint))
    # ---- character relighting
    region=plate[max(0,y0):min(H,y0+h),max(0,x0):min(W,x0+w)]
    amb=region.reshape(-1,3).mean(0); amb=amb/amb.mean()
    Cc=C*(amb**ambient)
    g=Cc.mean(2,keepdims=True); Cc=g+(Cc-g)*desat
    gr=plate[min(H-1,int(foot)):min(H,int(foot+height*0.15)),max(0,x0):min(W,x0+w)]
    if gr.size: 
        gcol=gr.reshape(-1,3).mean(0); gcol=gcol/gcol.max()
        yyb=np.mgrid[0:H,0:W][0].astype(np.float32)
        wb=np.clip((yyb-(foot-height*0.45))/(height*0.45),0,1)[...,None]*bounce
        Cc=Cc*(1-wb)+Cc*gcol*wb
    # directional shade: away from light (light comes from -sun dir)
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
    lx,ly=-sun[0],-min(sun[1],0)-0.6   # light from opposite of shadow, and from above
    n=np.hypot(lx,ly); lx,ly=lx/n,ly/n
    proj=((xx-cx)*lx+(yy-(foot-height/2))*ly)/(height*0.6)
    f=1-shade*np.clip(-proj,0,1.2)*hard - shade*0.5*np.clip((yy-(foot-height*0.35))/(height*0.35),0,1)
    Cc=Cc*f[...,None]
    if rim>0:
        r=max(3,height*0.035)
        sh_a=_shift(A,-lx*r,-ly*r)
        edge=np.clip(A-sh_a,0,1); edge=cv2.GaussianBlur(edge,(0,0),r*0.35)
        lum=(C.mean(2)>0.33).astype(np.float32); lum=cv2.erode(lum,np.ones((3,3),np.uint8))
        edge=edge*cv2.GaussianBlur(lum,(0,0),1.0)
        Cc=Cc+edge[...,None]*np.array([1.0,0.90,0.72])*rim*hard*(1-Cc)
    if lift:
        blk=np.percentile(plate,1.5,axis=(0,1))
        blk=blk*0.5; Cc=blk+Cc*(1-blk)
    Cc=np.clip(Cc,0,1)
    if soft>0:
        Cc=cv2.GaussianBlur(Cc,(0,0),soft*k/3*1.0+0.3); A=cv2.GaussianBlur(A,(0,0),soft*k/3*0.8+0.25)
    if grass>0:
        Lp=plate.mean(2); hp=Lp-cv2.GaussianBlur(Lp,(0,0),2.0*k/3+1)
        hp=np.clip(hp*8,0,1)
        yyg=np.mgrid[0:H,0:W][0].astype(np.float32)
        wg=np.clip(1-(foot-yyg)/(height*grass),0,1)*(yyg<foot+3)
        A=A*(1-hp*wg*0.9)
    if occ is not None:   # polygons (photo units) where the photo stays in front of Quito
        m=np.zeros((H,W),np.uint8)
        for poly in occ: cv2.fillPoly(m,[np.int32(np.array(poly)*k)],1)
        m=cv2.GaussianBlur(m.astype(np.float32),(0,0),1.2)
        A=A*(1-m)
    return plate,Cc,A
def finish(plate,crop=None,size=None,seed=7,grain=1.0,grade_on=True):
    """crop=(x,y,w,h) in 960 units*k already; size=(W,H) output. grade at output res."""
    im=plate
    if crop: x,y,w,h=[int(v) for v in crop]; im=im[y:y+h,x:x+w]
    im8=(np.clip(im,0,1)*255).astype(np.uint8)
    if size: im8=np.array(Image.fromarray(im8).resize(size,Image.LANCZOS))
    if grade_on: im8=grade(im8,seed=seed,grain_amt=grain)
    return im8
def fit_crop(k,W,H,ar,cx=0.5,cy=0.5,zoom=1.0):
    """crop box of aspect ar=w/h inside plate WxH centered at (cx,cy) fractions"""
    if W/H>ar: h=H/zoom; w=h*ar
    else: w=W/zoom; h=w/ar
    x=np.clip(cx*W-w/2,0,W-w); y=np.clip(cy*H-h/2,0,H-h)
    return (x,y,w,h)

class Scene:
    def __init__(s,photo,hi=True):
        s.plate,s.k=load_photo(photo,hi); s.H,s.W=s.plate.shape[:2]
        s.fg=np.zeros_like(s.plate); s.A=np.zeros((s.H,s.W),np.float32); s.photo=photo
    def add(s,name,**kw):
        s.plate,C,A=place(s.plate,name,k=s.k,**kw)
        # previous fg stays on top if it overlaps? new actors go on top
        s.fg=s.fg*(1-A[...,None])+C*A[...,None]; s.A=s.A+A*(1-s.A)
        return s
    def export(s,out_prefix,ar,size,cx=0.5,cy=0.5,zoom=1.0,seed=11,grain=1.0,merged=True):
        """writes <prefix>_bg.jpg, _fg.png (+ _full.jpg). ar=w/h; size=(W,H) px"""
        from look import grade_params
        x,y,w,h=[int(round(v)) for v in fit_crop(s.k,s.W,s.H,ar,cx,cy,zoom)]
        bg=(np.clip(s.plate[y:y+h,x:x+w],0,1)*255).astype(np.uint8)
        fgc=s.fg[y:y+h,x:x+w]; Ac=s.A[y:y+h,x:x+w]
        full=(np.clip(bg/255*(1-Ac[...,None])+fgc*Ac[...,None],0,1)*255).astype(np.uint8)
        R=lambda a: np.array(Image.fromarray(a).resize(size,Image.LANCZOS))
        bg,full=R(bg),R(full); Ar=np.array(Image.fromarray((Ac*255).astype(np.uint8)).resize(size,Image.LANCZOS))
        p=grade_params(bg)
        gb=grade(bg,seed=seed,grain_amt=grain,params=p); gf=grade(full,seed=seed,grain_amt=grain,params=p)
        Image.fromarray(gb).save(out_prefix+'_bg.jpg',quality=93)
        Image.fromarray(np.dstack([gf,Ar])).save(out_prefix+'_fg.png')
        if merged: Image.fromarray(gf).save(out_prefix+'_full.jpg',quality=93)
        return gf

# ---------- v2: lente + bbox ----------
import json
def _disk(r):
    r=max(1,int(round(r))); y,x=np.mgrid[-r:r+1,-r:r+1]; k=((x*x+y*y)<=r*r+0.5).astype(np.float32)
    return k/k.sum()
def lens_blur(img,depth,focus_d,maxr,back=1.0,front=0.45,tol=0.05):
    lo,hi=np.percentile(depth,2),np.percentile(depth,99.5); dn=np.clip((depth-lo)/(hi-lo),0,1)
    r=maxr*(back*np.clip((focus_d-dn-tol)/0.30,0,1)**0.85+front*np.clip((dn-focus_d-tol*1.6)/0.30,0,1))
    r=cv2.GaussianBlur(r,(0,0),3)
    w=np.clip(r/(maxr*0.25),0.02,1)[...,None]
    levels=[0,maxr*0.25,maxr*0.5,maxr*0.75,maxr]; outs=[img]
    for L in levels[1:]:
        k=_disk(L); num=cv2.filter2D(img*w,-1,k); den=cv2.filter2D(w,-1,k)[...,None]
        outs.append(num/np.maximum(den,1e-4))
    out=np.zeros_like(img)
    for j in range(len(levels)-1):
        a,b=levels[j],levels[j+1]; t=np.clip((r-a)/(b-a),0,1)[...,None]
        m=((r>=a)&((r<b)|(j==len(levels)-2)))[...,None]
        out=np.where(m,outs[j]*(1-t)+outs[j+1]*t,out)
    return out
class Scene2(Scene):
    def __init__(s,photo,focus=None,blur=0.0065,hi=True,**kw):
        super().__init__(photo,hi)
        if focus is not None and blur>0:
            d=np.load(f'{S}/depth/d{photo:02d}.npy'); d=cv2.resize(d,(s.W,s.H),interpolation=cv2.INTER_CUBIC)
            lo,hi_=np.percentile(d,2),np.percentile(d,99.5)
            fx,fy=int(focus[0]*s.k),int(focus[1]*s.k)
            fd=np.clip((np.median(d[max(0,fy-8):fy+8,max(0,fx-8):fx+8])-lo)/(hi_-lo),0,1)
            s.plate=lens_blur(s.plate,d,fd,blur*s.W,**kw)
    def export2(s,out_prefix,ar,size,cx=0.5,cy=0.5,zoom=1.0,seed=11,grain=1.0):
        from look import grade_params
        x,y,w,h=[int(round(v)) for v in fit_crop(s.k,s.W,s.H,ar,cx,cy,zoom)]
        bg=(np.clip(s.plate[y:y+h,x:x+w],0,1)*255).astype(np.uint8)
        fgc=s.fg[y:y+h,x:x+w]; Ac=s.A[y:y+h,x:x+w]
        full=(np.clip(bg/255*(1-Ac[...,None])+fgc*Ac[...,None],0,1)*255).astype(np.uint8)
        R=lambda a: np.array(Image.fromarray(a).resize(size,Image.LANCZOS))
        bg,full=R(bg),R(full); Ar=np.array(Image.fromarray((Ac*255).astype(np.uint8)).resize(size,Image.LANCZOS))
        p=grade_params(bg)
        gb=grade(bg,seed=seed,grain_amt=grain,params=p); gf=grade(full,seed=seed,grain_amt=grain,params=p)
        Image.fromarray(gb).save(out_prefix+'_bg.jpg',quality=94)
        Image.fromarray(np.dstack([gf,Ar])).save(out_prefix+'_fg.png')
        Image.fromarray(gf).save(out_prefix+'_full.jpg',quality=94)
        m=Ar>40; ys,xs=np.where(m)
        info={}
        if len(ys):
            t,b,l,r_=int(ys.min()),int(ys.max()),int(xs.min()),int(xs.max())
            band=m[t:t+max(4,int((b-t)*0.18))]; hx=int(np.where(band.any(0))[0].mean())
            info=dict(top=t,bottom=b,left=l,right=r_,headx=hx,W=size[0],H=size[1])
        json.dump(info,open(out_prefix+'.json','w'))
        return info
