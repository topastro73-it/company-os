# /compliance vendor-assessment — Valutazione fornitore

## Scopo
Valutare la postura di sicurezza di un fornitore PRIMA della firma. Supply chain security
è anche un requisito NIS2: nessun fornitore con dati senza assessment.

## Input
- Vendor · servizio fornito · dati trattati (personali? di clienti PMI? credenziali?)
- Criticità per il servizio (se cade lui, cadiamo noi?)

## Passi
1. Verifica se esiste già un assessment in `compliance/vendors/{slug}.md` (validità:
   12 mesi) — se fresco, aggiorna solo i delta.
2. **Questionario/raccolta**: certificazioni (ISO 27001, SOC 2…), policy pubbliche,
   incident history noti, sub-processor, localizzazione dati (extra-UE → SCC/adequacy),
   SLA e supporto, exit strategy (portabilità dati).
3. **Risk rating**: Critical / High / Medium / Low, in funzione di dati trattati ×
   criticità servizio × postura dimostrata.
4. **DPA**: tratta dati personali? → DPA obbligatorio; clausole specifiche necessarie
   (sub-processor, breach notification, audit right).
5. **Raccomandazione**: approvare / approvare con condizioni (elencate) / rifiutare.
6. Registra e imposta la data di rivalutazione (+12 mesi).

## Formato output
```markdown
---
zone: compliance
tier: 🟡
type: vendor-assessment
vendor: {slug}
risk-rating: {critical|high|medium|low}
dpa-required: true
valid-until: YYYY-MM-DD
---
# Vendor Assessment — {vendor} — {YYYY-MM-DD}

## Servizio e dati trattati   ## Certificazioni e postura
## Rischi identificati        ## DPA e clausole richieste
## Raccomandazione: {esito} + condizioni
```

## Destinazione
Zona `compliance` → `vendors/{slug}.md`.
Commit (admin): `[compliance] vendor: assessment {vendor}`.

## Handoff
Approvato → `finance` (contrattualizzazione) e richiedente (`cto`/`product`) ·
contratto da rivedere → `/compliance contract-review`.
