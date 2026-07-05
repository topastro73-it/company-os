# /product sync-clickup — Sync verso ClickUp

## Scopo
Portare spec e roadmap su ClickUp (epic, task, doc) senza mai scrivere senza approvazione.

## Input
- Cosa sincronizzare: una spec (`prd-{slug}`), la roadmap, o update di task esistenti

## Passi — SEMPRE PREPARE → APPROVE → EXECUTE
1. **PREPARE**
   - Leggi la spec sorgente nella zona `prodotto` (mai fidarti del testo già su ClickUp)
     e le coordinate/regole da `config/integrations.yaml` (workspace, folder Delivery
     Board / Product Roadmap / Product Specs, liste, priority map).
   - Genera il file di approvazione con la lista completa delle azioni:
     CREATE/UPDATE epic, task, subtask, doc — per ognuna: summary, lista, priorità, tag.
   - Regole task: **in inglese**, tag `from-company-os` + `spec:{slug}`, status iniziale
     Backlog, epic collegata via dependency blocking, dati verificati contro la spec
     (mai inventare: se manca, segnala il gap).
2. **APPROVE**: l'umano rivede il file e conferma esplicitamente. Nessuna conferma =
   nessuna azione. Solo i comandi read-only saltano l'approvazione.
3. **EXECUTE**: esegui le azioni via MCP ClickUp, logga ogni esito nel file, spostalo in
   `clickup-done/`. Aggiorna il frontmatter della spec (`clickup-epic:`, `clickup-doc:`).
4. **MCP assente**: prepara comunque il file in `clickup-pending/` e segnala:
   "ClickUp non disponibile — file pronto, eseguirò alla prossima sessione con MCP attivo."

## Formato output (file di approvazione)
```markdown
---
zone: prodotto
tier: 🟡
type: clickup-sync
status: pending          # pending → executed
---
# ClickUp Sync — approvazione richiesta ({YYYY-MM-DD})
| # | Azione | Oggetto | Dettagli |
|---|---|---|---|
| 1 | CREATE Epic | "…" | List: Epics, tag: from-company-os |
## Conferma: rispondi "approva" o modifica il file.
```

## Destinazione
Zona `prodotto` → `clickup-pending/YYYY-MM-DD-{cosa}.md`; eseguiti → `clickup-done/`.
Commit (admin): `[product] clickup: sync {cosa}`.
