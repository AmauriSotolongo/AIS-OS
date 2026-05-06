---
name: check
description: Chequeo rápido de progreso. Jala las tareas En Progreso de Notion, pregunta cuáles terminaste, las cierra, y te da la siguiente según prioridad Q2. Corre cuando sientas que necesitas reorientarte.
trigger: "/check", "qué sigue", "cómo voy", "dame mi siguiente tarea", "check"
bike-method-phase: 1
---

# check — ¿Cómo voy? ¿Qué sigue?

Reorienta el trabajo en segundos. Sin resumen largo — solo estado + siguiente acción.

## Ejecución

### Paso 1 — Leer el foco del día

Read `context/today.md`. Si existe, extraer los 3 outcomes del día — se usan en el Paso 4 para priorizar la siguiente tarea.

Si el archivo no existe o la fecha no es hoy → ignorarlo y priorizar solo por criterios Q2.

### Paso 2 — Jalar tareas En Progreso

Correr `notion-query-database-view` con la vista "Por estado":
`https://www.notion.so/2e968a705e1580239743c64f06d1d853?v=2e968a705e1580508bee000c51542a71`

Filtrar solo las tareas con `Estado = "En progreso"`. Si hay tareas `Sin empezar` también jalarlas — se necesitan para sugerir la siguiente.

### Paso 3 — Preguntar el estado

Mostrar las tareas En Progreso en lista numerada y preguntar directamente:

```
**En progreso ahora:**

1. [Nombre de tarea]
2. [Nombre de tarea]
3. [Nombre de tarea]

¿Cuáles terminaste? (números, "ninguna", o "todas")
```

Esperar respuesta antes de hacer cualquier cambio.

### Paso 4 — Cerrar las completadas

Para cada tarea confirmada como terminada:
- `notion-update-page` → `Estado: "Listo"` + `date:Fecha de cierre:start` → fecha de hoy (ISO-8601)

Hacer todas las actualizaciones en paralelo.

### Paso 5 — Sugerir la siguiente tarea

Con las tareas que quedaron abiertas + las `Sin empezar`, elegir la siguiente según este criterio:
1. **Outcome del día** — si alguna tarea abierta corresponde a uno de los Top 3 de `context/today.md`, tiene prioridad automática
2. Bloqueador activo del MVP de 1Klick (deadline 31 mayo)
3. Tarea que desbloquee a alguien más
4. Tarea con más impacto en MRR (objetivo: 50 clientes antes del 30 junio)
5. La más pequeña completable en el bloque actual

Mostrar solo una:

```
Cerradas: [nombres]. ✓

**Siguiente:** [Nombre de tarea]
[Una línea de por qué — ej: "bloquea el onboarding por QR"]
```

Sin opciones múltiples. Sin lista. Una tarea, una razón.

### Paso 6 — Confirmar arranque (opcional)

Si Amauri responde con algo como "vale", "hagámoslo", "vamos", "dale", "sí" o cualquier confirmación de que quiere empezar la tarea sugerida:
- `notion-update-page` → `Estado: "En progreso"` en la tarea sugerida
- Confirmar con una línea: `[Nombre de tarea] → En progreso. ✓`
- Luego continuar con lo que Amauri quiera hacer (ejecutar la tarea, buscar código, etc.)

## Notas

- Si no hay nada En Progreso → ir directo al Paso 4 y sugerir la primera Sin Empezar.
- Si Amauri dice "ninguna" → saltarse el Paso 3 e ir directo a sugerir la siguiente.
- Si dice "todas" → cerrar todo sin pedir confirmación individual.
- No cruzar commits, no tocar el Brain, no generar contenido. Solo tareas.
- La sugerencia debe ser una sola tarea. No dar opciones — eso es trasladar la decisión de vuelta a Amauri.
