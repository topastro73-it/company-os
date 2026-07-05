# /delivery health-check — Health score partner

## Scopo
Calcolare l'health score (0-100) di un partner (o di tutti), con trend e raccomandazioni.

## Input
- Partner slug (opzionale — se omesso: tutti, in modalità board)

## Passi
1. Carica la scheda partner e i dati disponibili (piattaforma/ERP se MCP attivo,
   altrimenti gli ultimi dati registrati — dichiara la freschezza).
2. Calcola i **5 indicatori pesati**:
   PMI Onboarded 25% · PMI Attive 30gg 25% · Churn PMI trimestre 20% ·
   Engagement venditori 15% · NPS 15%.
   `Health = Σ(indicatore × peso)`. Indicatore senza dati → ⚫ e segnala, non inventare.
3. Assegna la **fascia**: Healthy 80-100 · Stable 60-79 · At-Risk 40-59 · Critical 0-39.
4. **Trend**: confronta con lo score precedente registrato nella scheda; drop >15 punti
   in 30gg → WARNING anche se la fascia regge.
5. **Raccomandazioni per fascia**: Healthy → expansion play; Stable → engagement boost
   (training, co-marketing); At-Risk → call proattiva ≤14gg; Critical → escalation CEO,
   rescue plan ≤7gg.
6. Aggiorna `health-score` e lo storico nella scheda partner; in modalità board aggiorna
   anche il quadro cross-partner.

## Formato output
```markdown
## Partner Health — {nome} ({YYYY-MM-DD})
| Indicatore | Score | Dettaglio |
|---|---|---|
| PMI Onboarded | 85 | 34/40 target |
| … | | |

**Health Score: {N}/100 — {Fascia}** · Trend: {↑/↓ da N}
### Raccomandazioni (max 3, con owner e deadline)
```

## Destinazione
Singolo partner: zona `clienti/{slug}` → sezione health della `scheda-partner.md`.
Board cross-partner: zona `commerciale` → `delivery/health-board.md`.
Commit (admin): `[delivery] health: {slug} {score}`.
