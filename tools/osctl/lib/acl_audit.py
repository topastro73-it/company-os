"""acl_audit.py — confronta i permessi Drive reali con la matrice attesa.

Matrice attesa: config/acl.yaml (write/read per zona e sottocartella) risolta
in email via config/people.yaml. Report di drift:

  - persona IN PIÙ rispetto alla matrice  → 🔴 CRITICO (exit code 1)
  - persona IN MENO                        → 🟡 warning
  - cartella cliente senza ACL esplicita   → 🟡 warning (zona per_folder_acl)

`--fix` calcola le correzioni (aggiungi mancanti / rimuovi extra); di default
è dry-run — serve `--apply` per eseguirle davvero.
"""

from .drive import Drive, DriveError, FOLDER_MIME, sa_client_email

# Ruoli Drive equivalenti a "writer" nella nostra matrice.
WRITERISH = {"writer", "fileOrganizer", "organizer", "owner"}


def _actual_users(perms):
    """{email_lower: role} dai permessi Drive (solo type=user, non ereditati)."""
    out = {}
    for p in perms:
        if p.get("type") != "user" or not p.get("emailAddress"):
            continue
        role = "writer" if p.get("role") in WRITERISH else "reader"
        out[p["emailAddress"].lower()] = {"role": role, "perm_id": p.get("id")}
    return out


class AclAudit:
    def __init__(self, cfg, fix=False, apply_fix=False):
        self.cfg = cfg
        self.fix = fix
        self.apply = apply_fix
        self.drive = Drive(cfg)
        self.sa_email = sa_client_email()
        self.critical = 0
        self.warnings = 0

    def _audit_folder(self, label, folder_id, expected):
        actual = _actual_users(self.drive.list_permissions(folder_id))
        actual.pop(self.sa_email, None)  # il service account non conta come drift
        extra = sorted(set(actual) - set(expected))
        missing = sorted(set(expected) - set(actual))
        wrong = sorted(e for e in set(actual) & set(expected)
                       if actual[e]["role"] != expected[e])

        if not (extra or missing or wrong):
            print("  🟢 %s: ACL allineata (%d persone)" % (label, len(expected)))
            return

        for e in extra:
            print("  🔴 %s: %s ha accesso (%s) ma NON è nella matrice — CRITICO"
                  % (label, e, actual[e]["role"]))
            self.critical += 1
            if self.fix:
                if self.apply:
                    self.drive.remove_permission(folder_id, actual[e]["perm_id"])
                    print("       → permesso rimosso")
                else:
                    print("       → [dry-run] rimuoverei il permesso (usa --apply)")
        for e in missing:
            print("  🟡 %s: %s atteso come %s ma assente su Drive"
                  % (label, e, expected[e]))
            self.warnings += 1
            if self.fix:
                if self.apply:
                    self.drive.set_permission(folder_id, e, expected[e])
                    print("       → permesso creato (%s)" % expected[e])
                else:
                    print("       → [dry-run] darei %s (usa --apply)" % expected[e])
        for e in wrong:
            print("  🟡 %s: %s è %s ma la matrice prevede %s"
                  % (label, e, actual[e]["role"], expected[e]))
            self.warnings += 1

    def _audit_client_folders(self, zone_name, zone):
        """Zona per_folder_acl (clienti): ogni sottocartella deve avere almeno
        una ACL utente esplicita (l'owner del cliente)."""
        zid = zone.get("drive_id") or ""
        if not zid:
            return
        for child in self.drive.list_children(zid):
            if child["mimeType"] != FOLDER_MIME:
                continue
            perms = _actual_users(self.drive.list_permissions(child["id"]))
            perms.pop(self.sa_email, None)
            if not perms:
                print("  🟡 %s/%s: cartella cliente senza ACL esplicita "
                      "(nessun owner assegnato)" % (zone.get("drive_path"), child["name"]))
                self.warnings += 1

    def run(self):
        print("== ACL audit: Drive vs config/acl.yaml + people.yaml ==\n")
        audited = 0
        for zone_name, zone in self.cfg.zones.items():
            zid = zone.get("drive_id") or ""
            if not zid:
                print("  ⚪ %s: drive_id mancante — esegui `osctl bootstrap`" % zone_name)
                continue
            audited += 1
            expected = self.cfg.zone_expected_acl(zone_name)
            self._audit_folder(zone.get("drive_path", zone_name), zid, expected)

            for sub_name, sub in (zone.get("subfolders") or {}).items():
                sub_folder = self.drive.find_child(zid, sub_name, FOLDER_MIME)
                label = "%s/%s" % (zone.get("drive_path"), sub_name)
                if not sub_folder:
                    print("  🟡 %s: sottocartella attesa ma assente su Drive" % label)
                    self.warnings += 1
                    continue
                self._audit_folder(label, sub_folder["id"],
                                   self.cfg.zone_expected_acl(sub_name, node=sub))

            if zone.get("per_folder_acl"):
                self._audit_client_folders(zone_name, zone)

        print("\nRiepilogo: %d zone verificate · %d 🔴 critici · %d 🟡 warning"
              % (audited, self.critical, self.warnings))
        if self.critical:
            print("🔴 Drift critico: persone con accesso non previsto dalla matrice.")
            return 1
        return 0


def run_acl_audit(cfg, fix=False, apply_fix=False):
    try:
        return AclAudit(cfg, fix=fix, apply_fix=apply_fix).run()
    except DriveError as e:
        print("✗ acl-audit non eseguibile: %s" % e)
        return 2
