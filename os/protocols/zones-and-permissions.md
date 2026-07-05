# Zone e permessi

Il modello di accesso ha due componenti ortogonali:
- **Zona** = *dove vive* il file e *chi lo vede* → decisa dall'ACL Drive (`config/acl.yaml`)
- **Tier** 🔴🟡🟢 = *quanto è sensibile il contenuto* → decide publish esterni, redazione PII, secret-scan

## 1. Ogni file ha una zona

Ogni file operativo dichiara la propria zona nel frontmatter:

```yaml
---
zone: clienti          # _os | direzione | commerciale | clienti | prodotto | finance | compliance | marketing | shared
tier: 🟡               # 🔴 restricted | 🟡 internal (default) | 🟢 public
---
```

`scripts/audit/frontmatter-check.py` verifica che ogni file operativo dichiari zona e tier.
Un file senza `zone:` va trattato come appartenente alla zona della cartella in cui si trova;
un file senza `tier:` è 🟡 INTERNAL per default.

## 2. L'accesso lo decide l'ACL Drive

Il sistema **non ha un proprio livello di permessi**: chi può leggere/scrivere un file è
determinato dall'ACL della cartella Drive della zona, come da matrice in `config/acl.yaml`.
Se una persona non ha accesso alla cartella, non vede quei file — non serve altro.
`osctl acl-audit` confronta i permessi reali con la matrice e segnala il drift.

Conseguenze operative per l'agente:
- Scrivi ogni output **solo nella zona pertinente** (mai output di un cliente fuori da `20-Clienti/{slug}/`)
- Non copiare contenuti da una zona ristretta a una più larga (es. da `40-Finance/` a `30-Prodotto/`)
- Non aggirare mai l'ACL "per comodità" (es. duplicare un contratto in `90-Condivisi/`)

## 3. Per-folder ACL su 20-Clienti

`20-Clienti/` ha `per_folder_acl: true`: ogni cartella cliente `20-Clienti/{slug}/` ha la
propria ACL — la vede solo chi segue quel cliente (owner + team assegnato). Alla creazione
di una nuova cartella cliente:
1. Applica l'ACL di default della zona (`write:` in `acl.yaml`)
2. Assegna un **owner** esplicito (persona che segue il cliente)
3. Restringi ai soli coinvolti; `osctl acl-audit` segnala cartelle cliente senza owner

## 4. Sottozone ristrette (solo quando AGGIUNGONO accesso, mai quando lo tolgono)

Google Drive eredita i permessi solo verso il basso: chi ha accesso a una cartella lo eredita
in ogni sua sottocartella, e non esiste un modo nativo di restringerlo più in profondità.
Una "sottozona ristretta" in `acl.yaml` funziona **solo** se aggiunge persone in più rispetto
alla cartella madre (che magari non ha nessun accesso, es. finance); non puoi usarla per
*togliere* accesso a chi già ce l'ha sopra.

| Sottozona | Path | Accesso | Contenuto |
|---|---|---|---|
| Commercialista | `40-Finance/per-commercialista/` | write: il founder · read: + studio | Vetrina one-way per lo studio fiscale |
| Bandi | `40-Finance/bandi/` | il founder + consulente bandi | Rendicontazioni, documenti di progetto |
| Evidence audit | `50-Compliance/evidence/` | write: il founder · read: interni + auditor | Evidenze per l'ente di certificazione |

Queste funzionano perché la zona madre (`finance`, `compliance`) è già più ristretta di chi
viene aggiunto in profondità: nessuno perde permessi, si aggiunge solo un lettore in più.

**Contratti cliente**: NON è una sottozona di `20-Clienti/{slug}/` — chi lavora sul cliente
(delivery, CS) ha già accesso più ampio della cartella madre, quindi non si può restringere
sotto di essa. Vive nella zona separata e top-level `contratti` (`70-Contratti-Riservati/{slug}/`,
write: il founder · read: il founder, Head of Sales). Nella cartella cliente resta solo `contratti/README.md`
con il puntatore. Regola generale: se una restrizione è più stretta della zona madre, serve una
zona top-level a parte, non una sottocartella.

## 5. Tier 🔴🟡🟢 — a cosa serve la classificazione

Il tier NON decide chi accede (quello è l'ACL): decide **cosa può uscire** e **come**.

| Tier | Contenuto tipico | Regole |
|---|---|---|
| 🔴 RESTRICTED | Contratti firmati, cap table, IBAN, CF/P.IVA, bilanci non pubblici, compensi | Vive solo in `40-Finance/`, `70-Contratti-Riservati/`, e in git solo in `vault/`. Mai pubblicato, mai citato in wiki/learnings/commit/briefing |
| 🟡 INTERNAL | Pipeline, metriche non pubblicate, roadmap, note partner, decisioni | Default. Publish verso terzi solo dopo redazione PII |
| 🟢 PUBLIC | Blog, battlecard pubblici, case study autorizzati, materiale onboarding | Pubblicabile ovunque |

Il tier alimenta tre meccanismi: (a) gate del **publish esterno** (mai 🔴, 🟡 solo redatto),
(b) **redazione PII** prima di ogni uscita, (c) `secret-scan.sh` che blocca in CI/pre-commit
token, IBAN e file 🔴 fuori dalle destinazioni ammesse.

## 6. Regole PII

- **Mai** IBAN, CF, P.IVA, numeri di carta, telefoni personali, compensi/salari in:
  `system/wiki/`, `system/learnings.md`, messaggi di commit, briefing, titoli di PR
- **Clienti finali** (i clienti dei nostri partner) in wiki e learnings: **iniziali + ruolo**
  (es. "M. Rossi, CISO Acme"), salvo entity page dedicata in `system/wiki/entities/clients/{slug}.md`
- Learnings: regole **astratte** ("quando un partner rallenta…"), mai personalizzate sul nome
- Screenshot con UI cliente: redact/blur prima di salvare fuori dalla cartella cliente

## 7. Graceful degradation — zona non accessibile

Se una zona non è raggiungibile (Drive non montato, ACL mancante, vault non presente sul clone):
1. **Segnala** subito quale zona manca e cosa non potrai fare
2. **Prosegui** con quello che hai: snapshot in `company/` (per l'admin), file della zona corrente
3. **Non bloccare** mai il lavoro in attesa della zona; non inventare i dati mancanti
4. Se l'output andrebbe nella zona mancante, salvalo in staging locale e segnala:
   "zona X non disponibile — file pronto, lo sposto al ripristino"
5. Vault non montato → gli agenti su dati 🔴 degradano: rispondono solo con dati 🟡 disponibili
