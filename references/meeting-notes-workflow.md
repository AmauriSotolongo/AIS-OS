# Meeting Notes Workflow

## Fuente
Granola (free tier) o Google Meet — transcripción manual, sin integración directa.

## Database en Notion
URL: https://www.notion.so/9dccf247e287492cae9d6dd85784833f
Ubicación: Inbox → Meeting Notes
Data source ID: collection://ef38dcec-32cd-45ff-bf59-474f70c756bb

## Cómo usarlo
1. Termina tu call
2. Copia la transcripción de Granola (o Meet)
3. Pégala en el chat con: "procesa esta transcripción"
4. El AIOS crea la nota en Notion con:
   - Resumen ejecutivo (3 líneas)
   - Decisiones tomadas
   - Action items (qué, quién, cuándo)
   - Contexto relevante para 1Klick/Digital Compass
   - Transcripción raw archivada en la nota

## Schema
- Reunión: título de la call
- Fecha: fecha de la reunión
- Participantes: nombres separados por coma
- Tipo: Cliente / Equipo / Proveedor / Investor / Otro
- Proyecto: 1Klick / Digital Compass / General
- Resumen: 3 líneas ejecutivas
- Decisiones: lo que se acordó
- Action Items: qué, quién, para cuándo
- Transcripción: texto raw
