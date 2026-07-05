# /admin onboard-person — Attivazione progressiva di un collaboratore

## Scopo
Attivare l'accesso Drive di una persona una zona alla volta, via intervista — non tutta
la matrice `acl.yaml` in un colpo solo. Protocollo completo: `os/protocols/onboarding-collaborator.md`.

## Input
Nome della persona (nuova o già in `config/people.yaml` con `onboarded: false`).

## Passi
1. **Intervista** (4 domande, in ordine — non presumere):
   - Chi è, che ruolo ha, tipo (internal/external), email dell'account Google che userà
   - A quali zone deve **scrivere**? (solo quelle necessarie al ruolo)
   - A quali zone deve **solo leggere**?
   - Che **agente di default**? (`sales`, `delivery`, `product`, `cto`, `finance`,
     `compliance`, `marketing`)
   - Se tocca `clienti`: quali cartelle cliente specifiche segue (mai tutta la zona
     senza motivo)
2. Aggiorna `config/people.yaml`: crea/aggiorna la voce, imposta `zones_write`/`zones_read`
   coerenti con le risposte, poi **`onboarded: true`**
3. Lancia `osctl bootstrap --apply` (additivo: concede solo i permessi nuovi di questa
   persona, non tocca gli altri)
4. Verifica `osctl acl-audit`: deve restare a 0 🔴 critici
5. Committa: `[admin] onboard: {nome} → {zone/i}`
6. Handoff alla persona: installare Google Drive for Desktop, sincronizzare "Company HQ",
   aprire Claude Code dentro la propria zona (il `CLAUDE.md` pubblicato la accoglie da solo)

## Formato output
```markdown
## Onboarding — {nome}
Ruolo: {ruolo} · Agente: {agente} · Zone scrittura: {zone} · Zone lettura: {zone}
Cartelle cliente assegnate: {slug, slug...} (se applicabile)

✓ config/people.yaml aggiornato (onboarded: true)
✓ osctl bootstrap --apply eseguito
✓ osctl acl-audit: 0 critici
```

## Destinazione
Commit su `config/people.yaml`. Nessun file separato — lo stato è la config stessa.
