---
name: ingest
description: Procesa el Notion Inbox de Amauri (o un item directo) al Brain. Clasifica cada item, crea páginas wiki, cross-linkea con lo existente, y flaggea candidatos a LinkedIn post.
trigger: "procesa mi inbox", "vacía el inbox", "ingest", "guarda esto en el brain", "procesa esto"
bike-method-phase: 2  # Phase 2 — AI processes, Amauri reviews output before Brain is final.
---

# ingest

Toma el caos del Inbox y lo convierte en conocimiento estructurado en el Brain. Un run = inbox procesado + wiki actualizada.

## Notion Inbox

- **URL:** https://www.notion.so/32a68a705e15802495b8ecaccf6fbe67
- **Tipo:** página libre (no database) — bullets, texto, links, imágenes

---

## Paso 0 — ¿Hay un video/podcast para transcribir?

Si el usuario manda una URL de YouTube antes de ingestar → correr primero:
```
python3 scripts/transcribe_youtube.py <URL>
```
Esto guarda el audio transcrito en `Amauri Brain/raw/YYYY-MM-DD-slug.md`. Luego continuar con Modo C.

---

## Paso 1 — Obtener el input

### Modo A — Inbox completo
El usuario dice "procesa mi inbox" o "vacía el inbox" → leer la página del Inbox con `notion-fetch` (ID: `32a68a70-5e15-8024-95b8-ecaccf6fbe67`) y extraer todos los items.

### Modo B — Item directo
El usuario pega o escribe algo en el chat → usar eso como input. No leer Notion.

### Modo C — Raw file ya existe en Brain/raw/
El usuario dice "procesa el transcript de [video]" o "ya transcribí el video" → preguntar qué quiere extraer: *"¿Qué buscamos en el transcript? ¿Un tema específico o proceso todo?"*
- Si da un tema específico (ej: "lo de One Piece") → buscar ese fragmento en el raw file y extraer solo ese concepto
- Si dice "todo" → leer el raw completo y clasificar todos los insights relevantes

Para buscar en el raw file usar Bash grep o Read con el path correcto en `Amauri Brain/raw/`.

---

## Paso 2 — Clasificar cada item

Para cada item del inbox, asignar una categoría:

| Categoría | Criterio | Destino |
|---|---|---|
| `concepto` | idea, aprendizaje, reflexión, framework, metáfora | `Amauri Brain/wiki/concepts/` |
| `entidad` | persona, empresa o producto nuevo que aparecerá 2+ veces | `Amauri Brain/wiki/entities/` |
| `referencia` | link, artículo, recurso externo | `Amauri Brain/wiki/topics/` (tag: source-summary) |
| `feature/tarea` | algo que hay que hacer en 1Klick o Digital Compass | **skip Brain** — solo confirmar a Amauri que va a Tareas |
| `ruido` | item sin valor claro, screenshot sin contexto, link sin descripción | **skip** — preguntar a Amauri si quiere descartarlo |

Presentar la clasificación antes de procesar:
```
Encontré X items en el Inbox:

✅ concepto — "Metáfora de One Piece startupeable"
✅ concepto — "Agregar home como chat estilo Attio" → feature/tarea de 1Klick
🔗 referencia — link x.com/clear_graphics
⚠️ ruido — screenshot sin contexto (3 imágenes)

¿Proceso los conceptos y referencias? ¿Qué hago con el ruido?
```

Esperar confirmación antes de escribir al Brain.

---

## Paso 3 — Leer el Brain antes de escribir

Antes de crear páginas nuevas:
1. Leer `Amauri Brain/index.md` — verificar si el concepto ya existe
2. Si existe → actualizar la página existente en lugar de crear una nueva
3. Si es nuevo → crear página nueva con el template correcto

---

## Paso 4 — Escribir al Brain

### Para cada `concepto` nuevo:
Crear `Amauri Brain/wiki/concepts/[slug].md` con:

```markdown
---
title: [Título del concepto]
type: concept
tags: [tag relevante]
sources: 1
updated: YYYY-MM-DD
---

# [Título]

> "[Cita o idea central en una línea]"

**Tipo:** [categoría — ej: Founder Mindset, Ventas, Producto]
**Fuente:** Notion Inbox — YYYY-MM-DD

[Desarrollo del concepto en 2-4 líneas]

**Aplicación a [[1Klick]]:** [cómo conecta con el contexto actual]

**Ver también:** [[página relacionada]] si existe
```

### Para cada `referencia` nuevo:
Crear `Amauri Brain/wiki/topics/[slug].md` con:

```markdown
---
title: [Título del recurso]
type: topic
tags: [source-summary, tema]
sources: 1
updated: YYYY-MM-DD
---

# [Título]

**Fuente:** [URL]
**Fecha:** YYYY-MM-DD

[Resumen en 3-5 líneas de qué hay ahí y por qué importa]

**Aplicación a [[1Klick]] o [[Digital Compass]]:** [conexión concreta]
```

---

## Paso 5 — Actualizar index.md y log.md

Después de escribir todas las páginas:

1. Agregar cada página nueva a `Amauri Brain/index.md` bajo la sección correspondiente:
   ```
   - [[slug|Título]] — una línea de resumen (1 source)
   ```

2. Agregar entrada a `Amauri Brain/log.md`:
   ```
   ## [YYYY-MM-DD] ingest | Inbox — N items procesados
   Conceptos creados: X. Referencias: Y. Features/tareas skipped: Z.
   ```

---

## Paso 6 — Flaggear candidatos a LinkedIn

Al final, revisar los items procesados y señalar los que tienen potencial de post:

```
📲 Candidatos a LinkedIn:
- "Metáfora de One Piece startupeable" → tipo Perspectiva, buena narrativa
- [otro si aplica]

¿Quieres generar alguno ahora con /content-from-transcript?
```

Solo flaggear si el concepto tiene una narrativa clara o metáfora potente. No flaggear features ni referencias técnicas.

---

## Paso 7 — Limpiar el Inbox (opcional)

Preguntar: *"¿Lo quito del Inbox de Notion?"*

- Si el input fue **Modo A o B** (Inbox de Notion) → usar `notion-update-page` con `update_content` para borrar solo el item procesado (old_str = texto exacto del item, new_str = ""). No borrar todo el Inbox.
- Si el input fue **Modo C** (transcript de YouTube) → no hay nada que borrar del Inbox a menos que había una línea con el link o referencia al video.

Nunca reemplazar todo el contenido del Inbox — solo el item específico procesado.

---

## Reglas críticas

1. **Nunca escribir al Brain sin confirmación de la clasificación.** Siempre mostrar el Paso 2 antes de procesar.
2. **Nunca modificar `raw/`.** El Inbox de Notion es el raw — se procesa, no se archiva ahí.
3. **Un concepto = una página.** No meter dos ideas distintas en la misma página.
4. **Si un item es ambiguo**, preguntar a Amauri antes de clasificar. No asumir.
5. **Features y tareas de producto no van al Brain.** Son de Notion Tareas — solo confirmar que las vio.
