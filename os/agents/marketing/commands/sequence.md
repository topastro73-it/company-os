# /marketing sequence — Sequenza nurture email

## Scopo
Costruire una sequenza email che scaldi un segmento nel tempo (nurture), complementare
all'outbound di vendita (che è di Sales).

## Input
- Segmento target (ISP Tier-2, MSP, PMI via partner…) · obiettivo (da cold a warm,
  riattivazione, onboarding contenuti) · trigger di ingresso (download, evento, lista)

## Passi
1. Carica ICP del segmento, content disponibile da riusare (`marketing/content/index.md`),
   learnings su aperture/risposte.
2. **Disegna la sequenza**: 4-7 email su 3-6 settimane; ogni email = un solo messaggio,
   un solo contenuto di valore, una sola CTA. Progressione: problema → approfondimento
   → social proof → offerta di valore (assessment, demo).
3. Scrivi ogni email: oggetto (≤50 caratteri, no clickbait), corpo breve, variabili di
   personalizzazione `{nome}`, `{azienda}`, `{pain}`.
4. **Criteri di uscita**: risposta o click qualificante → handoff `sales` (opportunità);
   fine sequenza senza segnali → lista cold.
5. **Verifica claim e compliance** (feature shipped, pratiche che seguiamo, GDPR: base
   giuridica del contatto e unsubscribe sempre presenti).
6. L'attivazione reale (ESP/HubSpot) segue PREPARE → APPROVE → EXECUTE.

## Formato output
```markdown
---
zone: marketing
tier: 🟡
type: sequence
segment: {segmento}
---
# Nurture — {segmento} — {obiettivo}

| # | Giorno | Oggetto | Messaggio chiave | Contenuto linkato | CTA |
|---|---|---|---|---|---|

## Email 1
{testo con variabili}
…
## Criteri di uscita e metriche (open, click, reply target)
```

## Destinazione
Zona `marketing` → `email-templates/nurture-{segmento}.md`.
Commit (admin): `[marketing] sequence: nurture {segmento}`.

## Handoff
Lead qualificato → `sales` (`/sales opportunity`) · sequenze outbound a freddo → `sales`
(`/sales outbound`, che riusa questi template).
