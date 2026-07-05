# /cto incident-postmortem — Postmortem blameless

## Scopo
Trasformare un incidente in apprendimento sistemico: cosa è successo, perché, cosa cambia.

## Input
- Incidente (cosa, quando rilevato, quando risolto) · impatto (partner/PMI coinvolti, durata)

## Passi
1. **Timeline fattuale**: rilevazione → diagnosi → mitigazione → risoluzione, con orari.
   Chi ha fatto cosa (per capire il processo, mai per colpevolizzare).
2. **Impatto**: partner/PMI coinvolti, dati esposti sì/no, SLA violati, durata.
3. **Root cause analysis** (5 Whys): la causa radice è quasi sempre di processo/sistema,
   non di persona. Fermati alla causa che possiamo cambiare.
4. Cosa ha funzionato nella response / cosa no.
5. **Action items**: max 5, ognuno con owner e deadline — prevenzione (non ricapiti),
   rilevazione (accorgersene prima), mitigazione (danno minore).
6. **Obblighi di notifica**: dati personali coinvolti o servizio essenziale impattato?
   → handoff immediato `compliance` (valutazione notifica 24h/72h NIS2-GDPR) e `ceo`.
   Il postmortem è anche evidenza per il registro incidenti compliance.
7. Comunicazione ai partner coinvolti → `delivery` (gated PREPARE→APPROVE→EXECUTE).

## Formato output
```markdown
---
zone: prodotto
tier: 🟡
type: postmortem
incident-date: YYYY-MM-DD
severity: {P0|P1|P2}
---
# Postmortem — {incident} (blameless)

## Timeline          ## Impatto
## Root cause (5 Whys)
## Cosa ha funzionato / cosa no
## Action items | Azione | Tipo (prev/detect/mitig) | Owner | Deadline |
## Notifiche (compliance) e comunicazioni (partner)
```

## Destinazione
Zona `prodotto` → `postmortem/YYYY-MM-DD-{slug}.md`; riferimento nel registro incidenti
di `compliance`. Commit (admin): `[cto] postmortem: {incident}`.

## Handoff
`compliance` (registro + notifiche) · `ceo` (se impatto clienti) · `delivery` (comunicazione).
