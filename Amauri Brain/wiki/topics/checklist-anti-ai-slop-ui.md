---
title: Checklist anti "AI slop" para UI
type: topic
tags: [source-summary, diseño, producto, vibe-coding]
sources: 1
updated: 2026-10-06
---

# Checklist anti "AI slop" para UI

**Fuente:** https://vt.tiktok.com/ZSbhmnWTR/ (@jesseeisenbart) · `raw/2026-10-02-jesseeisenbart-hey-claude-my-app-looks-like-ai-slop-aitools-.md`
**Fecha:** 2026-10-06

Un prompt para Claude que lista las señales de que una app fue hecha con vibe coding y cómo quitarlas:

- **Color:** quitar gradientes morados y texto con gradiente. Un solo color de acento.
- **Tipografía:** una fuente display y otra para el cuerpo. Una escala tipográfica real. Líneas de menos de 70 caracteres. No centrar todo.
- **Forma:** un solo radio de borde. Sin sombras en todo. Sin blobs ni círculos flotantes.
- **Contenido:** screenshots reales en vez de ilustraciones. Sin emojis decorativos.
- **Interacción:** sin animaciones al hacer scroll. Sin hover effects en todo.
- **Sistema:** usar iconos Phosphor y no Lucide, que es el default de todo lo generado. Separar con espacio en blanco, no con divisores. Diseñar los estados vacíos.

Por qué importa: la PyME que llega a una demo compara contra cien landings genéricas. Si el producto se ve "hecho por IA", pierde credibilidad antes de mostrar valor.

**Aplicación a [[1Klick]]:** sirve como checklist de QA para `ads-ai` (dashboard, inbox, pricing) y para las landings de 1KlickAds. Los puntos con más retorno para 1Klick son los estados vacíos (onboarding por QR, inbox sin chats) y usar screenshots reales en la landing.

**Ver también:** [[simplicity-como-distilacion]], [[landing-page-patterns-yc]]
