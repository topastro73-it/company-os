#!/usr/bin/env python3
"""link-lint.py — verifica che i path citati nei file di sistema esistano davvero.

File di sistema scansionati: `os/`, `zones/`, `CLAUDE.md`, `ARCHITECTURE.md`.
Path verificati: riferimenti in backtick a `os/…`, `zones/…`, `config/…`,
`tools/…`, `scripts/…`, `system/…`, `bootstrap/…`, `company/…`, `vault/…`
e i path Drive (`_OS/…`, `20-Clienti/…`, …), questi ultimi normalmente in allowlist.

Obiettivo: intercettare i "riferimenti rotti" che fanno degradare il sistema in
silenzio (un agente che carica contesto da un file assente). Ignora i template
con placeholder `{slug}`/`{date}`/`*` e le directory generate on-demand.

Allowlist: scripts/audit/link-lint-allow.txt (una voce per riga; una voce che
termina con `/` vale come prefisso).

Uso:  python3 scripts/audit/link-lint.py [--strict]
Exit: 0 se nessun broken link (o solo warning), 1 se --strict e ci sono broken link.
"""
import os
import re
import subprocess
import sys

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)

# Dove cerchiamo i riferimenti (i file "di sistema" che caricano contesto).
SCAN_DIRS = ["os", "zones"]
SCAN_FILES = ["CLAUDE.md", "ARCHITECTURE.md"]
# File esclusi: registri storici che citano stati passati (non riferimenti vivi).
SKIP_FILES = {"system/CHANGELOG.md"}

# Prefissi repo + path Drive (che di norma stanno in allowlist).
PREFIX_RE = re.compile(
    r'`((?:os|zones|config|tools|scripts|system|bootstrap|company|vault|local'
    r'|_OS|\d{2}-[A-Za-z][A-Za-z-]*)/[^`\s]+|CLAUDE\.md|ARCHITECTURE\.md)`')


def load_allowlist():
    exact, prefixes = set(), []
    p = "scripts/audit/link-lint-allow.txt"
    if os.path.isfile(p):
        for line in open(p, encoding="utf-8"):
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            if line.endswith("/"):
                prefixes.append(line)
            else:
                exact.add(line)
    return exact, prefixes


ALLOW_EXACT, ALLOW_PREFIX = load_allowlist()

# Path "template/generato" (non un broken link) se contiene questi marcatori.
TEMPLATE_MARKERS = ("{", "}", "*", "YYYY", "<", "…", "|")
# Directory i cui contenuti sono generati on-demand (snapshot, scratch personale).
GENERATED_PREFIXES = ("local/",)


def allowed(p):
    if p in ALLOW_EXACT:
        return True
    return any(p == pre.rstrip("/") or p.startswith(pre) for pre in ALLOW_PREFIX)


def is_templatey(p):
    return any(m in p for m in TEMPLATE_MARKERS)


def is_generated(p):
    return any(p.startswith(g) for g in GENERATED_PREFIXES)


def iter_files():
    for f in SCAN_FILES:
        if os.path.isfile(f) and f not in SKIP_FILES:
            yield f
    for d in SCAN_DIRS:
        for root, _, files in os.walk(d):
            for fn in files:
                p = os.path.join(root, fn)
                if fn.endswith(".md") and p not in SKIP_FILES:
                    yield p


broken = {}   # path → set di file che lo citano
for f in iter_files():
    try:
        text = open(f, encoding="utf-8", errors="ignore").read()
    except OSError:
        continue
    for m in PREFIX_RE.finditer(text):
        ref = m.group(1).strip().rstrip("/")
        if is_templatey(ref) or is_generated(ref) or allowed(ref):
            continue
        if os.path.exists(ref) or os.path.exists(ref + ".md"):
            continue
        broken.setdefault(ref, set()).add(f)

if not broken:
    print("✅ link-lint: nessun riferimento rotto nei file di sistema")
    sys.exit(0)

print(f"⚠️  link-lint: {len(broken)} path referenziati ma inesistenti\n")
for ref in sorted(broken):
    srcs = ", ".join(sorted(broken[ref]))
    print(f"  ✗ {ref}\n      ← {srcs}")

sys.exit(1 if "--strict" in sys.argv else 0)
