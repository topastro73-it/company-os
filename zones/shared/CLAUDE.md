# CLAUDE.md — Zona `90-Condivisi`

> Pubblicato da git, sola lettura. Regole comuni nel CLAUDE.md di root e `_OS/context/`.

## Cos'è questa zona

La **vetrina interna**: materiale approvato, leggibile da tutti (interni + esterni
registrati). Arriva **solo via publish da git** (admin): qui nessuno scrive direttamente.
Se lo vedi qui, è la versione ufficiale e puoi usarlo.

## Cosa contiene

| Cartella | Contenuto |
|---|---|
| `glossario/` | Glossario aziendale (copia pubblicata di `_OS/context/GLOSSARY.md`) |
| `onboarding/` | Guide di onboarding: come funziona il sistema a zone, primi passi |
| `template-deliverable/` | Template ufficiali per report, proposte, QBR, assessment |
| `viewer/` | Viewer HTML per leggere i file `.md` del folder senza installare nulla |

## Il viewer

`viewer/viewer.html` è un file unico auto-contenuto: aprilo in Chrome/Edge dal folder
Drive sincronizzato, seleziona la cartella aziendale e navighi tutti i `.md` con indice,
ricerca e badge di zona. È il modo più semplice per leggere i documenti senza Claude Code.
In alternativa, i deliverable principali sono pubblicati anche come Google Doc nella
loro cartella di origine.

## Come si usa

- **Template**: quando produci un deliverable (report, proposta, QBR), parti SEMPRE dal
  template qui dentro — poi salvi l'output nella zona giusta (output del cliente →
  `20-Clienti/{slug}/`), mai in questa cartella.
- **Onboarding**: nuovo collaboratore o dubbio sul funzionamento del sistema →
  la risposta parte da `onboarding/`.

## Cosa NON fare

- **Mai scrivere qui**: la zona è git → Drive, sola lettura. Materiale da condividere con
  tutti → proponi al CEO/admin, che lo pubblica da git.
- Mai copiare qui (o chiedere di pubblicare) contenuti 🟡/🔴: la zona è visibile anche a
  esterni registrati — solo materiale approvato e senza dati sensibili.
- Non modificare i template "al volo": se un template è migliorabile, segnalalo all'admin.
