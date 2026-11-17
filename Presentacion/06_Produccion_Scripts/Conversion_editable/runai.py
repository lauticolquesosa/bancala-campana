import sys,win32com.client,time
ai=win32com.client.Dispatch("Illustrator.Application")
try: ai.UserInteractionLevel=-1  # DONTDISPLAYALERTS
except Exception as e: pass
code=open(sys.argv[1],encoding='utf8').read()
t=time.time()
r=ai.DoJavaScript(code)
sys.stdout.reconfigure(encoding="utf-8",errors="replace"); print(r); print('t=%.1fs'%(time.time()-t),file=sys.stderr)
