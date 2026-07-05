# Outbound & ABM Execution Skill

Esecuzione campagne Account-Based Marketing e sequenze outbound personalizzate. Usata da Sales, Marketing, CEO.

## Principi

1. **Personalizzazione estrema**: ogni messaggio deve sembrare scritto a mano per quel prospect specifico. Zero template generici. Ricerca l'azienda, il ruolo, i trigger event prima di scrivere
2. **Trigger events prima di tutto**: non contattare a freddo — aspetta (o cerca) un trigger: NIS2 deadline, breach nel settore, cambio CEO, crescita organico, nuovo round, evento di settore
3. **CEO brand su LinkedIn = canale #1**: il founder che condivide insight genuini genera piu pipeline di qualsiasi campagna outbound tradizionale. Ogni sequenza include un layer LinkedIn
4. **Value-first, pitch-last**: i primi 3 touchpoint danno valore (insight, dati, contenuti). La proposta arriva solo dopo aver stabilito credibilità
5. **Multi-canale coordinato**: LinkedIn + email + eventi + referral. Mai un solo canale
6. **Persistence senza spam**: 8 touchpoint in 8 settimane, poi nurture mensile. Mai piu di 1 touch/settimana nella sequenza attiva
7. **Voce umana, no AI-slop**: ogni email/messaggio passa il quick-check anti-slop prima dell'invio. No filler ("Spero che tu stia bene"), no voce passiva, no em-dash, no dichiarazioni vaghe. Vedi [`os/skills/writing/SKILL.md`](../writing/SKILL.md#anti-ai-slop-rules) (regole) e [`os/skills/writing/references/`](../writing/references/) (dettaglio EN + esempi)

---

## Comandi

| Comando | Descrizione | Output |
|---------|------------|--------|
| `sequence` | Sequenza outreach 8 settimane per account specifico | Piano in `company/commerciale/sequences/` |
| `email-template` | Template email personalizzato per tipo specifico | File in `company/commerciale/email-templates/` |
| `linkedin-sequence` | Piano LinkedIn completo (connection + messaggi + content) | Piano in `company/commerciale/sequences/` |
| `tracking` | Stato di tutte le sequenze attive | Report |
| `nurture-plan` | Piano nurture per prospect non convertiti | Piano in `company/commerciale/sequences/` |

---

## Comando: sequence

### Input
- Nome azienda target
- Contatto (nome, ruolo, LinkedIn URL se disponibile)
- Tipo partner (es. `segment-a` / `segment-b` / MSP-MSSP — l'ICP reale vive in `config/company.yaml`)
- Trigger event (perchè ora? cosa è successo?)
- Referral disponibile? (chi ci puo introdurre)

### Struttura sequenza 8 settimane

| Settimana | Canale | Tipo touchpoint | Obiettivo |
|-----------|--------|----------------|-----------|
| 1 | LinkedIn | **Warm-up**: engage con contenuto del prospect (like, commento, share) | Visibilità, familiarità |
| 2 | LinkedIn | **Connection request**: personalizzata, NO pitch, riferimento al trigger event | Connessione accettata |
| 3 | Email | **First touch**: valore puro — insight, dato, report rilevante per il loro settore | Apertura + click |
| 4 | LinkedIn | **Value message**: condividi contenuto CEO relevant (post, articolo, case study) | Engagement, risposta |
| 5 | Email | **Social proof**: caso simile (partner dello stesso segmento/size), risultati concreti | Credibilità, interesse |
| 6 | LinkedIn + Email | **Proposta soft**: "Stiamo lavorando con [simile a te] su [problema]. Ti interessa capire come?" | Meeting request |
| 7 | Email | **Follow-up diretto**: "Hai avuto modo di vedere il mio messaggio? Ti propongo 15 min" | Risposta, meeting |
| 8 | LinkedIn | **Nurture hook**: contenuto di alto valore + "Se non è il momento giusto, no problem — resto in contatto" | Porta aperta per nurture |

### Output format
```markdown
# Outbound Sequence — {azienda}

## Target
- Azienda: {nome}
- Contatto: {nome}, {ruolo}
- Tipo: {segmento — es. segment-a/segment-b/MSP}
- Trigger event: {descrizione}
- Referral: {nome o "Nessuno — cold outreach"}

## Timeline

### Settimana 1 — LinkedIn Warm-up
**Azione**: [Azione specifica con il post/contenuto del prospect da engagare]
**Messaggio**: —
**Obiettivo**: Apparire nel feed, creare familiarità

### Settimana 2 — Connection Request
**Canale**: LinkedIn
**Messaggio**:
> Ciao {nome}, ho visto il tuo [post/intervento/articolo] su [topic]. Lavoro nel nostro settore per {tipo partner} e mi piacerebbe connetterci — {riferimento trigger event}. {firma CEO}

**Obiettivo**: Connessione accettata

### Settimana 3 — First Touch (Email)
**Subject**: {subject personalizzato — max 6 parole, no clickbait}
**Body**:
> [Max 150 parole. Apri con il trigger event. Condividi 1 dato/insight rilevante. Chiudi con link a risorsa utile. ZERO pitch.]

**CTA**: Link a report/contenuto

[... settimane 4-8 ...]

## Contenuti necessari
| Settimana | Contenuto | Esiste? | Path / Azione |
|-----------|-----------|---------|---------------|
| 3 | Report settore {tipo} | Si/No | {path o "Creare con /marketing"} |
| 5 | Case study {segmento} | Si/No | {path o "Creare"} |

## Metriche tracking
| Settimana | Canale | Azione | Status | Risposta |
|-----------|--------|--------|--------|----------|
| 1 | LinkedIn | Warm-up | — | — |
| 2 | LinkedIn | Connection | — | — |
[...]
```

Salva in: `company/commerciale/sequences/sequence-{slug-azienda}-{YYYY-MM-DD}.md`
Commit: `[sales] outbound: sequence for {azienda}`

---

## Comando: email-template

### Input
- Tipo template (vedi lista sotto)
- Contesto: per chi, quale trigger, quale segmento

### 9 Tipi di Template

| # | Tipo | Quando usarlo | Tono |
|---|------|--------------|------|
| 1 | `cold-intro` | Primo contatto senza referral | Curioso, umile, valore immediato |
| 2 | `value-share` | Condividere insight/dato/report | Generoso, esperto, zero pitch |
| 3 | `case-study` | Social proof con risultato concreto | Concreto, numeri, credibile |
| 4 | `roi-model` | Mostrare il ritorno economico | Analitico, personalizzato, provocativo |
| 5 | `meeting-request` | Chiedere una call | Diretto, rispettoso del tempo, specifico |
| 6 | `follow-up` | Dopo un touchpoint senza risposta | Breve, aggiunge valore, non insistente |
| 7 | `post-event` | Dopo aver incontrato a un evento | Personale, riferimento specifico, rapido |
| 8 | `referral-ask` | Chiedere un'introduzione | Contestuale, facile dire si |
| 9 | `trigger-event` | Reagire a un evento (breach, NIS2, funding) | Tempestivo, empatico, utile |

### Regole per ogni template
- **Max 150 parole** nel body
- **1 solo CTA** (chiaro, specifico, bassa friction)
- **Subject**: max 6 parole, no emoji, no clickbait, no maiuscolo
- **Opening**: mai "Spero che tu stia bene", mai "Mi chiamo X e faccio Y". Apri con il prospect, non con te
- **Personalizzazione**: almeno 1 elemento specifico del prospect (azienda, ruolo, evento, post)
- **Firma**: nome + ruolo + 1 riga di context ("Aiutiamo [tipo partner] a [risultato]")
- **Anti-slop check**: prima di salvare, scorri i Quick Checks di [`os/skills/writing/SKILL.md`](../writing/SKILL.md#anti-ai-slop-rules). Tagliare avverbi (`really`, `just`, `simply`), voce passiva, em-dash, throat-clearing openers ("Here's the thing"), contrasti binari ("non X, è Y"), false agency ("la decisione emerge")

### Output format
```markdown
# Email Template: {tipo}

## Contesto
- Per: {segmento/ruolo}
- Trigger: {evento specifico}
- Obiettivo: {cosa deve fare il destinatario}

## Template

**Subject**: {subject}

**Body**:
> {Max 150 parole}

**CTA**: {azione specifica}

## Varianti
- Variante A (piu diretta): [...]
- Variante B (piu soft): [...]

## Note di personalizzazione
- Sostituire [{campo}] con dati specifici del prospect
- Se disponibile referral, aprire con "Mi ha suggerito di scriverti {nome referral}"
```

Salva in: `company/commerciale/email-templates/{tipo}-{contesto}-{YYYY-MM-DD}.md`
Commit: `[marketing] template: {tipo} email for {contesto}`

---

## Comando: linkedin-sequence

### Input
- Profilo target (nome, ruolo, azienda)
- Durata (default: 4 settimane)

### Processo
1. **Connection strategy**: messaggio personalizzato per la richiesta
2. **Messaging sequence**: 3-4 messaggi diretti post-connessione
3. **Content plan**: quali post del CEO far vedere / commentare / condividere
4. **Engagement plan**: come interagire con i contenuti del prospect

### Output format
```markdown
# LinkedIn Sequence — {nome}, {azienda}

## Connection Request
> {Messaggio — max 300 caratteri}

## Post-Connection Messages
### Giorno 2 (dopo accettazione)
> {Messaggio di ringraziamento + domanda aperta — NO pitch}

### Giorno 7
> {Valore: condividi insight o contenuto}

### Giorno 14
> {Social proof + soft ask}

### Giorno 21
> {Meeting request diretto}

## CEO Content Plan
| Settimana | Post da pubblicare | Obiettivo |
|-----------|-------------------|-----------|
| 1 | {Topic rilevante per il prospect} | Visibilità nel feed |
| 2 | {Case study o dato} | Credibilità |
| 3 | {Opinione su trend del settore} | Thought leadership |

## Engagement Plan
- Like: ogni post del prospect
- Commento: 1-2 commenti sostanziali/settimana su contenuti del prospect o del suo network
- Share: condividere 1 contenuto del prospect con commento del CEO
```

Salva in: `company/commerciale/sequences/linkedin-{slug}-{YYYY-MM-DD}.md`
Commit: `[marketing] outbound: LinkedIn sequence for {nome}`

---

## Comando: tracking

### Processo
1. Scansiona `company/commerciale/sequences/*.md`
2. Per ogni sequenza, leggi la tabella "Metriche tracking"
3. Genera report aggregato

### Output format
```
## Outbound Tracking — {data}

### Sequenze attive
| Account | Contatto | Settimana | Ultimo touch | Risposta | Next step |
|---------|----------|-----------|-------------|----------|-----------|
| {azienda} | {nome} | 4/8 | Email value | Aperta, no reply | Case study sett 5 |

### Summary
- Sequenze attive: {N}
- Risposte ottenute: {N} ({%})
- Meeting fissati: {N}
- In nurture: {N}

### Azioni richieste
1. {Account}: {azione}
```

---

## Comando: nurture-plan

### Input
- Lista prospect che non hanno risposto alla sequenza attiva

### Processo
1. Per ogni prospect non convertito:
   - 1 touch al mese (alternando email e LinkedIn)
   - Contenuto di valore (mai pitch)
   - Monitorare trigger event per riattivare sequenza
2. Genera piano 6 mesi

### Output format
```markdown
# Nurture Plan — {data}

## Prospect in nurture
| Prospect | Azienda | Ultima interazione | Motivo non-conversione |
|----------|---------|-------------------|----------------------|
| {nome} | {azienda} | {data} | {motivo} |

## Piano mensile
### Mese 1
| Prospect | Canale | Contenuto | Trigger da monitorare |
|----------|--------|-----------|---------------------|
| {nome} | Email | Report Q1 cybersecurity | NIS2 deadline, breach settore |

### Mese 2
[...]

## Regole di riattivazione
- Trigger event rilevante → ripartire da sequenza settimana 3
- Risposta positiva → passare a Sales per follow-up diretto
- Opt-out esplicito → rimuovere dal nurture
```

Salva in: `company/commerciale/sequences/nurture-{YYYY-MM-DD}.md`
Commit: `[marketing] nurture: updated nurture plan`

---

## Integrazione CEO Cadence

### Settimanale
- **Outbound tracking**: summary sequenze attive, risposte, meeting fissati nella settimana
- Alert se nessuna sequenza attiva o nessun touchpoint nella settimana

### Mensile
- Review pipeline outbound completa
- Nurture plan refresh
- Content gap per sequenze (contenuti necessari ma mancanti)

---

## Dove vivono i dati

| Dato | Path |
|------|------|
| Sequenze outbound | `company/commerciale/sequences/sequence-*.md` |
| Sequenze LinkedIn | `company/commerciale/sequences/linkedin-*.md` |
| Email template | `company/commerciale/email-templates/*.md` |
| Nurture plan | `company/commerciale/sequences/nurture-*.md` |
| Content index (per `reuse`) | `company/marketing/content-index.md` |
| Partner (per personalizzazione) | `20-Clienti/*/overview.md` |
| Segmenti (per targeting) | `company/commerciale/segments.md` |
| **PoC kickoff deck** (asset standard per attivare un nuovo prospect dopo meeting di qualifica) | `90-Condivisi/template-deliverable/company-poc-kickoff.pptx` (sorgente: `gen_poc_kickoff_deck.py`) |
