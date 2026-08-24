# CompanyOS

🇬🇧 [English version](README.md)

Sistema operativo aziendale AI — template pubblico riusabile.

**Il principio**: due piani. Questo repo git è il **cervello** (agenti, protocolli, guardrail,
config) e lo modifica solo l'admin. Il **corpo** è il folder Google Drive aziendale: lì lavorano
founder e collaboratori — ognuno col proprio Claude Code dentro la propria zona — e i permessi
sono le **ACL native di Drive**, non convenzioni.

→ Architettura completa: [ARCHITECTURE.md](ARCHITECTURE.md)
→ Setup iniziale (lingua, Drive, service account, persone): [bootstrap/README.md](bootstrap/README.md)

## Lingua

Alla prima sessione il sistema chiede la **lingua di lavoro** (italiano/inglese) e la salva in
`config/company.yaml → language`: governa le risposte, la lingua di generazione dei file md e
quale variante dei file di sistema viene presentata (base italiano, `.en.md` inglese). Si può
cambiare in qualsiasi momento dicendolo in chat. Dettagli: `os/protocols/language.md`.

## Mappa del repo

| Path | Cosa |
|---|---|
| `CLAUDE.md` | Kernel per le sessioni admin (questo repo) |
| `os/agents/` · `os/skills/` · `os/workflows/` · `os/protocols/` | Il sistema: agenti per funzione, skill, workflow cross-agente, protocolli (ogni file ha la variante inglese `.en.md`) |
| `zones/` | CLAUDE.md per zona Drive + contesto condiviso (pubblicati in sola lettura) |
| `config/` | Parametri d'istanza (`*.example.yaml` da copiare e compilare) |
| `company/` | Snapshot versionato delle zone operative Drive (il master è Drive) |
| `vault/` | 🔴 finance & legal & contratti — solo admin |
| `tools/osctl/` | Sync engine git ↔ Drive (bootstrap, publish, snapshot, acl-audit) |
| `tools/viewer/` | Lettore markdown standalone per chi lavora nel folder Drive |
| `scripts/audit/` | Guardrail meccanici (secret-scan, link-lint, frontmatter, health) — in CI e pre-commit |
| `system/` | CHANGELOG, learnings (LRN-XXX), wiki |

## Quotidiano

- **Admin**: sessione in questo repo → `/ceo start` … `/ceo close` (snapshot, wiki, push).
  Modifiche di sistema → changelog nello stesso commit → `osctl publish`.
- **Collaboratore**: apre Claude Code nella propria cartella Drive (es. `10-Commerciale/`):
  il CLAUDE.md di zona lo configura da solo. Scrive solo dove la ACL glielo permette;
  l'attivazione è progressiva, zona per zona (`os/protocols/onboarding-collaborator.md`).
- **Lettura senza Claude**: i deliverable sono pubblicati anche come Google Doc;
  il viewer (`_OS/viewer.html`) naviga tutti i `.md` della cartella aziendale.

## Come si istanzia

1. Clona il repo (privato) per la tua azienda
2. Apri Claude Code nella root e lancia `/admin setup`: l'intervista iniziale chiede lingua,
   identità azienda, persone e strumenti → compila `config/*.yaml` dai `*.example.yaml`
3. Segui [bootstrap/README.md](bootstrap/README.md): Shared Drive, service account,
   `osctl bootstrap`, onboarding progressivo delle persone

## Template

Un'istanza privata popola `config/`, `company/`, `vault/`, `zones/*/context/` con i propri
dati; `/admin export-template` rigenera questo template da un'istanza (config e dati svuotati,
leak-scan automatico).
