# Decisions — decisioni immutabili

## Dove

Zona `direzione`: `00-Direzione/decisions/` (snapshot: `company/direzione/decisions/`).
File: `YYYY-MM-DD-{slug}.md` — es. `2026-07-04-pricing-tier-enterprise.md`.
Frontmatter: `zone: direzione`, `tier: 🟡` (🔴 se cita importi/contratti riservati → allora
il dettaglio 🔴 sta in finance/vault e la decisione lo referenzia senza riportarlo).

## Quando registrare una decisione

Registra come decisione (non come semplice nota) quando la scelta:
- vincola il futuro (pricing, posizionamento, architettura, contratto quadro, assunzione)
- chiude un'alternativa reale (si è scelto A **invece di** B)
- dovrà essere spiegabile mesi dopo ("perché avevamo deciso così?")

Non registrare: task operativi, preferenze reversibili senza costo, ipotesi esplorative.
Il protocollo memory (`memory.md` §1) intercetta le decisioni emerse in chat e propone la
registrazione — sempre con conferma umana.

## Immutabilità

Le decisioni **non si modificano** e non si cancellano: si **superano** con una nuova decisione.
- La nuova decisione linka la vecchia nel Contesto ("supera DEC-012")
- La vecchia riceve SOLO l'aggiornamento dello stato: `Stato: Superata` + link alla nuova
- Tutto il resto del file resta com'era: è il record storico di cosa si sapeva allora

## Template

```markdown
---
zone: direzione
tier: 🟡
status: approvata          # proposta | approvata | superata
superseded-by:             # path della decisione che la supera (se superata)
---
# DEC-{NNN}: {Titolo della decisione}

- **Data**: YYYY-MM-DD
- **Agente/Owner**: {ceo/product/cto/sales/…} — {persona}
- **Stato**: Proposta | Approvata | Superata
- **Review date**: YYYY-MM-DD (opzionale — quando ricontrollarla)

## Contesto
Qual è il problema o l'opportunità? Cosa si sapeva al momento della decisione?

## Opzioni considerate

### Opzione A: {nome}
- **Pro**: … · **Contro**: … · **Effort**: S/M/L · **Impatto atteso**: …

### Opzione B: {nome}
- **Pro**: … · **Contro**: … · **Effort**: S/M/L · **Impatto atteso**: …

## Decisione
Abbiamo scelto **Opzione X** perché …

## Conseguenze
- Cosa cambia dopo questa decisione
- Next step
- Rischi da monitorare

## Follow-up
- [ ] Azione 1 — Owner: {persona} — Due: YYYY-MM-DD
- [ ] Azione 2 — Owner: {persona} — Due: YYYY-MM-DD
```

## Collegamenti

- La **wiki** può avere una entity page `system/wiki/entities/decisions/{slug}.md` con
  l'evoluzione narrativa; il file in `decisions/` resta la fonte formale
- Le decisioni architetturali tecniche (ADR) seguono lo stesso principio ma vivono in zona
  `prodotto` a cura del CTO; qui vanno solo quelle con impatto direzionale
- Al close, le decisioni prese in sessione compaiono nel blocco "Dove eravamo rimasti"
  della sessione successiva (vedi `session-rituals.md`)
