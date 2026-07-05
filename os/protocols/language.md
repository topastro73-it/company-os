---
zone: _os
tier: 🟡
---

# Protocollo lingua

La lingua operativa dell'istanza è **una sola fonte di verità**: `language` in
`config/company.yaml` (`it` | `en`). Governa tre cose: la lingua delle risposte in chat,
la lingua di **generazione** di ogni file markdown, e quale **variante** dei file di
sistema viene presentata.

## 1. Scelta all'avvio (setup di una nuova azienda)

Alla prima sessione su un'istanza non ancora configurata (manca `config/company.yaml`
o `language` non è impostata), **prima di generare qualsiasi cosa** chiedi:

> 🌐 In che lingua vuoi lavorare? / Which language do you want to work in? [italiano / english]

Scrivi la risposta in `config/company.yaml → language` (creando il file dalla copia di
`company.example.yaml` se serve). Da quel momento non richiederla più.

## 2. Cosa governa `language`

- **Risposte in chat**: sempre nella lingua configurata (salvo richiesta esplicita diversa).
- **Generazione file**: ogni output md (report, spec, proposte, briefing, wiki, decisioni)
  nasce nella lingua configurata. Eccezioni fisse, indipendenti dalla lingua:
  task ClickUp in inglese (`config/integrations.yaml → rules.task_language`),
  `system/wiki/` in inglese (protocollo memory).
- **Presentazione dei file di sistema**: i file di sistema hanno la versione italiana come
  base (`X.md`) e la variante inglese accanto (`X.en.md`). Con `language: en` carica e
  presenta la variante `.en.md` quando esiste (fallback: il file base); con `language: it`
  usa sempre il file base. `osctl publish` pubblica su Drive la variante giusta.

## 3. Cambio lingua in corsa

L'utente può cambiare lingua **in qualsiasi momento dicendolo in chat** (es. "passa
all'inglese", "switch to Italian"). Qualunque agente lo riceva:

1. Aggiorna `config/company.yaml → language` (modifica di config: commit
   `[admin] config: language → {lang}`; niente changelog di sistema, non è un file di sistema)
2. Esegui `osctl publish` così le zone Drive ricevono i CLAUDE.md e i contesti nella nuova lingua
3. Da subito: risposte e nuovi file nella nuova lingua. I file **già generati non si
   ritraducono** retroattivamente (si ritraducono on-demand se l'utente lo chiede per un file specifico)

## 4. Regole per le varianti `.en.md`

- Si crea una variante solo se il file base è in italiano; se un file è già in inglese,
  niente variante (il fallback lo copre).
- Le varianti sono **traduzioni fedeli**: stessa struttura, stessi path/zone/comandi/chiavi
  di config (mai tradotti), stessi guardrail. Cambia solo la prosa.
- Chi modifica un file di sistema aggiorna anche la variante nello stesso commit
  (il link-lint non lo impone; è responsabilità dell'admin — in dubbio, rigenera la variante).
