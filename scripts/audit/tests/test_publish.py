"""Selftest di `osctl publish`: dry-run in sola lettura e scope `--only`.

Drive è sostituito da un finto in memoria che registra le scritture: il dry-run non ne deve
fare nessuna e deve elencare solo ciò che un run vero caricherebbe. Nessun dato reale.
"""

import contextlib
import io
import os
import shutil
import sys
import tempfile
import time
import unittest
from types import SimpleNamespace
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "osctl"))

from lib import publish  # noqa: E402
from lib.drive import FOLDER_MIME, DriveError  # noqa: E402

OLD = "2000-01-01T00:00:00Z"
NEW = "2999-01-01T00:00:00Z"


class FakeDrive:
    """Albero Drive in memoria: id → {name, mimeType, modifiedTime, parent}."""

    def __init__(self, cfg):
        self.items = {"ROOT": {"name": "", "mimeType": FOLDER_MIME, "parent": None}}
        self.writes = []
        self._n = 0

    def add(self, parent, name, folder=False, modified=OLD):
        self._n += 1
        fid = "id%d" % self._n
        self.items[fid] = {"id": fid, "name": name, "parent": parent,
                           "mimeType": FOLDER_MIME if folder else "text/markdown",
                           "modifiedTime": modified}
        return fid

    def find_child(self, parent_id, name, mime=None):
        for f in self.items.values():
            if (f.get("parent") == parent_id and f["name"] == name
                    and (mime is None or f["mimeType"] == mime)):
                return f
        return None

    def ensure_folder(self, path, parent_id=None):
        cur = parent_id or "ROOT"
        for part in [p for p in path.split("/") if p]:
            found = self.find_child(cur, part, FOLDER_MIME)
            if not found:
                self.writes.append(("mkdir", part))
                cur = self.add(cur, part, folder=True)
            else:
                cur = found["id"]
        return cur

    def upload_or_update_file(self, local_path, parent_id, name=None, mime=None):
        self.writes.append(("upload", os.path.basename(local_path)))
        return "x", "aggiornato"

    def convert_md_to_gdoc(self, md_path, parent_id, name=None):
        self.writes.append(("gdoc", os.path.basename(md_path)))
        return "x", "aggiornato"


def _write(path, text="x\n"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


class PublishTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        r = self.tmp
        _write(os.path.join(r, "zones", "_root", "CLAUDE.md"))
        _write(os.path.join(r, "zones", "_root", "context", "COMPANY.md"))
        _write(os.path.join(r, "zones", "_root", "context", "GLOSSARY.md"))
        _write(os.path.join(r, "zones", "direzione", "CLAUDE.md"))
        _write(os.path.join(r, "os", "protocols", "language.md"))
        # Seed: a.md e b.md hanno un remoto più recente, c.md no (più nuovo in locale).
        for fn in ("a.md", "b.md", "c.md"):
            _write(os.path.join(r, "company", "direzione", "sub", fn))
        self.cfg = SimpleNamespace(
            root=r, language="it", publish={},
            drive={"root_id": "ROOT"},
            zones={
                "_os": {"drive_path": "_OS", "drive_id": "OS", "sync": "git_to_drive"},
                "direzione": {"drive_path": "00-Direzione", "drive_id": "DIR",
                              "sync": "drive_master"},
            })
        self.fake = FakeDrive(self.cfg)
        self.fake.items["OS"] = {"name": "_OS", "mimeType": FOLDER_MIME, "parent": "ROOT"}
        self.fake.items["DIR"] = {"name": "00-Direzione", "mimeType": FOLDER_MIME,
                                  "parent": "ROOT"}
        sub = self.fake.add("DIR", "sub", folder=True)
        self.fake.add(sub, "a.md", modified=NEW)
        self.fake.add(sub, "b.md", modified=NEW)
        self.fake.add(sub, "c.md", modified=OLD)
        ctx = self.fake.add("ROOT", "context", folder=True)
        self.fake.add(ctx, "COMPANY.md")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _run(self, dry_run, only=None, drive=None):
        factory = (lambda cfg: drive) if drive else (lambda cfg: self.fake)
        out = io.StringIO()
        with mock.patch.object(publish, "Drive", side_effect=factory), \
                contextlib.redirect_stdout(out):
            p = publish.Publisher(self.cfg, dry_run=dry_run, only=only)
            p.run()
        return p, out.getvalue()

    def test_dry_run_reports_only_newer_seed_and_writes_nothing(self):
        p, out = self._run(dry_run=True)
        self.assertEqual(self.fake.writes, [])
        self.assertIn("c.md", out)
        self.assertNotIn("a.md", out)
        self.assertNotIn("b.md", out)
        self.assertEqual(p.count["skip"], 2)
        self.assertEqual(p.count["check"], 0)

    def test_dry_run_matches_real_run(self):
        dry, _ = self._run(dry_run=True)
        real, _ = self._run(dry_run=False)
        uploads = [w for w in self.fake.writes if w[0] == "upload"]
        self.assertEqual(dry.count["file"], len(uploads))
        self.assertEqual(dry.count["file"], real.count["file"])

    def test_dry_run_missing_remote_folder_means_upload(self):
        # Cartella `context` non ancora su Drive: il dry-run non la crea e conta l'upload.
        self.fake.items = {k: v for k, v in self.fake.items.items()
                           if v.get("name") not in ("context", "COMPANY.md")}
        p, out = self._run(dry_run=True, only=["zones/_root/context"])
        self.assertEqual(self.fake.writes, [])
        self.assertEqual(p.count["file"], 2)

    def test_dry_run_offline_marks_seed_as_check(self):
        def boom(cfg):
            raise DriveError("GDRIVE_SA_KEY_PATH non impostata")
        out = io.StringIO()
        with mock.patch.object(publish, "Drive", side_effect=boom), \
                contextlib.redirect_stdout(out):
            p = publish.Publisher(self.cfg, dry_run=True)
            p.run()
        self.assertEqual(p.count["check"], 3)
        self.assertIn("da verificare", out.getvalue())

    def test_only_scopes_to_given_paths(self):
        p, _ = self._run(dry_run=False, only=["zones/_root/context/COMPANY.md",
                                              "zones/_root/context/GLOSSARY.md"])
        self.assertEqual(sorted(self.fake.writes),
                         [("upload", "COMPANY.md"), ("upload", "GLOSSARY.md")])

    def test_only_dir_skips_company_seed(self):
        p, out = self._run(dry_run=False, only=["zones/_root"])
        names = {w[1] for w in self.fake.writes}
        self.assertEqual(names, {"CLAUDE.md", "COMPANY.md", "GLOSSARY.md"})
        self.assertNotIn("company/ seed", out)

    def test_only_rejects_missing_and_outside_paths(self):
        with mock.patch.object(publish, "Drive", side_effect=lambda cfg: self.fake):
            with self.assertRaises(DriveError):
                publish.Publisher(self.cfg, only=["zones/nope.md"])
            with self.assertRaises(DriveError):
                publish.Publisher(self.cfg, only=["../"])


if __name__ == "__main__":
    unittest.main()
