---
name: propuesta-dc
description: Genera una propuesta de proyecto Digital Compass en formato PPTX a partir de 4 datos de intake.
trigger: /propuesta-dc
bike-method-phase: 1  # Phase 1 — Training wheels. Corre manualmente, revisa cada output antes de enviar.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

## Qué hace este skill

Toma 4 datos de intake y genera un archivo PPTX completo de propuesta para Digital Compass — estructura consistente, en español, lista para revisar y exportar como PDF.

**Tiempo objetivo:** 10 min total (vs 30 min baseline manual).

---

## Intake — 4 preguntas

Si el usuario no los proporciona al invocar el skill, preguntar uno por uno:

1. **Nombre del cliente** (empresa o persona)
2. **Tipo de proyecto** (ej: desarrollo web a la medida, automatización con IA, app móvil, integración de sistemas...)
3. **Features principales** (lista de 3-6 funcionalidades clave)
4. **Presupuesto estimado** (rango o número, en MXN o USD)

Si el usuario ya pegó una transcripción de Granola o un brief, extraer los 4 datos de ahí y confirmar antes de proceder.

---

## Ejecución

### Paso 1 — Genera el contenido de cada slide

Con los 4 datos de intake, genera el contenido para los 8 slides siguientes. Usa español latino natural, directo. Sin relleno corporativo.

**Slide 1 — Portada**
- Título: nombre del proyecto o "Propuesta de Proyecto"
- Subtítulo: nombre del cliente
- Fecha: fecha actual
- Logo placeholder: "Digital Compass"

**Slide 2 — Entendemos tu reto**
- Párrafo corto (2-3 líneas) sobre el problema o necesidad del cliente
- Inferir del tipo de proyecto y contexto dado

**Slide 3 — Lo que proponemos**
- Solución en 3-4 bullets concisos
- Enfocado en resultado, no en tecnología

**Slide 4 — Alcance del proyecto**
- Lista de features exactamente como las dio el usuario
- Añadir 1-2 features de soporte/calidad si aplica (ej: pruebas, documentación)

**Slide 5 — Tecnología y enfoque**
- Stack sugerido según tipo de proyecto (no inventar si no hay info — usar "a definir con el equipo")
- Metodología de trabajo: iterativa, entregas por sprint

**Slide 6 — Timeline**
- Fases del proyecto con duración estimada (semanas)
- Inferir del scope — si es complejo, 12-16 semanas; si es simple, 6-8 semanas
- Marcar claramente como "estimado sujeto a revisión"

**Slide 7 — Inversión**
- Usar el presupuesto dado por el usuario
- Presentar como: Inversión total + modalidad de pago sugerida (50% inicio / 50% entrega, o por fases)
- Si el usuario dio un rango, usar el punto medio como referencia

**Slide 8 — Próximos pasos**
- 3 bullets de acción: (1) Agendar kick-off, (2) Firmar acuerdo, (3) Inicio de desarrollo
- CTA: contacto de Digital Compass

---

### Paso 2 — Ejecuta el script

Con el contenido generado, llama al script pasando los datos como JSON:

```bash
python3 scripts/generate_proposal.py \
  --cliente "NOMBRE_CLIENTE" \
  --proyecto "TIPO_PROYECTO" \
  --output "output/proposals/proposal-CLIENTE-FECHA.pptx" \
  --data '{"slide_content": {...}}'
```

El script genera el PPTX y confirma la ruta del archivo.

---

### Paso 3 — Entrega al usuario

Confirmar:
- Ruta del archivo generado
- Qué revisar antes de enviar: pricing (Slide 7), timeline (Slide 6), alcance (Slide 4)
- Recordar: este es un borrador L2 — tú tienes la última palabra en los números

---

## Bike Method — Phase 1

Este skill está en Phase 1 (training wheels):
- Corre manualmente cada vez
- Revisa el PPTX completo antes de enviarlo al cliente
- Anota qué cambias con frecuencia → esos patrones van a mejorar el skill en la siguiente iteración

Avanza a Phase 2 (supervisado) cuando hayas generado 5+ propuestas y el output requiera cambios mínimos.
