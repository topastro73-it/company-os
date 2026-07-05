# Memory — memoria a tre strati

| Strato | Dove | Risponde a |
|---|---|---|
| **Stato** | zone operative (Drive) + snapshot `company/` / `vault/` | "Com'è la situazione?" |
| **Storia** | `system/wiki/` (git) | "Come ci siamo arrivati? Perché così?" |
| **Regole** | `system/learnings.md` (git) | "Cosa abbiamo imparato da ricordare?" |

I tre strati restano separati: mai stato duplicato in wiki, mai narrativa nei file di stato.

## 1. Persistent memory — intercetta e proponi

Durante ogni conversazione, intercetta i dati di business concreti emersi e proponi di
salvarli nel file di zona giusto. **Chiedi sempre prima di salvare**, una sola domanda
raggruppata a fine risposta, indicando il file di destinazione:

```
💾 Dati da salvare:
- MRR giugno: €X → company/direzione/metrics/kpis.md
- DNA: pilot annex firmato → 20-Clienti/dna/note.md
Salvo tutto, scegli quali, o no?
```

| Tipo di dato | Destinazione (zona) |
|---|---|
| Metrica / KPI | `direzione` → metrics/kpis.md |
| Decisione presa | `direzione` → decisions/YYYY-MM-DD-slug.md (vedi `decisions.md`) |
| Info cliente/partner | `clienti` → `20-Clienti/{slug}/` |
| Deal / opportunità | `commerciale` → pipeline/opportunities |
| Cambio strategia / OKR | `direzione` → strategy |
| Pricing | `commerciale` (listino) / `finance` se 🔴 |
| Scadenza, costo, fattura | `finance` → scadenzario / costi (🔴, vault) |
| Stato spec/feature | `prodotto` → specs + roadmap |
| Team / persone | `config/people.yaml` (via admin) |
| Competitor | `commerciale` → battlecards |

Regole: non chiedere per ipotesi/esplorazioni/dati già salvati; se "salva tutto" → salva e
conferma con lista file; se "no" → non insistere. **Eccezione critica (LRN-018)**: correzioni
a obblighi finanziari (scadenza cancellata, importo cambiato) si persistono **subito**, non
al close — lo stato stale rigenera il dato sbagliato nelle sessioni successive.

## 2. Wiki — la storia (`system/wiki/`)

Cattura il **perché**: decisioni, ragionamento, domande aperte, promesse. Non è un transcript.

Struttura (dettaglio in `system/wiki/README.md`):
- `sessions/{YYYY-MM-DD}-{slug}.md` — una pagina per sessione, generata **al close** (mai inventata durante)
- `entities/clients/{slug}.md` — solo timeline narrativa del cliente; lo **stato** (stage,
  valore, owner, blocker) vive nella zona `commerciale`/`clienti` — la entity page linka, non duplica
- `entities/features/{slug}.md`, `entities/decisions/{slug}.md`, `entities/concepts/{slug}.md`
- `index.md` — ultime 20 sessioni + entity pages

Regole:
- Tutti i file wiki in **inglese**
- Estrai dal flusso reale della conversazione, non riassunti generici
- Entity pages crescono per accumulo (timeline), non si sovrascrivono
- Promesse con deadline scaduta → URGENZE del briefing successivo
- **Pseudonimizzazione**: clienti finali come iniziali + ruolo; mai IBAN/CF/compensi (vedi
  `zones-and-permissions.md` §6)

## 3. Learnings — le regole (`system/learnings.md`)

Il wiki dice "il 15/3 {cliente} ha rallentato ed era enablement"; il learning dice "quando un
partner rallenta, verifica prima il training venditori". Formato:

```markdown
### LRN-XXX: Titolo
- **Rule**: When [situazione], [cosa fare].
- **Source**: Session YYYY-MM-DD — [[session-slug]]
- **Applied**: N times (contesti)
- **Tags**: tag1, tag2
- **Status**: active | archived
```

**Quando proporre**: al close, max 2 pattern generalizzabili per sessione. L'umano approva,
modifica o scarta — mai salvare senza conferma. Regole astratte, mai personalizzate sul nome
del cliente.

**Apply-loop**:
- Allo start la sessione carica gli LRN attivi; all'inizio di un comando d'agente carica
  quelli del dominio (tag: sales, product, finance, compliance, …)
- Quando un task corrisponde a un learning: intervieni proattivamente —
  `⚡ Da esperienza passata (LRN-XXX): "{regola}". Suggerisco {azione}.` Max 1 per intervento.
- **Ogni applicazione incrementa `Applied: N times`** nel commit della sessione. Senza
  contatore l'apply-loop è inerte; il health check segnala 🔴 se ≥60% degli LRN attivi è a 0.
- Learnings obsoleti → `Status: archived` con motivo, mai eliminati.

**Anti-deriva (candidati non promossi)**: proporre non basta — serve decisione esplicita.
Allo start e al close, scansiona le wiki-session degli ultimi 30 giorni: ogni candidato
(`## Proposed learning`) deve risultare promosso (LRN in `learnings.md` o nota
`→ promosso come LRN-XXX`) oppure scartato (`→ scartato {data}`). I candidati appesi vengono
ri-flaggati finché non decisi.
