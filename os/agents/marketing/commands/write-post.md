# /marketing write-post — Blog post / LinkedIn post

## Scopo
Scrivere un contenuto che il target legga fino in fondo e che converta.

## Input
- Topic · formato (blog SEO / LinkedIn) · persona target · CTA desiderata
- Idealmente: slot dal content plan corrente

## Passi
1. Carica il tono di voce (`marketing/brand/`), il positioning, e cosa abbiamo già
   scritto sul tema (`marketing/content/index.md` + `blog/`).
2. **Angolo**: parti dal problema del lettore, non dal prodotto. Per le PMI: linguaggio
   semplice, zero acronimi non spiegati. Per i partner: revenue e differenziazione.
3. **Struttura blog**: hook (problema reale) → sviluppo con dati/esempi (fonte citata)
   → punto di vista nostro → CTA unica. Titolo + meta description per SEO, keyword
   naturale, H2/H3 scansionabili. **LinkedIn**: hook in prima riga, paragrafi brevi,
   una idea sola, CTA finale.
4. **Verifica claim**: ogni affermazione su feature → shipped (zona `prodotto`); ogni
   raccomandazione di sicurezza → la seguiamo anche noi (zona `compliance`); ogni numero
   → fonte.
5. Classifica `tier: 🟢` solo se non contiene dati interni; altrimenti resta 🟡 e non
   si pubblica finché non è redatto.
6. Aggiorna `content/index.md`; la pubblicazione reale segue PREPARE → APPROVE → EXECUTE.

## Formato output
```markdown
---
zone: marketing
tier: 🟢
type: blog-post
persona: {…}
keyword: {…}
status: draft            # draft → review → published
---
# {Titolo}
{meta-description}
{corpo}
**CTA**: {…}
```

## Destinazione
Zona `marketing` → `blog/{slug}.md`. Commit (admin): `[marketing] content: {slug}`.

## Handoff
Post tecnico → co-firma `cto`/`ceo` se aumenta credibilità · enablement → `sales`.
