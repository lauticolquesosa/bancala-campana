import sys,glob,numpy as np,cv2
from PIL import Image
S=sys.argv[1]
for f in sorted(glob.glob(S+'/quito/q_*.png')):
    if 'saludo' in f: continue
    im=np.array(Image.open(f)); rgb=im[...,:3]; a=im[...,3].astype(np.float32)
    lab=cv2.cvtColor(rgb,cv2.COLOR_RGB2LAB).astype(np.float32)
    L=lab[...,0]; A=lab[...,1]-128; B=lab[...,2]-128
    # background reference: pure-ish white
    bgish=((L>242*255/255*1.0)&(np.abs(A)<4)&(np.abs(B)<6)).astype(np.uint8)
    dark=(L<105).astype(np.uint8)
    free=(1-cv2.dilate(dark,np.ones((3,3),np.uint8))).astype(np.uint8)
    n,lab_,st,_=cv2.connectedComponentsWithStats(free,connectivity=4)
    rm=np.zeros(L.shape,bool); cnt=0
    for i in range(1,n):
        if st[i,4]<150: continue
        m=lab_==i
        frac=bgish[m].mean()
        if frac>0.85:
            rm|=m; cnt+=1
    rmd=cv2.dilate(rm.astype(np.uint8),np.ones((3,3),np.uint8)).astype(bool)
    # in dilated ring only remove light pixels
    ring=rmd&~rm&(L>200)
    kill=(rm|ring).astype(np.float32)
    kill=cv2.GaussianBlur(kill,(0,0),0.7)
    a=a*(1-np.clip(kill*1.3,0,1))
    im[...,3]=a.astype(np.uint8)
    Image.fromarray(im).save(f); print(f.split('/')[-1],cnt)
