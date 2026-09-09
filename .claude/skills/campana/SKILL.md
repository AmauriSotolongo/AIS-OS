---
name: campana
description: Revisión semanal de la campaña de Meta Ads del funnel de demos. Cruza el gasto de Meta con el embudo real de Supabase (quiz → contacto → agenda → demo → cierre), calcula el costo por agenda de verdad, el no-show por vendedor, y entrega UNA recomendación de presupuesto o creativo. Corre los lunes, o antes de tocar el presupuesto.
trigger: "/campana", "cómo va la campaña", "revisa ads", "cómo van los anuncios", "revisión de campaña"
bike-method-phase: 1  # Phase 1 — Training wheels. Correr manualmente cada lunes.
---

# campana — Revisión Semanal de Meta Ads

Meta te dice si el anuncio compra clics baratos. Supabase te dice si compra clientes.
Esta skill cruza las dos y termina en una decisión, no en un reporte.

## La lección que justifica esta skill

El 23 jul 2026 el creativo `Static 1` tenía **mejor CTR (7.90% vs 4.03%)**, **mejor CPC
($1.06 vs $3.10)** y un CPL que se veía sano ($22.23). En Supabase produjo **1 agenda
contra 14** de `UGC 1` — $266 vs $22 por agenda, Fisher p=0.00003.

Meta veía a UGC mejor por 1.56x cuando en realidad era 14x. ¿Por qué? El evento `Lead`
del píxel se dispara en la **puerta de contacto (paso 6)**, no en la agenda. Es un proxy
débil.

**Regla dura: ningún creativo se juzga, se pausa ni se escala por CTR, CPC o CPL.
Solo por agendas en Supabase.** Si esta skill alguna vez te sugiere lo contrario, está rota.

## Dónde vive todo

| Cosa | Dato |
|---|---|
| Cuenta publicitaria | `2743046666066277` — "Gestión Integral del Caribe" (business Digital Compass, MXN) |
| Campaña activa | `120247373401590643` — `1Klick | Leads Web | MX | UGC`, CBO |
| Adset principal | `120247373413250643` (= `utm_term` en los leads) |
| Supabase | proyecto `jpkjwwljjaprdinsebil`, tabla `leads` (compartido con la app 1klickads) |
| Credenciales | `/Users/amaurisotolongo/Projects/1klickads-funnel/.env.local` |
| Script de métricas | `scripts/funnel_metrics.py` |

**NO es la cuenta "Recovery Center" ni ninguna otra.** Ese error deja el desglose por
anuncio vacío y te hace creer que la campaña no gastó.

## Ejecución

### Paso 1 — Supabase primero (es la fuente de verdad)

```bash
python3 scripts/funnel_metrics.py --days 45
```

Imprime: ventanas de 7d, tabla semanal, embudo de cierre, no-show por vendedor, mix de
creativos con fuga de atribución, y perfil del comprador. Léelo completo antes de tocar Meta.

Si falla por credenciales, pasar la ruta con `--env`. Si devuelve 0 filas, **parar** —
sin Supabase esta skill no puede concluir nada y no debe intentarlo.

### Paso 2 — Meta Ads

Con `ads_get_ad_entities` sobre la cuenta `2743046666066277`:

- **Nivel campaign**, `date_preset: last_7d`, campos:
  `id, name, status, effective_status, daily_budget, bid_strategy, amount_spent,
  impressions, clicks, outbound_clicks, ctr, cpc, cpm, frequency, reach, lead, cost_per_lead`
- **Nivel ad**, mismos campos sin `daily_budget`, para ver qué anuncios gastaron.
- **Día a día**: nivel campaign con `time_increment: "1"`, `date_preset: last_14d` y
  `filtering` por `campaign.id`. Esto es lo que revela si un cambio de presupuesto
  degradó el CPM o no.

**Trampas del conector (verificadas, no las re-descubras):**

| Síntoma | Causa | Arreglo |
|---|---|---|
| Error de validación en `spend` | el campo no existe | usar `amount_spent` |
| Error de validación en `inline_link_clicks` | no existe a nivel campaign/ad | usar `outbound_clicks` |
| `cost_per_result` / `results` devuelve `[]` | no combinan a nivel campaign | pedir campos base |
| Gasto incompleto con `last_14d` | preset poco fiable para totales | usar `maximum` o `time_range` |
| `link_url` vacío en `ads_get_creatives` | el conector no lo expone, nunca | verificar el UTM a mano en el administrador |

`clicks` de Meta son TODOS los clics, no solo al enlace. Para juzgar landing → quiz usar
`outbound_clicks`.

### Paso 3 — Cruzar: el único número que importa

```
costo por agenda = amount_spent (7d de Meta) / agendas (7d de Supabase)
```

Compáralo contra la semana anterior. Ese es el KPI de la campaña, no el CPL.

Luego calcula el CAC real: `amount_spent / cerrados`. Contra 1Klick Pro a $1,200 MXN/mes,
cualquier CAC bajo ~$1,200 se paga en menos de un mes.

Si la fuga de atribución (`SIN UTM`) sale arriba de ~10%, avísalo: el costo por agenda
está subestimado y algo se rompió en el paso de UTMs.

### Paso 4 — Diagnóstico del embudo

Con la salida del script, ubica dónde está la pérdida más grande. Orden histórico de
palancas, de más barata a menos:

1. **No-show** — ha vivido entre 40% y 55%. Es gratis de arreglar (recordatorios de
   WhatsApp T-24h / T-1h / T-10min, y limitar los slots de Cal a 24-48h). La mediana
   quiz→agenda es de ~2.6 minutos: agendan en caliente y se enfrían antes de la demo.
2. **Cierre sobre asistencia** — ~5-6%. Mira la varianza por vendedor; ha sido brutal
   (un vendedor con la mitad de las agendas y una fracción de los cierres). Rebalancear
   el routing es gratis.
3. **Puerta de contacto (P5 → P6)** — pierde ~37%, estable. Único punto del quiz que
   vale optimizar, pero solo después de 1 y 2.
4. **Volumen de Meta** — lo último. Casi nunca es la restricción.

Los pasos 1→5 del quiz retienen 96-98% cada uno. No pierdas tiempo ahí.

### Paso 5 — UNA recomendación

Cierra con una sola decisión y su guardarraíl. Sin menú de opciones — eso le devuelve
la decisión a Amauri, que es justo lo que la skill debe evitar.

**Reglas de decisión:**

- **Un cambio a la vez.** Presupuesto y evento de optimización nunca se mueven la misma
  semana, o no vas a saber cuál movió qué.
- **Subir presupuesto** se justifica si el CPM va estable o a la baja mientras el gasto
  sube, y la frecuencia semanal está por debajo de ~2.0. Guardarraíl: si el CPM sube
  >40% sobre la línea base o el costo por agenda pasa de ~$40 MXN sostenido 3 días,
  bajar un escalón y subir 25% cada 3-4 días.
- **Frecuencia semanal >2.0** = lanzar el creativo retador. Es el disparador real,
  no el calendario.
- **Creativo nuevo va en campaña APARTE**, nunca en el adset del ganador. En CBO con
  "highest volume" el retador se queda sin gastar — le pasó a `Static 2`, que murió
  archivado con $0 y 0 filas en Supabase.
- **Antes de despausar cualquier anuncio copiado**, verificar que el `utm_content` sea
  nuevo. Una copia hereda la URL del original y los dos creativos caen indistinguibles
  en Supabase. Esto se revisa a mano en el administrador.
- **Un test a $100/día tarda 2-3 semanas en leerse** (~14 agendas/semana). Solo una
  diferencia enorme se detecta en una semana. No lo mates antes de tiempo.
- **Optimizar a `Schedule`** requiere >50 agendas/semana sostenidas, o cae en
  learning limited.

Si Amauri toma una decisión de presupuesto o creativo, sugerir registrarla en
`decisions/log.md` con la fecha y el número que la justificó.

## Formato de salida

Cabe en una pantalla. Sin preámbulo.

```
## Cómo va (últimos 7 días)

[tabla: quiz / contacto / agenda / cerrados — 7d vs 7d previos]

Gasto $N MXN ($N/día). Costo por agenda $N (vs $N la semana pasada).
[una línea de lectura: ¿arriba del embudo está sano o no?]

## Dónde se pierde el dinero

[el embudo de cierre en 3 líneas: agendas → no-show → asistieron → cerrados]
[la tabla de vendedores solo si hay varianza que amerite acción]

## Qué hacer

[UNA recomendación, con el número que la justifica y su guardarraíl]
```

## Modo degradado

- **Sin conector de Meta** (pide OAuth): correr solo el Paso 1 y reportar el embudo de
  Supabase. Decir explícitamente que el gasto no está verificado y no inventar el costo
  por agenda con el ritmo de la semana pasada. Ofrecer reconectar en `/mcp`.
- **Sin Supabase**: parar. Meta sola no permite ninguna conclusión sobre creativos —
  ese es el punto entero de la skill.

## Notas

- Todo en MXN. Nunca mezclar con USD.
- `leads` no tiene columna `utm_id`; el utm_id vive dentro de `landing_url`.
- El píxel del funnel es `27638353089153383` (el de 1Klick), no el de la agencia
  Digital Compass.
- Hay 87 leads históricos de una campaña borrada (`utm_id 120247272093960643`). Su gasto
  ya no se puede consultar en Meta — no intentes calcular su CPL.
- Perfil del comprador confirmado en 3+ semanas: `nada`/`menos_5k` + `yo_mismo` +
  `anuncios_no_jalan`. El segmento `mas_20k` lleva 0 agendas sobre 5 contactos.
  **No invertir en ángulos de presupuesto alto.** Si un creativo nuevo apunta ahí,
  decirlo antes de que se lance.
- Los que dan WhatsApp sin agendar llevan **0 cierres históricos**. Todos los clientes
  vinieron por el calendario. No es un canal, es una fuga.
