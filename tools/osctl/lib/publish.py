"""publish.py — git → Drive (osctl publish).

Cosa pubblica:
  1. zones/_root/*                      → root del Drive (CLAUDE.md kernel + context/)
  2. zones/{zona}/CLAUDE.md             → cartella della zona
  3. os/{agents,protocols,workflows,templates} + tools/viewer/viewer.html → _OS/
  4. company/{zona}/** (seed)           → cartella della zona, SOLO se il file
     locale è più nuovo del remoto (le zone drive_master hanno il master su Drive)

I .md con frontmatter `render: gdoc`, o con `type:` incluso in
publish.gdoc_default_for, generano ANCHE un Google Doc accanto al .md.
"""

import os
import re

from .drive import Drive, DriveError, parse_rfc3339

FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def read_frontmatter(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            head = fh.read(4000)
    except OSError:
        return {}
    m = FM_RE.match(head)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.strip().startswith("#"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip("\"'")
    return fm


def wants_gdoc(cfg, path):
    pub = cfg.publish
    if not pub.get("gdoc_render"):
        return False
    fm = read_frontmatter(path)
    if fm.get("render") == "gdoc":
        return True
    return fm.get("type") in (pub.get("gdoc_default_for") or [])


class Publisher:
    def __init__(self, cfg, dry_run=False):
        self.cfg = cfg
        self.dry = dry_run
        self.drive = None if dry_run else Drive(cfg)
        self.count = {"file": 0, "gdoc": 0, "skip": 0}
        self._folder_cache = {}

    def _zone_folder(self, zone_name):
        """ID cartella Drive della zona (drive_id da acl.yaml o ensure_folder)."""
        if zone_name in self._folder_cache:
            return self._folder_cache[zone_name]
        zone = self.cfg.zones[zone_name]
        fid = zone.get("drive_id") or ""
        if not fid:
            if self.dry:
                fid = "(da creare: %s)" % zone.get("drive_path")
            else:
                fid = self.drive.ensure_folder(zone.get("drive_path"))
        self._folder_cache[zone_name] = fid
        return fid

    def _put(self, local, folder_id, rel_label, name=None):
        # Varianti lingua (os/protocols/language.md): i file `.en.md` non si pubblicano
        # come entità a sé; con language=en sostituiscono il contenuto del file base.
        if local.endswith(".en.md"):
            self.count["skip"] += 1
            return
        if self.cfg.language == "en" and local.endswith(".md"):
            variant = local[:-3] + ".en.md"
            if os.path.isfile(variant):
                name = name or os.path.basename(local)
                local = variant
        if self.dry:
            print("  [dry-run] %s → %s" % (local, rel_label))
        else:
            _, action = self.drive.upload_or_update_file(local, folder_id, name=name)
            print("  ✓ %s → %s (%s)" % (local, rel_label, action))
        self.count["file"] += 1
        if local.endswith(".md") and wants_gdoc(self.cfg, local):
            if self.dry:
                print("  [dry-run] %s → Google Doc in %s" % (local, rel_label))
            else:
                _, action = self.drive.convert_md_to_gdoc(local, folder_id)
                print("    ↳ Google Doc (%s)" % action)
            self.count["gdoc"] += 1

    def _put_tree(self, local_dir, folder_id, rel_label, only_newer=False):
        """Pubblica ricorsivamente una directory locale in una cartella Drive."""
        for root, dirs, files in os.walk(local_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            rel = os.path.relpath(root, local_dir)
            if self.dry:
                sub_id = folder_id
            else:
                sub_id = (folder_id if rel == "." else
                          self.drive.ensure_folder(rel.replace(os.sep, "/"), folder_id))
            for fn in sorted(files):
                if fn.startswith("."):
                    continue
                local = os.path.join(root, fn)
                label = os.path.join(rel_label, "" if rel == "." else rel, fn)
                if only_newer and not self.dry:
                    remote = self.drive.find_child(sub_id, fn)
                    if remote and os.path.getmtime(local) <= parse_rfc3339(
                            remote.get("modifiedTime")):
                        self.count["skip"] += 1
                        continue
                self._put(local, sub_id, label)

    # -- fasi -----------------------------------------------------------------

    def publish_root(self):
        src = os.path.join(self.cfg.root, "zones", "_root")
        if not os.path.isdir(src):
            return
        print("\n== zones/_root → root Drive ==")
        root_id = self.cfg.drive.get("root_id") or "(root)"
        self._put_tree(src, root_id, "/")

    def publish_zone_claudemd(self):
        print("\n== zones/{zona}/CLAUDE.md → cartelle zona ==")
        zdir = os.path.join(self.cfg.root, "zones")
        for zone_name, zone in self.cfg.zones.items():
            local = os.path.join(zdir, zone_name, "CLAUDE.md")
            if not os.path.isfile(local):
                continue
            fid = self._zone_folder(zone_name)
            self._put(local, fid, "%s/CLAUDE.md" % zone.get("drive_path"))

    def publish_os(self):
        print("\n== os/ + viewer → _OS/ ==")
        os_id = self._zone_folder("_os")
        for sub in ("agents", "protocols", "workflows", "templates"):
            local = os.path.join(self.cfg.root, "os", sub)
            if not os.path.isdir(local):
                continue
            if self.dry:
                sub_id = os_id
            else:
                sub_id = self.drive.ensure_folder(sub, os_id)
            self._put_tree(local, sub_id, "_OS/%s" % sub)
        viewer = os.path.join(self.cfg.root, "tools", "viewer", "viewer.html")
        if os.path.isfile(viewer):
            self._put(viewer, os_id, "_OS/viewer.html")

    def publish_company_seed(self):
        print("\n== company/ seed → zone (solo file più nuovi del remoto) ==")
        cdir = os.path.join(self.cfg.root, "company")
        for zone_name, zone in self.cfg.zones.items():
            local = os.path.join(cdir, zone_name)
            if not os.path.isdir(local) or zone.get("sync") != "drive_master":
                continue
            fid = self._zone_folder(zone_name)
            self._put_tree(local, fid, zone.get("drive_path", zone_name), only_newer=True)

    def run(self):
        self.publish_root()
        self.publish_zone_claudemd()
        self.publish_os()
        self.publish_company_seed()
        print("\nPublish completato: %(file)d file, %(gdoc)d Google Doc, "
              "%(skip)d saltati (remoto più recente)." % self.count)


def run_publish(cfg, dry_run=False):
    try:
        Publisher(cfg, dry_run=dry_run).run()
    except DriveError as e:
        print("✗ publish non eseguibile: %s" % e)
        return 2
    return 0
