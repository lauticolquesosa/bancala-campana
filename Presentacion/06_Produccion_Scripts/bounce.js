document.querySelectorAll('.bounce').forEach((el,ei)=>{
  const rots=[-3,2.2,-1.4,2.8,-2.2,1.6,-2.6,1.2];const ys=[0,-.03,.02,-.02,.03,-.01,.02,-.03];
  let i=ei*3;
  const walk=n=>{[...n.childNodes].forEach(c=>{
    if(c.nodeType===3){const f=document.createDocumentFragment();
      for(const ch of c.textContent){ if(ch===' '){f.appendChild(document.createTextNode(' '));continue;}
        const s=document.createElement('span');s.className='l';s.textContent=ch;
        const r=rots[i%rots.length]*(el.dataset.k?parseFloat(el.dataset.k):1),y=ys[i%ys.length];i++;
        s.style.transform=`translateY(${y}em) rotate(${r}deg)`;f.appendChild(s);}
      n.replaceChild(f,c);} else if(c.nodeType===1 && c.tagName!=='BR') walk(c);});};
  walk(el);});
