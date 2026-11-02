---
status: attivo
area: sistema
---

# Command: team-radar

## Trigger
"cosa sta facendo {persona}", "su cosa lavora {persona}", "cosa è successo questa settimana",
"novità in azienda", "team update". Sola lettura.

## Scopo
Tenere la persona aggiornata su cosa fanno gli altri e l'azienda. Per il digest completo per area
(pipeline, prodotto, finance) c'è `/cos weekly-digest`. Fonti e regole in `../SKILL.md`.
Rispetta le zone: in sessione non admin mostra solo ciò che la persona può leggere
(`config/acl.yaml`), e dillo se una lista sembra scarna.

## Una persona
1. **Chi** — `config/people.yaml` (nome, ruolo, `default_agent`); più corrispondenze → chiedi.
2. **Account e opportunità** — file dove è `owner-sales`/`owner-pm`, con stage e next-step.
3. **Progetti** — `company/direzione/projects/INDEX.md` (owner o supporto) e WO dove è `to:`.
4. **Meeting degli ultimi 7 giorni** — minute in cui compare tra i partecipanti, più le
   trascrizioni pertinenti delle fonti configurate col suo nome (`../SKILL.md` § Transcript), segnando quelle senza minuta.
5. **Impegni aperti** — righe delle minute e `blockers` con owner = la persona; task ClickUp
   assegnati (se ClickUp non risponde: non verificati).
6. **Decisioni** — dove compare come chi ha deciso, ultimi 14 giorni.

Output: **Account e progetti** (ruolo, stato) · **Meeting recenti** · **Impegni aperti**
(scaduti prima) · **Decisioni**.

## L'azienda
1. **Decisioni della settimana** — nuovi file in `company/direzione/decisions/` da lunedì.
2. **Meeting** — minute della settimana e trascrizioni pertinenti delle fonti configurate non ancora
   importate, per account; quelli senza account a parte. Dei meeting di altre aziende solo il conteggio.
3. **Movimento** — in admin `git log --since=<lunedì>` raggruppato per zona e agente; opportunità
   che hanno cambiato stage; blocker nuovi o chiusi.

Output: **Decisioni della settimana** · **Account in movimento** · **Bloccati / da attenzione** ·
**Chi ha fatto più meeting** (facoltativo, una riga). Con gli artifact, una pagina.

## Digest settimanale
Schedulalo il lunedì alle 08:30 col prompt **"cosa è successo la settimana scorsa"**.
