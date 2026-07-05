# Spec lifecycle

Ogni spec vive in zona `prodotto` (`30-Prodotto/specs/`, snapshot `company/prodotto/specs/`)
con frontmatter YAML: `status`, `last-updated`, `zone: prodotto`, `tier`, ed eventuali
`clickup-epic:`, `compliance-impact:`. L'agente Product mantiene `specs/INDEX.md` aggiornato.

## Stati

```
draft → evaluated → approved → in-development → shipped
             ↘ declined (finale)    ↘ deferred (con review-date) → rientra
                                    ↘ superseded (sostituita da nuova spec, linkata)
```

| Stato | Significato |
|---|---|
| `draft` | Bozza iniziale |
| `evaluated` | Valutazione business/tecnica completata (BUILD/CONFIGURE/CUSTOM/DECLINE) |
| `approved` | Approvata per sviluppo |
| `in-development` | In lavorazione (Epic ClickUp aperta) |
| `shipped` | Rilasciata e verificata (finale) |
| `declined` | Rifiutata, con motivo (finale) |
| `deferred` | Posticipata, con `review-date` obbligatoria |
| `superseded` | Sostituita da una spec successiva; frontmatter `superseded-by:` (finale) |

Ogni cambio di stato aggiorna frontmatter + INDEX.md. La creazione/aggiornamento di task
ClickUp collegati segue sempre `external-writes.md` (PREPARE → APPROVE → EXECUTE).

## Regola `in-development`

Al passaggio a `in-development` l'agente DEVE proporre:
> "Vuoi che generi il test plan e i test case?"

Il test plan va creato **prima** che lo sviluppo finisca, in `30-Prodotto/testing/`
(`test-plan-{slug}.md`, `test-case-{slug}.md`).

## Regola `shipped`

Una spec passa a `shipped` **solo quando entrambe** le condizioni sono vere:
- (a) TUTTI i task dell'Epic ClickUp associata sono in stato `Released` (non basta `Done`/`Tested`)
- (b) esiste un test report **UAT con verdetto GO** in `30-Prodotto/testing/test-report-{slug}-cycle{N}.md`

Verificare entrambe prima di aggiornare lo status. Se ClickUp non è disponibile, non marcare
`shipped`: segnala e rimanda alla prossima sessione con MCP attivo.

## Regola `spec-reconciliation`

Prima di marcare `shipped`, l'agente DEVE rileggere task e commenti dell'Epic per verificare
se durante lo sviluppo sono emersi cambiamenti rispetto alla spec originale: scope modificato,
AC aggiustati, funzionalità rimosse/aggiunte, comportamenti diversi da quanto scritto.

Se ci sono divergenze → aggiorna la PRD con i dati reali **prima** di impostare `status: shipped`.
La PRD finita descrive il prodotto **come è stato costruito**, non come era pianificato.

## Status check — prima di ogni attività prodotto

Prima di qualsiasi attività prodotto (evaluate-request, write-spec, prioritize-backlog,
roadmap-review, sprint-planning, status-check, product-plan, weekly-digest):

1. **Scansiona** `specs/INDEX.md` + frontmatter `status` / `last-updated` di ogni spec
2. **Identifica le stale** con queste soglie:

| Status | Stale dopo |
|---|---|
| `draft` | 7 giorni |
| `evaluated` / `approved` | 14 giorni |
| `in-development` | 30 giorni |
| `deferred` | alla `review-date` |
| `shipped` / `declined` / `superseded` | mai (finali) |

3. **Se ci sono stale**, chiedi PRIMA di procedere:

> 📋 **Spec Status Check** — confermami lo stato di queste spec:
>
> | Spec | Stato | Da quando | Aggiornamento? |
> |---|---|---|---|
> | prd-xyz.md | approved | 2026-06-15 | → in-development? shipped? deferred? |

4. **Aggiorna** frontmatter (`status`, `last-updated`, `last-status-check`) e INDEX.md
5. **Procedi** con il lavoro originale

Eccezioni (salta il check): già fatto nelle ultime 4 ore nella stessa sessione; nessuna spec
stale; attività non-prodotto.
