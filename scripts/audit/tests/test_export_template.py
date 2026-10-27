"""Selftest di `osctl export-template`: marker d'istanza, merge con le varianti, leak-scan.

Costruisce in una cartella temporanea una sorgente e un clone di template finti e lancia lo
script vero via subprocess, come in uso reale. Nessun dato reale nei fixture.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OSCTL = os.path.join(ROOT, "tools", "osctl", "osctl.py")
sys.path.insert(0, os.path.join(ROOT, "tools", "osctl"))

from lib.export_template import strip_instance  # noqa: E402

EXPORT_YAML = """target: "../tpl"
include:
  - os
exclude:
  - "os/private-*.md"
template_owned:
  - "os/owned.md"
deny_terms:
  - "Acmecorp"
allow_terms: []
"""


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


# Il marker si compone a runtime: scritto per intero, questo file verrebbe filtrato dall'export.
M = "@" + "instance"


class StripInstance(unittest.TestCase):
    def test_line_and_block(self):
        text = ("a\nb <!-- %s -->\n<!-- %s-begin -->\nc\n<!-- %s-end -->\n"
                "d  # %s\ne // %s\nf\n") % ((M,) * 5)
        self.assertEqual(strip_instance(text), "a\nf\n")

    def test_marker_outside_comment_is_text(self):
        text = 'MARK = "%s-begin"\nsi marca con `%s`\n' % (M, M)
        self.assertEqual(strip_instance(text), text)

    def test_unclosed_block_fails(self):
        with self.assertRaises(ValueError):
            strip_instance("<!-- %s-begin -->\nx\n" % M)


class ExportRun(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.src = os.path.join(self.tmp, "src")
        self.tpl = os.path.join(self.tmp, "tpl")
        _write(os.path.join(self.src, "config", "export.yaml"), EXPORT_YAML)
        _write(os.path.join(self.src, "config", "company.yaml"), "company:\n  short_name: Zetaco\n")
        _write(os.path.join(self.src, "config", "people.yaml"), "people:\n  p1:\n    name: Mario Esempio\n")
        _write(os.path.join(self.src, "config", "acl.yaml"), "zones: {}\n")
        _write(os.path.join(self.src, "CLAUDE.md"), "x\n")
        _write(os.path.join(self.src, "os", "a.md"), "comune\nsolo qui <!-- %s -->\n" % M)
        _write(os.path.join(self.src, "os", "private-x.md"), "Zetaco\n")
        _write(os.path.join(self.src, "os", "owned.md"), "versione istanza\n")
        _write(os.path.join(self.tpl, "os", "a.md"), "vecchio\n")
        _write(os.path.join(self.tpl, "os", "a.en.md"), "old\n")
        _write(os.path.join(self.tpl, "os", "gone.md"), "rimosso alla sorgente\n")
        _write(os.path.join(self.tpl, "os", "gone.en.md"), "removed\n")
        _write(os.path.join(self.tpl, "os", "owned.md"), "versione template\n")
        subprocess.run(["git", "init", "-q", self.tpl], check=True)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _run(self, *args):
        return subprocess.run([sys.executable, OSCTL, "--repo", self.src, "export-template"] + list(args),
                              capture_output=True, text=True)

    def test_dry_run_writes_nothing(self):
        r = self._run()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(open(os.path.join(self.tpl, "os", "a.md")).read(), "vecchio\n")
        self.assertIn("os/a.en.md", r.stdout)  # da ritradurre

    def test_apply_is_a_merge(self):
        r = self._run("--apply")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        t = lambda *p: os.path.join(self.tpl, *p)  # noqa: E731
        self.assertEqual(open(t("os", "a.md")).read(), "comune\n")
        self.assertTrue(os.path.exists(t("os", "a.en.md")))        # variante mai cancellata
        self.assertFalse(os.path.exists(t("os", "gone.md")))       # base sparito alla sorgente
        self.assertFalse(os.path.exists(t("os", "gone.en.md")))    # sua variante orfana
        self.assertFalse(os.path.exists(t("os", "private-x.md")))  # escluso
        self.assertEqual(open(t("os", "owned.md")).read(), "versione template\n")

    def test_leak_blocks(self):
        _write(os.path.join(self.src, "os", "b.md"), "cliente di Zetaco\n")
        r = self._run()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("os/b.md", r.stdout)


if __name__ == "__main__":
    unittest.main()
