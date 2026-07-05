---
zone: _os
tier: 🟡
---

# Onboarding collaboratore — attivazione progressiva

Il Drive "Company HQ" parte con **solo l'admin** (il founder) su tutte le zone. Ogni
collaboratore viene attivato **una zona alla volta**, quando serve davvero, tramite
intervista — non c'è un rollout automatico della matrice completa.

## Quando si attiva

Il CEO dice all'admin: "onboarda [nome]" — oppure il bisogno emerge da solo
(es. "{persona} deve vedere la pipeline"). L'admin fa l'intervista, non presume.

## Intervista (4 domande, in ordine)

1. **Chi è e che ruolo ha?** (se non già in `config/people.yaml`, crealo: nome, ruolo, tipo
   internal/external, email — l'email deve corrispondere all'account Google che userà)
2. **A quali zone deve scrivere?** (`direzione`, `commerciale`, `clienti`, `prodotto`,
   `finance`, `compliance`, `marketing` — solo quelle strettamente necessarie al ruolo)
3. **A quali zone deve solo leggere?** (spesso più ampie delle zone di scrittura — es. Sales
   legge `prodotto` per sapere cosa arriva, ma non ci scrive)
4. **Che agente di default userà?** (`sales`, `delivery`, `product`, `cto`, `finance`,
   `compliance`, `marketing` — determina quale CLAUDE.md di zona lo accoglie)

Per i clienti (`20-Clienti/{slug}/`): l'accesso è **per cartella**, non per zona intera —
chiedi anche quali cartelle cliente specifiche deve seguire, non dare mai accesso a tutta
`20-Clienti` a meno che il ruolo lo richieda davvero (es. Head of Sales sì, un SDR su
territorio specifico no).

## Applicazione

1. Aggiorna `config/people.yaml`: campi `zones_write`/`zones_read` (se non già corretti) e
   **`onboarded: true`** (finché è `false`, la persona resta fuori dalla matrice — vedi
   commento in testa al file)
2. Lancia `osctl bootstrap --apply` (o `osctl acl-audit --fix --apply` quando disponibile):
   additivo, concede solo i permessi nuovi della persona appena attivata, non tocca nessun
   altro
3. Verifica con `osctl acl-audit`: deve restare a 0 🔴 critici
4. Committa `config/people.yaml` con messaggio `[admin] onboard: {nome} → {zone}`
5. Comunica alla persona: installa Google Drive for Desktop, sincronizza "Company HQ",
   apre Claude Code dentro la sua zona (il `CLAUDE.md` pubblicato la accoglie da solo)

## Disattivazione / cambio ruolo

Stesso principio in negativo: Drive **non permette di rimuovere permessi ereditati** da una
zona più ampia, quindi la revoca va fatta **sulla zona esatta** dove è stato dato l'accesso
(`osctl` chiama `remove_permission` sulla singola cartella). Se qualcuno cambia ruolo o esce,
aggiorna `zones_write`/`zones_read` in `people.yaml`, poi rimuovi manualmente su Drive (o con
un futuro comando `osctl revoke`) l'accesso alle zone non più dovute — impostare `onboarded:
false` NON basta da solo a togliere l'accesso già concesso, impedisce solo che venga
ri-concesso al prossimo bootstrap.

## Perché così (non tutto subito)

Attivare l'intera matrice `acl.yaml` in un colpo solo (come fa `osctl bootstrap --apply` di
default) concede a tutti l'accesso "a target" fin dal primo giorno — comodo ma rischioso: se
la matrice ha un errore di progettazione (vedi LRN-025, il caso dei contratti), lo si scopre
dopo che l'accesso è già stato dato. Onboardare una persona alla volta, con intervista,
riduce il raggio d'errore e forza a verificare ogni volta che l'accesso richiesto sia
davvero necessario.
