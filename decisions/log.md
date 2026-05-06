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

## 2026-05-06 — Skill para archivar reuniones de Granola → Notion Meeting Notes

**Decision:** construir un skill que reciba notas de Granola (pegadas en chat) y cree una fila en la tabla Meeting Notes de Notion.

**Why:** Granola gratis solo guarda reuniones 30 días. El skill evita perder contexto de clientes y decisiones sin pagar Granola Pro.

**Alternatives considered:** procesar manual (descartado — es repetitivo y olvidable); conectar Granola API (no disponible en plan free).

**Owner:** Amauri — agendar en próximo `/level-up`.

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

## 2026-05-05 — Brief diario de CTO (`/morning`)

**Decision:** Construir skill L2 (`/morning`) que agrega GitHub (commits 24h) + Notion (tareas abiertas) + Brain (index + wiki reciente) + prioridades Q2 y genera un brief de arranque de día estructurado en 5 secciones.

**Why:** Amauri pierde ~15-20 min cada mañana revisando fuentes por separado antes de saber en qué enfocarse. Con 26 días para el deadline de mayo, ese overhead es dinero. El brief unifica el contexto en < 3 min.

**Pre-requisito:** conectar GitHub via MCP antes de correr el skill por primera vez.

**Proceso:**
- Trigger: Amauri corre `/morning` en el chat cada mañana
- Data: GitHub commits últimas 24h (todos los repos privados) + tareas Notion + Brain/index.md + context/priorities.md
- Transformación: AI agrega señales, cruza contra Q2 goals, prioriza
- Decision point: ninguno — Amauri lee y decide
- Destino: chat (output inline)

**Output format:**
1. Contexto técnico — qué se movió en GitHub ayer
2. Foco del día — top 3 tareas de Notion priorizadas contra mayo/junio
3. Señal de riesgo — posibles blockers para MVP o 50 clientes
4. Insight del Brain — 1 conexión relevante entre ideas y trabajo del día
5. La pregunta del día — la más importante antes de las 12pm

**Autonomy level:** L2 — AI genera el brief, Amauri lee y decide.

**KPI:** Less cost. Métrica: tiempo de "laptop abierto → sé qué hacer" (baseline: ~20 min → target: < 3 min).

**Alternatives considered:** Brief solo con Notion (descartado — sin contexto técnico es incompleto para un CTO). Entrega por WhatsApp/email (descartado — más fricción que chat, Amauri ya tiene Claude abierto).

**Owner:** Amauri.

---

## 2026-05-05 — Scope mínimo del MVP de 1Klick (31 mayo)

**Decision:** El MVP es 1KlickAds con dos capacidades: (1) subir campañas a Meta con IA y (2) agentes de IA vendiendo por WhatsApp. Todo lo demás queda fuera del alcance del 31 de mayo.

**Why:** Con 26 días al deadline, el scope debe estar congelado para que el sprint no se extienda. Estas dos capacidades son el core diferenciador — sin ellas no hay producto; con ellas hay algo que un cliente real puede usar y pagar.

**Alternatives considered:** Incluir onboarding completo, analytics, Marketing Studio (descartado — nice-to-have, no core). Solo Meta Ads sin WhatsApp (descartado — los agentes de ventas son la segunda pieza crítica para demostrar valor).

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
