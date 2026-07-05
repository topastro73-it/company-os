# /cos prepare-meeting — Brief pre-meeting

## Scopo
Arrivare a ogni meeting con background, dati con fonte, domande aperte e agenda.

## Input
- Topic · partecipanti (interni/esterni) · obiettivo (decisione, allineamento, discovery, update)
- Data e durata prevista

## Passi
1. **Identifica il meeting** e cosa deve produrre.
2. **Carica il contesto giusto** in base al topic:
   - cliente/partner → `clienti/{slug}/` (scheda, QBR, proposte) + opportunità in `commerciale`
   - prodotto/tech → `prodotto` (roadmap, spec, ADR rilevanti)
   - strategico → `direzione` (vision, OKR, decisioni recenti)
   - investor → `vault/finance` + `direzione/investor-updates/` (solo admin)
   - sempre: `direzione/decisions/` per decisioni aperte sul topic
3. **Costruisci il brief**: background (3-5 punti con riferimenti), dati chiave (ogni numero
   con fonte), domande aperte (con possibili risposte e pro/contro), 2-4 outcome possibili
   con implicazioni.
4. **Agenda** in slot temporali: argomento, owner della discussione, obiettivo dello slot.
5. Se meeting con partner attivo: rileggi la storia (wiki entity / scheda cliente) —
   non far ripartire conversazioni già fatte.

## Formato output
```markdown
---
zone: {direzione | clienti/{slug}}
tier: 🟡
type: meeting-brief
---
# Meeting Prep — {topic} — {data}
**Partecipanti**: … · **Obiettivo**: … · **Durata**: …

## Background        ## Dati chiave (con fonte)
## Domande aperte    ## Possibili outcome
## Agenda | Slot | Argomento | Owner | Obiettivo |
## Post-meeting: follow-up da tracciare (compilare dopo)
```

## Destinazione
Meeting interno/strategico → zona `direzione/briefing/meeting-{slug}-{data}.md`.
Meeting con un cliente → zona `clienti/{slug}/meeting-prep-{data}.md`.
