# /delivery alert-check — Scansione alert partner

## Scopo
Scansione rapida di tutti i partner per far emergere gli alert che richiedono azione ora.
Alimenta anche il briefing del CoS e lo start del CEO.

## Input
Nessuno.

## Passi
1. Scansiona le schede in `clienti/*/scheda-partner.md` (quick mode: dati disponibili,
   dichiara la freschezza).
2. Genera alert secondo le soglie:
   - health **< 40** → **CRITICAL** (rescue call ≤7gg, escalation CEO)
   - drop **> 15 punti in 30gg** → **WARNING** (call delivery ≤14gg)
   - PMI attive **< 30%** delle onboarded → **LOW ENGAGEMENT**
   - nessuna attività venditori da **30+gg** → **DORMANT**
   - contratto in scadenza entro **60gg** → **RENEWAL**
   - onboarding: milestone critica saltata (primo scan g.14, primo deal sett.8) → **ONBOARDING**
3. Per ogni alert: azione suggerita, owner, deadline.
4. Ordina per gravità; se zero alert, dichiaralo esplicitamente.

## Formato output
```markdown
---
zone: commerciale
tier: 🟡
type: alert-report
---
# Partner Alerts — {YYYY-MM-DD}

| Partner | Health | Alert | Azione suggerita | Owner | Entro |
|---|---|---|---|---|---|
| {slug} | 35 | CRITICAL | Rescue call + escalation CEO | {owner} | 7gg |
| {slug} | 72→55 | WARNING | Call check-in | {owner} | 14gg |
```

## Destinazione
Zona `commerciale` → `delivery/alerts-{YYYY-MM-DD}.md` (sovrascrivibile: conta l'ultimo).
Consegna anche in chat. Commit (admin): `[delivery] alerts: {YYYY-MM-DD}`.

## Handoff
CRITICAL → `ceo` (entro 24h) · RENEWAL → `finance` + `sales` ·
pattern ricorrente → `/delivery churn-analysis`.
