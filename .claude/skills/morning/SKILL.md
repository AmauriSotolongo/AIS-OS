---
name: morning
description: Brief diario de CTO. Agrega GitHub (commits 24h) + Notion (tareas abiertas) + Google Calendar (eventos de hoy) + Second Brain + prioridades Q2 y genera un resumen de arranque estructurado. Corre cada mañana antes de arrancar el trabajo.
trigger: "/morning", "dame mi brief", "qué tengo hoy", "arrancamos", "brief de hoy"
bike-method-phase: 1  # Phase 1 — Training wheels. Corre manualmente cada mañana.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

# morning — Brief Diario de CTO

Toma las señales del día anterior y las convierte en un plan de arranque claro. Un run = contexto unificado en < 3 minutos.

**Pre-requisito:** GitHub debe estar conectado via MCP. Sin GitHub, el brief corre en modo degradado (Notion + Brain solamente) y lo avisa.

## Repos de 1Klick en GitHub

El repo principal de 1KlickAds es `AmauriSotolongo/ads-ai`. Siempre arranca por este. Si el usuario menciona un repo nuevo o corrige uno, actualizar esta lista.

## Fuentes de datos

| Fuente | Qué leer | Cómo |
|---|---|---|
| GitHub | Commits últimas 24h en `ads-ai` (repo principal de 1Klick) | `list_commits` en `AmauriSotolongo/ads-ai`, perPage 20. Si el resultado excede tokens, parsear via Bash con `jq` o `python3` para extraer sha, fecha y mensaje. |
| Notion — activas | Tareas abiertas / en progreso | `notion-query-database-view` con la vista "Por estado": `https://www.notion.so/2e968a705e1580239743c64f06d1d853?v=2e968a705e1580508bee000c51542a71`. Leer el resultado completo — no usar búsqueda general porque trae tareas en "Listo" mezcladas con las activas. |
| Notion — cerradas | Tareas completadas con fecha de cierre | `notion-query-database-view` con la vista "Cerradas esta semana": `https://www.notion.so/2e968a705e1580239743c64f06d1d853?v=35768a705e1581b99a20000cfbca8978`. Filtrar en síntesis las que tienen `Fecha de cierre` en los últimos 7 días. |
| Google Calendar | Eventos de hoy | `list_events` con `calendarId: primary`, `timeMin` = inicio del día hoy (00:00 local), `timeMax` = fin del día (23:59 local), `maxResults: 10`. Extraer título, hora inicio y duración. |
| Second Brain | `Amauri Brain/index.md` | Read directo |
| Prioridades Q2 | `context/priorities.md` | Read directo |

## Relación con `/ingest`

`/ingest` alimenta el Brain. `/morning` lee el Brain. El orden correcto es:

```
/ingest  →  /morning
```

Si corres `/morning` con el inbox lleno, el "Insight del Brain" puede estar desactualizado. Para evitarlo, `/morning` hace una revisión rápida del inbox antes de generar el brief (ver Paso 0 abajo).

## Ejecución

### Paso −1 — Verificar conexiones (antes de todo)

Antes de recopilar datos, verificar que las tres fuentes externas estén autenticadas. Hacerlo en paralelo:

- **GitHub:** intentar `list_commits` en `AmauriSotolongo/ads-ai` con `perPage: 1`. Si responde → ✅. Si falla → ❌ GitHub.
- **Notion:** intentar cualquier herramienta real de Notion (distinta de `mcp__notion__authenticate`). Si solo aparece la herramienta de auth → ❌ Notion.
- **Google Calendar:** intentar `list_events`. Si responde con "requires authentication" o solo aparece la herramienta de auth → ❌ Calendar.

Si hay **una o más conexiones en ❌**, mostrar este bloque **antes** de continuar:

```
⚠️ Conexiones faltantes — el brief correrá en modo degradado:
- ❌ Notion → abre /mcp y selecciona "notion" para autenticar
- ❌ Google Calendar → abre /mcp y selecciona "claude.ai Google Calendar" para autenticar
- ❌ GitHub → verifica que el MCP de GitHub esté activo en /mcp

¿Continuar en modo degradado o primero autenticamos?
```

- Si dice **"continuar"** o **"modo degradado"** → seguir con Paso 0 marcando las fuentes faltantes como no disponibles.
- Si dice **"autenticar primero"** → iniciar el flujo OAuth de cada fuente faltante, luego reiniciar desde Paso −1.
- Si **todas las conexiones están OK** → continuar en silencio con Paso 0.

### Paso 0 — Revisar inbox de Notion (BLOQUEANTE — antes de Paso 1)

**Este paso es secuencial. No lanzar Paso 1 hasta que este paso termine.**

Hacer `notion-fetch` del inbox (ID: `32a68a70-5e15-8024-95b8-ecaccf6fbe67`) y revisar si el bloque `<content>` tiene texto o está vacío.

- Si hay items → **pausar aquí** y preguntar:
  > "Hay [N] items en tu inbox sin procesar. ¿Corremos `/ingest` primero para que el Brain esté fresco antes del brief?"
  - Si dice **sí** → correr `/ingest` completo, luego continuar con Paso 1.
  - Si dice **no** o **"ya después"** → continuar con Paso 1 sin preguntar más.
- Si el inbox está vacío (`<content>` sin texto) → continuar con Paso 1 en silencio.

### Paso 1 — Recopilar (todo en paralelo)

Lanzar todas las lecturas al mismo tiempo:
- `list_commits` en `ads-ai`
- Búsqueda Notion de tareas activas (vista "Por estado")
- Búsqueda Notion de tareas cerradas (vista "Cerradas esta semana")
- `list_events` en Google Calendar (eventos de hoy)
- Read `Amauri Brain/index.md`
- Read `context/priorities.md`

Si el resultado de GitHub excede el límite de tokens, el archivo se guarda en disco. Leerlo con Bash:
```bash
cat <ruta> | python3 -c "
import sys, json
data = json.load(sys.stdin)
text = data[0]['text'] if isinstance(data, list) else data
commits = json.loads(text)
for c in commits:
    print(c['sha'][:7], c['commit']['author']['date'][:10], c['commit']['message'][:100])
"
```

Si GitHub MCP no responde, anotar "Sin actividad GitHub" y continuar.

### Paso 2 — Calcular fechas antes de escribir

Antes de generar el brief, derivar las fechas correctas desde `currentDate` del sistema:

1. **Hoy** = fecha exacta del sistema (ej. 2026-05-05)
2. **Día de la semana** = calcularlo desde la fecha, nunca adivinarlo (2026-05-05 → martes)
3. **Ayer** = hoy − 1 día (2026-05-04 → lunes). Usar este nombre al referirse a los commits.

Nunca escribir un día de la semana sin haberlo derivado de la fecha real.

### Paso 3 — Sintetizar

Con toda la data, generar el brief siguiendo exactamente este formato:

---

# CTO Morning Brief
## {día de la semana calculado} {día} de {mes} de {año}

---

### Contexto técnico

¿Qué se movió **{ayer calculado}** en `ads-ai`? Agrupa commits por tema (UI polish, bugs, features). Una línea por grupo. Si no hay commits → "Sin actividad técnica ayer."

---

### Agenda de hoy

Eventos del calendario de hoy en orden cronológico. Formato: `HH:MM — Título (Xh)`. Si no hay eventos → "Día libre de reuniones."
Al final, una línea con el tiempo disponible estimado para trabajo profundo: bloques de 90min+ sin reuniones.

---

### Top 3 Outcomes de hoy

Tres resultados concretos que deben estar hechos al final del día, priorizados contra los deadlines de mayo/junio **y contra el tiempo real disponible en el calendario**. Para cada uno: qué es, por qué hoy y qué desbloquea. Si uno bloquea a otro, marcarlo. Formato: **negrita el outcome**, luego una línea de contexto.

---

### Progreso esta semana

Tareas cerradas en los últimos 7 días (con `Fecha de cierre` registrada). Formato: lista con nombre y fecha. Al final: total en una línea — "N tareas cerradas esta semana."

**Coherencia código ↔ tareas:** Al pie de la sección, agregar una línea que cruce commits de ayer con cierres de la semana:
- Si hay commits ayer pero 0 tareas cerradas esta semana → "⚠️ X commits ayer, 0 tareas cerradas esta semana — el tracking está atrás del trabajo real."
- Si hay commits y también cierres → "✓ X commits ayer, N tareas cerradas esta semana — tracking al día."
- Si no hay commits ni cierres → omitir la línea de coherencia.

Si no hay ninguna tarea con fecha de cierre → "Sin cierres registrados esta semana." + línea de coherencia si aplica.

---

### Señal de riesgo

Una sola cosa concreta que podría bloquear el MVP (31 mayo) o los 50 clientes (30 junio). Incluir días restantes a cada deadline para dar urgencia real. Si no hay blocker → "Sin blocker visible — mantener ritmo."

---

### Insight del Brain

Una conexión entre algo del Brain y el trabajo del día. Formato: [[nombre-del-concepto]] + cómo aplica específicamente hoy. Una idea concreta, no genérica.

---

### La pregunta del día

La pregunta más importante que Amauri debe responder antes de las 12pm. Una sola. Sin adornos.

---

### Paso 4 — Entregar

Directo al contenido. Sin preámbulo, sin "aquí está tu brief", sin resumen al final.

## Modo degradado

Si GitHub no está conectado:
- Omitir "Contexto técnico" o poner "Sin actividad GitHub confirmada."
- Todo lo demás igual. No avisar al inicio — es ruido.

Si Google Calendar no responde:
- Omitir "Agenda de hoy" o poner "Sin acceso al calendario."
- Los Top 3 Outcomes se priorizan sin considerar tiempo disponible.

## Notas de implementación

- No inventar información. Si una fuente no responde o está vacía, decirlo en una línea.
- El brief debe caber en una pantalla. Si algo no cabe, es demasiado largo.
- Para Notion: priorizar resultados con "1Klick" en el título sobre tareas generales.
- Si Amauri corrige un dato en el chat (repo, tarea, fecha), incorporarlo al brief actualizado sin pedir confirmación.
