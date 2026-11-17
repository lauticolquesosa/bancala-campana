# Bancala — Página web

Sitio de la campaña **Bancala · Mucho más que un banco** (UCASAL Sustentable). Estático: HTML + CSS + Three.js + GSAP/ScrollTrigger + Lenis, todo por CDN, sin build.

- `index.html` — home: Quito en 3D que recorre todo el scroll (sigue el cursor, parpadea, cambia de emoción, reacciona al clic y se puede girar arrastrándolo), manifiesto, ficha y emociones, carrusel de poses, "Menos en estas" en scroll horizontal, "Un día en la vida de Quito" con reloj, galería en profundidad, antes/después del look, estrategia, Estación Bancala, coverflow del stand, Instagram (historias en un teléfono, destacadas y abanico), infografía con lupa, reglas y stickers arrastrables.
- `piezas.html` — archivo completo: todas las piezas, poses, stickers y fotos del campus con filtros y visor.
- `js/quito3d.js` — Quito modelado en Three.js (sombreado toon + contorno tinta, brazos y piernas de manguera, 7 expresiones y 8 poses).
- `img/` y `data/piezas.json` se generan con `python source/build_assets.py` a partir de `../Presentacion`.

Local: `npx serve .` (o `python -m http.server`). Publicado en Vercel con `vercel --prod` desde esta carpeta.
