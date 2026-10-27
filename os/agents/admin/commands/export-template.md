# /admin export-template — Deriva il template pubblico `company-os`

## Scopo
Produrre il repo template pubblico a partire da questo: stessa logica di sistema,
zero dati dell'istanza privata sorgente. La derivazione deve essere meccanica, non artigianale.

## Input
- Destinazione (repo/branch `company-os`) · versione da taggare

## Passi
1. **Dry-run**: `python3 tools/osctl/osctl.py export-template` (parametri in
   `config/export.yaml`: clone di destinazione, radici incluse, file d'istanza esclusi, file
   `template_owned`, termini del leak-scan). Mostra file nuovi, aggiornati, da cancellare, varianti
   `.en.md` orfane, traduzioni da fare e da rifare, e l'esito del leak-scan **su ciò che uscirebbe**.
2. **Verifica il confine**: tutto ciò che è specifico dell'istanza vive SOLO in `config/*.yaml`,
   `company/`, `vault/`, `zones/*/context/`, oppure in file elencati in `exclude`. Dentro un file di
   sistema condiviso, una riga d'istanza si marca con un commento che contiene `@instance`
   (`<!--`, `#` o `//` a seconda del formato); un blocco si chiude fra `@instance-begin` e
   `@instance-end`. L'export li toglie. Un hit del leak-scan è un bug di confine: si sistema qui,
   con changelog, **prima** dell'export. Mai aggiungere un termine reale ad `allow_terms` per
   farlo passare: `allow_terms` è solo per parole generiche che coincidono con uno slug cliente.
3. **Applica**: `osctl export-template --apply` scrive nel working tree del clone. **L'export è
   un merge, non una sovrascrittura**:
   - i file base `X.md` si sovrascrivono dalla sorgente (marker `@instance` tolti);
   - le varianti `X.en.md` del template **non si cancellano mai**, salvo quando il loro file base
     è sparito dalla sorgente (orfane);
   - i file `template_owned` (`CLAUDE.md`, `ARCHITECTURE.md`, README, `LICENSE`, `config/`,
     `company/`, `vault/`, `system/`, `zones/*/context/`, il brand kit placeholder, `i18n-parity`)
     hanno contenuto proprio nel template: l'export non li tocca e segnala se il gemello qui è
     cambiato, perché il porting lì è a mano;
   - nessun commit e nessun push.
4. **Nel clone del template**: traduci i file "da tradurre" e ritraduci quelli "da ritradurre"
   (`os/protocols/language.md` §4), aggiorna `system/CHANGELOG.md` del template (nuova versione,
   con la versione del kernel di partenza), poi smoke test: `link-lint.py --strict`,
   `convention-check.py --strict`, **`i18n-parity.py --strict`** e `secret-scan.sh`, tutti verdi.
   Bootstrap docs coerenti: un terzo deve poter partire da `*.example.yaml`.
5. **PREPARE → APPROVE → EXECUTE** per il push al repo pubblico; tag versione.

## Formato output (in chat)
```
## Export template — {versione}
Confine: OK/KO ({hit da sistemare}) · Leak-scan: OK/KO · Smoke: OK/KO
Push: {repo}@{tag} · Note: {…}
```

## Destinazione
Repo esterno `company-os`. Nel repo sorgente: nessuna modifica (o i fix di confine,
committati con changelog). Registra in `system/CHANGELOG.md` la corrispondenza delle versioni
(es. kernel 2.10.0 ↔ company-os 0.6.0): è il punto da cui riparte il prossimo export.
