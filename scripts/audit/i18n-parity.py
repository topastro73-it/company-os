#!/usr/bin/env python3
"""i18n-parity.py — verifica che il layer bilingue IT/EN non vada in deriva.

Convenzione (`os/protocols/language.md` §4): i file di sistema hanno la versione
italiana come base (`X.md`) e la variante inglese accanto (`X.en.md`). Una variante
esiste solo se il file base è in italiano; i file già scritti in inglese non ne hanno
(li copre il fallback di `osctl publish`).

Tre difetti intercettati:

  MISSING  file base italiano senza variante `.en.md`
           → con `language: en` l'utente riceve il file in italiano, in silenzio
  ORPHAN   variante `.en.md` senza file base
           → residuo di un rename o di una cancellazione a metà
  STALE    file base modificato **dopo** la sua variante
           → la traduzione descrive un comportamento che il sistema non ha più.
             È il difetto che conta: non rompe nulla, non dà errore, e l'utente
             anglofono legge istruzioni sbagliate.

La freschezza si misura sul **timestamp dell'ultimo commit** che tocca il file, non
sull'mtime del filesystem (dopo un clone gli mtime sono tutti uguali e non dicono
niente). Aggiornare base e variante nello stesso commit è quindi la via normale per
restare verdi; tradurre in un commit successivo va altrettanto bene.

Allowlist: scripts/audit/i18n-parity-allow.txt (una voce per riga; una voce che
termina con `/` vale come prefisso). Serve per i file già in inglese e per quelli
deliberatamente monolingua.

Uso:  python3 scripts/audit/i18n-parity.py [--strict]
Exit: 0 se nessun difetto (o senza --strict), 1 se --strict e ci sono difetti.
"""
import os
import subprocess
import sys

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)

ALLOW_FILE = "scripts/audit/i18n-parity-allow.txt"

# Un file non ancora committato non ha data di commit: conta come appena scritto.
NOW = 1 << 62

# Fuori perimetro: piano operativo (arriva dallo snapshot, non è sistema),
# memoria narrativa (per protocollo è già in inglese) e scratch locale.
SKIP_PREFIXES = ("company/", "vault/", "local/", "system/wiki/", ".git/")


def load_allowlist():
    exact, prefixes = set(), []
    if not os.path.exists(ALLOW_FILE):
        return exact, prefixes
    for raw in open(ALLOW_FILE, encoding="utf-8"):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.endswith("/"):
            prefixes.append(line)
        else:
            exact.add(line)
    return exact, prefixes


def allowed(path, exact, prefixes):
    return path in exact or any(path.startswith(p) for p in prefixes)


def repo_markdown():
    """File tracciati + non ancora tracciati ma non ignorati: il check deve dire la
    verita' sul working tree, non solo sull'indice, altrimenti una traduzione appena
    scritta e non ancora staged risulta mancante."""
    out = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.md"], text=True)
    seen, files = set(), []
    for p in out.splitlines():
        if p and p not in seen and not p.startswith(SKIP_PREFIXES):
            seen.add(p)
            files.append(p)
    return files


def last_commit_times(paths):
    """path → epoch dell'ultimo commit che lo tocca, in una sola passata su git log."""
    times, current = {}, None
    proc = subprocess.run(
        ["git", "log", "--pretty=format:@%ct", "--name-only", "--no-renames"],
        capture_output=True, text=True, check=True)
    wanted = set(paths)
    for line in proc.stdout.splitlines():
        if line.startswith("@"):
            current = int(line[1:])
        elif line and current is not None and line in wanted and line not in times:
            times[line] = current
    return times


def main():
    strict = "--strict" in sys.argv
    exact, prefixes = load_allowlist()
    files = repo_markdown()
    bases = [f for f in files if not f.endswith(".en.md") and not f.endswith(".it.md")]
    variants = [f for f in files if f.endswith(".en.md")]
    have = set(files)

    missing = [b for b in bases
               if b[:-3] + ".en.md" not in have and not allowed(b, exact, prefixes)]
    orphans = [v for v in variants if v[:-6] + ".md" not in have]

    times = last_commit_times(files)
    stale = []
    for b in bases:
        v = b[:-3] + ".en.md"
        # Un file non ancora committato non ha timestamp in git: vale come
        # freschissimo (e' appena stato scritto), quindi non e' mai lui lo stale.
        if v in have and times.get(b, 0) > times.get(v, NOW):
            stale.append((b, v))

    pairs = sum(1 for b in bases if b[:-3] + ".en.md" in have)
    problems = len(missing) + len(orphans) + len(stale)

    if not problems:
        print(f"✅ i18n-parity: {pairs} coppie IT/EN allineate, nessuna deriva")
        return 0

    if missing:
        print(f"\n❌ MISSING — {len(missing)} file base senza variante inglese:")
        for b in sorted(missing):
            print(f"   {b}  →  manca {b[:-3]}.en.md")
        print("   (se il file è già in inglese o è volutamente monolingua, "
              f"aggiungilo a {ALLOW_FILE})")

    if orphans:
        print(f"\n❌ ORPHAN — {len(orphans)} varianti inglesi senza file base:")
        for v in sorted(orphans):
            print(f"   {v}  →  manca {v[:-6]}.md")

    if stale:
        print(f"\n❌ STALE — {len(stale)} traduzioni più vecchie del loro originale:")
        for b, v in sorted(stale):
            print(f"   {v}  →  {b} è stato modificato dopo. Ritraduci o allinea.")

    print(f"\ni18n-parity: {pairs} coppie, {problems} difetti"
          + ("" if strict else "  (informativo: usa --strict per farlo fallire)"))
    return 1 if strict else 0


if __name__ == "__main__":
    sys.exit(main())
