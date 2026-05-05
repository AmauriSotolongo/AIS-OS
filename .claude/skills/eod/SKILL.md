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
- `list_commits` en `AmauriSotolongo/ads-ai`, `perPage: 20` — rama `main`
- `list_commits` en `AmauriSotolongo/ads-ai`, `perPage: 10`, `sha: develop` — rama `develop`
- `notion-query-database-view` con la vista "Por estado": `https://www.notion.so/2e968a705e1580239743c64f06d1d853?v=2e968a705e1580508bee000c51542a71`

Si el resultado de GitHub excede tokens, parsear con Bash:
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

Filtrar commits de hoy (fecha = `currentDate`) en **ambas ramas**. Consolidar sin duplicados (mismo SHA). Si no hay commits hoy en ninguna rama → mostrar los de ayer como referencia.

### Paso 2 — Cruzar commits con tareas

Con los commits del día y las tareas en "En progreso" o "Sin empezar", hacer el cruce:

- Para cada tarea activa, buscar señales en los mensajes de commit que sugieran que fue completada (mismas palabras clave, mismo área del producto, fix relacionado).
- Si hay match claro → proponer cerrarla.
- Si es ambiguo → incluirla en la lista con un `?` para que Amauri decida.
- Si una tarea no tiene ningún commit relacionado → no sugerirla.

### Paso 3 — Presentar el cierre

Mostrar este resumen antes de hacer cualquier cambio en Notion:

```
## Cierre del día — {fecha}

**Commits de hoy:** X commits en ads-ai (main: N, develop: N)
Temas: [resumen de 1 línea por área — ej: "UI polish (modal, nav), fix contraste TopUpModal"]

---

**Tareas a cerrar:**

✅ [Nombre de tarea] — match con commits: "[fragmento del commit]"
✅ [Nombre de tarea] — match con commits: "[fragmento del commit]"
❓ [Nombre de tarea] — posible match, confirmar

**Sin match en commits:** [lista de tareas abiertas sin actividad relacionada hoy]

---

¿Cierro las ✅? ¿Y las ❓?
```

Esperar respuesta antes de escribir a Notion.

### Paso 4 — Cerrar tareas confirmadas

Para cada tarea confirmada por Amauri:
- Usar `notion-update-page` con `update_properties`
- Actualizar `Estado` → `"Listo"`
- Actualizar `date:Fecha de cierre:start` → fecha de hoy (ISO-8601: `YYYY-MM-DD`)

Hacer todas las actualizaciones en paralelo.

### Paso 5 — Confirmar

Mostrar solo:
```
Cerradas: [lista de nombres]. Tracking al día.
```

Sin resumen largo. Sin ceremonia.

## Notas de implementación

- Si Amauri dice "cierra todas" → cerrar todas las ✅ y ❓ sin pedir más confirmación.
- Si dice "solo las primeras dos" o similar → cerrar solo las mencionadas.
- Si no hay commits hoy → decir "Sin commits hoy. ¿Cerramos algo manualmente?" y mostrar lista de tareas en progreso.
- No crear tareas nuevas, no tocar el Brain, no generar contenido. Solo cerrar.
- Commits en `develop` cuentan igual que en `main` — trabajo hecho es trabajo hecho. No bloquear el cierre por rama.
- Si el trabajo está en `develop` y Amauri lo confirma → cerrar la tarea sin pedir merge primero.
