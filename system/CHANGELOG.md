# Changelog — CompanyOS

Ogni modifica ai file di sistema (`os/`, `zones/`, `config/`, `CLAUDE.md`, `tools/`) richiede
una entry qui nello stesso commit. Categorie: `feat` / `change` / `fix` / `breaking` / `refactor`.
Semver. Dopo il merge di una modifica di sistema → `osctl publish` per distribuirla su Drive.

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
