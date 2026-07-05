# /finance bandi-status — Pipeline bandi e agevolazioni

## Scopo
Tracciare bandi e agevolazioni (Invitalia, MIMIT, regionali, credito R&D, formazione 4.0):
cosa stiamo seguendo, scadenze, rendicontazioni. Area condivisa con il consulente bandi (esterno,
scrive SOLO qui).

## Input
- Nessuno (report) oppure aggiornamento ("aggiungi bando {X}", "presentata domanda {Y}")

## Passi
1. Carica `finance/bandi/` — un file per bando + `status.md` riepilogativo.
2. **Modello dati** per bando: ente, oggetto, importo potenziale, stage
   (`radar → valutazione → in-preparazione → presentato → ammesso | respinto →
   in-rendicontazione → chiuso`), scadenza presentazione, scadenze rendicontazione,
   owner (consulente bandi/CEO), documenti richiesti con stato.
3. **Alert**: scadenza presentazione ≤14gg con documenti mancanti → 🔴; rendicontazione
   ≤30gg → 🟡; requisiti a rischio (es. mantenimento requisiti startup innovativa) → flag.
4. **Eligibilità nuovi bandi**: segnala l'opportunità con requisiti e effort; la conferma
   di eligibilità fiscale/formale è **del commercialista** — mai darla per certa.
5. Aggiorna `status.md`; gli importi ammessi entrano nel cashflow come entrate **solo
   dopo l'ammissione formale**, con la data realistica di erogazione (mai come revenue).

## Formato output
```markdown
---
zone: finance/bandi
tier: 🔴
type: bandi-status
---
# Bandi — {YYYY-MM-DD}

## Alert (scadenze e documenti mancanti)
## Pipeline
| Bando | Ente | Importo | Stage | Prossima scadenza | Owner | Note |
## In rendicontazione (adempimenti e date)
## Nuove opportunità da valutare (validare con commercialista)
```

## Destinazione
Sottozona `finance/bandi` → `status.md` + file per bando.
Commit (admin): `[finance] bandi: status {YYYY-MM-DD}`.

## Handoff
Ammissione/erogazione → `/finance cashflow` · decisione di partecipare (effort alto) → `ceo`.
