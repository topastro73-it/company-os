---
status: attivo
area: sistema
---

# Command: new-project

## Trigger
"apri il progetto…", "nuovo cliente", "nuova opportunità", "crea un progetto interno".

## Scopo
Creare il file giusto, dal suo template, nella zona giusta — passo per passo, con conferma prima
di scrivere. Fonti e regole in `../SKILL.md`.

## Passi
0. **Non creare doppioni** — cerca per nome e slug in `company/clienti/`,
   `company/commerciale/opportunities/` e `company/direzione/projects/INDEX.md`.
1. **Che cosa è** — chiedi se serve:
   - **account** (cliente o partner) → `company/clienti/{slug}/overview.md` da `company/clienti/TEMPLATE.md`;
   - **opportunità** (una trattativa) → `company/commerciale/opportunities/{opp-slug}.md` da
     `TEMPLATE.md` nella stessa cartella, con `account:` che punta all'account;
   - **progetto interno** → `company/direzione/projects/P-NNN-{slug}.md` col prossimo numero libero,
     più la riga in `INDEX.md`.
2. **Raccogli** i campi obbligatori del template (nome, slug kebab-case, owner da
   `config/people.yaml`, tipo/segmento, stage o status iniziale, next-step con scadenza). Mai
   inventare valori: i campi ignoti restano vuoti con un commento. Rimostra tutto e chiedi "ok?".
3. **Scrivi** il file con frontmatter completo (`zone`, `tier`, `status`, `area`), poi gli indici
   (`INDEX.md` della zona, `PIPELINE.md` per un'opportunità).
4. **Facoltativo** — lista ClickUp o task iniziali via `clickup-pending/`; record HubSpot via
   `hubspot-pending/`. Entrambi aspettano l'approvazione.
5. Commit `[{agente}] opportunity|delivery|admin: nuovo {tipo} {slug}`; in admin ricorda il publish.
