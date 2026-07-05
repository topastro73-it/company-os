# /marketing content-plan — Piano editoriale

## Scopo
Pianificare i contenuti del periodo con obiettivi misurabili, non pubblicare a caso.

## Input
- Periodo (mese/trimestre) · capacità realistica (quanti pezzi possiamo davvero produrre)

## Passi
1. Carica ICP e segmenti (zona `commerciale`), roadmap/release (zona `prodotto`),
   obiezioni ricorrenti dal campo, content esistente (`marketing/content/index.md` —
   non rifare ciò che c'è, aggiorna o rilancia).
2. **Identifica i temi**: pain dei segmenti (NIS2 per le PMI, revenue per i partner),
   release in arrivo (solo shipped o certe), keyword/domande ricorrenti.
3. **Mappa sul funnel**: Awareness → Consideration → Decision; bilancia thought
   leadership, product content, case study, SEO play. Ogni pezzo serve un segmento
   e una fase — se non sai a chi serve, non va nel piano.
4. Per ogni content: titolo di lavoro, formato (blog, LinkedIn, email, one-pager),
   persona target, keyword, CTA, data, owner, metrica di successo.
5. **Compliance check** sui temi security: raccomandiamo solo ciò che facciamo.
6. Aggiorna `marketing/content/index.md` con i pezzi pianificati.

## Formato output
```markdown
---
zone: marketing
tier: 🟡
type: content-plan
period: {periodo}
---
# Content Plan — {periodo}

## Obiettivi del periodo (misurabili)
## Calendario
| Data | Titolo | Formato | Persona | Fase funnel | Keyword | CTA | Metrica |
|---|---|---|---|---|---|---|---|
## Backlog idee (non pianificate)
```

## Destinazione
Zona `marketing` → `content/plan-{periodo}.md`.
Commit (admin): `[marketing] plan: content {periodo}`.

## Handoff
Pezzi di enablement → `sales` · pezzi legati a release → `/marketing launch-plan`.
