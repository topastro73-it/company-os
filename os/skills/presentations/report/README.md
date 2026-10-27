# Template report (A4 orizzontale)

Template HTML per i report e i documenti destinati a clienti e partner: report di PoC, QBR,
assessment, proposte in formato documento. A4 orizzontale, font Inter, card, copertina scura;
colori e loghi vengono dal brand dell'azienda in `assets/` (vedi "Brand").

![Anteprima del template](assets/report-preview.png)

> Per i **deck** (slide `.pptx`) resta il brand template in `../brand/`. Questo template serve
> per i documenti da leggere, inviati come PDF.

## File

| File | Cosa è |
|------|--------|
| `report-template.html` | Il template: copertina più 14 pagine d'esempio, una per ogni componente. |
| `render.sh` | Genera il PDF con Chrome headless e le anteprime PNG per il controllo. |
| `assets/brand.css` | I colori del brand: le variabili CSS che il template usa. |
| `assets/logo-ink.png`, `assets/logo-white.png` | Logo aziendale su fondo chiaro (intestazioni) e su fondo scuro (copertina). |
| `assets/partner-logo.png` | Segnaposto per il logo del cliente o partner. |
| `assets/report-preview.png` | Anteprima delle 15 pagine (rigenerala dopo aver cambiato il brand). |

## Come si usa

1. **Copia** template e assets nella cartella `_src/` del deliverable, nella zona giusta
   (es. `company/clienti/{slug}/report/_src/`):
   ```bash
   mkdir -p company/clienti/acme/report/_src
   cp -R os/skills/presentations/report/assets os/skills/presentations/report/report-template.html company/clienti/acme/report/_src/
   mv company/clienti/acme/report/_src/report-template.html company/clienti/acme/report/_src/2026-11-05-acme-qbr.html
   ```
2. **Logo del partner**: sostituisci `assets/partner-logo.png` con il logo del cliente
   (quadrato o orizzontale, PNG). Il riquadro è alto 7 mm nell'intestazione, 12,5 mm in copertina.
3. **Segnaposto**: sostituisci `{{COMPANY}}` (il nome breve dell'azienda,
   `config/company.yaml → company.short_name`), `{{PARTNER}}`, `{{TITLE}}` (testo
   dell'intestazione, es. `QBR Q4`) e `{{DATE}}`.
4. **Pagine**: le pagine 02–15 sono un catalogo di componenti. Tieni quelle che servono,
   duplica le sezioni `<section class="page">` e cancella il resto. Rinumera il footer (`.pg`)
   e gli Exhibit.
5. **Render** (dalla root del repo):
   ```bash
   os/skills/presentations/report/render.sh company/clienti/acme/report/_src/2026-11-05-acme-qbr.html
   ```
   Il PDF esce nella cartella superiore a `_src/` con lo stesso nome. Lo script stampa anche
   la cartella delle anteprime PNG.
6. **Controlla ogni pagina** sulle anteprime. Le pagine hanno altezza fissa: il testo in
   eccesso viene tagliato senza errori. Se una pagina trabocca, accorcia o spezza su una pagina
   "· Continued".

## Componenti (pagina d'esempio)

| Pagina | Componente | Quando usarlo |
|---|---|---|
| 01 | Copertina scura con 3 card laterali e riga meta | Sempre |
| 02 | Titolo d'azione, lead, 2 card numerate | Executive summary |
| 03 | 2 card + riquadro scuro "What we ask" | Chiusura dell'executive summary, next steps |
| 04 | 6 numeri + timeline | Numeri del periodo, milestone |
| 05 | Flusso a 4 step con nota "loop" | Processo attuale |
| 06 | 2 card di contesto + tabella di confronto | Segmenti, oggi / con noi |
| 07 | Visual a punti + 4 card con bordo colorato | Un collo di bottiglia e le sue conseguenze |
| 08 | Tabella con pill Yes / Partly / Not yet | Uso della piattaforma, copertura |
| 09 | 2 card con check list | Cosa funziona, feedback |
| 10 | Tabella con pill di stato (In progress / In design / Under evaluation) | Richieste e roadmap |
| 11 | 4 card grigie numerate | Principi, modo di lavorare |
| 12 | Tabella oggi / target | Processo target |
| 13 | 5 step numerati + riquadro "da completare" | Proposta, parti in attesa di input |
| 14 | Tabella KPI | Metriche e target |
| 15 | Next steps numerati + "What we ask" | Chiusura |

## Regole di scrittura

- **Titolo d'azione**: ogni pagina ha un titolo che è una frase con la conclusione, non un
  argomento ("Il nuovo processo dimezza i tempi di risposta", non "Risultati").
- **Kicker** sopra il titolo per la sezione (`Insight 2 · Use of the platform`); `· Continued`
  per le pagine che proseguono.
- **Exhibit numerati** per tabelle e visual, con la fonte sotto (`.source`).
- **Una pagina, un messaggio**: meglio due pagine leggere che una piena.
- **Niente date o feature non validate** (regola 7 del CLAUDE.md): le pill di stato descrivono
  lo stato, le date le conferma Product/CTO.
- **Lingua**: per clienti esteri il documento è in inglese; il resto segue
  `os/protocols/language.md`.

## Brand

Il template non contiene colori né loghi: li legge da `assets/`. Per adattarlo al tuo brand:

- **Colori**: in `assets/brand.css` cambia i valori delle variabili, non i nomi. Le più visibili
  sono `--accent` (kicker, numeri, bordi delle card, parole evidenziate in copertina), `--accent-dk`
  (versione scura dell'accento, per i testi piccoli), `--accent-soft` (fondi delle pill), `--navy`
  (copertina e riquadri scuri), `--accent-glow` (il bagliore in copertina, l'accento trasparente) e
  `--ink` (titoli). `--green` e `--blue` servono alle pill di stato.
- **Loghi**: sostituisci `assets/logo-ink.png` (su bianco, alto 5,6 mm nell'intestazione) e
  `assets/logo-white.png` (su fondo scuro, alto 10 mm in copertina). PNG con fondo trasparente.
- **Controllo**: rifai `render.sh` sul template e guarda la copertina: l'accento deve restare
  leggibile su bianco (testi piccoli in `--accent-dk`) e sul blu scuro della copertina.

## Requisiti

- Google Chrome (o Chromium) per il render.
- Font **Inter**: caricato da Google Fonts; se installato in locale, si usa quello (anche
  offline). La variante "Inter Display" per i titoli è opzionale.
- `pdfinfo` / `pdftoppm` (poppler) per il controllo pagine e le anteprime: facoltativi.

