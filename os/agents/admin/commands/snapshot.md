# /admin snapshot — Backup Drive → git

## Scopo
Scaricare le zone operative Drive-master nel repo (`company/`, `vault/finance/`) e
committare: git resta versioning e backup completo anche del piano operativo.
Gira nightly (GitHub Action) e manualmente al `/ceo close`.

## Input
- Nessuno (tutte le zone Drive-master) oppure zona specifica

## Passi
1. Esegui `osctl snapshot`: per ogni zona con `sync: drive_master` in `config/acl.yaml`
   scarica i file nella destinazione (`company/{zona}/`; `finance` → `vault/finance/`).
2. **Direzione unica**: lo snapshot scrive SOLO da Drive verso git. Se in `company/` ci
   sono modifiche locali non pubblicate che verrebbero sovrascritte → fermati e segnala
   il conflitto (il master vince, ma la perdita va dichiarata, mai silenziosa).
3. **Secret-scan** sul materiale scaricato: file 🔴 fuori posto (es. contratto firmato
   in zona sbagliata) → alert, non committare finché non è ricollocato.
4. Commit: `[snapshot] drive: {YYYY-MM-DD}` (vault: commit separato nel repo privato).
5. Report: file nuovi/modificati/rimossi per zona, anomalie, dimensioni inattese.

## Formato output (in chat)
```
## Snapshot — {YYYY-MM-DD}
| Zona | Nuovi | Modificati | Rimossi | Anomalie |
|---|---|---|---|---|
Commit: {sha} · Vault: {sha|n/a} · Alert: {…}
```

## Destinazione
Git: `company/{zona}/` e `vault/finance/`. Nessuna scrittura su Drive.

## Guardrail specifici
- Drive irraggiungibile → segnala e termina senza commit parziale ambiguo
- Mai risolvere un conflitto scrivendo su Drive da qui: il fix si fa sul master (Drive)
