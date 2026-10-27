---
zone: direzione
tier: 🟡
type: criteria
goal: G-900
confirmed-by: human:persona-a
registered-at: 2026-10-01
---

# G-900 — Criteri

### C1 — Runway esplicita
- **Observe:** il piano di cassa nella zona finance dichiara la runway in mesi.
- **Fails if:** la runway manca o non è in mesi.

### C2 — Stress coperto
- **Observe:** la pipeline copre almeno la soglia del fabbisogno stress (file di soglie in zona finance).
- **Fails if:** la copertura è sotto soglia.
