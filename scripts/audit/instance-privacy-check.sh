#!/usr/bin/env bash
# instance-privacy-check — impedisce che i dati di un'istanza finiscano su un remote pubblico.
#
# Il template company-os è pubblico per definizione. Un'istanza compilata non lo è:
# contiene identità aziendale, learnings, decisioni e log di sessione. Questo check
# fallisce se i due si sovrappongono.
#
# Uso: scripts/audit/instance-privacy-check.sh [remote]   (default: origin)
set -euo pipefail

REMOTE="${1:-origin}"
URL="$(git remote get-url "$REMOTE" 2>/dev/null || true)"
[ -z "$URL" ] && { echo "ℹ️  instance-privacy: remote '$REMOTE' non configurato — salto"; exit 0; }

# 1. L'istanza è compilata?
IS_INSTANCE=0
[ -f config/company.yaml ] && IS_INSTANCE=1
grep -q '^# Chi siamo — {Company}' zones/_root/context/COMPANY.md 2>/dev/null || IS_INSTANCE=1
[ "$IS_INSTANCE" -eq 0 ] && { echo "✅ instance-privacy: template non compilato, nessun dato d'istanza"; exit 0; }

# 2. Il remote è pubblico?
VIS=""
if command -v gh >/dev/null 2>&1; then
  SLUG="$(printf '%s' "$URL" | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')"
  VIS="$(gh repo view "$SLUG" --json visibility --jq .visibility 2>/dev/null || true)"
fi

if [ "$VIS" = "PUBLIC" ]; then
  cat <<MSG
❌ instance-privacy: questa istanza è compilata ma '$REMOTE' è un repo PUBBLICO.
   $URL

   I dati d'istanza (identità aziendale, learnings, decisioni, log di sessione)
   non devono finire in un repo pubblico. Sposta l'istanza su un repo privato:

     gh repo create <tua-org>/<tuo-os> --private
     git remote rename $REMOTE upstream
     git remote add $REMOTE https://github.com/<tua-org>/<tuo-os>.git
     git push -u $REMOTE main

   'upstream' resta il template, da cui tirare gli aggiornamenti.
MSG
  exit 1
fi

if [ -z "$VIS" ]; then
  echo "⚠️  instance-privacy: impossibile verificare la visibilità di '$REMOTE' (gh assente o non autenticato)."
  echo "   Verifica a mano che $URL sia un repo PRIVATO."
  exit 0
fi

echo "✅ instance-privacy: istanza compilata su remote $VIS"
