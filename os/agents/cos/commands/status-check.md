# /cos status-check — Semafori su tutti i workstream

## Scopo
Rispondere a "come stiamo su tutto?" con un semaforo per ogni workstream e una sintesi.

## Input
Nessuno; opzionale: area specifica ("status prodotto").

## Passi
1. **Carica le fonti**: `prodotto` (roadmap, backlog, specs, testing), `direzione`
   (decisions, okrs), `commerciale` (PIPELINE, opportunità), `clienti` (health, onboarding),
   `compliance` (status), `vault/finance` (solo admin).
2. **Assegna il semaforo** a ogni workstream:
   - 🟢 on track · 🟡 rischio identificato ma gestibile · 🔴 fermo, serve intervento ·
     ⚫ nessun dato nel sistema (il dato mancante È un finding)
3. **Copri**:
   - **Prodotto**: epic/spec del quarter con stato e test status
     (📋 plan / 🧪 in test / ✅ GO / ❌ NO-GO / ⚠️ nessun test plan)
   - **Decisioni**: follow-up aperti, review date passate, decisioni pendenti
   - **OKR**: progresso per KR, KR a rischio
   - **Commerciale/Delivery**: deal 🔴, onboarding in ritardo, partner Critical
   - **Operativo**: azioni P0 senza owner o scadute, handoff non raccolti
4. **Sintesi esecutiva**: 3-5 righe — cosa va, cosa richiede intervento, cosa è fermo.

## Formato output
```markdown
---
zone: direzione
tier: 🟡
type: report
---
# Status Check — {YYYY-MM-DD}

## Prodotto   | Epic/Spec | Stato | Test | Semaforo | Note |
## Decisioni  | ID | Titolo | Follow-up | Semaforo |
## OKR        | KR | Target | Attuale | Semaforo |
## Commerciale & Delivery | Item | Stato | Semaforo |
## Operativo  | Azione | Owner | Deadline | Semaforo |

## Sintesi esecutiva
```

## Destinazione
Zona `direzione` → `briefing/status-{YYYY-MM-DD}.md`.
Commit (admin): `[cos] report: status check {YYYY-MM-DD}`.
