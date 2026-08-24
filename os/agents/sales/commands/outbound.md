# /sales outbound — Sequenza outbound / ABM

## Scopo
Creare o aggiornare una sequenza outbound per un segmento del funnel
(i segmenti reali sono dichiarati in `config/company.yaml`).

## Input
- Segmento target (da `zones/_root/context/` ICP) · obiettivo (meeting, trial/valutazione gratuita)
- Lista target (da `commerciale/target-funnel.md`) · canale (email, LinkedIn, telefono)

## Passi
1. Carica il funnel (`commerciale/target-funnel.md`) e i learnings outbound attivi.
2. **Definisci la sequenza**: 4-6 touch su 2-3 settimane, canali alternati.
   Per ogni touch: giorno, canale, obiettivo, messaggio (personalizzabile con variabili
   `{azienda}`, `{pain}`, `{trigger}`).
3. **Messaggio**: parla del problema del segmento — il suo driver di acquisto
   (regolatorio, es. una direttiva come NIS2; oppure di costo, rischio o crescita) —
   una sola CTA per touch, zero claim non supportati, zero feature non shipped.
4. **Criteri di uscita**: risposta → passa a opportunità (`/sales opportunity` in discovery);
   no risposta dopo sequenza completa → nurture/cold nel funnel.
5. Salva la sequenza; l'**invio reale** (Gmail/HubSpot) è una scrittura esterna:
   PREPARE (bozze) → APPROVE (review umana) → EXECUTE. Mai invii automatici.
6. Traccia i risultati per touch (sent/open/reply) per iterare.

## Formato output
```markdown
---
zone: commerciale
tier: 🟡
type: sequence
segment: segment-a
---
# Sequenza — {segmento} — {obiettivo}

| # | Giorno | Canale | Obiettivo | Oggetto/hook |
|---|---|---|---|---|

## Touch 1 — {canale}
{testo con variabili}
…
## Criteri di uscita e metriche
```

## Destinazione
Zona `commerciale` → `sequences/{segmento}-{slug}.md`.
Commit (admin): `[sales] outbound: sequenza {segmento}`.

## Handoff
Copy da raffinare o nurture di lungo periodo → `marketing` (`/marketing sequence`).
