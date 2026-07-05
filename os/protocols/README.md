# Protocolli — indice

I protocolli definiscono *come* il sistema opera. Il kernel (`CLAUDE.md`) definisce le regole
non negoziabili; qui c'è il dettaglio operativo. Ogni protocollo è auto-contenuto e max 120 righe.

| Protocollo | Cosa regola |
|---|---|
| [zones-and-permissions.md](zones-and-permissions.md) | Zone, ACL Drive, sottozone ristrette, tier 🔴🟡🟢, regole PII, graceful degradation |
| [sync.md](sync.md) | Ciclo di vita dei file tra git e Drive: publish, snapshot, master unico, conflitti, Google Doc |
| [external-writes.md](external-writes.md) | PREPARE → APPROVE → EXECUTE per ogni scrittura su sistemi esterni (ClickUp, HubSpot, Gmail, publish a terzi) |
| [memory.md](memory.md) | Memoria a tre strati: stato nelle zone, storia in `system/wiki/`, regole in `system/learnings.md` |
| [spec-lifecycle.md](spec-lifecycle.md) | Stati delle spec prodotto, regole in-development/shipped, reconciliation, status-check |
| [decisions.md](decisions.md) | Formato e ciclo di vita delle decisioni (immutabili, zona direzione) |
| [changelog.md](changelog.md) | Entry in `system/CHANGELOG.md` per ogni modifica di sistema, semver, checkpoint, rollback, publish |
| [session-rituals.md](session-rituals.md) | Routine di start e close, per admin (repo) e collaboratori (zona Drive) |
| [onboarding-collaborator.md](onboarding-collaborator.md) | Attivazione progressiva (per zona, via intervista) dei collaboratori sul Drive operativo |
| [language.md](language.md) | Lingua operativa: scelta al setup, generazione md, varianti `.en.md`, cambio in chat |

Workflow cross-agente in `os/workflows/` (indice in `os/workflows/README.md`).
I file di sistema hanno varianti inglesi `.en.md` accanto (vedi language.md).
