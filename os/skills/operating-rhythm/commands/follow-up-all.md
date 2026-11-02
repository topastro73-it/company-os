---
status: attivo
area: sistema
---

# Command: follow-up-all

## Trigger
"segui i miei meeting", "smaltisci i follow-up", "quali meeting non hanno la minuta", o un run
schedulato "prepara le minute dei meeting di ieri".

## Scopo
Smaltire, uno alla volta, i meeting della persona rimasti senza minuta. Per i follow-up promessi
e scaduti (impegni aperti) c'è `/cos follow-up-tracker`. Fonti e regole in `../SKILL.md`.

## Processo
1. **Trova i meeting in sospeso** — sempre tutte le trascrizioni delle fonti configurate degli
   ultimi 14 giorni (o del periodo chiesto), filtrate per pertinenza e già-importato come in
   `../SKILL.md` § Transcript; più gli eventi Calendar con esterni senza trascrizione né minuta.
   Senza fonti raggiungibili né Calendar: dillo e chiedi alla persona l'elenco.
2. Mostra la lista dal più vecchio: data, titolo, account (o "account da definire"), trascrizione
   sì/no, pertinenza (sì / parziale / dubbia). In fondo una riga sola: "N meeting di altre aziende
   esclusi" (senza titoli). I dubbi si chiedono qui, insieme agli account da definire. Chiedi: tutti o solo alcuni? Gli account da definire si chiedono subito, con una sola
   domanda che li elenca tutti.
3. Per ogni meeting scelto, la procedura di `publish-call` (bozza → un "ok" → scrivi). Bozze
   brevi; dopo le prime due, se la persona approva senza modifiche, proponi "ok a tutti i restanti".
4. Meeting senza nulla da registrare (annullato, solo saluti): annotalo nel report, nessun file.
5. Bilancio finale: minute scritte N, saltati N (perché), ancora in sospeso N.

## Modalità schedulata
Prepara le bozze dei meeting di ieri e **fermati prima di scrivere**: presentale come un'unica
lista da approvare.

## Regole
Mai dedurre un account. Mai assegnare task: i task ClickUp nascono in staging per l'approvazione.
