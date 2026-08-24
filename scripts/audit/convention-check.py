#!/usr/bin/env python3
"""convention-check.py — verifica che gli esempi nella documentazione rispettino
le convenzioni che la documentazione stessa insegna.

Oggi controlla una cosa sola, ma è la più insidiosa: gli **slug degli agenti** nei
formati di commit (`CLAUDE.md`: `[agente] azione: descrizione`).

Perché serve. Questo repo nasce come derivazione di un'istanza privata, e i comandi
di export ripuliscono i nomi propri ma non le convenzioni. Uno slug come `[cfo]` o
`[pm]` sopravvive a ogni leak-scan: non è un segreto, non è un nome, è solo un agente
che **in questo roster non esiste**. Il danno è doppio: rivela il roster dell'istanza
sorgente, e insegna all'adottante a scrivere commit che violano la convenzione del
repo in cui li scrive.

Il roster non è una lista scritta a mano da tenere aggiornata: si deriva da
`os/agents/*/`. Se aggiungi un agente, il check lo sa da solo.

Uso:  python3 scripts/audit/convention-check.py [--strict]
Exit: 0 se nessun difetto (o senza --strict), 1 se --strict e ci sono difetti.
"""
import os
import re
import subprocess
import sys

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)

# Fuori perimetro: piano operativo (viene dallo snapshot), storia (registra il
# passato, non insegna il presente) e scratch locale.
SKIP_PREFIXES = ("company/", "vault/", "local/", "system/wiki/", ".git/")
SKIP_FILES = {"system/CHANGELOG.md", "system/CHANGELOG.en.md"}

# Prefissi legittimi che non sono agenti: processi automatici e segnaposto
# didattici usati nei formati (`[agente] azione: descrizione`).
NON_AGENT_PREFIXES = {
    "snapshot",   # commit dello snapshot nightly Drive → git
    "system",     # modifiche di sistema fuori dal perimetro di un singolo agente
}
PLACEHOLDERS = {"slug", "agente", "agent", "x", "nome", "name"}

# Solo dentro backtick: fuori si rischiano falsi positivi banali (checkbox `- [x]`,
# link markdown, tabelle).
SLUG_RE = re.compile(r"`\[([a-z][a-z0-9-]*)\]")


def roster():
    base = "os/agents"
    if not os.path.isdir(base):
        return set()
    return {d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))}


def markdown_files():
    out = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.md"], text=True)
    seen, files = set(), []
    for p in out.splitlines():
        if p and p not in seen and not p.startswith(SKIP_PREFIXES) and p not in SKIP_FILES:
            seen.add(p)
            files.append(p)
    return files


def main():
    strict = "--strict" in sys.argv
    agents = roster()
    if not agents:
        print("⚠️  convention-check: nessun agente trovato in os/agents/, controllo saltato")
        return 0

    known = agents | NON_AGENT_PREFIXES | PLACEHOLDERS
    findings = []
    for path in markdown_files():
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for slug in SLUG_RE.findall(line):
                if slug not in known:
                    findings.append((path, n, slug, line.strip()))

    if not findings:
        print(f"✅ convention-check: slug di commit coerenti con il roster "
              f"({len(agents)} agenti)")
        return 0

    by_slug = {}
    for path, n, slug, line in findings:
        by_slug.setdefault(slug, []).append((path, n, line))

    n_slug = len(by_slug)
    print(f"\n❌ SLUG FUORI ROSTER — {n_slug} slug non "
          f"{'corrisponde' if n_slug == 1 else 'corrispondono'} a nessun agente in os/agents/:")
    for slug in sorted(by_slug):
        hits = by_slug[slug]
        print(f"\n   [{slug}]  — {len(hits)} occorrenz{'a' if len(hits) == 1 else 'e'}")
        for path, n, line in hits[:5]:
            print(f"     {path}:{n}  {line[:90]}")
        if len(hits) > 5:
            print(f"     … e altre {len(hits) - 5}")

    print(f"\n   Roster attuale: {' '.join(sorted(agents))}")
    print("   O lo slug è sbagliato (rinominalo), o l'agente manca (crealo), oppure")
    print("   è un prefisso non-agente legittimo → aggiungilo a NON_AGENT_PREFIXES.")
    print(f"\nconvention-check: {len(findings)} occorrenze, {n_slug} slug ignoti"
          + ("" if strict else "  (informativo: usa --strict per farlo fallire)"))
    return 1 if strict else 0


if __name__ == "__main__":
    sys.exit(main())
