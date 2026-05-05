---
name: content-from-transcript
description: Convierte una transcripción, idea o aprendizaje en borrador de post de LinkedIn en la voz de Amauri. L2 — AI drafts, Amauri reviews and publishes.
trigger: "genera un post", "content de esta reunión", "post de este evento", "procesa para LinkedIn", "post de esta idea", "usa mis aprendizajes"
bike-method-phase: 1  # Phase 1 — Training wheels. Corre manualmente primero. Amauri revisa cada borrador antes de publicar.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

# content-from-transcript

Convierte una transcripción en borrador de LinkedIn en la voz de Amauri. Una transcripción = un borrador. Amauri publica.

## Cadencia objetivo: 3 posts por semana

| Tipo | Frecuencia | Fuente |
|---|---|---|
| Producto / Builder | 1x/semana | Meeting Notes, Tareas de Notion, decisiones técnicas de 1Klick |
| Comunidad | 1x/semana | Eventos, meetups, speakers, LATAM tech |
| Perspectiva | 1x/semana | Ideas o Aprendizajes de Notion |

Si el usuario no especifica el tipo, preguntar cuál de los tres quiere generar esta vez para mantener balance semanal.

## Cuándo usar esta skill

- Después de un evento (Cumbre, meetup, conferencia)
- Después de una reunión interesante con un cliente o colaborador
- Cuando quieres publicar pero no sabes por dónde empezar
- Cuando tienes una idea o aprendizaje guardado en Notion que merece un post

## Fuentes de input (en orden de preferencia)

### Opción A — Transcripción de reunión
El usuario pega la transcripción en el chat, o dice "usa la reunión de [nombre]" → buscar en Notion (`notion-search` en Meeting Notes) y obtener el campo Transcripción.

### Opción B — Ideas de Notion
El usuario dice "usa mis ideas" o "genera un post de [tema]" → buscar en la database Ideas (ID: 32a68a70-5e15-8073-bae9-fafdbf0015ad) y presentar las 3 más recientes para que el usuario elija.

### Opción C — Aprendizajes de Notion
El usuario dice "usa mis aprendizajes" → buscar en la database Aprendizajes (ID: 32a68a70-5e15-80cb-a520-e25104c1c0e0) y presentar los 3 más recientes para que el usuario elija.

### Opción D — Input directo
El usuario pega o escribe una idea cruda en el chat. Usar eso como base.

### Paso 2 — Leer la voz

Leer `references/voice.md` para calibrar el registro antes de redactar.

**Reglas de voz de Amauri:**
- Frases cortas. Narrativa antes que datos.
- Empezar con algo que pasó — no con una lección.
- Comunidad sobre promoción. Humano sobre corporativo.
- Español latino natural. No traducir del inglés.
- Emojis funcionales (1-2 máximo, no decorativos).
- Hashtags al final, 4-6 relevantes.
- Sin em dashes (—) en exceso.

### Paso 3 — Extraer el insight

Identificar el momento más valioso de la transcripción:
- ¿Qué fue sorprendente, inesperado o contraintuitivo?
- ¿Qué aprendiste que no sabías antes?
- ¿Qué momento generó más energía o reacción?
- ¿Qué decisión tomaron que vale la pena compartir?

Si hay varios candidatos, presentar los 2 mejores y preguntar: *"¿Cuál resuena más contigo?"*

### Paso 4 — Redactar el borrador

Estructura probada de Amauri (basada en sus posts de mayor alcance):

```
[Línea de apertura — algo que pasó, concreto y específico]

[1-2 líneas de contexto — qué hacías, con quién, para qué]

[El insight o aprendizaje — qué cambió en cómo piensas]

[Implicación — por qué importa para tu audiencia en LATAM]

[Cierre con comunidad — qué viene, invitación a seguir]

[Emojis funcionales si aplican]

[Hashtags]
```

**No usar:**
- Frases genéricas tipo "Es un honor compartir..."
- Listas de bullets en el cuerpo del post
- Jerga corporativa o anglicismos innecesarios
- Más de 150 palabras en el cuerpo principal

### Paso 5 — Presentar y refinar

Presentar el borrador con:
```
---
BORRADOR — revisa antes de publicar

[post]

---
¿Cambios? Dime qué ajustar o di "listo" para terminar.
```

Si el usuario pide ajustes, hacer máximo 2 rondas de refinamiento. En la tercera, preguntar si prefiere reescribir desde cero con un insight diferente.

### Paso 6 — Imagen (opcional)

Cuando el usuario aprueba el borrador, ofrecer generar imagen con DALL-E 3:

```python
import urllib.request, json, os
key = os.environ.get('OPENAI_API_KEY') or open('.env').read().split('OPENAI_API_KEY=')[1].split('\n')[0]
# Construir prompt basado en el tema del post
# Estilo: minimalista, profesional, tonos del post, sin texto en la imagen
# Tamaño: 1024x1024, model: gpt-image-1 (devuelve b64_json, guardar en /tmp/)
```

Entregar el URL de la imagen. Advertir que expira en 2 horas — descargar inmediatamente.

### Paso 7 — Cierre

Cuando el usuario aprueba:
- Confirmar que el borrador está listo para copiar a LinkedIn
- Recordar: *"Bike Method Phase 1 — tú publicas manualmente. El AIOS no tiene acceso a LinkedIn."*
- Sugerir guardarlo en Notion si quiere mantener historial de posts

## Reglas críticas

1. **Amauri siempre revisa antes de publicar.** Esta skill nunca publica directamente.
2. **Un insight por post.** No intentar meter todo lo de la reunión.
3. **Si la transcripción es de una reunión de cliente**, no mencionar el nombre del cliente ni detalles confidenciales en el post. Preguntar si hay sensibilidad antes de redactar.
4. **Si no hay transcripción disponible**, pedir que la pegue. No inventar contenido.
5. **Mantener el registro de voz** — si el borrador suena genérico o corporativo, reescribir.
