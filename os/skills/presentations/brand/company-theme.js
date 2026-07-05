/**
 * Company — Brand template for pptxgenjs
 * --------------------------------------------------------------------------
 * Tema NEUTRO generico per il template CompanyOS. Personalizzalo con i token
 * del tuo brand: la single source of truth dei token vive in
 * `company/marketing/brand/company-brand.md` (colori, font, layout).
 *
 * Uso:
 *   const PptxGenJS = require("pptxgenjs");
 *   const { applyBrand, slideTitle, slideSection, slideContent,
 *           slideMetrics, slideClosing } = require("./company-theme");
 *   const pptx = new PptxGenJS();
 *   applyBrand(pptx);
 *   slideTitle(pptx, { title: "...", subtitle: "...", kicker: "Q2 / 2026" });
 *   await pptx.writeFile({ fileName: "deck.pptx" });
 *
 * Tutte le slide sono 16:9. I font di default sono sans-serif di sistema
 * (Arial): sostituiscili con i font del tuo brand se necessario.
 */

// ---------------------------------------------------------------------------
// Design tokens (mirror di company/marketing/brand/company-brand.md)
// Placeholder neutri — sostituisci con i colori/font del tuo brand.
// ---------------------------------------------------------------------------
const BRAND = {
  // signature / accent (placeholder neutro)
  accent: "2563EB",
  // backgrounds (dark ramp)
  bg: "111111",
  ink: "000000",
  surface: "1B1B1B",
  surfaceAlt: "222222",
  surfaceHi: "2E2E2E",
  line: "3A3A3A",
  // text
  textOn: "FFFFFF",
  muted: "9AA0A6",
  lightSurface: "F5F5F5",
  // semantic
  danger: "EF4444",
  warning: "F59E0B",
  success: "22C55E",
  // type (sans-serif di sistema — sostituisci col font del tuo brand)
  fontDisplay: "Arial",
  fontDisplayLight: "Arial",
  fontBody: "Arial",
  fontBodyMedium: "Arial",
};

// Wordmark testuale (placeholder al posto di un logo immagine).
// Sostituisci con `slide.addImage({ path: ... })` quando hai il logo del brand.
const WORDMARK = "Company";
const SITE = "company.example";

// Geometria slide 16:9 in pollici (LAYOUT_WIDE = 10 x 5.625)
const W = 10;
const H = 5.625;
const MARGIN = 0.5;

function addWordmark(slide, { x = MARGIN, y = 0.45, size = 18 } = {}) {
  slide.addText(WORDMARK, {
    x, y, w: 3, h: 0.4,
    fontFace: BRAND.fontDisplay, fontSize: size, bold: true, color: BRAND.textOn, charSpacing: 1,
  });
}

// ---------------------------------------------------------------------------
// Setup globale + master slides
// ---------------------------------------------------------------------------
function applyBrand(pptx) {
  pptx.defineLayout({ name: "CO_WIDE", width: W, height: H });
  pptx.layout = "CO_WIDE";
  pptx.author = "Company";
  pptx.company = "Company";
  pptx.theme = { headFontFace: BRAND.fontDisplay, bodyFontFace: BRAND.fontBody };

  // Master scuro standard (content/section/metrics)
  pptx.defineSlideMaster({
    title: "CO_DARK",
    background: { color: BRAND.bg },
    objects: [
      // footer hairline
      { rect: { x: MARGIN, y: H - 0.5, w: W - MARGIN * 2, h: 0.012, fill: { color: BRAND.line } } },
      // wordmark (footer sx)
      { text: { text: WORDMARK, options: { x: MARGIN, y: H - 0.46, w: 1.5, h: 0.3, fontFace: BRAND.fontDisplay, fontSize: 11, bold: true, color: BRAND.textOn } } },
      // site (footer dx)
      { text: { text: SITE, options: { x: W - 2.5, y: H - 0.46, w: 2.0, h: 0.3, align: "right", fontFace: BRAND.fontBody, fontSize: 9, color: BRAND.muted } } },
    ],
    slideNumber: { x: W - 0.5, y: H - 0.46, w: 0.3, h: 0.3, fontFace: BRAND.fontBody, fontSize: 9, color: BRAND.accent, align: "right" },
  });

  // Master nero pieno (title/closing)
  pptx.defineSlideMaster({
    title: "CO_INK",
    background: { color: BRAND.ink },
  });

  return pptx;
}

// ---------------------------------------------------------------------------
// Helper: titoletto "kicker" accent + barra accento
// ---------------------------------------------------------------------------
function accentBar(slide, x, y, w = 0.9) {
  slide.addShape("rect", { x, y, w, h: 0.06, fill: { color: BRAND.accent } });
}

// ---------------------------------------------------------------------------
// 1. TITLE SLIDE (nero, hero)
// ---------------------------------------------------------------------------
function slideTitle(pptx, { title, subtitle, kicker, date } = {}) {
  const slide = pptx.addSlide({ masterName: "CO_INK" });

  addWordmark(slide, { x: MARGIN, y: 0.45, size: 20 });
  if (kicker) {
    slide.addText(kicker.toUpperCase(), {
      x: MARGIN, y: 1.7, w: W - MARGIN * 2, h: 0.35,
      fontFace: BRAND.fontBodyMedium, fontSize: 12, color: BRAND.accent, charSpacing: 2,
    });
  }
  accentBar(slide, MARGIN, 2.12, 0.9);
  slide.addText(title || "", {
    x: MARGIN, y: 2.25, w: W - MARGIN * 2, h: 1.5,
    fontFace: BRAND.fontDisplay, fontSize: 34, bold: true, color: BRAND.textOn, lineSpacingMultiple: 1.05,
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: MARGIN, y: 3.75, w: W - MARGIN * 2, h: 1.0,
      fontFace: BRAND.fontDisplayLight, fontSize: 16, color: BRAND.muted, lineSpacingMultiple: 1.15,
    });
  }
  if (date) {
    slide.addText(date, {
      x: W - 2.5, y: 0.5, w: 2.0, h: 0.3, align: "right",
      fontFace: BRAND.fontBody, fontSize: 11, color: BRAND.muted,
    });
  }
  return slide;
}

// ---------------------------------------------------------------------------
// 2. SECTION DIVIDER
// ---------------------------------------------------------------------------
function slideSection(pptx, { number, title, subtitle } = {}) {
  const slide = pptx.addSlide({ masterName: "CO_DARK" });
  if (number != null) {
    slide.addText(String(number).padStart(2, "0"), {
      x: MARGIN, y: 1.4, w: 3, h: 1.6,
      fontFace: BRAND.fontDisplay, fontSize: 90, bold: true, color: BRAND.surfaceHi,
    });
  }
  accentBar(slide, MARGIN, 2.85, 0.9);
  slide.addText(title || "", {
    x: MARGIN, y: 2.95, w: W - MARGIN * 2, h: 1.0,
    fontFace: BRAND.fontDisplay, fontSize: 30, bold: true, color: BRAND.textOn,
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: MARGIN, y: 3.95, w: W - MARGIN * 2, h: 0.6,
      fontFace: BRAND.fontBody, fontSize: 14, color: BRAND.muted,
    });
  }
  return slide;
}

// ---------------------------------------------------------------------------
// 3. CONTENT SLIDE (titolo + bullet)
//    bullets: array di string | { text, sub }
// ---------------------------------------------------------------------------
function slideContent(pptx, { title, kicker, bullets = [], body } = {}) {
  const slide = pptx.addSlide({ masterName: "CO_DARK" });
  if (kicker) {
    slide.addText(kicker.toUpperCase(), {
      x: MARGIN, y: 0.45, w: W - MARGIN * 2, h: 0.3,
      fontFace: BRAND.fontBodyMedium, fontSize: 11, color: BRAND.accent, charSpacing: 2,
    });
  }
  slide.addText(title || "", {
    x: MARGIN, y: kicker ? 0.78 : 0.55, w: W - MARGIN * 2, h: 0.7,
    fontFace: BRAND.fontDisplay, fontSize: 24, bold: true, color: BRAND.textOn,
  });
  accentBar(slide, MARGIN, kicker ? 1.5 : 1.27, 0.7);

  if (body) {
    slide.addText(body, {
      x: MARGIN, y: 1.75, w: W - MARGIN * 2, h: 3.0,
      fontFace: BRAND.fontBody, fontSize: 14, color: BRAND.muted, lineSpacingMultiple: 1.2,
    });
    return slide;
  }

  const items = [];
  bullets.forEach((b) => {
    const main = typeof b === "string" ? b : b.text;
    items.push({
      text: main,
      options: {
        fontFace: BRAND.fontBodyMedium, fontSize: 15, color: BRAND.textOn,
        bullet: { code: "2022", color: BRAND.accent, indent: 18 },
        paraSpaceAfter: typeof b === "object" && b.sub ? 2 : 10,
      },
    });
    if (typeof b === "object" && b.sub) {
      items.push({
        text: b.sub,
        options: {
          fontFace: BRAND.fontBody, fontSize: 12, color: BRAND.muted,
          bullet: false, indent: 18, paraSpaceAfter: 10,
        },
      });
    }
  });
  slide.addText(items, {
    x: MARGIN, y: 1.8, w: W - MARGIN * 2, h: 3.2, valign: "top",
  });
  return slide;
}

// ---------------------------------------------------------------------------
// 4. METRICS SLIDE (numeri grandi in card)
//    metrics: array di { value, label, color? }
// ---------------------------------------------------------------------------
function slideMetrics(pptx, { title, kicker, metrics = [] } = {}) {
  const slide = pptx.addSlide({ masterName: "CO_DARK" });
  if (kicker) {
    slide.addText(kicker.toUpperCase(), {
      x: MARGIN, y: 0.45, w: W - MARGIN * 2, h: 0.3,
      fontFace: BRAND.fontBodyMedium, fontSize: 11, color: BRAND.accent, charSpacing: 2,
    });
  }
  slide.addText(title || "", {
    x: MARGIN, y: kicker ? 0.78 : 0.55, w: W - MARGIN * 2, h: 0.7,
    fontFace: BRAND.fontDisplay, fontSize: 24, bold: true, color: BRAND.textOn,
  });
  accentBar(slide, MARGIN, kicker ? 1.5 : 1.27, 0.7);

  const n = Math.min(metrics.length, 4) || 1;
  const gap = 0.3;
  const totalW = W - MARGIN * 2;
  const cardW = (totalW - gap * (n - 1)) / n;
  const cardY = 2.1;
  const cardH = 2.3;
  metrics.slice(0, 4).forEach((m, i) => {
    const x = MARGIN + i * (cardW + gap);
    slide.addShape("roundRect", {
      x, y: cardY, w: cardW, h: cardH, rectRadius: 0.08,
      fill: { color: BRAND.surface }, line: { color: BRAND.line, width: 1 },
    });
    slide.addText(m.value, {
      x, y: cardY + 0.45, w: cardW, h: 0.9, align: "center",
      fontFace: BRAND.fontDisplay, fontSize: 40, bold: true, color: m.color || BRAND.accent,
    });
    slide.addText(m.label, {
      x: x + 0.1, y: cardY + 1.45, w: cardW - 0.2, h: 0.7, align: "center", valign: "top",
      fontFace: BRAND.fontBody, fontSize: 12, color: BRAND.muted, lineSpacingMultiple: 1.1,
    });
  });
  return slide;
}

// ---------------------------------------------------------------------------
// 5. CLOSING / CTA SLIDE (nero)
// ---------------------------------------------------------------------------
function slideClosing(pptx, { title, cta, contact } = {}) {
  const slide = pptx.addSlide({ masterName: "CO_INK" });
  addWordmark(slide, { x: MARGIN, y: 0.55, size: 20 });
  accentBar(slide, MARGIN, 2.2, 0.9);
  slide.addText(title || "Let's talk.", {
    x: MARGIN, y: 2.35, w: W - MARGIN * 2, h: 1.2,
    fontFace: BRAND.fontDisplay, fontSize: 32, bold: true, color: BRAND.textOn,
  });
  if (cta) {
    slide.addText(cta, {
      x: MARGIN, y: 3.5, w: W - MARGIN * 2, h: 0.6,
      fontFace: BRAND.fontDisplayLight, fontSize: 16, color: BRAND.accent,
    });
  }
  slide.addText(contact || SITE, {
    x: MARGIN, y: H - 0.9, w: W - MARGIN * 2, h: 0.4,
    fontFace: BRAND.fontBody, fontSize: 12, color: BRAND.muted,
  });
  return slide;
}

module.exports = {
  BRAND,
  WORDMARK,
  addWordmark,
  applyBrand,
  accentBar,
  slideTitle,
  slideSection,
  slideContent,
  slideMetrics,
  slideClosing,
};
