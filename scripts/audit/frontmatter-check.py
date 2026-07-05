#!/usr/bin/env python3
"""frontmatter-check.py — valida il frontmatter YAML dei file operativi.

Sui file `.md` in `company/` e `vault/` verifica che il frontmatter dichiari:
  - `zone:` con un valore valido (le zone definite in config/acl.yaml)
  - `tier:` (o `privacy:`) con un valore valido (restricted/internal/public o 🔴🟡🟢)

I tier restano *classificazione* (publish esterni, redazione PII, secret-scan):
l'accesso lo decide l'ACL Drive della zona (ARCHITECTURE.md §2).

Uso:  python3 scripts/audit/frontmatter-check.py [--strict]
Exit: 0 ok/warning, 1 se --strict e ci sono zone/tier non validi.
"""
import os
import re
import subprocess
import sys

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools", "osctl"))

VALID_TIERS = {"restricted", "internal", "public", "🔴", "🟡", "🟢"}
SKIP_NAMES = {"README.MD", "TEMPLATE.MD", "INDEX.MD"}
FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def valid_zones():
    try:
        from lib.config import Config
        cfg = Config(repo_root=ROOT)
        return set(cfg.zones.keys())
    except Exception as e:  # config rotta: la segnala system-health, qui fallback
        print(f"⚠️  impossibile leggere config/acl.yaml ({e}) — uso l'elenco statico")
        return {"_os", "direzione", "commerciale", "clienti", "prodotto",
                "finance", "compliance", "marketing", "shared"}


def frontmatter(path):
    try:
        head = open(path, encoding="utf-8", errors="ignore").read(4000)
    except OSError:
        return None
    m = FM_RE.match(head)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.strip().startswith("#"):
            k, _, v = line.partition(":")
            fm[k.strip().lower()] = v.strip().strip("\"'")
    return fm


ZONES = valid_zones()
problems = []      # (path, motivo)
ok_count = 0
total = 0

for base in ("company", "vault"):
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in files:
            if not fn.endswith(".md") or fn.upper() in SKIP_NAMES:
                continue
            p = os.path.join(root, fn)
            total += 1
            fm = frontmatter(p)
            if fm is None:
                problems.append((p, "manca il frontmatter YAML"))
                continue
            zone = fm.get("zone", "")
            tier = fm.get("tier") or fm.get("privacy") or ""
            bad = []
            if not zone:
                bad.append("manca `zone:`")
            elif zone not in ZONES:
                bad.append(f"zone non valida: {zone!r}")
            if not tier:
                bad.append("manca `tier:`")
            elif tier.lower() not in VALID_TIERS:
                bad.append(f"tier non valido: {tier!r}")
            if bad:
                problems.append((p, "; ".join(bad)))
            else:
                ok_count += 1

print("== Frontmatter check (company/ + vault/) ==")
if total == 0:
    print("  ⚪ nessun file operativo nel repo (normale prima del primo snapshot)")
    sys.exit(0)

pct = ok_count / total * 100
print(f"  copertura zone+tier: {ok_count}/{total} ({pct:.0f}%)")
if problems:
    print(f"  ⚠️  {len(problems)} file con frontmatter incompleto. Primi 20:")
    for p, why in sorted(problems)[:20]:
        print(f"       ✗ {p}: {why}")
else:
    print("  ✅ tutti i file operativi dichiarano zone e tier validi")

sys.exit(1 if ("--strict" in sys.argv and problems) else 0)
