#!/usr/bin/env python3
"""Métricas del funnel de demos de 1Klick, directo desde Supabase.

Lo usa la skill /campana. Imprime el embudo real (quiz -> contacto -> agenda ->
demo -> cierre) que Meta NO puede ver: Meta solo llega hasta el evento `Lead`,
que es la puerta de contacto (paso 6) y es un proxy débil de la agenda.

Uso:
    python3 scripts/funnel_metrics.py [--days 60] [--env RUTA_A_.env.local]

Credenciales: se leen de /Users/amaurisotolongo/Projects/1klickads-funnel/.env.local
(NEXT_PUBLIC_SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY). No se duplican aquí.
"""

import argparse
import collections
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request

DEFAULT_ENV = "/Users/amaurisotolongo/Projects/1klickads-funnel/.env.local"
COLS = (
    "id,created_at,current_step,booked,booked_at,contacted_at,utm_content,"
    "utm_source,business_type,main_pain,ads_manager,ad_budget,main_goal,"
    "crm_status,crm_seller"
)


def load_env(path):
    """Lee KEY=VALUE de un .env sin dependencias externas."""
    if not os.path.exists(path):
        sys.exit(f"No encontré {path}. Pasa la ruta con --env.")
    env = {}
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip().strip("'\"")
    missing = [
        k
        for k in ("NEXT_PUBLIC_SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY")
        if not env.get(k)
    ]
    if missing:
        sys.exit(f"Faltan en {path}: {', '.join(missing)}")
    return env


def fetch_leads(env, days):
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).date()
    query = urllib.parse.urlencode(
        {
            "select": COLS,
            "created_at": f"gte.{since}",
            "order": "created_at.asc",
            "limit": "10000",
        }
    )
    url = f"{env['NEXT_PUBLIC_SUPABASE_URL']}/rest/v1/leads?{query}"
    key = env["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(
        url, headers={"apikey": key, "Authorization": f"Bearer {key}"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def parse(ts):
    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))


def pct(part, whole):
    return f"{part / whole * 100:.1f}%" if whole else "n/a"


def section(title):
    print(f"\n{'=' * 68}\n{title}\n{'=' * 68}")


def report_windows(leads, now):
    """Compara últimos 7d contra los dos periodos previos de 7d."""
    section("VENTANAS DE 7 DÍAS  (quiz → contacto → agenda)")
    print(f"{'periodo':14}{'quiz':>6}{'contacto':>10}{'agenda':>8}{'ag/quiz':>9}"
          f"{'ag/cont':>9}{'no-show':>9}{'cerrado':>9}")
    for label, start, end in [
        ("últimos 7d", 7, 0),
        ("7d previos", 14, 7),
        ("7d antes", 21, 14),
    ]:
        rows = [
            x
            for x in leads
            if end <= (now - parse(x["created_at"])).total_seconds() / 86400 < start
        ]
        if not rows:
            continue
        cont = [x for x in rows if x["contacted_at"]]
        book = [x for x in rows if x["booked"]]
        ns = sum(1 for x in rows if x["crm_status"] == "no_show")
        cz = sum(1 for x in rows if x["crm_status"] == "cerrado")
        print(
            f"{label:14}{len(rows):>6}{len(cont):>10}{len(book):>8}"
            f"{pct(len(book), len(rows)):>9}{pct(len(book), len(cont)):>9}"
            f"{ns:>9}{cz:>9}"
        )

    # Puerta de contacto: de los que terminaron las 5 preguntas, cuántos dan datos.
    print("\nPuerta de contacto (paso 5 → paso 6), últimos 7d:")
    recent = [
        x for x in leads if (now - parse(x["created_at"])).total_seconds() / 86400 < 7
    ]
    p5 = [x for x in recent if x["current_step"] >= 5]
    gave = [x for x in p5 if x["contacted_at"]]
    print(f"  llegaron a P5: {len(p5)}   dieron contacto: {len(gave)} "
          f"({pct(len(gave), len(p5))})")


def report_weekly(leads):
    section("POR SEMANA (lunes a domingo, fecha de quiz)")
    buckets = collections.defaultdict(lambda: collections.Counter())
    for x in leads:
        c = parse(x["created_at"])
        wk = (c - dt.timedelta(days=c.weekday())).strftime("%Y-%m-%d")
        b = buckets[wk]
        b["quiz"] += 1
        b["cont"] += bool(x["contacted_at"])
        b["book"] += bool(x["booked"])
        b["ns"] += x["crm_status"] == "no_show"
        b["cz"] += x["crm_status"] == "cerrado"
    print(f"{'semana':13}{'quiz':>6}{'contacto':>10}{'agenda':>8}{'ag/quiz':>9}"
          f"{'no-show':>9}{'cerrado':>9}")
    for wk in sorted(buckets):
        b = buckets[wk]
        print(
            f"{wk:13}{b['quiz']:>6}{b['cont']:>10}{b['book']:>8}"
            f"{pct(b['book'], b['quiz']):>9}{b['ns']:>9}{b['cz']:>9}"
        )


def report_close_funnel(leads):
    """El tramo que Meta no ve: agenda → demo asistida → cliente."""
    section("EMBUDO DE CIERRE (histórico del periodo consultado)")
    booked = [x for x in leads if x["booked"]]
    ns = sum(1 for x in booked if x["crm_status"] == "no_show")
    cz = sum(1 for x in booked if x["crm_status"] == "cerrado")
    seg = sum(1 for x in booked if x["crm_status"] == "seguimiento")
    untouched = sum(1 for x in booked if x["crm_status"] == "nuevo")
    showed = len(booked) - ns
    print(f"  agendas            {len(booked)}")
    print(f"  no-show            {ns}  ({pct(ns, len(booked))})   <- palanca más barata")
    print(f"  asistieron         {showed}")
    print(f"  cerrados           {cz}  ({pct(cz, showed)} de los que asistieron)")
    print(f"  en seguimiento     {seg}  (pipeline sin resolver)")
    print(f"  agendas sin tocar  {untouched}")
    print(f"\n  AGENDA → CLIENTE   {pct(cz, len(booked))}")

    # Los que dieron WhatsApp pero nunca agendaron: histórico de 0 cierres.
    nb = [x for x in leads if x["contacted_at"] and not x["booked"]]
    nb_cz = sum(1 for x in nb if x["crm_status"] == "cerrado")
    nb_new = sum(1 for x in nb if x["crm_status"] == "nuevo")
    print(f"\n  WhatsApp sin agendar: {len(nb)}  |  cerrados: {nb_cz}  "
          f"|  nunca tocados: {nb_new}")


def report_sellers(leads):
    section("POR VENDEDOR (solo agendas)")
    g = collections.defaultdict(lambda: collections.Counter())
    for x in leads:
        if x["booked"]:
            g[x["crm_seller"] or "SIN ASIGNAR"][x["crm_status"]] += 1
    print(f"{'vendedor':14}{'agendas':>9}{'no-show':>9}{'% n-s':>8}"
          f"{'cerrado':>9}{'% cierre':>10}{'seguim':>8}")
    for name, c in sorted(g.items(), key=lambda i: -sum(i[1].values())):
        total = sum(c.values())
        showed = total - c["no_show"]
        print(
            f"{name:14}{total:>9}{c['no_show']:>9}{pct(c['no_show'], total):>8}"
            f"{c['cerrado']:>9}{pct(c['cerrado'], showed):>10}{c['seguimiento']:>8}"
        )


def report_creatives(leads, now):
    section("CREATIVOS Y ATRIBUCIÓN (últimos 14d)")
    recent = [
        x for x in leads if (now - parse(x["created_at"])).total_seconds() / 86400 < 14
    ]
    mix = collections.Counter(x["utm_content"] or "SIN UTM" for x in recent)
    for k, v in mix.most_common():
        book = sum(
            1 for x in recent if (x["utm_content"] or "SIN UTM") == k and x["booked"]
        )
        print(f"  {k:16} quiz={v:<6} agendas={book:<5} ({pct(book, v)})")
    leak = mix.get("SIN UTM", 0)
    print(f"\n  Fuga de atribución: {pct(leak, len(recent))} "
          f"(estable esperado 7-9% desde el fix del 24 jul 2026)")
    if len([k for k in mix if k != "SIN UTM"]) == 1:
        print("  ⚠️  UN SOLO CREATIVO cargando el 100% del volumen — punto único de falla.")


def report_segments(leads):
    section("PERFIL DEL COMPRADOR (sobre los que dieron contacto)")
    for field in ("ad_budget", "ads_manager", "main_pain"):
        print(f"\n-- {field}")
        g = collections.defaultdict(lambda: collections.Counter())
        for x in leads:
            if not x["contacted_at"]:
                continue
            c = g[x[field] or "NA"]
            c["cont"] += 1
            c["book"] += bool(x["booked"])
            c["cz"] += x["crm_status"] == "cerrado"
        for k, c in sorted(g.items(), key=lambda i: -i[1]["cont"]):
            print(
                f"  {k:22} contacto={c['cont']:<5} agenda={c['book']:<5} "
                f"({pct(c['book'], c['cont'])})  cerrado={c['cz']}"
            )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=60, help="ventana a consultar")
    ap.add_argument("--env", default=DEFAULT_ENV, help="ruta al .env.local del funnel")
    args = ap.parse_args()

    leads = fetch_leads(load_env(args.env), args.days)
    if not leads:
        sys.exit("Supabase devolvió 0 filas. Revisa credenciales o la ventana --days.")
    now = dt.datetime.now(dt.timezone.utc)

    print(f"{len(leads)} leads desde hace {args.days} días "
          f"| último: {leads[-1]['created_at'][:16]} UTC")
    report_windows(leads, now)
    report_weekly(leads)
    report_close_funnel(leads)
    report_sellers(leads)
    report_creatives(leads, now)
    report_segments(leads)


if __name__ == "__main__":
    main()
