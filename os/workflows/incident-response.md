# Workflow: Incident Response

Outage o incidente tecnico/sicurezza sulla piattaforma.

## 1. Detect & assess (CTO)
- **Trigger**: outage, degrado, alert sicurezza, segnalazione cliente
- **Azione**: classifica severità — **P0** (down / data breach) · **P1** (degradato) ·
  **P2** (impatto minore); valuta impatto: quanti partner/end-customer, quali funzionalità
- **Output**: incident record `30-Prodotto/incidents/{YYYY-MM-DD}-{slug}.md`
  (severità, timeline, impatto, owner)
- **Handoff → CEO**: immediato per P0/P1; P2 può procedere diretto alla fase 3

## 2. Communicate (CEO + Marketing)
- **Azione P0/P1**: comunicazione immediata ai clienti impattati (bozze via
  `os/protocols/external-writes.md` — in P0 l'approvazione è prioritaria, non si salta);
  status page; notifica interna al team
- **Se dati personali coinvolti**: attiva subito Compliance (valutazione notifica GDPR 72h /
  obblighi NIS2 verso i partner Telco) — non aspettare la risoluzione
- **Output**: comunicazioni tracciate nella cartella dei clienti impattati
  (`20-Clienti/{slug}/`)

## 3. Resolve (CTO)
- **Azione**: fix e deploy; verifica risoluzione osservata (non solo deploy riuscito)
- **Output**: incident record aggiornato con timeline di risoluzione
- **Criterio di uscita**: servizio verificato funzionante + conferma su clienti campione

## 4. Post-mortem (CTO)
- **Quando**: entro 5 giorni lavorativi per P0/P1
- **Azione**: post-mortem **blameless** — cosa è successo, perché, cosa lo previene;
  action items con owner e deadline
- **Output**: sezione post-mortem nell'incident record; azioni preventive → backlog
  `30-Prodotto/`; se incidente di sicurezza → evidence in `50-Compliance/evidence/`
- **Handoff → CEO + Sales/Delivery**: post-mortem pronto

## 5. Follow-up (CEO + Sales/Delivery)
- **Azione**: comunicazione di chiusura ai clienti impattati; se impatto significativo →
  call personale con i clienti top; aggiorna health score in zona `clienti`
- **Learning**: pattern generalizzabile → proponi LRN-XXX (`os/protocols/memory.md` §3)

## Regole
- P0: l'incident record si apre PRIMA di iniziare il fix (30 secondi, non un report)
- Mai minimizzare nelle comunicazioni: fatti, impatto, ETA, next update
- Gli action item di post-mortem hanno sempre owner e deadline — senza, non è chiuso
