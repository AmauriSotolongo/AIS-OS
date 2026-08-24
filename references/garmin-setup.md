# Garmin Connect — Setup para AIOS

Conecta Garmin al AIOS para que `/morning` y `/eod` lean sueño, estrés, body battery y HRV. Señal de energía real, no autopercibida.

MCP: [taxuspt/garmin_mcp](https://github.com/taxuspt/garmin_mcp) — envuelve la librería `python-garminconnect`.

## Paso 1 — Autenticar una sola vez

El servidor no guarda usuario ni contraseña. Autenticas una vez en la terminal y quedan tokens OAuth en disco.

### Requisito: `uv`

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Se instala en `C:\Users\<usuario>\.local\bin`. **Cierra y reabre PowerShell** para que el PATH lo tome. Si no quieres reabrir, en la sesión actual:
```powershell
$env:Path = "C:\Users\$env:USERNAME\.local\bin;$env:Path"
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

También necesitas Git instalado ([git-scm.com](https://git-scm.com/downloads)) — el comando instala desde `git+https://`.

### Correr la auth

```
uvx --python 3.12 --from git+https://github.com/Taxuspt/garmin_mcp garmin-mcp-auth
```

Te pide email, contraseña y código MFA si lo tienes activo. La primera vez tarda un par de minutos (descarga Python 3.12 y 39 paquetes).

Tokens guardados en:
- Windows: `C:\Users\<usuario>\.garminconnect`
- macOS / Linux: `~/.garminconnect`

Verificar cuando quieras:
```
uvx --python 3.12 --from git+https://github.com/Taxuspt/garmin_mcp garmin-mcp-auth --verify
```

⚠️ Los tokens duran ~6 meses. Cuando expiren, corre el comando otra vez con `--force-reauth`. Si `/morning` empieza a fallar en la sección de energía, esto es lo primero que hay que revisar.

### Si falla

**`429 — IP rate limited by Garmin`** — Garmin bloqueó tu IP, no es tu contraseña. El CLI reporta "Invalid email or password" aunque el error real sea 429; ignora ese mensaje y mira las líneas de arriba. Espera 15-30 min sin reintentar (cada intento extiende el bloqueo), apaga la VPN si la tienes, o conéctate al hotspot del celular para salir por otra IP.

Ojo: puedes ver 429 en las líneas de `mobile+cffi` / `mobile+requests` y aun así terminar en `✓ Authentication successful`. Eso es normal — el fallback funcionó. Lo único que decide es la línea `Logged in as:`.

**`uvx no se reconoce`** — no reabriste la terminal después de instalar `uv`. Ver arriba.

## Paso 2 — El MCP ya está configurado

Vive en `.mcp.json` en la raíz del repo, así que aplica a cualquier sesión de Claude Code abierta en AIS-OS. No hay credenciales en el archivo — solo el comando y la lista de herramientas activas.

Abre una sesión nueva de Claude Code en el repo y aprueba el servidor cuando lo pregunte (`/mcp` para ver el estado).

Si el servidor no arranca y `/mcp` marca `failed`, es que Claude Code no resuelve `uvx` desde el PATH. Cambia `command` en `.mcp.json` por la ruta completa:

```json
"command": "C:\\Users\\Usuario\\.local\\bin\\uvx.exe"
```

**WSL:** los tokens viven en el home de quien corrió la auth. Si autenticaste en PowerShell pero corres Claude Code dentro de WSL, el servidor no los encuentra — repite el Paso 1 dentro de WSL, o apunta `GARMINTOKENS` al directorio de Windows montado.

## Paso 3 — Verificar

Pregunta en una sesión nueva: *"¿Cómo dormí anoche según Garmin?"* Si responde con datos reales, está conectado.

## Herramientas activas

El servidor trae 138 herramientas. Cargarlas todas se come contexto en cada sesión, así que `.mcp.json` usa `GARMIN_ENABLED_TOOLS` como allowlist de 11:

| Herramienta | Para qué |
|---|---|
| `get_stats` | Resumen del día: pasos, calorías, FC, estrés, body battery, sueño |
| `get_sleep_summary` | Sueño de la noche (fases, score) |
| `get_stress_summary` | Estrés del día |
| `get_body_battery` | Batería corporal — carga y descarga |
| `get_hrv_data` | HRV nocturno |
| `get_morning_training_readiness` | Readiness al despertar |
| `get_training_status` | Estado de entrenamiento (carga, forma) |
| `get_rhr_day` | Frecuencia cardíaca en reposo |
| `get_daily_steps` | Pasos por rango de fechas |
| `get_weekly_stress` | Tendencia semanal de estrés |
| `get_activities` | Actividades recientes |

Para activar más, agrega el nombre a `GARMIN_ENABLED_TOOLS` en `.mcp.json`. Lista completa en el README del repo. Si borras la variable, se cargan las 138.

## Uso en el AIOS

Ya está cableado en dos skills:

**`/morning`** — sección **Energía**, entre la agenda y los Top 3 Outcomes. Lee sueño de anoche, body battery y estrés de ayer. Una línea de datos, una de lectura. Con batería corta el outcome más pesado va al primer bloque; con batería alta se ataca lo que llevas posponiendo. Si Garmin no responde, la sección desaparece en silencio.

**`/eod`** — línea **Costo del día**. Cruza la caída de body battery contra las tareas cerradas. Día caro sin cierres es una señal; día caro con cierres es solo un martes.

Consultas sueltas también sirven: *"¿cómo viene mi estrés esta semana?"*

Garmin registra el sueño bajo la fecha de **despertar** — anoche se consulta con la fecha de hoy.

## Notas

- Todo es lectura para lo que tenemos activo. Las herramientas de escritura (crear workouts, subir actividades) están fuera de la allowlist.
- **Los datos de salud no salen del chat.** Ni a Notion, ni al Brain, ni al correo de cofundadores del `/eod`, ni a contenido. Está escrito explícitamente en ambas skills. Si algún día quieres registrarlos en algún lado, pídelo — no pasa por default.
- Nada de esto es consejo médico. Es contexto operativo para ordenar el día.
