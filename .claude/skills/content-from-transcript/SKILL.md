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

## Posicionamiento: Founder técnico LATAM

Marca personal de Amauri. Todo lo que sale de aquí debe sonar a *CTO que construye SaaS desde Cancún*. No a marketer, no a coach, no a guru de productividad.

## Cadencia objetivo: 3 posts + 2-3 comentarios estratégicos al día

LinkedIn con <5k followers no se gana posteando más, se gana comentando en posts de creators grandes del nicho (reach farming). Tus posts llegan a 700; un buen comentario en un post de 100k followers te puede ver 10x más gente.

| Tipo | Frecuencia | Fuente |
|---|---|---|
| Producto / Builder | 1x/semana | Meeting Notes, decisiones técnicas de 1Klick |
| Comunidad | 1x/semana | Eventos, meetups, speakers, LATAM tech |
| Perspectiva | 1x/semana | Brain (`wiki/concepts/`) |
| Comentario estratégico | 2-3x/día | Post de creator + Brain |

Si el usuario no especifica el tipo, preguntar cuál quiere generar esta vez para mantener balance semanal.

**Comentario estratégico:** input = post de un creator grande de IA / SaaS / founders LATAM. Output = comentario corto (20-40 palabras, NO mini-post) en la voz de Amauri.

Estructura validada:
```
[Reconocimiento humano corto — "Unos cracks", "Buen punto el primero", "Me encantó X"]. [Una observación tuya desde la trinchera, máximo 2 frases].
```

**No es:** mini-post estructurado, análisis técnico extendido, resumen del original, ni opinión-densa con cierre tipo slogan.
**Sí es:** comentario que parece escrito en 30 segundos por alguien que sabe del tema y tiene algo concreto que aportar.

Ejemplo validado (sobre post de Enzo Cavalie / Enter $30M ARR):
> Unos cracks, me encantó el primer punto. En LATAM, si tu onboarding depende del IT del cliente, no escalas.

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
- Empezar con algo que pasó o una afirmación contraintuitiva — no con una lección.
- Comunidad sobre promoción. Humano sobre corporativo.
- **Español mexicano.** No colombiano ni genérico. Ejemplos: "pluma" no "esfero", "refri" no "nevera".
- Emojis funcionales (1-2 máximo, no decorativos).
- Hashtags al final, 4-5 relevantes.
- Sin em dashes (—) en exceso.
- No mencionar la fuente del insight si Amauri no quiere parecer que está repitiendo una idea ajena — en ese caso presentarlo como reflexión propia.
- Evitar frases agresivas o que descalifiquen directamente al lector.
- El cierre debe hablar a todos, no asumir que el lector tiene un problema específico. Preferir "La pregunta esencial es..." sobre "Si tus X están bajos..."

---

## Paso 3 — Filtro de marca personal (Founder técnico LATAM)

Antes de extraer cualquier insight, validar que pasa **al menos uno** de estos filtros:

- ¿Es una decisión técnica o de producto que Amauri tomó en 1Klick?
- ¿Es un trade-off real que vivió construyendo SaaS desde LATAM?
- ¿Es algo que aprendió ship-eando rápido con IA que un founder no técnico no sabría?

Si el insight no pasa ninguno → **no es para su marca**. Decírselo claro y proponer guardarlo en el Brain o descartarlo. No redactar igual.

**Insights que NO escribimos** (aunque sean buenos):
- Tips genéricos de productividad o "cómo usar ChatGPT"
- Reflexiones de liderazgo / mindset sin sustancia técnica
- Growth hacks de LinkedIn, ventas o marketing como tema central
- Contenido motivacional o de hustle culture
- Resúmenes de libros sin opinión propia anclada en construir 1Klick

### Regla anti-promo (crítica para marca personal)

**Nunca** nombrar 1Klick, Digital Compass ni ningún producto propio en posts ni comentarios. La experiencia construyendo aparece como contexto, no como sujeto.

- ✅ "Construyendo SaaS B2B en LATAM…"
- ✅ "Como CTO de un SaaS de WhatsApp…"
- ✅ "Diseñando onboarding para PyMEs…"
- ❌ "En 1Klick lo estamos viviendo…"
- ❌ "Nuestro producto resuelve esto con…"
- ❌ Cualquier link o CTA al producto

Marca personal ≠ promo del producto. El take es el sujeto; tu trinchera es la evidencia.

---

## Paso 4 — Extraer el insight

Identificar el momento más valioso:
- ¿Qué fue sorprendente, inesperado o contraintuitivo?
- ¿Qué aprendiste que no sabías antes?
- ¿Qué decisión tomaron que vale la pena compartir?

Si hay varios candidatos, presentar los 2 mejores: *"¿Cuál resuena más contigo?"*

---

## Paso 5 — Redactar el borrador

Estructura validada (mezcla de apertura personal + estructura contraintuitiva):

```
[Afirmación contraintuitiva O "Me enseñaron mal." — concreto, corto]

[Reconocer que suena a excusa, pero defenderlo]

[Las voces que lo niegan — citas de lo que dicen los demás]

[El giro: la afirmación real]

[Ejemplo concreto que lo prueba — ejercicio, caso, situación]

[Conclusión de una línea: el principio destilado]

[Cierre universal — "La pregunta esencial es..." no "Si te pasa X..."]

[Hashtags]
```

**No usar:**
- "Es un honor compartir..."
- Jerga corporativa o anglicismos innecesarios
- Más de 160 palabras en el cuerpo
- Frases que descalifican directamente ("Eso no es talento, es terquedad")
- Cierres que asumen que el lector tiene un problema ("Si tus cierres están bajos...")

---

## Paso 6 — Presentar y refinar

```
---
BORRADOR — revisa antes de publicar

[post]

---
¿Cambios? Dime qué ajustar o di "listo" para terminar.
```

Sin límite de rondas — Amauri edita hasta que queda exacto. Si en alguna ronda manda una frase o párrafo reescrito, incorporarlo exactamente como lo escribió y ajustar el resto para que fluya.

---

## Paso 7 — Imagen (opcional)

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

## Paso 8 — Dar el texto final y registrar

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
6. **Nunca nombrar productos propios** (ver Regla anti-promo en Paso 3).

---

## Protocolo anti-bloqueo

A veces Amauri tiene pena de publicar (especialmente comentarios). Síntomas: pide más rondas de edición de las necesarias, dice "me da pena", procrastina con "después lo posteo".

Cuando lo detectes, NO sigas editando. Recordar:

1. Ya habla frente a 600 personas en escenario. 30 palabras en LinkedIn es objetivamente menos riesgoso.
2. El comentario no tiene que ser brillante. Tiene que ser suyo.
3. Los primeros 20 comentarios se sienten raros. Del 21 en adelante es músculo.
4. Reframe: no está "posteando para que lo vean". Está dejando rastro de cómo piensa.

**Protocolo de 30 segundos:**
1. Copia el comentario tal como está
2. Pégalo en el post
3. Publica
4. Cierra LinkedIn — no revisar engagement el mismo día
5. Mañana repite

La regla: **el bloqueo se quita con volumen, no con perfección.**
