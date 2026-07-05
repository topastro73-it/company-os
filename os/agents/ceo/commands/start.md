# /ceo start — Apertura sessione admin

## Scopo
Aprire la giornata del CEO: contesto ricostruito, alert in evidenza, 3 priorità chiare.

## Input
Nessuno (implicito: prima interazione della sessione admin).

## Passi
1. **Stale session check**: se l'ultima sessione in `direzione/ceo-cadence.md` non ha una
   pagina in `system/wiki/sessions/`, proponi recovery (full / stub / skip-and-log) PRIMA del briefing.
2. **Ritmo**: determina da `direzione/ceo-cadence.md` se scatta giornaliero / settimanale / mensile.
3. **Dove eravamo rimasti**: ultima pagina wiki → decisioni, domande aperte, promesse scadute (3-5 righe).
4. **Learnings**: carica `system/learnings.md`, applica proattivamente durante la sessione.
5. **Scansione alert** (dagli snapshot di zona; se stale, segnala e suggerisci `osctl snapshot`):
   - `vault/finance/`: scadenze fiscali ≤3gg, fatture scadute 30+gg
   - zona `commerciale`: opportunità 🔴/🟠 (aging in lettura), deal senza owner
   - zona `clienti`: partner Critical/At-Risk (health score), onboarding in ritardo
   - zona `compliance`: scadenze ≤7gg, audit ≤30gg, evidenze mancanti
   - zona `prodotto`: spec stale, decisioni in attesa del CEO
6. **Componi il briefing** (formato sotto) e **poni le domande** del ritmo attivo.
7. **Registra le risposte** in `direzione/ceo-cadence.md` e aggiorna i file di zona toccati.
8. Chiudi con: "cosa vuoi fare oggi?" → handoff all'agente richiesto.

## Formato output (in chat, non file)
```
🟣 **[Claude]**
Buongiorno {nome}. Ecco la tua giornata.

QUICK STATUS — decisioni in attesa: N · follow-up scaduti: N · partner alert: N ·
deal 🔴: N · scadenze fiscali 3gg: N · fatture scadute 30+gg: N

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
