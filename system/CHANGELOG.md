# Changelog — CompanyOS

Ogni modifica ai file di sistema (`os/`, `zones/`, `config/`, `CLAUDE.md`, `tools/`) richiede
una entry qui nello stesso commit. Categorie: `feat` / `change` / `fix` / `breaking` / `refactor`.
Semver. Dopo il merge di una modifica di sistema → `osctl publish` per distribuirla su Drive.

## [0.4.0] — feat: bonifica pre-pubblicazione + validazione degli slug

Un audit pre-pubblicazione ha mostrato che la sanificazione dell'export era **lessicale, non
semantica**: toglieva i nomi propri che aveva in lista, e si fermava lì. Quello che restava non
era un segreto, ma bastava a ricostruire l'azienda sorgente.

- fix(privacy): rimosso `toni@dna.fi` da `os/protocols/external-writes.md` (+ `.en.md`). Era un
  **indirizzo email funzionante di una persona reale** presso un cliente telco, con nome e
  riferimento a un artefatto di trattativa. Dato personale di un terzo, in un repo pubblico.
- fix(privacy): i 6 ticket `CYB-123`/`CYB-456` → `TASK-…`. `CYB-` è il prefisso ClickUp
  dell'istanza sorgente: una impronta digitale del workspace, corta ma cercabile.
- fix(privacy): il verticale dell'istanza sorgente (ISP Tier-2 / MSP / Telco / TIC, NIS2 come
  driver di domanda) era cablato in 22 coppie di file. Ora è parametrizzato su
  `config/company.yaml`, seguendo il modello che `os/agents/AGENTS.md` già usava. NIS2
  sopravvive come *esempio* di driver regolatorio, non come il driver del lettore.
- fix(privacy): rimosse le affermazioni in prima persona sul settore ("Vendiamo cybersecurity",
  "siamo B2B2B", "dati scan PMI"). Un template generico non può dire al lettore in che mercato
  è. La guida operativa è conservata, riscritta come condizionale che punta a
  `zones/_root/context/COMPANY.md`.
- fix(convention): i 24 esempi con slug `[cfo]` e `[pm]` → `[finance]` e `[product]`. Quei due
  agenti **non esistono in questo roster**: erano dell'istanza sorgente, e insegnavano
  all'adottante a violare la convenzione del repo in cui scrive.
- feat(audit): `scripts/audit/convention-check.py` — è il guardrail che avrebbe intercettato la
  riga sopra. Deriva il roster da `os/agents/*/` (nessuna lista da mantenere a mano) e verifica
  ogni `[slug]` negli esempi di commit. **Bloccante in CI.**
- fix(privacy): rimossi i riferimenti a `DEC-005` e a un audit interno del 2026-07-03, entrambi
  eventi dell'azienda sorgente citati in path che qui non esistono.

## [0.3.0] — feat: la parità IT/EN diventa un guardrail meccanico

Il layer bilingue esisteva senza nulla che ne verificasse la tenuta: una traduzione poteva
mancare, restare orfana o descrivere un comportamento superato, e niente lo segnalava. In un
template pubblico è il difetto peggiore, perché non rompe niente: l'utente anglofono legge
semplicemente istruzioni sbagliate.

- feat(audit): `scripts/audit/i18n-parity.py` — verifica tre difetti: **MISSING** (file base
  italiano senza variante), **ORPHAN** (variante senza file base), **STALE** (base modificato
  dopo la sua traduzione). La freschezza si misura sul timestamp dell'ultimo commit, non
  sull'mtime, che dopo un clone non dice niente. Legge anche i file non ancora committati, così
  dice la verità sul working tree. Allowlist in `scripts/audit/i18n-parity-allow.txt` per i file
  già in inglese (`README.md`, i reference della skill writing) e i README di cartella.
- feat(ci): `.github/workflows/audit.yml` — il check è **bloccante** accanto a secret-scan e
  link-lint. Richiede `fetch-depth: 0`, già presente.
- feat(i18n): aggiunto `CLAUDE.en.md`. Il kernel, cioè il file più importante del repo, era
  l'unico file di sistema italiano senza variante inglese: con `language: en` un adottante
  riceveva il kernel in italiano, in silenzio. Ora le coppie sono 142 e il check è verde.
- fix(agents): `os/agents/admin/commands/export-template.md` — l'export dichiarava una
  derivazione "meccanica" dall'istanza privata, ma una copia secca di `os/` **cancellerebbe il
  layer `.en.md`**, che vive solo qui e non nell'istanza sorgente. Il passo 2 ora dice che
  l'export è un **merge**: i file base si sovrascrivono, le varianti non si cancellano mai, e
  una variante il cui base è cambiato va ritradotta **prima** del push. Il passo 4 lo verifica
  con `i18n-parity.py --strict`.
- fix(cleanup): rimosso `os/skills/gmail/commands/test.md`, che conteneva la sola parola "test".
- fix(privacy): `CLAUDE.md` usava un cliente reale dell'istanza sorgente come esempio nel
  formato di commit → sostituito con `{cliente}`.
- Guardrail dei rituali aggiornati (close + session-rituals, IT ed EN) per includere il check.

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
