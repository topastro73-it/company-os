# /delivery new-partner — Avvio onboarding partner

## Scopo
Trasformare un deal won in un onboarding 90 giorni tracciato, dal giorno 1.

## Input
- Nome partner · tipo (Telco Tier-1 / ISP regionale / MSP-MSSP) · tier contrattuale
- Data firma · contatto principale (nome, ruolo, email) · target PMI contrattuale

## Passi
1. Verifica handoff da Sales: opportunità `won` in zona `commerciale` (linkala).
2. Crea la cartella `clienti/{slug}/` (se admin: chiedi ad `admin`/osctl di creare la
   cartella Drive con ACL per-cartella e owner del cliente assegnato).
3. Crea la **scheda partner** (formato sotto) con fase = SETUP, start = data firma.
4. Genera la **checklist onboarding** con le 4 fasi e le deadline calcolate dalla firma:
   SETUP (kickoff g.1, tenant g.3, utenti g.5, prime PMI g.7, catalogo g.10, test e2e g.14) →
   ENABLEMENT (training, materiale co-branded, lista 20-50 PMI target) →
   LAUNCH (campagna, 10+ assessment, prima proposta, primo deal sett.8) →
   OPTIMIZE (conversion analysis, QBR 90gg, health baseline).
5. Notifica: kickoff call da fissare (Sales + Delivery), setup tenant → `cto`.

## Formato output (scheda partner)
```markdown
---
zone: clienti/{slug}
tier: 🟡
type: partner
partner-type: isp-tier2
contract-tier: engage
signed: YYYY-MM-DD
onboarding-phase: setup
health-score: null        # baseline al giorno 90
owner-delivery: {persona}
target-pmi: 40
---
# {Nome Partner}
## Contatti  ## Contratto (rif. clienti/{slug}/contratti/ 🔴)
## Onboarding 90gg — checklist per fase (task, owner, deadline, stato)
## Timeline  ## Note
```

## Destinazione
Zona `clienti/{slug}` → `scheda-partner.md` + `onboarding-checklist.md`.
Commit (admin): `[delivery] onboarding: new partner {nome} — setup started`.

## Handoff
`cto` (tenant white-label) · `sales` (kickoff congiunto) · `finance` (prima fattura).
