# Integrazioni — script di esempio

Script **funzionanti**, presi da installazioni reali di company-os e ripuliti dai dati
dell'azienda d'origine. Non sono scheletri da riempire: se usi lo stesso fornitore
funzionano così come sono, se ne usi un altro servono da modello.

Tre regole valide per tutto quello che sta qui:

- **Sola lettura** — nessuno di questi script scrive sui sistemi esterni. Il caso
  peggiore è una lettura che fallisce.
- **Zero dipendenze** — solo bash e la standard library di Python 3. Niente `pip install`.
- **Credenziali fuori dal repo** — si leggono dal Keychain di macOS (o da variabili
  d'ambiente), mai da file versionati.

## Cosa c'è adesso

| File | Cosa fa |
|------|---------|
| `bank-qonto.sh` | Il comando che lanci tu: prende le credenziali Qonto dal Keychain e avvia lo script Python. |
| `bank_qonto_sync.py` | Legge da Qonto (API v2) i saldi dei conti e i movimenti di un mese, in formato leggibile o `--json`. |

Le istruzioni di configurazione — quali due valori servono, dove metterli, come si
chiama la voce nel Keychain — stanno nel commento in testa a ciascuno script.

## Come ci si arriva

L'intervista di configurazione `/admin setup` chiede se l'azienda ha un conto bancario:
se il fornitore è tra quelli coperti qui, rimanda a questa cartella invece di far
scrivere l'integrazione da zero.
