# Decisions Log

Append-only record of meaningful decisions and why they were made. `/level-up` Phase 2 (Method interview) writes scoped automation specs here. You can also append manually whenever you decide something worth remembering.

**Format per entry:**

```
## YYYY-MM-DD — Short title

**Decision:** what was decided.

**Why:** the reasoning, constraints, and what would change your mind.

**Alternatives considered:** what else was on the table.

**Owner:** who's accountable.
```

Keep it terse. Future-you will thank present-you for capturing the *why*, not just the *what*.

---

## 2026-05-05 — Generador de propuestas Digital Compass (PPTX)

**Decision:** Construir skill L2 (`/propuesta-dc`) que genera una propuesta de proyecto completa en formato PPTX para Digital Compass, a partir de 4 datos de intake: cliente, tipo de proyecto, features y presupuesto estimado.

**Why:** Amauri hace 3+ propuestas por semana (~30 min c/u = 1.5 h/semana). El tiempo no se va en Gamma sino en la fase previa: sin estructura fija, cada propuesta se reconstruye desde cero con resultados inconsistentes. Estandarizar el intake + generar el PPTX con plantilla fija elimina el blank page y la variabilidad.

**Proceso:**
- Trigger: Amauri invoca `/propuesta-dc` con los 4 datos (o los da en conversación)
- Data: nombre cliente, tipo de proyecto, features, presupuesto estimado
- Transformación: Claude genera contenido de slides → script python-pptx produce el archivo PPTX
- Decision point: Amauri revisa pricing, timeline y alcance antes de enviar
- Destino: archivo PPTX local (abre, revisa, exporta PDF)

**Autonomy level:** L2 — Drafted. AI genera el deck completo, Amauri revisa números y scope.

**KPI:** Tiempo por propuesta (baseline: 30 min → target: 10 min). Secundario: tasa de cierre.

**Alternatives considered:** Prompt para Gamma (descartado — no resuelve la inconsistencia estructural). Google Slides via MCP (formato limitado). PPTX elegido por control total de plantilla y diseño.

**Owner:** Amauri.

---

## 2026-05-04 — Generador de posts desde transcripciones

**Decision:** Construir skill L2 (AI-drafted, human-reviews) que convierte una transcripción de reunión o evento en borrador de post de LinkedIn en la voz de Amauri.

**Why:** El constraint no es tiempo de escritura sino blank page. Las transcripciones ya existen en Notion vía workflow de Granola. El insumo está — solo falta el paso de transformación. Más contenido publicado = más visibilidad en LATAM = más inbound para Digital Compass y 1Klick.

**Proceso:**
- Trigger: transcripción disponible (Notion o paste directo)
- Data: transcripción + references/voice.md
- Transformación: extraer insight más valioso → estructura de post → redactar en voz de Amauri
- Decision point: Amauri elige el insight y aprueba el borrador antes de publicar
- Destino: borrador listo para LinkedIn

**Autonomy level:** L2 — Drafted. AI genera, Amauri revisa y publica.

**KPI:** Más clientes vía visibilidad. Métrica: 3-4 posts publicados/mes (baseline actual: ~1-2).

**Alternatives considered:** Automatizar contenido desde inspiración ad-hoc (descartado — trigger difuso). Generador de propuestas (alta prioridad también, próximo /level-up).

**Owner:** Amauri.

---
