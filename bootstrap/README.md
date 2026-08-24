# Bootstrap CompanyOS — guida per il founder

Passi per portare il sistema da zero a operativo: Shared Drive provisionato,
ACL impostate, collaboratori a bordo, guardrail attivi. Riferimenti:
`ARCHITECTURE.md`, `tools/osctl/README.md`.

## 0. Configura l'istanza (intervista iniziale)

Apri Claude Code nella root del repo e lancia **`/admin setup`**: è l'intervista
iniziale (**lingua di lavoro** — italiano o inglese, poi identità azienda, persone,
strumenti, zone) e compila `config/*.yaml` dalle copie di `config/*.example.yaml`.
La lingua scelta governa risposte, generazione dei file e la variante dei file di sistema
presentata/pubblicata (`os/protocols/language.md`); potrai cambiarla in qualsiasi momento
dicendolo in chat.

## 1. Crea lo Shared Drive "Company HQ"

1. Google Drive (account Workspace admin) → **Drive condivisi** → **Nuovo**
2. Nome: **Company HQ**
3. Copia l'**ID** dello Shared Drive dall'URL
   (`https://drive.google.com/drive/folders/<QUESTO-ID>`)
4. Incollalo in `config/acl.yaml` → `drive.root_id`

> Non creare le sottocartelle a mano: le crea `osctl bootstrap` da `config/acl.yaml`.

## 2. Crea il service account e condividilo

1. [Google Cloud Console](https://console.cloud.google.com) → progetto aziendale →
   **API e servizi** → abilita **Google Drive API**
2. **IAM e amministrazione → Service account → Crea**: nome `company-osctl`
3. **Chiavi → Aggiungi chiave → JSON** → salva il file FUORI dal repo
   (es. `~/.keys/company-sa.json`)
4. Torna sullo Shared Drive → **Gestisci membri** → aggiungi l'email del service
   account (`company-osctl@...iam.gserviceaccount.com`) come **Content manager**
   (serve anche per gestire i permessi via `osctl`)

```bash
pip install google-api-python-client google-auth pyyaml
export GDRIVE_SA_KEY_PATH=~/.keys/company-sa.json
```

## 3. Verifica la config e lancia il bootstrap

```bash
python3 tools/osctl/osctl.py status              # config leggibile? email presenti?
python3 tools/osctl/osctl.py bootstrap           # DRY-RUN: piano cartelle + ACL
python3 tools/osctl/osctl.py bootstrap --apply   # crea cartelle, imposta ACL,
                                                 # scrive i drive_id in config/acl.yaml
git add config/acl.yaml && git commit -m "[admin] bootstrap: drive_id compilati"
```

⚠️ Se `status` segnala persone **senza email** in `config/people.yaml`, aggiungile
prima del `--apply`: senza email la persona viene saltata nelle ACL.

Poi pubblica il sistema (CLAUDE.md di zona, agenti, protocolli, viewer):

```bash
python3 tools/osctl/osctl.py publish
```

## 4. Invita le persone

Le ACL per zona le imposta `osctl` (bootstrap / `acl-audit --fix --apply`): non
assegnare permessi a mano dalle cartelle. Devi solo assicurarti che ognuno abbia
un account Google con l'email dichiarata in `config/people.yaml`. Per verificare
il risultato:

```bash
python3 tools/osctl/osctl.py acl-audit
```

## 5. Google Drive for Desktop per i collaboratori

Ogni collaboratore installa [Google Drive for Desktop](https://www.google.com/drive/download/)
e sincronizza lo Shared Drive. Vedrà solo le zone a cui la sua ACL dà accesso.
Per leggere i documenti senza installare nulla: apri `_OS/viewer.html` in
Chrome/Edge → "Apri cartella aziendale" → seleziona `Company HQ`.

## 6. Claude Code nella zona

Il collaboratore apre Claude Code **dentro la propria zona** del folder Drive
sincronizzato (es. `Company HQ/10-Commerciale/`): il `CLAUDE.md` pubblicato
lì configura identità, agente di default e output rules. I file `_OS/` sono in
sola lettura: non vanno modificati (le modifiche di sistema passano da git, solo admin).

## 7. Attiva il pre-commit hook (chi lavora sul repo)

```bash
git config core.hooksPath scripts/hooks
```

Da quel momento ogni commit passa da `secret-scan --staged`: token/chiavi ovunque
e file 🔴 fuori da `vault/` e `company/clienti/*/contratti/` bloccano il commit.

## 8. Attiva lo snapshot nightly

1. GitHub → repo → **Settings → Secrets and variables → Actions → New repository secret**
2. Nome: `GDRIVE_SA_KEY` — valore: **il contenuto** del JSON della chiave del service account
3. Il workflow `.github/workflows/snapshot.yml` (03:00 UTC, o manuale da Actions →
   *nightly-snapshot* → Run workflow) scaricherà le zone Drive-master in `company/`
   e committerà `[snapshot] drive: YYYY-MM-DD` se ci sono differenze.

> La zona `finance` (`snapshot_target: vault`) NON va nel repo condiviso: lo
> snapshot finance si esegue dal clone dell'admin, dove `vault/` è montata.

## Checklist finale

- [ ] `drive.root_id` compilato e committato
- [ ] `osctl bootstrap --apply` eseguito senza warning email
- [ ] `osctl publish` eseguito (CLAUDE.md + `_OS/` + viewer su Drive)
- [ ] `osctl acl-audit` verde
- [ ] Collaboratori invitati + Drive for Desktop installato
- [ ] `git config core.hooksPath scripts/hooks` su ogni clone
- [ ] Secret `GDRIVE_SA_KEY` aggiunto → snapshot nightly attivo
