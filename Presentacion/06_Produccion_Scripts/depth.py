import sys,os,numpy as np,cv2,onnxruntime as ort
from PIL import Image
S=os.path.dirname(os.path.abspath(__file__))
sess=ort.InferenceSession(S+'/depth/da2s.onnx',providers=['CPUExecutionProvider'])
inp=sess.get_inputs()[0].name
def run(i):
    o=f'{S}/depth/d{i:02d}.npy'
    if os.path.exists(o): return
    im=np.array(Image.open(f'{S}/ph/f{i:02d}.jpg').convert('RGB'))
    H,W=im.shape[:2]; s=518/min(H,W); h,w=int(round(H*s/14)*14),int(round(W*s/14)*14)
    x=cv2.resize(im,(w,h),interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
    x=(x-[0.485,0.456,0.406])/[0.229,0.224,0.225]
    d=sess.run(None,{inp:x.transpose(2,0,1)[None].astype(np.float32)})[0]
    d=d.reshape(d.shape[-2:]); d=cv2.resize(d,(W,H),interpolation=cv2.INTER_CUBIC)
    np.save(o,d.astype(np.float32)); print('ok',i,flush=True)
for a in sys.argv[1:]: run(int(a))
