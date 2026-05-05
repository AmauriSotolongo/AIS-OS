# GitHub — Setup para AIOS

Conecta GitHub al AIOS para que `/morning` pueda leer commits, repos y actividad técnica reciente.

## Paso 1 — Crear un Personal Access Token (PAT)

1. Ve a **github.com → Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. Click **Generate new token (classic)**
3. Nombre: `AIOS-morning-brief`
4. Expiration: 90 días (o sin expiración si prefieres)
5. Scopes requeridos:
   - `repo` (acceso completo a repos privados)
   - `read:user`
6. Click **Generate token** — copia el token, solo se muestra una vez

## Paso 2 — Agregar el MCP de GitHub

En la terminal, corre:

```bash
claude mcp add github -s local -- docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=TU_TOKEN_AQUI \
  ghcr.io/github/github-mcp-server
```

O con npx si no tienes Docker:

```bash
claude mcp add github -s local -- npx -y @modelcontextprotocol/server-github
```

Luego agrega el token en `.claude/settings.local.json` bajo `mcpServers.github.env`.

## Paso 3 — Verificar

Abre una nueva sesión de Claude Code y pregunta: *"¿Cuántos repos privados tengo en GitHub?"* Si responde correctamente, está conectado.

## Paso 4 — Registrar en connections.md

Agrega esta fila a la tabla:

```
| 8 | Source control | GitHub | mcp (PAT) | token en settings.local.json | 2026-05-05 |
```

## Herramientas disponibles post-conexión

| Operación | Uso en /morning |
|---|---|
| Listar repos | Inventario de repos activos |
| Commits recientes | Actividad técnica últimas 24h |
| Issues abiertos | Posibles blockers técnicos |
| Pull requests | Trabajo en revisión |

Una vez conectado, `/morning` usa GitHub automáticamente sin configuración adicional.
