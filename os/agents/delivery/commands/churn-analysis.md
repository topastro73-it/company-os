# /delivery churn-analysis — Analisi churn cross-partner

## Scopo
Capire perché perdiamo (o rischiamo di perdere) partner e PMI, e cosa cambiare.

## Input
- Periodo (default: ultimo trimestre)

## Passi
1. Scansiona tutte le schede partner: churned nel periodo, health <60, PMI perse per
   partner.
2. **Churn rate**: partner-level e cliente-finale-level, per segmento (`config/company.yaml`) e per tier.
3. **Root cause** per ogni churn o At-Risk/Critical: onboarding mai completato? Engagement
   venditori a zero? Value non percepito (PMI attive basse)? Problema di prodotto? Prezzo?
   Cerca il pattern, non l'aneddoto — usa i 5 indicatori come griglia.
4. **Pattern comuni**: es. "i partner senza primo deal entro la sett.8 churnano nel 70%
   dei casi" → candidato learning `LRN-XXX` (proponi al close).
5. **Azioni preventive**: per ogni partner a rischio, un'azione con owner e deadline;
   per i pattern, una proposta di modifica al processo (onboarding, enablement, prodotto).

## Formato output
```markdown
---
zone: commerciale
tier: 🟡
type: report
---
# Churn Analysis — {periodo}

## Numeri: churn partner {n}/{%} · churn PMI {%} · per segmento/tier
## Churned nel periodo (partner, causa radice, segnali ignorati)
## A rischio ora
| Partner | Health | Fascia | Causa principale | Azione | Owner | Deadline |
## Pattern identificati (candidati learning)
## Proposte di modifica al processo
```

## Destinazione
Zona `commerciale` → `delivery/churn-analysis-{YYYY-MM-DD}.md`.
Commit (admin): `[delivery] churn: analisi {periodo}`.

## Handoff
Pattern di prodotto → `product` · pattern di vendita/aspettative → `sales` ·
rischio churn di peso → `ceo`.
