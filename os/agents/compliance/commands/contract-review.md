# /compliance contract-review — Analisi o draft contratto

## Scopo
Rivedere (o draftare) un contratto identificando rischi e clausole mancanti.
Draft e analisi, mai parere legale definitivo.

## Input
- Tipo: partnership/reseller, SaaS agreement, NDA, DPA, fornitore
- Controparte · il testo (se review) o i termini chiave (se draft)

## Passi
1. Carica precedenti con la stessa controparte (`clienti/{slug}/contratti/` se partner —
   ACL ristretta) e i template standard; coerenza con clausole già negoziate.
2. **Checklist di review**:
   - oggetto e corrispettivi chiari · durata, rinnovo, recesso · SLA e penali ·
     limitazione di responsabilità (cap, esclusioni) · IP (chi possiede cosa) ·
     riservatezza · legge applicabile e foro
   - **dati personali trattati? → DPA obbligatorio** allegato o richiamato; il fornitore
     ha vendor assessment valido? Se no → **flag bloccante**, assessment prima della firma
   - clausole white-label/tenant per i contratti partner (branding, responsabilità verso PMI)
3. **Red flags** per severità: bloccante / da negoziare / accettabile con nota.
4. Proposta di modifica per ogni red flag (testo alternativo pronto).
5. **Soglie**: valore >€50k o clausole non standard → raccomanda revisione legale esterna,
   sempre. La firma è SOLO del CEO.

## Formato output
```markdown
---
zone: compliance
tier: 🟡
type: contract-review
counterparty: {slug}
---
# Contract Review — {tipo} — {controparte} — {data}

## Sintesi e raccomandazione (firmabile? a quali condizioni?)
## Red flags | Clausola | Severità | Rischio | Proposta |
## Check DPA e vendor assessment
## Next steps

> Draft/analisi interna. Far validare da un avvocato prima dell'uso.
```

## Destinazione
Analisi: zona `compliance` → `audits/contract-{controparte}-{YYYY-MM-DD}.md`.
Il contratto firmato (🔴) va SOLO in `clienti/{slug}/contratti/` o `vault/`.
Commit (admin): `[compliance] contract: review {controparte}`.

## Handoff
Firma → `ceo` · esito al deal owner → `sales` · DPA mancante fornitore →
`/compliance vendor-assessment`.
