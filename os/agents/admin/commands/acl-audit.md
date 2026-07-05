# /admin acl-audit — Audit permessi Drive

## Scopo
Verificare che i permessi Drive **reali** coincidano con la matrice `config/acl.yaml`.
Le ACL sono l'enforcement del sistema: il drift è una falla, non un dettaglio.

## Input
Nessuno. Cadenza: parte di `/admin health`; comunque dopo ogni cambio di persone o zone.

## Passi
1. Esegui `osctl acl-audit`: legge i permessi via Drive API per ogni zona e sottocartella
   e li confronta con `config/acl.yaml` + `config/people.yaml`.
2. **Rileva drift**:
   - persona con accesso in più (non in matrice) → 🔴 rimuovere
   - persona mancante (in matrice ma senza accesso) → 🟡 aggiungere
   - cartella cliente `20-Clienti/{slug}/` senza owner assegnato → 🟡
   - sottocartelle sensibili (`contratti/`, `per-commercialista/`, `evidence/`) con ACL
     più larga del previsto → 🔴
   - esterni (commercialista, auditor, consulente bandi) con accesso oltre la loro sottozona → 🔴
3. **Proponi i fix**: per ogni drift, l'azione Drive esatta. L'applicazione è una
   scrittura esterna → PREPARE → APPROVE → EXECUTE.
4. Se il drift è voluto (nuova persona, cliente assegnato) → aggiorna PRIMA
   `config/acl.yaml`/`people.yaml` (commit + changelog), poi applica.
5. Report datato; drift 🔴 su dati → segnala anche a `compliance`.

## Formato output
```markdown
## ACL Audit — {YYYY-MM-DD}
Zone verificate: {n} · Drift: {n} (🔴 {n} · 🟡 {n})

| Zona/cartella | Atteso | Reale | Drift | Fix proposto |
|---|---|---|---|---|
```

## Destinazione
Report in chat + `system/audits/acl-audit-{YYYY-MM-DD}.md` (git).
Commit: `[admin] system: acl-audit {YYYY-MM-DD}`.
