# Company — Brand Template for Slides

Neutral brand template for generating on-brand presentations with **pptxgenjs**.
Generic default theme: customize it with your brand's tokens.

## Files

| File | What it is |
|------|--------|
| `company-theme.js` | pptxgenjs module: `BRAND` tokens, `applyBrand()` (master slide) + helpers per slide type. |
| `build-sample.js` | Generates a demo deck with all slide types. |
| `preview.html` | HTML mock of the slides (for quick preview in the browser, no PowerPoint). |
| `../../../company/marketing/brand/company-brand.md` | **SSoT** for the design tokens (colors, fonts, layout). |

> The logo is a **text placeholder** (`WORDMARK = "Company"`). Replace it with your brand's
> logo — add the asset in `assets/` and switch to `slide.addImage({ path: ... })` in the theme.

## Quick start

```bash
# from the repo root, in a folder with pptxgenjs installed (npm i pptxgenjs)
node os/skills/presentations/brand/build-sample.js mio-deck.pptx
```

> The `.pptx` is an **on-demand build**: it is not committed (see CLAUDE.md "Deliverables for humans").
> The versioned source is the **code** that generates it.

## Using the template in a custom deck

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

## Available helpers

| Helper | Slide |
|--------|-------|
| `slideTitle(pptx, {title, subtitle, kicker, date})` | Black cover with wordmark + hero. |
| `slideSection(pptx, {number, title, subtitle})` | Section divider with a giant number. |
| `slideContent(pptx, {title, kicker, bullets[]})` or `{body}` | Bullets (with sub-text) or paragraph. |
| `slideMetrics(pptx, {title, kicker, metrics[]})` | Up to 4 cards with big numbers. |
| `slideClosing(pptx, {title, cta, contact})` | Final slide / black CTA. |
| `applyBrand(pptx)` | 16:9 layout + `CO_DARK` / `CO_INK` masters. Call it **once** at the start. |

All helpers return the pptxgenjs `slide` object, so you can add custom elements
using the tokens `T.BRAND.accent`, `T.BRAND.bg`, etc.

## Fonts

The template uses **system sans-serif** fonts (Arial) by default. Replace them with your brand's
fonts in the `BRAND.fontDisplay` / `BRAND.fontBody` tokens; if you use non-system fonts, install them on the
machine before exporting to PDF for faithful rendering (otherwise, PowerPoint applies a fallback).

## Alignment with the SKILL

See `os/skills/presentations/SKILL.md` for the deck structures (pitch, demo, proposal):
build the structure with those outlines and render it with these helpers.
