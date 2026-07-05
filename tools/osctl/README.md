# osctl — sync engine CompanyOS

CLI Python che tiene allineati i due piani del sistema (ARCHITECTURE.md §4):

- **Sistema** (agenti, protocolli, CLAUDE.md di zona) — master **git** → pubblicato su Drive
- **Operativo** (clienti, pipeline, finance…) — master **Drive** → fotografato in git

Fonte di verità: `config/acl.yaml` (zone, ACL, direzione di sync) + `config/people.yaml`
(persone → email). Mai two-way sullo stesso file: ogni file ha un solo master.

## Setup

1. **Service account Google**
   - Google Cloud Console → crea un progetto (o usa quello aziendale)
   - Abilita la **Google Drive API**
   - Crea un **service account** e scarica la chiave JSON
   - Scope usato: `https://www.googleapis.com/auth/drive`

2. **Shared Drive**
   - Crea lo Shared Drive **"Company HQ"** (Google Workspace admin)
   - Aggiungi il service account (l'email `...@...iam.gserviceaccount.com`)
     come **Content manager** (o Manager, serve per gestire i permessi)
   - Copia l'ID dello Shared Drive (dall'URL) in `config/acl.yaml` → `drive.root_id`

3. **Dipendenze e chiave**

   ```bash
   pip install google-api-python-client google-auth pyyaml
   export GDRIVE_SA_KEY_PATH=/percorso/sicuro/sa-key.json   # MAI dentro il repo
   ```

   Senza `google-api-python-client` funzionano comunque `osctl status` e i parser
   di config; i comandi che toccano Drive falliscono con messaggio d'installazione.

## Comandi

```bash
python3 tools/osctl/osctl.py status                  # stato config/env, sempre disponibile
python3 tools/osctl/osctl.py bootstrap               # DRY-RUN: piano cartelle + ACL
python3 tools/osctl/osctl.py bootstrap --apply       # crea l'albero Drive, imposta le ACL,
                                                     # scrive i drive_id in config/acl.yaml
python3 tools/osctl/osctl.py publish                 # git → Drive (sistema + company seed)
python3 tools/osctl/osctl.py publish --dry-run
python3 tools/osctl/osctl.py snapshot                # Drive → git (company/, vault/finance/)
python3 tools/osctl/osctl.py acl-audit               # drift permessi (exit 1 se critico)
python3 tools/osctl/osctl.py acl-audit --fix         # correzioni in DRY-RUN
python3 tools/osctl/osctl.py acl-audit --fix --apply # applica le correzioni
```

Note operative:

- `bootstrap` è **idempotente**: cartelle e permessi già esistenti non vengono duplicati.
- `publish` converte in **Google Doc** i `.md` con frontmatter `render: gdoc` o con
  `type:` incluso in `publish.gdoc_default_for` (acl.yaml).
- `snapshot` **non committa**: scrive `company/.snapshot-manifest.json` e stampa il diff;
  il commit (`[snapshot] drive: YYYY-MM-DD`) spetta al chiamante (Action nightly o `/close`).
- La zona `finance` ha `snapshot_target: vault` → finisce in `vault/finance/`
  (repo privato dell'admin, mai nel repo condiviso).

## Nightly (GitHub Action)

`.github/workflows/snapshot.yml` esegue lo snapshot ogni notte alle 03:00 UTC e
committa se ci sono differenze. Per attivarlo: aggiungi il secret `GDRIVE_SA_KEY`
(contenuto JSON della chiave del service account) nelle impostazioni del repo.

In alternativa, cron locale sull'ambiente dell'admin:

```cron
0 3 * * * cd /path/company-os && GDRIVE_SA_KEY_PATH=$HOME/.keys/sa.json \
  python3 tools/osctl/osctl.py snapshot && git add company vault && \
  git commit -m "[snapshot] drive: $(date +\%F)" && git push
```

## ACL: come vengono risolte

- `write:`/`read:` in acl.yaml elencano chiavi persona di people.yaml o ruoli speciali:
  `admin` (chiavi sotto `admin:`), `all_internal` (`type: internal`), `everyone` (tutti).
- Ogni persona è risolta nella **prima email** del campo `emails:`; chi non ha email
  viene **saltato con warning** (aggiungi l'email a people.yaml prima del bootstrap).
- Zone `git_to_drive` (`_os`, `shared`): su Drive tutti sono **reader** — si scrive solo via git.
