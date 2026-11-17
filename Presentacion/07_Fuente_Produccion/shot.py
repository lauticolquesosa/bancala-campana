import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
# usage: shot.py file.html out.png width height [scale]
f,out,w,h=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]); sc=float(sys.argv[5]) if len(sys.argv)>5 else 1
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=sc)
    pg.goto(Path(f).resolve().as_uri()); pg.wait_for_timeout(300)
    pg.screenshot(path=out,full_page=True); b.close()
