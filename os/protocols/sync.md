# Sync — ciclo di vita dei file tra git e Drive

Due piani, due master: il **sistema** vive in git, l'**operativo** vive su Drive.
`osctl` (in `tools/osctl/`) muove i file nella direzione dichiarata da `sync:` in `config/acl.yaml`.

## 1. Un solo master per file

Ogni file ha **un solo master**. Mai two-way sullo stesso file.

| Direzione | Zone | Master | L'altro lato è |
|---|---|---|---|
| `git_to_drive` (publish) | `_os`, `shared` | git | copia read-only su Drive |
| `drive_master` (snapshot) | direzione, commerciale, clienti, prodotto, finance, compliance, marketing | Drive | snapshot versionato in `company/` (finance → `vault/`) |

In sessione admin puoi editare lo snapshot `company/` **solo** se il file è git-master
o se subito dopo ripubblichi la modifica sul master Drive; altrimenti edita su Drive.

## 2. Publish (git → Drive)

`osctl publish` distribuisce il sistema sulle zone Drive:
- `zones/` → i `CLAUDE.md` di zona e il contesto (`_OS/`, root, `90-Condivisi/`)
- `os/` selezionati (agenti, protocolli, template) → `_OS/`
- `tools/viewer/viewer.html` → `_OS/`
- seed iniziali di `company/` al bootstrap

**Quando**: obbligatorio dopo ogni merge di una modifica di sistema (vedi
`os/protocols/changelog.md`); il collaboratore lavora sempre sull'ultima versione pubblicata.
Su Drive questi file sono **read-only**: nessuno li modifica lì — le modifiche passano da git.

## 3. Snapshot (Drive → git)

`osctl snapshot` scarica le zone Drive-master e committa:
- zone standard → `company/{zona}/` (es. `10-Commerciale/` → `company/commerciale/`)
- `40-Finance/` → `vault/finance/` (repo privato dell'admin, mai nel repo principale)
- commit: `[snapshot] drive: YYYY-MM-DD`

**Quando**:
- **Nightly** — GitHub Action con service account (backup e versioning completo anche dell'operativo)
- **Al `/close` admin** — così la sessione chiude con lo stato reale delle zone

Git resta il versioning e il backup di tutto, ma per le zone Drive-master è **copia**, non master.

## 4. Conflitti — il master vince

Se lo stesso file risulta modificato su entrambi i lati:
1. **Vince il master** della zona (Drive per le zone operative, git per `_os`/`shared`)
2. La versione perdente non si butta: salvala come `{nome}.conflict-YYYY-MM-DD.md`
   accanto allo snapshot e segnala all'admin nel summary del sync
3. Mai merge automatico tra i due lati: chi ha scritto sul lato sbagliato ri-applica a mano sul master

Prevenzione: non editare mai lo snapshot di una zona Drive-master se non sei in grado di
riportare subito la modifica su Drive.

## 5. Conversione Google Doc

I deliverable per umani vengono pubblicati **anche** come Google Doc nella stessa cartella,
così chiunque con accesso Drive li apre e commenta senza installare nulla. La conversione
scatta in publish quando:
- il frontmatter ha `render: gdoc`, **oppure**
- il frontmatter `type:` è tra i default di `config/acl.yaml` →
  `publish.gdoc_default_for: [report, proposta, qbr, investor-update]`

Regole:
- il `.md` resta il **source of truth**; il Google Doc è un artefatto rigenerabile
- edit sostanziali ricevuti come commenti sul Doc → si riportano nel `.md`, poi si ri-renderizza
- il Doc rigenerato **sovrascrive** il precedente (stesso file, stesso ID: i link non si rompono)

## 6. Se osctl non è disponibile

MCP/rete/credenziali assenti non bloccano il lavoro:
1. **Lavora sui file** che hai (snapshot `company/` per l'admin, cartella Drive locale per i collaboratori)
2. Segnala: "osctl non disponibile — modifiche locali pronte, sync al ripristino"
3. Le modifiche di sistema restano in git e si pubblicano al primo `osctl publish` utile
4. Al ripristino: prima `snapshot` (allinei lo stato), poi `publish` (distribuisci il sistema)
5. Nessuna operazione manuale su Drive che simuli il sync (rischio doppio master)
