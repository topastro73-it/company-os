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

from .drive import FOLDER_MIME, Drive, DriveError, parse_rfc3339

FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

# Cartelle di build/dipendenze: artefatti locali, mai contenuto di zona.
SKIP_DIRS = {"node_modules", "__pycache__", "venv", "dist", "build"}


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
    """Pubblica git → Drive.

    dry_run: nessuna scrittura su Drive. Se la chiave del service account è
    disponibile, il dry-run interroga Drive in sola lettura (find_child +
    modifiedTime) e riporta esattamente cosa caricherebbe un run vero; senza
    chiave degrada a "da verificare" per i file del seed (non può confrontare).

    only: lista di path repo-relativi (file o cartelle). Se presente si pubblica
    solo ciò che vi sta sotto; le fasi e le sottocartelle fuori scope non
    vengono nemmeno visitate (niente query né ensure_folder).
    """

    def __init__(self, cfg, dry_run=False, only=None):
        self.cfg = cfg
        self.dry = dry_run
        self.only = [self._norm(p) for p in only] if only else None
        self.drive = None
        self.offline = False
        if dry_run:
            try:
                self.drive = Drive(cfg)
            except DriveError as e:
                self.offline = True
                print("[dry-run] Drive non raggiungibile (%s)" % str(e).splitlines()[0])
                print("[dry-run] modalità offline: i file del seed company/ risultano "
                      "'da verificare', non 'da caricare'.")
        else:
            self.drive = Drive(cfg)
        self.count = {"file": 0, "gdoc": 0, "skip": 0, "check": 0}
        self._folder_cache = {}

    # -- scope (--only) --------------------------------------------------------

    def _norm(self, path):
        absp = os.path.abspath(path if os.path.isabs(path)
                               else os.path.join(self.cfg.root, path))
        rel = os.path.relpath(absp, self.cfg.root).replace(os.sep, "/")
        if rel == ".." or rel.startswith("../"):
            raise DriveError("--only %s: fuori dal repo" % path)
        if not os.path.exists(absp):
            raise DriveError("--only %s: path inesistente" % path)
        return "" if rel == "." else rel.rstrip("/")

    def _rel(self, local):
        rel = os.path.relpath(local, self.cfg.root).replace(os.sep, "/")
        return "" if rel == "." else rel

    def _in_scope(self, local):
        """Il file (o la cartella) `local` è dentro uno dei path di --only?"""
        if self.only is None:
            return True
        rel = self._rel(local)
        return any(p == "" or rel == p or rel.startswith(p + "/") for p in self.only)

    def _touches(self, local_dir):
        """La cartella `local_dir` contiene, o sta dentro, un path di --only?"""
        if self.only is None:
            return True
        rel = self._rel(local_dir)
        return any(p == "" or rel == "" or rel == p or rel.startswith(p + "/")
                   or p.startswith(rel + "/") for p in self.only)

    # -- cartelle --------------------------------------------------------------

    def _folder(self, path, parent_id):
        """ID della sottocartella `path` sotto `parent_id`.

        Run vero: ensure_folder (la crea se manca). Dry-run: solo lettura;
        None se la cartella (o il parent) non esiste ancora, o se offline.
        """
        if not self.dry:
            return self.drive.ensure_folder(path, parent_id)
        if self.offline or not parent_id:
            return None
        cur = parent_id
        for part in [p for p in path.split("/") if p]:
            found = self.drive.find_child(cur, part, FOLDER_MIME)
            if not found:
                return None
            cur = found["id"]
        return cur

    def _zone_folder(self, zone_name):
        """ID cartella Drive della zona (drive_id da acl.yaml o ensure_folder)."""
        if zone_name in self._folder_cache:
            return self._folder_cache[zone_name]
        zone = self.cfg.zones[zone_name]
        fid = zone.get("drive_id") or ""
        if not fid:
            fid = self._folder(zone.get("drive_path"), self.cfg.drive.get("root_id"))
        self._folder_cache[zone_name] = fid
        return fid

    # -- file ------------------------------------------------------------------

    def _put(self, local, folder_id, rel_label, name=None, variants=True):
        if not self._in_scope(local):
            return
        # Varianti lingua (os/protocols/language.md): i file `.en.md` non si pubblicano
        # come entità a sé; con language=en sostituiscono il contenuto del file base.
        # Vale solo per i file di sistema: in company/ un `.en.md` è un documento a sé.
        if variants and local.endswith(".en.md"):
            self.count["skip"] += 1
            return
        if variants and self.cfg.language == "en" and local.endswith(".md"):
            variant = local[:-3] + ".en.md"
            if os.path.isfile(variant):
                name = name or os.path.basename(local)
                local = variant
        if self.dry:
            print("  [dry-run] carica %s → %s" % (local, rel_label))
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

    def _put_tree(self, local_dir, folder_id, rel_label, only_newer=False, variants=True):
        """Pubblica ricorsivamente una directory locale in una cartella Drive."""
        if not self._touches(local_dir):
            return
        sub_ids = {".": folder_id}
        for root, dirs, files in os.walk(local_dir):
            dirs[:] = [d for d in dirs
                       if not d.startswith(".") and d not in SKIP_DIRS
                       and self._touches(os.path.join(root, d))]
            rel = os.path.relpath(root, local_dir)
            if rel not in sub_ids:
                parent = sub_ids[os.path.dirname(rel) or "."]
                sub_ids[rel] = (self._folder(os.path.basename(rel), parent)
                                if parent else None)
            sub_id = sub_ids[rel]
            for fn in sorted(files):
                if fn.startswith("."):
                    continue
                local = os.path.join(root, fn)
                if not self._in_scope(local):
                    continue
                label = os.path.join(rel_label, "" if rel == "." else rel, fn)
                if only_newer:
                    if self.dry and self.offline:
                        print("  [dry-run] da verificare %s → %s (offline)" % (local, label))
                        self.count["check"] += 1
                        continue
                    remote = self.drive.find_child(sub_id, fn) if sub_id else None
                    if remote and os.path.getmtime(local) <= parse_rfc3339(
                            remote.get("modifiedTime")):
                        self.count["skip"] += 1
                        continue
                self._put(local, sub_id, label, variants=variants)

    # -- fasi -----------------------------------------------------------------

    def publish_root(self):
        src = os.path.join(self.cfg.root, "zones", "_root")
        if not os.path.isdir(src) or not self._touches(src):
            return
        print("\n== zones/_root → root Drive ==")
        root_id = self.cfg.drive.get("root_id") or "(root)"
        self._put_tree(src, root_id, "/")

    def publish_zone_claudemd(self):
        zdir = os.path.join(self.cfg.root, "zones")
        todo = [(n, z, os.path.join(zdir, n, "CLAUDE.md")) for n, z in self.cfg.zones.items()]
        todo = [t for t in todo if os.path.isfile(t[2]) and self._in_scope(t[2])]
        if not todo:
            return
        print("\n== zones/{zona}/CLAUDE.md → cartelle zona ==")
        for zone_name, zone, local in todo:
            fid = self._zone_folder(zone_name)
            self._put(local, fid, "%s/CLAUDE.md" % zone.get("drive_path"))

    def publish_os(self):
        subs = [(sub, os.path.join(self.cfg.root, "os", sub))
                for sub in ("agents", "protocols", "workflows", "templates", "skills")]
        subs = [(s, d) for s, d in subs if os.path.isdir(d) and self._touches(d)]
        viewer = os.path.join(self.cfg.root, "tools", "viewer", "viewer.html")
        do_viewer = os.path.isfile(viewer) and self._in_scope(viewer)
        if not subs and not do_viewer:
            return
        print("\n== os/ + viewer → _OS/ ==")
        os_id = self._zone_folder("_os")
        for sub, local in subs:
            sub_id = self._folder(sub, os_id) if os_id else None
            self._put_tree(local, sub_id, "_OS/%s" % sub)
        if do_viewer:
            self._put(viewer, os_id, "_OS/viewer.html")

    def publish_company_seed(self):
        cdir = os.path.join(self.cfg.root, "company")
        todo = [(n, z, os.path.join(cdir, n)) for n, z in self.cfg.zones.items()
                if z.get("sync") == "drive_master"]
        todo = [t for t in todo if os.path.isdir(t[2]) and self._touches(t[2])]
        if not todo:
            return
        print("\n== company/ seed → zone (solo file più nuovi del remoto) ==")
        for zone_name, zone, local in todo:
            fid = self._zone_folder(zone_name)
            self._put_tree(local, fid, zone.get("drive_path", zone_name), only_newer=True,
                           variants=False)

    def run(self):
        if self.only is not None:
            print("Scope (--only): %s" % ", ".join(p or "." for p in self.only))
        self.publish_root()
        self.publish_zone_claudemd()
        self.publish_os()
        self.publish_company_seed()
        if self.dry:
            msg = ("\n[dry-run] Nessuna scrittura su Drive. Un publish vero caricherebbe "
                   "%(file)d file e %(gdoc)d Google Doc; %(skip)d saltati (remoto più "
                   "recente o variante lingua)." % self.count)
            if self.count["check"]:
                msg += (" %(check)d file del seed da verificare (offline: senza chiave "
                        "non si confronta il modifiedTime)." % self.count)
            print(msg)
        else:
            print("\nPublish completato: %(file)d file, %(gdoc)d Google Doc, "
                  "%(skip)d saltati (remoto più recente o variante lingua)." % self.count)
        if self.only is not None and not (self.count["file"] or self.count["skip"]
                                          or self.count["check"]):
            print("⚠ --only non corrisponde a nessun file pubblicabile "
                  "(zones/, os/, tools/viewer/viewer.html, company/{zona drive_master}/).")


def run_publish(cfg, dry_run=False, only=None):
    try:
        Publisher(cfg, dry_run=dry_run, only=only).run()
    except DriveError as e:
        print("✗ publish non eseguibile: %s" % e)
        return 2
    return 0
