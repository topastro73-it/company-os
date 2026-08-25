---
zone: direzione
tier: 🟡
status: attiva
data: 2026-08-25
---

# Piano operativo: iCloud Drive invece di Google Shared Drive

## Decisione
Per ora Techadvisor **non** attiva lo Shared Drive Google previsto dall'architettura di
CompanyOS. I documenti aziendali restano su iCloud Drive (`00 - TechAdvisor`). Il repo git
resta l'**unico master** del sistema: nessun meccanismo di zone/ACL/sync automatico verso
una cartella condivisa esterna è attivo.

## Perché
Andrea è l'unica persona che usa il sistema al momento (`config/people.yaml`). Il valore
delle ACL Drive per-zona/per-collaboratore matura solo quando arrivano altre persone da
onboardare; fino ad allora, iCloud Drive è già il posto dove vivono i documenti e non c'è
motivo di migrare.

## Conseguenze
- `company/` resta vuota (nessuno `osctl snapshot` da Drive) salvo per questa cartella `decisions/`.
- `config/acl.yaml` non viene compilato per ora.
- Comandi `/admin publish`, `/admin snapshot`, `/admin acl-audit` restano non applicabili.
- La pipeline commerciale e gli output di zona vivono nel repo (`company/{zona}/`), scritti
  direttamente in sessione admin.

## Si supera quando
Arriva un secondo collaboratore da onboardare, o Andrea decide di attivare Google Shared
Drive esplicitamente. A quel punto: nuova decisione che sostituisce questa, poi si segue
`bootstrap/README.md` §1-§3.
