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
3. **Cadence log** (obbligatorio quanto il passo 2): aggiorna `direzione/ceo-cadence.md` — data del
   ritmo eseguito (giornaliero sempre; settimanale se prima sessione della settimana; mensile se prima
   del mese) e un entry nel log risposte. La zona `direzione` è **drive_master**: si scrive sul Drive,
   non sullo snapshot `company/direzione/` (regola kernel §5); lo snapshot nightly lo riporta in git.
   Se il Drive non è raggiungibile, dichiaralo nel summary e lascia la nota al CEO, senza scrivere
   sullo snapshot. Questo passo sta qui e non solo in `/ceo start` per una ragione precisa: una
   scrittura obbligatoria collocata in mezzo a un'interazione lunga salta, e salta in silenzio.
4. **Learnings**: se sono emersi pattern riutilizzabili, proponi max 2 nuovi `LRN-XXX` per
   `system/learnings.md`; aggiorna i contatori di quelli applicati. Il CEO approva/rifiuta.
5. **Memoria**: dati business emersi in chat non ancora salvati → proponi il file di zona giusto
   (`os/protocols/memory.md`).
6. **Changelog check**: se la sessione ha toccato `os/`, `zones/`, `config/`, `tools/`, `CLAUDE.md`
   → verifica entry in `system/CHANGELOG.md` nello stesso commit; se manca, creala ora.
   Poi chiedi: "serve `osctl publish` per distribuire su Drive?" (→ `/admin publish`).
7. **Guardrail**: esegui `scripts/audit/secret-scan.sh --staged`, `scripts/audit/link-lint.py`
   e, se la sessione ha toccato file di sistema, `scripts/audit/i18n-parity.py`.
   Se rosso: fermati e sistema prima di committare.
8. **Commit & push**: `git add -A` → commit `[ceo] close: YYYY-MM-DD` → `git fetch` →
   se il remote ha commit nuovi, `git merge origin/main --no-edit` → `git push origin main`
   (fallback `--rebase` se rejected).
9. **Health**: esegui `/admin health` in modalità sintetica; riporta il semaforo.
10. **Summary finale**: SHA, file toccati, esito snapshot/publish, conflitti, alert health.

## Guardrail
- **MAI** `git reset --hard` o `git push --force`
- Repo già clean → dichiaralo e fermati
- Branch ≠ main → avvisa prima di procedere

## Destinazione
Git (commit) + `system/wiki/` + `system/learnings.md`. Nessun file di zona nuovo.
