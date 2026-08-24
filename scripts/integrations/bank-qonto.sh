#!/usr/bin/env bash
# =============================================================================
# bank-qonto.sh — saldi e movimenti del conto Qonto (SOLA LETTURA)
# =============================================================================
#
# COSA FA
#   È il comando che lanci tu. Legge le credenziali Qonto dal Keychain di macOS
#   e le passa a `bank_qonto_sync.py` come variabili d'ambiente: le credenziali
#   non vengono mai stampate a video né scritte su disco. Lo script Python
#   interroga l'API Qonto e mostra saldi dei conti e movimenti del mese.
#
#   SOLA LETTURA: non viene mai chiamato un endpoint di scrittura. Nessun
#   bonifico, nessuna modifica al conto, nessun dato inviato a terzi. Il caso
#   peggiore è una lettura che fallisce.
#
# È UN ESEMPIO, NON UNO SCHELETRO
#   Questo file arriva insieme al template: è codice vero, in uso in
#   un'installazione reale, ripulito dai dati dell'azienda d'origine. Se usi
#   Qonto funziona così com'è. Se usi un'altra banca, prendilo come modello:
#   la struttura (credenziali dal Keychain, gestione errori, output `--json`)
#   vale per qualunque provider, cambia solo la parte di chiamata all'API.
#
# COSA SERVE, UNA VOLTA SOLA PER MACCHINA
#   Ti servono due valori, che trovi in Qonto → Integrazioni → API key:
#     • il "login" dell'organizzazione — una stringa tipo `acme-1234`
#     • la "secret key"
#
#   Salvali nel Keychain con questi due comandi (sostituisci i valori
#   d'esempio con i tuoi):
#
#     security add-generic-password -a "qonto" -s "QONTO_LOGIN"  -w "acme-1234"      -U
#     security add-generic-password -a "qonto" -s "QONTO_SECRET" -w "la-tua-secret"  -U
#
#   Il `-a "qonto"` è il nome dell'account nel Keychain, cioè l'etichetta sotto
#   cui le due voci vengono salvate. Se nel tuo Keychain si chiamano in un altro
#   modo — per esempio perché segui più aziende dalla stessa macchina — non
#   devi modificare questo file: basta dichiarare il nome giusto in una
#   variabile d'ambiente.
#
#     export QONTO_KEYCHAIN_ACCOUNT="qonto-acme"
#     bash scripts/integrations/bank-qonto.sh balance
#
#   Senza quella variabile viene usato il valore predefinito: `qonto`.
#
# SE NON USI macOS (o non vuoi usare il Keychain)
#   Puoi esportare direttamente le due credenziali: se sono già presenti
#   nell'ambiente, il Keychain non viene nemmeno interrogato.
#
#     export QONTO_LOGIN="acme-1234"
#     export QONTO_SECRET="la-tua-secret"
#
#   ⚠️  In questo caso le credenziali restano nella tua shell: non scriverle mai
#   dentro un file versionato nel repo.
#
# USO
#   bash scripts/integrations/bank-qonto.sh balance
#   bash scripts/integrations/bank-qonto.sh balance --json
#   bash scripts/integrations/bank-qonto.sh transactions --month 2026-08
#   bash scripts/integrations/bank-qonto.sh transactions --month 2026-08 --json
#
# DIPENDENZE
#   Nessuna libreria di terze parti. Servono solo bash, python3 (con la sola
#   standard library) e — se usi il Keychain — il comando `security` di macOS.
#   Niente `pip install`, niente da installare.
# =============================================================================

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Nome dell'account sotto cui le credenziali sono salvate nel Keychain.
# Configurabile perché non tutti lo chiamano allo stesso modo.
KEYCHAIN_ACCOUNT="${QONTO_KEYCHAIN_ACCOUNT:-qonto}"

keychain_get() {
  local key="$1"
  if ! security find-generic-password -a "$KEYCHAIN_ACCOUNT" -s "$key" -w 2>/dev/null; then
    echo "bank-qonto.sh: credenziale '$key' assente dal Keychain (account '$KEYCHAIN_ACCOUNT')." >&2
    echo "  Salvala una volta sola:" >&2
    echo "  security add-generic-password -a \"$KEYCHAIN_ACCOUNT\" -s \"$key\" -w \"<valore>\" -U" >&2
    echo "  Se la voce esiste ma con un altro nome account, esporta QONTO_KEYCHAIN_ACCOUNT." >&2
    echo "  In alternativa esporta direttamente QONTO_LOGIN e QONTO_SECRET." >&2
    exit 1
  fi
}

# Credenziali gia' in ambiente -> si usano quelle e il Keychain non viene toccato.
if [ -z "${QONTO_LOGIN:-}" ] || [ -z "${QONTO_SECRET:-}" ]; then
  if ! command -v security >/dev/null 2>&1; then
    echo "bank-qonto.sh: comando 'security' non disponibile (non sei su macOS?)." >&2
    echo "  Esporta QONTO_LOGIN e QONTO_SECRET prima di lanciare lo script." >&2
    exit 1
  fi
  QONTO_LOGIN="$(keychain_get QONTO_LOGIN)"
  QONTO_SECRET="$(keychain_get QONTO_SECRET)"
fi
export QONTO_LOGIN QONTO_SECRET

exec python3 "$HERE/bank_qonto_sync.py" "$@"
