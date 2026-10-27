#!/usr/bin/env python3
"""system-health.py — cruscotto di salute del sistema (CompanyOS).

Controlli di freschezza (semaforo 🟢/🟡/🔴):
  1. CHANGELOG: system/CHANGELOG.md aggiornato rispetto alle ultime modifiche
     a os/, zones/, CLAUDE.md (regola: ogni modifica di sistema → entry changelog)
  2. Snapshot: company/.snapshot-manifest.json recente (<48h; warn se assente)
  3. Learnings: LRN reali in system/learnings.md con Applied fermi a 0
     (le intestazioni dentro i blocchi di codice sono esempi di formato, non learning)
  4. Config: i file config/*.yaml sono parsabili
  5. Ledger: ledger-check su snapshot (e mount Drive se OS_DRIVE_MOUNT è impostata)
  6. Pre-commit: core.hooksPath = scripts/hooks

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
# Grace period: un reset di massa dei contatori (es. migrazione da un altro repo)
# azzera legittimamente il 100%. Senza finestra di grazia il check resta 🔴
# in modo permanente e inazionabile fino alla prima applicazione naturale —
# alert fatigue. Se il frontmatter dichiara un reset recente (<30gg), il
# pavimento di severità è 🟡, non 🔴.
# Il conteggio si ancora alle intestazioni `### LRN-XXX` **fuori dai blocchi di codice**:
# il file documenta il proprio formato in un blocco ```markdown, e contare quell'esempio
# come learning reale rendeva rosso un clone pristino, dove non c'è niente di rotto.
# Sotto i 3 learning la percentuale è rumore (0 / 50 / 100%): il controllo resta neutro
# finché non c'è abbastanza materiale per dire qualcosa di sensato sull'apply-loop.
LRN_MIN_SAMPLE = 3
FENCE_RE = re.compile(r"^```.*?^```", re.S | re.M)
LRN_SPLIT_RE = re.compile(r"^###\s+(?=LRN-\d)", re.M)
lp = "system/learnings.md"
applied0 = total = 0
reset_recent = False
if os.path.isfile(lp):
    txt = open(lp, encoding="utf-8", errors="ignore").read()
    for block in LRN_SPLIT_RE.split(FENCE_RE.sub("", txt))[1:]:
        total += 1
        m = re.search(r"\*\*Applied\*\*:\s*(\d+)", block)
        if m and int(m.group(1)) == 0:
            applied0 += 1
    m = re.search(r"migrated-from:.*?(\d{4}-\d{2}-\d{2}).*contatori Applied azzerati", txt)
    if m:
        reset_date = datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
        reset_recent = (NOW - reset_date).days < 30
if total == 0:
    rows.append(("⚪", "learnings", "nessun LRN registrato (o file assente)"))
elif total < LRN_MIN_SAMPLE:
    rows.append(("⚪", "learnings",
                 f"{total} LRN registrat{'o' if total == 1 else 'i'} — troppo pochi per "
                 f"valutare l'apply-loop (soglia: {LRN_MIN_SAMPLE})"))
else:
    pct0 = applied0 / total * 100
    icon = "🔴" if pct0 >= 60 else "🟡" if pct0 >= 30 else "🟢"
    if reset_recent and icon == "🔴":
        icon = "🟡"
        rows.append((icon, "learnings", f"{applied0}/{total} LRN con Applied:0 ({pct0:.0f}%) — reset contatori <30gg fa, atteso"))
    else:
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

# 5) Ledger Org-OS (ADR-004/006) --------------------------------------------
def _drive_mount_set():
    if os.environ.get("OS_DRIVE_MOUNT"):
        return True
    try:
        return any(re.match(r"^\s*(?:export\s+)?OS_DRIVE_MOUNT\s*=\s*\S", line)
                   for line in open(".env", encoding="utf-8"))
    except OSError:
        return False


def _ledger(args):
    try:
        r = subprocess.run([sys.executable, "scripts/audit/ledger-check.py"] + args,
                           capture_output=True, text=True)
    except OSError as e:
        return 2, str(e)
    return r.returncode, r.stdout + r.stderr


if not os.path.isfile("scripts/audit/ledger-check.py"):
    rows.append(("🟡", "ledger", "scripts/audit/ledger-check.py assente"))
else:
    targets = [("snapshot", [])]
    if _drive_mount_set():
        targets.append(("drive", ["--drive"]))
    parts, worst = [], "🟢"
    for label, args in targets:
        code, out = _ledger(args)
        if code == 0 and "ledger assente" in out:
            parts.append(f"{label}: assente")
            worst = "🟡" if worst == "🟢" else worst
        elif code == 0:
            parts.append(f"{label}: pulito")
        else:
            n = sum(1 for line in out.splitlines()
                    if line.startswith("🔴 ") and not line.startswith("🔴 ledger-check:"))
            parts.append(f"{label}: {n} errori — python3 scripts/audit/ledger-check.py"
                         + (" --drive" if args else ""))
            worst = "🔴"
    rows.append((worst, "ledger", "; ".join(parts)))

# 6) Hook pre-commit attivo ---------------------------------------------------
hooks = subprocess.run(["git", "config", "core.hooksPath"], capture_output=True, text=True).stdout.strip()
if hooks.rstrip("/") == "scripts/hooks":
    rows.append(("🟢", "pre-commit", "core.hooksPath = scripts/hooks (secret-scan + ledger-check)"))
else:
    rows.append(("🟡", "pre-commit", "hook non attivo: git config core.hooksPath scripts/hooks"))

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
