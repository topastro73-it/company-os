# /admin publish — Distribuzione git → Drive

## Scopo
Portare il sistema (agenti, protocolli, CLAUDE.md di zona, viewer, seed) sulle zone Drive,
in sola lettura per i collaboratori. È l'unico modo in cui una modifica di sistema
raggiunge chi lavora su Drive.

## Input
- Nessuno (publish completo) oppure scope (`zones/`, `os/agents/`, un file specifico)

## Passi
1. **Pre-check**: working tree pulito e pushato; `scripts/audit/link-lint.py` e
   `secret-scan.sh` verdi; changelog aggiornato per le modifiche che stai distribuendo.
2. **PREPARE**: esegui `osctl publish --dry-run` (o simula): lista completa di cosa
   verrà scritto — file → cartella Drive di destinazione, quali `.md` con
   `render: gdoc` verranno convertiti in Google Doc, cosa verrà sovrascritto.
3. **APPROVE**: mostra la lista al founder; conferma esplicita. Nessuna conferma =
   nessuna scrittura.
4. **EXECUTE**: `osctl publish`; logga gli esiti; errori parziali → report di cosa è
   andato e cosa no (mai lasciare lo stato ambiguo).
5. **Verifica**: spot-check su Drive (un CLAUDE.md di zona, il viewer in `_OS/`).
6. Registra: commit `[admin] system: publish {scope}` se il publish ha aggiornato
   metadati (es. ID Google Doc nei frontmatter).

## Formato output (in chat)
```
## Publish — {YYYY-MM-DD}
Scope: {…} · File scritti: {n} · Google Doc creati/aggiornati: {n}
Errori: {n} (dettaglio) · Verifica spot: OK/KO
```

## Destinazione
Drive: `_OS/`, `90-Condivisi/`, `CLAUDE.md` di zona. Nessun file operativo di zona
viene toccato (quelli sono Drive-master).

## Guardrail specifici
- Mai pubblicare file 🔴 o contenuti di `vault/`
- Zone `git_to_drive` soltanto: publish non scrive MAI su zone Drive-master
