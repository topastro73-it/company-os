# Company — Brand Template per Slide

Brand template neutro per generare presentazioni on-brand con **pptxgenjs**.
Tema di default generico: personalizzalo con i token del tuo brand.

## File

| File | Cosa è |
|------|--------|
| `company-theme.js` | Modulo pptxgenjs: token `BRAND`, `applyBrand()` (master slide) + helper per tipo di slide. |
| `build-sample.js` | Genera un deck demo con tutti i tipi di slide. |
| `preview.html` | Mock HTML delle slide (per anteprima rapida nel browser, no PowerPoint). |
| `../../../company/marketing/brand/company-brand.md` | **SSoT** dei design token (colori, font, layout). |

> Il logo è un **placeholder testuale** (`WORDMARK = "Company"`). Sostituiscilo con il logo del tuo
> brand — aggiungi l'asset in `assets/` e passa a `slide.addImage({ path: ... })` nel tema.

## Quick start

```bash
# dalla root del repo, in una cartella con pptxgenjs installato (npm i pptxgenjs)
node os/skills/presentations/brand/build-sample.js mio-deck.pptx
```

> Il `.pptx` è un **build on-demand**: non si committa (vedi CLAUDE.md "Deliverable per umani").
> La sorgente versionata è il **codice** che lo genera.

## Usare il template in un deck custom

```js
const PptxGenJS = require("pptxgenjs");
const T = require("./os/skills/presentations/brand/company-theme");

const pptx = new PptxGenJS();
T.applyBrand(pptx);

T.slideTitle(pptx, {
  kicker: "Q2 / 2026",
  title: "Titolo del deck",
  subtitle: "Sottotitolo / value proposition.",
  date: "Company · 2026",
});

T.slideSection(pptx, { number: 1, title: "Sezione", subtitle: "..." });

T.slideContent(pptx, {
  kicker: "La Soluzione",
  title: "Titolo slide",
  bullets: [
    { text: "Punto chiave", sub: "Dettaglio." },
    "Punto semplice",
  ],
});

T.slideContent(pptx, { title: "Solo testo", body: "Paragrafo lungo..." });

T.slideMetrics(pptx, {
  title: "I numeri",
  metrics: [
    { value: "+18%", label: "Metrica 1" },
    { value: "-23%", label: "Metrica 2" },
  ],
});

T.slideClosing(pptx, {
  title: "Call to action.",
  cta: "Prenota una demo →",
  contact: "nome@example.com · company.example",
});

await pptx.writeFile({ fileName: "deck.pptx" });
```

## Helper disponibili

| Helper | Slide |
|--------|-------|
| `slideTitle(pptx, {title, subtitle, kicker, date})` | Cover nera con wordmark + hero. |
| `slideSection(pptx, {number, title, subtitle})` | Divisore di sezione con numero gigante. |
| `slideContent(pptx, {title, kicker, bullets[]})` o `{body}` | Bullet (con sub-testo) o paragrafo. |
| `slideMetrics(pptx, {title, kicker, metrics[]})` | Fino a 4 card con numeri grandi. |
| `slideClosing(pptx, {title, cta, contact})` | Slide finale / CTA nera. |
| `applyBrand(pptx)` | Layout 16:9 + master `CO_DARK` / `CO_INK`. Chiamalo **una volta** all'inizio. |

Tutti gli helper ritornano l'oggetto `slide` di pptxgenjs, così puoi aggiungere elementi custom
usando i token `T.BRAND.accent`, `T.BRAND.bg`, ecc.

## Font

Il template usa font **sans-serif di sistema** (Arial) di default. Sostituiscili con i font del tuo
brand nei token `BRAND.fontDisplay` / `BRAND.fontBody`; se usi font non di sistema, installali sulla
macchina prima di esportare in PDF per una resa fedele (in mancanza, PowerPoint applica un fallback).

## Allineamento con la SKILL

Vedi `os/skills/presentations/SKILL.md` per le strutture-deck (pitch, demo, proposal):
costruisci la struttura con quegli schemi e renderizzala con questi helper.
