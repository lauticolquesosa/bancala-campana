"""Foto de perfil de Instagram (1080 x 1080, pensada para el recorte circular).
Quito saludando y guinando, grande, sobre azul Bancala con un sol menta detras y la trama de marca."""
from lib import *
R = os.path.normpath(S + '/..') + '/02_Piezas/01_Redes_Instagram/Foto_de_perfil'
os.makedirs(R, exist_ok=True)


def perfil(bg='#2d7cde', sun='#7ae2a6', out='Foto_perfil_Quito.png', name='perfil', qx=205, qy=170, qh=780, shy=902):
    body = f'''<div class="abs" style="inset:0;background:radial-gradient(circle at 50% 42%,{bg} 0%,{bg} 45%,#1b4d8b 100%)"></div>
<div class="abs trama-b" style="inset:0;opacity:.10;background-size:760px auto"></div>
<div class="abs" style="left:190px;top:150px;width:700px;height:700px;border-radius:50%;background:{sun};
  box-shadow:0 0 0 26px rgba(122,226,166,.28),0 0 0 58px rgba(122,226,166,.12)"></div>
<div class="abs" style="left:300px;top:{shy}px;width:480px;height:46px;border-radius:50%;
  background:radial-gradient(closest-side,rgba(27,40,70,.45),rgba(27,40,70,0))"></div>
<img class="abs" src="{Q}q_c4_8_saludo.png" style="left:{qx}px;top:{qy}px;height:{qh}px;filter:drop-shadow(0 10px 18px rgba(10,20,50,.35))">'''
    render(name, body, 1080, 1080, f'{R}/{out}')


if __name__ == '__main__':
    perfil()  # cuerpo entero
    perfil(out='Foto_perfil_Quito_cerca.png', name='perfil2', qx=62, qy=135, qh=1000, shy=2000)  # encuadre cerrado (recomendado)
