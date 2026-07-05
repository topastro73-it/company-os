---
type: learnings
updated: template
total: 1
active: 1
zone: _os
tier: 🟡
---

# Learnings — regole apprese dall'esperienza

Regole operative che il sistema applica proattivamente (protocollo: `os/protocols/memory.md`).
Il template parte quasi vuoto: i learnings crescono man mano che la tua azienda opera. Ne resta
uno seed, generico e utile a chiunque, sul modello dei permessi Drive.

## Formato

```markdown
### LRN-XXX: Titolo
- **Rule**: When [situazione], [cosa fare / cosa succede].
- **Source**: [sessione / evento]
- **Applied**: 0 times
- **Tags**: ...
- **Status**: active
```

## Learnings attivi

### LRN-001: Google Drive eredita i permessi solo verso il basso — mai una sottocartella "più ristretta"
- **Rule**: When progettando una zona/sottozona con ACL più stretta della cartella madre (es.
  "contratti/ dentro la cartella cliente, solo per pochi"), verifica PRIMA se qualcuno con
  accesso più ampio alla madre esiste già: se sì, erediterà comunque l'accesso alla
  sottocartella — Google Drive non permette di *togliere* permessi più in profondità, solo di
  aggiungerne. Le zone "più ristrette della madre" devono essere cartelle **top-level separate**
  (es. `70-Contratti-Riservati/`), mai sottocartelle di una zona più permissiva. Le sottozone in
  `acl.yaml` restano valide SOLO quando *aggiungono* persone (es. una sottocartella `bandi/` che
  dà accesso a un consulente altrimenti escluso dalla zona finance).
- **Source**: Template seed — modello di permessi CompanyOS
- **Applied**: 0 times
- **Tags**: sistema, drive, acl, permessi, architettura
- **Status**: active

---

## Archived learnings

*(nessuno)*
