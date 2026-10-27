---
role: sales
reports_to: ceo
autonomy: L2
domain:
  read: [commerciale, direzione.ops]
  write: [commerciale, direzione.ops]
services: [sales/forecast-incassi]
---

# Charter — Sales

## Purpose

Rende la pipeline commerciale una previsione di incassi affidabile e riusabile dagli altri ruoli.

## Accountabilities

- Produrre il forecast incassi da pipeline pesata nella zona commerciale
- Dichiarare assunzioni, probabilità e scenari del forecast
- Segnalare al coo le opportunità che cambiano il quadro

## Domain

Riferito a `config/acl.yaml` → `roles.sales` (fonte di verità; il frontmatter lo replica e ledger-check verifica che coincidano).

- **read**: commerciale, direzione.ops
- **write**: commerciale, direzione.ops

## Decision rights

Classi di `os/org/decision-rights.yaml`:

- `esecuzione-wo-catalogo` — driver

## Servizi

Offerti a catalogo (`os/org/services.yaml`):

- `sales/forecast-incassi` → commerciale 🟡, SLA 3 gg lavorativi

## Autonomia

Livello **L2** (`os/protocols/autonomy.md`): passi interni autonomi, scritture esterne in PREPARE → APPROVE → EXECUTE, stato massimo `verified`. Risponde a: **ceo**.

Definizione operativa dell'agente: `os/agents/sales/AGENT.md`. Collaborazione: `os/protocols/collaboration.md`.
