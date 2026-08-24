# /admin setup — Intervista iniziale: da repo clonato a istanza configurata

## Scopo
Portare una persona **non necessariamente tecnica** da "ho clonato il repo" a "il sistema sa chi
siamo, chi lavora qui e con quali strumenti". È il passo 0 di `bootstrap/README.md`: tutto il resto
(Shared Drive, ACL, snapshot) viene dopo e presuppone questo.

## Input
Nessuno. Si attiva quando `config/company.yaml` non esiste, oppure su richiesta esplicita.

---

## Come si conduce (regole non negoziabili)

Queste regole valgono più del contenuto delle domande. Un'intervista fatta male fa abbandonare
il setup, e un setup abbandonato lascia un sistema che mente su se stesso.

1. **Una domanda alla volta.** Mai un questionario. Aspetta la risposta prima della successiva.
2. **Nessun gergo senza traduzione.** Chi risponde può non sapere cosa sia un service account,
   una ACL o un MCP. Se un termine serve, spiegalo in mezza riga *quando lo usi*, non prima.
3. **"Non lo so" è sempre una risposta valida**, e va offerta esplicitamente. Registra
   `da confermare` e vai avanti. Non insistere mai due volte sulla stessa domanda.
4. **Scrivi mentre procedi**, non alla fine. Dopo ogni fase salva quello che hai raccolto. Se la
   sessione si interrompe, chi torna riprende da dove era rimasto e non ripete nulla.
5. **Proponi, non chiedere a vuoto.** Quando serve una scelta, offri le opzioni che il sistema già
   supporta (§3) invece di lasciare il campo aperto. "Che gestionale usi?" è una domanda difficile;
   "usi Fatture in Cloud, un altro, o niente per ora?" è facile.
6. **Non chiedere quello che puoi dedurre.** Nome del repo, sistema operativo, presenza di `git`,
   fuso: leggili. Chiedi conferma solo se la deduzione conta.
7. **Niente segreti in chat.** Token, password e chiavi non si dettano: si mettono in `.env` o nel
   keychain. Tu scrivi solo il *nome* della variabile in `config/integrations.yaml`. Se qualcuno
   incolla un secret in chat, dillo subito e chiedi di ruotarlo.
8. **Mai bloccare.** Ogni cosa non risolta diventa una riga nel recap finale (§6), non un muro.

---

## Fase 0 — Lingua

Prima domanda in assoluto, prima di generare qualsiasi file (`os/protocols/language.md` §1):

> 🌐 In che lingua vuoi lavorare? / Which language do you want to work in? [italiano / english]

Scrivi `config/company.yaml → language` copiando `config/company.example.yaml`. Da qui in avanti
tutta l'intervista e ogni file generato usano quella lingua.

## Fase 1 — Chi siete

Cinque domande, in quest'ordine. Dopo ognuna scrivi il campo.

| # | Domanda | Dove finisce |
|---|---------|--------------|
| 1 | Come si chiama l'azienda? | `company.yaml → name` |
| 2 | In una riga: cosa fate e per chi? | `company.yaml → one_liner` + `zones/_root/context/COMPANY.md` |
| 3 | Vendete ad aziende, a consumatori, o entrambi? E passate da rivenditori/partner? | `company.yaml → positioning.model` |
| 4 | Quali sono i vostri due o tre tipi di cliente principali? (nomi vostri, non categorie standard) | `company.yaml → segments` |
| 5 | C'è un settore regolamentato che vi condiziona? (es. sanità, finanza, sicurezza; oppure nessuno) | `zones/_root/context/COMPANY.md` |

Sulla 4: sono le etichette che compariranno in tutta la pipeline commerciale. Se non le hanno
ancora, va bene `segment-a`, `segment-b`: si rinominano dopo, e diglielo.

## Fase 2 — Chi ci lavora

> 👥 Chi userà il sistema, oltre a te? Per ognuno mi serve nome, email di lavoro e di cosa si occupa.
> Se sei solo per ora, va benissimo: si aggiungono quando arrivano.

Per ogni persona scrivi una riga in `config/people.yaml` (da `people.example.yaml`), mappando
"di cosa si occupa" su una zona e un agente di default. Non chiedere "quale zona": deducila e
mostra la mappatura per conferma alla fine della fase.

⚠️ **L'email è obbligatoria** se la persona dovrà accedere alle cartelle: senza, `osctl` la salta
quando imposta i permessi. Se non la sanno, segna `da confermare` e ricordalo nel recap.

Chiudi la fase mostrando la tabella persona → zona → agente e chiedendo un solo "va bene?".

## Fase 3 — Con che strumenti lavorate

È la fase che decide quanto il sistema sarà utile il primo giorno. Va condotta **per categoria**,
proponendo ogni volta cosa il template già porta. Formula sempre così:

> Usate {categoria}? [{opzione supportata} / un altro / non ancora]

Se rispondono con qualcosa che supportiamo, **attiva** (scrivi la sezione in
`config/integrations.yaml`, dì quale variabile d'ambiente serve e dove metterla, e indica lo
script o la skill già pronta). Se rispondono "un altro", registra il nome e dì onestamente che
l'integrazione non c'è ma il posto dove aggiungerla è quello. Se "non ancora", salta e basta.

| Categoria | Domanda | Se sì, cosa attivi | Cosa portiamo già |
|---|---|---|---|
| **Conto aziendale** | Usate Qonto, un'altra banca, o niente da collegare? | `integrations.yaml → banca` | `scripts/integrations/bank-qonto.sh` + `bank_qonto_sync.py` (sola lettura, saldi e movimenti) · skill `qonto` |
| **Fatturazione / ERP** | Come emettete fattura? Fatture in Cloud, altro gestionale, commercialista? | `integrations.yaml → fatturazione` | skill `fatture-in-cloud`, `erp`, `financial-import` |
| **Pagamenti ricorrenti** | Incassate con Stripe o simili? | `integrations.yaml → stripe` | skill `stripe` (MRR, churn, riconciliazione payout) |
| **CRM** | Dove tenete le trattative oggi? HubSpot, un foglio, la testa? | `integrations.yaml → hubspot` | skill `opportunity-management`: **la pipeline vive nel repo**, il CRM esterno è opzionale e fa da specchio |
| **Task / progetti** | Usate ClickUp, Jira, Asana, Trello, altro? | `integrations.yaml → clickup` | skill `clickup` (epic, task, doc) |
| **Email** | Su cosa gira la posta di lavoro? Google Workspace, Microsoft, altro? | `integrations.yaml → gmail` | skill `gmail` (contesto in lettura; bozze solo dopo approvazione) |
| **Documenti condivisi** | Dove vivono oggi i file dell'azienda? | `config/acl.yaml` | è il piano operativo del sistema: vedi Fase 4 |
| **Compliance** | Avete certificazioni in corso o richieste dai clienti? (ISO 27001, SOC 2, GDPR, NIS2, nessuna) | `zones/_root/context/COMPANY.md` | agente `compliance`, skill `audit-compliance` |

Chiudi la fase con: *"Tutto quello che non abbiamo collegato si aggiunge in qualsiasi momento
dicendomelo. Non serve rifare il setup."*

## Fase 4 — Il piano operativo (Google Drive)

Qui si alza il livello tecnico, e va detto prima:

> Il sistema tiene la parte "cervello" qui nel repo e la parte "operativa" in una cartella Drive
> condivisa, dove ognuno vede solo ciò che gli compete. Per crearla servono due cose che di solito
> fa chi vi gestisce l'IT: uno Shared Drive e un accesso tecnico per il sistema.
> Vuoi che ti guidi passo passo adesso, oppure preferisci che prepari le istruzioni da girare a chi
> se ne occupa?

- **"Guidami"** → segui `bootstrap/README.md` §1-§3 un passo alla volta, aspettando conferma a ogni
  passo. Non incollare tre comandi insieme.
- **"Preparo le istruzioni"** → genera un file in `local/` con i passi §1-§2 e l'elenco esatto di
  cosa ti serve indietro (ID dello Shared Drive, email del service account, dove hanno salvato la
  chiave). Poi chiudi il setup: il resto si fa quando quei dati arrivano.

In entrambi i casi **non serve** aver finito questa fase per usare il sistema sul repo: dillo, e
proponi la Fase 5.

## Fase 5 — Verifica

Esegui e commenta in una riga ciascuno, tradotti in linguaggio comprensibile:

```bash
python3 tools/osctl/osctl.py status
python3 scripts/audit/link-lint.py
python3 scripts/audit/system-health.py
```

Se `status` segnala persone senza email, riportalo qui, non prima.

## Fase 6 — Recap e prossimo passo

Chiudi sempre con questo blocco, anche se l'intervista è stata interrotta a metà:

```
✅ Configurato
   Azienda: {nome} · lingua: {it|en} · {N} persone · {N} integrazioni collegate

⏳ Da completare (non blocca l'uso del sistema)
   • {cosa} — {chi/come}

▶️ Prossimo passo
   {il singolo passo successivo, uno solo}
```

Poi committa: `[admin] setup: istanza configurata — {nome azienda}`.

⚠️ `config/*.yaml` è gitignorato per scelta (contiene dati vostri): il commit riguarda solo ciò che
è finito in `zones/_root/context/`. Dillo, altrimenti sembra che il lavoro sia andato perso.

---

## Ripresa di un setup interrotto

All'apertura di una sessione, se `config/company.yaml` esiste ma è incompleto (campi vuoti o
`da confermare`), non ricominciare da capo:

> Il setup era arrivato a {fase}. Riprendiamo da lì? Restano {N} cose da chiudere.

## Guardrail

- **Mai inventare** un dato non fornito. Un campo vuoto è meglio di un campo plausibile e falso:
  tutti gli agenti leggeranno questo file come verità.
- **Mai chiedere un secret in chat** (§7 delle regole di conduzione).
- **Mai far partire `osctl bootstrap --apply`** senza aver mostrato prima il dry-run e ottenuto un sì.
- Se l'intervista supera i ~15 minuti, proponi tu una pausa: "il resto può aspettare, il sistema è
  già usabile".

## Destinazione
`config/company.yaml`, `config/people.yaml`, `config/integrations.yaml` (gitignorati),
`zones/_root/context/COMPANY.md`. Nessun report.
