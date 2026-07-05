#!/usr/bin/env python3
"""osctl — sync engine CompanyOS: git (sistema) ↔ Google Drive (operativo).

Comandi:
  osctl bootstrap   crea l'albero Drive da config/acl.yaml, imposta le ACL e
                    scrive i drive_id nel config (idempotente; DRY-RUN di
                    default, usa --apply per eseguire davvero)
  osctl publish     git → Drive: zone CLAUDE.md, os/, viewer, company/ seed
  osctl snapshot    Drive → git: zone drive_master in company/ (+vault/), manifest
  osctl acl-audit   permessi Drive reali vs matrice attesa (exit 1 se drift critico);
                    --fix calcola le correzioni (dry-run, --apply per eseguirle)
  osctl status      stato config, env e dipendenze (funziona sempre, senza Drive)

Requisiti Drive: google-api-python-client + service account (GDRIVE_SA_KEY_PATH).
`status` e i parser funzionano anche senza. Messaggi in italiano.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.config import Config, ConfigError  # noqa: E402


# ---------------------------------------------------------------------------
# bootstrap
# ---------------------------------------------------------------------------

def _write_drive_ids(acl_path, zone_ids):
    """Riscrive i `drive_id:` di acl.yaml preservando il resto del file.

    Edit testuale line-based (niente dump YAML: manterrebbe male i commenti).
    """
    with open(acl_path, encoding="utf-8") as fh:
        lines = fh.readlines()
    current_zone = None
    out = []
    for line in lines:
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        if indent == 2 and stripped.endswith(":") and not stripped.startswith("#"):
            current_zone = stripped[:-1]
        if (indent == 4 and stripped.startswith("drive_id:")
                and current_zone in zone_ids):
            line = '    drive_id: "%s"\n' % zone_ids[current_zone]
        out.append(line)
    with open(acl_path, "w", encoding="utf-8") as fh:
        fh.writelines(out)


def cmd_bootstrap(cfg, args):
    dry = not args.apply
    if dry:
        print("[dry-run] Bootstrap (usa --apply per eseguire davvero)\n")
    print("== Albero Drive da config/acl.yaml ==")
    plan = []
    for zone_name, zone in cfg.zones.items():
        expected = cfg.zone_expected_acl(zone_name)
        plan.append((zone_name, zone, expected))
        print("  %-15s %-16s write=%d read-only=%d %s" % (
            zone_name, zone.get("drive_path", ""),
            sum(1 for r in expected.values() if r == "writer"),
            sum(1 for r in expected.values() if r == "reader"),
            "(drive_id già presente)" if zone.get("drive_id") else ""))
        for email, role in sorted(expected.items()):
            print("      %-8s %s" % (role, email))
        for sub_name, sub in (zone.get("subfolders") or {}).items():
            sub_expected = cfg.zone_expected_acl(sub_name, node=sub)
            print("    └ %s/" % sub_name)
            for email, role in sorted(sub_expected.items()):
                print("      %-8s %s" % (role, email))
    if dry:
        print("\n[dry-run] Nessuna modifica fatta. Prerequisiti per --apply:")
        print("  - Shared Drive creato e condiviso col service account (Content manager)")
        print("  - drive.root_id compilato in config/acl.yaml")
        print("  - GDRIVE_SA_KEY_PATH esportata")
        return 0

    from lib.drive import Drive, DriveError, FOLDER_MIME
    try:
        drive = Drive(cfg)
    except DriveError as e:
        print("✗ bootstrap non eseguibile: %s" % e)
        return 2

    zone_ids = {}
    for zone_name, zone, expected in plan:
        fid = zone.get("drive_id") or drive.ensure_folder(zone.get("drive_path"))
        zone_ids[zone_name] = fid
        print("  ✓ %s → %s" % (zone.get("drive_path"), fid))
        existing = {(p.get("emailAddress") or "").lower()
                    for p in drive.list_permissions(fid) if p.get("type") == "user"}
        for email, role in expected.items():
            if email not in existing:
                drive.set_permission(fid, email, role)
                print("    + %s %s" % (role, email))
        for sub_name, sub in (zone.get("subfolders") or {}).items():
            sub_id = drive.ensure_folder(sub_name, fid)
            print("  ✓ %s/%s → %s" % (zone.get("drive_path"), sub_name, sub_id))
            sub_existing = {(p.get("emailAddress") or "").lower()
                            for p in drive.list_permissions(sub_id)
                            if p.get("type") == "user"}
            for email, role in cfg.zone_expected_acl(sub_name, node=sub).items():
                if email not in sub_existing:
                    drive.set_permission(sub_id, email, role)
                    print("    + %s %s" % (role, email))

    acl_path = os.path.join(cfg.root, "config", "acl.yaml")
    _write_drive_ids(acl_path, zone_ids)
    print("\n✓ drive_id scritti in config/acl.yaml — ricorda di committare.")
    return 0


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

def cmd_status(cfg, args):
    print("== osctl status ==\n")

    print("Config:")
    print("  zone definite: %d (%s)" % (len(cfg.zones), ", ".join(cfg.zones)))
    with_id = [z for z, v in cfg.zones.items() if v.get("drive_id")]
    print("  drive_id compilati: %d/%d %s" % (
        len(with_id), len(cfg.zones),
        "— esegui `osctl bootstrap`" if len(with_id) < len(cfg.zones) else ""))
    print("  root Drive: %s (shared_drive=%s)" % (
        cfg.drive.get("root_id") or "(vuoto — vedi bootstrap/README.md)",
        cfg.drive.get("shared_drive")))

    print("\nPersone (people.yaml):")
    for key, p in cfg.people.items():
        emails = cfg.emails_for(key)
        flag = emails[0] if emails else "⚠️  senza email (saltata nelle ACL)"
        print("  %-15s %-10s %s" % (key, (p or {}).get("type", "?"), flag))

    print("\nDipendenze:")
    try:
        import yaml  # noqa: F401
        print("  PyYAML: ✓")
    except ImportError:
        print("  PyYAML: assente (uso il parser minimale incluso)")
    try:
        import googleapiclient  # noqa: F401
        print("  google-api-python-client: ✓")
    except ImportError:
        print("  google-api-python-client: ✗ — pip install google-api-python-client google-auth")

    key_path = os.environ.get("GDRIVE_SA_KEY_PATH", "")
    if key_path and os.path.isfile(key_path):
        print("  GDRIVE_SA_KEY_PATH: ✓ (%s)" % key_path)
    elif key_path:
        print("  GDRIVE_SA_KEY_PATH: impostata ma il file non esiste (%s)" % key_path)
    else:
        print("  GDRIVE_SA_KEY_PATH: non impostata")

    manifest = os.path.join(cfg.root, "company", ".snapshot-manifest.json")
    if os.path.isfile(manifest):
        try:
            with open(manifest, encoding="utf-8") as fh:
                data = json.load(fh)
            print("\nUltimo snapshot: %s" % data.get("timestamp", "?"))
        except (OSError, ValueError):
            print("\nUltimo snapshot: manifest illeggibile")
    else:
        print("\nUltimo snapshot: mai eseguito (manca company/.snapshot-manifest.json)")

    for w in cfg.warnings:
        print("⚠️  %s" % w)
    return 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="osctl", description="Sync engine CompanyOS (git ↔ Drive)")
    ap.add_argument("--repo", help="radice del repo (default: autodetect)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("bootstrap", help="crea albero Drive + ACL (dry-run di default)")
    p.add_argument("--dry-run", action="store_true", help="(default) mostra solo il piano")
    p.add_argument("--apply", action="store_true", help="esegue davvero le modifiche")

    p = sub.add_parser("publish", help="git → Drive")
    p.add_argument("--dry-run", action="store_true")

    p = sub.add_parser("snapshot", help="Drive → git (non committa)")
    p.add_argument("--dry-run", action="store_true")

    p = sub.add_parser("acl-audit", help="drift permessi Drive vs matrice")
    p.add_argument("--fix", action="store_true", help="calcola le correzioni (dry-run)")
    p.add_argument("--apply", action="store_true", help="con --fix: applica le correzioni")
    p.add_argument("--dry-run", action="store_true")

    p = sub.add_parser("status", help="stato config/env (non richiede Drive)")
    p.add_argument("--dry-run", action="store_true")

    args = ap.parse_args(argv)

    try:
        cfg = Config(repo_root=args.repo)
    except ConfigError as e:
        print("✗ errore di config: %s" % e)
        return 2

    if args.cmd == "bootstrap":
        if args.dry_run:
            args.apply = False
        return cmd_bootstrap(cfg, args)
    if args.cmd == "publish":
        from lib.publish import run_publish
        return run_publish(cfg, dry_run=args.dry_run)
    if args.cmd == "snapshot":
        from lib.snapshot import run_snapshot
        return run_snapshot(cfg, dry_run=args.dry_run)
    if args.cmd == "acl-audit":
        from lib.acl_audit import run_acl_audit
        apply_fix = args.fix and args.apply and not args.dry_run
        return run_acl_audit(cfg, fix=args.fix, apply_fix=apply_fix)
    if args.cmd == "status":
        return cmd_status(cfg, args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
