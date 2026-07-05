# /admin export-template — Deriva il template pubblico `company-os`

## Scopo
Produrre il repo template pubblico a partire da questo: stessa logica di sistema,
zero dati dell'istanza privata sorgente. La derivazione deve essere meccanica, non artigianale.

## Input
- Destinazione (repo/branch `company-os`) · versione da taggare

## Passi
1. **Verifica il confine**: tutto ciò che è specifico dell'istanza privata sorgente vive SOLO in
   `config/*.yaml`, `company/`, `vault/`, `zones/*/context/`. Grep di controllo su
   `os/`, `tools/`, `scripts/` per nomi propri (nome azienda, clienti, persone, ID
   workspace) → ogni hit fuori confine è un bug da sistemare PRIMA dell'export.
2. **Costruisci il template**:
   - svuota `company/`, `vault/`; `config/` → solo `*.example.yaml` (stessi campi,
     valori vuoti/placeholder); `zones/*/context/` → file placeholder con istruzioni
   - mantieni: `os/` (agenti, protocolli, skill), `tools/osctl/`, `tools/viewer/`,
     `scripts/audit/`, `.github/workflows/`, `ARCHITECTURE.md` e `CLAUDE.md` genericizzati
   - azzera `system/` (CHANGELOG ripartito da 0.1.0, learnings vuoto, wiki vuota)
3. **Leak-scan obbligatorio**: `secret-scan.sh` + scan dedicato su nomi/dati reali
   (persone, clienti, importi, email, ID ClickUp/Drive). Un solo hit → export bloccato.
4. **Smoke test**: nel repo derivato, `link-lint.py` verde e bootstrap docs coerenti
   (un terzo deve poter partire da `*.example.yaml`).
5. **PREPARE → APPROVE → EXECUTE** per il push al repo pubblico; tag versione.

## Formato output (in chat)
```
## Export template — {versione}
Confine: OK/KO ({hit da sistemare}) · Leak-scan: OK/KO · Smoke: OK/KO
Push: {repo}@{tag} · Note: {…}
```

## Destinazione
Repo esterno `company-os`. Nel repo sorgente: nessuna modifica (o i fix di confine,
committati con changelog).
