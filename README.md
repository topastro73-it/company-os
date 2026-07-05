# CompanyOS

Sistema operativo aziendale AI — template pubblico OpenSource.

**Il principio**: due piani. Questo repo git è il **cervello** (agenti, protocolli, guardrail,
config) e lo modifica solo l'admin. Il **corpo** è il folder Google Drive aziendale: lì lavorano
founder e collaboratori — ognuno col proprio Claude Code dentro la propria zona — e i permessi
sono le **ACL native di Drive**, non convenzioni.

→ Architettura completa: [ARCHITECTURE.md](ARCHITECTURE.md)
→ Setup iniziale (Drive, service account, persone): [bootstrap/README.md](bootstrap/README.md)

## Mappa del repo

| Path | Cosa |
|---|---|
| `CLAUDE.md` | Kernel per le sessioni admin (questo repo) |
| `os/agents/` · `os/skills/` · `os/workflows/` · `os/protocols/` | Il sistema: agenti per funzione, skill, workflow cross-agente, protocolli |
| `zones/` | CLAUDE.md per zona Drive + contesto condiviso (pubblicati in sola lettura) |
| `config/` | Parametri d'istanza: azienda, persone, ACL zone, integrazioni |
| `company/` | Snapshot versionato delle zone operative Drive (il master è Drive) |
| `vault/` | 🔴 finance & legal — solo admin |
| `tools/osctl/` | Sync engine git ↔ Drive (bootstrap, publish, snapshot, acl-audit) |
| `tools/viewer/` | Lettore markdown standalone per chi lavora nel folder Drive |
| `scripts/audit/` | Guardrail meccanici (secret-scan, link-lint, frontmatter, health) — in CI e pre-commit |
| `system/` | CHANGELOG, learnings (LRN-XXX), wiki |

## Quotidiano

- **Admin**: sessione in questo repo → `/ceo start` … `/ceo close` (snapshot, wiki, push).
  Modifiche di sistema → changelog nello stesso commit → `osctl publish`.
- **Collaboratore**: apre Claude Code nella propria cartella Drive (es. `10-Commerciale/`):
  il CLAUDE.md di zona lo configura da solo. Scrive solo dove la ACL glielo permette.
- **Lettura senza Claude**: i deliverable sono pubblicati anche come Google Doc;
  il viewer (`_OS/viewer.html`) naviga tutti i `.md` della cartella aziendale.

## Template

Questo è il template pubblico **company-os**. Un'istanza privata lo popola con i propri dati
(`config/`, `company/`, `vault/`, `zones/*/context/`); `/admin export-template` rigenera il
template da un'istanza (config e dati svuotati, leak-scan automatico).
