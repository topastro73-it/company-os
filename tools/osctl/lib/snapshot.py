"""snapshot.py — Drive → git (osctl snapshot).

Scarica le zone con `sync: drive_master` in `company/{zona}/`; la zona con
`snapshot_target: vault` (finance) va in `vault/finance/`. Scrive un manifest
con timestamp in `company/.snapshot-manifest.json` e stampa il diff sintetico.

NON committa: il commit lo fa il chiamante (GitHub Action nightly o /close).
"""

import json
import os
import subprocess
from datetime import datetime, timezone

from .drive import Drive, DriveError

MANIFEST_REL = os.path.join("company", ".snapshot-manifest.json")


def _git_diff_summary(root, paths):
    """Diff sintetico (git status --porcelain) sulle directory toccate."""
    existing = [p for p in paths if os.path.exists(os.path.join(root, p))]
    if not existing:
        return []
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain", "--"] + existing,
            cwd=root, capture_output=True, text=True).stdout
    except OSError:
        return []
    return [l for l in out.splitlines() if l.strip()]


def run_snapshot(cfg, dry_run=False):
    targets = {}   # zone → path relativo locale
    for zone_name, zone in cfg.zones.items():
        if zone.get("sync") != "drive_master":
            continue
        if zone.get("snapshot_target") == "vault":
            targets[zone_name] = os.path.join("vault", zone_name)
        else:
            targets[zone_name] = os.path.join("company", zone_name)

    if dry_run:
        print("[dry-run] Zone da scaricare:")
        for z, t in targets.items():
            zid = cfg.zones[z].get("drive_id") or "(drive_id mancante — serve bootstrap)"
            print("  %s → %s/  [%s]" % (cfg.zones[z].get("drive_path"), t, zid))
        return 0

    try:
        drive = Drive(cfg)
    except DriveError as e:
        print("✗ snapshot non eseguibile: %s" % e)
        return 2

    manifest = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "zones": {},
    }
    for zone_name, rel_target in targets.items():
        zone = cfg.zones[zone_name]
        zid = zone.get("drive_id") or ""
        if not zid:
            print("⚠️  zona %s senza drive_id — esegui prima `osctl bootstrap`" % zone_name)
            manifest["zones"][zone_name] = {"status": "no-drive-id"}
            continue
        dest = os.path.join(cfg.root, rel_target)
        print("↓ %s → %s/" % (zone.get("drive_path"), rel_target))
        try:
            stats = drive.download_folder_tree(zid, dest)
        except Exception as e:  # una zona rotta non deve fermare le altre
            print("  ✗ errore su %s: %s" % (zone_name, e))
            manifest["zones"][zone_name] = {"status": "error", "error": str(e)}
            continue
        print("  %d file scaricati, %d saltati" % (stats["files"], stats["skipped"]))
        manifest["zones"][zone_name] = {"status": "ok", **stats}

    manifest_path = os.path.join(cfg.root, MANIFEST_REL)
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("\nManifest scritto: %s (%s)" % (MANIFEST_REL, manifest["timestamp"]))

    changes = _git_diff_summary(cfg.root, list(targets.values()) + [MANIFEST_REL])
    if changes:
        print("\nDiff rispetto a git (%d file):" % len(changes))
        for line in changes[:40]:
            print("  %s" % line)
        if len(changes) > 40:
            print("  … e altri %d" % (len(changes) - 40))
        print("\nNon committo: il commit spetta al chiamante "
              "([snapshot] drive: YYYY-MM-DD).")
    else:
        print("\nNessuna differenza rispetto a git: snapshot già allineato.")
    return 0
