from lib import *
W,H=1240,1754
AF=[ # name, plate, kicker, headline, bubble(text,x,y,w,tail), n
 ('Afiche_01_No_soy_reposera','playa29','Te banco en todas. Menos en esta.','No soy<br>reposera.',('¡Tapate un poco, che!',120,930,330,'tl'),'01'),
 ('Afiche_02_No_soy_peluqueria','pelu33','Te banco en todas. Menos en esta.','No soy<br>peluquería.',('¡Los pelos van al tacho, no a mí!',430,820,400,'tr'),'02'),
 ('Afiche_03_No_soy_tu_cuaderno','cuaderno41','Te banco en todas. Menos en esta.','No soy<br>tu cuaderno.',('¡Eso no es un apunte!',150,960,330,'tl'),'03'),
 ('Afiche_04_Si_me_moves_devolveme','mudanza10','Te banco en todas. Menos en esta.','Si me movés,<br>devolveme.',('¿Me llevan… y me traen?',760,1000,360,'tr'),'04'),
 ('Afiche_05_Te_banco_en_todas','charla23','Mucho más que un banco.','Te banco<br>en todas.',('Acá se arreglan los grandes temas del mundo.',520,700,420,'tl'),'05'),
]
def poster(pl,kick,head,bub,n,size=150):
    t,bx,by,bw,tail=bub
    return f'''
<img class="abs" src="{P}{pl}_a3_bg.jpg" style="left:0;top:0;width:1240px;height:1604px">
<div class="scrimT" style="height:760px"></div>
<div class="abs kick" style="left:84px;top:86px;font-size:30px;color:#fff;opacity:.95">{kick}</div>
<div class="abs kick" style="right:84px;top:86px;font-size:30px;color:var(--mint)">{n}/05</div>
<div class="abs dsp bounce" data-k=".7" style="left:78px;top:150px;font-size:{size}px;line-height:.98">{head}</div>
<img class="abs" src="{P}{pl}_a3_fg.png" style="left:0;top:0;width:1240px;height:1604px">
<div class="bubble {tail}" style="left:{bx}px;top:{by}px;width:{bw}px;font-size:34px">{t}</div>
<div class="abs" style="left:0;right:0;top:1604px;height:150px;background:var(--navy)"></div>
<div class="abs" style="left:84px;top:1604px;height:150px;display:flex;align-items:center">{logos(52)}</div>
<div class="abs" style="right:84px;top:1604px;height:150px;display:flex;flex-direction:column;justify-content:center;align-items:flex-end">
  <div class="dsp thin" style="font-size:40px;color:var(--mint)">Mucho más que un banco.</div>
  <div class="kick" style="font-size:20px;color:#fff;margin-top:8px;opacity:.85">#TeBancoEnTodas</div></div>
'''
if __name__=='__main__':
    for name,pl,k,h,b,n in AF:
        render(name,poster(pl,k,h,b,n),W,H,f'{OUT}/02_Piezas/02_Impresos/Afiches_A3_Serie_Te_banco_en_todas/{name}.png',scale=2)
        print(name)
