# CompanyOS Bootstrap — founder's guide

Steps to take the system from zero to operational: Shared Drive provisioned,
ACLs set, collaborators onboarded, guardrails active. References:
`ARCHITECTURE.md`, `tools/osctl/README.md`.

## 0. Configure the instance (initial interview)

Open Claude Code in the repo root and ask it to configure the instance: it will run
the initial interview (**working language** — Italian or English, then company identity,
people, zones) and fill in `config/*.yaml` from the `config/*.example.yaml` copies.
The chosen language governs replies, file generation and which variant of the system files
is presented/published (`os/protocols/language.md`); you can change it at any time
by saying so in chat.

## 1. Create the "Company HQ" Shared Drive

1. Google Drive (Workspace admin account) → **Shared drives** → **New**
2. Name: **Company HQ**
3. Copy the Shared Drive **ID** from the URL
   (`https://drive.google.com/drive/folders/<THIS-ID>`)
4. Paste it into `config/acl.yaml` → `drive.root_id`

> Do not create the subfolders by hand: `osctl bootstrap` creates them from `config/acl.yaml`.

## 2. Create the service account and share it

1. [Google Cloud Console](https://console.cloud.google.com) → company project →
   **APIs & Services** → enable the **Google Drive API**
2. **IAM & Admin → Service accounts → Create**: name `company-osctl`
3. **Keys → Add key → JSON** → save the file OUTSIDE the repo
   (e.g. `~/.keys/company-sa.json`)
4. Go back to the Shared Drive → **Manage members** → add the service account's
   email (`company-osctl@...iam.gserviceaccount.com`) as **Content manager**
   (also needed to manage permissions via `osctl`)

```bash
pip install google-api-python-client google-auth pyyaml
export GDRIVE_SA_KEY_PATH=~/.keys/company-sa.json
```

## 3. Verify the config and run the bootstrap

```bash
python3 tools/osctl/osctl.py status              # config readable? emails present?
python3 tools/osctl/osctl.py bootstrap           # DRY-RUN: folder + ACL plan
python3 tools/osctl/osctl.py bootstrap --apply   # creates folders, sets ACLs,
                                                 # writes the drive_ids into config/acl.yaml
git add config/acl.yaml && git commit -m "[admin] bootstrap: drive_id compilati"
```

⚠️ If `status` reports people **without an email** in `config/people.yaml`, add them
before running `--apply`: without an email the person is skipped in the ACLs.

Then publish the system (zone CLAUDE.md files, agents, protocols, viewer):

```bash
python3 tools/osctl/osctl.py publish
```

## 4. Invite the people

Per-zone ACLs are set by `osctl` (bootstrap / `acl-audit --fix --apply`): do not
assign permissions by hand from the folders. You only need to make sure everyone has
a Google account with the email declared in `config/people.yaml`. To verify
the result:

```bash
python3 tools/osctl/osctl.py acl-audit
```

## 5. Google Drive for Desktop for collaborators

Each collaborator installs [Google Drive for Desktop](https://www.google.com/drive/download/)
and syncs the Shared Drive. They will only see the zones their ACL grants access to.
To read documents without installing anything: open `_OS/viewer.html` in
Chrome/Edge → "Open company folder" → select `Company HQ`.

## 6. Claude Code in the zone

The collaborator opens Claude Code **inside their own zone** of the synced Drive
folder (e.g. `Company HQ/10-Commerciale/`): the `CLAUDE.md` published there
configures identity, default agent and output rules. The `_OS/` files are
read-only: they must not be modified (system changes go through git, admin only).

## 7. Enable the pre-commit hook (whoever works on the repo)

```bash
git config core.hooksPath scripts/hooks
```

From that moment every commit goes through `secret-scan --staged`: tokens/keys anywhere
and 🔴 files outside `vault/` and `company/clienti/*/contratti/` block the commit.

## 8. Enable the nightly snapshot

1. GitHub → repo → **Settings → Secrets and variables → Actions → New repository secret**
2. Name: `GDRIVE_SA_KEY` — value: **the content** of the service account key JSON
3. The `.github/workflows/snapshot.yml` workflow (03:00 UTC, or manually from Actions →
   *nightly-snapshot* → Run workflow) will download the Drive-master zones into `company/`
   and commit `[snapshot] drive: YYYY-MM-DD` if there are differences.

> The `finance` zone (`snapshot_target: vault`) does NOT go into the shared repo: the
> finance snapshot is run from the admin's clone, where `vault/` is mounted.

## Final checklist

- [ ] `drive.root_id` filled in and committed
- [ ] `osctl bootstrap --apply` run without email warnings
- [ ] `osctl publish` run (CLAUDE.md + `_OS/` + viewer on Drive)
- [ ] `osctl acl-audit` green
- [ ] Collaborators invited + Drive for Desktop installed
- [ ] `git config core.hooksPath scripts/hooks` on every clone
- [ ] `GDRIVE_SA_KEY` secret added → nightly snapshot active
