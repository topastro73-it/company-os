# Workflow: Customer Escalation

Un cliente ha un problema critico o una richiesta urgente.

## 1. Intake (Sales / Delivery)
- **Trigger**: segnalazione da cliente/partner (email, call, canale partner)
- **Azione**: documenta cliente, problema, impatto (quanti utenti/end-customer), urgenza,
  cosa è stato promesso
- **Output**: `20-Clienti/{slug}/escalations/{YYYY-MM-DD}-{slug}.md` (cartella cliente:
  la vede solo chi segue il cliente)
- **Handoff → Product**: escalation documentata, con severità proposta

## 2. Triage (Product)
- **Input**: file escalation nella cartella cliente
- **Azione**: classifica —
  - **Bug** → handoff CTO (se outage/degrado: passa a `incident-response.md`)
  - **Feature request urgente** → `feature-lifecycle.md` fase 2, fast-track ma **senza
    saltare il framework** (no shortcut)
  - **Configurazione / uso** → handoff Delivery
- **Output**: triage annotato nel file escalation (tipo, owner, ETA di prima risposta)

## 3. Resolution (per tipo)
- **Bug critico (CTO)**: fix + verifica; task ClickUp via external-writes; se serve
  comunicazione ai clienti impattati → coordina con CEO/Marketing
- **Feature urgente (Product)**: valutazione con esito esplicito e data di risposta al cliente
- **Configurazione (Delivery)**: risolvi, documenta la soluzione in
  `30-Prodotto/knowledge-base/` (riusabile, pseudonimizzata)
- **Criterio di uscita**: risoluzione verificata (non solo deployata) e annotata nel file

## 4. Follow-up (Sales / Delivery)
- **Azione**: comunica la risoluzione al cliente (bozza email via external-writes);
  aggiorna health score del cliente in zona `clienti`
- **Se impatto sul deal**: aggiorna l'opportunità in `10-Commerciale/`
- **Lesson learned**: se emerge un pattern generalizzabile → proponi learning LRN-XXX
  al close (`os/protocols/memory.md` §3)

## Regole
- SLA di prima risposta: entro la giornata lavorativa per severità alta
- Ogni escalation resta nella cartella cliente — mai in zone più larghe
- Escalation ricorrenti sullo stesso tema (≥3) → segnala a Product come segnale di backlog
