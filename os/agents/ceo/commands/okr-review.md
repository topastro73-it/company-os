# /ceo okr-review — Review OKR

## Scopo
Fotografare il progresso degli OKR del quarter, identificare i KR a rischio, correggere rotta.

## Input
- Nessuno obbligatorio; opzionale: quarter (default: corrente)

## Passi
1. Carica zona `direzione` → `okrs/{quarter}.md` e le metriche dagli snapshot di zona
   (`commerciale` per pipeline/revenue, `clienti` per health/churn, `prodotto` per delivery).
2. Per ogni **Objective**: stato On Track / At Risk / Off Track.
3. Per ogni **Key Result**: valore attuale vs target, % progresso, trend rispetto all'ultima
   review, blocker identificati. Cita la fonte di ogni numero (file di zona).
4. **Azioni correttive** per i KR At Risk/Off Track: azione, owner (agente), deadline.
5. **Proponi aggiustamenti** solo se motivati: KR da droppare, target da rivedere, nuovi KR.
   Un cambio target è una decisione → se accettato, registra con `/ceo decision`.
6. Aggiungi la sezione review al file OKR (append, non riscrivere lo storico).

## Formato output
```markdown
## Review {YYYY-MM-DD}

| Objective / KR | Target | Attuale | Progresso | Trend | Semaforo |
|---|---|---|---|---|---|

### KR a rischio
- [KR] — perché — azione correttiva (owner, deadline)

### Note e decisioni proposte
```

## Destinazione
Zona `direzione` → `okrs/{quarter}.md` (sezione review appesa).
Commit: `[ceo] okr: review {quarter}`.

## Handoff
- KR prodotto a rischio → `product` (riprioritizzazione) o `cto` (capacity)
- KR revenue a rischio → `sales` (`/sales board` + `deal-review` sui top deal)
- KR retention a rischio → `delivery` (`/delivery alert-check`)
