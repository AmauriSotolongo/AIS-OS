# Garmin Connect — Setup para AIOS

Conecta Garmin al AIOS para que `/morning` y `/eod` lean sueño, estrés, body battery y HRV. Señal de energía real, no autopercibida.

MCP: [taxuspt/garmin_mcp](https://github.com/taxuspt/garmin_mcp) — envuelve la librería `python-garminconnect`.

## Paso 1 — Autenticar una sola vez

El servidor no guarda usuario ni contraseña. Autenticas una vez en la terminal y quedan tokens OAuth en `~/.garminconnect`.

```bash
uvx --python 3.12 --from git+https://github.com/Taxuspt/garmin_mcp garmin-mcp-auth
```

Te pide:
- Email de Garmin Connect
- Contraseña
- Código MFA (si lo tienes activo)

Requisitos: Python 3.12 y `uv` instalado (`curl -LsSf https://astral.sh/uv/install.sh | sh`).

Verificar cuando quieras:

```bash
uvx --python 3.12 --from git+https://github.com/Taxuspt/garmin_mcp garmin-mcp-auth --verify
```

⚠️ Los tokens duran ~6 meses. Cuando expiren, vuelve a correr el comando de arriba. Si `/morning` empieza a fallar en la sección de energía, esto es lo primero que hay que revisar.

## Paso 2 — El MCP ya está configurado

Vive en `.mcp.json` en la raíz del repo, así que aplica a cualquier sesión de Claude Code abierta en AIS-OS. No hay credenciales en el archivo — solo el comando y la lista de herramientas activas.

Abre una sesión nueva de Claude Code en el repo y aprueba el servidor cuando lo pregunte (`/mcp` para ver el estado).

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

- `/morning` — cruza sueño y body battery contra la agenda del día. Día de demos con 4 horas de sueño no se ataca igual.
- `/eod` — registra si el día quemó más de lo que aportó.
- Consultas sueltas — *"¿cómo viene mi estrés esta semana?"*

## Notas

- Todo es lectura para lo que tenemos activo. Las herramientas de escritura (crear workouts, subir actividades) están fuera de la allowlist.
- Datos de salud: no los saques del AIOS ni los pegues en contenido público sin decisión explícita.
