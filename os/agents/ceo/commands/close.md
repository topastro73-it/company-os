# /ceo close — Chiusura sessione admin

## Scopo
Persistere tutto: snapshot delle zone, memoria narrativa, learnings, commit, push, health.

## Input
Nessuno. Eseguibile solo in sessione admin (git).

## Passi
1. **Snapshot Drive → git**: esegui `osctl snapshot` (zone Drive-master → `company/`,
   finance → `vault/finance/`). Se Drive non raggiungibile: segnala e prosegui col repo.
2. **Wiki di sessione**: genera `system/wiki/sessions/YYYY-MM-DD-{slug}.md` — decisioni prese,
   ragionamenti, promesse, domande aperte. Pseudonimizza le persone dei clienti (iniziali + ruolo);
   mai dati 🔴/PII (regola kernel §2).
3. **Learnings**: se sono emersi pattern riutilizzabili, proponi max 2 nuovi `LRN-XXX` per
   `system/learnings.md`; aggiorna i contatori di quelli applicati. Il CEO approva/rifiuta.
4. **Memoria**: dati business emersi in chat non ancora salvati → proponi il file di zona giusto
   (`os/protocols/memory.md`).
5. **Changelog check**: se la sessione ha toccato `os/`, `zones/`, `config/`, `tools/`, `CLAUDE.md`
   → verifica entry in `system/CHANGELOG.md` nello stesso commit; se manca, creala ora.
   Poi chiedi: "serve `osctl publish` per distribuire su Drive?" (→ `/admin publish`).
6. **Guardrail**: esegui `scripts/audit/secret-scan.sh --staged` e `scripts/audit/link-lint.py`.
   Se rosso: fermati e sistema prima di committare.
7. **Commit & push**: `git add -A` → commit `[ceo] close: YYYY-MM-DD` → `git fetch` →
   se il remote ha commit nuovi, `git merge origin/main --no-edit` → `git push origin main`
   (fallback `--rebase` se rejected).
8. **Health**: esegui `/admin health` in modalità sintetica; riporta il semaforo.
9. **Summary finale**: SHA, file toccati, esito snapshot/publish, conflitti, alert health.

## Guardrail
- **MAI** `git reset --hard` o `git push --force`
- Repo già clean → dichiaralo e fermati
- Branch ≠ main → avvisa prima di procedere

## Destinazione
Git (commit) + `system/wiki/` + `system/learnings.md`. Nessun file di zona nuovo.
