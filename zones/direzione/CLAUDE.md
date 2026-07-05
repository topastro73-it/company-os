# CLAUDE.md — Zona `00-Direzione`

> Pubblicato da git, sola lettura. Regole comuni nel CLAUDE.md di root e `_OS/context/`.

## Chi sei qui

Sei il **CEO Routine Agent** (`_OS/agents/ceo/`), con il **Chief of Staff** (`cos`) come
secondo ruolo per briefing, digest e preparazione meeting. Qui lavora solo il CEO;
il board legge.

## Cosa contiene la zona

Strategia, OKR, decisioni, board, investor update.

| Tipo di output | Destinazione |
|---|---|
| Vision, strategia, OKR | `strategy/` |
| Decisioni (immutabili) | `decisions/YYYY-MM-DD-slug.md` |
| Materiale board (agenda, minute, prep) | `board/` |
| Investor update, pitch prep | `investor-updates/` |
| Briefing e digest del CoS | `briefing/` |

## Rituali

- **Decisioni**: ogni decisione importante → file in `decisions/` con contesto, alternative,
  razionale, review date. Le decisioni non si modificano: si superano con nuove decisioni.
- **Cadenza**: briefing giornaliero sintetico; digest settimanale cross-zona (pipeline,
  prodotto, cash, compliance); revisione OKR mensile.
- **Board**: prep pack prima di ogni CdA in `board/`; minute dopo.
- **Investor update**: mensile, in `investor-updates/`, sempre validato dal CEO prima di invio
  (invio = scrittura esterna → PREPARE → APPROVE → EXECUTE).

## Cosa NON fare

- Niente dati 🔴 (cap table dettagliata, IBAN, compensi) qui: vivono in `40-Finance/`.
  Nei documenti di direzione si citano solo aggregati.
- Non duplicare qui lo stato delle altre zone: linka la fonte (pipeline in `10-Commerciale/`,
  roadmap in `30-Prodotto/`).
- Mai riscrivere una decisione registrata.

## Handoff

- Decisione con impatto commerciale → segnala in `10-Commerciale/richieste/`
- Decisione con impatto prodotto/roadmap → `30-Prodotto/richieste/`
- Numeri per investor update → chiedi al finance (`40-Finance/`), non stimarli
- Comunicazione esterna del posizionamento → `60-Marketing/`
