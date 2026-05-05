# Notion MCP Reference

## Connection
- Transport: HTTP (OAuth)
- Endpoint: https://mcp.notion.com/mcp
- Auth: OAuth — completado via `/mcp` en Claude Code
- Scope: user (disponible en todos los proyectos)

## Tools disponibles
- `notion-search` — búsqueda semántica en todo el workspace
- `notion-fetch` — contenido completo de una página o database
- `notion-query-database-view` — query a databases con filtros
- `notion-create-pages` — crear páginas
- `notion-update-page` — actualizar propiedades de una página
- `notion-create-database` — crear databases
- `notion-get-users` — listar usuarios del workspace
- `notion-query-meeting-notes` — buscar notas de reuniones

## Uso típico
Buscar tareas: `notion-search` con query + `query_type: internal`
Ver contenido: `notion-fetch` con el ID de la página
Query a DB: primero fetch para obtener el data_source_url, luego `notion-query-database-view`
