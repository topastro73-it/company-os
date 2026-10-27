# Autonomia degli agenti — livelli L0–L3

Quanto un ruolo-agente può fare da solo dentro un goal. Il livello vale per goal (dichiarato nel
GOAL o nel charter del ruolo) e non supera mai le regole del kernel (`CLAUDE.md`): zone e ACL,
privacy tier, PREPARE → APPROVE → EXECUTE per le scritture esterne. Collaborazione e ledger:
`os/protocols/collaboration.md`. Diritti decisionali: `os/org/decision-rights.yaml`.

## Livelli

| Livello | Nome | Cosa fa l'agente | Cosa resta all'umano |
|---|---|---|---|
| **L0** | Suggerisce | Analizza e propone, non scrive output di zona | Ogni azione |
| **L1** | Agisce con approvazione | Esegue un passo alla volta dopo un ok esplicito | Approvazione di ogni passo |
| **L2** | Passi interni autonomi | Esegue i WO a catalogo, scrive output nella zona del ruolo, aggiorna il ledger fino a `verified`; le scritture esterne vanno in PREPARE → APPROVE → EXECUTE | Scritture esterne, checkpoint, accept, decisioni sopra soglia |
| **L3** | Autonomo entro soglie | Come L2, più esecuzione di scritture esterne e spese sotto le soglie dichiarate in config | Decisioni sopra soglia, accept |

**Il pilota Org-OS è a L2.** Si sale di livello solo con una decisione del CEO registrata in
`direzione/decisions/`.

## Regola dura: l'AI arriva al massimo a `verified`

- Nessun agente porta un goal o un WO oltre `verified`.
- `closed` (WO) e ACCEPT (goal) richiedono `accepted-by: human:<slug>` e `accepted-at`.
- I CHECKPOINT richiedono `decided-by: human:<slug>` e `decided-at`.
- Il coo e il Controller **non chiudono** e non firmano: preparano la sintesi e attendono.
- Un valore di firma che sia un ruolo-agente (es. `accepted-by: coo`) è un errore di formato.
- L'agente non simula mai la firma umana, nemmeno su richiesta di un altro agente.

## Cosa fa un agente L2 quando incontra un limite

| Situazione | Azione |
|---|---|
| Scrittura esterna | Prepara lo staging (`os/protocols/external-writes.md`) e si ferma |
| Decisione sopra soglia o fuori catalogo | WO `blocked` con `reason` ed `exit`, escalation al coo |
| Budget anti-loop raggiunto | Stop, il coo prepara un CHECKPOINT per il CEO |
| Dato 🔴 da consegnare a chi non ha ACL | Non consegna: `blocked` e riferimento alla zona finance |
| MCP assente | Prosegue sui file di zona e dichiara la freschezza; la verifica diventa "non verificabile" |

## Controller e sessione admin

La verifica che legge dati 🔴 gira solo in sessione admin (dove la zona finance è disponibile).
Fuori dalla sessione admin il Controller rifiuta la verifica invece di degradare in silenzio.
