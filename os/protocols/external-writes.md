# External writes — PREPARE → APPROVE → EXECUTE

Ogni **scrittura su un sistema esterno** passa da tre fasi obbligatorie, con approvazione
umana esplicita nel mezzo. Vale per: ClickUp (task, epic, doc), HubSpot (CRM), Gmail
(anche solo bozze), publish Drive verso terzi (`per-commercialista/`, `evidence/`, condivisioni),
Calendar, e qualsiasi integrazione futura. Le **letture** sono libere.

## Fase 1 — PREPARE

L'agente analizza l'input (spec, roadmap, pipeline, email thread) e genera un **file di
staging** con la lista completa delle azioni proposte. Il file va nella zona pertinente:

| Sistema | Staging | Log eseguiti |
|---|---|---|
| ClickUp | `company/prodotto/clickup-pending/` (Drive: `30-Prodotto/clickup-pending/`) | `company/prodotto/clickup-done/` |
| HubSpot | `company/commerciale/hubspot-pending/` | `company/commerciale/hubspot-done/` |
| Gmail (bozze/invii) | `company/{zona}/mail-pending/` della zona del contenuto | `company/{zona}/mail-done/` |
| Publish a terzi | `company/{zona}/publish-pending/` | `company/{zona}/publish-done/` |

Naming: `YYYY-MM-DD-{comando}.md` (es. `2026-07-04-sync-spec-bulk-import.md`).

### Formato del file di approvazione

```markdown
---
zone: prodotto
tier: 🟡
system: clickup            # clickup | hubspot | gmail | drive-publish
command: sync-spec         # comando che ha generato lo staging
status: pending            # pending | approved | executed | cancelled
---
# {Sistema} — Approvazione richiesta
Data: YYYY-MM-DD · Agente: {slug} · Sorgente: {file spec/pipeline/thread}

## Azioni proposte

| # | Tipo | Oggetto | Dettagli |
|---|------|---------|---------|
| 1 | CREATE Task | "Nome task" | List: Feature, Priority: High, Status: Backlog |
| 2 | UPDATE Task | CYB-123 | Status: In Progress → Done |
| 3 | CREATE Draft | a: toni@dna.fi | Oggetto: "Pilot annex", allegato: … |

## Conferma
Rivedi le azioni, poi: `/{agente} approve {path-del-file}`. Per annullare: status → cancelled.
```

Ogni riga deve essere abbastanza dettagliata da valutare l'azione **senza aprire il sistema
esterno**. Dati citati (soglie, AC, importi, destinatari) verificati sulla sorgente nel repo/zona
— mai copiati da versioni stale, mai inventati: se un dato manca, segnala il gap invece di riempirlo.

## Fase 2 — APPROVE

Un umano rivede il file e approva esplicitamente (comando `approve` o conferma in chat sul
file specifico). Regole:
- **Mai eseguire senza approvazione esplicita** — "ok" generico su altro argomento non vale
- Approvazione parziale: l'umano cancella/commenta le righe non volute; si esegue il resto
- File più vecchio di 7 giorni → ri-validare i dati prima di eseguire (PREPARE di nuovo se serve)

## Fase 3 — EXECUTE

L'agente esegue le azioni approvate via MCP, nell'ordine del file:
1. Ogni azione eseguita viene marcata nel file con esito e ID creato (es. `→ done, task CYB-456`)
2. Errore su un'azione → si annota, si prosegue con le successive, si riporta il bilancio finale
3. Al termine: `status: executed`, file spostato nella cartella `*-done/` corrispondente
4. Summary in chat: azioni riuscite/fallite, link agli oggetti creati

## MCP non disponibile

Il flusso non si blocca: PREPARE si completa comunque, il file resta in `*-pending/` e si
segnala "sistema esterno non disponibile — file pronto, eseguirò al prossimo avvio con MCP attivo".
Al ritorno del tool, si riparte dalla Fase 2 (o 3 se già approvato e ancora fresco).
