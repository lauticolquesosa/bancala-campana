"""Bancala Look: grade fotografico unico para toda la campana."""
import numpy as np, cv2
def _hsv(rgb):
    return cv2.cvtColor(rgb.astype(np.float32),cv2.COLOR_RGB2HSV)  # H 0-360, S,V 0-1
def _rgb(hsv):
    return cv2.cvtColor(hsv.astype(np.float32),cv2.COLOR_HSV2RGB)
def curve(t):
    s=0.5+0.5*np.tanh(1.9*(t-0.5))/np.tanh(0.95)
    return 0.028+0.945*(0.55*s+0.45*t)
def hue_band(h,c,w):
    d=np.abs(((h-c)+180)%360-180); return np.clip(1-d/w,0,1)
def grade(img, normalize=True, grain=True, vignette=True, seed=7, grain_amt=1.0, params=None):
    """img uint8 RGB -> uint8 RGB"""
    x=img.astype(np.float32)/255.
    if normalize:
        if params is None:
            L=0.2126*x[...,0]+0.7152*x[...,1]+0.0722*x[...,2]
            med=np.median(L); gain=np.clip((0.44/max(med,1e-3))**0.45,0.88,1.18)
            m=(x*gain).reshape(-1,3).mean(0); g=m.mean()/m; g=1+(g-1)*0.25
            params=(gain,g)
        gain,g=params
        x=np.clip(x*gain,0,1); x=np.clip(x*g,0,1)
    # highlight shoulder (protect skies)
    x=np.where(x>0.78,0.78+(x-0.78)*0.72,x)
    x=curve(x)
    # HSL tweaks
    hsv=_hsv(x); h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    g=hue_band(h,105,55)            # greens -> olive, softer
    h=h-10*g; s=s*(1-0.20*g)
    b=hue_band(h,212,32)            # skies -> brand blue, calmer
    h=h+(214-h)*0.35*b; s=s*(1-0.12*b)
    o=hue_band(h,28,22)             # skin/wood: warm, keep
    s=s*(1+0.04*o)
    s=s*0.95
    hsv=np.dstack([h%360,np.clip(s,0,1),v]); x=_rgb(hsv)
    # split toning
    L=(0.2126*x[...,0]+0.7152*x[...,1]+0.0722*x[...,2])[...,None]
    ws=np.clip(1-L*1.6,0,1)**2; wh=np.clip((L-0.45)/0.55,0,1)**2
    x=x+ws*np.array([-0.012,0.004,0.030])+wh*np.array([0.030,0.012,-0.022])
    x=np.clip(x,0,1)
    # halation / bloom on highlights
    H_,W_=x.shape[:2]; sig=max(H_,W_)/120
    hl=np.clip((L-0.72)/0.28,0,1)*x
    bl=cv2.GaussianBlur(hl,(0,0),sig)
    x=1-(1-x)*(1-bl*np.array([0.20,0.13,0.08]))
    if vignette:
        yy,xx=np.mgrid[0:H_,0:W_].astype(np.float32)
        r=np.sqrt(((xx-W_/2)/(W_/2))**2+((yy-H_/2)/(H_/2))**2)/1.414
        x=x*(1-0.11*np.clip(r-0.40,0,1)**1.6/0.36)[...,None]
    if grain:
        rng=np.random.default_rng(seed)
        n=rng.normal(0,1,(H_,W_)).astype(np.float32)
        n=cv2.GaussianBlur(n,(0,0),0.65)
        amp=0.022*grain_amt*(0.35+0.65*(1-np.abs(L[...,0]*2-1)))
        x=x+(n*amp)[...,None]
    return (np.clip(x,0,1)*255+0.5).astype(np.uint8)
def grade_params(img):
    x=img.astype(np.float32)/255.
    L=0.2126*x[...,0]+0.7152*x[...,1]+0.0722*x[...,2]
    med=np.median(L); gain=np.clip((0.44/max(med,1e-3))**0.45,0.88,1.18)
    m=(x*gain).reshape(-1,3).mean(0); g=m.mean()/m; g=1+(g-1)*0.25
    return (gain,g)
