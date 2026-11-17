# Bancala — Mucho más que un banco

Campaña de UCASAL Sustentable para cuidar los bancos de los espacios comunes de la Facultad (patios, pasillos, galerías). Protagonista: Quito, el banquito.

| Carpeta | Contenido |
|---|---|
| `01_Presentacion` | PDF final de presentación del proyecto (28 láminas, 16:9) y `Bancala_Presentacion_Editable.pptx` (todo nativo: cajas de texto, formas e imágenes sueltas). |
| `02_Piezas` | Todas las piezas exportadas por separado: redes (posteos 4:5, 4 carruseles —el 04 es "Un día en la vida de Quito"—, 7 historias 9:16, destacadas), impresos (infografía A3, 5 afiches A3, stickers A4) y arquigrafía de la Estación Bancala (panel del refugio, mesa Muro de historias y placa de los bancos, con artes finales y mockups) y el **Stand Bancala** (`04_Stand_Bancala`: mockup, backwall 300 × 220 cm, mostrador, roll-up, Quito 3D en tamaño real (estatua de piso apoyada contra el backwall, punto de foto), folleto A5, afiche A3, display de mesa con QR y planta). **Cada carpeta tiene su `.ai` editable** con una mesa de trabajo por pieza o lámina. |
| `03_Concepto_y_Fundamentacion` | PDF de síntesis estratégica (A4, 9 páginas). |
| `04_Recursos` | Logos (Bancala, UCASAL, UCASAL Sustentable), 12 poses de Quito en PNG transparente + stickers, tipografías, tramas limpias y fotos del campus (originales y editadas con el look Bancala). |
| `05_Material_Original` | Presentación anterior, infografía y pieza anteriores, contexto escrito y referencias tipográficas. |
| `06_Produccion_Scripts` | Scripts que generan el look fotográfico (`look.py`), la integración de Quito en las fotos (`comp.py`, `scenes.py`) y todas las piezas (HTML → PNG/PDF). El stand se genera con `cut_quito_real.py` (recorte de la estatua de Quito en tamaño real), `p_stand.py` (piezas) y `mockup_stand.py` (render del mockup); `mockup_foto.py` monta el stand sobre una foto real del campus (cámara calibrada con los puntos de fuga de la foto, sol de mediodía). En `Conversion_editable/` está el conversor HTML → Illustrator (`.ai`) y HTML → PowerPoint (`.pptx`). |

## Archivos editables

**Illustrator (`.ai`, uno por carpeta de pieza).** Cada lámina es una mesa de trabajo con su propia capa, con nombre.
- Todo el texto es texto vivo. Los titulares llevan Titan One con el tratamiento de marca hecho con **efectos en vivo**: contorno tinta por fuera (*Desplazamiento de trazo*) y sombra desplazada (*Sombra paralela*), más la leve rotación por letra. Se edita el texto y el efecto acompaña.
- Las formas (tarjetas, globos, botones, líneas) son trazados vectoriales con relleno y trazo editables.
- Las fotos, Quito y los recortes son imágenes incrustadas que se pueden mover. Las fotos con recorte están dentro de una máscara de recorte, así que se pueden reencuadrar.
- Los logos e íconos son vectores.
- Los colores de marca están cargados como **muestras globales** (grupo "Bancala"). Si cambiás una muestra, se actualiza en toda la pieza.
- La plancha de stickers trae una capa **Troquel** (línea de corte magenta, no imprimible).
- La arquigrafía suma una mesa de trabajo con el mockup fotográfico como referencia.
- El stand (`Stand_Bancala.ai`) tiene el gran formato (backwall, mostrador, roll-up, planta) dibujado a escala 1:10 y los impresos (folleto, afiche, display) a tamaño real.
- Afiches e infografía están a tamaño A3 real y los stickers a A4. Las piezas de redes miden 1 pt = 1 px (1080 × 1350, 1080 × 1920, etc.).
- Antes de abrirlos, instalá las fuentes de `04_Recursos/Tipografias`: `TitanOne-Regular_Display.ttf`, `PatrickHandSC-Regular.ttf` y `SpaceMono-Bold.ttf` (burbujas y chip de hora del carrusel 04) y las instancias de `Instancias_estaticas_para_Illustrator/`.

**Canva.** Diseño "Bancala · Presentación de Proyecto (editable)", en Proyectos de la cuenta. Las 28 láminas tienen texto, formas e imágenes sueltas. Canva gratis no incluye Titan One y no permite subir fuentes, así que los titulares usan **Lilita One** con el efecto *Burbuja* (contorno tinta + sombra), que es la equivalente más cercana. Con Canva Pro se puede subir Titan One y reemplazarla.

Música de las historias: "Le Surfuku" – Léo Lago (CC BY). Crédito obligatorio al publicar.
