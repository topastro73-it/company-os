# Audit & Compliance Skill

Skill per gestire la compliance aziendale, la readiness a certificazioni,
e l'audit continuo della postura di sicurezza dell'azienda.

## Perché è critico

> ⚠️ Adatta framework e priorità al tuo settore. Esempio per un'azienda che vende servizi digitali B2B:

Se non sei compliant e certificato:
1. I clienti enterprise non ti scelgono (il procurement richiede certificazioni)
2. Perdi credibilità con i clienti finali
3. Rischi sanzioni dirette (framework come NIS2 possono riguardarti come fornitore di servizi digitali)

La compliance non è un costo — è un **prerequisito di vendita** in molti mercati B2B.

## Framework coperti

> Esempi di framework. Compila `Priorità` e `Status target` con la situazione reale della tua azienda — non dichiarare uno status "certificato" senza evidenze e auditor accreditato.

| Framework | Perché può servire | Priorità | Status target |
|-----------|---------------|----------|--------------|
| **NIS2** | Obbligo legale EU per molti settori | [da definire] | [da definire] |
| **GDPR** | Trattamento dati personali di soggetti UE | [da definire] | [da definire] |
| **ISO 27001** | Spesso richiesto nel procurement enterprise | [da definire] | [da definire] |
| **ISO 9001** | Qualità dei processi | [da definire] | [da definire] |
| **ISO 27017** | Cloud security | [da definire] | [da definire] |
| **ISO 27018** | PII in cloud | [da definire] | [da definire] |
| **SOC 2 Type II** | Credibilità enterprise e mercati US/UK | [da definire] | [da definire] |
| **Cyber Essentials** | Mercato UK | [da definire] | [da definire] |

---

## Comandi disponibili

### `/audit compliance-status`
Dashboard dello stato di compliance su tutti i framework.

**Processo**:
1. Leggi `company/compliance/status.md` per lo stato corrente
2. Per ogni framework attivo: quanti requisiti mappati, quanti soddisfatti, quanti gap
3. Genera dashboard con semafori

**Output format**:
```markdown
# Compliance Dashboard — {data}

## Overview
| Framework | Requisiti | Soddisfatti | Gap | Compliance % | Status |
|-----------|----------|------------|-----|-------------|--------|
| NIS2 | 45 | 38 | 7 | 84% | giallo |
| GDPR | 30 | 28 | 2 | 93% | verde |
| ISO 27001 | 114 | 67 | 47 | 59% | rosso |
| SOC 2 | 64 | 30 | 34 | 47% | rosso |

## Gap critici (bloccano certificazione)
1. [Gap] — Framework: [quale] — Effort: [S/M/L] — Owner: [ruolo]

## Gap importanti (da risolvere entro [data])
1. [Gap] — Framework: [quale] — Effort: [S/M/L]

## Prossimi milestone
- [Data]: [milestone]

## Raccomandazioni
1. [Azione prioritaria]
```

**Output**: `company/compliance/reports/compliance-status-{date}.md`

---

### `/audit gap-analysis [framework]`
Analisi gap dettagliata per un framework specifico.

**Processo**:
1. Carica requisiti del framework da `company/compliance/frameworks/`
2. Per ogni requisito: stato (compliant / partial / non-compliant / N/A)
3. Per ogni gap: cosa manca, effort per colmarlo, owner, priorità
4. Genera roadmap di remediation

**Output**: `company/compliance/reports/gap-analysis-{framework}-{date}.md`

---

### `/audit nis2-readiness`
Verifica specifica readiness NIS2 — spesso il più critico per un fornitore di servizi digitali.

**Processo**:
1. Verifica i 10 requisiti chiave NIS2:
   - [ ] Risk management policy documentata e approvata dal management
   - [ ] Incident response plan con notifica 24h/72h
   - [ ] Business continuity e disaster recovery plan testato
   - [ ] Supply chain security (valutazione fornitori)
   - [ ] Vulnerability management e patching policy
   - [ ] Crittografia e encryption policy
   - [ ] Access control e autenticazione (MFA)
   - [ ] Network security e monitoring
   - [ ] Training cybersecurity per management e dipendenti
   - [ ] Audit e testing periodici documentati
2. Per ogni requisito: stato, evidenza disponibile, gap
3. Valuta: siamo pronti per un audit? Se no, cosa manca?
4. Timeline per raggiungere readiness

**Output**: `company/compliance/reports/nis2-readiness-{date}.md`

---

### `/audit gdpr-check`
Verifica compliance GDPR.

**Processo**:
1. Verifica requisiti chiave:
   - [ ] Registro dei trattamenti aggiornato
   - [ ] Privacy policy e cookie policy aggiornate
   - [ ] DPA firmati con tutti i processor
   - [ ] Processo per gestire richieste diritti interessati (DSAR)
   - [ ] DPIA per trattamenti ad alto rischio
   - [ ] DPO nominato (se necessario)
   - [ ] Notifica data breach entro 72h procedura
   - [ ] Privacy by design integrata nello sviluppo
   - [ ] Formazione dipendenti su privacy
   - [ ] Trasferimenti extra-UE gestiti (SCC, adequacy)
2. Gap e remediation plan
3. Disclaimer: validare con DPO/avvocato

**Output**: `company/compliance/reports/gdpr-check-{date}.md`

---

### `/audit iso27001-roadmap`
Genera roadmap per mantenimento/rinnovo certificazione ISO 27001.

**Processo**:
1. Mappa i 93 controlli dell'Annex A (ISO 27001:2022)
2. Per ogni controllo: stato corrente, gap, effort
3. Identifica: cosa abbiamo già, cosa manca, cosa è parziale
4. Genera roadmap:
   - Fase 1: ISMS review (policy, scope, risk assessment)
   - Fase 2: Aggiornamento controlli
   - Fase 3: Audit interno
   - Fase 4: Audit esterno di sorveglianza/rinnovo
5. Timeline e budget stimato

**Output**: `company/compliance/reports/iso27001-roadmap-{date}.md`

---

### `/audit soc2-readiness`
Valuta readiness per SOC 2 Type II.

**Processo**:
1. Verifica i 5 Trust Service Criteria:
   - Security (obbligatorio)
   - Availability
   - Processing Integrity
   - Confidentiality
   - Privacy
2. Per ogni criterio: controlli in place, gap, evidenze
3. Stima: timeline per Type I (point-in-time) e Type II (periodo osservazione)

**Output**: `company/compliance/reports/soc2-readiness-{date}.md`

---

### `/audit policy-review`
Revisiona tutte le policy aziendali per completezza e aggiornamento.

**Processo**:
1. Inventario policy in `company/compliance/policies/`:
   - Information Security Policy
   - Acceptable Use Policy
   - Incident Response Policy
   - Business Continuity Policy
   - Data Classification Policy
   - Access Control Policy
   - Encryption Policy
   - Vendor Management Policy
   - Change Management Policy
   - HR Security Policy (onboarding/offboarding)
2. Per ogni policy: esiste? È aggiornata? È approvata? È comunicata?
3. Identifica policy mancanti o stale
4. Proponi piano di creazione/aggiornamento

**Output**: `company/compliance/reports/policy-review-{date}.md`

---

### `/audit evidence-check`
Verifica che le evidenze di compliance siano raccolte e aggiornate.

**Processo**:
1. Per ogni framework attivo, verifica le evidenze richieste:
   - Log di sistema e monitoring
   - Report di vulnerability scan
   - Record di formazione dipendenti
   - Verbali di approvazione management
   - Report di audit precedenti
   - Test di disaster recovery
   - Registri di incidenti
   - Valutazioni fornitori
2. Per ogni evidenza: esiste? È aggiornata? È archiviata correttamente?
3. Alert per evidenze mancanti o scadute

**Output**: `company/compliance/reports/evidence-check-{date}.md`

---

### `/audit vendor-assessment [vendor]`
Valutazione della postura di sicurezza di un fornitore.

**Processo**:
1. Questionario fornitore: certificazioni, policy, incident history, DPA
2. Risk rating: Critical / High / Medium / Low
3. Raccomandazione: approvare / approvare con condizioni / rifiutare
4. DPA necessario? Clausole specifiche?

**Output**: `company/compliance/vendors/{vendor}.md`

---

## Struttura nel repo

```
company/compliance/
├── status.md                        # Dashboard stato compliance
├── frameworks/
│   ├── nis2-requirements.md         # Requisiti NIS2 mappati
│   ├── gdpr-requirements.md         # Requisiti GDPR mappati
│   ├── iso27001-controls.md         # Controlli ISO 27001 mappati
│   └── soc2-criteria.md             # Criteri SOC 2 mappati
├── policies/
│   ├── information-security.md
│   ├── incident-response.md
│   ├── business-continuity.md
│   ├── access-control.md
│   ├── encryption.md
│   ├── vendor-management.md
│   ├── data-classification.md
│   ├── acceptable-use.md
│   ├── change-management.md
│   └── hr-security.md
├── vendors/
│   └── {vendor-slug}.md             # Valutazioni fornitori
├── audits/
│   └── {date}-{type}.md             # Record di audit
└── evidence/
    └── README.md                    # Dove trovare le evidenze
```

---

## Integrazione nei workflow decisionali

### Nel CEO Decision Cadence

**Giornaliero**:
- Se c'è una scadenza compliance nei prossimi 7 giorni → alert
- Se un audit è schedulato nei prossimi 30 giorni → reminder preparazione

**Settimanale**:
- "Policy review: [N] policy non aggiornate da 6+ mesi"
- "Evidenze: [N] evidenze mancanti per [framework]"

**Mensile**:
- "Compliance dashboard: NIS2 [N]%, GDPR [N]%, ISO27001 [N]%"
- "Prossimo milestone certificazione: [cosa] — [data] — siamo pronti?"
- "Vendor assessment: [N] fornitori non valutati da 12+ mesi"

### Nel PM workflow

**Quando il PM scrive una PRD** (`/product write-spec`):
- Step aggiuntivo: "Questa feature ha impatti sulla compliance?"
- Check: tratta dati personali? Cambia l'architettura di sicurezza? Richiede DPIA?
- Se sì: flag nel frontmatter della spec: `compliance-impact: [NIS2/GDPR/ISO27001]`
- Handoff automatico → `/audit` per impact assessment

### Nel CTO workflow

**Quando il CTO fa tech-decision o architecture-review**:
- Step aggiuntivo: "Questa decisione impatta la compliance?"
- Check: cambia encryption, access control, logging, data flow?
- Se sì: documentare impatto nell'ADR e notificare audit skill
- Verifica: la nuova architettura mantiene i controlli ISO27001 mappati?

### Nel Legal workflow

**Quando Legal rivede contratti**:
- Verifica automatica: il contratto include clausole DPA se tratta dati personali?
- Check: il fornitore è stato valutato con vendor assessment?
- Se no: flag → `/audit vendor-assessment [vendor]` prima di firmare

### Nel HR workflow

**Quando HR gestisce onboarding/offboarding**:
- Onboarding: verifica che il nuovo dipendente faccia security training
- Offboarding: verifica revoca accessi, NDA in place
- Tracking: record formazione per evidenze compliance

### Nel Marketing workflow

**Quando Marketing crea contenuti su compliance (es. NIS2) per i clienti**:
- Cross-check: "Siamo noi compliant su quello che stiamo raccomandando?"
- Se no: flag — non possiamo raccomandare qualcosa che noi stessi non facciamo

### Nel Sales workflow

**Quando Sales risponde a RFP/procurement enterprise**:
- Carica automaticamente: certificazioni disponibili, policy, SOC2 report
- Identifica gap: "Il cliente richiede ISO27001 e non ce l'abbiamo ancora — come rispondiamo?"
- Proponi: risposta onesta con roadmap di certificazione

### Nel Chief of Staff workflow

**Nel daily-briefing e weekly-digest**:
- Include sezione "Compliance" se ci sono alert o scadenze
- Nel product-plan: evidenzia spec con `compliance-impact`
- Nel startup-snapshot: include compliance % nel section

---

## Cadenza di audit consigliata

| Attività | Frequenza | Owner | Comando |
|----------|----------|-------|---------|
| Compliance status dashboard | Mensile | CoS/Legal | `/audit compliance-status` |
| Policy review | Trimestrale | Legal | `/audit policy-review` |
| Evidence check | Trimestrale | Legal/CTO | `/audit evidence-check` |
| Vendor assessment | Annuale per vendor | Legal | `/audit vendor-assessment` |
| NIS2 readiness | Trimestrale | Legal/CTO | `/audit nis2-readiness` |
| GDPR check | Semestrale | Legal | `/audit gdpr-check` |
| Penetration test | Annuale | CTO (esterno) | Manuale |
| DR test | Semestrale | CTO | Manuale |
| Security training | Annuale | HR | Manuale |

---

## Regole

- **SEMPRE** disclaimer: "Questa analisi è un assessment interno. Per certificazioni formali serve un auditor accreditato."
- **MAI** dichiarare compliance senza evidenze documentate
- **SEMPRE** collegare ogni gap a un'azione concreta con owner e deadline
- La compliance è un processo continuo, non un progetto one-shot
- Se vendi compliance ai tuoi clienti, DEVI essere più compliant di loro
- Ogni spec con impatto compliance va flaggata nel frontmatter
