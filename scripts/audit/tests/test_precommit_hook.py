"""Regressione del pre-commit (C2): il ledger che entra nel commit è quello IN STAGE.

Clona il repo (HEAD) in una cartella temporanea, attiva `scripts/hooks` e prova a committare.
Lancio: python3 -m unittest scripts/audit/tests/test_precommit_hook.py
"""
import os
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
GOAL_GLOB = os.path.join("company", "direzione", "ops", "goals")
FAKE_AMOUNT = "Fabbisogno € " + "48" + ".500\n"


def git(cwd, *args):
    return subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                           *args], cwd=cwd, capture_output=True, text=True)


class PreCommitHookTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="precommit-test-")
        self.repo = os.path.join(self.tmp, "repo")
        r = git(ROOT, "clone", "-q", ROOT, self.repo)
        if r.returncode != 0:
            self.skipTest("clone non disponibile: " + r.stderr)
        git(self.repo, "config", "core.hooksPath", "scripts/hooks")
        goals = os.path.join(self.repo, GOAL_GLOB)
        dirs = sorted(d for d in os.listdir(goals) if os.path.isdir(os.path.join(goals, d))) \
            if os.path.isdir(goals) else []
        if not dirs:
            self.skipTest("nessun goal nel ledger")
        self.goal = os.path.join(goals, dirs[0], "GOAL.md")
        with open(self.goal, encoding="utf-8") as fh:
            self.goal_orig = fh.read()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def stage_dirty_goal_keep_clean_worktree(self):
        with open(self.goal, "a", encoding="utf-8") as fh:
            fh.write(FAKE_AMOUNT)
        git(self.repo, "add", self.goal)
        with open(self.goal, "w", encoding="utf-8") as fh:
            fh.write(self.goal_orig)

    def touch(self, rel, text):
        p = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "a", encoding="utf-8") as fh:
            fh.write(text)
        git(self.repo, "add", rel)

    def commit(self):
        return git(self.repo, "commit", "-q", "-m", "[admin] system: test")

    def test_dirty_staged_ledger_is_blocked(self):
        self.stage_dirty_goal_keep_clean_worktree()
        self.assertNotEqual(self.commit().returncode, 0)

    def test_dirty_staged_ledger_with_rule_files_is_blocked(self):
        self.stage_dirty_goal_keep_clean_worktree()
        self.touch(os.path.join("os", "org", "README.md"), "\n# nota\n")
        self.touch(os.path.join("system", "CHANGELOG.md"), "\n- nota\n")
        self.assertNotEqual(self.commit().returncode, 0)

    def _red_wo(self):
        wo_dir = os.path.join(self.repo, "company", "direzione", "ops", "wo")
        for name in sorted(os.listdir(wo_dir)):
            p = os.path.join(wo_dir, name)
            with open(p, encoding="utf-8") as fh:
                text = fh.read()
            if "output-zone: finance\n" in text and "\nto: " in text:
                return p, text
        self.skipTest("nessun WO verso la zona finance")

    def test_staged_wo_checked_against_staged_rules_not_worktree(self):
        # working tree: ACL che concede la zona finance a una persona (NON in stage)
        acl = os.path.join(self.repo, "config", "acl.yaml")
        with open(acl, encoding="utf-8") as fh:
            acl_orig = fh.read()
        with open(os.path.join(self.repo, "config", "people.yaml"), encoding="utf-8") as fh:
            people = sorted(set(re.findall(r"^  ([a-z][a-z0-9-]*):\n", fh.read(), re.M)))
        fin = re.search(r"^  finance:\n(?:    .*\n)*?    read: \[([^\]]*)\]", acl_orig, re.M)
        fin_read = {x.strip() for x in fin.group(1).split(",")} if fin else set()
        outsider = next((p for p in people if p not in fin_read and p != "admin"), None)
        if outsider is None:
            self.skipTest("nessuna persona senza ACL")
        with open(acl, "w", encoding="utf-8") as fh:
            fh.write(acl_orig.replace("read: [", "read: [%s, " % outsider))
        # in stage: un WO 🔴 verso quella persona
        p, text = self._red_wo()
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(re.sub(r"^to: .*$", "to: human:%s" % outsider, text, count=1, flags=re.M))
        git(self.repo, "add", p)
        self.assertNotEqual(self.commit().returncode, 0)

    def test_staged_rule_change_breaking_ledger_is_blocked(self):
        svc = os.path.join(self.repo, "os", "org", "services.yaml")
        with open(svc, encoding="utf-8") as fh:
            orig = fh.read()
        _, wo_text = self._red_wo()
        service = re.search(r"^service: (\S+)", wo_text, re.M).group(1).split("/")[-1]
        m = re.search(r"^  [a-z-]+/%s:\n(?:    .*\n)*?    output-zone: (finance)\n" % re.escape(service),
                      orig, re.M)
        if not m:
            self.skipTest("servizio del WO non trovato a catalogo")
        broken = orig[:m.start(1)] + "prodotto" + orig[m.end(1):]
        with open(svc, "w", encoding="utf-8") as fh:
            fh.write(broken)
        git(self.repo, "add", svc)
        with open(svc, "w", encoding="utf-8") as fh:      # working tree riportata all'originale
            fh.write(orig)
        self.touch(os.path.join("system", "CHANGELOG.md"), "\n- nota\n")
        self.assertNotEqual(self.commit().returncode, 0)

    def test_clean_rule_change_passes(self):
        self.touch(os.path.join("os", "org", "README.md"), "\n# nota\n")
        self.touch(os.path.join("system", "CHANGELOG.md"), "\n- nota\n")
        r = self.commit()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
