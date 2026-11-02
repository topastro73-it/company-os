---
status: attivo
area: sistema
---

# Command: meeting-prep

## Trigger
"preparami la call con…", "brief per il meeting", "chi c'è alla riunione", o prima di un meeting
in un run schedulato.

## Scopo
Preparare la persona a un meeting: chi c'è, di quale account o progetto si parla, cosa è stato
promesso l'ultima volta e se è stato fatto, cosa chiudere oggi. Per un brief con agenda a slot
e possibili outcome c'è `/cos prepare-meeting`. Fonti e regole in `../SKILL.md`.

## Processo
1. **Trova il meeting** — quello che la persona nomina, dal Calendar (titolo, ora, partecipanti).
   Più candidati → chiedi quale. Mai indovinare.
2. **Partecipanti** — interni da `config/people.yaml` (ruolo); esterni dalla scheda account e
   dalle tabelle "Partecipanti" delle minute precedenti. Sconosciuti: dillo.
3. **Account / progetto** — `company/clienti/{slug}/overview.md`, le opportunità con
   `account: {slug}` (stage, `next-step`, `blockers`), o il progetto `P-NNN`.
4. **L'ultima volta** — la minuta più recente con lo stesso account o le stesse persone: decisioni,
   impegni, "Promesse fatte a terzi". Cerca sempre anche tra le trascrizioni delle fonti configurate
   (`../SKILL.md` § Transcript, parola chiave = account o partecipanti): un meeting più recente
   non ancora importato conta, e va segnalato ("trascrizione del gg/mm senza minuta").
5. **Promesse mantenute?** — per ogni impegno: stato nella minuta, aggiornamenti successivi
   (opportunità, minute più nuove, `git log`), task ClickUp collegati. ✓ fatto / ✗ aperto / ? non verificabile.
6. **Decisioni e regole che valgono** — decisioni in `company/direzione/decisions/` e regole di
   canale/pricing che toccano l'account (es. cosa si può mostrare, cosa non promettere).
7. **Ultime email** (skill gmail) — ultimi thread coi partecipanti e cosa aspetta risposta.

## Output
**Chi** (una riga a testa) · **Di cosa si parla** (account, stage, cosa serve) · **L'ultima volta**
(data, decisioni, impegni ✓/✗) · **Ultime email** · **Attenzione** (regole e rischi aperti) ·
**Da chiudere oggi** (2–4 punti da spingere). Leggibile in due minuti, ogni fatto col suo path.

## Destinazione
Su richiesta: `company/commerciale/meeting-prep/YYYY-MM-DD-{slug}-brief.md` (prospect) o
`company/clienti/{slug}/report/YYYY-MM-DD-{slug}-brief.md` (cliente), frontmatter
`status: attivo`, `area`, `zone`, `tier`, `account`, `date`.
