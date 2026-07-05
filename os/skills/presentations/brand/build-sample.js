/**
 * Company brand template — sample deck.
 * Genera un deck dimostrativo con tutti i tipi di slide del template.
 *
 *   node os/skills/presentations/brand/build-sample.js [outFile.pptx]
 *
 * Default out: ./company-brand-sample.pptx (binario = build on-demand,
 * NON committato — vedi CLAUDE.md "Deliverable per umani").
 */
const PptxGenJS = require("pptxgenjs");
const {
  applyBrand, slideTitle, slideSection, slideContent, slideMetrics, slideClosing,
} = require("./company-theme");

const out = process.argv[2] || "company-brand-sample.pptx";

const pptx = new PptxGenJS();
applyBrand(pptx);

// 1 — Title
slideTitle(pptx, {
  kicker: "Q2 / 2026",
  title: "Company: la tua value proposition in una riga",
  subtitle:
    "Sottotitolo che spiega il beneficio principale per il cliente target.",
  date: "Company · 2026",
});

// 2 — Section divider
slideSection(pptx, {
  number: 1,
  title: "Il Problema",
  subtitle: "Perché il mercato lascia valore sul tavolo.",
});

// 3 — Content / bullets
slideContent(pptx, {
  kicker: "La Soluzione",
  title: "Cosa fa il prodotto, in tre punti",
  bullets: [
    { text: "Capacità 1", sub: "Beneficio concreto per il cliente." },
    { text: "Capacità 2", sub: "Un secondo beneficio misurabile." },
    { text: "Capacità 3", sub: "Il differenziatore rispetto alle alternative." },
  ],
});

// 4 — Metrics
slideMetrics(pptx, {
  kicker: "L'Impatto",
  title: "I risultati",
  metrics: [
    { value: "+18%", label: "Metrica di crescita 1" },
    { value: "-23%", label: "Metrica di riduzione 2" },
    { value: "5x", label: "Metrica di efficienza 3" },
    { value: "<48h", label: "Metrica di velocità 4" },
  ],
});

// 5 — Content (body) — esempio testo lungo
slideContent(pptx, {
  kicker: "Perché ora",
  title: "Il contesto di mercato rende urgente il problema",
  body:
    "Descrivi qui il trend di mercato o normativo che rende la tua soluzione " +
    "necessaria adesso. Spiega perché il cliente possiede già gli asset (relazione, " +
    "canale, dati) e come il prodotto colma il gap operativo, automatizzando il " +
    "processo end-to-end.",
});

// 6 — Closing / CTA
slideClosing(pptx, {
  title: "Trasformiamo il problema in valore ricorrente.",
  cta: "Prenota una call di 30 minuti →",
  contact: "nome@example.com · company.example",
});

pptx.writeFile({ fileName: out }).then((f) => {
  console.log("✓ Sample deck generato:", f);
});
