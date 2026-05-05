---
name: content-from-transcript
description: Genera un borrador de post de LinkedIn en la voz de Amauri a partir de una transcripción, concepto del Brain, o idea directa. L2 — AI drafts, Amauri reviews and publishes.
trigger: "genera un post", "content de esta reunión", "post de este evento", "procesa para LinkedIn", "post de esta idea", "revisa mi brain"
bike-method-phase: 1  # Phase 1 — Training wheels. Amauri revisa cada borrador antes de publicar.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

# content-from-transcript

Genera un borrador de LinkedIn en la voz de Amauri. Un input = un borrador. Amauri publica.

## Cadencia objetivo: 3 posts por semana

| Tipo | Frecuencia | Fuente |
|---|---|---|
| Producto / Builder | 1x/semana | Meeting Notes, decisiones técnicas de 1Klick |
| Comunidad | 1x/semana | Eventos, meetups, speakers, LATAM tech |
| Perspectiva | 1x/semana | Brain (`wiki/concepts/`) |

Si el usuario no especifica el tipo, preguntar cuál de los tres quiere generar esta vez para mantener balance semanal.

---

## Paso 1 — Obtener el input

### Opción A — Transcripción de reunión
El usuario pega la transcripción, o dice "usa la reunión de [nombre]" → buscar en Notion con `notion-search` en Meeting Notes y obtener el campo Transcripción.

### Opción B — Brain
El usuario dice "revisa mi brain" → leer `Amauri Brain/index.md`, identificar los 3 conceptos más relevantes o recientes y presentarlos para que elija.

### Opción C — Input directo
El usuario pega o escribe una idea cruda en el chat. Usar eso como base.

---

## Paso 2 — Leer la voz y el Brain

**Primero:** leer `references/voice.md`.

**Segundo:** leer el Brain:
- `Amauri Brain/wiki/entities/Amauri Sotolongo.md` — quién es, cómo piensa
- Si el concepto elegido está en `wiki/concepts/`, leerlo completo para anclar el borrador en ideas reales de Amauri

**Reglas de voz:**
- Frases cortas. Narrativa antes que datos.
- Empezar con algo que pasó — no con una lección.
- Comunidad sobre promoción. Humano sobre corporativo.
- Español latino natural. No traducir del inglés.
- Emojis funcionales (1-2 máximo, no decorativos).
- Hashtags al final, 4-6 relevantes.
- Sin em dashes (—) en exceso.

---

## Paso 3 — Extraer el insight

Identificar el momento más valioso:
- ¿Qué fue sorprendente, inesperado o contraintuitivo?
- ¿Qué aprendiste que no sabías antes?
- ¿Qué decisión tomaron que vale la pena compartir?

Si hay varios candidatos, presentar los 2 mejores: *"¿Cuál resuena más contigo?"*

---

## Paso 4 — Redactar el borrador

Estructura base:

```
[Línea de apertura — algo que pasó, concreto y específico]

[1-2 líneas de contexto]

[El insight — qué cambió en cómo piensas]

[Implicación para la audiencia LATAM]

[Cierre con comunidad o pregunta]

[Hashtags]
```

**No usar:**
- "Es un honor compartir..."
- Jerga corporativa o anglicismos innecesarios
- Más de 150 palabras en el cuerpo

---

## Paso 5 — Presentar y refinar

```
---
BORRADOR — revisa antes de publicar

[post]

---
¿Cambios? Dime qué ajustar o di "listo" para terminar.
```

Máximo 2 rondas de refinamiento. En la tercera, preguntar si prefiere reescribir desde cero con un insight diferente.

---

## Paso 6 — Imagen (opcional)

Cuando el usuario aprueba el borrador, ofrecer generar imagen con gpt-image-1:

```python
import urllib.request, json, base64

key = open('/Users/amaurisotolongo/Desktop/AmauriOS/AIS-OS/.env').read().split('OPENAI_API_KEY=')[1].split('\n')[0].strip()

# Construir prompt: minimalista, editorial, sin texto, sin logos
# Colores cálidos, profesional, LinkedIn-ready, 1024x1024

payload = json.dumps({
    "model": "gpt-image-1",
    "prompt": "[prompt basado en el tema del post]",
    "n": 1,
    "size": "1024x1024"
}).encode()

req = urllib.request.Request(
    "https://api.openai.com/v1/images/generations",
    data=payload,
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())

b64 = data["data"][0]["b64_json"]
slug = "[slug-del-post]"  # ej: post-bote-mercado
out_path = f"/Users/amaurisotolongo/Desktop/posts/{slug}.png"
with open(out_path, "wb") as f:
    f.write(base64.b64decode(b64))

print(f"Imagen guardada en: {out_path}")
```

La imagen se guarda directamente en `Desktop/posts/` con el nombre del post como slug.

---

## Paso 7 — Dar el texto final y registrar

1. Entregar el texto con espacios listos para copiar a LinkedIn.
2. Recordar: *"Bike Method Phase 1 — tú publicas manualmente."*
3. Cuando confirme que publicó, crear entrada en `📲 LinkedIn Posts` (DB: `658ab7b2-77ca-46aa-ade4-745fa2b5911b`, data source: `8dd5ea91-9a7b-4bb1-84ff-1981a4e0c708`) con:
   - `Post`: título corto del post
   - `Fecha`: fecha de hoy
   - `Tipo`: Perspectiva / Producto/Builder / Comunidad
   - `Fuente`: Brain / Meeting Notes / Inbox
   - `Publicado`: true

---

## Reglas críticas

1. **Amauri siempre revisa antes de publicar.** Esta skill nunca publica directamente.
2. **Un insight por post.** No meter todo.
3. **Si la transcripción es de cliente**, preguntar sensibilidad antes de redactar.
4. **Si no hay input disponible**, pedirlo. No inventar contenido.
5. **Si suena genérico o corporativo**, reescribir.
