#!/usr/bin/env python3
"""system-health.py — cruscotto di salute di CompanyOS.

Controlli di freschezza (semaforo 🟢/🟡/🔴):
  1. CHANGELOG: system/CHANGELOG.md aggiornato rispetto alle ultime modifiche
     a os/, zones/, CLAUDE.md (regola: ogni modifica di sistema → entry changelog)
  2. Snapshot: company/.snapshot-manifest.json recente (<48h; warn se assente)
  3. Learnings: LRN in system/learnings.md con Applied fermi a 0
  4. Config: i file config/*.yaml sono parsabili

Uso:  python3 scripts/audit/system-health.py
Exit: 0 sempre (è un report). Usato da `/system health` e dal close routine.
"""
import glob
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools", "osctl"))

NOW = datetime.now(timezone.utc)
rows = []


def git_last_ts(*paths):
    """Epoch dell'ultimo commit che tocca i path (0 se mai toccati)."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--"] + list(paths),
            capture_output=True, text=True).stdout.strip()
        return int(out) if out else 0
    except (OSError, ValueError):
        return 0


# 1) CHANGELOG vs modifiche di sistema -------------------------------------
sys_ts = git_last_ts("os", "zones", "CLAUDE.md")
log_ts = git_last_ts("system/CHANGELOG.md")
if not os.path.isfile("system/CHANGELOG.md"):
    rows.append(("🟡", "changelog", "system/CHANGELOG.md assente — crealo alla prima modifica di sistema"))
elif sys_ts == 0:
    rows.append(("⚪", "changelog", "nessun commit su os//zones/ ancora"))
elif log_ts >= sys_ts:
    rows.append(("🟢", "changelog", "aggiornato rispetto alle modifiche di sistema"))
else:
    gap_days = (sys_ts - log_ts) / 86400
    icon = "🔴" if gap_days > 7 else "🟡"
    rows.append((icon, "changelog",
                 f"os//zones/ modificati DOPO l'ultima entry ({gap_days:.0f}gg di gap)"))

# 2) Snapshot manifest -------------------------------------------------------
manifest = "company/.snapshot-manifest.json"
if not os.path.isfile(manifest):
    rows.append(("🟡", "snapshot", "manifest assente — snapshot mai eseguito (osctl snapshot)"))
else:
    ts = None
    try:
        with open(manifest, encoding="utf-8") as fh:
            raw = json.load(fh).get("timestamp", "")
        ts = datetime.strptime(raw[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    except (OSError, ValueError):
        pass
    if ts is None:
        rows.append(("🟡", "snapshot", "manifest illeggibile"))
    else:
        age_h = (NOW - ts).total_seconds() / 3600
        icon = "🟢" if age_h < 48 else "🔴"
        rows.append((icon, "snapshot", f"ultimo {ts.date()} ({age_h:.0f}h fa)"))

# 3) Learnings apply-loop -----------------------------------------------------
lp = "system/learnings.md"
applied0 = total = 0
if os.path.isfile(lp):
    txt = open(lp, encoding="utf-8", errors="ignore").read()
    for m in re.finditer(r"\*\*Applied\*\*:\s*(\d+)", txt):
        total += 1
        if int(m.group(1)) == 0:
            applied0 += 1
if total == 0:
    rows.append(("⚪", "learnings", "nessun LRN registrato (o file assente)"))
else:
    pct0 = applied0 / total * 100
    icon = "🔴" if pct0 >= 60 else "🟡" if pct0 >= 30 else "🟢"
    rows.append((icon, "learnings", f"{applied0}/{total} LRN con Applied:0 ({pct0:.0f}%)"))

# 4) Config yaml parsabili -----------------------------------------------------
bad = []
try:
    from lib.config import load_yaml
    for path in sorted(glob.glob("config/*.yaml")):
        try:
            load_yaml(path)
        except Exception as e:
            bad.append(f"{path}: {e}")
except Exception as e:
    bad.append(f"parser non importabile: {e}")
rows.append(("🔴" if bad else "🟢", "config",
             "; ".join(bad) if bad else f"{len(glob.glob('config/*.yaml'))} file yaml parsabili"))

# Report --------------------------------------------------------------------
print(f"# 🩺 System Health — {NOW.date()}\n")
print("| | Controllo | Stato |")
print("|--|--|--|")
for icon, name, detail in rows:
    print(f"| {icon} | {name} | {detail} |")

crit = sum(1 for r in rows if r[0] == "🔴")
warn = sum(1 for r in rows if r[0] == "🟡")
print(f"\n**Riepilogo**: {crit} 🔴 · {warn} 🟡 · {len(rows) - crit - warn} 🟢/⚪")
if crit:
    print("\n> 🔴 = controllo oltre soglia critica — intervieni prima del prossimo close.")
sys.exit(0)
