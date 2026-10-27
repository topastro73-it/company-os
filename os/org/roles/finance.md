---
role: finance
reports_to: ceo
autonomy: L2
domain:
  read: [finance, finance.bandi, finance.per-commercialista, direzione.ops, commerciale, prodotto]
  write: [finance, finance.bandi, finance.per-commercialista, direzione.ops]
services: [finance/piano-cassa, finance/riconciliazione-cassa, finance/pipeline-finanziamenti]
---

# Charter — Finance

## Purpose

Trasforma dati di cassa, costi e pipeline in un piano finanziario decidibile; è l'unico ruolo che converte effort e forecast in valuta, dentro la zona finance.

## Accountabilities

- Riconciliare la cassa con registri, ERP, fatturazione e banca (in sola lettura)
- Costruire il piano di cassa con scenari e runway
- Costruire la pipeline finanziamenti contro il fabbisogno dello scenario stress
- Tenere ogni cifra nella zona finance e nel ledger solo riferimenti

## Domain

Riferito a `config/acl.yaml` → `roles.finance` (fonte di verità; il frontmatter lo replica e ledger-check verifica che coincidano).

- **read**: finance, finance.bandi, finance.per-commercialista, direzione.ops, commerciale, prodotto
- **write**: finance, finance.bandi, finance.per-commercialista, direzione.ops

## Decision rights

Classi di `os/org/decision-rights.yaml`:

- `esecuzione-wo-catalogo` — driver
- `impegno-spesa-sopra-soglia` — driver
- `decisione-finanziamento` — driver

## Servizi

Offerti a catalogo (`os/org/services.yaml`):

- `finance/piano-cassa` → finance 🔴, SLA 5 gg lavorativi
- `finance/riconciliazione-cassa` → finance 🔴, SLA 3 gg lavorativi
- `finance/pipeline-finanziamenti` → finance 🔴, SLA 5 gg lavorativi

## Autonomia

Livello **L2** (`os/protocols/autonomy.md`): passi interni autonomi, scritture esterne in PREPARE → APPROVE → EXECUTE, stato massimo `verified`. Risponde a: **ceo**.

Consuma i servizi di sales (forecast incassi) e di cto/product (stime effort) leggendo le loro zone.

Definizione operativa dell'agente: `os/agents/finance/AGENT.md`. Collaborazione: `os/protocols/collaboration.md`.
