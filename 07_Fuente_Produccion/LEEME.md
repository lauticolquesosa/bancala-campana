# Fuente de producción

Material con el que se generaron todas las piezas (HTML → PNG/PDF).

| Carpeta | Contenido |
|---|---|
| `site/` | HTML fuente de cada pieza (`c1_1.html` = Carrusel 01 slide 1, `s1..s7` historias, `h0..h5` destacadas, `post1..4`, `Afiche_0X`, `info`, `stk`, `panel`, `piso`, `placa`, `mesa`, `plano`, `presentacion`, `concepto`). Se abren en Chrome tal cual. |
| `plates2/` | Fotos del campus con el look Bancala, separadas en fondo (`_bg`) y primer plano recortado (`_fg`) para que el titular quede entre ambos. |
| `quito/`, `stickers/` | Poses de Quito en PNG transparente y versiones troqueladas. |
| `brand/`, `fonts/` | Logos, tramas y tipografías que usan los HTML. |
| `ph/`, `mock/`, `art/` | Fotos procesadas, mockups de arquigrafía y artes finales intermedios. |
| `*.py` | Scripts de producción (Python + Playwright). |

Para regenerar los `.ai` / `.pptx` editables: `06_Produccion_Scripts/Conversion_editable` (requiere Illustrator, Python, Playwright, python-pptx y pywin32).
