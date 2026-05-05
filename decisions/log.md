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
