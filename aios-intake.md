# AIS-OS Intake

This is the source-of-truth file for your AIOS. Fill it in by typing, voice-pasting (Wispr Flow / OS dictation), or running `/onboard` for a guided conversation. Whichever mode, this file is what `/onboard` reads to scaffold your Day-1 setup.

**Hard cap: 7 questions.** Each answerable in under 60 seconds. Don't overthink — you can edit and re-run `/onboard` any time.

---

## Q1 — Who are you, what do you sell, who do you sell it to?

Identity, offer, ICP. One paragraph each is fine.

```
Quién soy: Soy Amauri, Co-Founder y CTO de 1Klick, un ecosistema SaaS de automatización de ventas para empresas latinoamericanas. También co-fundé Digital Compass, una consultora de IA basada en Cancún, México. Me encargo de la arquitectura técnica, el desarrollo de producto y la estrategia de IA. Soy speaker activo en la comunidad de IA/tech en LATAM y organizo eventos sobre tecnología e inteligencia artificial en la región.

Qué vendo: 1Klick es un ecosistema SaaS compuesto por 1Klick Ads (automatización de campañas de Meta Ads) y próximamente 1Klick Sales (CRM para WhatsApp con agentes de IA), diseñado para que las empresas latinoamericanas vendan más con menos fricción. Complementariamente, a través de Digital Compass ofrezco consultoría de IA para PyMEs en México y LATAM, ayudándolas a implementar soluciones prácticas que generan resultados reales.

A quién se lo vendo: Mi cliente ideal es la PyME latinoamericana con operaciones activas y ganas de crecer, pero sin un equipo técnico interno. En 1Klick apuntamos a dueños de negocio y agencias de marketing que quieren escalar sus resultados en Meta y automatizar su proceso de ventas por WhatsApp. En Digital Compass atendemos empresas en México que necesitan estrategia e implementación de IA a la medida.
```

---

## Q2 — Paste 1-2 things you've written recently. Don't edit them.

An email, a LinkedIn post, a DM, a doc — anything that sounds like you when you're not trying. **Paste verbatim.** Do not type these mid-conversation with Claude — chat-shaped samples are worse than no samples (voice contamination).

```
Sample 1 — LinkedIn post (raw):

El 4 de abril nos reunimos más de 600 personas en Cancún con un objetivo en común: entender cómo la IA está cambiando los negocios en LATAM.

Honestamente, no sabíamos qué esperar.

Lo que vivimos superó todas las expectativas. 

Salas llenas. Conversaciones reales. Empresarios, emprendedores y profesionales que no solo vinieron a escuchar — vinieron a transformar la forma en que trabajan.

Eso fue la Cumbre de IA y Tecnología Cancún 2026.

Tuvimos un lineup increíble de speakers que subieron al escenario a compartir lo que realmente está pasando con la IA en los negocios:

🎤 Gerry Del Real — sobre el futuro de la IA en los negocios de LATAM
🎤 Wander Oliveira Campos Digital Marketing — sobre cómo la IA está revolucionando el marketing
🎤 César Basurto — Atoms, sobre IA aplicada a ecommerce
🎤 Wayo Castellanos — sobre IA y finanzas personales y empresariales
🎤 Josué Abellán Arias — sobre negocios, legado y construir algo que trascienda
🎤 Yo — presenté Senna, un asistente de IA en WhatsApp para negocios
🎤 ...y muchos speakers más que llenaron el día de ideas, casos de éxito y visión

Pero lo más importante que me llevo no es el número de asistentes ni las fotos del evento.

Es saber que hay una comunidad hambrienta de seguir aprendiendo. 💪

Y eso es exactamente lo que viene:

→ Capacitaciones prácticas de IA para negocios
→ Talleres y workshops
→ Más eventos en Cancún y LATAM
→ Recursos y herramientas para implementar IA hoy

Esto fue el inicio. No el cierre.

Gracias a cada persona que estuvo ahí, a todos los speakers, a los sponsors y al equipo que hizo posible todo esto.

Si quieres ser parte de lo que sigue — sígueme aquí y únete a nuestra comunidad. El futuro de los negocios en LATAM lo estamos construyendo juntos. 🧭

#IA #InteligenciaArtificial #Cancún #LATAM #DigitalCompass #CumbreIA #Negocios #Tecnología
```

```
Sample 2 — LinkedIn post (raw):

La semana pasada tuve el honor de subir al escenario junto a Gerry Del Real en el Claude Code Meetup en Cancún.

Compartir lo que hemos construido con IA fue una experiencia que me recuerda por qué vale la pena seguir apostando por esto. Y me reafirma que Quintana Roo tiene todo para ser un referente tecnológico en la región.

Gracias a Ricardo Lira de la Vega, Esteban Gorupicz y Cesar Méndez por la organización y por hacer que fuera posible.

#Claude #ClaudeCode #Anthropic #AI #CommunityBuilding #Mexico #Mérida #Cancún #DevCommunity
```

---

## Q3 — What are your 2-3 biggest priorities for the next 90 days?

Quarterly priorities. Not yearly aspirations. Things that, if not done by July, would make you say "I wasted Q2."

```
1. Lanzar 1Klick con primeros clientes pagando — mínimo 50 clientes activos usando la plataforma (Meta Ads + agentes de ventas por WhatsApp) antes del 30 de junio. Si no llegamos a 50 con MRR real para julio, perdimos el Q2.
2. MVP de 1Klick en producción — primera versión completa con agentes de ventas por WhatsApp funcionando, onboarding por QR incluido, con al menos 1 cliente piloto real. Fecha límite: fin de mayo.
```

---

## Q4 — Where does revenue actually land, and where is it tracked?

Multiple answers OK. Stripe? Skool? GoHighLevel? QuickBooks? A spreadsheet?

```
Stripe
```

---

## Q5 — Where do you talk to customers, your team, and the outside world day-to-day?

Email (which one — Gmail / Outlook)? Slack? Teams? DMs (Skool / Discord / iMessage)? Phone?

```
Gmail y WhatsApp
```

---

## Q6 — Where do meeting recordings, notes, and important docs live?

Granola? Otter? Fireflies? Google Drive? Notion? Dropbox? A folder on your desktop you keep meaning to organize?

```
Google Drive, Notion, y Granola
```

---

## Q7 — What's the one task that eats your week, and where do you currently track work?

The single biggest time-suck or recurring drudgery. Plus where tasks/projects live (ClickUp / Asana / Linear / Notion / a notebook).

```
Tareas: Notion
Drudgery: Propuestas para clientes y generación de contenido — ambas consumen tiempo y se sienten repetitivas pero no se pueden ignorar.
```

---

When this file is filled, run `/onboard` (or re-run it) and the wizard will scaffold your Day-1 file set: `context/`, `references/voice.md`, populated `connections.md`, and a filled `CLAUDE.md`.
