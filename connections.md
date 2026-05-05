# Connections

Registry of every system your AIOS can reach. Filled by `/onboard` from Q4-Q7 answers; expanded over time as you wire new tools. `/audit` checks this file for domain coverage and freshness.

| # | Domain | Tool | Mechanism | Auth | Last checked |
|---|---|---|---|---|---|
| 1 | Revenue / Financials | Stripe | mcp (API key) | key en .env | 2026-05-04 |
| 2 | Customer interactions | WhatsApp | not yet connected | — | — |
| 3 | Calendar | Google Calendar | mcp (OAuth) | autenticado | 2026-05-04 |
| 4 | Communication | Gmail | mcp (OAuth) | autenticado | 2026-05-04 |
| 5 | Project / task tracking | Notion | mcp (OAuth) | autenticado | 2026-05-04 |
| 6 | Meeting intelligence | Granola → Notion | manual (paste transcript) | n/a | 2026-05-04 |
| 7 | Knowledge / files | Google Drive + Notion | mcp (OAuth) | autenticado | 2026-05-04 |
| 8 | Source control | GitHub | mcp (PAT) | token en ~/.claude.json | 2026-05-05 |

**Mechanism options:** `mcp` (MCP server), `script` (Python/Bash hitting an API, in `scripts/`), `export` (CSV/JSON dump pipeline), `key+ref` (`.env` key + `references/{tool}-api.md` guide), `not yet connected`.

When you wire a new tool, also save `references/{tool}-api.md` capturing endpoints, auth flow, and common queries — researched-once-saved-forever.
