# /marketing launch-plan — Piano di lancio feature

## Scopo
Trasformare una feature shipped in domanda e adozione, con effort proporzionato al peso.

## Input
- Feature (con release notes in zona `prodotto`) · data di disponibilità effettiva

## Passi
1. Carica la PRD e le release notes (`prodotto/releases/`) — si lancia solo ciò che è
   **shipped** con UAT GO; verifica il beneficio per ogni ruolo utente (es. Partner, Venditore, Cliente finale).
2. **Classifica il lancio**:
   - **Tier 1** (major): blog post + email partner + social + sales enablement + webinar/demo
   - **Tier 2** (notable): blog post + email + changelog
   - **Tier 3** (minor): changelog e nota nelle release notes partner
3. **Messaggio**: beneficio prima della feature; declinato per audience (il partner vuole
   revenue, il cliente finale vuole il risultato senza complessità).
4. **Timeline**: pre-launch (asset pronti, sales brief) → launch day (pubblicazioni,
   invii) → post-launch (follow-up, raccolta feedback a 2 settimane).
5. **Success metrics**: adozione (partner attivi sulla feature), traffico/lead, feedback.
6. Asset di enablement → zona `commerciale` (dove Sales li trova); invii e pubblicazioni
   → PREPARE → APPROVE → EXECUTE.

## Formato output
```markdown
---
zone: marketing
tier: 🟡
type: launch-plan
feature: {slug}
launch-tier: {1|2|3}
---
# Launch Plan — {feature}

## Classificazione e razionale   ## Messaggio per audience
## Asset da produrre | Asset | Owner | Deadline | Stato |
## Timeline (pre / day / post)
## Success metrics
```

## Destinazione
Zona `marketing` → `content/launch-{feature}.md`.
Commit (admin): `[marketing] launch: {feature}`.

## Handoff
Enablement → `sales` · comunicazione ai partner attivi → `delivery` · feedback raccolto
→ `product`.
