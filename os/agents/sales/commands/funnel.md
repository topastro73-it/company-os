# /sales funnel — Funnel ISP Tier-2 / MSP

## Scopo
Mantenere la target list consolidata del funnel: chi è attivo, chi è warm, chi è cold,
e cosa fare dopo per ciascuno.

## Input
- Nessuno (lettura/report) oppure aggiornamenti ("sposta {azienda} a warm", "aggiungi {lista}")

## Passi
1. Carica `commerciale/isp-funnel.md` — la target list consolidata.
2. **Classifica** ogni target:
   - **Attivo**: conversazione in corso → deve esistere un'opportunità collegata
   - **Warm**: risposta/interesse ma non qualificato → next touch pianificato
   - **Cold**: mai contattato o sequenza esaurita senza risposta → candidato outbound
3. **Coerenza col cockpit**: ogni "attivo" senza opportunità → creala (`/sales opportunity`);
   ogni opportunità open il cui account non è nel funnel → aggiungilo.
4. **Aging del warm**: warm senza touch da >14gg → flag, proponi il next touch.
5. **Report**: numeri per fascia, movimenti dall'ultimo aggiornamento, prossime azioni
   per owner (chi contatta chi, entro quando).

## Formato output
```markdown
---
zone: commerciale
tier: 🟡
type: funnel
updated: YYYY-MM-DD
---
# Funnel ISP Tier-2 / MSP — {YYYY-MM-DD}

## Summary: attivi {n} · warm {n} · cold {n} · conversioni cold→warm→attivo del mese

## Attivi   | Azienda | Opportunità | Stage | Owner | Next step |
## Warm     | Azienda | Ultimo touch | Interesse | Next touch (data) | Owner |
## Cold     | Azienda | Segmento | Fonte lista | In sequenza? |

## Prossime azioni (owner + deadline)
```

## Destinazione
Zona `commerciale` → `isp-funnel.md` (aggiornamento in place).
Commit (admin): `[sales] funnel: aggiornamento {YYYY-MM-DD}`.

## Handoff
Batch di cold da attivare → `/sales outbound`; attivo qualificato → `/sales opportunity`.
