---
name: propuesta-dc
description: Genera una propuesta de proyecto Digital Compass en formato PDF a partir de 5 datos de intake.
trigger: /propuesta-dc
bike-method-phase: 1  # Phase 1 — Training wheels. Corre manualmente, revisa cada output antes de enviar.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

## Qué hace este skill

Toma 5 datos de intake y genera un PDF de propuesta para Digital Compass — estructura consistente, en español, comercial (no técnico), lista para enviar al cliente. Internamente arma un PPTX y lo convierte a PDF con LibreOffice headless; el PPTX intermedio se borra.

**Tiempo objetivo:** 10 min total (vs 30 min baseline manual).

---

## Intake — 5 preguntas

Si el usuario no los proporciona al invocar el skill, preguntar uno por uno:

1. **Nombre del cliente** (empresa o persona — exactamente como debe aparecer)
2. **Tipo de proyecto** (ej: app de fidelización, automatización con IA, sitio web a la medida, integración de sistemas…)
3. **Features principales** (lista de 3-6 funcionalidades clave)
4. **Presupuesto estimado** (rango o número, en MXN o USD)
5. **Mantenimiento mensual recurrente** (opcional — monto y a partir de qué mes; ej: $2,000 MXN/mes desde el tercer mes). Si no aplica, dejarlo fuera.

Si el usuario ya pegó una transcripción de Granola o un brief, extraer los datos de ahí y confirmar antes de proceder.

**Antes de ejecutar el script:** confirmar el nombre exacto del cliente en el chat ("¿Grupo Santos o Grupo Santes?"). Un error en el nombre llega al PDF, al archivo y a Notion — cuesta más corregirlo que preguntar.

---

## Principio rector: comercial, no técnico

Amauri vende beneficios de negocio, no stack ni features. Toda la propuesta — desde la portada hasta el alcance — se escribe pensando en **qué gana el dueño del negocio**, no en cómo se construye.

- Habla en dinero, recurrencia, marca, margen, clientes nuevos. No en APIs, frameworks, ni "arquitectura serverless".
- Las features se describen por su valor para el cliente: "Tarjeta digital que vive en el teléfono, sin app" — no "Apple Wallet (PassKit) integration".
- El Slide 5 (originalmente "Tecnología y enfoque") suele renombrarse a algo como "Cómo lo vive tu cliente" — el journey del usuario final en pasos numerados. Usa el campo `tecnologia.titulo` para sobreescribir el título.

---

## Ejecución

### Paso 1 — Genera el contenido de cada slide

Con los datos de intake, genera el contenido para los 8 slides siguientes. Español latino natural, directo, sin relleno corporativo. Markup soportado: `**palabras clave**` en *bold + italic + color platino* para destacar.

**Slide 1 — Portada**
- Título: una frase de valor comercial (ej: "Más clientes, más recurrencia, mejor margen"), no el nombre técnico del proyecto.
- Cliente, fecha y "DIGITAL COMPASS" los pone el script.

**Slide 2 — Entendemos tu reto**
- Párrafo corto (3-5 líneas) que enumera los **dolores del negocio** del cliente.
- Tocar cada problema central que la propuesta resuelve — no quedarse solo en uno aunque sea el más vistoso.
- Para apps de fidelización/retail: típicamente tres dolores (retención, reputación/Google, comisiones).
- **Reviews de Google**: enmarcarlas en su valor dual — buenas reviews atraen clientes nuevos (visibilidad en Maps, ranking local, confianza), malas reviews golpean la marca en público. No reducirlo solo al filtro defensivo.

**Slide 3 — Lo que proponemos**
- 4-5 bullets de **beneficios**, no de features.
- Cada bullet termina en un resultado tangible (recurrencia, margen, visibilidad, ahorro, conocimiento del cliente).

**Slide 4 — Alcance del proyecto**
- Features exactamente como las dio el usuario, pero **traducidas a lenguaje cliente**: en vez de "Apple Wallet API", "Tarjeta digital que vive en el teléfono, sin app".
- Añadir "Implementación y arranque" o equivalente al final.

**Slide 5 — Cómo lo vive tu cliente** (`tecnologia.titulo`)
- Renombrar el slide vía `tecnologia.titulo` cuando el proyecto sea customer-facing.
- 5 pasos numerados del journey del usuario final. Ej: "**1.** Escanea un QR en la mesa…"
- Solo conservar el título "Tecnología y enfoque" cuando el cliente es técnico y específicamente pide stack.

**Slide 6 — Timeline**
- Fases por semanas. Inferir del scope: simple 6 semanas, intermedio 8-10, complejo 12-16.
- Marcar como "estimado sujeto a revisión" (el script ya pone el asterisco).

**Slide 7 — Inversión**
- `inversion.total`: monto destacado (ej: "$80,000 MXN").
- `inversion.modalidad`: una sola línea que combina:
  - Modalidad de pago (50%/50% o por fases)
  - Mantenimiento mensual si aplica (ej: " · Mantenimiento: $2,000 MXN/mes desde el tercer mes")
- Si el cliente dio un rango, usar el punto medio como referencia.

**Slide 8 — Próximos pasos**
- 3 bullets: (1) Agendar kick-off, (2) Firmar acuerdo y primer pago, (3) Inicio de desarrollo / primer demo.
- Contacto: `digitalcompass.ia@gmail.com  |  +52 (998) 145 2628`.

---

### Paso 2 — Ejecuta el script

```bash
python3 scripts/generate_proposal.py \
  --cliente "NOMBRE_CLIENTE" \
  --proyecto "TIPO_PROYECTO" \
  --output "/Users/amaurisotolongo/Desktop/Propuestas/proposal-CLIENTE-YYYY-MM-DD.pdf" \
  --data '{"slide_content": {...}}'
```

El script genera un PPTX intermedio, lo convierte a PDF vía LibreOffice headless, y borra el PPTX. Output final: solo el PDF. Pasa `--keep-pptx` si por alguna razón quieres conservar el PPTX.

**Estructura completa del JSON:**

```json
{
  "slide_content": {
    "portada": { "titulo": "..." },
    "reto":    { "texto": "..." },
    "propuesta": { "bullets": ["...", "..."] },
    "alcance":   { "features": ["...", "..."] },
    "tecnologia": {
      "titulo": "Cómo lo vive tu cliente",
      "bullets": ["**1.** ...", "**2.** ..."]
    },
    "timeline":  { "fases": ["Semana 1 · ...", "..."] },
    "inversion": {
      "total": "$80,000 MXN",
      "modalidad": "50% inicio · 50% go-live  ·  Mantenimiento: $2,000 MXN/mes desde el tercer mes"
    },
    "proximos_pasos": {
      "bullets": ["...", "...", "..."],
      "contacto": "digitalcompass.ia@gmail.com  |  +52 (998) 145 2628"
    }
  }
}
```

---

### Paso 3 — Entrega al usuario

Confirmar:
- Ruta del PDF generado como link clickeable (`file:///...`).
- Qué revisar antes de enviar: pricing + mantenimiento (Slide 7), timeline (Slide 6), alcance (Slide 4).
- Recordar: este es un borrador — el usuario tiene la última palabra en los números.

---

## Lecciones acumuladas (revisar antes de cada run)

Patrones observados en runs anteriores:

- **Tono:** la primera versión casi siempre sale demasiado técnica. Por defecto inclinarse a lo comercial desde el primer intento.
- **Texto:** Amauri prefiere conciso. Bullets cortos, párrafos de 3-5 líneas máx. Si el primer draft se siente largo, ya está largo.
- **Reviews de Google:** narrativa dual (positivo + protección). No vender solo el filtro.
- **Mantenimiento mensual:** preguntarlo en intake. Va junto a la modalidad de pago en Slide 7.
- **Slide 5:** renombrar a "Cómo lo vive tu cliente" para apps customer-facing. Solo dejar "Tecnología y enfoque" si el cliente final es técnico.
- **Revertir cambios:** si el usuario pide "déjalo como estaba", restaurar el texto literal del intento anterior — no re-sintetizar.

---

## Bike Method — Phase 1

Este skill está en Phase 1 (training wheels):
- Corre manualmente cada vez.
- Revisa el PDF completo antes de enviarlo al cliente.
- Anota qué cambias con frecuencia → esos patrones suben a "Lecciones acumuladas" arriba.

Avanza a Phase 2 (supervisado) cuando hayas generado 5+ propuestas y el output requiera cambios mínimos.
