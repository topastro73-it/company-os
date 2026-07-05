# /admin health — Salute del sistema

## Scopo
Un semaforo unico sulla salute meccanica del sistema. Eseguito al `/ceo close` (sintetico)
e on-demand (completo). Verde non è opzionale: rosso = si ferma e si sistema.

## Input
- Nessuno; opzionale: `--quick` (solo check bloccanti)

## Passi
1. **Guardrail eseguibili** (`scripts/audit/`):
   - `secret-scan.sh` — token/chiavi/IBAN/file 🔴 fuori dalle destinazioni ammesse
   - `link-lint.py` — i path citati nei file di sistema esistono
   - `frontmatter-check.py` — `zone:` + `tier:` dichiarati sui file operativi
2. **ACL**: `osctl acl-audit` (drift permessi Drive) — vedi `/admin acl-audit`.
3. **Sync freshness**: ultimo snapshot (nightly girato? quanto è vecchio `company/`?),
   publish pendenti (modifiche di sistema committate ma non distribuite).
4. **Igiene repo**: `.env` mai committato (`git log --all -- .env` vuoto), branch = main,
   CI verde sull'ultimo push, changelog allineato all'ultima modifica di sistema.
5. **Freschezza protocolli/memoria**: learnings senza review da troppo, wiki sessions
   mancanti rispetto alla cadence.
6. Componi il report: ogni check → 🟢/🟡/🔴 con azione se non verde.

## Formato output
```markdown
## System Health — {YYYY-MM-DD}

| Check | Esito | Dettaglio / azione |
|---|---|---|
| secret-scan | 🟢 | — |
| link-lint | 🟡 | 2 path mancanti → fix o allowlist |
| acl-audit | 🟢 | — |
| snapshot freshness | 🟢 | ultimo: ieri 02:00 |
| publish pendenti | 🟡 | 3 file → /admin publish |
| … | | |

Verdetto: 🟢/🟡/🔴 — {sintesi 1 riga}
```

## Destinazione
Report in chat; se 🔴: `system/audits/health-{YYYY-MM-DD}.md` + blocco esplicito
("non chiudere la sessione finché…"). Commit solo se ci sono fix applicati.
