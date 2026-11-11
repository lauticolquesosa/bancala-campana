import sys,os; S=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,S+'/sr')
import esr, torch, numpy as np
from PIL import Image
m=esr.SRVGG(nc=32); sd=torch.load(S+'/sr/general.pth',map_location='cpu'); sd=sd.get('params',sd); m.load_state_dict(sd); m.eval(); esr._m=m
for i in [int(a) for a in sys.argv[1:]]:
    out=f'{S}/phx/f{i:02d}.jpg'
    if os.path.exists(out): continue
    im=np.array(Image.open(f'{S}/ph/f{i:02d}.jpg'))
    up=esr.upscale(im,'x',tile=320)
    lan=np.array(Image.fromarray(im).resize((up.shape[1],up.shape[0]),Image.LANCZOS))
    mix=(up.astype(np.float32)*0.6+lan*0.4)
    W,H=im.shape[1]*3,im.shape[0]*3
    Image.fromarray(mix.clip(0,255).astype(np.uint8)).resize((W,H),Image.LANCZOS).save(out,quality=95)
    print('ok',i,flush=True)
