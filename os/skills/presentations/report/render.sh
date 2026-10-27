#!/usr/bin/env bash
# Render di un report HTML (template report-template.html) in PDF A4 orizzontale + anteprime PNG.
# Uso: os/skills/presentations/report/render.sh <file.html> [output.pdf]
# Default output: stesso nome del file .html, nella cartella superiore (es. _src/x.html -> x.pdf).
set -euo pipefail

html="${1:?Uso: render.sh <file.html> [output.pdf]}"
html_abs="$(cd "$(dirname "$html")" && pwd)/$(basename "$html")"
name="$(basename "$html" .html)"
out="${2:-$(dirname "$(dirname "$html_abs")")/$name.pdf}"

chrome=""
for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" google-chrome chromium chromium-browser; do
  if command -v "$c" >/dev/null 2>&1 || [ -x "$c" ]; then chrome="$c"; break; fi
done
[ -n "$chrome" ] || { echo "Chrome/Chromium non trovato" >&2; exit 1; }

profile="$(mktemp -d)"
"$chrome" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 \
  --user-data-dir="$profile" --print-to-pdf="$out" "file://$html_abs" >/dev/null 2>&1

echo "PDF: $out"
command -v pdfinfo >/dev/null && pdfinfo "$out" | grep -E "Pages|Page size"

# Anteprime per il controllo visivo (pagina per pagina): richiede poppler (pdftoppm)
if command -v pdftoppm >/dev/null; then
  prev="$(mktemp -d)"
  pdftoppm -r 50 -png "$out" "$prev/p" 2>/dev/null
  echo "Anteprime: $prev"
fi
