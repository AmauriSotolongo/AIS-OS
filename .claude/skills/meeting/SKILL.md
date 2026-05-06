---
name: meeting
trigger: "/meeting", "archiva esta reunión", "guarda esta reunión", "notas de granola"
bike-method-phase: 1  # Phase 1 — Training wheels. Run manually first.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

## What this skill does

Recibe notas de Granola (pegadas en chat), las parsea y crea una fila en la base de datos **Meeting Notes** de Notion. L2 — AI parsea, Amauri aprueba antes de escribir.

## Trigger

Amauri pega las notas de Granola en el chat y escribe `/meeting` (o cualquier trigger de arriba).

## Notion schema (conocido, no buscar cada vez)

La base de datos **Meeting Notes** tiene ID `9dccf247-e287-492c-ae9d-6dd85784833f` y data source `ef38dcec-32cd-45ff-bf59-474f70c756bb`.

Campos reales (usar estos nombres exactos al crear):

| Propiedad Notion | Tipo | Valores permitidos |
|---|---|---|
| `Reunión` | title | texto libre |
| `date:Fecha:start` | date | YYYY-MM-DD |
| `Tipo` | select | Cliente / Equipo / Proveedor / Investor / Otro |
| `Proyecto` | select | 1Klick / Digital Compass / General |
| `Participantes` | text | texto libre |
| `Resumen` | text | párrafo resumen |
| `Action Items` | text | bullets con responsable |
| `Decisiones` | text | bullets con decisiones tomadas |
| `Transcripción` | text | URL de Granola si existe |

## Execution

### Step 1 — Parse las notas

Lee el texto pegado y extrae:

| Campo | Descripción |
|---|---|
| **Reunión** | Nombre de la reunión o tema principal |
| **Fecha** | Fecha de la reunión (YYYY-MM-DD). Si no está explícita, usa la fecha actual. |
| **Participantes** | Lista de personas presentes con rol si se menciona |
| **Proyecto** | Infiere: Digital Compass, 1Klick, o General |
| **Tipo** | Cliente si hay empresa externa; Equipo si es interna |
| **Resumen** | 2-3 oraciones con el contexto y resultado de la reunión |
| **Action Items** | Acciones concretas con responsable |
| **Decisiones** | Acuerdos o decisiones tomadas |
| **Transcripción** | URL de Granola si está en el texto |

Si algún campo no está claro, infiere con contexto o deja en blanco — no preguntes por cada campo.

### Step 2 — Mostrar preview

Muestra el preview antes de crear nada:

```
📋 **Meeting Notes — Preview**

**Reunión:** [título]
**Fecha:** [fecha]
**Participantes:** [lista]
**Proyecto:** [proyecto]
**Tipo:** [tipo]

**Resumen:** [resumen]

**Action Items:**
- [acción 1 — responsable]
- [acción 2 — responsable]

**Decisiones:**
- [decisión 1]

¿Creo la fila en Notion? (sí / edita lo que necesites)
```

### Step 3 — Crear en Notion (solo si Amauri confirma)

Cuando Amauri diga "sí" o confirme, usar directamente el data source conocido — **no buscar la base de datos de nuevo**:

```
parent: { type: "data_source_id", data_source_id: "ef38dcec-32cd-45ff-bf59-474f70c756bb" }
```

Si el MCP de Notion no está disponible en la sesión, avisar: "El MCP de Notion no está activo. Copia esto manualmente:" y mostrar los campos listos para pegar.

### Step 4 — Confirmar

Después de crear la fila, responder con una línea:
`✓ Reunión "[título]" archivada en Notion.`

## Notes

- No modifiques las notas originales de Granola.
- Si Amauri pega múltiples reuniones a la vez, procésalas una por una — muestra preview de cada una antes de continuar con la siguiente.
- Si Amauri pide follow-up email u otra acción adicional junto con `/meeting`, preguntar si lo quiere después de confirmar Notion, no antes.
- El campo `Proyecto` se infiere del contexto: si menciona Digital Compass → "Digital Compass"; si menciona 1Klick → "1Klick"; si es ambiguo → "General".
