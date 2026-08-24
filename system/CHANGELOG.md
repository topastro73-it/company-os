# Changelog — CompanyOS

Ogni modifica ai file di sistema (`os/`, `zones/`, `config/`, `CLAUDE.md`, `tools/`) richiede
una entry qui nello stesso commit. Categorie: `feat` / `change` / `fix` / `breaking` / `refactor`.
Semver. Dopo il merge di una modifica di sistema → `osctl publish` per distribuirla su Drive.

## [0.2.1] — fix: la scrittura del cadence log passa da `start` a `close`

- fix(agents): `os/agents/ceo/commands/close.md` — nuovo passo 3 **Cadence log**, obbligatorio quanto
  la wiki di sessione. Prima l'aggiornamento di `direzione/ceo-cadence.md` era specificato **solo** nel
  passo 7 di `/ceo start`, cioè in mezzo al briefing: se la sessione proseguiva su altro, la scrittura
  saltava in silenzio e il cadence log diventava una falsa fonte di verità per tutte le sessioni
  successive che lo leggevano. Passi 3-9 rinumerati a 4-10.
- fix(agents): `os/agents/ceo/commands/start.md` — nuovo passo 2 **Cadence freshness check**, il
  controllo inverso dello stale session detector: se la wiki più recente è avanti di oltre 5 giorni
  rispetto al cadence log, il log è stale e si propone il riallineamento. Il passo 1 rileva la sessione
  senza wiki, il passo 2 la wiki senza cadence. Passi 2-8 rinumerati a 3-9; il passo 8 (ex 7) dichiara
  di non essere più l'unico punto di scrittura.
- fix(protocols): `os/protocols/session-rituals.md` — stessi due innesti nel rituale admin (START e
  CLOSE), più una regola comune: una scrittura obbligatoria non vive dentro un'interazione lunga.
- Varianti `.en.md` aggiornate in parallelo per tutti e tre i file.
- **Nota di zona**: `direzione` è `drive_master`, quindi il cadence log si scrive **sul Drive**, mai
  sullo snapshot `company/direzione/` (regola kernel §5). I passi nuovi lo dicono esplicitamente.
- Richiede `osctl publish` per distribuire su Drive.

## [0.2.0] — feat: bilingue IT/EN + protocollo lingua

- feat(protocols): `os/protocols/language.md` — lingua scelta nell'intervista iniziale
  (`config/company.yaml → language`), governa risposte, generazione md e variante dei file
  di sistema presentata/pubblicata; cambiabile in qualsiasi momento in chat
- feat(i18n): variante inglese `.en.md` accanto a ogni file di sistema (agenti, skill,
  protocolli, workflow, zone, context, bootstrap, ARCHITECTURE, system) — 142 file
- feat(osctl): `Config.language` + selezione variante in publish (con `en` i file di
  sistema vanno su Drive in inglese); fallback ai `*.example.yaml` su clone fresco
- feat(docs): `README.md` in inglese (primario) + `README.it.md`
- fix: refuso path `system/system/wiki` in opportunity-management

## [0.1.0] — template iniziale — feat: CompanyOS

Sistema operativo aziendale AI, template pubblico riusabile.

- Architettura a due piani: repo git = master del sistema (agenti, protocolli, guardrail,
  config); Google Drive = master operativo con ACL native per zona.
- 10 agenti (ceo, cos, sales, delivery, product, cto, finance, compliance, marketing, admin),
  skill curate, protocolli, workflow.
- `osctl`: bootstrap / publish / snapshot / acl-audit (git ↔ Drive).
- Viewer markdown standalone; guardrail meccanici (secret-scan, link-lint, frontmatter, health)
  in CI e pre-commit.
- Onboarding progressivo dei collaboratori (una zona alla volta, via intervista).
