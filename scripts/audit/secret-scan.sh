#!/usr/bin/env bash
# secret-scan.sh — blocca segreti e file 🔴 fuori posto prima che entrino nel repo
# (ARCHITECTURE.md §8, privacy tiers §2).
# Uso:
#   scripts/audit/secret-scan.sh            # scansiona i file tracciati
#   scripts/audit/secret-scan.sh --staged   # scansiona solo il diff in staging (pre-commit)
# Exit 0 = pulito, 1 = trovati potenziali segreti (blocca commit / CI).
#
# Logica:
#  - TOKEN/chiavi API/private key → vietati OVUNQUE nel repo (non sono dati di business leciti)
#  - IBAN e filename 🔴 (cap-table, *-signed-*, iban-*, cf-*) → leciti SOLO sotto
#    vault/ e company/clienti/*/contratti/; bloccati se compaiono altrove.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 2

MODE="${1:-tracked}"
FAIL=0

# File/dir esclusi dallo scan del contenuto (pattern documentati, esempi env, questo script).
EXCLUDE_RE='^(\.env\.example|scripts/audit/secret-scan\.sh|tools/viewer/viewer\.html)'
# Destinazioni dove i dati 🔴 (IBAN, cap-table, signed) sono LECITI.
ALLOWED_RESTRICTED_RE='^(vault/|company/clienti/[^/]+/contratti/)'

# Token / chiavi: vietati ovunque.
read -r -d '' TOKEN_PATTERNS <<'EOF'
\bpk_[0-9]{6,}_[A-Za-z0-9]{20,}
\bsk_live_[A-Za-z0-9]{16,}
\bghp_[A-Za-z0-9]{30,}
\bxox[baprs]-[A-Za-z0-9-]{10,}
\bAKIA[0-9A-Z]{16}
-----BEGIN [A-Z ]*PRIVATE KEY-----
[a-z0-9]+-[0-9]{3,4}:[a-f0-9]{32}
EOF
# IBAN: lecito solo nelle destinazioni ristrette.
IBAN_PATTERN='IT[0-9]{2}[A-Z][0-9]{10,26}'

if [ "$MODE" = "--staged" ]; then
  FILES=$(git diff --cached --name-only --diff-filter=ACM)
  GET() { git show ":$1" 2>/dev/null | tr -d '\000'; }
else
  FILES=$(git ls-files)
  GET() { tr -d '\000' < "$1" 2>/dev/null; }
fi

report() { # $1=file $2=hits
  echo "🔴 $1:"
  printf '%s\n' "$2" | sed -E 's/([A-Za-z0-9]{4})[A-Za-z0-9]{6,}/\1…MASKED…/g' | sed 's/^/     /'
  FAIL=1
}

while IFS= read -r f; do
  [ -z "$f" ] && continue
  echo "$f" | grep -qE "$EXCLUDE_RE" && continue
  content=$(GET "$f")
  [ -z "$content" ] && continue
  # token ovunque
  while IFS= read -r pat; do
    [ -z "$pat" ] && continue
    hits=$(printf '%s' "$content" | grep -nE -e "$pat" | head -3)
    [ -n "$hits" ] && report "$f (token/chiave)" "$hits"
  done <<< "$TOKEN_PATTERNS"
  # IBAN solo se fuori dalle destinazioni ristrette
  if ! echo "$f" | grep -qE "$ALLOWED_RESTRICTED_RE"; then
    hits=$(printf '%s' "$content" | grep -nE "$IBAN_PATTERN" | head -3)
    [ -n "$hits" ] && report "$f (IBAN fuori da vault/ e clienti/*/contratti/)" "$hits"
  fi
done <<< "$FILES"

# Filename 🔴 tracciati fuori dalle destinazioni ristrette.
BAD_NAMES=$(printf '%s\n' "$FILES" \
  | grep -iE '(-signed-|/iban-|^iban-|/cf-|^cf-|cap-table)' \
  | grep -vE "$ALLOWED_RESTRICTED_RE" || true)
if [ -n "$BAD_NAMES" ]; then
  echo "🔴 File 🔴 RESTRICTED tracciati fuori da vault/ e company/clienti/*/contratti/:"
  printf '%s\n' "$BAD_NAMES" | sed 's/^/     /'
  FAIL=1
fi

if [ "$FAIL" = 0 ]; then echo "✅ secret-scan: nessun segreto fuori posto ($MODE)"; fi
exit $FAIL
