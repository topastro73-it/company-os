# Presentations Skill

Framework per la creazione di presentazioni. Usato da CEO, Marketing, Sales, PM.

## Tipi di Presentazione Disponibili

### 1. Pitch Deck (Investitori) — Owner: CEO
Struttura standard (10-12 slide):
1. **Title + One-liner**
2. **Problem** — Il pain point, dimensione del problema
3. **Solution** — Come lo risolviamo (demo screenshot)
4. **Market** — TAM/SAM/SOM
5. **Business Model** — Come facciamo soldi
6. **Traction** — Metriche chiave, crescita, clienti
7. **Competition** — Mappa competitiva, differenziazione
8. **Team** — Fondatori, advisor
9. **Financials** — Revenue, proiezioni, unit economics
10. **The Ask** — Quanto raccogliamo, use of funds
11. **Vision** — Dove saremo tra 5 anni
12. **Contact** — CTA

### 2. Product Demo Deck (Clienti) — Owner: Sales + PM
Struttura (8-10 slide):
1. **Title + Customer-centric hook**
2. **Il loro problema** (parlare di LORO)
3. **Come lo risolviamo** — Overview soluzione
4. **Demo walkthrough** — 3-5 slide con screenshot/flow
5. **Risultati** — Case study, metriche di impatto
6. **Perché noi** — Differenziatori
7. **Pricing overview** — Tier e range
8. **Next steps** — Trial, POC, contratto

### 3. Sales Proposal Deck — Owner: Sales
Struttura (6-8 slide):
1. **Title + Prospect name**
2. **La vostra sfida** (personalizzata)
3. **La nostra soluzione per voi** (personalizzata)
4. **Impatto atteso** (ROI, metriche)
5. **Pricing** (quotazione specifica)
6. **Timeline** (implementazione)
7. **Social proof** (case study simile)
8. **Next steps**

## Come generare le presentazioni

Per generare un file `.pptx` reale, chiedi a Claude Code:
"Genera una presentazione .pptx per [tipo] seguendo il framework in `os/skills/presentations/SKILL.md`"

Claude Code può generare file PowerPoint reali usando la libreria pptxgenjs.

## Brand template (OBBLIGATORIO)

Tutte le presentazioni dell'azienda devono usare il **brand template** in
`os/skills/presentations/brand/` — NON generare deck con lo stile di default di pptxgenjs.

- **Token & guidelines**: `company/marketing/brand/company-brand.md` (SSoT: colori, font, layout).
- **Modulo pptxgenjs**: `os/skills/presentations/brand/company-theme.js`
  (`applyBrand()` + helper `slideTitle / slideSection / slideContent / slideMetrics / slideClosing`).
- **Come usarlo**: vedi `os/skills/presentations/brand/README.md`.
- **Sample**: `node os/skills/presentations/brand/build-sample.js`.

Identità in breve (tema neutro di default, da personalizzare col tuo brand): sfondo dark, accento
firma **`#2563EB`** (placeholder), font **sans-serif di sistema**, numeri grandi per le metriche,
footer con wordmark + sito + pagina.

Workflow: scegli la struttura dal tipo di deck (sotto) → mappa ogni slide su un helper del template → genera il `.pptx`.

## Principi di Design
- **Una idea per slide** — non sovraccaricare
- **Poco testo** — massimo 5-6 righe per slide
- **Numeri grandi** — le metriche chiave in font grande
- **Consistenza** — stesso stile, font, colori su tutte le slide
- **Visual > testo** — screenshot, grafici, diagrammi quando possibile
