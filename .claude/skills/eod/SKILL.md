---
name: eod
description: Cierre de día para CTO. Cruza commits del día con tareas en progreso, sugiere cuáles marcar como Listo, y las cierra con confirmación. Un run = tracking al día en < 5 minutos.
trigger: "/eod", "cierre del día", "qué hice hoy", "cerrar tareas", "fin del día"
bike-method-phase: 1
---

# eod — Cierre de Día

Cruza lo que se movió en código con lo que está abierto en Notion. Cierra el gap de tracking.

## Ejecución

### Paso 1 — Recopilar (en paralelo)

Lanzar al mismo tiempo:
- `list_commits` en `AmauriSotolongo/ads-ai` (repo de 1KlickAds), `perPage: 20` — rama `main`
- `list_commits` en `AmauriSotolongo/ads-ai` (repo de 1KlickAds), `perPage: 10`, `sha: develop` — rama `develop`
- `notion-query-database-view` con la vista "Por estado": `https://www.notion.so/2e968a705e1580239743c64f06d1d853?v=2e968a705e1580508bee000c51542a71`

**Importante:** `main` casi siempre excede el límite de tokens y se guarda en un archivo. Después de recibir los tres resultados, parsear **ambas ramas** con Bash sin excepción — incluso si el resultado inline parece legible. Esto garantiza que ambas ramas siempre se lean completas:

```bash
# Para cada rama que excedió tokens (ruta devuelta en el mensaje de error):
cat <ruta> | python3 -c "
import sys, json
data = json.load(sys.stdin)
text = data[0]['text'] if isinstance(data, list) else data
commits = json.loads(text)
for c in commits:
    print(c['sha'][:7], c['commit']['author']['date'][:10], c['commit']['message'][:100])
"
```

Nunca avanzar al Paso 2 sin haber confirmado los commits de **main** y **develop** por separado.

Filtrar commits de hoy (fecha = `currentDate`) en **ambas ramas**. Consolidar sin duplicados (mismo SHA). Si no hay commits hoy en ninguna rama → mostrar los de ayer como referencia.

### Paso 2 — Clasificar tareas y cruzar con commits

**Primero: clasificar cada tarea por tipo.**

- **Tarea de código** — bugs, features, refactors, integraciones técnicas. Estas sí deben tener un commit relacionado.
- **Tarea no-código** — cotizaciones, propuestas, reuniones, gestiones externas (ej. verificación Meta). Para estas no hay commits en GitHub; se cierran por contexto o confirmación de Amauri, no por match.

**Segundo: para las ya en "Listo" con `date:Fecha de cierre:start` = hoy:**
- Si es tarea de código → buscar el commit que la respalda y mostrarlo en el resumen.
- Si es tarea no-código → mostrarla en el resumen sin buscar commit (es esperado que no haya).

**Tercero: para tareas activas ("En progreso" o "Sin empezar"):**
- Tarea de código → cruzar con commits del día. Match claro → ✅. Ambiguo → ❓. Sin señal → omitir.
- Tarea no-código → no incluir en la sección de matches. Solo mencionar si Amauri trae contexto.

**Caso sin commits (día de Notion puro):** si no hay commits hoy, igual mostrar el resumen con las tareas ya cerradas en Notion y preguntar si hay más que cerrar manualmente.

### Paso 3 — Presentar el cierre

Mostrar este resumen antes de hacer cualquier cambio en Notion:

```
## Cierre del día — {fecha}

**Commits de hoy:** X commits en 1KlickAds (main: N, develop: N)  ← omitir línea si no hay commits
Temas: [resumen de 1 línea por área]  ← omitir si no hay commits

---

**Ya cerradas hoy en Notion:**
- [Nombre de tarea de código] — commit: "[fragmento del commit]"
- [Nombre de tarea no-código]

**Tareas a cerrar (con match en commits):**

✅ [Nombre de tarea] — match: "[fragmento del commit]"
❓ [Nombre de tarea] — posible match, confirmar

**Sin match:** [tareas de código abiertas sin actividad hoy]

---

¿Cierro las ✅? ¿Y las ❓?
```

Si no hay commits y no hay tareas que proponer → mostrar solo las ya cerradas y preguntar "¿Algo más que cerrar hoy?"

Esperar respuesta antes de escribir a Notion.

### Paso 4 — Cerrar tareas confirmadas

Para cada tarea confirmada por Amauri:
- Usar `notion-update-page` con `update_properties`
- Actualizar `Estado` → `"Listo"`
- Actualizar `date:Fecha de cierre:start` → fecha de hoy (ISO-8601: `YYYY-MM-DD`)

Hacer todas las actualizaciones en paralelo.

### Paso 5 — Correo al cofundador

Preguntar: "¿Mando el resumen a tu cofundador?"

Si Amauri confirma, crear un borrador con `create_draft` en Gmail:
- **Para:** digitalcompass.ia@gmail.com
- **Asunto:** Cierre del día — {fecha larga, ej. "6 de mayo 2026"}
- **Cuerpo:** resumen directo — commits del día (agrupados por tema, no listados por SHA), tareas cerradas y qué sigue en progreso. Tono natural, sin ceremonia.

Nota: solo se puede crear el borrador, no enviarlo directamente. Avisar a Amauri que está en Gmail listo para enviar, o si quiere verlo primero.

### Paso 6 — Confirmar

Mostrar solo:
```
Cerradas: [lista de nombres]. Tracking al día.
```

Sin resumen largo. Sin ceremonia.

## Notas de implementación

- Si Amauri dice "cierra todas" → cerrar todas las ✅ y ❓ sin pedir más confirmación.
- Si dice "solo las primeras dos" o similar → cerrar solo las mencionadas.
- Si no hay commits hoy → mostrar igual las tareas ya en Listo con fecha de hoy, y preguntar "¿Algo más que cerrar?"
- Siempre incluir en el resumen final las tareas ya cerradas hoy en Notion. Las de código van con su commit de respaldo. Las no-código van sin commit — es esperado, no es un gap.
- No buscar commits para tareas no-código (cotizaciones, propuestas, PDFs, reuniones, gestiones externas). No anotar "sin commit" — es obvio y genera ruido. Solo listar el nombre.
- Un commit que trabaja sobre componentes relacionados a una tarea ya matcheada (ej. refactor de un componente dentro del mismo flujo) cuenta como cubierto por esa tarea. No reportar como "commit sin tarea" salvo que sea trabajo genuinamente nuevo sin ninguna tarea en Notion.
- No crear tareas nuevas, no tocar el Brain, no generar contenido. Solo cerrar.
- Commits en `develop` cuentan igual que en `main` — trabajo hecho es trabajo hecho. No bloquear el cierre por rama.
- Si el trabajo está en `develop` y Amauri lo confirma → cerrar la tarea sin pedir merge primero.
