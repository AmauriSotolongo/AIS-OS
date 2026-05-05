---
title: LLM Wiki Pattern
type: topic
tags: [source-summary, knowledge-management, llm, second-brain]
sources: 1
updated: 2026-05-05
---

# LLM Wiki Pattern

**Fuente:** `raw/2026-05-05-llm-wiki-pattern.md`

## Idea central

La mayoría de los sistemas de RAG re-derivan conocimiento desde cero en cada consulta. El LLM Wiki es diferente: el LLM construye y mantiene un wiki persistente — archivos markdown estructurados e interconectados — que se ubica entre tú y las fuentes brutas. Con cada fuente nueva, el LLM integra el conocimiento en el wiki existente: actualiza páginas de entidades, revisa resúmenes, marca contradicciones.

El wiki es un artefacto que **acumula** valor. No empieza desde cero en cada pregunta.

## Las tres capas

| Capa                        | Quién la controla | Regla                             |
| --------------------------- | ----------------- | --------------------------------- |
| `raw/` — fuentes brutas     | Amauri            | Inmutable. El LLM solo lee.       |
| `wiki/` — páginas generadas | El LLM            | El LLM escribe y mantiene todo.   |
| `CLAUDE.md` — schema        | Co-evolucionan    | Las reglas de operación del wiki. |

## Las tres operaciones

**Ingest** — cuando llega una fuente nueva:
nueva fuente → leer → discutir takeaways → summary page → actualizar entity/concept pages → actualizar index → loggear

**Query** — cuando Amauri pregunta:
leer index → leer páginas relevantes → sintetizar con citas → ofrecer guardar como synthesis page

**Lint** — chequeo de salud periódico:
contradicciones, claims obsoletos, orphan pages, links faltantes, gaps a investigar

## Por qué funciona

La parte tediosa de un knowledge base no es leer ni pensar — es el bookkeeping: actualizar cross-references, marcar cuando nueva info contradice lo anterior, mantener consistencia entre decenas de páginas. Los humanos abandonan wikis porque el costo de mantenimiento crece más rápido que el valor. Los LLMs no se aburren. El wiki se mantiene porque el costo de mantenimiento es casi cero.

## Herramientas opcionales

- Obsidian — IDE para navegar el wiki (graph view, Dataview, Marp)
- Obsidian Web Clipper — convierte artículos web a markdown
- qmd — motor de búsqueda local para markdown (BM25/vector + LLM reranking), tiene CLI y servidor MCP
- Marp — slide decks en markdown

## Conexión con este wiki

Este documento describe el patrón exacto que implementamos aquí. El wiki que estás leyendo **es** la implementación de este patrón para [[Amauri Sotolongo]].

## Referencia histórica

Relacionado en espíritu con el Memex de Vannevar Bush (1945): base de conocimiento privada y curada activamente, donde las conexiones entre documentos son tan valiosas como los documentos. Lo que Bush no pudo resolver: quién hace el mantenimiento. El LLM lo resuelve.
