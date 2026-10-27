# /ceo start — Apertura sessione admin

## Scopo
Aprire la giornata del CEO: contesto ricostruito, alert in evidenza, 3 priorità chiare.

## Input
Nessuno (implicito: prima interazione della sessione admin).

## Passi
1. **Stale session check**: se l'ultima sessione in `direzione/ceo-cadence.md` non ha una
   pagina in `system/wiki/sessions/`, proponi recovery (full / stub / skip-and-log) PRIMA del briefing.
2. **Cadence freshness check** (il controllo inverso del passo 1): confronta la data più recente in
   `direzione/ceo-cadence.md` con quella del file più recente in `system/wiki/sessions/`. Se la wiki è
   avanti di **oltre 5 giorni**, il cadence log è stale, cioè sono state lavorate sessioni senza
   registrarle:
   ```
   ⚠️ Cadence log fermo al {data-cadence}, ultima sessione reale {data-wiki} — lo riallineo a oggi?
   ```
   Se il CEO conferma → aggiorna solo le date correnti sul Drive (zona `direzione`, drive_master),
   senza backfillare la storia persa salvo richiesta esplicita. Il passo 1 rileva la sessione lavorata
   senza wiki; questo rileva la wiki scritta senza cadence.
3. **Ritmo**: determina da `direzione/ceo-cadence.md` se scatta giornaliero / settimanale / mensile.
4. **Dove eravamo rimasti**: ultima pagina wiki → decisioni, domande aperte, promesse scadute (3-5 righe).
5. **Learnings**: carica `system/learnings.md`, applica proattivamente durante la sessione.
6. **Scansione alert** (dagli snapshot di zona; se stale, segnala e suggerisci `osctl snapshot`):
   - `vault/finance/`: scadenze fiscali ≤3gg, fatture scadute 30+gg
   - zona `commerciale`: opportunità 🔴/🟠 (aging in lettura), deal senza owner
   - zona `clienti`: partner Critical/At-Risk (health score), onboarding in ritardo
   - zona `compliance`: scadenze ≤7gg, audit ≤30gg, evidenze mancanti
   - zona `prodotto`: spec stale, decisioni in attesa del CEO
7. **Standup COO** (Org-OS): segui `os/agents/coo/commands/standup.md` sui goal attivi del
   ledger (zona `direzione`, sottozona `ops`; in admin sul mount Drive, altrimenti lo snapshot
   `company/direzione/ops/`). Per ogni goal: ondata corrente, WO bloccati (motivo + via
   d'uscita), checkpoint in attesa di firma, proposta per la prossima ondata. Scrivi
   `00-Direzione/ops/standup/YYYY-MM-DD.md`, esegui `python3 scripts/audit/ledger-check.py --drive`,
   copia nello snapshot ed esegui `python3 scripts/audit/ledger-check.py`. Ledger assente → salta
   il passo e scrivi "nessun goal attivo". I blocchi entrano in URGENTE se chiedono una firma o una
   decisione del CEO.
8. **Componi il briefing** (formato sotto) e **poni le domande** del ritmo attivo.
9. **Registra le risposte** in `direzione/ceo-cadence.md` e aggiorna i file di zona toccati.
   ⚠️ Questo passo **non è più l'unico punto di scrittura** del cadence log: la scrittura obbligatoria
   è al passo 3 di `/ceo close`. Qui si registra ciò che emerge durante il briefing, ma se la sessione
   prosegue e questo passo salta, il close recupera comunque.
10. Chiudi con: "cosa vuoi fare oggi?" → handoff all'agente richiesto.

## Formato output (in chat, non file)

Eccezione: lo **standup COO** del passo 7 è un file del ledger (`ops/standup/YYYY-MM-DD.md`,
formato in `os/agents/coo/commands/standup.md`); in chat ne va solo la riga `GOAL ATTIVI`.

```
🟣 **[Claude]**
Buongiorno {nome}. Ecco la tua giornata.

QUICK STATUS — decisioni in attesa: N · follow-up scaduti: N · partner alert: N ·
deal 🔴: N · scadenze fiscali 3gg: N · fatture scadute 30+gg: N
GOAL ATTIVI: N · WO bloccati: N · checkpoint da firmare: N (standup: ops/standup/YYYY-MM-DD.md)

URGENTE (risposta ORA)
1. [cosa] — [1 riga contesto] — [opzioni A/B/C]

LE TUE 3 PRIORITÀ PER OGGI
1. [priorità] — perché: [motivo]

UNA DOMANDA PER TE
[la domanda più importante che nessuno ti sta facendo]
```
Il ritmo settimanale aggiunge: review settimana scorsa, spec status, admin & finance,
metriche stale, priorità della settimana. Il mensile aggiunge: retrospettiva risultati,
non-fatto, rischi (OKR, partner, runway), 3 domande strategiche.

## Destinazione
Zona `direzione` — aggiornamenti a `ceo-cadence.md` e `ceo-routine.md`. Nessun report file.
